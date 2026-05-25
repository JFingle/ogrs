package com.openrsc.server.plugins.custom.guilds;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * OGRS — in-memory guild storage + lifecycle. Phase 2-α of the
 * housing/contract arc (sparky 2026-05-24). Mirrors ContractRegistry's
 * static-map-with-locks pattern.
 *
 * Constraints:
 *   - Guild name uniqueness (case-insensitive).
 *   - A player can only belong to ONE guild at a time.
 *   - Founder cannot leave or be kicked — they have to disband or
 *     transfer leadership first (transfer command lands in 2-β).
 *   - Min member count to form: 1 (founder); min recruits to access
 *     wilderness estates: 5 (gated when 1F-wilderness lands).
 *
 * Costs (gold sinks):
 *   - Creation fee: 100,000gp paid up front from founder's inventory.
 *     Caller (GuildCommands) enforces; this registry just creates.
 *
 * In-memory only — guilds lost on restart for v1. DB persistence in
 * Phase 2-β.
 */
public final class GuildRegistry {

	private static final Map<Integer, Guild> GUILDS = new HashMap<>();
	private static final Map<String, Integer> NAME_TO_ID = new HashMap<>();     // lowercase name -> id
	private static final Map<String, Integer> MEMBER_TO_GUILD = new HashMap<>(); // lowercase username -> id
	private static final AtomicInteger NEXT_ID = new AtomicInteger(1);

	private GuildRegistry() {}

	// ─── Create / Lookup ─────────────────────────────────────────────

	public static synchronized Guild create(final String name, final String founderUsername) {
		final String key = name.toLowerCase();
		if (NAME_TO_ID.containsKey(key)) return null;  // name taken
		if (MEMBER_TO_GUILD.containsKey(founderUsername.toLowerCase())) return null; // already in a guild
		final Guild g = new Guild(NEXT_ID.getAndIncrement(), name, founderUsername);
		GUILDS.put(g.id, g);
		NAME_TO_ID.put(key, g.id);
		MEMBER_TO_GUILD.put(founderUsername.toLowerCase(), g.id);
		return g;
	}

	public static synchronized Guild byName(final String name) {
		final Integer id = NAME_TO_ID.get(name.toLowerCase());
		return id == null ? null : GUILDS.get(id);
	}

	public static synchronized Guild byMember(final String username) {
		final Integer id = MEMBER_TO_GUILD.get(username.toLowerCase());
		return id == null ? null : GUILDS.get(id);
	}

	public static synchronized List<Guild> listAll() {
		return new ArrayList<>(GUILDS.values());
	}

	// ─── Invite / Accept / Leave / Kick ──────────────────────────────

	/** Inviter must be FOUNDER or OFFICER. Invitee must not already be
	 *  in a guild. Sets a pending invite; invitee accepts via accept(). */
	public static synchronized boolean invite(final Guild g, final String inviterUsername,
	                                          final String inviteeUsername) {
		final Guild.Role role = g.roleOf(inviterUsername);
		if (role == null || !role.canInviteOrKick()) return false;
		if (MEMBER_TO_GUILD.containsKey(inviteeUsername.toLowerCase())) return false;
		g.pendingInvites.put(inviteeUsername.toLowerCase(), inviterUsername);
		return true;
	}

	/** Invitee accepts a pending invite. Joins as RECRUIT. */
	public static synchronized Guild accept(final String inviteeUsername) {
		final String key = inviteeUsername.toLowerCase();
		// Find the guild that has this player pending (first wins; players
		// can only have one outstanding invite cycle in practice).
		for (Guild g : GUILDS.values()) {
			if (g.pendingInvites.containsKey(key)) {
				g.pendingInvites.remove(key);
				if (MEMBER_TO_GUILD.containsKey(key)) return null;
				g.members.put(key, Guild.Role.RECRUIT);
				MEMBER_TO_GUILD.put(key, g.id);
				return g;
			}
		}
		return null;
	}

	public static synchronized boolean leave(final String username) {
		final String key = username.toLowerCase();
		final Integer gid = MEMBER_TO_GUILD.get(key);
		if (gid == null) return false;
		final Guild g = GUILDS.get(gid);
		if (g == null) return false;
		if (g.roleOf(username) == Guild.Role.FOUNDER) return false;  // founder must disband
		g.members.remove(key);
		MEMBER_TO_GUILD.remove(key);
		return true;
	}

	public static synchronized boolean kick(final Guild g, final String byUsername, final String targetUsername) {
		final Guild.Role byRole = g.roleOf(byUsername);
		if (byRole == null || !byRole.canInviteOrKick()) return false;
		final Guild.Role tgtRole = g.roleOf(targetUsername);
		if (tgtRole == null) return false;
		if (tgtRole == Guild.Role.FOUNDER) return false;  // can't kick founder
		// Officers can only kick MEMBER/RECRUIT, not other OFFICERs.
		if (byRole == Guild.Role.OFFICER && tgtRole == Guild.Role.OFFICER) return false;
		g.members.remove(targetUsername.toLowerCase());
		MEMBER_TO_GUILD.remove(targetUsername.toLowerCase());
		return true;
	}

	// ─── Disband ─────────────────────────────────────────────────────

	// ─── Bank operations ─────────────────────────────────────────────

	/** Deposit gold to the guild's treasury. Available to any member. */
	public static synchronized boolean deposit(final Guild g, final String username, final long gold) {
		if (gold <= 0) return false;
		if (g.roleOf(username) == null) return false;
		g.bankGold += gold;
		return true;
	}

	/** Withdraw gold from the guild treasury. Role-gated:
	 *  RECRUIT cannot withdraw; everyone else can (up to balance).
	 *  Returns the amount actually withdrawn (0 on refusal). */
	public static synchronized long withdraw(final Guild g, final String username, final long gold) {
		if (gold <= 0) return 0;
		final Guild.Role r = g.roleOf(username);
		if (r == null || !r.canWithdrawBank()) return 0;
		final long actual = Math.min(gold, g.bankGold);
		g.bankGold -= actual;
		return actual;
	}

	// ─── Role management (promote / demote / transfer) ───────────────

	public enum PromoteResult {
		OK, NOT_AUTHORIZED, TARGET_NOT_MEMBER, ALREADY_TOP, CANNOT_PROMOTE_TO_FOUNDER
	}

	public enum DemoteResult {
		OK, NOT_AUTHORIZED, TARGET_NOT_MEMBER, ALREADY_BOTTOM, CANNOT_DEMOTE_FOUNDER, OFFICER_CANT_DEMOTE_OFFICER
	}

	public enum TransferResult {
		OK, NOT_FOUNDER, TARGET_NOT_MEMBER, TARGET_IS_SELF
	}

	/** Promote target one tier (RECRUIT → MEMBER → OFFICER).
	 *  - FOUNDER can promote any non-founder up to OFFICER.
	 *  - OFFICER can only promote RECRUIT → MEMBER (not MEMBER → OFFICER).
	 *  - No promotion path to FOUNDER (use transfer instead). */
	public static synchronized PromoteResult promote(final Guild g, final String byUsername, final String targetUsername) {
		final Guild.Role by = g.roleOf(byUsername);
		if (by == null) return PromoteResult.NOT_AUTHORIZED;
		final Guild.Role tgt = g.roleOf(targetUsername);
		if (tgt == null) return PromoteResult.TARGET_NOT_MEMBER;
		final Guild.Role nextTier;
		switch (tgt) {
			case RECRUIT: nextTier = Guild.Role.MEMBER;  break;
			case MEMBER:  nextTier = Guild.Role.OFFICER; break;
			case OFFICER: return PromoteResult.CANNOT_PROMOTE_TO_FOUNDER;
			case FOUNDER:
			default:      return PromoteResult.ALREADY_TOP;
		}
		// Authorisation: OFFICER can only do RECRUIT→MEMBER.
		if (by == Guild.Role.OFFICER && nextTier == Guild.Role.OFFICER) return PromoteResult.NOT_AUTHORIZED;
		if (by != Guild.Role.FOUNDER && by != Guild.Role.OFFICER)        return PromoteResult.NOT_AUTHORIZED;
		g.members.put(targetUsername.toLowerCase(), nextTier);
		return PromoteResult.OK;
	}

	/** Demote target one tier (OFFICER → MEMBER → RECRUIT).
	 *  - FOUNDER can demote anyone (not themselves).
	 *  - OFFICER can only demote MEMBER → RECRUIT (not other officers). */
	public static synchronized DemoteResult demote(final Guild g, final String byUsername, final String targetUsername) {
		final Guild.Role by = g.roleOf(byUsername);
		if (by == null) return DemoteResult.NOT_AUTHORIZED;
		final Guild.Role tgt = g.roleOf(targetUsername);
		if (tgt == null) return DemoteResult.TARGET_NOT_MEMBER;
		if (tgt == Guild.Role.FOUNDER)  return DemoteResult.CANNOT_DEMOTE_FOUNDER;
		if (tgt == Guild.Role.RECRUIT)  return DemoteResult.ALREADY_BOTTOM;
		// Officer can't demote a fellow officer.
		if (by == Guild.Role.OFFICER && tgt == Guild.Role.OFFICER) return DemoteResult.OFFICER_CANT_DEMOTE_OFFICER;
		if (by != Guild.Role.FOUNDER && by != Guild.Role.OFFICER)  return DemoteResult.NOT_AUTHORIZED;
		final Guild.Role nextTier = (tgt == Guild.Role.OFFICER) ? Guild.Role.MEMBER : Guild.Role.RECRUIT;
		g.members.put(targetUsername.toLowerCase(), nextTier);
		return DemoteResult.OK;
	}

	/** Hand off the founder role. Caller becomes OFFICER, target becomes
	 *  FOUNDER. Only the current founder can call this. */
	public static synchronized TransferResult transferFounder(final Guild g, final String byUsername, final String targetUsername) {
		if (g.roleOf(byUsername) != Guild.Role.FOUNDER) return TransferResult.NOT_FOUNDER;
		if (byUsername.equalsIgnoreCase(targetUsername)) return TransferResult.TARGET_IS_SELF;
		if (g.roleOf(targetUsername) == null)            return TransferResult.TARGET_NOT_MEMBER;
		g.members.put(targetUsername.toLowerCase(), Guild.Role.FOUNDER);
		g.members.put(byUsername.toLowerCase(),     Guild.Role.OFFICER);
		return TransferResult.OK;
	}

	/** Set the guild motto. Founder/officer only. Caller is responsible
	 *  for length / sanitisation. */
	public static synchronized boolean setMotto(final Guild g, final String byUsername, final String motto) {
		final Guild.Role r = g.roleOf(byUsername);
		if (r == null || !r.canManageEstate()) return false;
		g.motto = motto;
		return true;
	}

	/** Bulk-load registry state from persistence on server startup.
	 *  Wipes the in-memory state first and resets NEXT_ID past any
	 *  loaded guild id. The supplied guilds must arrive with their
	 *  members + pendingInvites maps already populated. */
	public static synchronized void loadFromPersistence(final List<Guild> guilds) {
		GUILDS.clear();
		NAME_TO_ID.clear();
		MEMBER_TO_GUILD.clear();
		int maxId = 0;
		for (Guild g : guilds) {
			GUILDS.put(g.id, g);
			NAME_TO_ID.put(g.name.toLowerCase(), g.id);
			for (String member : g.members.keySet()) {
				MEMBER_TO_GUILD.put(member, g.id);
			}
			if (g.id > maxId) maxId = g.id;
		}
		NEXT_ID.set(maxId + 1);
	}

	public static synchronized boolean disband(final Guild g, final String byUsername) {
		final Guild.Role role = g.roleOf(byUsername);
		if (role == null || !role.canDisband()) return false;
		for (String m : new ArrayList<>(g.members.keySet())) {
			MEMBER_TO_GUILD.remove(m);
		}
		NAME_TO_ID.remove(g.name.toLowerCase());
		GUILDS.remove(g.id);
		return true;
	}
}

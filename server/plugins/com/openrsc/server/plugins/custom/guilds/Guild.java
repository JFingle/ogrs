package com.openrsc.server.plugins.custom.guilds;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * OGRS — Guild data record. Phase 2-α of the housing/contract arc
 * (sparky 2026-05-24). In-memory v1; DB persistence ships once the
 * model shakes out.
 *
 * Roles (4 tiers from the design):
 *   FOUNDER  — created the guild. Can disband + transfer leadership.
 *   OFFICER  — can invite/kick, manage guild estate (when 1F lands),
 *              withdraw from guild bank.
 *   MEMBER   — chat, deposit to bank, withdraw from limited pool.
 *   RECRUIT  — on probation; can chat + enter estate but no bank
 *              withdrawal access.
 *
 * Membership uniqueness: a player can only belong to one guild at a
 * time. Enforced by GuildRegistry.
 */
public final class Guild {

	public enum Role {
		FOUNDER, OFFICER, MEMBER, RECRUIT;

		public boolean canInviteOrKick()    { return this == FOUNDER || this == OFFICER; }
		public boolean canWithdrawBank()    { return this == FOUNDER || this == OFFICER || this == MEMBER; }
		public boolean canManageEstate()    { return this == FOUNDER || this == OFFICER; }
		public boolean canDisband()         { return this == FOUNDER; }
	}

	public final int    id;
	public final String name;             // unique, case-insensitive
	public final String founderUsername;  // never changes (used for audit)
	public final long   createdEpochMs;
	public       String motto = "";       // editable by FOUNDER+OFFICER

	/** member username (lowercase) -> role. */
	public final Map<String, Role> members = new HashMap<>();

	/** Pending invites — keyed by invitee username (lowercase), value
	 *  is the inviter username for audit. Cleared on accept/decline. */
	public final Map<String, String> pendingInvites = new HashMap<>();

	public Guild(final int id, final String name, final String founderUsername) {
		this.id = id;
		this.name = name;
		this.founderUsername = founderUsername;
		this.createdEpochMs = System.currentTimeMillis();
		this.members.put(founderUsername.toLowerCase(), Role.FOUNDER);
	}

	public Role roleOf(final String username) {
		return members.get(username.toLowerCase());
	}

	public boolean hasMember(final String username) {
		return members.containsKey(username.toLowerCase());
	}

	public int memberCount() { return members.size(); }

	public List<String> usernamesByRole(final Role role) {
		final List<String> out = new ArrayList<>();
		for (Map.Entry<String, Role> e : members.entrySet()) {
			if (e.getValue() == role) out.add(e.getKey());
		}
		return out;
	}
}

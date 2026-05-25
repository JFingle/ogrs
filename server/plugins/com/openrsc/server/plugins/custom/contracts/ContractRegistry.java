package com.openrsc.server.plugins.custom.contracts;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * OGRS — in-memory contract storage + lifecycle helpers. Phase 1C of
 * the housing/contract arc (sparky 2026-05-24).
 *
 * v1 storage is a static HashMap — contracts lost on server restart.
 * Adequate for iterating on the design; DB persistence ships as a
 * follow-up once the mechanics + UI shake out.
 *
 * Thread safety: all mutation is gated through the static methods
 * with synchronized blocks. The OpenRSC server runs game logic on a
 * single thread but commands can fire from other threads — keep it
 * defensive.
 *
 * Gold escrow: when a contract is posted, the employer's coins are
 * removed from inventory and stored implicitly in the contract.gold
 * field. On worker delivery, those coins go to the worker. On
 * cancel/expire, coins refund to the employer (must be online for
 * v1; offline-refund via mailbox lands later).
 *
 * Item escrow on completion: when worker delivers, the delivered
 * items are moved into the contract object. Employer collects them
 * by right-clicking the Job Board → "Collect" — items move to bank
 * (or inventory if room) on collection.
 */
public final class ContractRegistry {

	private static final Map<Integer, Contract> CONTRACTS = new HashMap<>();
	private static final AtomicInteger NEXT_ID = new AtomicInteger(1);

	// Completion-side storage: when a worker delivers, we stash the
	// delivered items here keyed by contract id. Employer collects at
	// the Job Board.
	private static final Map<Integer, Item[]> PENDING_DELIVERY = new HashMap<>();

	private ContractRegistry() {}

	// ─── Post / List / Lookup ────────────────────────────────────────

	public static synchronized Contract post(final Player employer,
	                                         final int itemId, final int itemAmount,
	                                         final int goldReward, final int hoursDeadline) {
		final long now = System.currentTimeMillis();
		final long deadline = now + hoursDeadline * 3600L * 1000L;
		final Contract c = new Contract(NEXT_ID.getAndIncrement(),
			Contract.Type.RESOURCE_DELIVERY, employer.getUsername(),
			itemId, itemAmount, goldReward, now, deadline);
		CONTRACTS.put(c.id, c);
		return c;
	}

	/** Post a mentorship contract. Apprentice (employer) pays goldReward
	 *  to a mentor who has skillId at minLevel+ to bond with them for
	 *  durationHours of in-game play within 20 tiles. v1 just records
	 *  the contract; bonded XP-bonus + auto-completion ship in 1D-β. */
	public static synchronized Contract postMentorship(final Player apprentice,
	                                                    final int skillId, final int minLevel,
	                                                    final int durationHours,
	                                                    final int goldReward, final int hoursDeadline) {
		final long now = System.currentTimeMillis();
		final long deadline = now + hoursDeadline * 3600L * 1000L;
		final Contract c = new Contract(NEXT_ID.getAndIncrement(),
			Contract.Type.MENTORSHIP, apprentice.getUsername(),
			-1, 0, goldReward, now, deadline);
		c.mentorSkillId = skillId;
		c.mentorMinLevel = minLevel;
		c.mentorDurationHrs = durationHours;
		CONTRACTS.put(c.id, c);
		return c;
	}

	public static synchronized List<Contract> listOpen() {
		final List<Contract> out = new ArrayList<>();
		final long now = System.currentTimeMillis();
		for (Contract c : CONTRACTS.values()) {
			if (c.status == Contract.Status.OPEN && !c.isExpired(now)) out.add(c);
		}
		// Newest first.
		out.sort((a, b) -> Long.compare(b.createdEpochMs, a.createdEpochMs));
		return out;
	}

	public static synchronized Contract byId(final int id) {
		return CONTRACTS.get(id);
	}

	/** Returns the worker's active accepted contract, or null. */
	public static synchronized Contract activeForWorker(final String username) {
		for (Contract c : CONTRACTS.values()) {
			if (c.status == Contract.Status.ACCEPTED
				&& c.workerName.equalsIgnoreCase(username)) return c;
		}
		return null;
	}

	/** Returns all completed contracts waiting for this employer to collect. */
	public static synchronized List<Contract> readyForCollection(final String username) {
		final List<Contract> out = new ArrayList<>();
		for (Contract c : CONTRACTS.values()) {
			if (c.status == Contract.Status.COMPLETED
				&& c.posterName.equalsIgnoreCase(username)
				&& PENDING_DELIVERY.containsKey(c.id)) out.add(c);
		}
		return out;
	}

	// ─── State transitions ───────────────────────────────────────────

	public static synchronized boolean accept(final Contract c, final Player worker) {
		if (c.status != Contract.Status.OPEN) return false;
		// One active contract per worker at a time — keeps the mechanic
		// honest and stops alt-account stuffing.
		if (activeForWorker(worker.getUsername()) != null) return false;
		c.status = Contract.Status.ACCEPTED;
		c.workerName = worker.getUsername();
		c.acceptedEpochMs = System.currentTimeMillis();
		return true;
	}

	/** Worker delivers the items. Returns true on success. Items + gold
	 *  movement is the caller's responsibility (validate inventory has
	 *  the items, remove them, hand over gold). This method only
	 *  performs the bookkeeping. */
	public static synchronized boolean markDelivered(final Contract c, final Item[] deliveredItems) {
		if (c.status != Contract.Status.ACCEPTED) return false;
		c.status = Contract.Status.COMPLETED;
		c.completedEpochMs = System.currentTimeMillis();
		PENDING_DELIVERY.put(c.id, deliveredItems);
		return true;
	}

	/** Employer collects the delivered items. Returns the array, or
	 *  null if no pending delivery exists. */
	public static synchronized Item[] collect(final Contract c) {
		if (c.status != Contract.Status.COMPLETED) return null;
		final Item[] items = PENDING_DELIVERY.remove(c.id);
		CONTRACTS.remove(c.id);
		return items;
	}

	public static synchronized boolean cancel(final Contract c, final String byUsername) {
		if (c.status != Contract.Status.OPEN) return false;
		if (!c.posterName.equalsIgnoreCase(byUsername)) return false;
		c.status = Contract.Status.CANCELLED;
		// Caller refunds gold to the employer.
		return true;
	}

	// ─── Utility ─────────────────────────────────────────────────────

	/** Format a one-line summary of a contract for chat display. */
	public static String summary(final Contract c) {
		final int hoursLeft = Math.max(0, (int) ((c.deadlineEpochMs - System.currentTimeMillis()) / 3600000L));
		if (c.type == Contract.Type.MENTORSHIP) {
			return String.format("#%d MENTOR — skill:%d lvl%d+, %dh bonded, %dgp (%dh left, by @whi@%s@yel@)",
				c.id, c.mentorSkillId, c.mentorMinLevel, c.mentorDurationHrs,
				c.goldReward, hoursLeft, c.posterName);
		}
		return String.format("#%d DELIV — %dx item:%d for %dgp (%dh left, by @whi@%s@yel@)",
			c.id, c.itemAmount, c.itemId, c.goldReward, hoursLeft, c.posterName);
	}
}

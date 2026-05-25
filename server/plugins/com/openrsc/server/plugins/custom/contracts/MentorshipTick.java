package com.openrsc.server.plugins.custom.contracts;

import com.openrsc.server.event.rsc.DuplicationStrategy;
import com.openrsc.server.event.rsc.GameTickEvent;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;

/**
 * OGRS — mentorship runtime. Phase 1D-β.
 *
 * Single long-running event scheduled at server boot via
 * {@link MentorshipTickStarter}. Fires every 5 game ticks (3.2s @
 * 640ms tick) and iterates accepted MENTORSHIP contracts. For each:
 *
 *   1. Look up apprentice (poster) + mentor (worker) Player objects.
 *      If either is offline, skip — bond doesn't accrue while one of
 *      them isn't playing.
 *   2. Check Chebyshev distance &lt;= 20 tiles. If outside range,
 *      the bond is broken for this tick — no accrual.
 *   3. If within range, increment contract.bondedTicksAccrued by 5
 *      (the tick stride). Heartbeat message every ~60s of bonded
 *      play so both players see progress.
 *   4. When accrued ticks * tick-ms &gt;= mentorDurationHrs * 3600s,
 *      complete the contract — mentor's gold queued for pickup at
 *      Job Board, apprentice notified.
 *
 * Per design, the +50% XP-bonus to the apprentice while bonded is NOT
 * shipped here — that requires a Skills.addExperience hook. For v1
 * the value-prop is "playing together earns the mentor gold and
 * accelerates contract progress"; the XP-bonus polish lands as a
 * follow-up once the hook surface is added.
 */
public final class MentorshipTick extends GameTickEvent {

	private static final int STRIDE_TICKS = 5;
	private static final int BOND_RANGE = 20;
	// Heartbeat every ~60 sec while bonded = ~94 ticks @ 640ms each.
	// Convert to "stride iterations": 94 / STRIDE_TICKS = ~19.
	private static final long HEARTBEAT_EVERY_STRIDES = 19;

	public MentorshipTick(final World world) {
		super(world, null, STRIDE_TICKS, "OGRS Mentorship Tick", DuplicationStrategy.ALLOW_MULTIPLE);
	}

	@Override
	public void run() {
		final long nowMs = System.currentTimeMillis();
		final long tickMs = getWorld().getServer().getConfig().GAME_TICK;
		final long strideMs = tickMs * STRIDE_TICKS;

		for (Contract c : ContractRegistry.snapshotAccepted()) {
			if (c.type != Contract.Type.MENTORSHIP) continue;
			final Player apprentice = getWorld().getPlayer(
				com.openrsc.server.util.rsc.DataConversions.usernameToHash(c.posterName));
			final Player mentor     = getWorld().getPlayer(
				com.openrsc.server.util.rsc.DataConversions.usernameToHash(c.workerName));
			if (apprentice == null || mentor == null) continue;

			final int dx = Math.abs(apprentice.getX() - mentor.getX());
			final int dy = Math.abs(apprentice.getY() - mentor.getY());
			if (Math.max(dx, dy) > BOND_RANGE) continue;

			// Bonded this stride.
			c.bondedTicksAccrued += STRIDE_TICKS;
			final long bondedMs = c.bondedTicksAccrued * tickMs;
			final long requiredMs = c.mentorDurationHrs * 3600L * 1000L;

			// Heartbeat — both parties get a progress nudge.
			final long stridesAccrued = c.bondedTicksAccrued / STRIDE_TICKS;
			if (stridesAccrued % HEARTBEAT_EVERY_STRIDES == 0) {
				final long minutesBonded = bondedMs / 60000L;
				final long minutesNeeded = requiredMs / 60000L;
				apprentice.message("@yel@Mentorship #" + c.id + ": bonded "
					+ minutesBonded + "/" + minutesNeeded + " min with @whi@" + mentor.getUsername() + "@yel@.");
				mentor.message("@yel@Mentorship #" + c.id + ": bonded "
					+ minutesBonded + "/" + minutesNeeded + " min with @whi@" + apprentice.getUsername() + "@yel@.");
			}

			// Completion threshold met?
			if (bondedMs >= requiredMs) {
				ContractRegistry.completeMentorship(c);
				apprentice.message("@gre@Mentorship #" + c.id + " complete. Thanks to @whi@" + mentor.getUsername() + "@gre@.");
				mentor.message("@gre@Mentorship #" + c.id + " complete. " + c.goldReward
					+ "gp available at the Job Board (right-click View).");
			}
		}
	}
}

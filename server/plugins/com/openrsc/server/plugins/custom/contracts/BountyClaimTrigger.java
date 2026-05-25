package com.openrsc.server.plugins.custom.contracts;

import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.PlayerKilledPlayerTrigger;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * OGRS — bounty payout hook. Phase 3-α.
 *
 * Fires on every PvP kill. If the kill happened in the Wilderness AND
 * the victim had open bounty contracts on them, settle each (mark
 * COMPLETED, queue the killer's payout via
 * ContractRegistry.claimBounties). Self-snipe is filtered inside the
 * registry (killer's own bounties on the target are skipped).
 *
 * Killer collects the queued gold at the Job Board (right-click View).
 *
 * The "default" PvP behaviour (loot, prayer skull, etc.) is NOT
 * blocked — bounty is an additive reward layer.
 */
public final class BountyClaimTrigger implements PlayerKilledPlayerTrigger {

	private static final Logger LOGGER = LogManager.getLogger(BountyClaimTrigger.class);

	@Override
	public boolean blockPlayerKilledPlayer(final Player killer, final Player killed) {
		return false;  // never block default loot/death handling
	}

	@Override
	public void onPlayerKilledPlayer(final Player killer, final Player killed) {
		if (killer == null || killed == null) return;
		if (killer == killed) return;  // self-death paranoia
		if (!killed.getLocation().inWilderness()) return;

		final int queued = ContractRegistry.claimBounties(killer.getUsername(), killed.getUsername());
		if (queued > 0) {
			killer.message("@gre@Bounty collected: @whi@" + queued + "gp@gre@ on " + killed.getUsername()
				+ ". Pick up at the Job Board.");
			LOGGER.info("Bounty payout queued: {}gp to {} for killing {}",
				queued, killer.getUsername(), killed.getUsername());
		}
	}
}

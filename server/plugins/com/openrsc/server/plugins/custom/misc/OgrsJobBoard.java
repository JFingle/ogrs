package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Job Board interaction (Phase 1B of the housing/contract arc).
 *
 * Scenery id 1326 placed in town centers. Right-click View / Post opens
 * the contract menu. v1 is a placeholder shell — the actual storage,
 * UI panel, and per-contract-type mechanics ship in subsequent phases:
 *
 *   1C — Resource delivery contracts (player-to-player item commissions)
 *   1D — Mentorship contracts (20-tile bonded play with +50% XP)
 *   1E — Construction-job contracts (commission furniture on your plot,
 *        the one place employer-collected XP is allowed)
 *
 * For now: shows a flavor message + previews the future contract types
 * so players know what's coming. Lets us drop the physical scenery
 * early without committing the implementation in one giant session.
 */
public final class OgrsJobBoard implements OpLocTrigger {

	private static final int BOARD_ID = 1326;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == BOARD_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != BOARD_ID) return;

		if ("post".equalsIgnoreCase(command)) {
			player.message("@yel@You consider pinning a job postal here, but the system isn't yet open.");
			player.message("Post-a-contract UI lands in Phase 1C — resource delivery first.");
			return;
		}

		// Default: View
		player.message("@gre@The Lumbridge Job Board.");
		player.message("Coming soon:");
		player.message("  @whi@Resource delivery@yel@ — pay another player to gather + bring items.");
		player.message("  @whi@Mentorship@yel@ — pay a high-skilled player to bond-train alongside you (20-tile range, +50% XP while bonded).");
		player.message("  @whi@Construction jobs@yel@ — once you own a plot, hire others to build furniture (the XP goes to you).");
		player.message("Build out: 1C (resource), 1D (mentor), 1E (construction-job).");
	}
}

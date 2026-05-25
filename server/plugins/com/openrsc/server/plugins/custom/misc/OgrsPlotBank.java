package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.custom.plots.Plot;
import com.openrsc.server.plugins.custom.plots.PlotFeature;
import com.openrsc.server.plugins.custom.plots.PlotRegistry;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Lodge Bank Chest interaction. Phase 1F-γ.
 *
 * Handles right-click Use on scenery id 1328 (Lodge Bank Chest).
 * Permission gate:
 *   - If the chest is INSIDE a plot's bounding box AND the player is
 *     the deed holder, open the bank for them.
 *   - If the chest is in a communal lodge (placed by SceneryLocsCustom,
 *     not registered as a PlotFeature), open the bank for anyone —
 *     future Phase 1G work.
 *   - Otherwise (chest on someone else's plot), block with a message.
 */
public final class OgrsPlotBank implements OpLocTrigger {

	private static final int CHEST_ID = 1328;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == CHEST_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != CHEST_ID) return;

		// Find the plot (if any) that contains this scenery.
		Plot owning = null;
		for (Plot pl : PlotRegistry.listAll()) {
			if (pl.contains(obj.getX(), obj.getY())) { owning = pl; break; }
		}

		if (owning != null) {
			// Plot-built chest — permission gate.
			final PlotFeature pf = owning.featureAt(obj.getX(), obj.getY());
			if (pf == null) {
				player.message("(@yel@The chest looks built but isn't registered. Try again after a restart.)");
				return;
			}
			if (owning.deedHolder == null) {
				player.message("@red@This chest's plot has no deed holder.");
				return;
			}
			if (owning.tier == Plot.Tier.WILDERNESS) {
				final com.openrsc.server.plugins.custom.guilds.Guild g =
					com.openrsc.server.plugins.custom.guilds.GuildRegistry.byName(owning.deedHolder);
				if (g == null || !g.hasMember(player.getUsername())) {
					player.message("@red@This chest is property of guild @whi@" + owning.deedHolder + "@red@.");
					return;
				}
			} else if (!owning.deedHolder.equalsIgnoreCase(player.getUsername())) {
				player.message("@red@This chest belongs to @whi@" + owning.deedHolder + "@red@. Hands off.");
				return;
			}
		}
		// else: communal lodge (no plot match) — open for anyone.

		player.setAccessingBank(true);
		ActionSender.showBank(player);
	}
}

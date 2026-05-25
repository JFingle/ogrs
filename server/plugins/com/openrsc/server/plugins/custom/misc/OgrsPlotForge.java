package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.plots.Plot;
import com.openrsc.server.plugins.custom.plots.PlotFeature;
import com.openrsc.server.plugins.custom.plots.PlotRegistry;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Lodge Forge interaction. Phase 1F-δ.
 *
 * Scenery id 1329. Right-click Use is permission-gated like the bank
 * chest (deed holder only on plots; anyone in a communal lodge).
 *
 * v1 = visual + permission gate. The actual smithing pipeline lives
 * in upstream Smithing.java (UseLocTrigger on the authentic anvil
 * scenery ids). Routing OGRS forge ID 1329 through that flow is a
 * v2 work item — for v1, deed holders get a placeholder message
 * confirming the forge is built and theirs, with a roadmap pointer.
 */
public final class OgrsPlotForge implements OpLocTrigger {

	private static final int FORGE_ID = 1329;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == FORGE_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != FORGE_ID) return;

		// Find the plot (if any) that contains this scenery.
		Plot owning = null;
		for (Plot pl : PlotRegistry.listAll()) {
			if (pl.contains(obj.getX(), obj.getY())) { owning = pl; break; }
		}

		if (owning != null) {
			final PlotFeature pf = owning.featureAt(obj.getX(), obj.getY());
			if (pf == null) return;
			if (owning.deedHolder == null) return;
			if (owning.tier == Plot.Tier.WILDERNESS) {
				final com.openrsc.server.plugins.custom.guilds.Guild g =
					com.openrsc.server.plugins.custom.guilds.GuildRegistry.byName(owning.deedHolder);
				if (g == null || !g.hasMember(player.getUsername())) {
					player.message("@red@This forge belongs to guild @whi@" + owning.deedHolder + "@red@.");
					return;
				}
			} else if (!owning.deedHolder.equalsIgnoreCase(player.getUsername())) {
				player.message("@red@This forge belongs to @whi@" + owning.deedHolder + "@red@.");
				return;
			}
		}

		// Permission OK.
		player.message("@gre@You stand at your forge. Bring iron bars + a hammer to smith here.");
		player.message("(v1 visual + permission only — full smithing integration ships as a follow-up.)");
	}
}

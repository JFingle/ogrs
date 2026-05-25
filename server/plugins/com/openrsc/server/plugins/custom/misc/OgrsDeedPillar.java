package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.plots.Plot;
import com.openrsc.server.plugins.custom.plots.PlotRegistry;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

import java.util.List;
import java.util.Map;

/**
 * OGRS — Deed Pillar interaction (Phase 1F-α). Scenery id 1327 at
 * each plot's entry point. Right-click Inspect/Bid handlers.
 */
public final class OgrsDeedPillar implements OpLocTrigger {

	private static final int PILLAR_ID = 1327;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == PILLAR_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != PILLAR_ID) return;

		final Plot plot = PlotRegistry.byPillarLocation(obj.getX(), obj.getY());
		if (plot == null) {
			player.message("@red@(Internal error — no plot registered at this pillar.)");
			return;
		}

		if ("bid".equalsIgnoreCase(command)) {
			player.message("@gre@To bid on @whi@" + plot.name + "@gre@:");
			player.message("  ::plot bid " + plot.id + " <amount>");
			player.message("Auction floor: @whi@" + plot.tier.auctionFloor() + "gp@gre@. Bids escrow immediately.");
			return;
		}

		// Inspect
		player.message("@gre@" + plot.name + " (Plot #" + plot.id + ", " + plot.tier + ")");
		player.message("  Theme: @whi@" + plot.themeHint + "@gre@");
		player.message("  Area: (" + plot.boxMinX + "," + plot.boxMinY + ")..(" + plot.boxMaxX + "," + plot.boxMaxY + ")");
		player.message("  Feature slots: @whi@" + plot.tier.featureSlots());
		final long now = System.currentTimeMillis();
		if (plot.isVacant(now)) {
			player.message("  @yel@VACANT — open for bidding.");
			player.message("  Auction floor: @whi@" + plot.tier.auctionFloor() + "gp@yel@");
			if (!plot.openBids.isEmpty()) {
				player.message("  Current bids: @whi@" + plot.openBids.size() + "@yel@");
				final List<Map.Entry<String, Integer>> top = plot.bidsHighestFirst();
				for (int i = 0; i < Math.min(3, top.size()); i++) {
					player.message("    " + (i + 1) + ". @whi@" + top.get(i).getKey()
						+ "@yel@ @ " + top.get(i).getValue() + "gp");
				}
			}
		} else {
			player.message("  Owner: @whi@" + plot.deedHolder);
			final long hoursLeft = Math.max(0, (plot.tenancyExpiresMs - now) / 3600000L);
			player.message("  Tenancy: @whi@" + hoursLeft + "h@gre@ remaining.");
		}
		player.message("  Use ::plot info " + plot.id + " for full details.");
	}
}

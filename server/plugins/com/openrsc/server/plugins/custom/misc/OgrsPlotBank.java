package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.custom.plots.PlotPermissions;
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
		if (!PlotPermissions.canUseFeatureAt(player, obj.getX(), obj.getY(), "chest")) return;
		player.setAccessingBank(true);
		ActionSender.showBank(player);
	}
}

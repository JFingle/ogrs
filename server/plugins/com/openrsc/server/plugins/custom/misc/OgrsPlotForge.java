package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.plots.PlotPermissions;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Lodge Forge right-click "Use" interaction. Scenery id 1329.
 *
 * Right-click "Use" (no item) prints a hint pointing the player at
 * the actual smithing flow: use a metal bar on the forge to start
 * smithing — the upstream Smithing plugin handles the bar-on-forge
 * UseLocTrigger and treats id 1329 just like an anvil.
 *
 * The permission check sits in PlotPermissions and is enforced both
 * here and in Smithing — keeping the rules in one place.
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
		if (!PlotPermissions.canUseFeatureAt(player, obj.getX(), obj.getY(), "forge")) return;
		player.message("@gre@A bright forge waits for your work. Use a metal bar on it (with a hammer in your pack) to begin smithing.");
	}
}

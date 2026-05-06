package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.PlayerLoginTrigger;

/**
 * Dev-mode QoL: when a player logs in on Tutorial Island and the world
 * has `skip_tutorial_on_register: true`, immediately skip them to the
 * Lumbridge respawn point and clear the tutorial cache flag.
 *
 * Production worlds leave the flag off and the tutorial flow is unchanged.
 *
 * Coexists with the existing `plugins/shared/PlayerLogin.java` no-op stub —
 * the plugin handler dispatches to all PlayerLoginTrigger implementations.
 */
public class OgrsAutoSkipTutorial implements PlayerLoginTrigger {

	@Override
	public void onPlayerLogin(final Player player) {
		if (!player.getWorld().getServer().getConfig().SKIP_TUTORIAL_ON_REGISTER) {
			return;
		}
		if (!player.getLocation().onTutorialIsland()) {
			return;
		}

		// Drop the tutorial cache flag so authentic tutorial-completion checks
		// throughout the codebase treat them as graduated.
		if (player.getCache().hasKey("tutorial")) {
			player.getCache().remove("tutorial");
		}

		player.teleport(
			player.getWorld().getServer().getConfig().RESPAWN_LOCATION_X,
			player.getWorld().getServer().getConfig().RESPAWN_LOCATION_Y,
			false);
		player.message("@gre@OGRS: tutorial skipped — welcome to Lumbridge.");
	}

	@Override
	public boolean blockPlayerLogin(final Player player) {
		return false;
	}
}

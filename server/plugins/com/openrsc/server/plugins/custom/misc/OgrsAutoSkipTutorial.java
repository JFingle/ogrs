package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.event.SingleEvent;
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
 *
 * Why the teleport is scheduled (sparky 2026-05-19 #14): when fired
 * synchronously inline during onPlayerLogin, the engine's post-login init
 * occasionally overwrites the new position with the player's stored
 * Tutorial Island spawn (witnessed: fingle account stayed at 216, 744
 * even though the trigger fired and the cache key cleared). Deferring
 * the teleport by one tick puts it after the engine's init quietly
 * finishes, and the position sticks. Also gives the Android client a
 * moment to finish handshake before terrain shifts under it — Tutorial
 * Island's special render path was crashing the Android client; a
 * one-tick gap eliminates the racy state.
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

		// Defer the teleport one tick — see class javadoc.
		final int respawnX = player.getWorld().getServer().getConfig().RESPAWN_LOCATION_X;
		final int respawnY = player.getWorld().getServer().getConfig().RESPAWN_LOCATION_Y;
		player.getWorld().getServer().getGameEventHandler().add(
			new SingleEvent(player.getWorld(), null, 1, "OGRS skip tutorial") {
				@Override
				public void action() {
					if (player.isRemoved() || !player.getLocation().onTutorialIsland()) return;
					player.teleport(respawnX, respawnY, false);
					player.message("@gre@OGRS: tutorial skipped — welcome to Lumbridge.");
				}
			});
	}

	@Override
	public boolean blockPlayerLogin(final Player player) {
		return false;
	}
}

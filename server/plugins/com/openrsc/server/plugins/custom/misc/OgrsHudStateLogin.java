package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.event.SingleEvent;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.PlayerLoginTrigger;

/**
 * OGRS — UI track P1 — push the player's HUD state (poison + slayer
 * task) to the client right after login so the HUD icons reflect
 * persisted state from prior sessions. Mirrors OgrsRunEnergyLogin's
 * one-tick-deferred pattern so the network session is fully up.
 *
 * Without this, players who logged out while poisoned or mid-slayer-
 * task would see no HUD indicator until the next state change.
 */
public class OgrsHudStateLogin implements PlayerLoginTrigger {

	@Override
	public void onPlayerLogin(final Player player) {
		player.getWorld().getServer().getGameEventHandler().add(
			new SingleEvent(player.getWorld(), null, 1, "OGRS HUD state login push") {
				@Override
				public void action() {
					if (player.isRemoved()) return;
					ActionSender.sendPoisonState(player);
					com.openrsc.server.plugins.custom.skills.slayer.SlayerService.ogrsPushSlayerTask(player);
				}
			});
	}

	@Override
	public boolean blockPlayerLogin(final Player player) {
		return false;
	}
}

package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.event.SingleEvent;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.PlayerLoginTrigger;

/**
 * OGRS — push the run-energy state to the client right after login so the
 * standalone bar/percent reads correctly on first frame. The Player.setRunEnergy /
 * setRunning hooks only fire sendRunEnergy() on state CHANGE, so a fresh
 * full-energy idle player never triggers an automatic send. One push at login
 * fixes that without polluting the hot path.
 *
 * Deferred one tick so the network session is fully established (mirrors
 * OgrsAutoSkipTutorial's reasoning).
 */
public class OgrsRunEnergyLogin implements PlayerLoginTrigger {

	@Override
	public void onPlayerLogin(final Player player) {
		if (!player.getWorld().getServer().getConfig().WANT_RUN_ENERGY) return;
		player.getWorld().getServer().getGameEventHandler().add(
			new SingleEvent(player.getWorld(), null, 1, "OGRS run-energy login push") {
				@Override
				public void action() {
					if (player.isRemoved()) return;
					ActionSender.sendRunEnergy(player);
				}
			});
	}

	@Override
	public boolean blockPlayerLogin(final Player player) {
		return false;
	}
}

package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Crypt Gate interaction (sparky 2026-05-22).
 *
 * Three blocking gates (scenery id 1324) divide the dungeon at:
 *   (122, 3720) — between Giant Nest (spider) and Ghost Hollow
 *   (121, 3738) — between Zombie Warrens and Ossuary (skeletons)
 *   (122, 3742) — between Ossuary and Tomb (boss room)
 *
 * Each gate is type=1 (blocking) so the player can't walk through. On
 * "Open" click, this plugin detects which side of the gate the player
 * is standing on and teleports them one tile to the other side, with a
 * "The gate creaks open" message.
 *
 * No key required yet — future work can add a key check here for each
 * gate (e.g., Burial Crest for the boss gate). The Sealed Stone Door
 * (scenery 1323) at the Spider Vault entrance is the only key-gated
 * door so far — handled by OgrsCryptSpiderVault.
 */
public class OgrsCryptGate implements OpLocTrigger {

	private static final int GATE_ID = 1324;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == GATE_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != GATE_ID) return;

		final int gx = obj.getX();
		final int gy = obj.getY();
		final int py = player.getY();

		// Player is north of the gate → teleport to one tile south of it.
		// Player is south of (or on) the gate → teleport one tile north.
		final int destY = (py < gy) ? (gy + 1) : (gy - 1);

		player.message("The gate creaks open as you push through.");
		player.teleport(gx, destY, false);
	}
}

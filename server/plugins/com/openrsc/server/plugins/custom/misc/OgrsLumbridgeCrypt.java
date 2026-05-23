package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Lumbridge Crypt entrance, exits, and inner descent. First OGRS
 * dungeon (sparky 2026-05-19 #11, expanded 2026-05-21 with the
 * Burial Chamber).
 *
 * Layout — three layers connected by two scenery pairs:
 *
 *   Surface           hatch (1319) east of Lumbridge (173, 638)
 *      |  Climb-down
 *      v  Climb-up
 *   Spider Chamber    ladder (1320) at (120, 3700); spiders Y 3700-3713
 *      |  Walk-down  (steps 1321 at (122, 3714))
 *      v  Walk-up    (steps 1322 at (122, 3720))
 *   Burial Chamber    undead Y 3720-3740; Crypt Lord boss at (122, 3740)
 *
 * IMPORTANT — plane-3 landscape data only covers world Y 2832..3791 (the
 * authentic underground band). Earlier crypt revs placed the chamber at
 * Y 3800+, which is past the loaded tile data — teleporting there
 * caused the client to disconnect because there were no tiles to draw.
 * Sticking the dungeon at Y 3700..3740 keeps everything inside the
 * loaded plane-3 region.
 *
 * The hatch+ladder pair handles surface ↔ spider chamber; the
 * steps pair handles spider chamber ↔ burial chamber. The teleport
 * destinations are tile-adjacent to the source scenery so the
 * player visibly steps off the stairs on arrival.
 *
 * OGRS owns scenery ids 1319-1322 exclusively — upstream Ladders.java
 * doesn't know about ids in the OGRS reserved range, so the engine
 * routes them here.
 */
public class OgrsLumbridgeCrypt implements OpLocTrigger {

	private static final int HATCH_ID      = 1319;
	private static final int LADDER_UP_ID  = 1320;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		final int id = obj.getID();
		return id == HATCH_ID || id == LADDER_UP_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		switch (obj.getID()) {
			// Each teleport target is OFFSET by one tile from the source
			// scenery — otherwise the client lands on the very tile that
			// triggered the action, which has hit GameActivity/client
			// crashes during plane transitions (sparky 2026-05-22).
			// v3 layout: ladder at (112,3702), steps_down at (122,3719),
			// steps_up at (122,3722). Teleport targets offset 1 tile from
			// the scenery so the client doesn't re-trigger interaction.
			case HATCH_ID:
				player.message("You climb down into the crypt. The air is cold and damp.");
				player.teleport(114, 3702, false);   // 1 east of ladder at (113, 3701)
				break;
			case LADDER_UP_ID:
				player.message("You climb back up to the surface.");
				player.teleport(173, 639, false);    // 1 south of hatch
				break;
		}
	}
}

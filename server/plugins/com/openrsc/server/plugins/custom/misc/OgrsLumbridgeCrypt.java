package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Lumbridge Crypt surface ↔ antechamber transition. First OGRS
 * dungeon (sparky 2026-05-19 #11; expanded into Crypt v2 on 2026-05-21
 * with the Burial Chamber and boss room).
 *
 * Scope of THIS plugin: just the hatch + ladder pair that ferries the
 * player between Lumbridge surface and the spider antechamber. The
 * inter-chamber transitions are owned by sibling plugins:
 *
 *   1319 hatch / 1320 ladder   — this plugin (surface ↔ antechamber)
 *   1323 sealed stone door     — OgrsCryptSpiderVault (key-gated)
 *   1324 inner gate (×3)       — OgrsCryptGate (spider/ghost,
 *                                warrens/ossuary, boss-room)
 *
 * IMPORTANT — plane-3 landscape data only covers world Y 2832..3791
 * (the authentic underground band). Crypt v1 placed the chamber at
 * Y 3800+, which is past loaded tile data — teleporting there
 * disconnected the client because there were no tiles to draw. v2
 * lives entirely at Y 3700..3740 inside the loaded plane-3 region.
 *
 * Floor synthesis for the unauthored crypt sectors lives in
 * WorldLoader.ogrsLoadCryptWalkable — overlay=5 (cave moss) is
 * load-bearing; overlay=8 maps to the TRANSPARENT sentinel and the
 * renderer silently skips face insertion (no floor renders).
 *
 * Teleport destinations are offset one tile from the source scenery
 * so the client doesn't immediately re-trigger interaction on landing
 * (caused intermittent GameActivity/client crashes during plane
 * transitions, sparky 2026-05-22).
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
			case HATCH_ID:
				player.message("You climb down into the crypt. The air is cold and damp.");
				player.teleport(114, 3702, false);   // 1 east of ladder at (113, 3701)
				break;
			case LADDER_UP_ID:
				player.message("You climb back up to the surface.");
				player.teleport(173, 639, false);    // 1 south of hatch at (173, 638)
				break;
		}
	}
}

package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Lumbridge Crypt entrance + exit. First OGRS dungeon (sparky
 * 2026-05-19 #11), MVP cut.
 *
 * Surface hatch (scenery id 1319) at (120, 645) — Lumbridge castle
 * interior, north side, away from existing NPCs. Click "Climb-down"
 * teleports the player to the crypt at (120, 3800) in the otherwise-
 * unused Y 3700-3900 band of the world.
 *
 * Crypt ladder (scenery id 1320) at (120, 3800) — back up to (120, 645).
 *
 * The crypt itself is populated by NpcLocsCustom.json — a handful of
 * spider variants for the player to fight. Future expansion: more
 * floors, a boss room, a chest with a one-time reward.
 *
 * Owns these two scenery ids exclusively. Upstream Ladders.java
 * doesn't know about ids in the OGRS reserved range, so it ignores
 * these and only our plugin handles them.
 */
public class OgrsLumbridgeCrypt implements OpLocTrigger {

	private static final int HATCH_ID  = 1319;
	private static final int LADDER_ID = 1320;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		final int id = obj.getID();
		return (id == HATCH_ID || id == LADDER_ID);
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() == HATCH_ID) {
			player.message("You climb down into the crypt. The air is cold and damp.");
			player.teleport(120, 3800, false);
		} else if (obj.getID() == LADDER_ID) {
			player.message("You climb back up to the surface.");
			player.teleport(120, 645, false);
		}
	}
}

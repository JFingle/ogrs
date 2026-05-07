package com.openrsc.server.plugins.custom.skills.mining;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.event.SingleEvent;
import com.openrsc.server.model.Point;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.OpLocTrigger;
import com.openrsc.server.util.rsc.DataConversions;
import com.openrsc.server.util.rsc.Formulae;
import com.openrsc.server.util.rsc.MessageType;

import static com.openrsc.server.plugins.Functions.give;

/**
 * OGRS Mining — Goblin Iron Vein.
 *
 * Custom OpLoc handler for mining the Goblin Iron Veins (1311) scattered
 * around the camp. We don't extend upstream's ObjectMining.xml at runtime;
 * this plugin runs a parallel mining loop just for the OGRS-flavored
 * veins, mirroring the upstream shape (level + pickaxe + roll, deplete
 * then respawn).
 *
 * Lifecycle:
 *   1311 Goblin Iron Vein  + Mine     →  roll → +Iron Ore + 35 XP, swap to 1312, schedule respawn
 *   1311                   + Prospect →  flavor message
 *   1312 Depleted Vein     (no Mine)  →  auto-swaps back after RESPAWN_TICKS
 *
 * Tuning: required Mining lvl 15, ~10s respawn (consistent with the dev-fast
 * iteration cadence we're running for farming).
 */
public final class OgrsGoblinVein implements OpLocTrigger {

	private static final int VEIN_ID = 1311;
	private static final int DEPLETED_ID = 1312;
	private static final int REQUIRED_MINING_LEVEL = 15;
	private static final int XP_DISPLAY = 35; // engine multiplies by 4
	private static final int RESPAWN_TICKS = 16; // ~10s at 640ms

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		final int id = obj.getID();
		return (id == VEIN_ID && (command.equalsIgnoreCase("mine") || command.equalsIgnoreCase("prospect")))
			|| (id == DEPLETED_ID && command.equalsIgnoreCase("examine"));
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		final int id = obj.getID();
		if (id == DEPLETED_ID) {
			player.message("@gre@The vein is spent. Iron will catch up in a moment.");
			return;
		}
		if (command.equalsIgnoreCase("prospect")) {
			player.playerServerMessage(MessageType.QUEST, "You inspect the vein.");
			player.playerServerMessage(MessageType.QUEST, "@gre@This rock contains iron ore — and goblin scratches.");
			return;
		}
		// Mine.
		if (!hasPickaxe(player)) {
			player.message("@yel@You need a pickaxe to mine this vein.");
			return;
		}
		if (player.getSkills().getLevel(Skill.MINING.id()) < REQUIRED_MINING_LEVEL) {
			player.playerServerMessage(MessageType.QUEST,
				"You need a Mining level of " + REQUIRED_MINING_LEVEL + " to work this vein.");
			return;
		}

		ActionSender.sendSound(player, "mine");
		// Simple 60% success (was scaled to level in upstream — keep it
		// flat for OGRS dev-fast; upstream's RandomCheck calc would slot
		// here later when we tune mining curves).
		if (DataConversions.random(1, 100) > 60) {
			player.playerServerMessage(MessageType.QUEST, "You swing your pickaxe at the rock...");
			player.playerServerMessage(MessageType.QUEST, "@yel@You only chip flakes loose. Try again.");
			return;
		}

		give(player, ItemId.IRON_ORE.id(), 1);
		// Lucky ~10% chance to also dislodge a piece of coal — small bonus
		// for working a goblin-mangled vein.
		if (DataConversions.random(1, 100) <= 10) {
			give(player, ItemId.COAL.id(), 1);
			player.message("@gre@A lump of coal comes loose with the iron.");
		}
		player.getSkills().addExperience(Skill.MINING.id(), XP_DISPLAY * 4);
		player.playerServerMessage(MessageType.QUEST,
			"You manage to obtain some iron ore. (+" + XP_DISPLAY + " Mining XP)");

		// Swap to depleted, schedule respawn back to active vein.
		final World world = player.getWorld();
		final Point loc = obj.getLocation();
		final int direction = obj.getDirection();
		final int type = obj.getType();
		final GameObject depleted = new GameObject(world, loc, DEPLETED_ID, direction, type);
		world.replaceGameObject(obj, depleted);

		world.getServer().getGameEventHandler().add(
			new SingleEvent(world, null, RESPAWN_TICKS, "OGRS Mining - vein respawn") {
				@Override
				public void action() {
					final GameObject current = world.getRegionManager()
						.getRegion(loc).getGameObject(loc, null);
					if (current != null && current.getID() == DEPLETED_ID) {
						final GameObject vein = new GameObject(world, loc, VEIN_ID, direction, type);
						world.replaceGameObject(current, vein);
					}
				}
			}
		);
	}

	private static boolean hasPickaxe(final Player player) {
		for (final int id : Formulae.miningAxeIDs) {
			if (player.getCarriedItems().hasCatalogID(id)) return true;
		}
		return false;
	}
}

package com.openrsc.server.plugins.custom.scenery;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.OpLocTrigger;
import com.openrsc.server.util.rsc.DataConversions;

import static com.openrsc.server.plugins.Functions.give;

/**
 * OGRS scenery handler: Search a Goblin Crate.
 *
 * Listens for the right-click "Search" verb on Goblin Crate scenery
 * (id 1310, scattered around the camp east of Lumbridge). Rolls a
 * weighted loot table per search; the crate stays in place and can be
 * searched again — RSC1-era behaviour, no per-crate cooldown.
 *
 * Loot table (1d100 roll):
 *    1- 50  Bones                       (50%)
 *   51- 80  Coins (5–15)                (30%)
 *   81- 92  Goblin Armour, random tint  (12%)
 *   93- 97  Goblin Trinket              ( 5%)
 *   98-100  Empty                       ( 3%)
 *
 * "prospect" sound on every search so the action has feedback even
 * when the roll is empty.
 */
public final class GoblinCrateSearch implements OpLocTrigger {

	private static final int CRATE_ID = 1310;

	// Upstream Goblin Armour ids (different colour tints — green/orange/blue).
	// See client EntityHandler lines 2633-2635.
	private static final int[] GOBLIN_ARMOUR_TINTS = { 273, 274, 275 };

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == CRATE_ID && command.equalsIgnoreCase("search");
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		ActionSender.sendSound(player, "prospect");
		final int roll = DataConversions.random(1, 100);

		if (roll <= 50) {
			give(player, ItemId.BONES.id(), 1);
			player.message("@gre@You rummage through the crate and pull out a handful of bones.");
		} else if (roll <= 80) {
			final int coins = DataConversions.random(5, 15);
			give(player, ItemId.COINS.id(), coins);
			player.message("@gre@You find a small pile of coins (" + coins + ").");
		} else if (roll <= 92) {
			final int armourId = GOBLIN_ARMOUR_TINTS[DataConversions.random(0, GOBLIN_ARMOUR_TINTS.length - 1)];
			give(player, armourId, 1);
			player.message("@gre@You find a piece of goblin armour, balled up under the rags.");
		} else if (roll <= 97) {
			give(player, ItemId.OGRS_GOBLIN_TRINKET.id(), 1);
			player.message("@gre@A bone trinket on twine — odd thing to keep, but it's worth a few gp.");
		} else {
			player.message("@yel@The crate holds nothing but mouse droppings and old rags.");
		}
	}
}

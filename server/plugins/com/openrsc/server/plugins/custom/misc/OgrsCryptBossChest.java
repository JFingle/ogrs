package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

/**
 * OGRS — Crypt Lord's Chest at the back of the Burial Chamber boss
 * room (122, 3743). One-time payoff per player for clearing the
 * dungeon: a chunky coin + rune drop on first Search.
 *
 * Distinct from {@link OgrsCryptLordDrop}'s first-kill Cryptkeeper's
 * Skull — that's a kill trophy, this is a treasure trophy. They
 * complement each other; clearing the dungeon yields BOTH on the
 * first run, then degrades to skeleton-tier kill loot only.
 *
 * Gated by player cache key "ogrs_crypt_chest_opened". No cooldown,
 * no refill — the chest is a "you've been here" moment, not a farm.
 * If we ever want a daily refill, swap the boolean for a timestamp.
 */
public final class OgrsCryptBossChest implements OpLocTrigger {

	private static final int CHEST_ID = 1325;
	private static final String OPENED_KEY = "ogrs_crypt_chest_opened";

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == CHEST_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != CHEST_ID) return;

		if (player.getCache().hasKey(OPENED_KEY)) {
			player.message("The chest is empty. The Crypt Lord's hoard was for you, once.");
			return;
		}

		player.getCache().store(OPENED_KEY, true);
		player.message("@gre@You force the chest open. Cold air spills out.");
		player.message("Inside: a heap of coins and a bundle of runes.");

		// First-time payoff. Tunable; sized to feel like a meaningful
		// dungeon-clear reward without trivialising mid-tier rune farming.
		player.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), 5000));
		player.getCarriedItems().getInventory().add(new Item(ItemId.CHAOS_RUNE.id(), 50));
		player.getCarriedItems().getInventory().add(new Item(ItemId.DEATH_RUNE.id(), 15));
		player.getCarriedItems().getInventory().add(new Item(ItemId.NATURE_RUNE.id(), 10));
	}
}

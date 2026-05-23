package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.KillNpcTrigger;
import com.openrsc.server.plugins.triggers.OpLocTrigger;
import com.openrsc.server.util.rsc.DataConversions;
import com.openrsc.server.util.rsc.MessageType;

/**
 * OGRS — Crypt Spider Vault gating logic (sparky 2026-05-22).
 *
 * Two parts:
 *
 * 1) KEY DROP — any Zombie lvl24 (id 41) killed inside the Zombie
 *    Warrens drops the Crypt Spider Key (item 1609). 100% one-time
 *    drop, gated by player cache flag so subsequent zombie kills give
 *    nothing extra (key isn't re-droppable for the same character).
 *
 * 2) DOOR USE — clicking "Use" on the Sealed Stone Door (scenery 1323
 *    at world tile (133, 3740)) consumes the key from the player's
 *    inventory and teleports them one tile east into the Spider Vault
 *    corridor. The key "crumbles" — they get one shot at the mini-boss.
 *
 * The mini-boss is a Giant Spider lvl 31 (id 74). Standard skeleton
 * drop table applies on kill; OGRS doesn't gate the EXIT, so the
 * player can walk back through the corridor freely once inside.
 */
public class OgrsCryptSpiderVault implements OpLocTrigger, KillNpcTrigger {

	private static final int DOOR_ID = 1323;
	private static final int KEY_ITEM = 1609;
	private static final int ZOMBIE_NPC_ID = 41;
	private static final String FIRST_KEY_DROP_KEY = "ogrs_crypt_spider_key_dropped";

	// Zombie Warrens tile rectangle (must match gen_crypt_v4.py warrens
	// bounding box). Mob has to be killed INSIDE this zone for the key
	// drop to fire, so wilderness zombies don't trigger it.
	private static final int WARRENS_X1 = 108, WARRENS_X2 = 137;
	private static final int WARRENS_Y1 = 3730, WARRENS_Y2 = 3737;

	// ─── DOOR (OpLocTrigger) ──────────────────────────────────────────

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == DOOR_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != DOOR_ID) return;
		final Item key = player.getCarriedItems().getInventory().get(
			new Item(KEY_ITEM, 1));
		if (key == null) {
			player.message("The door is sealed shut. You'll need a key.");
			return;
		}
		// Consume the key (crumbles).
		player.getCarriedItems().getInventory().remove(new Item(KEY_ITEM, 1), true);
		player.playerServerMessage(MessageType.QUEST,
			"@gre@The key crumbles to rust as you turn it in the lock.");
		// Teleport to the corridor just past the door (1 east).
		player.teleport(134, 3740, false);
	}

	// ─── KEY DROP (KillNpcTrigger) ─────────────────────────────────────

	private static boolean isInWarrens(final Npc npc) {
		final int x = npc.getX(), y = npc.getY();
		return x >= WARRENS_X1 && x <= WARRENS_X2
		    && y >= WARRENS_Y1 && y <= WARRENS_Y2;
	}

	@Override
	public boolean blockKillNpc(final Player player, final Npc npc) {
		if (npc.getID() != ZOMBIE_NPC_ID) return false;
		if (!isInWarrens(npc)) return false;
		// Only fire once per character — after that, default loot only.
		return !player.getCache().hasKey(FIRST_KEY_DROP_KEY);
	}

	@Override
	public void onKillNpc(final Player player, final Npc npc) {
		// Mark the cache so future zombie kills use upstream's default loot.
		player.getCache().store(FIRST_KEY_DROP_KEY, true);
		// Give the player the key directly (cleaner than a ground item that
		// can despawn before they reach it).
		if (player.getCarriedItems().getInventory().getFreeSlots() > 0) {
			player.getCarriedItems().getInventory().add(new Item(KEY_ITEM, 1));
			player.message("@yel@The zombie clutched a heavy iron key. You take it.");
		} else {
			player.message("@yel@A key falls from the zombie — but your pack is full!");
			player.getWorld().registerItem(
				new com.openrsc.server.model.entity.GroundItem(
					player.getWorld(), KEY_ITEM, npc.getX(), npc.getY(), 1, player),
				player.getConfig().GAME_TICK * 150);
		}
	}
}

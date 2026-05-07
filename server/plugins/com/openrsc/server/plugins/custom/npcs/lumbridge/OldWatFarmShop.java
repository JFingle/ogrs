package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.Shop;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.AbstractShop;

/**
 * Old Wat's Farming Supplies — east-of-Lumbridge allotment.
 *
 * Now stocks the real OGRS farming items (Rake, Potato Seed, Compost)
 * alongside upstream's gardening tools and water sources. The OGRS items
 * come from the content/items YAML pipeline — see content/items/rake.yaml
 * etc. and `tools/codegen-client-items.py`.
 *
 * Talk-to is owned by BoazTheFarmer (the renamed plugin, NPC id 837).
 * Right-click "Trade" opens the shop directly. Same pattern as the
 * other Lumbridge villager shops (Edith / Garth / Marigold) and the
 * Slayer master shop.
 */
public final class OldWatFarmShop extends AbstractShop {

	public static final String NAME = "Old Wat's Farming Supplies";
	public static final int OWNER_NPC_ID = 837;

	private final Item[] stock = new Item[]{
		// OGRS farming kit (content/items/*.yaml).
		new Item(ItemId.OGRS_RAKE.id(), 5),
		new Item(ItemId.OGRS_POTATO_SEED.id(), 25),
		new Item(ItemId.OGRS_ONION_SEED.id(), 20),
		new Item(ItemId.OGRS_TOMATO_SEED.id(), 15),
		new Item(ItemId.OGRS_COMPOST.id(), 15),
		// Upstream gardening tools + water sources.
		new Item(ItemId.SPADE.id(), 3),
		new Item(ItemId.TROWEL.id(), 3),
		new Item(ItemId.WATERING_CAN.id(), 3),
		new Item(ItemId.EMPTY_WATERING_CAN.id(), 3),
		new Item(ItemId.SHEARS.id(), 5),
		new Item(ItemId.BUCKET.id(), 10),
		new Item(ItemId.POTATO.id(), 5),
	};

	private final Shop baseShop = new Shop(false, 30000, 130, 40, 3, stock);
	private final Shop shop = new Shop(baseShop, NAME, OWNER_NPC_ID);

	@Override public Shop[] getShops(World w) { return new Shop[]{shop}; }
	@Override public boolean isMembers() { return false; }
	@Override public Shop getShop() { return shop; }
	@Override public boolean blockTalkNpc(Player p, Npc n) { return false; }
	@Override public void onTalkNpc(Player p, Npc n) { /* not used */ }
	@Override public boolean blockOpNpc(Player p, Npc n, String c) {
		return n.getID() == OWNER_NPC_ID && "Trade".equalsIgnoreCase(c);
	}
}

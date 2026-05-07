package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.Shop;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.AbstractShop;

/**
 * Lydia's Cloth & Leather — Lumbridge market. Crafting essentials plus
 * starter leather armour for new adventurers.
 */
public final class LydiaCloth extends AbstractShop {
	public static final String NAME = "Lydia's Cloth & Leather";
	public static final int OWNER_NPC_ID = 851;

	private final Item[] stock = new Item[]{
		new Item(ItemId.NEEDLE.id(), 10),
		new Item(ItemId.THREAD.id(), 20),
		new Item(ItemId.LEATHER_ARMOUR.id(), 5),
		new Item(ItemId.LEATHER_GLOVES.id(), 5),
		new Item(ItemId.SHEARS.id(), 3),
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

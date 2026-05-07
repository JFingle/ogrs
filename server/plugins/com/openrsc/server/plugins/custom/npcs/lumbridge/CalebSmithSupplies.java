package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.Shop;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.AbstractShop;

/**
 * Caleb's Smithing Supplies — Lumbridge village. Hammers, chisels, tinder,
 * buckets, pots — the basic toolkit any new adventurer needs but RSC's
 * default Lumbridge general store doesn't always carry in stock.
 */
public final class CalebSmithSupplies extends AbstractShop {
	public static final String NAME = "Caleb's Smithing Supplies";
	public static final int OWNER_NPC_ID = 848;

	private final Item[] stock = new Item[]{
		new Item(ItemId.HAMMER.id(), 5),
		new Item(ItemId.CHISEL.id(), 5),
		new Item(ItemId.TINDERBOX.id(), 5),
		new Item(ItemId.BUCKET.id(), 10),
		new Item(ItemId.POT.id(), 10),
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

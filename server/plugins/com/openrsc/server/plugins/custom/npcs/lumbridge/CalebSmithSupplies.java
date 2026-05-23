package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.OgrsNpcId;
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
	public static final String NAME = "Garth's Smithing Supplies";
	public static final int OWNER_NPC_ID = OgrsNpcId.GARTH.id();

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

	// OGRS — Talk-to dialog (sparky 2026-05-19: NPCs need character).
	@Override public boolean blockTalkNpc(Player p, Npc n) { return n.getID() == OWNER_NPC_ID; }
	@Override public void onTalkNpc(Player p, Npc n) {
		com.openrsc.server.plugins.Functions.npcsay(p, n,
			"A hammer in every pack and a chisel for every stone, friend.",
			"Lumbridge crowd thinks the real smith's in Varrock. They're not wrong, but I make do.");
		final int opt = com.openrsc.server.plugins.Functions.multi(p, n,
			"Show me what you've got.",
			"Why isn't the real smith here?",
			"Just looking around, thanks.");
		if (opt == 0) {
			p.setAccessingShop(shop);
			com.openrsc.server.net.rsc.ActionSender.showShop(p, shop);
		} else if (opt == 1) {
			com.openrsc.server.plugins.Functions.npcsay(p, n,
				"Varrock's got the ore, the coal, and the customers.",
				"I sell the toolkit. They sell the finished blade.",
				"Honest work either way — just different scales.");
		}
	}
	@Override public boolean blockOpNpc(Player p, Npc n, String c) {
		return n.getID() == OWNER_NPC_ID && "Trade".equalsIgnoreCase(c);
	}
}

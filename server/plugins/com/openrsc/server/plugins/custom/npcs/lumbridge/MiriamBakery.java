package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.Shop;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.AbstractShop;

/**
 * Miriam's Bakery — Lumbridge village square. Talk-to handled by
 * OgrsAmbientVillagers; right-click "Trade" opens the shop.
 */
public final class MiriamBakery extends AbstractShop {
	public static final String NAME = "Edith's Bakery";
	public static final int OWNER_NPC_ID = 838;

	private final Item[] stock = new Item[]{
		new Item(ItemId.BREAD.id(), 10),
		new Item(ItemId.CAKE.id(), 5),
		new Item(ItemId.POT_OF_FLOUR.id(), 10),
		new Item(ItemId.EGG.id(), 10),
		new Item(ItemId.MILK.id(), 5),
		new Item(ItemId.POT.id(), 5),
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
			"Morning, dear! Mind the flour — it's everywhere today.",
			"Lord knows what they're doing at the mill — the price keeps creeping up.");
		final int opt = com.openrsc.server.plugins.Functions.multi(p, n,
			"What's for sale today?",
			"Tell me about the village.",
			"Just saying hello.");
		if (opt == 0) {
			p.setAccessingShop(shop);
			com.openrsc.server.net.rsc.ActionSender.showShop(p, shop);
		} else if (opt == 1) {
			com.openrsc.server.plugins.Functions.npcsay(p, n,
				"Old Wat's down at the allotment — bring him decent dirt and he'll talk all day.",
				"The smith's lad keeps a stall now, sweet boy.",
				"Mind the swamp south of here. The frogs are louder than they ought to be.");
		}
	}
	@Override public boolean blockOpNpc(Player p, Npc n, String c) {
		return n.getID() == OWNER_NPC_ID && "Trade".equalsIgnoreCase(c);
	}
}

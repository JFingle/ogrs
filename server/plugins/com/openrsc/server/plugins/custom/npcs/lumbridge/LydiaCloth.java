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
 * Lydia's Cloth & Leather — Lumbridge market. Crafting essentials plus
 * starter leather armour for new adventurers.
 */
public final class LydiaCloth extends AbstractShop {
	public static final String NAME = "Marigold's Cloth & Leather";
	public static final int OWNER_NPC_ID = OgrsNpcId.MARIGOLD.id();

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

	// OGRS — Talk-to dialog (sparky 2026-05-19: NPCs need character).
	@Override public boolean blockTalkNpc(Player p, Npc n) { return n.getID() == OWNER_NPC_ID; }
	@Override public void onTalkNpc(Player p, Npc n) {
		com.openrsc.server.plugins.Functions.npcsay(p, n,
			"Careful with my dye, friend — that's woad, all the way from the north.",
			"A bit of needle and thread will keep you alive longer than a poor sword will.");
		final int opt = com.openrsc.server.plugins.Functions.multi(p, n,
			"Let me see your goods.",
			"How does one make armour?",
			"Just looking, thank you.");
		if (opt == 0) {
			p.setAccessingShop(shop);
			com.openrsc.server.net.rsc.ActionSender.showShop(p, shop);
		} else if (opt == 1) {
			com.openrsc.server.plugins.Functions.npcsay(p, n,
				"Cowhide first — tan it at the tanner up in Al-Kharid.",
				"Then needle, thread, and a steady hand. Patience does the rest.",
				"Don't try to rush it. The seam where you hurry is the seam that splits.");
		}
	}
	@Override public boolean blockOpNpc(Player p, Npc n, String c) {
		return n.getID() == OWNER_NPC_ID && "Trade".equalsIgnoreCase(c);
	}
}

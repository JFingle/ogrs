package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.NpcId;
import com.openrsc.server.model.Shop;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.AbstractShop;

/**
 * The Grizzled Traveler's shop. Stocked with mid-tier combat consumables so
 * a player taking on a slayer task has a place to gear up.
 *
 * Registered with the world via {@link AbstractShop#getShops(World)} which
 * the PluginHandler calls during init. Talk-to and right-click "Trade" are
 * BOTH suppressed here ({@link #blockTalkNpc} returns false) — the
 * {@link com.openrsc.server.plugins.custom.npcs.lumbridge.GrizzledTraveler}
 * dialog plugin owns Grizzled's interaction surface, and gates the shop
 * open behind a "Browse your supplies" multi-choice option so the player
 * sees the slayer dialog first.
 *
 * The shop is looked up at click time via the player's world shop list so
 * the dialog plugin doesn't need a static reference.
 */
public final class SlayerShop extends AbstractShop {

	public static final String NAME = "Grizzled Traveler's Supplies";
	public static final int OWNER_NPC_ID = 836; // Grizzled Traveler

	private final Item[] stock = new Item[]{
		new Item(ItemId.BRONZE_DAGGER.id(), 5),
		new Item(ItemId.BRONZE_SHORT_SWORD.id(), 5),
		new Item(ItemId.IRON_SHORT_SWORD.id(), 3),
		new Item(ItemId.LEATHER_ARMOUR.id(), 4),
		new Item(ItemId.LEATHER_GLOVES.id(), 4),
		new Item(ItemId.BREAD.id(), 10),
	};

	// Shop(general, respawnRateMillis, buyModifier%, sellModifier%, priceModifier, items...)
	// Then wrap with the copy-constructor to attach name + owner ids.
	private final Shop baseShop = new Shop(false, 30000, 130, 40, 3, stock);
	private final Shop shop = new Shop(baseShop, NAME, OWNER_NPC_ID);

	@Override
	public Shop[] getShops(final World world) {
		return new Shop[]{shop};
	}

	@Override
	public boolean isMembers() {
		return false;
	}

	@Override
	public Shop getShop() {
		return shop;
	}

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		// Hand off Talk-to entirely to GrizzledTraveler.java — it gates the
		// shop open behind a multi-choice, so the slayer-task flow is the
		// primary interaction.
		return false;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		// Never invoked — blockTalkNpc returns false, gating dispatch off.
		// AbstractShop's TalkNpcTrigger contract requires the method to exist.
	}

	@Override
	public boolean blockOpNpc(final Player player, final Npc n, final String command) {
		// Override AbstractShop's default (which delegates to blockTalkNpc).
		// We DO want the right-click "Trade" command to fire onOpNpc so the
		// shop opens directly without going through the dialog. Talk-to is
		// not an Op command, so it isn't gated here.
		return n.getID() == OWNER_NPC_ID && "Trade".equalsIgnoreCase(command);
	}
}

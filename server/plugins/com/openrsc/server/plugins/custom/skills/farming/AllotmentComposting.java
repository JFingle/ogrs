package com.openrsc.server.plugins.custom.skills.farming;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.Point;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.UseLocTrigger;

/**
 * OGRS Farming — UseLoc handler for "use Compost on an Allotment Bed."
 *
 * Composting is the third verb in the OSRS-style flow (Rake → Compost →
 * Plant → Harvest). Optional; planting straight on an empty bed still
 * works, just without the yield bonus.
 *
 * Mechanics:
 *   - Empty Bed (1301) + use Compost   → Composted Bed (1306), consume 1 compost.
 *   - Composted Bed (1306) + use Compost → message: already composted (no-op).
 *
 * Composted beds accept seeds via {@link AllotmentSeedPlanting}. The
 * planting code marks the tile in {@link AllotmentPatch#boostedTiles},
 * and the harvest path reads that flag to roll a max-yield bonus before
 * clearing it. Per-tile state is in-memory only (lost on restart) — the
 * persistence pass that solves growth-time also persists boost flags.
 */
public final class AllotmentComposting implements UseLocTrigger {

	private static final int EMPTY_BED_ID = 1301;
	private static final int COMPOSTED_BED_ID = 1306;

	@Override
	public boolean blockUseLoc(final Player player, final GameObject obj, final Item item) {
		if (item.getCatalogId() != ItemId.OGRS_COMPOST.id()) return false;
		final int id = obj.getID();
		return id == EMPTY_BED_ID || id == COMPOSTED_BED_ID;
	}

	@Override
	public void onUseLoc(final Player player, final GameObject obj, final Item item) {
		if (obj.getID() == COMPOSTED_BED_ID) {
			player.message("@yel@This bed is already dressed with compost.");
			return;
		}
		// Belt-and-suspenders re-check: if another player just planted in
		// this tick the id won't be 1301 anymore.
		if (obj.getID() != EMPTY_BED_ID) {
			player.message("@yel@That bed isn't ready for compost.");
			return;
		}

		player.getCarriedItems().remove(new Item(ItemId.OGRS_COMPOST.id(), 1));

		final World world = player.getWorld();
		final Point loc = obj.getLocation();
		final int direction = obj.getDirection();
		final int type = obj.getType();
		final GameObject composted = new GameObject(world, loc, COMPOSTED_BED_ID, direction, type);
		world.replaceGameObject(obj, composted);
		ActionSender.sendSound(player, "filljug");

		player.message("@gre@You work compost into the soil. The earth darkens.");
		player.message("@gre@A seed in this bed will swell well.");
	}
}

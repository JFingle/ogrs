package com.openrsc.server.plugins.custom.skills.farming;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.UseLocTrigger;

/**
 * OGRS Farming — UseLoc handler for "use seed on empty allotment bed."
 *
 * The OSRS-style flow splits raking from planting: the player rakes the
 * weedy patch (handled by AllotmentPatch) to expose an Empty Allotment
 * Bed, then drops a specific seed onto it to choose what grows. This
 * trigger is the second half of that handshake.
 *
 * Recognized seeds → (growing-id, ready-id) pairs:
 *   OGRS_POTATO_SEED → AllotmentPatch.POTATO_PAIR
 *   OGRS_ONION_SEED  → AllotmentPatch.ONION_PAIR
 *   OGRS_TOMATO_SEED → AllotmentPatch.TOMATO_PAIR
 *
 * Adding a new crop is two YAML files (growing + ready scenery), one
 * item YAML (the seed), an ItemId enum entry, and one line here in the
 * pair lookup. The growth-tick + harvest XP are shared.
 */
public final class AllotmentSeedPlanting implements UseLocTrigger {

	@Override
	public boolean blockUseLoc(final Player player, final GameObject obj, final Item item) {
		final int id = obj.getID();
		final boolean isPlantableBed = id == AllotmentPatch.EMPTY_BED_ID || id == AllotmentPatch.COMPOSTED_BED_ID;
		return isPlantableBed && pairFor(item.getCatalogId()) != null;
	}

	@Override
	public void onUseLoc(final Player player, final GameObject obj, final Item item) {
		final int[] pair = pairFor(item.getCatalogId());
		if (pair == null) return; // belt-and-suspenders; blockUseLoc already filtered

		// Double-check the bed is still plantable before consuming the seed —
		// avoids losing a seed if another player planted in the same tick.
		final int id = obj.getID();
		if (id != AllotmentPatch.EMPTY_BED_ID && id != AllotmentPatch.COMPOSTED_BED_ID) {
			player.message("@yel@That bed isn't ready for planting.");
			return;
		}

		// If planting on a composted bed, mark the tile so the harvest path
		// rolls a yield bonus. Marker is on the tile, not the obj — both bed
		// states get swapped to a growing state immediately.
		if (id == AllotmentPatch.COMPOSTED_BED_ID) {
			AllotmentPatch.markBoosted(obj.getLocation());
		}

		player.getCarriedItems().remove(new Item(item.getCatalogId(), 1));
		AllotmentPatch.startGrowing(player, obj, pair);
		player.message("@gre@You press the seed into the turned earth.");
		player.message("@gre@Give it a few minutes to take root.");
	}

	private static int[] pairFor(final int seedId) {
		if (seedId == ItemId.OGRS_POTATO_SEED.id()) return AllotmentPatch.POTATO_PAIR;
		if (seedId == ItemId.OGRS_ONION_SEED.id())  return AllotmentPatch.ONION_PAIR;
		if (seedId == ItemId.OGRS_TOMATO_SEED.id()) return AllotmentPatch.TOMATO_PAIR;
		return null;
	}
}

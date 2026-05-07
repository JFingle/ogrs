package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import java.util.Random;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Boaz the Farmer (NPC 850). First Farming-skill gameplay loop —
 * Layer 1 of the rich farming design (memory item #14).
 *
 * Boaz lets the player "plant a row" in his allotment via dialog. State
 * is per-player in player.getCache(): ogrs_farm_plant_at = epoch millis
 * when planted. After GROWTH_MS real-time has elapsed, the row is
 * "ready" and the player can harvest for potatoes + Farming XP.
 *
 * No seed item required for MVP. No scenery — Boaz IS the patch
 * interface. State persists across logout (player_cache row).
 *
 * Future layers (memory #14 layers 2-9) will add:
 *   * Spatial patches via the scenery pipeline (#23)
 *   * Soil quality, tending, companion planting
 *   * Sacred crops (fig, olive, wheat, vine, mustard seed)
 *   * Field hands paid to tend while away
 *   * Patch upgrades (fence, scarecrow, irrigation)
 *
 * Boaz is removed from {@link OgrsAmbientVillagers}'s switch so both
 * plugins don't fire on the same Talk-to. The ambient flavor about
 * "tell Ruth there's water by the gate" survives as one of the dialog
 * branches here.
 */
public class BoazTheFarmer implements TalkNpcTrigger {

	// NPC: Old Wat the Farmer (renamed from "Boaz" for the project-identity
	// pivot — themes over biblical names). Class file kept its original
	// name; only the in-game NPC display name + id changed.
	private static final int NPC_ID = 837;

	private static final String CACHE_PLANT_AT = "ogrs_farm_plant_at";
	/** Real-time growth duration. 30 seconds for testing; later layers
	 *  scale this per-crop and per-soil-quality. */
	private static final long GROWTH_MS = 30_000L;

	/** Yield range — random N potatoes per harvest. */
	private static final int HARVEST_MIN = 3;
	private static final int HARVEST_MAX = 6;
	/** Farming XP (display units) granted per potato harvested. */
	private static final int XP_PER_POTATO_DISPLAY = 8;

	private static final Random rng = new Random();

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		return n.getID() == NPC_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		final long now = System.currentTimeMillis();
		final boolean isPlanted = player.getCache().hasKey(CACHE_PLANT_AT);
		final long plantedAt = isPlanted ? player.getCache().getLong(CACHE_PLANT_AT) : 0L;
		final long elapsed = isPlanted ? now - plantedAt : 0L;
		final long remaining = isPlanted ? Math.max(0L, GROWTH_MS - elapsed) : 0L;
		final boolean isMature = isPlanted && elapsed >= GROWTH_MS;

		if (!isPlanted) {
			handleEmpty(player, n);
		} else if (!isMature) {
			handleGrowing(player, n, remaining);
		} else {
			handleMature(player, n);
		}
	}

	// ==================== Empty patch ====================

	private void handleEmpty(final Player player, final Npc n) {
		npcsay(player, n,
			"Working the long field today. Plenty more rows to tend.",
			"Could use a hand if you've a moment to spare.");

		final int option = multi(player, n,
			"I'll plant a row for you.",
			"What do you grow here?",
			"Goodbye.");

		if (option == 0) {
			player.getCache().store(CACHE_PLANT_AT, System.currentTimeMillis());
			npcsay(player, n,
				"Aye — that row at the back. Press the seedlings in firm.",
				"Come back in a few minutes and we'll see how they're settling.");
			player.message("@gre@You plant a row of potatoes. They'll be ready to harvest soon.");
		} else if (option == 1) {
			npcsay(player, n,
				"Mostly potatoes, friend. Hardy. They forgive a busy man.",
				"In good soil with steady hands you'll get a fine yield.",
				"There's other crops about the wider lands — herbs, fruit, the sacred trees up north.",
				"All in good time.");
		} else {
			npcsay(player, n, "Walk well.");
		}
	}

	// ==================== Growing ====================

	private void handleGrowing(final Player player, final Npc n, final long remainingMs) {
		final long secondsLeft = (remainingMs + 999L) / 1000L;
		npcsay(player, n,
			"Your row is coming along.",
			"Give 'em another " + secondsLeft + " seconds or so before pulling.");

		final int option = multi(player, n,
			"I'll wait.",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"Wisdom in waiting. Most things worth growing don't hurry.");
		} else {
			npcsay(player, n, "Walk well.");
		}
	}

	// ==================== Mature — harvest ====================

	private void handleMature(final Player player, final Npc n) {
		npcsay(player, n,
			"Look at that — your row's ready.",
			"Pull what you've earned.");

		final int option = multi(player, n,
			"Harvest the potatoes.",
			"I'll come back later.",
			"Goodbye.");

		if (option == 0) {
			final int yield = HARVEST_MIN + rng.nextInt(HARVEST_MAX - HARVEST_MIN + 1);
			final int totalXp = yield * XP_PER_POTATO_DISPLAY;

			give(player, ItemId.POTATO.id(), yield);
			// Engine storage is ×4 display units (RSC convention).
			player.getSkills().addExperience(Skill.FARMING.id(), totalXp * 4);
			player.getCache().remove(CACHE_PLANT_AT);

			npcsay(player, n,
				"There you are — " + yield + " good potatoes.",
				"Plant another row whenever you're ready.");
			player.message("@gre@You harvest " + yield + " potatoes. +" + totalXp + " Farming XP.");
		} else if (option == 1) {
			npcsay(player, n,
				"They'll keep a while. Don't leave 'em too long though.");
		} else {
			npcsay(player, n, "Walk well.");
		}
	}
}

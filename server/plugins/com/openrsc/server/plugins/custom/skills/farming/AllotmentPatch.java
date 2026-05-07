package com.openrsc.server.plugins.custom.skills.farming;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.event.SingleEvent;
import com.openrsc.server.model.Point;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.triggers.OpLocTrigger;
import com.openrsc.server.util.rsc.DataConversions;

import static com.openrsc.server.plugins.Functions.give;
import static com.openrsc.server.plugins.Functions.ifheld;

/**
 * OGRS Farming — allotment plot state machine.
 *
 * Layer 2 of memory item #14: real spatial farming. The state of a plot is
 * intrinsic to the world (the GameObject id at the tile IS the state) — no
 * per-player or per-tile map; replaceGameObject is atomic. Multiplayer
 * concern: plots are shared world-state, so two players racing on one tile
 * is a known limitation until per-player patch claims land.
 *
 * Lifecycle (OSRS-style — this rewrite splits rake from plant):
 *   1296 Weedy Allotment  + Rake     →  1301 Empty Allotment Bed
 *   1301 Empty Allotment  + UseInv   →  1299/1302/1304 (per-seed growing)
 *      (UseInv handled by AllotmentSeedPlanting — a separate UseLocTrigger)
 *   1299/1302/1304 Growing + Inspect →  flavor only; growth event runs.
 *   1300/1303/1305 Ready  + Harvest  →  crop + Farming XP, swap → 1296.
 *
 * The Rake step now consumes only the rake's PRESENCE (rake stays — tools
 * are reusable). The seed is consumed at plant-time, not rake-time.
 *
 * Compost: small chance per harvest a clump comes up with the roots
 * (4-in-10). Layer 3 will gate yield on whether compost was applied to
 * the empty bed before planting.
 */
public class AllotmentPatch implements OpLocTrigger {

	private static final int WEEDY_PATCH_ID = 1296;
	private static final int EMPTY_BED_ID = 1301;

	// Per-crop growing/ready ids. The growing → ready promotion needs to
	// know which ready id to swap to, hence the 2-element pairs.
	static final int[] POTATO_PAIR = {1299, 1300};
	static final int[] ONION_PAIR  = {1302, 1303};
	static final int[] TOMATO_PAIR = {1304, 1305};

	/** Real-time growth in ticks. 30 ticks at 640ms = ~19 seconds — short
	 *  enough to test in one session. Backlog: tune to OSRS-ish (5–20 min
	 *  per stage) once a per-patch persistence layer lands so the timer
	 *  survives restarts. Sparky flagged: "seeds grow too fast." */
	static final int GROWTH_TICKS = 30;

	/** Display XP units per harvest. Engine stores ×4. */
	private static final int HARVEST_XP_DISPLAY = 8;

	/** Yield ranges per crop (inclusive). OSRS-style: a single Harvest
	 *  action represents picking the whole row, so the bag fills with a
	 *  randomised batch rather than one item per click. */
	private static final int POTATO_MIN_YIELD = 3, POTATO_MAX_YIELD = 6;
	private static final int ONION_MIN_YIELD  = 3, ONION_MAX_YIELD  = 5;
	private static final int TOMATO_MIN_YIELD = 3, TOMATO_MAX_YIELD = 5;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		final int id = obj.getID();
		return id == WEEDY_PATCH_ID || id == EMPTY_BED_ID || isGrowing(id) || isReady(id);
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		final int id = obj.getID();
		if (id == WEEDY_PATCH_ID && command.equalsIgnoreCase("rake")) {
			rake(player, obj);
		} else if (id == EMPTY_BED_ID && command.equalsIgnoreCase("inspect")) {
			player.message("@gre@The bed is bare and turned. Use a seed on it to plant.");
		} else if (isGrowing(id) && command.equalsIgnoreCase("inspect")) {
			player.message("@gre@The seedlings are still settling in. Give them a few minutes.");
		} else if (isReady(id) && command.equalsIgnoreCase("harvest")) {
			harvest(player, obj);
		}
	}

	static boolean isGrowing(final int id) {
		return id == POTATO_PAIR[0] || id == ONION_PAIR[0] || id == TOMATO_PAIR[0];
	}

	static boolean isReady(final int id) {
		return id == POTATO_PAIR[1] || id == ONION_PAIR[1] || id == TOMATO_PAIR[1];
	}

	private int harvestCropId(final int readyId) {
		if (readyId == POTATO_PAIR[1]) return ItemId.POTATO.id();
		if (readyId == ONION_PAIR[1])  return ItemId.ONION.id();
		if (readyId == TOMATO_PAIR[1]) return ItemId.TOMATO.id();
		return ItemId.NOTHING.id();
	}

	/** Random yield count for the given ready-state id, inclusive on both ends. */
	private int rollYield(final int readyId) {
		if (readyId == POTATO_PAIR[1]) return DataConversions.random(POTATO_MIN_YIELD, POTATO_MAX_YIELD);
		if (readyId == ONION_PAIR[1])  return DataConversions.random(ONION_MIN_YIELD,  ONION_MAX_YIELD);
		if (readyId == TOMATO_PAIR[1]) return DataConversions.random(TOMATO_MIN_YIELD, TOMATO_MAX_YIELD);
		return 1;
	}

	private void rake(final Player player, final GameObject obj) {
		if (!ifheld(player, ItemId.OGRS_RAKE.id())) {
			player.message("@yel@You need a rake to break this soil.");
			return;
		}
		final World world = player.getWorld();
		final Point loc = obj.getLocation();
		final int direction = obj.getDirection();
		final int type = obj.getType();

		final GameObject empty = new GameObject(world, loc, EMPTY_BED_ID, direction, type);
		world.replaceGameObject(obj, empty);
		player.message("@gre@You clear the weeds and turn the soil.");
		player.message("@gre@The bed is ready for a seed.");
	}

	private void harvest(final Player player, final GameObject obj) {
		final World world = player.getWorld();
		final Point loc = obj.getLocation();
		final int direction = obj.getDirection();
		final int type = obj.getType();
		final int readyId = obj.getID();

		final GameObject weedy = new GameObject(world, loc, WEEDY_PATCH_ID, direction, type);
		world.replaceGameObject(obj, weedy);

		final int cropId = harvestCropId(readyId);
		final int yield = rollYield(readyId);
		if (cropId != ItemId.NOTHING.id() && yield > 0) {
			// give() handles non-stackable items by adding `yield` separate
			// inventory entries, which is what we want for potato/onion/tomato.
			give(player, cropId, yield);
		}
		// 4-in-10 chance: compost clump comes up with the roots.
		// Layer-3: soil-quality scaling using compost as a planting input.
		if (DataConversions.random(1, 10) <= 4) {
			give(player, ItemId.OGRS_COMPOST.id(), 1);
			player.message("@gre@A clump of dark compost comes up with the roots.");
		}
		// XP scales with the size of the haul — harder to harvest more.
		player.getSkills().addExperience(Skill.FARMING.id(), HARVEST_XP_DISPLAY * yield * 4);
		player.message("@gre@You pull " + yield + " from the row.");
		player.message("@gre@+" + (HARVEST_XP_DISPLAY * yield) + " Farming XP. The bed is overgrown again.");
	}

	/**
	 * Used by AllotmentSeedPlanting after consuming a seed: swap the empty
	 * bed visually to the matching growing-state and schedule maturity.
	 */
	static void startGrowing(final Player player, final GameObject empty, final int[] cropPair) {
		final World world = player.getWorld();
		final Point loc = empty.getLocation();
		final int direction = empty.getDirection();
		final int type = empty.getType();

		final GameObject growing = new GameObject(world, loc, cropPair[0], direction, type);
		world.replaceGameObject(empty, growing);

		world.getServer().getGameEventHandler().add(
			new SingleEvent(world, null, GROWTH_TICKS, "OGRS Farming - allotment maturity") {
				@Override
				public void action() {
					final GameObject current = world.getRegionManager()
						.getRegion(loc).getGameObject(loc, null);
					if (current != null && current.getID() == cropPair[0]) {
						final GameObject ready = new GameObject(world, loc, cropPair[1], direction, type);
						world.replaceGameObject(current, ready);
					}
				}
			}
		);
	}
}

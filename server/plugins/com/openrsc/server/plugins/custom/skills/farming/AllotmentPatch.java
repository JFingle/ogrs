package com.openrsc.server.plugins.custom.skills.farming;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.event.SingleEvent;
import com.openrsc.server.model.Point;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

import static com.openrsc.server.plugins.Functions.give;

/**
 * OGRS Farming — spatial allotment patch state machine. First piece of
 * Layer 2 of memory item #14 (real spatial farming).
 *
 * Three OGRS scenery defs the server swaps between for one tile:
 *   1296 Allotment Patch  (mudpatch)     → command "Rake"     (empty)
 *   1299 Allotment        (dugupsoil1)   → command "Inspect"  (growing)
 *   1300 Allotment        (potatoplant)  → command "Harvest"  (ready)
 *
 * Lifecycle:
 *   EMPTY  + Rake     → swap to GROWING, schedule maturity tick.
 *   GROWING + Inspect → flavor message; growth event already running.
 *   READY  + Harvest  → swap back to EMPTY, give 1 potato + Farming XP.
 *
 * State is intrinsic to the world (the GameObject id at the tile IS the
 * state). No separate per-player or per-tile state map needed for MVP —
 * the visible scenery is the source of truth, and replaceGameObject is
 * atomic. Single-player dev concern only; multiplayer needs per-player
 * patches but that depends on the spatial-patch-claim system (memory #14
 * Layer 2 follow-on).
 *
 * Items pipeline isn't built yet, so for MVP "Rake" stands in for the
 * full rake → compost → plant cycle. When the items pipeline lands,
 * this plugin gates on having a Rake + Potato Seed in inventory.
 */
public class AllotmentPatch implements OpLocTrigger {

	private static final int EMPTY_PATCH_ID = 1296;
	private static final int GROWING_PATCH_ID = 1299;
	private static final int READY_PATCH_ID = 1300;

	/** Real-time growth in ticks. 30 ticks at 640ms = ~19 seconds — short
	 *  enough to test in one session; future Layer-3 soil-quality scaling
	 *  multiplies this per-patch. */
	private static final int GROWTH_TICKS = 30;

	/** Display XP units per harvested potato. Engine stores ×4. */
	private static final int HARVEST_XP_DISPLAY = 8;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		final int id = obj.getID();
		return id == EMPTY_PATCH_ID || id == GROWING_PATCH_ID || id == READY_PATCH_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		switch (obj.getID()) {
			case EMPTY_PATCH_ID:
				if (command.equalsIgnoreCase("rake")) {
					plant(player, obj);
				}
				break;
			case GROWING_PATCH_ID:
				if (command.equalsIgnoreCase("inspect")) {
					player.message("@gre@The seedlings are still settling in. Give them a few minutes.");
				}
				break;
			case READY_PATCH_ID:
				if (command.equalsIgnoreCase("harvest")) {
					harvest(player, obj);
				}
				break;
		}
	}

	private void plant(final Player player, final GameObject obj) {
		final World world = player.getWorld();
		final Point loc = obj.getLocation();
		final int direction = obj.getDirection();
		final int type = obj.getType();

		// Swap mudpatch → growing visually.
		final GameObject growing = new GameObject(world, loc, GROWING_PATCH_ID, direction, type);
		world.replaceGameObject(obj, growing);
		player.message("@gre@You rake the soil and press a seedling into the row.");
		player.message("@gre@Give it a few minutes to take root.");

		// Schedule maturity. The tick handler looks up whatever is currently
		// at the tile — if someone harvested then re-planted in the meantime,
		// or if the server-restart cleared the growing object, we no-op.
		world.getServer().getGameEventHandler().add(
			new SingleEvent(world, null, GROWTH_TICKS, "OGRS Farming - patch maturity") {
				@Override
				public void action() {
					final GameObject current = world.getRegionManager()
						.getRegion(loc).getGameObject(loc, null);
					if (current != null && current.getID() == GROWING_PATCH_ID) {
						final GameObject ready = new GameObject(world, loc, READY_PATCH_ID, direction, type);
						world.replaceGameObject(current, ready);
					}
				}
			}
		);
	}

	private void harvest(final Player player, final GameObject obj) {
		final World world = player.getWorld();
		final Point loc = obj.getLocation();
		final int direction = obj.getDirection();
		final int type = obj.getType();

		final GameObject mudpatch = new GameObject(world, loc, EMPTY_PATCH_ID, direction, type);
		world.replaceGameObject(obj, mudpatch);

		give(player, ItemId.POTATO.id(), 1);
		// Engine stores XP ×4 (RSC display convention).
		player.getSkills().addExperience(Skill.FARMING.id(), HARVEST_XP_DISPLAY * 4);

		player.message("@gre@You pull a potato from the row.");
		player.message("@gre@+" + HARVEST_XP_DISPLAY + " Farming XP. The bare soil is ready for another seedling.");
	}
}

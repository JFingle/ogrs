package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpInvTrigger;

/**
 * OGRS Slayer Enchanted Gem (#12) — portable task-progress readout.
 *
 * Right-click "Rub" on the gem from inventory; the gem reports the
 * player's current slayer task (or its absence) without forcing a
 * round trip to the Grizzled Traveler. Reads cache state via
 * {@link SlayerService}; no persistence of its own.
 *
 * Item YAML at {@code content/items/slayer_enchanted_gem.yaml} declares
 * the "Rub" command verb. The engine's inventory action dispatch sends
 * the verb here as the {@code command} parameter; we match case-
 * insensitively against "rub".
 */
public final class SlayerGem implements OpInvTrigger {

	private static final int GEM_ID = ItemId.OGRS_SLAYER_GEM.id();

	@Override
	public boolean blockOpInv(final Player player, final Integer invIndex, final Item item, final String command) {
		return item.getCatalogId() == GEM_ID && command != null && command.equalsIgnoreCase("rub");
	}

	@Override
	public void onOpInv(final Player player, final Integer invIndex, final Item item, final String command) {
		final int slayerLevel = SlayerService.getPlayerLevel(player);
		final SlayerData task = SlayerService.getActiveTask(player);

		if (task == null) {
			player.message("The gem is dim. You hear a faint voice: 'Come and see me when you're ready for a task.'");
			player.message("Your Slayer level is " + slayerLevel + ".");
			return;
		}

		if (task.isComplete()) {
			player.message("The gem pulses warmly. 'You've done what I asked. Return for your reward.'");
			player.message("Task: " + task.npcName + " — complete.");
			return;
		}

		final int done = task.total - task.remaining;
		player.message("The gem hums softly. You hear: 'You have " + task.remaining + " " + task.npcName
			+ " left to slay.'");
		player.message("Task: " + done + "/" + task.total + "  |  Slayer level: " + slayerLevel + ".");
	}
}

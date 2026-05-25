package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.contracts.Contract;
import com.openrsc.server.plugins.custom.contracts.ContractRegistry;
import com.openrsc.server.plugins.triggers.OpLocTrigger;

import java.util.List;

/**
 * OGRS — Job Board interaction (Phase 1B + 1C). Scenery id 1326 in
 * Lumbridge castle courtyard. Right-click commands:
 *
 *   View — context-aware:
 *     * If you have items to collect (employer of a completed contract)
 *       → collect them (added to bank).
 *     * If you have an active contract and the required items in your
 *       inventory → deliver them and claim the gold.
 *     * Otherwise → list up to 10 most-recent open contracts in chat.
 *   Post — points the player at the ::contract post chat command for
 *     v1. A full posting UI ships in a later phase.
 *
 * All contract storage lives in ContractRegistry (in-memory for v1).
 */
public final class OgrsJobBoard implements OpLocTrigger {

	private static final int BOARD_ID = 1326;

	@Override
	public boolean blockOpLoc(final Player player, final GameObject obj, final String command) {
		return obj.getID() == BOARD_ID;
	}

	@Override
	public void onOpLoc(final Player player, final GameObject obj, final String command) {
		if (obj.getID() != BOARD_ID) return;

		if ("post".equalsIgnoreCase(command)) {
			player.message("@gre@To post a contract:");
			player.message("  @whi@::contract post <itemId> <amount> <gold> <hours>");
			player.message("Gold escrows immediately. ::contract list to see what others posted.");
			return;
		}

		// "View" — context-aware.
		// Priority 1a: mentor's payout from completed mentorships.
		final int mentorGold = ContractRegistry.collectMentorPayout(player.getUsername());
		if (mentorGold > 0) {
			player.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), mentorGold));
			player.message("@gre@Collected " + mentorGold + "gp in mentorship payouts.");
			return;
		}
		// Priority 1b: collect pending deliveries (employer's reward from resource contracts).
		final List<Contract> ready = ContractRegistry.readyForCollection(player.getUsername());
		if (!ready.isEmpty()) {
			collectPending(player, ready);
			return;
		}
		// Priority 2: deliver an active resource contract if items are on hand.
		final Contract active = ContractRegistry.activeForWorker(player.getUsername());
		if (active != null && active.type == Contract.Type.RESOURCE_DELIVERY
			&& player.getCarriedItems().getInventory().countId(active.itemId) >= active.itemAmount) {
			deliver(player, active);
			return;
		}
		// Priority 3: list open contracts.
		listOpen(player, active);
	}

	private static void collectPending(final Player employer, final List<Contract> ready) {
		int collected = 0;
		for (Contract c : ready) {
			final Item[] items = ContractRegistry.collect(c);
			if (items == null) continue;
			for (Item it : items) {
				// Add directly to inventory if room, else drop on the board tile.
				if (employer.getCarriedItems().getInventory().getFreeSlots() > 0) {
					employer.getCarriedItems().getInventory().add(it);
				} else {
					employer.getWorld().registerItem(
						new com.openrsc.server.model.entity.GroundItem(
							employer.getWorld(), it.getCatalogId(), employer.getX(), employer.getY(),
							it.getAmount(), employer),
						employer.getConfig().GAME_TICK * 150);
					employer.message("@yel@Inventory full — " + it.getAmount() + " of item " + it.getCatalogId()
						+ " dropped at your feet.");
				}
			}
			collected++;
		}
		employer.message("@gre@Collected " + collected + " completed contract(s).");
	}

	private static void deliver(final Player worker, final Contract c) {
		final int need = c.itemAmount;
		worker.getCarriedItems().getInventory().remove(new Item(c.itemId, need), true);
		worker.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), c.goldReward));
		ContractRegistry.markDelivered(c, new Item[]{ new Item(c.itemId, need) });
		worker.message("@gre@Delivered " + need + " of item " + c.itemId + " for " + c.goldReward + "gp.");
		worker.message("Employer @whi@" + c.posterName + "@gre@ can collect their goods here.");
	}

	private static void listOpen(final Player p, final Contract activeReminder) {
		if (activeReminder != null) {
			p.message("@yel@Active contract: " + ContractRegistry.summary(activeReminder));
			p.message("Bring the items here — the board will accept them automatically.");
			p.message("");
		}
		final List<Contract> open = ContractRegistry.listOpen();
		if (open.isEmpty()) {
			p.message("@yel@No open contracts. Post one with ::contract post.");
			return;
		}
		p.message("@gre@Open contracts (top 10) — accept with ::contract accept <id>:");
		int shown = 0;
		for (Contract c : open) {
			p.message("@yel@" + ContractRegistry.summary(c));
			if (++shown >= 10) break;
		}
	}
}

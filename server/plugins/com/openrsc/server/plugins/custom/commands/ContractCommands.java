package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.contracts.Contract;
import com.openrsc.server.plugins.custom.contracts.ContractRegistry;
import com.openrsc.server.plugins.triggers.CommandTrigger;

import java.util.List;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * OGRS — chat-command interface for the contract system. Phase 1C of
 * the housing/contract arc (sparky 2026-05-24).
 *
 * Posting + accepting + delivering via chat commands is the MVP UX.
 * A proper Job Board UI panel ships in a later phase, but this gets
 * the mechanic end-to-end testable in one session.
 *
 * Commands:
 *   ::contract post &lt;itemId&gt; &lt;amount&gt; &lt;gold&gt; &lt;hours&gt;
 *       Post a resource-delivery contract. Gold deducted from
 *       inventory immediately (escrow).
 *   ::contract list
 *       Show up to 10 most-recent open contracts.
 *   ::contract accept &lt;id&gt;
 *       Claim an open contract. Limit: one active contract per worker.
 *   ::contract deliver
 *       Worker must be at the Job Board with the required items in
 *       inventory. Use the board itself instead (right-click → Deliver).
 *       This command is a fallback for testing.
 *   ::contract status
 *       Show your active contract (worker side).
 *   ::contract cancel &lt;id&gt;
 *       Employer cancels an open contract. Gold refunded.
 *
 * Aliased ::jobs as a synonym for ::contract.
 */
public final class ContractCommands implements CommandTrigger {

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(), "contract", "contracts", "jobs");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		if (args.length == 0) {
			showHelp(player);
			return;
		}
		final String sub = args[0].toLowerCase();
		switch (sub) {
			case "post":    handlePost(player, args);    break;
			case "list":    handleList(player);          break;
			case "accept":  handleAccept(player, args);  break;
			case "deliver": handleDeliver(player);       break;
			case "status":  handleStatus(player);        break;
			case "cancel":  handleCancel(player, args);  break;
			default:        showHelp(player);
		}
	}

	private static void showHelp(final Player p) {
		p.message("@gre@Contracts — chat commands (MVP):");
		p.message("  ::contract post <itemId> <amt> <gold> <hours> — post resource delivery");
		p.message("  ::contract list — show open contracts");
		p.message("  ::contract accept <id> — claim one (1 active per worker)");
		p.message("  ::contract deliver — turn in items (at Job Board)");
		p.message("  ::contract status — show your active contract");
		p.message("  ::contract cancel <id> — refund a contract you posted");
	}

	private static void handlePost(final Player p, final String[] args) {
		if (args.length < 5) {
			p.message("Usage: ::contract post <itemId> <amount> <gold> <hours>");
			return;
		}
		final int itemId, amount, gold, hours;
		try {
			itemId = Integer.parseInt(args[1]);
			amount = Integer.parseInt(args[2]);
			gold   = Integer.parseInt(args[3]);
			hours  = Integer.parseInt(args[4]);
		} catch (NumberFormatException e) {
			p.message("All four args must be integers.");
			return;
		}
		if (amount <= 0 || gold <= 0 || hours <= 0 || hours > 168) {
			p.message("Bad args. Amount/gold/hours all > 0; hours <= 168 (1 week).");
			return;
		}
		// Escrow the gold from employer's inventory.
		final int coinsId = ItemId.COINS.id();
		if (p.getCarriedItems().getInventory().countId(coinsId) < gold) {
			p.message("@red@You don't have " + gold + " coins to escrow.");
			return;
		}
		p.getCarriedItems().getInventory().remove(new Item(coinsId, gold), true);
		final Contract c = ContractRegistry.post(p, itemId, amount, gold, hours);
		p.message("@gre@Contract #" + c.id + " posted. " + gold + "gp escrowed.");
		p.message("Workers can ::contract accept " + c.id + " to claim it.");
	}

	private static void handleList(final Player p) {
		final List<Contract> open = ContractRegistry.listOpen();
		if (open.isEmpty()) {
			p.message("@yel@No open contracts. Be the first to post one!");
			return;
		}
		p.message("@gre@Open contracts (top 10):");
		int shown = 0;
		for (Contract c : open) {
			p.message("@yel@" + ContractRegistry.summary(c));
			if (++shown >= 10) break;
		}
	}

	private static void handleAccept(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::contract accept <id>"); return; }
		final int id;
		try { id = Integer.parseInt(args[1]); } catch (NumberFormatException e) {
			p.message("Bad id."); return;
		}
		final Contract c = ContractRegistry.byId(id);
		if (c == null) { p.message("@red@Contract #" + id + " not found."); return; }
		if (c.posterName.equalsIgnoreCase(p.getUsername())) {
			p.message("@red@You can't accept your own contract.");
			return;
		}
		if (ContractRegistry.activeForWorker(p.getUsername()) != null) {
			p.message("@red@You already have an active contract. Finish or it'll expire.");
			return;
		}
		if (!ContractRegistry.accept(c, p)) {
			p.message("@red@Contract #" + id + " can't be accepted (already taken or closed).");
			return;
		}
		p.message("@gre@Accepted contract #" + id + ". Gather " + c.itemAmount + " of item " + c.itemId);
		p.message("then ::contract deliver at the Job Board to claim " + c.goldReward + "gp.");
	}

	static void handleDeliver(final Player p) {
		final Contract c = ContractRegistry.activeForWorker(p.getUsername());
		if (c == null) { p.message("@red@You have no active contract to deliver."); return; }
		final int need = c.itemAmount;
		final int have = p.getCarriedItems().getInventory().countId(c.itemId);
		if (have < need) {
			p.message("@red@Need " + need + " of item " + c.itemId + ", you have " + have + ".");
			return;
		}
		// Remove items, pay worker.
		p.getCarriedItems().getInventory().remove(new Item(c.itemId, need), true);
		p.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), c.goldReward));
		final Item[] delivered = new Item[]{ new Item(c.itemId, need) };
		ContractRegistry.markDelivered(c, delivered);
		p.message("@gre@Delivered " + need + " of item " + c.itemId + " for " + c.goldReward + "gp.");
		p.message("Employer @whi@" + c.posterName + "@gre@ can collect at the Job Board.");
	}

	private static void handleStatus(final Player p) {
		final Contract c = ContractRegistry.activeForWorker(p.getUsername());
		if (c == null) { p.message("You have no active contract."); return; }
		p.message("@gre@Active: " + ContractRegistry.summary(c));
		p.message("Bring " + c.itemAmount + " of item " + c.itemId + " to the Job Board, then ::contract deliver.");
	}

	private static void handleCancel(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::contract cancel <id>"); return; }
		final int id;
		try { id = Integer.parseInt(args[1]); } catch (NumberFormatException e) {
			p.message("Bad id."); return;
		}
		final Contract c = ContractRegistry.byId(id);
		if (c == null) { p.message("@red@Contract #" + id + " not found."); return; }
		if (!ContractRegistry.cancel(c, p.getUsername())) {
			p.message("@red@Can't cancel — either not yours or already accepted.");
			return;
		}
		p.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), c.goldReward));
		p.message("@gre@Cancelled #" + id + ". " + c.goldReward + "gp refunded.");
	}
}

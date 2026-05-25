package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.plots.Plot;
import com.openrsc.server.plugins.custom.plots.PlotRegistry;
import com.openrsc.server.plugins.triggers.CommandTrigger;

import java.util.List;
import java.util.Map;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * OGRS — chat-command interface for estate plots. Phase 1F-α/β.
 *
 *   ::plot list                  — all plots + status
 *   ::plot info &lt;id&gt;          — full details (owner, bids, tenancy)
 *   ::plot bid &lt;id&gt; &lt;gold&gt;  — place a bid; gold escrows immediately
 *   ::plot withdraw &lt;id&gt;      — refund your bid on a plot
 *   ::plot mine                  — info on the plot you own (if any)
 *   ::plot close &lt;id&gt;         — ADMIN: close the auction now, highest
 *                                  bidder wins, others refunded.
 *
 * Weekly auto-close cron lands in Phase 1F-β-2. For v1 sparky / admins
 * close auctions manually with ::plot close so the mechanic is
 * testable without waiting a week.
 */
public final class PlotCommands implements CommandTrigger {

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(), "plot", "plots", "estate");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		if (args.length == 0) { showHelp(player); return; }
		switch (args[0].toLowerCase()) {
			case "list":     handleList(player);          break;
			case "info":     handleInfo(player, args);    break;
			case "bid":      handleBid(player, args);     break;
			case "withdraw": handleWithdraw(player, args); break;
			case "mine":     handleMine(player);          break;
			case "build":    handleBuild(player, args);   break;
			case "close":    handleAdminClose(player, args); break;
			default:         showHelp(player);
		}
	}

	private static void showHelp(final Player p) {
		p.message("@gre@Plots — chat commands:");
		p.message("  ::plot list             — all 5 plots + status");
		p.message("  ::plot info <id>        — details on a plot");
		p.message("  ::plot bid <id> <gold>  — place a bid (escrowed)");
		p.message("  ::plot withdraw <id>    — refund your bid");
		p.message("  ::plot mine             — info on your owned plot");
		p.message("  ::plot build <type>     — build a feature on your plot");
		p.message("                            (types: bankchest — more coming)");
		p.message("  ::plot close <id>       — ADMIN: close auction now");
	}

	private static void handleList(final Player p) {
		final List<Plot> all = PlotRegistry.listAll();
		final long now = System.currentTimeMillis();
		p.message("@gre@Estate plots (" + all.size() + "):");
		for (Plot pl : all) {
			final String status = pl.isVacant(now)
				? "@yel@VACANT@gre@ (" + pl.openBids.size() + " bids)"
				: "@whi@owned by " + pl.deedHolder + "@gre@";
			p.message("  #" + pl.id + " @whi@" + pl.name + "@gre@ — " + pl.tier + " — " + status);
		}
	}

	private static void handleInfo(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::plot info <id>"); return; }
		final int id;
		try { id = Integer.parseInt(args[1]); } catch (NumberFormatException e) {
			p.message("Bad id."); return;
		}
		final Plot pl = PlotRegistry.byId(id);
		if (pl == null) { p.message("@red@No plot #" + id + "."); return; }
		showInfo(p, pl);
	}

	private static void showInfo(final Player p, final Plot pl) {
		final long now = System.currentTimeMillis();
		p.message("@gre@" + pl.name + " (Plot #" + pl.id + ")");
		p.message("  Tier: @whi@" + pl.tier + "@gre@   Theme: @whi@" + pl.themeHint);
		p.message("  Area: (" + pl.boxMinX + "," + pl.boxMinY + ")..(" + pl.boxMaxX + "," + pl.boxMaxY + ")");
		p.message("  Deed Pillar at: (" + pl.deedPillarX + "," + pl.deedPillarY + ")");
		p.message("  Feature slots: @whi@" + pl.tier.featureSlots() + "@gre@   Auction floor: @whi@" + pl.tier.auctionFloor() + "gp");
		if (pl.isVacant(now)) {
			p.message("  Status: @yel@VACANT — open for bidding");
			if (pl.openBids.isEmpty()) {
				p.message("  No bids yet. Place one with ::plot bid " + pl.id + " <amount>");
			} else {
				p.message("  Bids (highest first):");
				int rank = 1;
				for (Map.Entry<String, Integer> e : pl.bidsHighestFirst()) {
					p.message("    " + rank + ". @whi@" + e.getKey() + "@gre@ @ " + e.getValue() + "gp");
					if (rank++ >= 5) break;
				}
			}
		} else {
			final long hoursLeft = Math.max(0, (pl.tenancyExpiresMs - now) / 3600000L);
			p.message("  Owner: @whi@" + pl.deedHolder + "@gre@   Tenancy: @whi@" + hoursLeft + "h@gre@ remaining");
		}
	}

	private static void handleBid(final Player p, final String[] args) {
		if (args.length < 3) { p.message("Usage: ::plot bid <id> <gold>"); return; }
		final int id, amount;
		try {
			id = Integer.parseInt(args[1]);
			amount = Integer.parseInt(args[2]);
		} catch (NumberFormatException e) {
			p.message("Bad args."); return;
		}
		final Plot pl = PlotRegistry.byId(id);
		if (pl == null) { p.message("@red@No plot #" + id + "."); return; }
		final long now = System.currentTimeMillis();
		if (!pl.isVacant(now)) { p.message("@red@Plot is currently owned by @whi@" + pl.deedHolder + "@red@."); return; }
		if (amount < pl.tier.auctionFloor()) {
			p.message("@red@Bid below auction floor of " + pl.tier.auctionFloor() + "gp.");
			return;
		}
		// WILDERNESS plots are guild-only. Bidder must be FOUNDER/OFFICER
		// of a guild; deed holder becomes the guild name.
		if (pl.tier == Plot.Tier.WILDERNESS) {
			final com.openrsc.server.plugins.custom.guilds.Guild g =
				com.openrsc.server.plugins.custom.guilds.GuildRegistry.byMember(p.getUsername());
			if (g == null) {
				p.message("@red@Wilderness plots are guild-only. ::guild create one first.");
				return;
			}
			final com.openrsc.server.plugins.custom.guilds.Guild.Role role = g.roleOf(p.getUsername());
			if (role == null || !role.canManageEstate()) {
				p.message("@red@Only your guild's founder/officers can bid on wilderness plots.");
				return;
			}
		}
		// Refund any prior bid this player had on this plot.
		final int prior = PlotRegistry.withdrawBid(pl, p.getUsername());
		if (prior > 0) {
			p.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), prior));
			p.message("@yel@Refunded prior bid of " + prior + "gp.");
		}
		final int coinsId = ItemId.COINS.id();
		if (p.getCarriedItems().getInventory().countId(coinsId) < amount) {
			p.message("@red@You don't have " + amount + "gp to bid.");
			return;
		}
		p.getCarriedItems().getInventory().remove(new Item(coinsId, amount), true);
		if (!PlotRegistry.placeBid(pl, p.getUsername(), amount)) {
			// Shouldn't fail given the floor check, but refund just in case.
			p.getCarriedItems().getInventory().add(new Item(coinsId, amount));
			p.message("@red@Bid rejected.");
			return;
		}
		p.message("@gre@Bid " + amount + "gp on #" + pl.id + " '" + pl.name + "'.");
	}

	private static void handleWithdraw(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::plot withdraw <id>"); return; }
		final int id;
		try { id = Integer.parseInt(args[1]); } catch (NumberFormatException e) {
			p.message("Bad id."); return;
		}
		final Plot pl = PlotRegistry.byId(id);
		if (pl == null) { p.message("@red@No plot #" + id + "."); return; }
		final int refund = PlotRegistry.withdrawBid(pl, p.getUsername());
		if (refund == 0) { p.message("@yel@You have no bid on that plot."); return; }
		p.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), refund));
		p.message("@gre@Withdrew bid. Refunded " + refund + "gp.");
	}

	private static void handleMine(final Player p) {
		final Plot pl = PlotRegistry.byHolder(p.getUsername());
		if (pl == null) { p.message("@yel@You don't own a plot. Bid on one — ::plot list to see what's open."); return; }
		showInfo(p, pl);
	}

	private static void handleBuild(final Player p, final String[] args) {
		if (args.length < 2) {
			p.message("Usage: ::plot build <type>   (type: bankchest)");
			return;
		}
		final com.openrsc.server.plugins.custom.plots.PlotFeature.Type featureType;
		switch (args[1].toLowerCase()) {
			case "bankchest": case "bank":
				featureType = com.openrsc.server.plugins.custom.plots.PlotFeature.Type.BANK_CHEST;
				break;
			case "forge": case "anvil":
				featureType = com.openrsc.server.plugins.custom.plots.PlotFeature.Type.FORGE;
				break;
			default:
				p.message("@red@Unknown feature type. Try: bankchest, forge.");
				return;
		}

		final Plot pl = PlotRegistry.byHolder(p.getUsername());
		if (pl == null) { p.message("@red@You don't own a plot. Win an auction first."); return; }
		if (!pl.contains(p.getX(), p.getY())) {
			p.message("@red@You must be standing inside your plot (" + pl.boxMinX + "," + pl.boxMinY
				+ ")..(" + pl.boxMaxX + "," + pl.boxMaxY + ") to build.");
			return;
		}
		if (pl.features.size() >= pl.tier.featureSlots()) {
			p.message("@red@Plot is at its " + pl.tier.featureSlots() + " feature slot limit.");
			return;
		}
		if (pl.featureAt(p.getX(), p.getY()) != null) {
			p.message("@red@There's already a feature on this tile.");
			return;
		}
		final int constructionLvl = p.getSkills().getLevel(
			com.openrsc.server.constants.Skill.CONSTRUCTION.id());
		if (constructionLvl < featureType.minConstructionLevel) {
			p.message("@red@Need Construction level " + featureType.minConstructionLevel
				+ " to build " + featureType.displayName + " (you have " + constructionLvl + ").");
			return;
		}
		final int coinsId = ItemId.COINS.id();
		if (p.getCarriedItems().getInventory().countId(coinsId) < featureType.goldCost) {
			p.message("@red@Need " + featureType.goldCost + "gp in materials to build " + featureType.displayName + ".");
			return;
		}
		p.getCarriedItems().getInventory().remove(new Item(coinsId, featureType.goldCost), true);

		// Spawn the scenery + record the feature.
		final com.openrsc.server.model.Point loc = com.openrsc.server.model.Point.location(p.getX(), p.getY());
		final com.openrsc.server.model.entity.GameObject obj =
			new com.openrsc.server.model.entity.GameObject(p.getWorld(), loc, featureType.sceneryId, 0, 0);
		p.getWorld().registerGameObject(obj);
		final com.openrsc.server.plugins.custom.plots.PlotFeature pf =
			new com.openrsc.server.plugins.custom.plots.PlotFeature(pl.id, featureType, p.getX(), p.getY(), p.getUsername());
		pl.features.put(Plot.featureKey(p.getX(), p.getY()), pf);

		// Construction XP — 250 per level required, scales with feature tier.
		final int xp = featureType.minConstructionLevel * 250 * 4; // *4 = engine storage units
		p.getSkills().addExperience(com.openrsc.server.constants.Skill.CONSTRUCTION.id(), xp);
		p.message("@gre@Built " + featureType.displayName + " on your plot. Cost " + featureType.goldCost
			+ "gp. Right-click Use to access (deed-holder only).");
	}

	private static void handleAdminClose(final Player p, final String[] args) {
		if (!p.isAdmin()) { p.message("@red@Admin only."); return; }
		if (args.length < 2) { p.message("Usage: ::plot close <id>"); return; }
		final int id;
		try { id = Integer.parseInt(args[1]); } catch (NumberFormatException e) {
			p.message("Bad id."); return;
		}
		final Plot pl = PlotRegistry.byId(id);
		if (pl == null) { p.message("@red@No plot #" + id + "."); return; }
		// Snapshot loser bids before close so we can refund them.
		final java.util.List<Map.Entry<String, Integer>> sorted = pl.bidsHighestFirst();
		final Map.Entry<String, Integer> winner = PlotRegistry.closeAuction(pl);
		if (winner == null) { p.message("@yel@No bids on plot #" + id + "."); return; }
		// Refund the losers (winner's gold sinks into the server economy).
		for (int i = 1; i < sorted.size(); i++) {
			final Map.Entry<String, Integer> loser = sorted.get(i);
			final long hash = com.openrsc.server.util.rsc.DataConversions.usernameToHash(loser.getKey());
			final Player loserPlayer = p.getWorld().getPlayer(hash);
			if (loserPlayer != null) {
				loserPlayer.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), loser.getValue()));
				loserPlayer.message("@yel@Auction on '" + pl.name + "' closed. Refunded your " + loser.getValue() + "gp bid.");
			}
			// Offline losers — gold lost for v1 (real impl: mailbox).
		}
		// For WILDERNESS plots, rewrite deedHolder from the winning
		// player's username to their guild name.
		if (pl.tier == Plot.Tier.WILDERNESS) {
			final com.openrsc.server.plugins.custom.guilds.Guild g =
				com.openrsc.server.plugins.custom.guilds.GuildRegistry.byMember(winner.getKey());
			if (g != null) {
				pl.deedHolder = g.name;
				p.message("@gre@Auction closed. Winner: @whi@" + g.name + "@gre@ (via "
					+ winner.getKey() + ") @ " + winner.getValue() + "gp.");
			} else {
				// Winning bidder somehow left their guild between bid and close.
				// Refund instead.
				final long whash = com.openrsc.server.util.rsc.DataConversions.usernameToHash(winner.getKey());
				final Player wp = p.getWorld().getPlayer(whash);
				if (wp != null) {
					wp.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), winner.getValue()));
					wp.message("@yel@Wilderness auction skipped — you're no longer in a guild. " + winner.getValue() + "gp refunded.");
				}
				pl.deedHolder = null;
				p.message("@yel@Auction void: winning bidder is no longer in a guild.");
				return;
			}
		} else {
			p.message("@gre@Auction closed. Winner: @whi@" + winner.getKey() + "@gre@ @ " + winner.getValue() + "gp.");
		}
		// Notify the winner if online.
		final long hash = com.openrsc.server.util.rsc.DataConversions.usernameToHash(winner.getKey());
		final Player wp = p.getWorld().getPlayer(hash);
		if (wp != null) {
			wp.message("@gre@You won the deed to '" + pl.name + "' for " + winner.getValue() + "gp. Tenancy: 7 days.");
		}
	}
}

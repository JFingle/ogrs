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
			case "post":     handlePost(player, args);    break;
			case "mentor":   handleMentorPost(player, args); break;
			case "buildjob": handleBuildJobPost(player, args); break;
			case "build":    handleBuildExec(player);     break;
			case "bounty":   handleBountyPost(player, args); break;
			case "list":     handleList(player);          break;
			case "accept":   handleAccept(player, args);  break;
			case "deliver":  handleDeliver(player);       break;
			case "status":   handleStatus(player);        break;
			case "cancel":   handleCancel(player, args);  break;
			default:         showHelp(player);
		}
	}

	private static void showHelp(final Player p) {
		p.message("@gre@Contracts — chat commands (MVP):");
		p.message("  ::contract post <itemId> <amt> <gold> <hours> — resource delivery");
		p.message("  ::contract mentor <skillId> <minLvl> <bondHrs> <gold> <deadlineHrs>");
		p.message("    — mentorship: bonded play with apprentice");
		p.message("  ::contract buildjob <feature> <plotId> <targetX> <targetY> <gold> <hours>");
		p.message("    — pay a worker to build a feature on your plot (XP credits YOU)");
		p.message("  ::contract bounty <player> <gold> <hours>");
		p.message("    — bounty: anyone who kills <player> in the Wilderness collects the gold");
		p.message("  ::contract list   — show open contracts");
		p.message("  ::contract accept <id> — claim one (1 active per worker)");
		p.message("  ::contract deliver — turn in items (at Job Board)");
		p.message("  ::contract build   — execute a construction-job (worker, at target tile)");
		p.message("  ::contract status  — show your active contract");
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

	private static void handleMentorPost(final Player p, final String[] args) {
		if (args.length < 6) {
			p.message("Usage: ::contract mentor <skillId> <minLevel> <bondHrs> <gold> <deadlineHrs>");
			p.message("skillId: e.g. 14=Mining, 7=Cooking. See ::stats.");
			return;
		}
		final int skillId, minLevel, bondHrs, gold, deadlineHrs;
		try {
			skillId   = Integer.parseInt(args[1]);
			minLevel  = Integer.parseInt(args[2]);
			bondHrs   = Integer.parseInt(args[3]);
			gold      = Integer.parseInt(args[4]);
			deadlineHrs = Integer.parseInt(args[5]);
		} catch (NumberFormatException e) {
			p.message("All five args must be integers.");
			return;
		}
		if (minLevel < 1 || minLevel > 99 || bondHrs <= 0 || gold <= 0 || deadlineHrs <= 0 || deadlineHrs > 168) {
			p.message("Bad args. minLevel 1-99, bondHrs/gold/deadlineHrs all > 0, deadlineHrs <= 168.");
			return;
		}
		final int coinsId = com.openrsc.server.constants.ItemId.COINS.id();
		if (p.getCarriedItems().getInventory().countId(coinsId) < gold) {
			p.message("@red@You don't have " + gold + " coins to escrow.");
			return;
		}
		p.getCarriedItems().getInventory().remove(new com.openrsc.server.model.container.Item(coinsId, gold), true);
		final com.openrsc.server.plugins.custom.contracts.Contract c =
			com.openrsc.server.plugins.custom.contracts.ContractRegistry.postMentorship(
				p, skillId, minLevel, bondHrs, gold, deadlineHrs);
		p.message("@gre@Mentorship contract #" + c.id + " posted. " + gold + "gp escrowed.");
		p.message("Mentors with lvl " + minLevel + "+ in skill " + skillId
			+ " can ::contract accept " + c.id);
	}

	private static void handleBuildJobPost(final Player p, final String[] args) {
		if (args.length < 7) {
			p.message("Usage: ::contract buildjob <feature> <plotId> <targetX> <targetY> <gold> <hours>");
			p.message("Feature: bankchest | forge");
			return;
		}
		final com.openrsc.server.plugins.custom.plots.PlotFeature.Type ftype;
		switch (args[1].toLowerCase()) {
			case "bankchest": case "bank":
				ftype = com.openrsc.server.plugins.custom.plots.PlotFeature.Type.BANK_CHEST; break;
			case "forge": case "anvil":
				ftype = com.openrsc.server.plugins.custom.plots.PlotFeature.Type.FORGE; break;
			default:
				p.message("@red@Unknown feature type. Try: bankchest, forge."); return;
		}
		final int plotId, tx, ty, gold, hours;
		try {
			plotId = Integer.parseInt(args[2]);
			tx     = Integer.parseInt(args[3]);
			ty     = Integer.parseInt(args[4]);
			gold   = Integer.parseInt(args[5]);
			hours  = Integer.parseInt(args[6]);
		} catch (NumberFormatException e) {
			p.message("@red@All numeric args must parse as int."); return;
		}
		final com.openrsc.server.plugins.custom.plots.Plot pl =
			com.openrsc.server.plugins.custom.plots.PlotRegistry.byId(plotId);
		if (pl == null) { p.message("@red@No plot #" + plotId + "."); return; }
		if (pl.deedHolder == null || !pl.deedHolder.equalsIgnoreCase(p.getUsername())) {
			p.message("@red@You don't own that plot.");
			return;
		}
		if (!pl.contains(tx, ty)) {
			p.message("@red@(" + tx + "," + ty + ") is outside your plot's bounding box.");
			return;
		}
		if (pl.featureAt(tx, ty) != null) {
			p.message("@red@A feature already exists at (" + tx + "," + ty + ")."); return;
		}
		if (pl.features.size() >= pl.tier.featureSlots()) {
			p.message("@red@Plot is at its " + pl.tier.featureSlots() + " feature slot limit."); return;
		}
		if (gold <= 0 || hours <= 0 || hours > 168) {
			p.message("@red@Bad gold/hours."); return;
		}
		final int coinsId = ItemId.COINS.id();
		if (p.getCarriedItems().getInventory().countId(coinsId) < gold) {
			p.message("@red@You don't have " + gold + "gp to escrow."); return;
		}
		p.getCarriedItems().getInventory().remove(new Item(coinsId, gold), true);
		final Contract c = ContractRegistry.postConstructionJob(
			p, ftype.ordinal(), plotId, tx, ty, gold, hours);
		p.message("@gre@Construction job #" + c.id + " posted: " + ftype.displayName
			+ " on plot #" + plotId + " at (" + tx + "," + ty + ") for " + gold + "gp.");
		p.message("Workers with Construction lvl " + ftype.minConstructionLevel + "+ can ::contract accept " + c.id);
		p.message("The build's XP credits to YOU (employer-side Construction XP).");
	}

	private static void handleBuildExec(final Player p) {
		final Contract c = ContractRegistry.activeForWorker(p.getUsername());
		if (c == null) { p.message("@red@You have no active contract."); return; }
		if (c.type != Contract.Type.CONSTRUCTION_JOB) {
			p.message("@red@Active contract isn't a construction-job. Use ::contract deliver instead.");
			return;
		}
		final com.openrsc.server.plugins.custom.plots.Plot pl =
			com.openrsc.server.plugins.custom.plots.PlotRegistry.byId(c.constructionPlotId);
		if (pl == null) { p.message("@red@Plot vanished — contract is broken."); return; }
		if (p.getX() != c.constructionTargetX || p.getY() != c.constructionTargetY) {
			p.message("@red@You must stand on the exact target tile (" + c.constructionTargetX + ","
				+ c.constructionTargetY + ") to build.");
			return;
		}
		if (pl.featureAt(p.getX(), p.getY()) != null) {
			p.message("@red@A feature already exists here (race?)."); return;
		}
		final com.openrsc.server.plugins.custom.plots.PlotFeature.Type ftype =
			com.openrsc.server.plugins.custom.plots.PlotFeature.Type.values()[c.constructionFeatureTypeOrdinal];
		final int constructionLvl = p.getSkills().getLevel(
			com.openrsc.server.constants.Skill.CONSTRUCTION.id());
		if (constructionLvl < ftype.minConstructionLevel) {
			p.message("@red@Need Construction lvl " + ftype.minConstructionLevel
				+ " (you have " + constructionLvl + ")."); return;
		}
		// Spawn scenery + record feature.
		final com.openrsc.server.model.Point loc = com.openrsc.server.model.Point.location(p.getX(), p.getY());
		final com.openrsc.server.model.entity.GameObject obj =
			new com.openrsc.server.model.entity.GameObject(p.getWorld(), loc, ftype.sceneryId, 0, 0);
		p.getWorld().registerGameObject(obj);
		final com.openrsc.server.plugins.custom.plots.PlotFeature pf =
			new com.openrsc.server.plugins.custom.plots.PlotFeature(pl.id, ftype, p.getX(), p.getY(), p.getUsername());
		pl.features.put(com.openrsc.server.plugins.custom.plots.Plot.featureKey(p.getX(), p.getY()), pf);
		// XP credits the EMPLOYER — the narrow exception per design.
		final long employerHash = com.openrsc.server.util.rsc.DataConversions.usernameToHash(c.posterName);
		final Player employer = p.getWorld().getPlayer(employerHash);
		final int xp = ftype.minConstructionLevel * 250 * 4;
		if (employer != null) {
			employer.getSkills().addExperience(com.openrsc.server.constants.Skill.CONSTRUCTION.id(), xp);
			employer.message("@gre@Worker @whi@" + p.getUsername() + "@gre@ completed your construction job on plot #"
				+ pl.id + ". You gained " + (xp / 4) + " Construction XP.");
		}
		// Pay the worker.
		p.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), c.goldReward));
		p.message("@gre@Built " + ftype.displayName + ". Paid " + c.goldReward + "gp.");
		if (employer == null) {
			p.message("@yel@(Employer offline — XP deferred. Will land when they log in.)");
		}
		ContractRegistry.completeConstructionJob(c);
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
		// Mentorship-specific gate: mentor must meet the min skill level.
		if (c.type == Contract.Type.MENTORSHIP) {
			final int mentorLvl = p.getSkills().getLevel(c.mentorSkillId);
			if (mentorLvl < c.mentorMinLevel) {
				p.message("@red@You need lvl " + c.mentorMinLevel + " in skill " + c.mentorSkillId
					+ " to mentor (you have " + mentorLvl + ").");
				return;
			}
		}
		// Construction-job-specific gate: worker must meet the feature's
		// Construction min-level.
		if (c.type == Contract.Type.CONSTRUCTION_JOB) {
			final com.openrsc.server.plugins.custom.plots.PlotFeature.Type ftype =
				com.openrsc.server.plugins.custom.plots.PlotFeature.Type.values()[c.constructionFeatureTypeOrdinal];
			final int workerLvl = p.getSkills().getLevel(
				com.openrsc.server.constants.Skill.CONSTRUCTION.id());
			if (workerLvl < ftype.minConstructionLevel) {
				p.message("@red@Need Construction lvl " + ftype.minConstructionLevel
					+ " to take this job (you have " + workerLvl + ").");
				return;
			}
		}
		if (!ContractRegistry.accept(c, p)) {
			p.message("@red@Contract #" + id + " can't be accepted (already taken or closed).");
			return;
		}
		if (c.type == Contract.Type.MENTORSHIP) {
			p.message("@gre@Accepted mentorship #" + id + ". Bond with @whi@" + c.posterName
				+ "@gre@ within 20 tiles + perform skill " + c.mentorSkillId
				+ " activity for " + c.mentorDurationHrs + "h to earn " + c.goldReward + "gp.");
		} else if (c.type == Contract.Type.CONSTRUCTION_JOB) {
			p.message("@gre@Accepted construction job #" + id + ". Walk to plot #"
				+ c.constructionPlotId + " tile (" + c.constructionTargetX + ","
				+ c.constructionTargetY + ") and ::contract build to construct + claim "
				+ c.goldReward + "gp.");
			p.message("@yel@Note: the Construction XP credits to @whi@" + c.posterName
				+ "@yel@ (employer), not you. You earn gold.");
		} else {
			p.message("@gre@Accepted contract #" + id + ". Gather " + c.itemAmount + " of item " + c.itemId);
			p.message("then ::contract deliver at the Job Board to claim " + c.goldReward + "gp.");
		}
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

	private static void handleBountyPost(final Player p, final String[] args) {
		if (args.length < 4) {
			p.message("Usage: ::contract bounty <player> <gold> <hours>");
			return;
		}
		final String target = args[1];
		if (target.equalsIgnoreCase(p.getUsername())) {
			p.message("@red@You can't put a bounty on yourself.");
			return;
		}
		final int gold, hours;
		try {
			gold = Integer.parseInt(args[2]);
			hours = Integer.parseInt(args[3]);
		} catch (NumberFormatException e) {
			p.message("Bad args."); return;
		}
		if (gold < 1000) { p.message("@red@Bounty minimum is 1000gp."); return; }
		if (hours < 1 || hours > 168) { p.message("@red@Hours must be 1-168 (week max)."); return; }
		final int coinsId = ItemId.COINS.id();
		if (p.getCarriedItems().getInventory().countId(coinsId) < gold) {
			p.message("@red@You don't have " + gold + "gp.");
			return;
		}
		p.getCarriedItems().getInventory().remove(new Item(coinsId, gold), true);
		final Contract c = ContractRegistry.postBounty(p, target, gold, hours);
		p.message("@gre@Bounty posted: " + gold + "gp on @whi@" + target + "@gre@ for " + hours + "h. Contract #" + c.id + ".");
		p.message("Anyone who kills " + target + " in the Wilderness collects the reward at the Job Board.");
	}
}

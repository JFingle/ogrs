package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.guilds.Guild;
import com.openrsc.server.plugins.custom.guilds.GuildRegistry;
import com.openrsc.server.plugins.triggers.CommandTrigger;

import java.util.List;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * OGRS — chat-command interface for the guild system. Phase 2-α of
 * the housing/contract arc.
 *
 * Commands:
 *   ::guild create &lt;name&gt;       — pay 100k, become FOUNDER of a new guild
 *   ::guild list                  — show all guilds + member counts
 *   ::guild info [name]           — your guild, or named guild details
 *   ::guild invite &lt;player&gt;     — invite a player (FOUNDER/OFFICER only)
 *   ::guild accept                — accept a pending invite
 *   ::guild leave                 — leave your guild (not as FOUNDER)
 *   ::guild kick &lt;player&gt;       — remove a member (FOUNDER/OFFICER only)
 *   ::guild disband               — permanently delete your guild (FOUNDER only)
 *
 * NOT in v1 (queued for 2-β):
 *   ::guild chat &lt;msg&gt; — needs message channel routing
 *   ::guild promote / demote — needs the role-transfer rules nailed down
 *   ::guild bank — needs the bank UI panel
 *   ::guild transfer — pass FOUNDER role to another member
 */
public final class GuildCommands implements CommandTrigger {

	private static final int CREATION_FEE = 100_000;

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(), "guild", "guilds", "g");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		if (args.length == 0) {
			showHelp(player);
			return;
		}
		final String sub = args[0].toLowerCase();
		switch (sub) {
			case "create":   handleCreate(player, args);   break;
			case "list":     handleList(player);           break;
			case "info":     handleInfo(player, args);     break;
			case "invite":   handleInvite(player, args);   break;
			case "accept":   handleAccept(player);         break;
			case "leave":    handleLeave(player);          break;
			case "kick":     handleKick(player, args);     break;
			case "disband":  handleDisband(player);        break;
			case "bank":     handleBankShow(player);       break;
			case "deposit":  handleDeposit(player, args);  break;
			case "withdraw": handleWithdraw(player, args); break;
			default:         showHelp(player);
		}
	}

	private static void showHelp(final Player p) {
		p.message("@gre@Guilds — chat commands:");
		p.message("  ::guild create <name>      — found a guild (100k fee)");
		p.message("  ::guild list               — all guilds");
		p.message("  ::guild info [name]        — your guild, or named guild");
		p.message("  ::guild invite <player>    — invite (founder/officer)");
		p.message("  ::guild accept             — accept a pending invite");
		p.message("  ::guild leave              — leave (not as founder)");
		p.message("  ::guild kick <player>      — remove (founder/officer)");
		p.message("  ::guild disband            — delete the guild (founder)");
		p.message("  ::guild bank               — show treasury balance");
		p.message("  ::guild deposit <gold>     — add to treasury");
		p.message("  ::guild withdraw <gold>    — pull from treasury (member+)");
		p.message("  ::gc <message>             — speak to your guild channel");
	}

	private static void handleCreate(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::guild create <name>"); return; }
		// Join all remaining args as the name (so "Bandit Camp" works).
		final StringBuilder nameSb = new StringBuilder();
		for (int i = 1; i < args.length; i++) {
			if (i > 1) nameSb.append(' ');
			nameSb.append(args[i]);
		}
		final String name = nameSb.toString().trim();
		if (name.length() < 3 || name.length() > 32) {
			p.message("@red@Name must be 3-32 chars.");
			return;
		}
		if (GuildRegistry.byMember(p.getUsername()) != null) {
			p.message("@red@You're already in a guild. Leave first.");
			return;
		}
		if (GuildRegistry.byName(name) != null) {
			p.message("@red@A guild named '" + name + "' already exists.");
			return;
		}
		if (p.getCarriedItems().getInventory().countId(ItemId.COINS.id()) < CREATION_FEE) {
			p.message("@red@You need " + CREATION_FEE + "gp to found a guild.");
			return;
		}
		p.getCarriedItems().getInventory().remove(new Item(ItemId.COINS.id(), CREATION_FEE), true);
		final Guild g = GuildRegistry.create(name, p.getUsername());
		if (g == null) {
			// Race — name taken or already-in-guild between checks. Refund.
			p.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), CREATION_FEE));
			p.message("@red@Couldn't create the guild. Refunded " + CREATION_FEE + "gp.");
			return;
		}
		p.message("@gre@Guild '" + g.name + "' founded! You are the FOUNDER.");
		p.message("Invite members with ::guild invite <player>");
	}

	private static void handleList(final Player p) {
		final List<Guild> all = GuildRegistry.listAll();
		if (all.isEmpty()) {
			p.message("@yel@No guilds yet. Be the first with ::guild create <name>!");
			return;
		}
		p.message("@gre@Guilds (" + all.size() + "):");
		for (Guild g : all) {
			p.message("@yel@  " + g.name + " — " + g.memberCount() + " members, founder @whi@" + g.founderUsername);
		}
	}

	private static void handleInfo(final Player p, final String[] args) {
		Guild g;
		if (args.length >= 2) {
			final StringBuilder nameSb = new StringBuilder();
			for (int i = 1; i < args.length; i++) {
				if (i > 1) nameSb.append(' ');
				nameSb.append(args[i]);
			}
			g = GuildRegistry.byName(nameSb.toString().trim());
		} else {
			g = GuildRegistry.byMember(p.getUsername());
		}
		if (g == null) {
			p.message("@yel@No such guild. You're " + (GuildRegistry.byMember(p.getUsername()) == null ? "not in a guild." : "in a guild — use ::guild info."));
			return;
		}
		p.message("@gre@Guild: " + g.name);
		p.message("  Founder: @whi@" + g.founderUsername);
		p.message("  Members: @whi@" + g.memberCount());
		if (g.motto != null && !g.motto.isEmpty()) {
			p.message("  Motto: @whi@" + g.motto);
		}
		// Show top-tier members.
		final List<String> officers = g.usernamesByRole(Guild.Role.OFFICER);
		if (!officers.isEmpty()) {
			p.message("  Officers: @whi@" + String.join(", ", officers));
		}
	}

	private static void handleInvite(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::guild invite <player>"); return; }
		final Guild g = GuildRegistry.byMember(p.getUsername());
		if (g == null) { p.message("@red@You're not in a guild."); return; }
		final String target = args[1];
		if (target.equalsIgnoreCase(p.getUsername())) {
			p.message("@red@Can't invite yourself.");
			return;
		}
		if (!GuildRegistry.invite(g, p.getUsername(), target)) {
			p.message("@red@Couldn't invite — check your role (founder/officer only) and that '" + target + "' isn't already guilded.");
			return;
		}
		p.message("@gre@Invited @whi@" + target + "@gre@ to '" + g.name + "'.");
		// Notify the invitee if online.
		final long hash = com.openrsc.server.util.rsc.DataConversions.usernameToHash(target);
		final Player tgt = p.getWorld().getPlayer(hash);
		if (tgt != null) {
			tgt.message("@gre@You've been invited to guild '" + g.name + "' by @whi@" + p.getUsername()
				+ "@gre@. ::guild accept to join.");
		}
	}

	private static void handleAccept(final Player p) {
		final Guild g = GuildRegistry.accept(p.getUsername());
		if (g == null) {
			p.message("@red@No pending invite (or you're already in a guild).");
			return;
		}
		p.message("@gre@You joined '" + g.name + "' as a RECRUIT.");
	}

	private static void handleLeave(final Player p) {
		final Guild g = GuildRegistry.byMember(p.getUsername());
		if (g == null) { p.message("@red@You're not in a guild."); return; }
		if (g.roleOf(p.getUsername()) == Guild.Role.FOUNDER) {
			p.message("@red@Founders can't leave — ::guild disband to remove the guild entirely.");
			return;
		}
		if (!GuildRegistry.leave(p.getUsername())) {
			p.message("@red@Couldn't leave.");
			return;
		}
		p.message("@yel@You left '" + g.name + "'.");
	}

	private static void handleKick(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::guild kick <player>"); return; }
		final Guild g = GuildRegistry.byMember(p.getUsername());
		if (g == null) { p.message("@red@You're not in a guild."); return; }
		if (!GuildRegistry.kick(g, p.getUsername(), args[1])) {
			p.message("@red@Couldn't kick. Check your role + the target's role.");
			return;
		}
		p.message("@yel@Kicked @whi@" + args[1] + "@yel@ from '" + g.name + "'.");
	}

	private static void handleDisband(final Player p) {
		final Guild g = GuildRegistry.byMember(p.getUsername());
		if (g == null) { p.message("@red@You're not in a guild."); return; }
		if (!GuildRegistry.disband(g, p.getUsername())) {
			p.message("@red@Only the founder can disband.");
			return;
		}
		p.message("@yel@Guild '" + g.name + "' disbanded.");
	}

	private static void handleBankShow(final Player p) {
		final Guild g = GuildRegistry.byMember(p.getUsername());
		if (g == null) { p.message("@red@You're not in a guild."); return; }
		p.message("@gre@Guild '" + g.name + "' treasury: @whi@" + g.bankGold + "gp");
		final Guild.Role r = g.roleOf(p.getUsername());
		if (r != null && !r.canWithdrawBank()) {
			p.message("  (Your role is " + r + " — deposit-only.)");
		}
	}

	private static void handleDeposit(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::guild deposit <gold>"); return; }
		final long amount;
		try { amount = Long.parseLong(args[1]); } catch (NumberFormatException e) {
			p.message("Bad amount."); return;
		}
		if (amount <= 0) { p.message("@red@Amount must be positive."); return; }
		final Guild g = GuildRegistry.byMember(p.getUsername());
		if (g == null) { p.message("@red@You're not in a guild."); return; }
		final int coinsId = ItemId.COINS.id();
		// countId returns int; deposits up to 2.1B fit in inventory.
		if (p.getCarriedItems().getInventory().countId(coinsId) < amount) {
			p.message("@red@You don't have " + amount + "gp.");
			return;
		}
		p.getCarriedItems().getInventory().remove(new Item(coinsId, (int) amount), true);
		if (!GuildRegistry.deposit(g, p.getUsername(), amount)) {
			// Race — refund.
			p.getCarriedItems().getInventory().add(new Item(coinsId, (int) amount));
			p.message("@red@Deposit rejected. Refunded.");
			return;
		}
		p.message("@gre@Deposited " + amount + "gp to '" + g.name + "'. Treasury: @whi@" + g.bankGold + "gp");
	}

	private static void handleWithdraw(final Player p, final String[] args) {
		if (args.length < 2) { p.message("Usage: ::guild withdraw <gold>"); return; }
		final long amount;
		try { amount = Long.parseLong(args[1]); } catch (NumberFormatException e) {
			p.message("Bad amount."); return;
		}
		if (amount <= 0) { p.message("@red@Amount must be positive."); return; }
		final Guild g = GuildRegistry.byMember(p.getUsername());
		if (g == null) { p.message("@red@You're not in a guild."); return; }
		final Guild.Role r = g.roleOf(p.getUsername());
		if (r == null || !r.canWithdrawBank()) {
			p.message("@red@Your role (" + r + ") can't withdraw. Talk to a founder/officer.");
			return;
		}
		// Cap at inventory headroom — coin stacks in inv max out at Integer.MAX_VALUE.
		final long capped = Math.min(amount, (long) Integer.MAX_VALUE);
		final long actual = GuildRegistry.withdraw(g, p.getUsername(), capped);
		if (actual == 0) {
			p.message("@yel@Treasury is empty or withdrawal refused.");
			return;
		}
		p.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), (int) actual));
		p.message("@gre@Withdrew " + actual + "gp. Treasury: @whi@" + g.bankGold + "gp");
	}
}

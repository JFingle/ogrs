package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.guilds.Guild;
import com.openrsc.server.plugins.custom.guilds.GuildRegistry;
import com.openrsc.server.plugins.triggers.CommandTrigger;
import com.openrsc.server.util.rsc.DataConversions;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * OGRS — guild chat channel. Phase 2-β.
 *
 *   ::gc &lt;message&gt;        — speak to your guild
 *   ::guildchat &lt;message&gt; — alias
 *
 * Broadcasts a single chat-log line to every online member of the
 * speaker's guild, formatted with a tag and role badge:
 *
 *   @cya@[Guild] @whi@(F) Sparky@gre@: hello everyone
 *
 * Role glyph: F = founder, O = officer, M = member, R = recruit.
 *
 * Offline members miss the message (no scrollback in v1 — IRC-style).
 * If/when there's an in-client guild UI panel, we'll add scrollback
 * there.
 */
public final class GuildChatCommand implements CommandTrigger {

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(), "gc", "guildchat");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		final Guild g = GuildRegistry.byMember(player.getUsername());
		if (g == null) {
			player.message("@red@You're not in a guild. ::guild create <name> to start one.");
			return;
		}
		if (args.length == 0) {
			player.message("@gre@Usage: ::gc <message>   (speaks to @whi@" + g.name + "@gre@)");
			return;
		}
		final StringBuilder msgSb = new StringBuilder();
		for (int i = 0; i < args.length; i++) {
			if (i > 0) msgSb.append(' ');
			msgSb.append(args[i]);
		}
		final String body = sanitize(msgSb.toString());
		if (body.isEmpty()) return;

		final Guild.Role speakerRole = g.roleOf(player.getUsername());
		final String line = "@cya@[" + g.name + "] @whi@(" + roleGlyph(speakerRole) + ") "
			+ player.getUsername() + "@gre@: " + body;

		int delivered = 0;
		for (String member : g.members.keySet()) {
			final Player mp = player.getWorld().getPlayer(DataConversions.usernameToHash(member));
			if (mp != null) {
				mp.message(line);
				delivered++;
			}
		}
		// Speaker's own message already echoed via the iteration above
		// (they're in g.members). If they were somehow not included
		// (mid-leave race), echo directly so they see their own send.
		if (delivered == 0) player.message(line);
	}

	private static String roleGlyph(final Guild.Role r) {
		if (r == null) return "?";
		switch (r) {
			case FOUNDER: return "F";
			case OFFICER: return "O";
			case MEMBER:  return "M";
			case RECRUIT: return "R";
			default:      return "?";
		}
	}

	private static String sanitize(final String s) {
		// Strip control bytes; cap at a sensible length so a single
		// shout can't blow up everyone's chat log.
		final String trimmed = s.replace('\r', ' ').replace('\n', ' ').trim();
		return trimmed.length() > 200 ? trimmed.substring(0, 200) : trimmed;
	}
}

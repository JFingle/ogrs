package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.constants.Spells;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.CommandTrigger;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * OGRS — staff autocast chat command.
 *
 * Picker UI lands in the Combat tab work; until then, players (and tests)
 * use this command:
 *
 *   ::autocast              — show current state + a hint
 *   ::autocast off          — disable
 *   ::autocast list         — print every recognized spell name
 *   ::autocast wind_strike  — set autocast to that spell (case-insensitive)
 *
 * No state is persisted across login yet — autocast resets each session
 * by design until persistence + UI land.
 */
public class AutocastCommand implements CommandTrigger {

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(), "autocast", "ac");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		if (args.length == 0) {
			showStatus(player);
			return;
		}

		final String arg = args[0].toLowerCase();

		if (arg.equals("off") || arg.equals("none") || arg.equals("disable")) {
			player.setAutocastSpellId(-1);
			player.message("@gre@Autocast: OFF.");
			return;
		}

		if (arg.equals("list")) {
			listSpells(player);
			return;
		}

		// Try to match a spell name.
		final Spells match = findSpell(arg);
		if (match == null) {
			player.message("@red@Unknown spell '" + args[0]
				+ "'. Try @whi@::autocast list@red@ for valid names, or @whi@::autocast off@red@.");
			return;
		}
		if (!com.openrsc.server.content.OgrsAutocast.isAutocastEligible(match)) {
			player.message("@red@" + prettyName(match)
				+ " can't be autocast. Only combat offensive spells (Strike/Bolt/Blast/Wave + Iban/Crumble/God spells) are autocastable; teleports, debuffs, buffs, and utility spells aren't.");
			return;
		}

		player.setAutocastSpellId(match.ordinal());
		player.message("@gre@Autocast: " + prettyName(match)
			+ ". Equip a matching staff and attack a mob to cast.");
	}

	private static void showStatus(final Player player) {
		if (!player.isAutocastEnabled()) {
			player.message("@gre@Autocast is OFF. Use @whi@::autocast <spell>@gre@ to enable, "
				+ "or @whi@::autocast list@gre@ to see options.");
			return;
		}
		final Spells current = Spells.values()[player.getAutocastSpellId()];
		player.message("@gre@Autocast: " + prettyName(current)
			+ " (use @whi@::autocast off@gre@ to disable).");
	}

	private static void listSpells(final Player player) {
		final StringBuilder sb = new StringBuilder();
		sb.append("@gre@Autocast spells: ");
		final Spells[] all = Spells.values();
		boolean first = true;
		for (final Spells s : all) {
			if (!first) sb.append(", ");
			sb.append(s.name().toLowerCase());
			first = false;
		}
		// Spam-safe: chunk by 250 chars across multiple messages.
		final String full = sb.toString();
		final int chunk = 250;
		for (int i = 0; i < full.length(); i += chunk) {
			player.message(full.substring(i, Math.min(i + chunk, full.length())));
		}
	}

	private static Spells findSpell(final String input) {
		// Strip common separators so 'wind_strike', 'wind-strike', 'windstrike'
		// all match.
		final String key = input.replace("-", "_").replace(" ", "_").toUpperCase();
		for (final Spells s : Spells.values()) {
			if (s.name().equals(key)) return s;
			if (s.name().replace("_", "").equals(key.replace("_", ""))) return s;
		}
		return null;
	}

	private static String prettyName(final Spells s) {
		final String[] parts = s.name().toLowerCase().split("_");
		final StringBuilder sb = new StringBuilder();
		for (int i = 0; i < parts.length; i++) {
			if (i > 0) sb.append(' ');
			sb.append(Character.toUpperCase(parts[i].charAt(0)));
			if (parts[i].length() > 1) sb.append(parts[i].substring(1));
		}
		return sb.toString();
	}
}

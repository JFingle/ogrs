package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.constants.Skill;
import com.openrsc.server.event.rsc.impl.PoisonEvent;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.CommandTrigger;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * Priest / monk-style player commands for OGRS. First seed of the prayer
 * expansion track (memory item #20).
 *
 * Today this is a chat-command interface because adding genuine prayers to
 * the prayer panel requires extending the protocol-177 prayer-active wire
 * format (the Prayers array is fixed at 14 booleans, mirrored on the client).
 * That protocol surgery is its own focused session. Until then, the priest
 * mechanics live as `::cleanse` (and friends as we add them), which any
 * player above the relevant Prayer level can invoke.
 *
 * Commands:
 *   ::cleanse              — if poisoned, cure the poison and grant Prayer XP.
 *                            Free for now; future tier will cost prayer points.
 *   ::poisonme [damage]    — DEV: self-poison for testing the cleanse loop.
 *                            Defaults to 6 damage/tick.
 */
public class PriestCommands implements CommandTrigger {

	private static final int CLEANSE_PRAYER_XP_DISPLAY = 25;     // display units
	private static final int CLEANSE_PRAYER_LEVEL_REQ = 1;        // start permissive; raise once tiered prayers land

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(),
			"cleanse", "cleansepoison",
			"poisonme");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		final String c = cmd.toLowerCase();
		if (c.equals("cleanse") || c.equals("cleansepoison")) {
			cleanse(player);
		} else if (c.equals("poisonme")) {
			if (!player.isAdmin()) {
				player.message("@gre@Only admins can self-poison for testing.");
				return;
			}
			final int dmg = parseIntOr(args, 0, 6);
			player.setPoisonDamage(dmg);
			player.startPoisonEvent();
			player.message("@gre@DEV: poisoned yourself for " + dmg + " damage/tick.");
		}
	}

	private void cleanse(final Player player) {
		if (player.getSkills().getMaxStat(Skill.PRAYER.id()) < CLEANSE_PRAYER_LEVEL_REQ) {
			player.message("@gre@You need Prayer level " + CLEANSE_PRAYER_LEVEL_REQ + " to cleanse poison.");
			return;
		}

		final PoisonEvent poisonEvent = player.getAttribute("poisonEvent", null);
		final boolean isPoisoned = poisonEvent != null
			|| player.getCache().hasKey("poisoned")
			|| player.getPoisonDamage() > 0;

		if (!isPoisoned) {
			player.message("@gre@There is no poison in you to cleanse.");
			return;
		}

		// Engine API to clear poison state cleanly.
		player.cure();
		// Make sure setPoisonDamage(0) gets called explicitly — cure() handles
		// the event but some edge paths leave the field non-zero.
		player.setPoisonDamage(0);

		// Display-units XP × 4 for the engine's storage (RSC convention).
		player.getSkills().addExperience(Skill.PRAYER.id(), CLEANSE_PRAYER_XP_DISPLAY * 4);

		player.message("@gre@A quiet calm settles over you — the venom drains from your veins.");
		player.message("@gre@+" + CLEANSE_PRAYER_XP_DISPLAY + " Prayer XP.");
	}

	private static int parseIntOr(final String[] args, final int idx, final int fallback) {
		if (args == null || args.length <= idx) return fallback;
		try {
			return Integer.parseInt(args[idx]);
		} catch (final NumberFormatException e) {
			return fallback;
		}
	}
}

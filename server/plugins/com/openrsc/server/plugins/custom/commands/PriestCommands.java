package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.constants.Skill;
import com.openrsc.server.event.rsc.impl.PoisonEvent;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.CommandTrigger;
import com.openrsc.server.util.rsc.DataConversions;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * Priest / monk-style player commands for OGRS. First seeds of the prayer
 * expansion track (memory item #20).
 *
 * Today this is a chat-command interface because adding genuine prayers to
 * the prayer panel requires extending the protocol-177 prayer-active wire
 * format (the Prayers array is fixed at 14 booleans, mirrored on the client).
 * That protocol surgery is its own focused session. Until then, the priest
 * mechanics live as `::cleanse` and `::heal`, which any player above the
 * relevant Prayer level can invoke.
 *
 * Commands:
 *   ::cleanse              — if poisoned, cure the poison and grant Prayer XP.
 *                            Free for now; future tier will cost prayer points.
 *   ::heal <player>        — sacrifice 5 of your own HP to heal another
 *                            player by 5 HP. "No greater love" — biblical
 *                            framing of intercessory prayer. Grants Prayer XP
 *                            proportional to HP actually transferred.
 *   ::poisonme [damage]    — DEV: self-poison for testing the cleanse loop.
 *                            Defaults to 6 damage/tick.
 */
public class PriestCommands implements CommandTrigger {

	// Cleanse Poison —
	// RSC prayer XP is small (bones are 4-15 XP). Lowered from the initial 25.
	private static final int CLEANSE_PRAYER_XP_DISPLAY = 2;
	private static final int CLEANSE_PRAYER_LEVEL_REQ = 1;

	// Heal Other —
	// 5 HP transfer at a 1:1 cost. 3 XP/HP healed = 15 XP per full cast,
	// scaled down if the target was nearly full.
	private static final int HEAL_HP_AMOUNT = 5;
	private static final int HEAL_PRAYER_XP_PER_HP = 3;
	private static final int HEAL_PRAYER_LEVEL_REQ = 5;

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(),
			"cleanse", "cleansepoison",
			"heal", "healother",
			"poisonme");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		final String c = cmd.toLowerCase();
		if (c.equals("cleanse") || c.equals("cleansepoison")) {
			cleanse(player);
		} else if (c.equals("heal") || c.equals("healother")) {
			healOther(player, args);
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

	// ==================== Cleanse Poison ====================

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

		player.cure();
		player.setPoisonDamage(0);
		player.getSkills().addExperience(Skill.PRAYER.id(), CLEANSE_PRAYER_XP_DISPLAY * 4);

		player.message("@gre@A quiet calm settles over you — the venom drains from your veins.");
		player.message("@gre@+" + CLEANSE_PRAYER_XP_DISPLAY + " Prayer XP.");
	}

	// ==================== Heal Other ====================

	private void healOther(final Player player, final String[] args) {
		if (args == null || args.length < 1 || args[0].isEmpty()) {
			player.message("@gre@Usage: ::heal <player_name>");
			return;
		}

		if (player.getSkills().getMaxStat(Skill.PRAYER.id()) < HEAL_PRAYER_LEVEL_REQ) {
			player.message("@gre@You need Prayer level " + HEAL_PRAYER_LEVEL_REQ + " to heal another.");
			return;
		}

		final String targetName = args[0].replace('_', ' ');
		final Player target = player.getWorld().getPlayer(DataConversions.usernameToHash(targetName));
		if (target == null) {
			player.message("@gre@You cannot find " + targetName + ".");
			return;
		}
		if (target == player) {
			player.message("@gre@You cannot pour yourself out for yourself. Eat food.");
			return;
		}

		final int targetCurHp = target.getSkills().getLevel(Skill.HITS.id());
		final int targetMaxHp = target.getSkills().getMaxStat(Skill.HITS.id());
		if (targetCurHp >= targetMaxHp) {
			player.message("@gre@" + target.getUsername() + " is already in full health.");
			return;
		}

		final int casterCurHp = player.getSkills().getLevel(Skill.HITS.id());
		// Don't let the caster reduce themselves to 0; keep at least 1 HP.
		final int casterCanGive = Math.max(0, casterCurHp - 1);
		if (casterCanGive < 1) {
			player.message("@gre@You are too weak to give of yourself.");
			return;
		}

		final int hpHealed = Math.min(HEAL_HP_AMOUNT,
			Math.min(casterCanGive, targetMaxHp - targetCurHp));

		// Apply: caster pays in HP, target receives.
		player.getSkills().setLevel(Skill.HITS.id(), casterCurHp - hpHealed);
		target.getSkills().setLevel(Skill.HITS.id(), targetCurHp + hpHealed);

		final int xp = hpHealed * HEAL_PRAYER_XP_PER_HP;
		player.getSkills().addExperience(Skill.PRAYER.id(), xp * 4);

		player.message("@gre@You pour out " + hpHealed + " of your strength to mend " + target.getUsername() + ".");
		player.message("@gre@+" + xp + " Prayer XP.");
		target.message("@gre@A wave of warmth passes through you — " + player.getUsername()
			+ " has knitted you whole, restoring " + hpHealed + " HP.");
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

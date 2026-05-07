package com.openrsc.server.plugins.custom.items;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.event.rsc.impl.projectile.ProjectileEvent;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.Mob;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.OpInvTrigger;
import com.openrsc.server.util.OgrsProjectileTypes;
import com.openrsc.server.util.rsc.DataConversions;

/**
 * OGRS item handler: Cracked Shaman Staff "Channel" — special attack.
 *
 * Context-aware single button:
 *
 *   Out of combat → +5 HP heal pulse, capped at max. Plays "recharge".
 *   In combat (you have an opponent within range) → "Spirit Bite":
 *     fires a SKULL projectile at the opponent for 4-9 damage, then
 *     heals the caster for 50% of damage dealt (rounded up). Plays
 *     "spellok" for the cast and "recharge" for the lifesteal pulse.
 *
 * Same 30-tick (~19s) cooldown for both modes; cached under
 * {@code ogrs_shaman_staff_cd}. Cooldown isn't burned if the heal
 * mode would overheal.
 *
 * Conceptually this is the project's first weapon "special attack" —
 * a verb you press to break the back-and-forth rhythm with a unique
 * damage shape + projectile sprite. Future weapons will follow this
 * pattern: a special-attack interface + per-weapon implementation.
 */
public final class CrackedShamanStaffChannel implements OpInvTrigger {

	private static final int HEAL_AMOUNT = 5;
	private static final int BITE_MIN_DAMAGE = 4;
	private static final int BITE_MAX_DAMAGE = 9;
	private static final long COOLDOWN_TICKS = 30L;
	private static final String CACHE_KEY = "ogrs_shaman_staff_cd";

	@Override
	public boolean blockOpInv(final Player player, final Integer invIndex, final Item item, final String command) {
		return item.getCatalogId() == ItemId.OGRS_CRACKED_SHAMAN_STAFF.id()
			&& "channel".equalsIgnoreCase(command);
	}

	@Override
	public void onOpInv(final Player player, final Integer invIndex, final Item item, final String command) {
		final long now = player.getWorld().getServer().getCurrentTick();
		final long lastUsed = player.getCache().hasKey(CACHE_KEY)
			? player.getCache().getLong(CACHE_KEY)
			: -COOLDOWN_TICKS;
		if (now - lastUsed < COOLDOWN_TICKS) {
			final long remainTicks = COOLDOWN_TICKS - (now - lastUsed);
			ActionSender.sendSound(player, "spellfail");
			player.message("@yel@The staff is still warm. Wait about " + ((remainTicks * 640L) / 1000L + 1L) + "s.");
			return;
		}

		// Context routing — combat = lifesteal bite; idle = pure heal pulse.
		final Mob opponent = player.getOpponent();
		if (player.inCombat() && opponent != null && !opponent.isRemoved() && player.withinRange(opponent, 8)) {
			fireSpiritBite(player, opponent, now);
		} else {
			fireHealPulse(player, now);
		}
	}

	private void fireHealPulse(final Player player, final long now) {
		final int curHp = player.getSkills().getLevel(Skill.HITS.id());
		final int maxHp = player.getSkills().getMaxStat(Skill.HITS.id());
		if (curHp >= maxHp) {
			player.message("@yel@You are already at full strength.");
			return; // don't burn cooldown when there's nothing to heal
		}
		final int healed = Math.min(HEAL_AMOUNT, maxHp - curHp);
		player.getSkills().setLevel(Skill.HITS.id(), curHp + healed);
		player.getCache().store(CACHE_KEY, now);
		ActionSender.sendSound(player, "recharge");

		player.message("@gre@The staff hums against your palm. A pulse of green light passes through your chest.");
		player.message("@gre@+" + healed + " HP. The bone tip dims and goes still.");
	}

	private void fireSpiritBite(final Player player, final Mob opponent, final long now) {
		// Damage roll, capped at the opponent's current HP.
		final int rolled = DataConversions.random(BITE_MIN_DAMAGE, BITE_MAX_DAMAGE);
		final int oppCurHp = opponent.getSkills().getLevel(Skill.HITS.id());
		final int damage = Math.min(rolled, oppCurHp);

		// Lifesteal — half of damage dealt (rounded up), capped at missing HP.
		final int casterCurHp = player.getSkills().getLevel(Skill.HITS.id());
		final int casterMaxHp = player.getSkills().getMaxStat(Skill.HITS.id());
		final int lifesteal = Math.min((damage + 1) / 2, casterMaxHp - casterCurHp);

		// Visual — fire a SKULL projectile from caster to opponent. The
		// ProjectileEvent ctor sends the sprite immediately and schedules a
		// 1-tick action for the damage. Type 4 (SKULL) keeps the bite
		// thematic (shaman's death-magic) and distinct from regular MAGIC orbs.
		player.getWorld().getServer().getGameEventHandler().add(
			new ProjectileEvent(player.getWorld(), player, opponent, damage, OgrsProjectileTypes.SKULL)
		);
		// Heal the caster on the same tick — server-side; the projectile
		// damage gets applied to opponent by ProjectileEvent.action().
		// HP bar updates client-side via the standard stat-update; no hit
		// splat (upstream has no signed-damage convention for heals).
		if (lifesteal > 0) {
			player.getSkills().setLevel(Skill.HITS.id(), casterCurHp + lifesteal);
			ActionSender.sendStat(player, Skill.HITS.id());
		}
		player.getCache().store(CACHE_KEY, now);
		ActionSender.sendSound(player, "spellok");

		player.message("@cya@Spirit Bite — the staff drinks for you.");
		player.message("@gre@" + damage + " damage. +" + lifesteal + " HP returned.");
	}
}

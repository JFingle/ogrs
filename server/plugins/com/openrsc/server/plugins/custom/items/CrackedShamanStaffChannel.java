package com.openrsc.server.plugins.custom.items;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.OpInvTrigger;

/**
 * OGRS item handler: Cracked Shaman Staff "Channel" verb.
 *
 * Right-click → Channel triggers a small healing pulse: +5 HP capped
 * at max, with a 30-tick cooldown stored in {@code player.getCache()}.
 * Plays the "recharge" sound for feedback so the player gets audio
 * confirmation when it lands and a quieter "spellfail" beep on
 * cooldown attempts.
 *
 * Game tick = 640ms, so 30 ticks = ~19s — quick enough that the staff
 * is meaningful in a fight but not a spammable god-button. The HP
 * amount + cooldown are tunables; bumping them or scaling on Magic
 * level is a backlog item once we revisit the spellbook.
 */
public final class CrackedShamanStaffChannel implements OpInvTrigger {

	private static final int HEAL_AMOUNT = 5;
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
			: -COOLDOWN_TICKS; // first use never on cooldown
		final long elapsed = now - lastUsed;
		if (elapsed < COOLDOWN_TICKS) {
			final long remainTicks = COOLDOWN_TICKS - elapsed;
			ActionSender.sendSound(player, "spellfail");
			player.message("@yel@The staff is still warm. Wait about " + ((remainTicks * 640L) / 1000L + 1L) + "s.");
			return;
		}

		final int curHp = player.getSkills().getLevel(Skill.HITS.id());
		final int maxHp = player.getSkills().getMaxStat(Skill.HITS.id());
		if (curHp >= maxHp) {
			player.message("@yel@You are already at full strength.");
			return; // don't burn the cooldown if there's nothing to heal
		}

		final int healed = Math.min(HEAL_AMOUNT, maxHp - curHp);
		player.getSkills().setLevel(Skill.HITS.id(), curHp + healed);
		player.getCache().store(CACHE_KEY, now);
		ActionSender.sendSound(player, "recharge");

		player.message("@gre@The staff hums against your palm. A pulse of green light passes through your chest.");
		player.message("@gre@+" + healed + " HP. The bone tip dims and goes still.");
	}
}

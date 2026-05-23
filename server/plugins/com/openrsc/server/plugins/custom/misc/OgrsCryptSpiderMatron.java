package com.openrsc.server.plugins.custom.misc;

import com.openrsc.server.constants.OgrsNpcId;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.AttackNpcTrigger;

/**
 * OGRS — Crypt Spider Matron combat behavior (sparky 2026-05-23 #11
 * follow-up). The matron is a boss-tier (lvl 130) spider at the south
 * end of the spider chamber. NPC definition lives in
 * content/npcs/crypt_spider_matron.yaml (id 844).
 *
 * Custom behaviour layered on top of the engine's default melee combat:
 *   - On player engagement, apply poison to the player.
 *   - Heavier poison spit (80 dmg) if the player is using a ranged
 *     weapon when they engage — sparky: "spit poison if the player
 *     is ranged."
 *   - Lighter venomous-bite poison (40 dmg) for melee engagement —
 *     even a non-ranged attacker gets venom on contact.
 *
 * Poison damage ticks down via the engine's PoisonEvent loop (poison
 * heals over time, dealing dmg/10 per tick until 0). 80 ≈ 8 ticks of
 * damage; 40 ≈ 4 ticks.
 *
 * blockAttackNpc returns FALSE so the engine still runs the default
 * attack-engagement code (we don't want to swallow the click). We only
 * piggy-back on the trigger to apply poison side-effect.
 */
public final class OgrsCryptSpiderMatron implements AttackNpcTrigger {

	private static final int MATRON_ID = OgrsNpcId.CRYPT_SPIDER_MATRON.id();
	private static final int RANGED_SPIT_POISON = 80;
	private static final int MELEE_BITE_POISON  = 40;

	@Override
	public boolean blockAttackNpc(final Player player, final Npc affectedmob) {
		return affectedmob.getID() == MATRON_ID;
	}

	@Override
	public void onAttackNpc(final Player player, final Npc affectedmob) {
		if (affectedmob.getID() != MATRON_ID) return;

		// Don't stack poison if the player is already poisoned heavier.
		// setPoisonDamage just replaces the value; preserve existing
		// venom if it's larger so multiple engagements don't accidentally
		// weaken the effect.
		final int incoming = player.isRanging() ? RANGED_SPIT_POISON : MELEE_BITE_POISON;
		if (player.getPoisonDamage() < incoming) {
			player.setPoisonDamage(incoming);
			if (player.isRanging()) {
				player.message("@gre@The matron rears back and spits a jet of venom at you!");
			} else {
				player.message("The matron's fangs sink in — you feel venom course through your veins.");
			}
		}
	}
}

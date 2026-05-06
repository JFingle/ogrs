package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.KillNpcTrigger;

/**
 * Hook every NPC kill: if the kill matches the player's active slayer task,
 * decrement the count and grant XP equal to the NPC's max hits (OSRS
 * convention).
 *
 * blockKillNpc returns false because we are an OBSERVER — we do not want to
 * preempt the default loot drop / death animation. We just listen.
 */
public class SlayerKillTracker implements KillNpcTrigger {

	@Override
	public boolean blockKillNpc(final Player player, final Npc n) {
		return false;
	}

	@Override
	public void onKillNpc(final Player player, final Npc n) {
		if (!SlayerService.recordKill(player, n.getID())) {
			return;
		}
		final int xp = Math.max(1, n.getDef().getHits());
		final int totalXp = SlayerService.addXp(player, xp);
		final int level = SlayerService.getLevel(totalXp);
		final SlayerData task = SlayerService.getActiveTask(player);

		if (task != null && task.isComplete()) {
			player.message("@gre@Slayer task complete! Return to the Grizzled Traveler.");
			player.message("@gre@" + xp + " Slayer XP. Total: " + totalXp + " (lvl " + level + ").");
		} else if (task != null) {
			player.message("@gre@" + xp + " Slayer XP — " + task.remaining + "/" + task.total
				+ " " + task.npcName + "s left. (lvl " + level + ")");
		}
	}
}

package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.KillNpcTrigger;

/**
 * Hook every NPC kill: if the kill matches the player's active slayer task,
 * decrement the count and grant XP equal to the NPC's max hits (OSRS
 * convention).
 *
 * IMPORTANT — blockKillNpc semantics: despite the name and javadoc, this
 * returning true does NOT skip the NPC's default loot/animation. The NPC's
 * `killedBy` flow runs the plugin handler first and then continues with
 * default loot regardless (see Npc.java:322). The dispatcher in
 * PluginHandler#handlePlugin only invokes our onKillNpc when blockKillNpc
 * returns true. So we MUST return true to be reached at all.
 *
 * We return true only when there's an active slayer task matching the NPC,
 * so we don't interpose on every kill in the world.
 */
public class SlayerKillTracker implements KillNpcTrigger {

	@Override
	public boolean blockKillNpc(final Player player, final Npc n) {
		// Claim the kill (so onKillNpc fires) only when the killed NPC is in
		// the player's active task family. SlayerService.isTaskTarget knows
		// e.g. "Goblin" maps to ids {4, 62, 153, 154, 660}. Returning true
		// does NOT skip default loot — see Npc.java#killedBy.
		return SlayerService.isTaskTarget(player, n.getID());
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

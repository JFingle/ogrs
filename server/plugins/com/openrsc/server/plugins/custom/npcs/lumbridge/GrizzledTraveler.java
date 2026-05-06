package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.skills.slayer.SlayerData;
import com.openrsc.server.plugins.custom.skills.slayer.SlayerService;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * The first OGRS NPC. He stands two tiles NE of the Lumbridge respawn at
 * (122, 650) and acts as the Slayer Master for the MVP.
 *
 * NPC id 836 is reserved in NpcDefsCustom.json + NpcLocsCustom.json. Phase 1
 * will replace the magic number with an OGRS NpcId enum once we have a
 * proper id registry.
 */
public class GrizzledTraveler implements TalkNpcTrigger {

	private static final int OGRS_GRIZZLED_TRAVELER_ID = 836;
	private static final int COMPLETION_BONUS_XP = 50;

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		return n.getID() == OGRS_GRIZZLED_TRAVELER_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		final SlayerData task = SlayerService.getActiveTask(player);
		final int xp = SlayerService.getXp(player);
		final int lvl = SlayerService.getLevel(xp);

		if (task == null) {
			offerNewTask(player, n);
		} else if (task.isComplete()) {
			completeTask(player, n, task);
		} else {
			reportProgress(player, n, task, lvl);
		}
	}

	private void offerNewTask(final Player player, final Npc n) {
		npcsay(player, n,
			"Aye, you've the look of someone who's seen a few things.",
			"Folk call me a Slayer Master. Care to test your steel?");

		final int option = multi(player, n,
			"Yes, give me a slayer task.",
			"What is Slayer?",
			"Not right now, thanks.");

		if (option == 0) {
			final SlayerData task = SlayerService.assignRandomTask(player);
			npcsay(player, n,
				"Aye. Your task is to slay " + task.total + " " + task.npcName + "s.",
				"Try the Lumbridge area — there's plenty about.",
				"Now off with you.");
			player.message("@gre@New Slayer task: kill " + task.total + " " + task.npcName + "s.");
		} else if (option == 1) {
			npcsay(player, n,
				"Slayer is the fine art of huntin' particular creatures.",
				"I'll mark a target, you bring it down — earn experience and a name for yourself.",
				"The harder the prey, the more you earn.");
		} else {
			npcsay(player, n, "Suit yourself. Come back when you're feelin' braver.");
		}
	}

	private void completeTask(final Player player, final Npc n, final SlayerData task) {
		final int total = SlayerService.addXp(player, COMPLETION_BONUS_XP);
		final int lvl = SlayerService.getLevel(total);
		SlayerService.clearTask(player);
		npcsay(player, n,
			"Aye, you got 'em all. Knew you had it in ye.",
			"Here, a token for finishing — return when you'd like another contract.");
		player.message("@gre@Slayer task complete! +" + COMPLETION_BONUS_XP
			+ " bonus XP. Total: " + total + " (lvl " + lvl + ").");
	}

	private void reportProgress(final Player player, final Npc n, final SlayerData task, final int lvl) {
		npcsay(player, n,
			"You're still on a contract. " + task.remaining + " " + task.npcName + "s left to slay.",
			"Don't come back 'til it's done.");
		player.message("@gre@Slayer task: " + task.remaining + "/" + task.total
			+ " " + task.npcName + "s left. (Slayer level " + lvl + ")");
	}
}

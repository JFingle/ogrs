package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.Shop;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.custom.skills.slayer.SlayerData;
import com.openrsc.server.plugins.custom.skills.slayer.SlayerService;
import com.openrsc.server.plugins.custom.skills.slayer.SlayerShop;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Grizzled Traveler — Slayer Master at (122, 650).
 *
 * Owns the Talk-to interaction surface for NPC id 836. Branches:
 *   * No active task  → offer task / explain Slayer / browse shop / decline
 *   * Task in progress → report remaining + Slayer level / browse shop
 *   * Task complete   → reward XP + clear task / browse shop
 *
 * The "browse shop" path looks up the Slayer shop registered by
 * {@link SlayerShop} via the world's shop list and opens it on demand.
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
		final int lvl = SlayerService.getPlayerLevel(player);

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
			"Show me what you've got for sale.",
			"Not right now, thanks.");

		if (option == 0) {
			final SlayerData task = SlayerService.assignRandomTask(player);
			npcsay(player, n,
				"Aye. Your task is to slay " + task.total + " " + task.npcName + "s.",
				"There's plenty about the Lumbridge area.",
				"Now off with you.");
			player.message("@gre@New Slayer task: kill " + task.total + " " + task.npcName + "s.");
		} else if (option == 1) {
			npcsay(player, n,
				"Slayer is the fine art of huntin' particular creatures.",
				"I'll mark a target, you bring it down — earn experience and a name for yourself.",
				"The harder the prey, the more you earn.");
		} else if (option == 2) {
			openShop(player, n);
		} else {
			npcsay(player, n, "Suit yourself. Come back when you're feelin' braver.");
		}
	}

	private void completeTask(final Player player, final Npc n, final SlayerData task) {
		final int total = SlayerService.addXp(player, COMPLETION_BONUS_XP);
		final int lvl = SlayerService.getPlayerLevel(player);
		SlayerService.clearTask(player);
		npcsay(player, n,
			"Aye, you got 'em all. Knew you had it in ye.",
			"Here, a token for finishing — return when you'd like another contract.");
		player.message("@gre@Slayer task complete! +" + COMPLETION_BONUS_XP
			+ " bonus XP. Total: " + total + " (lvl " + lvl + ").");

		offerShopAfterDialog(player, n);
	}

	private void reportProgress(final Player player, final Npc n, final SlayerData task, final int lvl) {
		npcsay(player, n,
			"You're still on a contract. " + task.remaining + " " + task.npcName + "s left to slay.",
			"Don't come back 'til it's done.");
		player.message("@gre@Slayer task: " + task.remaining + "/" + task.total
			+ " " + task.npcName + "s left. (Slayer level " + lvl + ")");

		offerShopAfterDialog(player, n);
	}

	/** Inline shop offer used after the task progress / completion dialog. */
	private void offerShopAfterDialog(final Player player, final Npc n) {
		final int opt = multi(player, n,
			"Show me what you've got for sale.",
			"No, that'll be all.");
		if (opt == 0) {
			openShop(player, n);
		}
	}

	/** Opens the SlayerShop instance registered with the world. */
	private void openShop(final Player player, final Npc n) {
		Shop shop = null;
		for (final Shop s : player.getWorld().getShops()) {
			if (SlayerShop.NAME.equals(s.area)) {
				shop = s;
				break;
			}
		}
		if (shop == null) {
			npcsay(player, n, "Hm. Seems my stock's gone walkabout. Try me again shortly.");
			return;
		}
		player.setAccessingShop(shop);
		ActionSender.showShop(player, shop);
	}
}

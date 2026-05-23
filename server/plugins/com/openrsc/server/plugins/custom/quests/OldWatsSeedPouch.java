package com.openrsc.server.plugins.custom.quests;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.OgrsNpcId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.KillNpcTrigger;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;
import com.openrsc.server.util.rsc.DataConversions;

import static com.openrsc.server.plugins.Functions.give;
import static com.openrsc.server.plugins.Functions.multi;
import static com.openrsc.server.plugins.Functions.npcsay;
import static com.openrsc.server.plugins.Functions.say;

/**
 * OGRS quest: Old Wat's Missing Seed Pouch.
 *
 * First quest piped through the YAML quest pipeline. Metadata (id 52,
 * name, points, journal, rewards) lives in
 * {@code content/quests/old_wats_seed_pouch.yaml} and is consumed via
 * {@link AbstractOgrsQuest}. This class only hosts the trigger logic.
 *
 * State machine (player.getQuestStage(this)):
 *   0  Not started.
 *      Old Wat's Talk-to opens with farming flavor + an option to ask
 *      what's wrong. Choosing "Anything I can help with?" branches into
 *      the pouch hook; accepting moves to stage 1.
 *   1  Searching.
 *      Goblins (id 62) drop the Seed Pouch (1598) at 30% on kill,
 *      moving the player to stage 2. Talking to Old Wat re-tells the
 *      mission; if the player already has the pouch, falls through to
 *      stage 2 dialog.
 *   2  Returned.
 *      Talking to Old Wat takes the pouch and triggers
 *      sendQuestComplete → AbstractOgrsQuest.handleReward (XP + items
 *      + quest points).
 *  -1  Completed.
 *      Old Wat falls back to generic farmer chat. (Replaces what the
 *      now-deleted BoazTheFarmer.java used to handle.)
 *
 * Old Wat's NPC plugin file is removed; this class owns Old Wat's
 * Talk-to trigger entirely. Two plugins both returning blockTalkNpc=true
 * for the same NPC would fire BOTH onTalkNpc handlers (PluginHandler
 * iterates and accumulates — confirmed by reading the dispatcher).
 *
 * The {@link OldWatFarmShop} plugin still owns Old Wat's right-click
 * "Trade" verb (different trigger — OpNpc). No conflict.
 */
public final class OldWatsSeedPouch extends AbstractOgrsQuest implements TalkNpcTrigger, KillNpcTrigger {

	private static final int OLD_WAT_NPC_ID = OgrsNpcId.OLD_WAT.id();
	private static final int GOBLIN_NPC_ID = 62;  // upstream NpcId.GOBLIN_LVL13 family
	private static final int GOBLIN_SHAMAN_NPC_ID = OgrsNpcId.GOBLIN_SHAMAN.id();

	/** 30% drop on rank-and-file goblin kill while in stage 1. */
	private static final int POUCH_DROP_PERCENT = 30;

	public OldWatsSeedPouch() {
		super("old_wats_seed_pouch.yaml");
	}

	// ===== TalkNpc =====

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		return n.getID() == OLD_WAT_NPC_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		final int stage = player.getQuestStage(this);
		final boolean hasPouch = player.getCarriedItems().hasCatalogID(ItemId.OGRS_SEED_POUCH.id());

		if (stage == 0) {
			talkNotStarted(player, n);
		} else if (stage == 1 && !hasPouch) {
			talkSearching(player, n);
		} else if (stage >= 1 && hasPouch) {
			talkReturning(player, n);
		} else {
			talkAfterCompleted(player, n);
		}
	}

	private void talkNotStarted(final Player player, final Npc n) {
		npcsay(player, n,
			"Working the long field today.",
			"Could use a hand if you've a moment.");
		final int choice = multi(player, n,
			"What's that you're working on?",
			"Anything I can help with?",
			"I'll come back later.");

		if (choice == 0) {
			npcsay(player, n,
				"Mostly potatoes — hardy. They forgive a busy man.",
				"Onions and tomatoes too in the rotation. Different soil for each.",
				"Rake the bed first, then a seed in the turned earth.");
		} else if (choice == 1) {
			npcsay(player, n,
				"Funny you should ask.",
				"Lost my seed pouch out east last week — near where the goblins make camp.",
				"Those green pests must have grabbed it.",
				"Bring it back and I'll see you right with seeds and coin.");
			final int yes = multi(player, n,
				"I'll find it for you.",
				"Maybe another time.");
			if (yes == 0) {
				say(player, n, "I'll find it for you.");
				npcsay(player, n,
					"Bless you. Goblins drop their kit when they fall — that's where it'll be.",
					"East of the castle, past the fields.");
				player.updateQuestStage(this, 1);
			} else if (yes == 1) {
				say(player, n, "Maybe another time.");
				npcsay(player, n, "Walk well, then.");
			}
		} else {
			npcsay(player, n, "Walk well.");
		}
	}

	private void talkSearching(final Player player, final Npc n) {
		npcsay(player, n,
			"Any luck with that pouch?",
			"It'll be on one of the goblins out east. They don't give it up easy.");
		final int choice = multi(player, n,
			"What did the pouch look like again?",
			"I'll keep looking.");
		if (choice == 0) {
			npcsay(player, n,
				"Small leather thing. Drawstring top.",
				"Smells of soil and seed — you'll know it when you see it.");
		} else {
			npcsay(player, n, "Walk well.");
		}
	}

	private void talkReturning(final Player player, final Npc n) {
		say(player, n, "I found your pouch.");
		npcsay(player, n,
			"Bless you. Pass it here.",
			"Take some seeds and a few coins for the trouble — and my thanks.");
		player.getCarriedItems().remove(new Item(ItemId.OGRS_SEED_POUCH.id(), 1));
		player.sendQuestComplete(getQuestId());
	}

	private void talkAfterCompleted(final Player player, final Npc n) {
		// Folded-in flavor from the retired BoazTheFarmer talk handler so
		// Old Wat still has something to say when the quest is done.
		npcsay(player, n,
			"How's the planting? Soil treating you well?",
			"Mind the goblins out east — greedy little ones.",
			"Plenty more rows to tend. Walk well.");
	}

	// ===== KillNpc =====

	/** Returning true causes onKillNpc to fire — does NOT block default
	 *  loot. Loot drop happens after the plugin handler in Npc.java's
	 *  death sequence regardless. */
	@Override
	public boolean blockKillNpc(final Player player, final Npc npc) {
		final int id = npc.getID();
		if (id != GOBLIN_NPC_ID && id != GOBLIN_SHAMAN_NPC_ID) return false;
		if (player.getQuestStage(this) != 1) return false;
		// Don't roll if the player already has one in inventory.
		return !player.getCarriedItems().hasCatalogID(ItemId.OGRS_SEED_POUCH.id());
	}

	@Override
	public void onKillNpc(final Player player, final Npc npc) {
		final boolean shaman = npc.getID() == GOBLIN_SHAMAN_NPC_ID;
		// Shaman = guaranteed drop; rank-and-file = 30% roll.
		final boolean dropped = shaman || DataConversions.random(1, 100) <= POUCH_DROP_PERCENT;
		if (!dropped) return;

		give(player, ItemId.OGRS_SEED_POUCH.id(), 1);
		if (shaman) {
			player.message("@gre@The shaman crumples. A leather pouch tumbles from a fold of its robe — Old Wat's.");
		} else {
			player.message("@gre@A small leather pouch falls from the goblin's belt. This must be Old Wat's.");
		}
		player.updateQuestStage(this, 2);
	}
}

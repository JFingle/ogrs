package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.Skill;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Old Aric the Wayfinder — id 843 — Lumbridge castle approach (126,651).
 *
 * OGRS analogue of OSRS's Adventurer Jon. A wandering elder who gives
 * tips that adapt to what the player has been doing: the lowest skill
 * level gets called out first, so a brand-new account feels guided
 * toward an obvious next step.
 *
 * Dialog branches:
 *   1. "What should I do next?" — picks a tip based on lowest
 *      meaningful skill (combat / cooking / mining / woodcutting),
 *      else a general wandering-spirit hint.
 *   2. "Tell me about this place." — flavor / world-building.
 *   3. "Any tips for the fight?" — combat tactics.
 *   4. "Just passing through." — goodbye.
 *
 * Future expansion (task #27 follow-up): track milestones via
 * player.getCache() and dispense small rewards at thresholds (first
 * 99, first quest complete, first 100 of a slayer task).
 */
public class OldAric implements TalkNpcTrigger {

	private static final int NPC_ID = 843;

	// Skill levels below these thresholds get specifically suggested.
	// Tuning rationale: "still using a bronze axe" / "still on tier-1
	// foods" / "haven't really hunted yet" should fire below these.
	private static final int COMBAT_GREEN  = 10;
	private static final int COOK_GREEN    = 10;
	private static final int MINE_GREEN    = 15;
	private static final int WOOD_GREEN    = 15;
	private static final int FISH_GREEN    = 10;
	private static final int FIRE_GREEN    = 10;

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		return n.getID() == NPC_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Easy now, friend. Sit a moment.",
			"I've walked these roads since before the river found its bed.");

		boolean stay = true;
		while (stay) {
			final int option = multi(player, n,
				"What should I do next?",
				"Tell me about this place.",
				"Any tips for the fight?",
				"Just passing through.");

			switch (option) {
				case 0: tipForNextStep(player, n); break;
				case 1: worldFlavor(player, n);    break;
				case 2: combatTips(player, n);     break;
				default: stay = false;
			}
		}
		npcsay(player, n, "Walk well. The road remembers those who walk it kindly.");
	}

	private void tipForNextStep(final Player player, final Npc n) {
		// Lowest "green" skill calls the shot. Order is intentional —
		// combat first because survival matters, then food/fuel, then
		// gathering. Each branch returns once a tip fires.
		final int combat   = player.getCombatLevel();
		final int cook     = player.getSkills().getLevel(Skill.COOKING.id());
		final int mine     = player.getSkills().getLevel(Skill.MINING.id());
		final int wood     = player.getSkills().getLevel(Skill.WOODCUTTING.id());
		final int fish     = player.getSkills().getLevel(Skill.FISHING.id());
		final int fire     = player.getSkills().getLevel(Skill.FIREMAKING.id());

		if (combat < COMBAT_GREEN) {
			npcsay(player, n,
				"You've fight in you yet, but not the practice for it.",
				"The cows north of the river are forgiving teachers.",
				"When they grow easy, the goblins east of town will test you proper.");
			return;
		}
		if (cook < COOK_GREEN && fish < FISH_GREEN) {
			npcsay(player, n,
				"A wanderer should know how to feed himself.",
				"There's shrimp in the river south of the castle — net them, char them on a fire.",
				"Edith in the square will show you bread, if coin's no object.");
			return;
		}
		if (cook < COOK_GREEN) {
			npcsay(player, n,
				"You can gather, but can you cook?",
				"Make a fire with a tinderbox and a log, then char what you've caught.",
				"Burnt food teaches as much as a perfect roast does, mind.");
			return;
		}
		if (mine < MINE_GREEN) {
			npcsay(player, n,
				"There's metal in the earth waiting for a patient hand.",
				"Tin and copper rocks lie southwest, past the Lumbridge swamp.",
				"Mine both, smelt them together, and you'll have bronze.");
			return;
		}
		if (wood < WOOD_GREEN) {
			npcsay(player, n,
				"A good axe will outlast a poor sword most days.",
				"Trees crowd the road north of here — bring a bronze axe at least.",
				"Yew will come later, when your arms are stronger.");
			return;
		}
		if (fire < FIRE_GREEN) {
			npcsay(player, n,
				"You've logs and a flint, but no warmth yet.",
				"Strike the tinderbox to the log right in your pack — a fire'll start under you.",
				"Easier than dropping the log first, eh?");
			return;
		}

		// Player is past the early-greens — give them a broader nudge.
		npcsay(player, n,
			"You've found your feet, friend.",
			"The hard work now is choosing a direction, not learning the road.",
			"Talk to anyone who's standing still. The ones who tarry have stories.",
			"And keep an eye for strangers — many a journey begins with one.");
	}

	private void worldFlavor(final Player player, final Npc n) {
		npcsay(player, n,
			"This is Old Gielinor. Older than the maps name it.",
			"There are kingdoms north — Varrock for swords, Falador for steel.",
			"Karamja burns to the south, all jungle and ash.",
			"And the wilderness past the hedge — that's no place to die for nothing.");
	}

	private void combatTips(final Player player, final Npc n) {
		npcsay(player, n,
			"Three things keep a man alive in a scrap.",
			"First — know when to walk away. You can run now, did you know that?",
			"Second — armor before glory. A cracked helm has saved more lives than a fine sword.",
			"Third — feed yourself between fights. Don't trust a full health bar; trust your pack.");
	}
}

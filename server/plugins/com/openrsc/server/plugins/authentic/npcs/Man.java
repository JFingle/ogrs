package com.openrsc.server.plugins.authentic.npcs;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.NpcId;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;
import com.openrsc.server.util.rsc.DataConversions;

import static com.openrsc.server.plugins.Functions.*;

public class Man implements TalkNpcTrigger {

	@Override
	public boolean blockTalkNpc(Player player, Npc n) {
		// Dialogue same between all Man, Farmer, Thief, Rogue, Alkharid Warrior
		return inArray(n.getID(), NpcId.MAN.id(), NpcId.MAN_ALKHARID.id(), NpcId.MAN_ARDOUGNE.id(),
			NpcId.FARMER.id(), NpcId.FARMER_ARDOUGNE.id(),
			NpcId.THIEF.id(), NpcId.THIEF_BLANKET.id(), NpcId.HEAD_THIEF.id(),
			NpcId.ROGUE.id(), NpcId.ALKHARID_WARRIOR.id());
	}

	@Override
	public void onTalkNpc(Player player, Npc n) {
		// OGRS — pool extended from 20 to 25 with five Lumbridge-area-aware
		// lines that reference OGRS-added content (Old Aric, Old Wat, the
		// allotment, the spider hollow, Garth's smith stall). Keeps upstream
		// flavor intact while letting villagers feel like they live in THIS
		// world. (sparky 2026-05-19: 'NPCs need more character'.)
		int selected = DataConversions.getRandom().nextInt(25);
		boolean autoChoose = DataConversions.getRandom().nextBoolean();
		String[] menuOptions;

		say(player, n, "Hello", "How's it going?");

		if (selected == 0)
			npcsay(player, n, "Get out of my way", "I'm in a hurry");
		else if (selected == 1)
			player.message("The man ignores you");
		else if (selected == 2)
			npcsay(player, n, "Not too bad");
		else if (selected == 3)
			npcsay(player, n, "Very well, thank you");
		else if (selected == 4) {
			npcsay(player, n, "Have this flier");
			give(player, ItemId.FLIER.id(), 1);
		} else if (selected == 5)
			npcsay(player, n, "I'm a little worried",
				"I've heard there's lots of people going about,",
				"killing citizens at random");
		else if (selected == 6) {
			npcsay(player, n, "I'm fine", "How are you?");
			say(player, n, "Very well, thank you");
		} else if (selected == 7)
			npcsay(player, n, "Hello");
		else if (selected == 8) {
			npcsay(player, n, "Who are you?");
			say(player, n, "I am a bold adventurer");
			npcsay(player, n, "A very noble profession");
		} else if (selected == 9) {
			npcsay(player, n, "Not too bad",
				"I'm a little worried about the increase in Goblins these days");
			say(player, n, "Don't worry. I'll kill them");
		} else if (selected == 10)
			npcsay(player, n, "Hello", "Nice weather we've been having");
		else if (selected == 11)
			npcsay(player, n, "No, I don't want to buy anything");
		else if (selected == 12) {
			npcsay(player, n, "Do I know you?");
			say(player, n,
				"No, I was just wondering if you had anything interesting to say");
		} else if (selected == 13) {
			npcsay(player, n, "How can I help you?");
			menuOptions = new String[]{"Do you wish to trade?",
				"I'm in search of a quest",
				"I'm in search of enemies to kill"};
			int option;
			if (autoChoose) {
				option = DataConversions.getRandom().nextInt(menuOptions.length);
			} else {
				option = multi(player, n, false, menuOptions);
			}
			if (option == 0) {
				say(player, n, "Do you wish to trade?");
				npcsay(player, n, "No, I have nothing I wish to get rid of",
					"If you want to do some trading,",
					"there are plenty of shops and market stalls around though");
			}
			else if (option == 1) {
				say(player, n, "I'm in search of a quest");
				npcsay(player, n, "I'm sorry I can't help you there");
			}
			else if (option == 2) {
				say(player, n, "I'm in search of enemies to kill");
				npcsay(player, n,
					"I've heard there are many fearsome creatures under the ground");
			}
		} else if (selected == 14) {
			npcsay(player, n, "Are you asking for a fight?");
			n.startCombat(player);
		} else if (selected == 15)
			npcsay(player, n, "That is classified information");
		else if (selected == 16)
			npcsay(player, n, "No, I don't have any spare change");
		else if (selected == 17)
			npcsay(player, n, "None of your business");
		else if (selected == 18)
			npcsay(player, n, "I think we need a new king",
				"The one we've got isn't very good");
		else if (selected == 19)
			npcsay(player, n, "Yo wassup!");
		// OGRS-flavor lines (20-24). Reference Lumbridge-area content the
		// player can actually find: Old Aric near castle, Old Wat at the
		// allotment east of town, Edith's bakery, the spider hollow SW
		// of Lumbridge, Garth's smith stall.
		else if (selected == 20)
			npcsay(player, n,
				"Did you talk to the old pilgrim by the castle yet?",
				"Says he's seen everything twice. Probably has.");
		else if (selected == 21)
			npcsay(player, n,
				"Edith's flour prices are getting out of hand.",
				"It's the mill, she says. I say it's something else entirely.");
		else if (selected == 22)
			npcsay(player, n,
				"Don't wander southwest of Lumbridge if you can help it.",
				"There's spiders down there. Big ones.",
				"My cousin's lad saw one big as a hound.");
		else if (selected == 23)
			npcsay(player, n,
				"Old Wat's allotment is the strangest patch of dirt in the kingdom.",
				"He talks to his plants like they're listening.",
				"Maybe they are. Things grow there.");
		else if (selected == 24)
			npcsay(player, n,
				"Garth at the smith stall — his tools are honest work.",
				"Won't sell you a sword, mind. Says that's Varrock's trade.");
	}
}

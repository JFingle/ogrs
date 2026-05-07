package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Samuel the Scribe (NPC id 838).
 *
 * Hannah's son. The biblical Samuel was raised in the temple, became a
 * prophet, anointed kings. In OGRS he's a young scholar — quiet, observant,
 * someone you'd trust with a letter. Dialog references his mother and
 * carries the "called to listen" temperament without doctrine.
 */
public class SamuelTheScribe implements TalkNpcTrigger {

	private static final int NPC_ID = 838;

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		return n.getID() == NPC_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Greetings. Are you new to Lumbridge?",
			"I keep records here — births, harvests, who passed through and who didn't.");

		final int option = multi(player, n,
			"What brings a scholar to a small village?",
			"Have you seen anything strange lately?",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"My mother is here. She tends sheep in the fields north-west of the castle.",
				"She gave up a great deal so I could read and write. I won't be far from her.");
			npcsay(player, n,
				"And I find I learn more from quiet villages than from libraries.",
				"You hear the truth easier when there isn't a crowd to please.");
		} else if (option == 1) {
			npcsay(player, n,
				"Strange? Always.",
				"There's an old man under a tree to the east — Job. Spend an evening listening to him sometime.",
				"He has seen things most of us are spared, and somehow speaks softer for it.");
		} else {
			npcsay(player, n, "May your road be straight, friend.");
		}
	}
}

package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/** Benjamin (id 842) — a village kid full of plans. */
public class BenjaminTheBoy implements TalkNpcTrigger {
	private static final int NPC_ID = 842;

	@Override public boolean blockTalkNpc(final Player player, final Npc n) { return n.getID() == NPC_ID; }

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Hi! Are you an adventurer?",
			"I'm gonna be one too. Soon as Mum lets me past the gate.");

		final int option = multi(player, n,
			"What kind of adventurer?",
			"Have you ever beaten a goblin?",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"The kind that fights goblins! And dragons. And bigger goblins!",
				"Then I'd come back and tell everyone, and Mum would say I have to sweep first.");
		} else if (option == 1) {
			npcsay(player, n,
				"...one time. With a stick.",
				"It was running away. Reuben SAYS it counts.");
		} else {
			npcsay(player, n, "Bye! Watch out for goblins!");
		}
	}
}

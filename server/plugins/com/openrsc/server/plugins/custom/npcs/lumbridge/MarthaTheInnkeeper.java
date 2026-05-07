package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/** Martha the Innkeeper (id 843) — bustling, capable, no time for nonsense. */
public class MarthaTheInnkeeper implements TalkNpcTrigger {
	private static final int NPC_ID = 843;

	@Override public boolean blockTalkNpc(final Player player, final Npc n) { return n.getID() == NPC_ID; }

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Eh? Sorry, traveller, the soup's not waiting on me. Speak quick.",
			"Bread's fresh, ale's passable, beds upstairs aren't the worst.");

		final int option = multi(player, n,
			"Anything happening in the village?",
			"You always this busy?",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"Goblins to the north. There's always goblins to the north.",
				"And there's an old man under the tree out east. Doesn't eat much. Hardly drinks anything either.",
				"I leave him a loaf when I can. He never asks. That's why.");
		} else if (option == 1) {
			npcsay(player, n,
				"Always. Could be worse — could be sitting still.",
				"There's plenty of folk who have time to think. Half of them think themselves into circles.");
		} else {
			npcsay(player, n, "Mind the door on the way out!");
		}
	}
}

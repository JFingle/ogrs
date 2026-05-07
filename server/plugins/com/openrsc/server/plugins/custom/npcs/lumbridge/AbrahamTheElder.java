package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Abraham the Elder (id 844). The patriarch — a man who left his home
 * because something deeper than home called him.
 */
public class AbrahamTheElder implements TalkNpcTrigger {
	private static final int NPC_ID = 844;

	@Override public boolean blockTalkNpc(final Player player, final Npc n) { return n.getID() == NPC_ID; }

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Hello, friend.",
			"I haven't been in this village long. I rarely am, in any village.");

		final int option = multi(player, n,
			"Where are you going?",
			"Where are you from?",
			"You look tired.",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"I do not know exactly. The road tells me.",
				"I left a place I knew well, a long time ago, because something asked me to.",
				"Some days I feel foolish for it. Most days I don't.");
		} else if (option == 1) {
			npcsay(player, n,
				"A city far behind me. Nothing of it remains worth telling.",
				"What I carry now I did not have then.");
		} else if (option == 2) {
			npcsay(player, n,
				"I am old, friend. Tired is just my shape now.",
				"But I would not trade the road for a younger body that stayed at home.");
		} else {
			npcsay(player, n, "Go well.");
		}
	}
}

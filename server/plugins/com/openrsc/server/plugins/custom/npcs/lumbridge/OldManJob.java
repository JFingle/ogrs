package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Old Man Job (NPC id 839).
 *
 * The book of Job — a man who lost his children, his wealth, his health,
 * and held to integrity through it. The point of the story isn't that he
 * "won" — it's that he met something larger than the loss. In OGRS he sits
 * under a tree, ash on his cloak, calm in his eyes. Dialog touches the
 * shape of trials without explanation.
 */
public class OldManJob implements TalkNpcTrigger {

	private static final int NPC_ID = 839;

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		return n.getID() == NPC_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Sit a moment, if you'd like. The shade is good.",
			"I have nothing to sell and nothing to teach. Just a tree, and time.");

		final int option = multi(player, n,
			"Why the ash on your cloak?",
			"You look like you've been through a great deal.",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"It used to mean something. Mourning, mostly.",
				"It's been there long enough now that I forget I'm wearing it.");
			npcsay(player, n,
				"The dust reminds me of where I started.",
				"And how much smaller I am than I once thought.");
		} else if (option == 1) {
			npcsay(player, n,
				"Ah. Yes.",
				"I lost more than I had any right to keep — children, lands, the body of my youth.",
				"You'd think it would have hollowed me out.");
			npcsay(player, n,
				"But I have come to think a man is not what he holds.",
				"He's what holds him, when he can hold nothing himself.");
		} else {
			npcsay(player, n, "Walk gently, friend. The road is long.");
		}
	}
}

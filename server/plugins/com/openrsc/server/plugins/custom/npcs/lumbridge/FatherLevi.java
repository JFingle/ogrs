package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/** Father Levi the Priest (id 840) — Lumbridge churchyard. */
public class FatherLevi implements TalkNpcTrigger {
	private static final int NPC_ID = 840;

	@Override public boolean blockTalkNpc(final Player player, final Npc n) { return n.getID() == NPC_ID; }

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Peace, traveller. The church is open if you've need of it.",
			"I keep the candles lit and the door unlocked. That's about it most days.");

		final int option = multi(player, n,
			"What's your work here, Father?",
			"Will you pray for me?",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"To listen, mostly. Births, deaths, the things people carry.",
				"And to remind them they are not alone in carrying them.");
		} else if (option == 1) {
			npcsay(player, n,
				"Of course. I do most evenings — for travellers, soldiers, the sick.",
				"Walk safe. The road is long, but you're not as alone on it as you might feel.");
		} else {
			npcsay(player, n, "Go in peace.");
		}
	}
}

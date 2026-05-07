package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Anna the Prophetess (id 841). Mirrors Luke 2 — an aged widow who
 * waited many years in the temple and recognised the Promised One when
 * she finally saw him.
 */
public class AnnaTheProphetess implements TalkNpcTrigger {
	private static final int NPC_ID = 841;

	@Override public boolean blockTalkNpc(final Player player, final Npc n) { return n.getID() == NPC_ID; }

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Bless you, child. Sit if your legs are weary.",
			"I've kept this corner of the church for many decades now.");

		final int option = multi(player, n,
			"Why have you stayed here so long?",
			"Have you seen many strange travellers?",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"My husband died young. I had nowhere I needed to be.",
				"So I stayed where the silence is kind, and I waited.");
			npcsay(player, n,
				"What was I waiting for? I'm not sure I could put it in words anymore.",
				"But when it came I knew it. And I have been at peace ever since.");
		} else if (option == 1) {
			npcsay(player, n,
				"Many. The road brings them in.",
				"Watch for the quiet ones, child. The loud ones tell you who they are.",
				"The quiet ones tell you who you are.");
		} else {
			npcsay(player, n, "Walk well.");
		}
	}
}

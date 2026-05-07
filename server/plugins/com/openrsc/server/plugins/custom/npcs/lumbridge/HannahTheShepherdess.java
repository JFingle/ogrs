package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.*;

/**
 * Hannah the Shepherdess (NPC id 837).
 *
 * Lore note: the biblical Hannah (1 Samuel 1) was a barren wife who wept
 * before God for a child and was given Samuel. In OGRS she's content,
 * tending sheep, with a son who is a scholar in the village. Dialog hints
 * at the connection without naming chapter and verse.
 */
public class HannahTheShepherdess implements TalkNpcTrigger {

	private static final int NPC_ID = 837;

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		return n.getID() == NPC_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		npcsay(player, n,
			"Oh — hello there, traveller.",
			"Mind your step around the lambs, would you? They're in a mood today.");

		final int option = multi(player, n,
			"How long have you been a shepherdess?",
			"Quiet life out here.",
			"Goodbye.");

		if (option == 0) {
			npcsay(player, n,
				"Most of my life now. I wasn't always.",
				"There was a time I'd have given anything for a son to come home to.",
				"And one day, against all the odds, one came.");
			npcsay(player, n,
				"He's a scribe in the village now — Samuel. Quiet boy, watches the world.",
				"You'll know him by the ink under his fingernails.");
		} else if (option == 1) {
			npcsay(player, n,
				"It is. Quieter than the wars to the north, anyway.",
				"There's grace in small mornings. People forget that.");
		} else {
			npcsay(player, n, "Walk safe, traveller.");
		}
	}
}

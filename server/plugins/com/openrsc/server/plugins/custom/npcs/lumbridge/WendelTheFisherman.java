package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.npcsay;

/** Wendel the Fisherman (id 841) — riverside ambience. Brief flavor only. */
public class WendelTheFisherman implements TalkNpcTrigger {
	private static final int NPC_ID = 841;
	@Override public boolean blockTalkNpc(Player p, Npc n) { return n.getID() == NPC_ID; }
	@Override public void onTalkNpc(Player p, Npc n) {
		npcsay(p, n,
			"Quiet day on the river.",
			"The fish know when to hide. Wiser than half the men I've met.");
	}
}

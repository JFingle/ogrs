package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.TalkNpcTrigger;

import static com.openrsc.server.plugins.Functions.npcsay;

/**
 * Shared dialog plugin for the OGRS ambient Lumbridge villagers (NPC ids
 * 845–854). One short flavor exchange per id — enough to make the village
 * feel inhabited without writing a dedicated plugin for each.
 *
 * If a villager grows beyond a one-liner (gains a quest hook, opens a
 * shop, becomes a recurring character), promote them to their own
 * TalkNpcTrigger plugin and remove their case from here.
 */
public class OgrsAmbientVillagers implements TalkNpcTrigger {

	private static final int MIN_ID = 845;
	private static final int MAX_ID = 854;

	@Override
	public boolean blockTalkNpc(final Player player, final Npc n) {
		final int id = n.getID();
		// Boaz (850) was promoted to a dedicated dialog plugin
		// (BoazTheFarmer) — first Farming-skill gameplay master.
		// Two trigger plugins firing on the same NPC would dispatch both
		// onTalkNpc methods; explicitly carve him out here.
		if (id == 850) return false;
		return id >= MIN_ID && id <= MAX_ID;
	}

	@Override
	public void onTalkNpc(final Player player, final Npc n) {
		switch (n.getID()) {
			case 845: // Miriam the Baker
				npcsay(player, n,
					"Bread's still in the oven, traveller. Come back when the loaves are out.",
					"You'll smell them before you see them.");
				break;
			case 846: // Elias the Fisherman
				npcsay(player, n,
					"Quiet day on the river.",
					"The fish know when to hide. Wiser than half the men I've met.");
				break;
			case 847: // Naomi the Weaver
				npcsay(player, n,
					"There's a rhythm to this. You learn to listen for it.",
					"And what I weave keeps someone warm. That's enough most days.");
				break;
			case 848: // Caleb the Smith
				npcsay(player, n,
					"Always work for a smith. Never enough hours.",
					"Bring me a bent blade if you find one. I'll straighten it for cheap.");
				break;
			case 849: // Ruth the Gleaner
				npcsay(player, n,
					"Just gathering what was left at the field's edge.",
					"There is grace in what others overlook.");
				break;
			case 850: // Boaz the Farmer
				npcsay(player, n,
					"Working the long field today. If you see Ruth gleaning the edges,",
					"tell her there's a pitcher of cool water by the gate.");
				break;
			case 851: // Lydia the Seller
				npcsay(player, n,
					"Fine cloth, traveller — purple, dyed proper.",
					"Not today perhaps. Another time. I'll be in the market until dusk.");
				break;
			case 852: // Esther the Maiden
				npcsay(player, n,
					"Mind yourself, sir. The well is deep here.",
					"And the water cold enough to wake a corpse.");
				break;
			case 853: // Reuben the Boy
				npcsay(player, n,
					"Did you SEE the size of that one?",
					"I'm catching it tomorrow! Benjamin doesn't believe me but he'll see.");
				break;
			case 854: // Tabitha the Seamstress
				npcsay(player, n,
					"If you tear that cloak again, bring it back.",
					"I'll mend it twice if I must. Better than throwing good cloth out.");
				break;
			default:
				// Should be unreachable if blockTalkNpc is correct.
				npcsay(player, n, "Hello, traveller.");
		}
	}
}

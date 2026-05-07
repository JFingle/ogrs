// === GENERATED FILE — DO NOT EDIT BY HAND ===
// Source: content/npcs/*.yaml
// Regenerate: python3 tools/codegen-client-npcs.py
// See backlog #6(a) — build-time codegen for the client NPC table.

package com.openrsc.client.entityhandling.generated;

import com.openrsc.client.entityhandling.defs.NPCDef;
import java.util.ArrayList;

public final class OgrsClientNpcs {

	private OgrsClientNpcs() { /* no instances */ }

	/**
	 * Append every OGRS YAML-defined NPC to the client's NPCDef list,
	 * keeping id == list-index alignment with the server-side load order.
	 * Returns the next free id. Caller threads `i` through:
	 *   <pre>i = OgrsClientNpcs.register(npcs, i);</pre>
	 */
	public static int register(final ArrayList<NPCDef> npcs, int i) {
		int[] sprites;

		// id 836 — from content/npcs/grizzled_traveler.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Grizzled Traveler", "A weathered figure who has clearly seen too much.", "", "Trade", 20, 25, 40, 30, false, sprites, 0xAAAAAA, 0x6B4226, 0x4F2D1B, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 837 — from content/npcs/hannah_the_shepherdess.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Hannah", "A weathered shepherdess. There is a quiet joy about her.", "", 1, 1, 5, 1, false, sprites, 0xA88858, 0x3A6BA0, 0x6B5230, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 838 — from content/npcs/samuel_the_scribe.yaml
		sprites = new int[]{0, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Samuel", "A young scholar with ink-stained fingers. He listens more than he speaks.", "", 1, 1, 5, 1, false, sprites, 0x4A2D1B, 0xE8E4D0, 0x6B5230, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 839 — from content/npcs/old_man_job.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Old Man Job", "Ash on his cloak, calm in his eyes. He looks like he has weathered storms most never see.", "", 1, 1, 5, 1, false, sprites, 0xDDDDDD, 0x707070, 0x4F2D1B, 0xC68642, 160, 220, 6, 6, 5, i++));

		// id 840 — from content/npcs/father_levi_the_priest.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Father Levi", "A village priest with kind eyes and ink-stained sleeves.", "", 1, 1, 5, 1, false, sprites, 0xCCCCCC, 0xE8E4D0, 0x4A4A4A, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 841 — from content/npcs/anna_the_prophetess.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Anna", "An aged widow who has lived many quiet years in this church.", "", 1, 1, 5, 1, false, sprites, 0xDDDDDD, 0x4A4A4A, 0x303030, 0xC68642, 160, 220, 6, 6, 5, i++));

		// id 842 — from content/npcs/benjamin_the_boy.yaml
		sprites = new int[]{0, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Benjamin", "A young boy with grass stains on his knees and somewhere to be.", "", 1, 1, 5, 1, false, sprites, 0xC4934A, 0xA02020, 0x404020, 0xCC9966, 130, 200, 6, 6, 5, i++));

		// id 843 — from content/npcs/martha_the_innkeeper.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Martha", "An innkeeper, sleeves rolled, hands always moving.", "", 1, 1, 5, 1, false, sprites, 0x6B4226, 0xC04040, 0x6B5230, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 844 — from content/npcs/abraham_the_elder.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Abraham", "An old man leaning on a long staff. Eyes that have seen great distances.", "", 1, 1, 5, 1, false, sprites, 0xEEEEEE, 0x6B5230, 0x4F2D1B, 0xC68642, 160, 220, 6, 6, 5, i++));

		// id 845 — from content/npcs/miriam_the_baker.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Miriam", "A baker with flour in her hair and a quick smile.", "", 1, 1, 5, 1, false, sprites, 0xA88858, 0xE8E4D0, 0x6B5230, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 846 — from content/npcs/elias_the_fisherman.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Elias", "A weathered fisherman, net coiled at his feet.", "", 1, 1, 5, 1, false, sprites, 0x808080, 0x3A6BA0, 0x4F2D1B, 0xC68642, 160, 220, 6, 6, 5, i++));

		// id 847 — from content/npcs/naomi_the_weaver.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Naomi", "A weaver, hands moving steadily across an unseen loom.", "", 1, 1, 5, 1, false, sprites, 0x6B4226, 0x6B5230, 0x303030, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 848 — from content/npcs/caleb_the_smith.yaml
		sprites = new int[]{0, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Caleb", "A young smith, soot on his arms, an anvil's voice nearby.", "", 1, 1, 5, 1, false, sprites, 0x303030, 0x4A2D1B, 0x303030, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 849 — from content/npcs/ruth_the_gleaner.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Ruth", "A young woman gathering what the harvesters left behind.", "", 1, 1, 5, 1, false, sprites, 0x4A2D1B, 0x886600, 0x6B4226, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 850 — from content/npcs/boaz_the_farmer.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Boaz", "A farmer with strong forearms and a sun-creased face.", "", 1, 1, 5, 1, false, sprites, 0x6B4226, 0x886600, 0x4F2D1B, 0xC68642, 160, 220, 6, 6, 5, i++));

		// id 851 — from content/npcs/lydia_the_seller.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Lydia", "A merchant of fine cloth, a basket on her arm.", "", 1, 1, 5, 1, false, sprites, 0x4A2D1B, 0x6020A0, 0x4A4A4A, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 852 — from content/npcs/esther_the_maiden.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Esther", "A young woman in a fine kerchief, courteous to strangers.", "", 1, 1, 5, 1, false, sprites, 0x303030, 0xA02020, 0x4A2D1B, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 853 — from content/npcs/reuben_the_boy.yaml
		sprites = new int[]{0, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Reuben", "A boy missing a shoe, perfectly content about it.", "", 1, 1, 5, 1, false, sprites, 0xC4934A, 0x303080, 0x404020, 0xCC9966, 130, 200, 6, 6, 5, i++));

		// id 854 — from content/npcs/tabitha_the_seamstress.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Tabitha", "A seamstress whose tunics quietly clothe half the village.", "", 1, 1, 5, 1, false, sprites, 0xA88858, 0x405060, 0x6B5230, 0xCC9966, 160, 220, 6, 6, 5, i++));

		return i;
	}
}

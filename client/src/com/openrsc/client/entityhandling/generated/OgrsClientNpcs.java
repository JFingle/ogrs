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

		// id 837 — from content/npcs/old_wat_the_farmer.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Old Wat", "A weathered farmer with sun-creased eyes and dirt under his nails.", "", "Trade", 1, 1, 5, 1, false, sprites, 0x6B4226, 0x886600, 0x4F2D1B, 0xC68642, 160, 220, 6, 6, 5, i++));

		// id 838 — from content/npcs/edith_the_baker.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Edith", "A baker with flour in her hair and a quick smile.", "", "Trade", 1, 1, 5, 1, false, sprites, 0xA88858, 0xE8E4D0, 0x6B5230, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 839 — from content/npcs/garth_the_smith.yaml
		sprites = new int[]{0, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Garth", "A young smith, soot on his arms, an anvil's voice nearby.", "", "Trade", 1, 1, 5, 1, false, sprites, 0x303030, 0x4A2D1B, 0x303030, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 840 — from content/npcs/marigold_the_cloth_seller.yaml
		sprites = new int[]{3, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Marigold", "A merchant of fine cloth, a basket on her arm.", "", "Trade", 1, 1, 5, 1, false, sprites, 0x4A2D1B, 0x6020A0, 0x4A4A4A, 0xCC9966, 160, 220, 6, 6, 5, i++));

		// id 841 — from content/npcs/wendel_the_fisherman.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Wendel", "A weathered fisherman, net coiled at his feet.", "", 1, 1, 5, 1, false, sprites, 0x808080, 0x3A6BA0, 0x4F2D1B, 0xC68642, 160, 220, 6, 6, 5, i++));

		// id 842 — from content/npcs/goblin_shaman.yaml
		sprites = new int[]{142, 140, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Goblin Shaman", "A taller, dark-robed goblin with rune-scratched bones around its neck.", "", "Pickpocket", 30, 25, 35, 25, false, sprites, 0x000000, 0x000000, 0x000000, 0x000000, 245, 230, 9, 8, 5, i++));

		// id 843 — from content/npcs/old_aric.yaml
		sprites = new int[]{6, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Old Aric", "A weathered elder, leaning on a staff. His eyes carry the look of someone who has walked further than most.", "", "Examine", 1, 1, 10, 1, false, sprites, 0xFFFFFF, 0xE8E0D0, 0xA9A29A, 0xE6C8A0, 160, 220, 6, 6, 5, i++));

		// id 844 — from content/npcs/crypt_spider_matron.yaml
		sprites = new int[]{166, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		npcs.add(new NPCDef("Crypt Spider Matron", "A massive, venom-soaked spider with eight burning eyes. The crypt's true keeper.", "", 130, 120, 200, 110, true, sprites, 0x000000, 0x000000, 0x000000, 0x000000, 320, 280, 6, 6, 5, i++));

		return i;
	}
}

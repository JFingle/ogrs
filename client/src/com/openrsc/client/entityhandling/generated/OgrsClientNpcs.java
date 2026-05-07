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

		return i;
	}
}

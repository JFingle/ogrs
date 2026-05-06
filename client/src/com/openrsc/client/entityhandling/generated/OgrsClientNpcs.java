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

		return i;
	}
}

// === GENERATED FILE — DO NOT EDIT BY HAND ===
// Source: content/items/*.yaml
// Regenerate: python3 tools/codegen-client-items.py

package com.openrsc.client.entityhandling.generated;

import com.openrsc.client.entityhandling.defs.ItemDef;
import java.util.ArrayList;

public final class OgrsClientItems {

	private OgrsClientItems() { /* no instances */ }

	/**
	 * Append every OGRS YAML-defined item to the client's ItemDef list.
	 * Returns the next free id. Caller threads `i` through:
	 *   <pre>i = OgrsClientItems.register(items, i);</pre>
	 * The 14-arg ItemDef constructor signature is:
	 *   (name, description, command, basePrice, spriteID, spriteLocation,
	 *    stackable, wieldable, wearableID, pictureMask, membersItem,
	 *    untradeable, noteable, id)
	 */
	public static int register(final ArrayList<ItemDef> items, int i) {

		// id 1593 — from content/items/rake.yaml
		items.add(new ItemDef("Rake", "A wooden-handled iron rake. Pulls weeds and breaks fresh soil.", "", 12, 96, "items:96", false, false, 0, 0xC4895E, false, false, true, i++));

		// id 1594 — from content/items/potato_seed.yaml
		items.add(new ItemDef("Potato Seed", "A handful of pale potato seeds. Sow into raked soil.", "", 3, 270, "items:270", true, false, 0, 0xCD853F, false, false, false, i++));

		// id 1595 — from content/items/compost.yaml
		items.add(new ItemDef("Compost", "A handful of dark, well-rotted compost. Smells of the earth.", "", 8, 23, "items:23", false, false, 0, 0x4A2E18, false, false, true, i++));

		// id 1596 — from content/items/onion_seed.yaml
		items.add(new ItemDef("Onion Seed", "A handful of small, papery onion seeds. Sow into raked soil.", "", 4, 276, "items:276", true, false, 0, 0xE6BE8A, false, false, false, i++));

		// id 1597 — from content/items/tomato_seed.yaml
		items.add(new ItemDef("Tomato Seed", "A pinch of tomato seeds. Plant in raked soil and water often.", "", 6, 276, "items:276", true, false, 0, 0xCC3300, false, false, false, i++));

		return i;
	}
}

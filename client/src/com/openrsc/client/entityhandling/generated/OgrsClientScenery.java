// === GENERATED FILE — DO NOT EDIT BY HAND ===
// Source: content/scenery/*.yaml
// Regenerate: python3 tools/codegen-client-scenery.py

package com.openrsc.client.entityhandling.generated;

import com.openrsc.client.entityhandling.defs.GameObjectDef;
import java.util.ArrayList;

public final class OgrsClientScenery {

	private OgrsClientScenery() { /* no instances */ }

	/**
	 * Append every OGRS YAML-defined scenery def to the client's
	 * GameObjectDef list, keeping id == list-index alignment with the
	 * server-side append order. Returns the next free id. Caller threads
	 * `i` through:
	 *   <pre>i = OgrsClientScenery.register(objects, i);</pre>
	 */
	public static int register(final ArrayList<GameObjectDef> objects, int i) {

		// id 1296 — from content/scenery/allotment_patch.yaml
		objects.add(new GameObjectDef("Allotment Patch", "A patch of cleared earth, weeds creeping at the edges. It wants seeds.", "Rake", "Examine", 1, 1, 1, 0, "wheat", ++i));

		return i;
	}
}

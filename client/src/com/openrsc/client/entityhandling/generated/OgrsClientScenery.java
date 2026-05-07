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
		objects.add(new GameObjectDef("Weedy Allotment", "An overgrown row, choked with weeds and stray grass. Time to break it.", "Rake", "Examine", 0, 1, 1, 0, "smallfern", ++i));

		// id 1297 — from content/scenery/compost_heap.yaml
		objects.add(new GameObjectDef("Compost Heap", "A heap of well-rotted plant matter, ready to feed a garden.", "Take", "Examine", 1, 1, 1, 0, "compostbin", ++i));

		// id 1298 — from content/scenery/garden_fence.yaml
		objects.add(new GameObjectDef("Fence", "A rustic wooden fence keeping rabbits out of the rows.", "WalkTo", "Examine", 1, 1, 1, 0, "gnomefence", ++i));

		// id 1299 — from content/scenery/allotment_growing.yaml
		objects.add(new GameObjectDef("Allotment", "Potato seedlings just breaking the soil. Patience, friend.", "Inspect", "Examine", 0, 1, 1, 0, "dugupsoil1", ++i));

		// id 1300 — from content/scenery/allotment_ready.yaml
		objects.add(new GameObjectDef("Allotment", "A row of mature potato plants, leaves wide and waxy. They want pulling.", "Harvest", "Examine", 0, 1, 1, 0, "potatoplant", ++i));

		// id 1301 — from content/scenery/allotment_empty_bed.yaml
		objects.add(new GameObjectDef("Allotment Bed", "Bare earth, freshly turned. It's ready for a seed.", "", "Inspect", 0, 1, 1, 0, "mudpatch", ++i));

		// id 1302 — from content/scenery/allotment_growing_onion.yaml
		objects.add(new GameObjectDef("Allotment", "Onion seedlings just breaking the soil. Small, pungent green tips.", "Inspect", "Examine", 0, 1, 1, 0, "dugupsoil2", ++i));

		// id 1303 — from content/scenery/allotment_ready_onion.yaml
		objects.add(new GameObjectDef("Allotment", "A row of mature onion plants, leaves drooping with weight. They want pulling.", "Harvest", "Examine", 0, 1, 1, 0, "onionplant", ++i));

		// id 1304 — from content/scenery/allotment_growing_tomato.yaml
		objects.add(new GameObjectDef("Allotment", "Tomato seedlings reaching for the sun. Tiny green nubs on slim stems.", "Inspect", "Examine", 0, 1, 1, 0, "dugupsoil3", ++i));

		// id 1305 — from content/scenery/allotment_ready_tomato.yaml
		objects.add(new GameObjectDef("Allotment", "Plump red tomatoes hanging heavy on the vines. Ready to pick.", "Harvest", "Examine", 0, 1, 1, 0, "tomatoplant", ++i));

		return i;
	}
}

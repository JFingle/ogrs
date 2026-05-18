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
		objects.add(new GameObjectDef("Allotment Bed", "Bare earth, freshly turned. It's ready for a seed.", "", "Inspect", 0, 1, 1, 0, "dugupsoil1", ++i));

		// id 1302 — from content/scenery/allotment_growing_onion.yaml
		objects.add(new GameObjectDef("Allotment", "Onion seedlings just breaking the soil. Small, pungent green tips.", "Inspect", "Examine", 0, 1, 1, 0, "dugupsoil2", ++i));

		// id 1303 — from content/scenery/allotment_ready_onion.yaml
		objects.add(new GameObjectDef("Allotment", "A row of mature onion plants, leaves drooping with weight. They want pulling.", "Harvest", "Examine", 0, 1, 1, 0, "onionplant", ++i));

		// id 1304 — from content/scenery/allotment_growing_tomato.yaml
		objects.add(new GameObjectDef("Allotment", "Tomato seedlings reaching for the sun. Tiny green nubs on slim stems.", "Inspect", "Examine", 0, 1, 1, 0, "dugupsoil3", ++i));

		// id 1305 — from content/scenery/allotment_ready_tomato.yaml
		objects.add(new GameObjectDef("Allotment", "Plump red tomatoes hanging heavy on the vines. Ready to pick.", "Harvest", "Examine", 0, 1, 1, 0, "tomatoplant", ++i));

		// id 1306 — from content/scenery/allotment_composted_bed.yaml
		objects.add(new GameObjectDef("Composted Bed", "A bed dressed with dark compost. Crops will swell on this earth.", "", "Inspect", 0, 1, 1, 0, "dugupsoil2", ++i));

		// id 1307 — from content/scenery/goblin_firepit.yaml
		objects.add(new GameObjectDef("Firepit", "A roaring goblin firepit. Greasy bones half-buried in the ash.", "WalkTo", "Examine", 0, 1, 1, 0, "firea1", ++i));

		// id 1308 — from content/scenery/goblin_cauldron.yaml
		objects.add(new GameObjectDef("Goblin Cauldron", "A rusted iron cauldron, contents bubbling. Smells of bone broth.", "WalkTo", "Examine", 1, 1, 1, 0, "cauldron", ++i));

		// id 1309 — from content/scenery/goblin_totem.yaml
		objects.add(new GameObjectDef("Goblin Totem", "A crooked wooden totem, hung with goblin trinkets and old bones.", "WalkTo", "Examine", 1, 1, 1, 0, "totemtreeevil", ++i));

		// id 1310 — from content/scenery/goblin_crate.yaml
		objects.add(new GameObjectDef("Goblin Crate", "A battered wooden crate, smelling of damp grain and worse.", "WalkTo", "Search", 1, 1, 1, 0, "crate", ++i));

		// id 1311 — from content/scenery/goblin_iron_vein.yaml
		objects.add(new GameObjectDef("Goblin Iron Vein", "A vein of iron ore in dark rock, half-worked by clumsy goblin tools.", "Mine", "Prospect", 1, 1, 1, 0, "rocks2", ++i));

		// id 1312 — from content/scenery/goblin_vein_depleted.yaml
		objects.add(new GameObjectDef("Depleted Vein", "A spent rock outcrop. Give it a few moments — the iron will catch up.", "WalkTo", "Examine", 1, 1, 1, 0, "rocks1", ++i));

		// id 1313 — from content/scenery/cooking_fire.yaml
		objects.add(new GameObjectDef("Cooking Fire", "A small steady cookfire. Good for crisping a potato or charring a tomato.", "WalkTo", "Examine", 0, 1, 1, 0, "firea1", ++i));

		// id 1314 — from content/scenery/draynor_bank_stool.yaml
		objects.add(new GameObjectDef("Banker's Stool", "A simple wooden stool, well-worn from long shifts behind the counter.", "WalkTo", "Examine", 0, 1, 1, 0, "stool", ++i));

		// id 1315 — from content/scenery/draynor_bank_coin_sacks.yaml
		objects.add(new GameObjectDef("Coin Sacks", "Heavy linen sacks, drawstrings cinched tight. Customer deposits, waiting to be filed.", "WalkTo", "Examine", 0, 1, 1, 0, "sacks", ++i));

		// id 1316 — from content/scenery/draynor_bank_ledger_shelf.yaml
		objects.add(new GameObjectDef("Ledger Shelf", "Row after row of leather-bound ledgers, each one a record of someone's small fortune.", "WalkTo", "Examine", 0, 1, 1, 0, "bookcase", ++i));

		// id 1317 — from content/scenery/draynor_bank_wall_torch.yaml
		objects.add(new GameObjectDef("Wall Torch", "A pitch-soaked torch in an iron sconce, guttering low. Smells faintly of resin.", "WalkTo", "Examine", 0, 1, 1, 0, "torcha1", ++i));

		// id 1318 — from content/scenery/draynor_bank_notice.yaml
		objects.add(new GameObjectDef("Bank Notice", "Painted in neat script: \"Bank of Gielinor — Draynor Branch. Open dawn to dusk. No fish on the counter.\"", "Read", "Examine", 0, 1, 1, 0, "signpost", ++i));

		return i;
	}
}

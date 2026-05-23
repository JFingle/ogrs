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

		// id 1598 — from content/items/seed_pouch.yaml
		items.add(new ItemDef("Seed Pouch", "Old Wat's missing leather pouch. Smells faintly of soil and seed.", "", 1, 25, "items:25", false, false, 0, 0x9C7A4A, false, true, false, i++));

		// id 1599 — from content/items/goblin_trinket.yaml
		items.add(new ItemDef("Goblin Trinket", "A crude bone trinket on twine. Smells faintly of stew.", "", 5, 24, "items:24", false, false, 0, 0xA08060, false, false, true, i++));

		// id 1600 — from content/items/cracked_shaman_staff.yaml
		items.add(new ItemDef("Cracked Shaman Staff", "A goblin shaman's staff. The bone tip thrums when held — a small reservoir of channeled life.", "Channel", 1, 91, "items:91", false, false, 0, 0x6B8E5E, false, true, false, i++));

		// id 1601 — from content/items/baked_potato.yaml
		items.add(new ItemDef("Baked Potato", "A potato baked golden in the embers. Smells of earth and salt.", "Eat", 8, 60, "items:60", false, false, 0, 0xC68642, false, false, true, i++));

		// id 1602 — from content/items/roasted_onion.yaml
		items.add(new ItemDef("Roasted Onion", "A whole onion roasted soft and sweet. Skin papery, heart yielding.", "Eat", 6, 18, "items:18", false, false, 0, 0xC07028, false, false, true, i++));

		// id 1603 — from content/items/charred_tomato.yaml
		items.add(new ItemDef("Charred Tomato", "A blistered, smoky tomato fresh off the embers. Hot, sweet, and tart.", "Eat", 12, 60, "items:60", false, false, 0, 0x8B0000, false, false, true, i++));

		// id 1604 — from content/items/burnt_crop.yaml
		items.add(new ItemDef("Burnt Crop", "An unrecognisable lump of charcoal that used to be food.", "", 1, 64, "items:64", false, false, 0, 0x2A1A0E, false, true, false, i++));

		// id 1605 — from content/items/spider_leg.yaml
		items.add(new ItemDef("Spider Leg", "A bristly leg, snapped clean at the joint. Some folk roast them. Most don't.", "Eat", 3, 133, "items:133", false, false, 0, 0x2A1810, false, false, true, i++));

		// id 1606 — from content/items/spider_egg.yaml
		items.add(new ItemDef("Spider Egg", "A leathery, waxen orb the size of a marble. Something inside twitches.", "Examine", 35, 19, "items:19", false, false, 0, 0x3A2E20, false, false, true, i++));

		// id 1607 — from content/items/iron_dagger_spiderbane.yaml
		items.add(new ItemDef("Iron dagger of spiderbane", "Iron blade etched with eight-legged runes. Aches to taste arachnid.", "", 280, 28, "items:28", false, true, 49, 0x2A4A2A, false, false, true, i++));

		// id 1608 — from content/items/cryptkeepers_skull.yaml
		items.add(new ItemDef("Cryptkeeper's Skull", "A pitted skull, still humming faintly with cold magic. Proof you bested the Crypt Lord.", "", 0, 173, "items:173", false, false, 0, 0x2B2B2B, false, true, false, i++));

		// id 1609 — from content/items/crypt_spider_key.yaml
		items.add(new ItemDef("Crypt Spider Key", "A heavy iron key, etched with eight-legged sigils. Will crumble on use.", "", 0, 79, "items:79", false, false, 0, 0x4A3A1A, false, true, false, i++));

		// id 1610 — from content/items/slayer_enchanted_gem.yaml
		items.add(new ItemDef("Slayer Enchanted Gem", "A small faceted gem, humming faintly. Rub it to hear your slayer master's voice.", "Rub", 0, 160, "items:160", false, false, 0, 0x4A1A6E, false, true, false, i++));

		return i;
	}
}

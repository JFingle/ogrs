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
		items.add(new ItemDef("Slayer Enchanted Gem", "A small faceted gem, humming faintly. Rub it to hear your slayer master's voice.", "Rub", 500, 160, "items:160", false, false, 0, 0x4A1A6E, false, true, false, i++));

		// id 1611 — from content/items/poison_drip.yaml
		items.add(new ItemDef("Poison Drip", "A glob of sticky, glistening venom. Looks lethal.", "", 25, 177, "items:177", true, false, 0, 0x000000, false, false, true, i++));

		// id 1612 — from content/items/spider_egg_sac.yaml
		items.add(new ItemDef("Spider Egg Sac", "A leathery sac swollen with dozens of unhatched spiderlings. Don't squeeze.", "", 100, 219, "items:219", false, false, 0, 0x3A1A4A, false, false, true, i++));

		// id 1613 — from content/items/antidote_vial.yaml
		items.add(new ItemDef("Antidote Vial", "A small glass vial of bright green liquid. The label reads \"DRINK\".", "Drink", 80, 478, "items:478", false, false, 0, 0x4AB82E, false, false, true, i++));

		// id 1614 — from content/items/web_projectile.yaml
		items.add(new ItemDef("Web Projectile", "A wad of sticky spider-web. Heavy. Feels like it wants to be thrown.", "", 35, 200, "items:200", true, false, 0, 0xCCCCDD, false, false, true, i++));

		// id 1615 — from content/items/prayer_bones.yaml
		items.add(new ItemDef("Bones", "The remains of a fallen creature. Worth burying.", "Bury", 1, 20, "items:20", false, false, 0, 0x000000, false, false, true, i++));

		// id 1616 — from content/items/prayer_big_bones.yaml
		items.add(new ItemDef("Big bones", "Larger bones from a larger beast. More prayer worth.", "Bury", 5, 413, "items:413", false, false, 0, 0x000000, false, false, true, i++));

		// id 1617 — from content/items/prayer_babydragon_bones.yaml
		items.add(new ItemDef("Baby dragon bones", "Small but still potent. The bones of a dragon hatchling.", "Bury", 20, 814, "items:814", false, false, 0, 0xC0E0C0, false, false, true, i++));

		// id 1618 — from content/items/prayer_dragon_bones.yaml
		items.add(new ItemDef("Dragon bones", "Bones from a fully-grown dragon. Heavy with residual power.", "Bury", 80, 814, "items:814", false, false, 0, 0x000000, false, false, true, i++));

		// id 1619 — from content/items/prayer_wolf_bones.yaml
		items.add(new ItemDef("Wolf bones", "The bones of a wild wolf. Bury for a small prayer offering.", "Bury", 2, 20, "items:20", false, false, 0, 0x9E8B7A, false, false, true, i++));

		// id 1620 — from content/items/prayer_burnt_bones.yaml
		items.add(new ItemDef("Burnt bones", "Charred bones, useless for prayer but still grant a sliver of XP.", "Bury", 0, 20, "items:20", false, false, 0, 0x222222, false, false, true, i++));

		// id 1621 — from content/items/prayer_prayer_ashes.yaml
		items.add(new ItemDef("Ashes", "A handful of grey ashes. Scatter in a holy place for a small blessing.", "Scatter", 1, 181, "items:181", false, false, 0, 0x000000, false, false, true, i++));

		// id 1622 — from content/items/prayer_demonic_ashes.yaml
		items.add(new ItemDef("Demonic ashes", "Black ashes that smoulder faintly. The remains of something unholy.", "Scatter", 50, 1002, "items:1002", false, false, 0, 0x000000, false, false, true, i++));

		// id 1623 — from content/items/prayer_holy_symbol_yahwist.yaml
		items.add(new ItemDef("Holy symbol", "A simple iron cross on a thong. Wear it to ward off evil.", "", 25, 44, "items:44", false, false, 0, 0x000000, false, false, true, i++));

		// id 1624 — from content/items/prayer_holy_water_vial.yaml
		items.add(new ItemDef("Holy water vial", "A vial of consecrated water. Throw at undead for heavy damage.", "", 35, 1239, "items:1239", true, false, 0, 0x000000, false, false, true, i++));

		// id 1625 — from content/items/prayer_communion_cup.yaml
		items.add(new ItemDef("Communion cup", "A silver cup used in sacred rites. Hold during prayer for a bonus.", "Use", 75, 1195, "items:1195", false, false, 0, 0xE6CC55, false, false, true, i++));

		// id 1626 — from content/items/prayer_incense_stick.yaml
		items.add(new ItemDef("Incense stick", "A slender stick that smokes a sweet, calming fragrance when lit.", "Light", 8, 381, "items:381", true, false, 0, 0x7C4F2A, false, false, true, i++));

		// id 1627 — from content/items/prayer_censer_unlit.yaml
		items.add(new ItemDef("Censer (unlit)", "A hanging brass censer. Light incense in it for sustained Prayer XP.", "", 40, 585, "items:585", false, false, 0, 0x7A6F4A, false, false, true, i++));

		// id 1628 — from content/items/prayer_censer_lit.yaml
		items.add(new ItemDef("Censer (lit)", "A lit censer, smoking with holy incense. Slowly grants Prayer XP.", "", 40, 585, "items:585", false, false, 0, 0xD4A64A, false, false, true, i++));

		// id 1629 — from content/items/prayer_blessed_candle.yaml
		items.add(new ItemDef("Blessed candle", "A pure white candle. Burns with a gentle, holy light.", "Light", 15, 599, "items:599", false, false, 0, 0xF5E8C8, false, false, true, i++));

		// id 1630 — from content/items/prayer_cherubim_seal.yaml
		items.add(new ItemDef("Cherubim seal", "A small gold medallion stamped with winged figures. Boon to the faithful.", "", 200, 385, "items:385", false, false, 0, 0xE0C040, false, true, true, i++));

		// id 1631 — from content/items/prayer_mitre.yaml
		items.add(new ItemDef("Mitre", "A tall ceremonial bishop's hat. Worn by senior clerics.", "", 150, 807, "items:807", false, false, 0, 0xF8F0D8, false, false, true, i++));

		// id 1632 — from content/items/prayer_priest_robe_top.yaml
		items.add(new ItemDef("Priest robe (top)", "Cream-coloured cleric's robe. Modest, unadorned.", "", 80, 807, "items:807", false, false, 0, 0xEDE2C8, false, false, true, i++));

		// id 1633 — from content/items/prayer_priest_robe_bottom.yaml
		items.add(new ItemDef("Priest robe (bottom)", "Cream-coloured cleric's gown. Falls to the ankles.", "", 80, 808, "items:808", false, false, 0, 0xEDE2C8, false, false, true, i++));

		// id 1634 — from content/items/prayer_stole.yaml
		items.add(new ItemDef("Stole", "A long white sash worn around the neck of a priest. Sign of office.", "", 60, 183, "items:183", false, false, 0, 0xFFFFFF, false, false, true, i++));

		// id 1635 — from content/items/prayer_yahwist_scripture.yaml
		items.add(new ItemDef("Yahwist scripture", "A weathered scroll inked with old promises. Reading it heals the spirit.", "Read", 250, 1238, "items:1238", false, false, 0, 0x9E7B4A, false, false, true, i++));

		// id 1636 — from content/items/prayer_sealed_scroll.yaml
		items.add(new ItemDef("Sealed scroll", "A scroll bound with wax. The seal is unbroken — what's inside?", "Open", 20, 1173, "items:1173", false, false, 0, 0xCC6644, false, false, true, i++));

		// id 1637 — from content/items/prayer_open_prayer_scroll.yaml
		items.add(new ItemDef("Open prayer scroll", "A scroll of prayer verses. Recite during prayer for a small bonus.", "Recite", 30, 752, "items:752", false, false, 0, 0xE8D8B0, false, false, true, i++));

		// id 1638 — from content/items/prayer_anointing_horn.yaml
		items.add(new ItemDef("Anointing horn", "A small ram's horn filled with sacred oil. Anoint others for a blessing.", "Anoint", 120, 466, "items:466", false, false, 0, 0x9E6F2A, false, false, true, i++));

		// id 1639 — from content/items/prayer_anointing_oil_flask.yaml
		items.add(new ItemDef("Anointing oil flask", "A small clay flask of pressed olive oil, consecrated for sacred use.", "Anoint", 45, 464, "items:464", true, false, 0, 0xE0B040, false, false, true, i++));

		// id 1640 — from content/items/prayer_bread_of_presence.yaml
		items.add(new ItemDef("Bread of presence", "Twelve loaves arranged on the altar. Symbol of provision and covenant.", "", 50, 138, "items:138", false, false, 0, 0xE6CC55, false, false, true, i++));

		// id 1641 — from content/items/prayer_unleavened_bread.yaml
		items.add(new ItemDef("Unleavened bread", "Flat, hastily-baked bread. Eaten in haste during sacred remembrances.", "Eat", 12, 138, "items:138", false, false, 0, 0xC8A878, false, false, true, i++));

		// id 1642 — from content/items/magic_spellbook_standard.yaml
		items.add(new ItemDef("Standard spellbook", "The classic Yahwist & Saradomin combined spellbook. Most spells.", "Read", 50, 30, "items:30", false, false, 0, 0x000000, false, false, true, i++));

		// id 1643 — from content/items/magic_spellbook_ancient.yaml
		items.add(new ItemDef("Ancient spellbook", "A forbidden book of dark eastern magic. Hits multiple targets.", "Read", 250, 768, "items:768", false, false, 0, 0x3A1A4A, true, false, true, i++));

		// id 1644 — from content/items/magic_spellbook_yahwist.yaml
		items.add(new ItemDef("Yahwist scripture book", "A bound collection of Yahwist prayer-spells. Healing focus.", "Read", 500, 1238, "items:1238", false, false, 0, 0xE0C040, true, false, true, i++));

		// id 1645 — from content/items/magic_wizard_hat.yaml
		items.add(new ItemDef("Wizard hat", "A pointed blue wizard's hat. Helps with magic.", "", 30, 185, "items:185", false, false, 0, 0x000000, false, false, true, i++));

		// id 1646 — from content/items/magic_wizard_top.yaml
		items.add(new ItemDef("Wizard top", "A long blue wizard's robe. Adorned with stars.", "", 40, 184, "items:184", false, false, 0, 0x000000, false, false, true, i++));

		// id 1647 — from content/items/magic_wizard_bottom.yaml
		items.add(new ItemDef("Wizard bottom", "Loose blue wizard's leggings.", "", 35, 1234, "items:1234", false, false, 0, 0x4A4ABF, false, false, true, i++));

		// id 1648 — from content/items/magic_mystic_blue_hat.yaml
		items.add(new ItemDef("Mystic blue hat", "A finer wizard's hat in deep mystic blue. Boosts spell accuracy.", "", 250, 1264, "items:1264", false, false, 0, 0x000000, false, false, true, i++));

		// id 1649 — from content/items/magic_mystic_blue_top.yaml
		items.add(new ItemDef("Mystic blue top", "Deep mystic blue wizard's robe. Boosts spell accuracy.", "", 350, 184, "items:184", false, false, 0, 0x1A2A8E, false, false, true, i++));

		// id 1650 — from content/items/magic_mystic_blue_bottom.yaml
		items.add(new ItemDef("Mystic blue bottom", "Deep mystic blue wizard's leggings. Boosts spell accuracy.", "", 300, 1234, "items:1234", false, false, 0, 0x1A2A8E, false, false, true, i++));

		// id 1651 — from content/items/magic_mystic_dark_hat.yaml
		items.add(new ItemDef("Mystic dark hat", "A near-black mystic hat. Worn by darker mages.", "", 350, 199, "items:199", false, false, 0, 0x222244, false, false, true, i++));

		// id 1652 — from content/items/magic_mystic_dark_top.yaml
		items.add(new ItemDef("Mystic dark top", "A near-black mystic robe. Worn by darker mages.", "", 450, 184, "items:184", false, false, 0, 0x222244, false, false, true, i++));

		// id 1653 — from content/items/magic_mystic_dark_bottom.yaml
		items.add(new ItemDef("Mystic dark bottom", "Near-black mystic leggings.", "", 400, 1234, "items:1234", false, false, 0, 0x222244, false, false, true, i++));

		// id 1654 — from content/items/magic_infinity_hat.yaml
		items.add(new ItemDef("Infinity hat", "Hat of pure magical essence. Worn by master mages.", "", 1500, 185, "items:185", false, false, 0, 0xDA9100, true, false, true, i++));

		// id 1655 — from content/items/magic_infinity_top.yaml
		items.add(new ItemDef("Infinity top", "Robe of pure magical essence. Worn by master mages.", "", 2000, 184, "items:184", false, false, 0, 0xDA9100, true, false, true, i++));

		// id 1656 — from content/items/magic_infinity_bottom.yaml
		items.add(new ItemDef("Infinity bottom", "Leggings of pure magical essence.", "", 1800, 1234, "items:1234", false, false, 0, 0xDA9100, true, false, true, i++));

		// id 1657 — from content/items/magic_staff_basic.yaml
		items.add(new ItemDef("Staff", "A simple wooden staff. Modest magic boost.", "", 20, 100, "items:100", false, true, 35, 0x000000, false, false, true, i++));

		// id 1658 — from content/items/magic_staff_magic.yaml
		items.add(new ItemDef("Magic staff", "A purified wooden staff. Notable magic boost.", "", 200, 198, "items:198", false, true, 35, 0x000000, false, false, true, i++));

		// id 1659 — from content/items/magic_battlestaff.yaml
		items.add(new ItemDef("Battlestaff", "A combat-grade staff that doubles as a melee weapon.", "", 400, 614, "items:614", false, true, 35, 0x000000, false, false, true, i++));

		// id 1660 — from content/items/magic_staff_of_air.yaml
		items.add(new ItemDef("Staff of air", "A wizard's staff that supplies unlimited air runes.", "", 250, 101, "items:101", false, true, 35, 0x000000, false, false, true, i++));

		// id 1661 — from content/items/magic_staff_of_water.yaml
		items.add(new ItemDef("Staff of water", "A wizard's staff that supplies unlimited water runes.", "", 250, 102, "items:102", false, true, 35, 0x000000, false, false, true, i++));

		// id 1662 — from content/items/magic_staff_of_earth.yaml
		items.add(new ItemDef("Staff of earth", "A wizard's staff that supplies unlimited earth runes.", "", 250, 103, "items:103", false, true, 35, 0x000000, false, false, true, i++));

		// id 1663 — from content/items/magic_staff_of_fire.yaml
		items.add(new ItemDef("Staff of fire", "A wizard's staff that supplies unlimited fire runes.", "", 250, 197, "items:197", false, true, 35, 0x000000, false, false, true, i++));

		// id 1664 — from content/items/magic_cape_magic_skill.yaml
		items.add(new ItemDef("Magic skill cape", "A cape worn by those who have mastered Magic to level 99.", "", 99000, 512, "items:512", false, false, 0, 0x1A2A8E, true, false, true, i++));

		// id 1665 — from content/items/magic_cape_magic_master.yaml
		items.add(new ItemDef("Magic master cape", "A cape worn only by 200M XP Magic masters. Trim shimmers.", "", 250000, 512, "items:512", false, false, 0, 0xDA9100, true, false, true, i++));

		// id 1666 — from content/items/magic_cape_runecraft_skill.yaml
		items.add(new ItemDef("Runecraft skill cape", "A cape worn by those who have mastered Runecraft to level 99.", "", 99000, 513, "items:513", false, false, 0, 0x4A8A1A, true, false, true, i++));

		// id 1667 — from content/items/magic_pouch_small.yaml
		items.add(new ItemDef("Small rune pouch", "Holds up to 5 of any one rune type. Doesn't take a bank slot.", "", 100, 1117, "items:1117", false, false, 0, 0x9E7B4A, true, true, true, i++));

		// id 1668 — from content/items/magic_pouch_medium.yaml
		items.add(new ItemDef("Medium rune pouch", "Holds up to 12 of any one rune type.", "", 250, 1117, "items:1117", false, false, 0, 0x4A8A1A, true, true, true, i++));

		// id 1669 — from content/items/magic_pouch_large.yaml
		items.add(new ItemDef("Large rune pouch", "Holds up to 25 of any one rune type.", "", 500, 1117, "items:1117", false, false, 0, 0x1A2A8E, true, true, true, i++));

		// id 1670 — from content/items/magic_essence_rock.yaml
		items.add(new ItemDef("Rune essence rock", "A glowing rock holding raw runic energy. Mine with a chisel.", "", 0, 986, "items:986", false, false, 0, 0xC0C0E0, false, false, false, i++));

		// id 1671 — from content/items/magic_essence_mined.yaml
		items.add(new ItemDef("Rune essence", "A small chunk of raw runic energy. Craft into runes at an altar.", "", 3, 150, "items:150", true, false, 0, 0xE0E0FF, false, false, true, i++));

		// id 1672 — from content/items/magic_pure_essence.yaml
		items.add(new ItemDef("Pure essence", "A purer form of rune essence. Craftable into all rune types.", "", 8, 150, "items:150", true, false, 0, 0xFFFFFF, true, false, true, i++));

		// id 1673 — from content/items/thief_lockpick.yaml
		items.add(new ItemDef("Lockpick", "A bent steel pin. Used to open locked chests and doors.", "", 20, 714, "items:714", false, false, 0, 0x000000, false, false, true, i++));

		// id 1674 — from content/items/thief_lockpick_master.yaml
		items.add(new ItemDef("Master lockpick", "A finely-tuned silver lockpick. Higher success on harder locks.", "", 200, 714, "items:714", false, false, 0, 0xC8C8D8, true, false, true, i++));

		// id 1675 — from content/items/thief_safecracking_tools.yaml
		items.add(new ItemDef("Safecracking tools", "A roll of slim files and turning tools. For the truly committed thief.", "", 500, 714, "items:714", false, false, 0, 0x4A4A5A, true, false, true, i++));

		// id 1676 — from content/items/thief_disguise_kit.yaml
		items.add(new ItemDef("Disguise kit", "Wig, glasses, fake mustache. Vanishes guard suspicion temporarily.", "Use", 350, 381, "items:381", false, false, 0, 0x8A6B4A, true, false, true, i++));

		// id 1677 — from content/items/thief_bag_of_holding.yaml
		items.add(new ItemDef("Bag of holding", "A leather bag that holds far more than it should. Magical.", "Open", 1500, 1263, "items:1263", false, false, 0, 0x7A5A2E, true, true, true, i++));

		// id 1678 — from content/items/thief_money_purse.yaml
		items.add(new ItemDef("Money purse", "A leather purse — looks heavy.", "Open", 50, 824, "items:824", false, false, 0, 0x000000, false, false, true, i++));

		// id 1679 — from content/items/thief_silver_coin_pouch.yaml
		items.add(new ItemDef("Silver coin pouch", "A small velvet pouch containing silver coinage.", "Open", 100, 824, "items:824", false, false, 0, 0xB8B8C8, false, false, true, i++));

		// id 1680 — from content/items/thief_mystery_box.yaml
		items.add(new ItemDef("Mystery box", "A sealed wooden box. Could be anything inside.", "Open", 250, 605, "items:605", false, false, 0, 0x6A4A2E, true, false, true, i++));

		// id 1681 — from content/items/thief_snuff_box.yaml
		items.add(new ItemDef("Snuff box", "An ornate enameled box. Worth a few coins on its own.", "Open", 150, 605, "items:605", false, false, 0, 0x3A2A1A, false, false, true, i++));

		// id 1682 — from content/items/thief_iron_key.yaml
		items.add(new ItemDef("Iron key", "A heavy iron key. Smells of rust.", "", 10, 47, "items:47", false, false, 0, 0x3A3A3A, false, false, true, i++));

		// id 1683 — from content/items/thief_brass_key.yaml
		items.add(new ItemDef("Brass key", "A brass key — small but well-made.", "", 15, 99, "items:99", false, false, 0, 0x000000, false, false, true, i++));

		// id 1684 — from content/items/thief_ornate_key.yaml
		items.add(new ItemDef("Ornate key", "A gilded key with elaborate teeth. Opens something important.", "", 100, 421, "items:421", false, false, 0, 0xE0C040, false, false, true, i++));

		// id 1685 — from content/items/thief_stolen_ring.yaml
		items.add(new ItemDef("Stolen ring", "A simple gold ring — clearly someone else's.", "", 35, 283, "items:283", false, false, 0, 0x000000, false, false, true, i++));

		// id 1686 — from content/items/thief_stolen_necklace.yaml
		items.add(new ItemDef("Stolen necklace", "A gold chain necklace lifted from a noble's neck.", "", 80, 288, "items:288", false, false, 0, 0x000000, false, false, true, i++));

		// id 1687 — from content/items/thief_signet_ring.yaml
		items.add(new ItemDef("Signet ring", "A heavy gold signet ring engraved with a sigil. Worth a fortune.", "", 300, 283, "items:283", false, false, 0, 0x1A2A8E, true, false, true, i++));

		// id 1688 — from content/items/thief_locket.yaml
		items.add(new ItemDef("Locket", "A small heart-shaped locket. Someone's tender keepsake.", "Open", 60, 288, "items:288", false, false, 0, 0xC8407A, false, false, true, i++));

		// id 1689 — from content/items/thief_brooch.yaml
		items.add(new ItemDef("Brooch", "A decorative golden brooch set with a small gem.", "", 120, 283, "items:283", false, false, 0, 0xCC4444, false, false, true, i++));

		// id 1690 — from content/items/thief_copper_pile.yaml
		items.add(new ItemDef("Copper pile", "A small stack of copper coins. Not worth much, but it's something.", "", 1, 10, "items:10", true, false, 0, 0xB87333, false, false, true, i++));

		// id 1691 — from content/items/thief_doubloons.yaml
		items.add(new ItemDef("Doubloons", "Heavy gold pirate coins, foreign make.", "", 10, 10, "items:10", true, false, 0, 0xE0C040, true, false, true, i++));

		// id 1692 — from content/items/thief_gold_nugget.yaml
		items.add(new ItemDef("Gold nugget", "A small chunk of raw gold. Smelt or sell.", "", 35, 1118, "items:1118", false, false, 0, 0x000000, false, false, true, i++));

		// id 1693 — from content/items/thief_cipher_scroll.yaml
		items.add(new ItemDef("Cipher scroll", "A scroll covered in seemingly-random symbols. Coded message.", "Read", 100, 49, "items:49", false, false, 0, 0x6A5A3A, true, false, true, i++));

		// id 1694 — from content/items/thief_map_fragment.yaml
		items.add(new ItemDef("Map fragment", "A torn corner of a map. Edges burnt. Half of a treasure clue.", "Read", 200, 49, "items:49", false, false, 0, 0xC8A878, true, false, true, i++));

		// id 1695 — from content/items/thief_wax_tablet.yaml
		items.add(new ItemDef("Wax tablet", "A wooden frame holding inscribed beeswax. A merchant's ledger entry.", "Read", 40, 1174, "items:1174", false, false, 0, 0xC8A040, false, false, true, i++));

		// id 1696 — from content/items/thief_pocket_watch.yaml
		items.add(new ItemDef("Pocket watch", "A silver pocket watch on a chain. Ticks softly.", "", 180, 1118, "items:1118", false, false, 0, 0xC0C0C8, true, false, true, i++));

		// id 1697 — from content/items/thief_wine_bottle.yaml
		items.add(new ItemDef("Wine bottle", "A dusty bottle of red wine. Vintage uncertain.", "Drink", 25, 142, "items:142", false, false, 0, 0x000000, false, false, true, i++));

		return i;
	}
}

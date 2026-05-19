package com.openrsc.server.util;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Spells;

/**
 * OGRS — projectile sprite type selector.
 *
 * The client renders incoming projectiles with sprite at index
 * {@code spriteProjectile (3160) + type}. SpriteDef entries are
 * registered in {@code EntityHandler.loadProjectiles()} in matching
 * order; the indices in this file MUST match what's registered there
 * and what {@code scripts/art/pack-router-sprites.py} writes into the
 * sprite archive.
 *
 * Slots 0-6: original router projectiles (HANDOFF.md §1A).
 * Slots 7-44: per-spell unique projectile art (§1C / §3B). Each
 * authored spell gets its own sprite so visuals don't collide on the
 * router (Wind/Sara no longer both ORB, Water/Fire no longer both
 * MAGIC, etc.).
 */
public final class OgrsProjectileTypes {

	public static final int ORB = 0;
	public static final int MAGIC = 1;
	public static final int RANGED = 2;
	public static final int GNOMEBALL = 3;
	public static final int SKULL = 4;
	public static final int SPIKEBALL = 5;
	public static final int BLANK = 6;

	// OGRS §3B — per-spell unique projectile types. Index order matches
	// pack-router-sprites.py UNIQUE_PROJ_FOLDERS list and the new
	// EntityHandler.loadProjectiles() entries.
	public static final int CONFUSE = 7;
	public static final int WEAKEN = 8;
	public static final int VULNERABILITY = 9;
	public static final int ENFEEBLE = 10;
	public static final int STUN = 11;
	public static final int CRUMBLE_UNDEAD = 12;
	public static final int FEAR = 13;
	public static final int CHILL_BOLT = 14;
	public static final int SHOCK_BOLT = 15;
	public static final int ELEMENTAL_BOLT = 16;
	public static final int IBAN_BLAST = 17;
	public static final int FIRE = 18;
	public static final int THICK_SKIN = 19;
	public static final int BURST_STRENGTH = 20;
	public static final int ROCK_SKIN = 21;
	public static final int CAMOUFLAGE = 22;
	public static final int LOW_ALCH = 23;
	public static final int HIGH_ALCH = 24;
	public static final int TELEGRAB = 25;
	public static final int BONES_BANANAS = 26;
	public static final int BONES_BREAD = 27;
	public static final int SUPERHEAT = 28;
	public static final int CHARGE = 29;
	public static final int CHARGE_AIR = 30;
	public static final int CHARGE_WATER = 31;
	public static final int CHARGE_EARTH = 32;
	public static final int CHARGE_FIRE = 33;
	public static final int TELE_VARROCK = 34;
	public static final int TELE_LUMBRIDGE = 35;
	public static final int TELE_FALADOR = 36;
	public static final int TELE_CAMELOT = 37;
	public static final int TELE_ARDOUGNE = 38;
	public static final int TELE_WATCHTOWER = 39;
	public static final int ENCHANT1 = 40;
	public static final int ENCHANT2 = 41;
	public static final int ENCHANT3 = 42;
	public static final int ENCHANT4 = 43;
	public static final int ENCHANT5 = 44;

	private OgrsProjectileTypes() { /* static */ }

	/**
	 * Pick a projectile sprite for an arrow/bolt/dart by ammo item id.
	 * Tier upgrade and poison variants are visually distinct so the
	 * player sees their gear progression in the air.
	 */
	public static int forArrow(final int ammoId) {
		// Poison variants always look death-themed regardless of tier.
		if (ammoId == ItemId.POISON_BRONZE_ARROWS.id()
			|| ammoId == ItemId.POISON_IRON_ARROWS.id()
			|| ammoId == ItemId.POISON_STEEL_ARROWS.id()
			|| ammoId == ItemId.POISON_MITHRIL_ARROWS.id()
			|| ammoId == ItemId.POISON_ADAMANTITE_ARROWS.id()
			|| ammoId == ItemId.POISON_RUNE_ARROWS.id()) {
			return SKULL;
		}
		// Tier upgrades — early tiers stay arrow-shaped, mid+ get visual flourishes.
		if (ammoId == ItemId.MITHRIL_ARROWS.id())     return ORB;       // shimmer
		if (ammoId == ItemId.ADAMANTITE_ARROWS.id())  return SPIKEBALL; // weight
		if (ammoId == ItemId.RUNE_ARROWS.id())        return SKULL;     // top-tier menace
		// Darts read tiny — go BLANK so they're a flicker rather than a drawn arrow.
		if (ammoId == ItemId.BRONZE_THROWING_DART.id()
			|| ammoId == ItemId.IRON_THROWING_DART.id()
			|| ammoId == ItemId.STEEL_THROWING_DART.id()
			|| ammoId == ItemId.MITHRIL_THROWING_DART.id()) {
			return BLANK;
		}
		// Default — arrow shape.
		return RANGED;
	}

	/**
	 * Spell display-name -> unique projectile type. Routes each authored
	 * spell to its own sprite slot; falls through to the router visuals
	 * for spells with no unique art (Wind family still uses ORB,
	 * Saradomin Strike still uses ORB, plain Water spells use MAGIC).
	 *
	 * Order is significant: most-specific match wins. We check unique
	 * spell names first, then element families.
	 */
	public static int forSpellName(final String spellName) {
		if (spellName == null) return MAGIC;
		final String n = spellName.toLowerCase();

		// --- Unique spell projectiles (§3B) ----------------------------
		if (n.contains("crumble"))        return CRUMBLE_UNDEAD;
		if (n.contains("fear"))           return FEAR;
		if (n.contains("vulnerability"))  return VULNERABILITY;
		if (n.contains("enfeeble"))       return ENFEEBLE;
		if (n.contains("stun"))           return STUN;
		if (n.contains("confuse"))        return CONFUSE;
		if (n.contains("weaken"))         return WEAKEN;
		if (n.contains("chill"))          return CHILL_BOLT;
		if (n.contains("shock"))          return SHOCK_BOLT;
		if (n.contains("iban"))           return IBAN_BLAST;
		if (n.contains("elemental"))      return ELEMENTAL_BOLT;
		if (n.contains("thick skin"))     return THICK_SKIN;
		if (n.contains("burst of strength")) return BURST_STRENGTH;
		if (n.contains("rock skin"))      return ROCK_SKIN;
		if (n.contains("camouflage"))     return CAMOUFLAGE;
		if (n.contains("low level alchemy") || n.contains("low alch")) return LOW_ALCH;
		if (n.contains("high level alchemy") || n.contains("high alch")) return HIGH_ALCH;
		if (n.contains("telekinetic grab") || n.contains("telegrab")) return TELEGRAB;
		if (n.contains("bones to banana")) return BONES_BANANAS;
		if (n.contains("bones to bread"))  return BONES_BREAD;
		if (n.contains("superheat"))       return SUPERHEAT;
		// Charge orbs first (they contain "charge") before generic Charge.
		if (n.contains("charge air"))      return CHARGE_AIR;
		if (n.contains("charge water"))    return CHARGE_WATER;
		if (n.contains("charge earth"))    return CHARGE_EARTH;
		if (n.contains("charge fire"))     return CHARGE_FIRE;
		if (n.contains("charge"))          return CHARGE;
		if (n.contains("varrock teleport"))   return TELE_VARROCK;
		if (n.contains("lumbridge teleport")) return TELE_LUMBRIDGE;
		if (n.contains("falador teleport"))   return TELE_FALADOR;
		if (n.contains("camelot teleport"))   return TELE_CAMELOT;
		if (n.contains("ardougne teleport"))  return TELE_ARDOUGNE;
		if (n.contains("watchtower teleport"))return TELE_WATCHTOWER;
		// Enchants — pick tier from name; "lvl 1" / "level-1" / "1" digits.
		if (n.contains("enchant")) {
			if (n.contains("5")) return ENCHANT5;
			if (n.contains("4")) return ENCHANT4;
			if (n.contains("3")) return ENCHANT3;
			if (n.contains("2")) return ENCHANT2;
			return ENCHANT1;
		}

		// --- Element families fall through to router or new FIRE -------
		if (n.contains("fire") || n.contains("flame")) return FIRE;
		if (n.contains("wind") || n.contains("air"))   return ORB;
		if (n.contains("earth") || n.contains("rock")) return SPIKEBALL;
		if (n.contains("water") || n.contains("ice"))  return MAGIC;
		if (n.contains("bolt"))                          return RANGED;
		if (n.contains("snare") || n.contains("bind")
			|| n.contains("entangle") || n.contains("hold")) return SPIKEBALL;
		return MAGIC;
	}

	/** God spell -> per-god visual. Three gods, three flavors. */
	public static int forGodSpell(final Spells spellEnum) {
		if (spellEnum == Spells.SARADOMIN_STRIKE)  return ORB;
		if (spellEnum == Spells.CLAWS_OF_GUTHIX)   return GNOMEBALL;
		if (spellEnum == Spells.FLAMES_OF_ZAMORAK) return SKULL;
		return MAGIC;
	}
}

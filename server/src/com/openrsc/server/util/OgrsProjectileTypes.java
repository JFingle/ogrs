package com.openrsc.server.util;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Spells;

/**
 * OGRS — projectile sprite type selector.
 *
 * The client renders incoming projectiles with sprite at index
 * {@code spriteProjectile (3160) + type}, where type is one of the
 * SpriteDef entries loaded by {@code EntityHandler.loadProjectiles()}:
 *
 *   0 ORB        — purple/violet magic orb
 *   1 MAGIC      — default magic projectile
 *   2 RANGED     — arrow
 *   3 GNOMEBALL  — green sphere (gnomeball quest item shape)
 *   4 SKULL      — death/cursed look
 *   5 SPIKEBALL  — heavy iron ball
 *   6 BLANK      — invisible/no-render
 *
 * Until the sprite-archive injection work lands (memory backlog: real
 * custom projectile sprites), we vary visuals across spell + ammo
 * tier by remapping fires through this resolver. Effect: different
 * arrows look different per tier; different spells look different per
 * element. No new client assets needed.
 *
 * Defaults: arrows → RANGED, spells → MAGIC, throwables → RANGED.
 */
public final class OgrsProjectileTypes {

	public static final int ORB = 0;
	public static final int MAGIC = 1;
	public static final int RANGED = 2;
	public static final int GNOMEBALL = 3;
	public static final int SKULL = 4;
	public static final int SPIKEBALL = 5;
	public static final int BLANK = 6;

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
	 * Substring-driven spell type picker. Uses the spell display name so
	 * Wind / Water / Earth / Fire variants are recognised across tiers
	 * (Strike / Bolt / Blast / Wave). Defaults to MAGIC.
	 */
	public static int forSpellName(final String spellName) {
		if (spellName == null) return MAGIC;
		final String n = spellName.toLowerCase();
		// Element families.
		if (n.contains("wind")  || n.contains("air"))   return ORB;
		if (n.contains("earth") || n.contains("rock"))  return SPIKEBALL;
		if (n.contains("water") || n.contains("ice"))   return MAGIC;
		if (n.contains("fire")  || n.contains("flame")) return MAGIC;
		// Mechanics families.
		if (n.contains("bolt"))                          return RANGED;
		if (n.contains("crumble"))                       return SKULL;
		if (n.contains("curse") || n.contains("weaken")) return SKULL;
		if (n.contains("alch")  || n.contains("telegrab")
			|| n.contains("heal")  || n.contains("plank"))  return GNOMEBALL;
		if (n.contains("snare") || n.contains("bind")
			|| n.contains("entangle") || n.contains("hold")) return SPIKEBALL;
		return MAGIC;
	}

	/** God spell -> per-god visual. Three gods, three flavors. */
	public static int forGodSpell(final Spells spellEnum) {
		if (spellEnum == Spells.SARADOMIN_STRIKE)  return ORB;       // light/holy
		if (spellEnum == Spells.CLAWS_OF_GUTHIX)   return GNOMEBALL; // nature/balance
		if (spellEnum == Spells.FLAMES_OF_ZAMORAK) return SKULL;     // chaos/death
		return MAGIC;
	}
}

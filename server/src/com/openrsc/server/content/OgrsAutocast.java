package com.openrsc.server.content;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.constants.SpellDamages;
import com.openrsc.server.constants.Spells;
import com.openrsc.server.event.rsc.impl.combat.CombatFormula;
import com.openrsc.server.event.rsc.impl.projectile.ProjectileEvent;
import com.openrsc.server.model.entity.EntityType;
import com.openrsc.server.external.Gauntlets;
import com.openrsc.server.external.SpellDef;
import com.openrsc.server.model.entity.KillType;
import com.openrsc.server.model.entity.Mob;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.net.rsc.handlers.SpellHandler;
import com.openrsc.server.util.OgrsProjectileTypes;

import java.util.Map;

/**
 * OGRS — Magic autocast helper.
 *
 * Combat behaviour: when CombatEvent runs and the hitter is a Player who
 * has selected an autocast spell + has an eligible staff equipped + meets
 * level and rune requirements, the player's normal melee swing for the
 * round is replaced with a magic cast of the selected spell. Drains runes,
 * deals magic damage, awards magic XP, fires a projectile, leans on the
 * same SpellHandler infrastructure as a manual cast.
 *
 * Eligibility design (sparky 2026-05-19): "for the most part elemental
 * spells can cast elemental spells auto, but we will make staffs at some
 * point that can cast other spells in the spell book automatically."
 *  - Plain STAFF / MAGIC_STAFF can autocast any combat spell. (Generic
 *    spellcaster — leans on inventory runes.)
 *  - Element staves (Air/Water/Earth/Fire and the battlestaff variants)
 *    can autocast spells of their element (Strike/Bolt/Blast/Wave that
 *    share the staff's element).
 *  - Other staves (Iban, god staves, Slayer's, etc.) are NOT autocast
 *    eligible for this MVP; their unique spells go through manual cast.
 *
 * Falls through to melee whenever any precondition fails — quiet failure
 * by design, so combat keeps moving and the player can fix the underlying
 * issue (out of runes, switched weapons, etc.).
 */
public final class OgrsAutocast {

	private OgrsAutocast() {}

	/**
	 * Lightweight precondition check used by AttackHandler to decide
	 * whether a click-attack should go through the autocast path (spell
	 * range + cast loop) instead of the melee/ranged path. No state
	 * change — purely a yes/no.
	 */
	public static boolean canStartAutocast(final Player player) {
		if (!player.isAutocastEnabled()) return false;
		final Spells spellEnum = spellFromId(player.getAutocastSpellId());
		if (spellEnum == null) return false;
		if (!isAutocastEligible(spellEnum)) return false;
		final SpellDef spell = player.getWorld().getServer().getEntityHandler().getSpellDef(spellEnum);
		if (spell == null) return false;
		if (player.getSkills().getMaxStat(Skill.MAGIC.id()) < spell.getReqLevel()) return false;
		if (!hasEligibleStaff(player, spellEnum)) return false;
		final int sType = spell.getSpellType();
		if (sType != 1 && sType != 2 && sType != 3) return false;
		return true;
	}

	/**
	 * Allow-list of spells that may be autocast. Sparky 2026-05-20:
	 *   "most combat spells should be available, weaken and those are
	 *    kind of not used as much... they arent autocast tho, same with
	 *    teleports, those arent autocast."
	 *
	 * Eligible:
	 *   - Elemental combat strikes/bolts/blasts/waves (Wind/Water/Earth/Fire)
	 *   - God spells (Saradomin Strike, Claws of Guthix, Flames of Zamorak)
	 *   - Special offensive bolts (Crumble Undead, Iban Blast, Chill/Shock/
	 *     Elemental Bolt)
	 *
	 * NOT eligible: teleports, debuffs (Confuse/Weaken/Vulnerability/
	 * Enfeeble/Stun/Fear/Curse), utility (alch/telegrab/superheat/bones-
	 * to-X), buffs (Thick Skin/Burst of Strength/Rock Skin/Camouflage),
	 * charge orbs, enchants. Enchant autocast is on sparky's wishlist
	 * but needs a different code path (targets inventory, not mobs).
	 */
	public static boolean isAutocastEligible(final Spells s) {
		if (s == null) return false;
		switch (s) {
			// Elemental combat (modern + retro variants).
			case WIND_STRIKE:
			case WATER_STRIKE:
			case EARTH_STRIKE:
			case FIRE_STRIKE:
			case WIND_BOLT:
			case WATER_BOLT:
			case EARTH_BOLT:
			case FIRE_BOLT:
			case WIND_BLAST:
			case WATER_BLAST:
			case EARTH_BLAST:
			case FIRE_BLAST:
			case WIND_WAVE:
			case WATER_WAVE:
			case EARTH_WAVE:
			case FIRE_WAVE:
			case WIND_BOLT_R:
			// God spells.
			case SARADOMIN_STRIKE:
			case CLAWS_OF_GUTHIX:
			case FLAMES_OF_ZAMORAK:
			// Other offensive.
			case CRUMBLE_UNDEAD:
			case IBAN_BLAST:
			case CHILL_BOLT:
			case SHOCK_BOLT:
			case ELEMENTAL_BOLT:
				return true;
			default:
				return false;
		}
	}

	/**
	 * Attempt to fire the player's autocast spell at the target.
	 *
	 * @return true if a spell was actually cast (CombatEvent should skip
	 *         the melee swing this round); false to fall through to melee.
	 */
	public static boolean tryAutocast(final Player player, final Mob target) {
		if (!player.isAutocastEnabled()) return false;

		final Spells spellEnum = spellFromId(player.getAutocastSpellId());
		if (spellEnum == null) return false;
		if (!isAutocastEligible(spellEnum)) {
			player.setAutocastSpellId(-1);
			return false;
		}

		final SpellDef spell = player.getWorld().getServer().getEntityHandler().getSpellDef(spellEnum);
		if (spell == null) return false;

		// Magic level gate.
		if (player.getSkills().getMaxStat(Skill.MAGIC.id()) < spell.getReqLevel()) {
			// One-shot user message: turn autocast off so the player isn't
			// silently melee'ing while thinking they're casting.
			player.setAutocastSpellId(-1);
			player.message("@gre@OGRS: your magic level is too low for that autocast spell — autocast disabled.");
			return false;
		}

		// Staff gate.
		if (!hasEligibleStaff(player, spellEnum)) {
			player.setAutocastSpellId(-1);
			player.message("@gre@OGRS: you need a compatible staff equipped to autocast that spell — autocast disabled.");
			return false;
		}

		// Combat-spell gate. Type 1 = mob (player), 2 = mob (npc), 3 = npc-or-player.
		// Boost/teleport/alch spells are type 0 and shouldn't autocast.
		final int sType = spell.getSpellType();
		if (sType != 1 && sType != 2 && sType != 3) return false;

		// OGRS — pre-check runes WITHOUT going through
		// SpellHandler.checkAndRemoveRunes, which calls setSuspiciousPlayer
		// when runes are missing and triggers anti-cheat (immediate channel
		// close == "client froze" from the player's POV). Autocast is a
		// loop on a timer — it'll legitimately try and fail every few
		// ticks if runes run out, which is normal play, not cheating.
		if (!hasAllRunesForSpell(player, spell)) {
			// Quiet skip — leave autocast enabled so the player resumes
			// once they refill, and fall through to melee this round.
			return false;
		}
		// Drain runes now that we've confirmed they're present. The
		// substituted runes (equipped element staff covers the matching
		// rune) are skipped just like the standard path.
		drainRunesForSpell(player, spell);

		// Damage roll using the spell's modern-magic max.
		double max = player.getWorld().getServer().getConstants()
			.getSpellDamages()
			.getSpellDamage(spellEnum, target.isPlayer() ? EntityType.PLAYER : EntityType.NPC,
				SpellDamages.MagicType.MODERNMAGIC);

		// Chaos gauntlets on bolt spells, mirroring the manual-cast path.
		final boolean gauntletBonus =
			player.getCarriedItems().getEquipment().hasEquipped(ItemId.GAUNTLETS_OF_CHAOS.id())
			&& player.getCache().getInt("famcrest_gauntlets") == Gauntlets.CHAOS.id();
		if (gauntletBonus && spell.getName().contains("bolt")) {
			max += 1;
		}

		final int damage = CombatFormula.calculateMagicDamage(max);

		// Projectile visual — pick by spell name like the manual cast does.
		final int projectileType = OgrsProjectileTypes.forSpellName(spell.getName());
		player.getWorld().getServer().getGameEventHandler().add(
			new ProjectileEvent(player.getWorld(), player, target, damage, projectileType, true));

		player.setKillType(KillType.MAGIC);
		// finalizeSpell handles magic XP + cast timer + spellok sound.
		SpellHandler.finalizeSpell(player, spell, null);

		return true;
	}

	/**
	 * Maps the integer spell ID (the same one stored as autocastSpellId) to
	 * the Spells enum value used by SpellDef lookups. The enum ordinal
	 * matches the catalog ID we expose to players + clients.
	 */
	private static Spells spellFromId(final int id) {
		final Spells[] all = Spells.values();
		if (id < 0 || id >= all.length) return null;
		return all[id];
	}

	/**
	 * Does the player have a staff equipped that's eligible to autocast the
	 * given spell? Plain staff / magic staff = wildcard. Element staves
	 * must match the spell's element.
	 */
	private static boolean hasEligibleStaff(final Player player, final Spells spellEnum) {
		final com.openrsc.server.model.container.Equipment eq =
			player.getCarriedItems().getEquipment();

		// Generic spellcaster staves — any combat spell allowed.
		if (eq.hasEquipped(ItemId.STAFF.id())) return true;
		if (eq.hasEquipped(ItemId.MAGIC_STAFF.id())) return true;

		// Element staves — match by spell's elemental keyword.
		final String name = spellEnum.name();
		if (name.startsWith("WIND_") || name.startsWith("AIR_")) {
			return eq.hasEquipped(ItemId.STAFF_OF_AIR.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_AIR.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_AIR.id());
		}
		if (name.startsWith("WATER_")) {
			return eq.hasEquipped(ItemId.STAFF_OF_WATER.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_WATER.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_WATER.id());
		}
		if (name.startsWith("EARTH_")) {
			return eq.hasEquipped(ItemId.STAFF_OF_EARTH.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_EARTH.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_EARTH.id());
		}
		if (name.startsWith("FIRE_")) {
			return eq.hasEquipped(ItemId.STAFF_OF_FIRE.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_FIRE.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_FIRE.id());
		}

		// Spell isn't elemental and no generic staff equipped → ineligible.
		return false;
	}

	/**
	 * Non-mutating, anti-cheat-safe rune check. Returns true iff the
	 * player has every rune the spell requires in their inventory,
	 * with the same element-staff substitution rule as the standard
	 * cast path (equipped Staff of Air / Battlestaff of Air covers the
	 * Air-Rune requirement, etc.).
	 *
	 * Crucially, this does NOT call SpellHandler.checkSpellRunes, which
	 * marks the player as suspicious when runes are missing. Autocast
	 * legitimately polls per-tick, so a missing-rune frame is normal
	 * play, not an attempted exploit.
	 */
	private static boolean hasAllRunesForSpell(final Player player, final SpellDef spell) {
		final com.openrsc.server.model.container.Equipment eq =
			player.getCarriedItems().getEquipment();
		for (Map.Entry<Integer, Integer> e : spell.getRunesRequired()) {
			final int runeId = e.getKey();
			final int needed = e.getValue();
			if (isRuneCoveredByEquippedStaff(eq, runeId)) continue;
			if (player.getCarriedItems().getInventory().countId(runeId) < needed) {
				return false;
			}
		}
		return true;
	}

	/** Drain runes for the spell. Caller must have first verified
	 *  {@link #hasAllRunesForSpell} returns true — otherwise this is a
	 *  no-op for the missing ones (player won't be flagged either way).
	 *  Element-staff-covered runes aren't drained. */
	private static void drainRunesForSpell(final Player player, final SpellDef spell) {
		final com.openrsc.server.model.container.Equipment eq =
			player.getCarriedItems().getEquipment();
		for (Map.Entry<Integer, Integer> e : spell.getRunesRequired()) {
			final int runeId = e.getKey();
			final int needed = e.getValue();
			if (isRuneCoveredByEquippedStaff(eq, runeId)) continue;
			player.getCarriedItems().remove(new Item(runeId, needed));
		}
	}

	/** Mirrors SpellHandler's static staff-rune substitution table:
	 *  the 4 element staves (each in 3 tiers) provide their matching
	 *  rune for free as long as one is equipped. */
	private static boolean isRuneCoveredByEquippedStaff(
			final com.openrsc.server.model.container.Equipment eq, final int runeId) {
		if (runeId == ItemId.AIR_RUNE.id()) {
			return eq.hasEquipped(ItemId.STAFF_OF_AIR.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_AIR.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_AIR.id());
		}
		if (runeId == ItemId.WATER_RUNE.id()) {
			return eq.hasEquipped(ItemId.STAFF_OF_WATER.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_WATER.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_WATER.id());
		}
		if (runeId == ItemId.EARTH_RUNE.id()) {
			return eq.hasEquipped(ItemId.STAFF_OF_EARTH.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_EARTH.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_EARTH.id());
		}
		if (runeId == ItemId.FIRE_RUNE.id()) {
			return eq.hasEquipped(ItemId.STAFF_OF_FIRE.id())
				|| eq.hasEquipped(ItemId.BATTLESTAFF_OF_FIRE.id())
				|| eq.hasEquipped(ItemId.ENCHANTED_BATTLESTAFF_OF_FIRE.id());
		}
		return false;
	}
}

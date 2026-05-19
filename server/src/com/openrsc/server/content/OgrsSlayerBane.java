package com.openrsc.server.content;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.NpcId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.Mob;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * OGRS — Slayer-bane weapons (sparky 2026-05-19 #36): a wielded weapon
 * can carry an additive damage bonus against a specific NPC family
 * ("the bane"). Sparky's framing: 'Enchanted slayer gear, like 5%
 * ghostbane, or demonbane, or goblinbane — yeah it's a steel longsword
 * but it has a little bonus, and requires a slayer level to use.'
 *
 * The slayer-level wield gate is set in each item's YAML
 * (`weapon.required_skill: 18`, `weapon.required_level: N`) and
 * enforced by the upstream ItemDef wield check — this class only
 * handles damage at hit time.
 *
 * To add a new bane weapon:
 *   1. Add the item YAML in content/items/<name>.yaml with the
 *      `weapon:` sub-block carrying required_skill: 18 and the
 *      appropriate required_level.
 *   2. Add an ItemId constant.
 *   3. Add a BANE.put entry below mapping the weapon id to the set of
 *      target NPC ids.
 *   4. Run tools/codegen-client-items.py (client-side display def).
 */
public final class OgrsSlayerBane {

	// Default bane bonus — 5% per sparky's spec. Per-weapon overrides
	// would slot in as a parallel Map<Integer, Double> if needed.
	private static final double MULTIPLIER = 1.05;

	private static final Map<Integer, Set<Integer>> BANE = new HashMap<>();

	static {
		BANE.put(ItemId.OGRS_IRON_DAGGER_SPIDERBANE.id(), new HashSet<>(Arrays.asList(
			NpcId.SPIDER.id(),
			NpcId.GIANT_SPIDER_LVL8.id(),
			NpcId.GIANT_SPIDER_LVL31.id(),
			NpcId.DEADLY_RED_SPIDER.id(),
			NpcId.ICE_SPIDER.id(),
			NpcId.POISON_SPIDER.id(),
			NpcId.SHADOW_SPIDER.id(),
			NpcId.JUNGLE_SPIDER.id(),
			NpcId.BLESSED_SPIDER.id(),
			NpcId.DUNGEON_SPIDER.id()
		)));
	}

	private OgrsSlayerBane() {}

	/**
	 * Returns the damage multiplier for a melee hit based on whether
	 * the attacker has a bane weapon wielded that matches the
	 * victim's NPC id. Returns 1.0 when no bonus applies.
	 */
	public static double melee(final Mob source, final Mob victim) {
		if (!(source instanceof Player) || !(victim instanceof Npc)) return 1.0;
		final Player p = (Player) source;
		final int weaponId = getWeaponId(p);
		if (weaponId < 0) return 1.0;
		final Set<Integer> targets = BANE.get(weaponId);
		if (targets == null || !targets.contains(((Npc) victim).getID())) return 1.0;
		return MULTIPLIER;
	}

	private static int getWeaponId(final Player p) {
		if (p.getWorld().getServer().getConfig().WANT_EQUIPMENT_TAB) {
			final Item i = p.getCarriedItems().getEquipment().get(4);
			return (i != null) ? i.getCatalogId() : -1;
		}
		synchronized (p.getCarriedItems().getInventory().getItems()) {
			for (final Item i : p.getCarriedItems().getInventory().getItems()) {
				if (i.isWielded() && i.getDef(p.getWorld()).getWieldPosition() == 4) {
					return i.getCatalogId();
				}
			}
		}
		return -1;
	}
}

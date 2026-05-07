package com.openrsc.server.plugins.custom.skills.cooking;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.Skill;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.GameObject;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.UseLocTrigger;
import com.openrsc.server.util.rsc.DataConversions;
import com.openrsc.server.util.rsc.MessageType;

import static com.openrsc.server.plugins.Functions.give;

/**
 * OGRS Cooking — bake / roast / char OGRS crops on a fire.
 *
 * Use a raw Potato / Onion / Tomato on either the OGRS Cooking Fire
 * (1313, near the allotment) or the Goblin Firepit (1307, in the camp).
 * Rolls vs Cooking level; on success grants the cooked variant + Cooking
 * XP, on failure produces a Burnt Crop and no XP. Plays the cooking
 * sound either way for feedback.
 *
 * Burn curve: 50% burn at lvl 1, ramping down so it's basically zero
 * by lvl ~50. Required level: 1 (entry-tier; no gating). XP scales by
 * crop tier — tomato yields more than onion yields more than potato.
 *
 * Picks up the eat_heals via the OGRS items pipeline; the cooked food
 * items are edible through the standard upstream Eating plugin.
 */
public final class OgrsCropCooking implements UseLocTrigger {

	private static final int COOKING_FIRE_ID = 1313;
	private static final int GOBLIN_FIREPIT_ID = 1307;

	@Override
	public boolean blockUseLoc(final Player player, final GameObject obj, final Item item) {
		final int oid = obj.getID();
		if (oid != COOKING_FIRE_ID && oid != GOBLIN_FIREPIT_ID) return false;
		final int iid = item.getCatalogId();
		return iid == ItemId.POTATO.id() || iid == ItemId.ONION.id() || iid == ItemId.TOMATO.id();
	}

	@Override
	public void onUseLoc(final Player player, final GameObject obj, final Item item) {
		// Per-crop result + XP shape.
		final int rawId = item.getCatalogId();
		final int cookedId;
		final int xpDisplay;
		final String successLine;
		if (rawId == ItemId.POTATO.id()) {
			cookedId = ItemId.OGRS_BAKED_POTATO.id();
			xpDisplay = 25;
			successLine = "@gre@The potato bakes golden. You pull it from the embers.";
		} else if (rawId == ItemId.ONION.id()) {
			cookedId = ItemId.OGRS_ROASTED_ONION.id();
			xpDisplay = 30;
			successLine = "@gre@The onion roasts soft. The skin slips off.";
		} else /* TOMATO */ {
			cookedId = ItemId.OGRS_CHARRED_TOMATO.id();
			xpDisplay = 40;
			successLine = "@gre@The tomato blisters and chars beautifully.";
		}

		// Burn check — simple linear curve.
		final int level = player.getSkills().getLevel(Skill.COOKING.id());
		final int burnRoll = DataConversions.random(1, 100);
		final int burnChance = Math.max(0, 50 - level);
		final boolean burned = burnRoll <= burnChance;

		// Consume the raw crop regardless of outcome.
		player.getCarriedItems().remove(new Item(rawId, 1));

		ActionSender.sendSound(player, "cooking");
		if (burned) {
			give(player, ItemId.OGRS_BURNT_CROP.id(), 1);
			player.playerServerMessage(MessageType.QUEST,
				"You let the fire run hot — the crop burns to a cinder.");
			return;
		}

		give(player, cookedId, 1);
		player.getSkills().addExperience(Skill.COOKING.id(), xpDisplay * 4);
		player.message(successLine);
		player.playerServerMessage(MessageType.QUEST,
			"+" + xpDisplay + " Cooking XP.");
	}
}

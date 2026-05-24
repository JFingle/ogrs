package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.OpInvTrigger;

/**
 * OGRS Antidote Vial (item 1613) — Spider Boss spec drop. "Drink" verb
 * cures the player's poison instantly and consumes the vial.
 *
 * The 60-second poison-immunity window from the spec is NOT implemented
 * yet — the engine has no "poison immunity" state field. v2 work: add
 * a cache key with timestamp, gate setPoisonDamage to no-op while the
 * timestamp is recent.
 *
 * For now: instant cure + vial consumed. Still significantly improves
 * the Crypt Spider Matron fight — players who get poisoned have a
 * counter rather than tanking the venom for its full duration.
 */
public final class AntidoteVial implements OpInvTrigger {

	private static final int VIAL_ID = ItemId.OGRS_ANTIDOTE_VIAL.id();

	@Override
	public boolean blockOpInv(final Player player, final Integer invIndex, final Item item, final String command) {
		return item.getCatalogId() == VIAL_ID && command != null && command.equalsIgnoreCase("drink");
	}

	@Override
	public void onOpInv(final Player player, final Integer invIndex, final Item item, final String command) {
		if (player.getCurrentPoisonPower() <= 0) {
			player.message("You're not poisoned — no need to drink this.");
			return;
		}
		player.cure();
		player.getCarriedItems().getInventory().remove(new Item(VIAL_ID, 1), true);
		player.message("@gre@You drink the antidote. The venom drains from your veins.");
	}
}

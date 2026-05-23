package com.openrsc.server.plugins.custom.npcs.lumbridge;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.constants.OgrsNpcId;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.net.rsc.ActionSender;
import com.openrsc.server.plugins.triggers.KillNpcTrigger;
import com.openrsc.server.util.rsc.DataConversions;

import static com.openrsc.server.plugins.Functions.give;

/**
 * OGRS Goblin Shaman extra-drop handler — separate from the quest
 * trigger so non-quest kills (or post-quest kills) still award the
 * staff. The OldWatsSeedPouch quest plugin handles the pouch drop;
 * this one handles the always-on staff drop at 50%.
 *
 * Returning {@code true} from {@code blockKillNpc} only causes
 * {@code onKillNpc} to fire — confirmed in Npc.java's death sequence
 * that default loot still drops regardless of the plugin return value.
 */
public final class GoblinShamanDrops implements KillNpcTrigger {

	private static final int GOBLIN_SHAMAN_NPC_ID = OgrsNpcId.GOBLIN_SHAMAN.id();
	private static final int STAFF_DROP_PERCENT = 50;

	@Override
	public boolean blockKillNpc(final Player player, final Npc npc) {
		return npc.getID() == GOBLIN_SHAMAN_NPC_ID;
	}

	@Override
	public void onKillNpc(final Player player, final Npc npc) {
		if (DataConversions.random(1, 100) > STAFF_DROP_PERCENT) return;
		give(player, ItemId.OGRS_CRACKED_SHAMAN_STAFF.id(), 1);
		ActionSender.sendSound(player, "foundgem");
		player.message("@gre@The shaman's staff clatters to the floor. The bone tip is still warm.");
	}
}

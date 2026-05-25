package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.persistence.OgrsPersistence;
import com.openrsc.server.plugins.triggers.CommandTrigger;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * OGRS — admin-only manual flush of the social registries to DB.
 *
 *   ::ogrssave  — force OgrsPersistence.flushAll() right now. Used
 *                 before a planned restart so the snapshot is fresh.
 *
 * The periodic 30-second flush handles the common case; this command
 * exists so an admin can guarantee a fresh snapshot before bringing
 * the server down (server uptime is normally protected, but planned
 * maintenance happens occasionally).
 */
public class OgrsSaveCommand implements CommandTrigger {

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(), "ogrssave", "ogrsflush");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		if (!player.isAdmin()) {
			player.message("@red@Admin only.");
			return;
		}
		final long startNs = System.nanoTime();
		OgrsPersistence.flushAll(player.getWorld());
		final long elapsedMs = (System.nanoTime() - startNs) / 1_000_000L;
		player.message("@gre@OGRS persistence: flush complete (" + elapsedMs + "ms).");
	}
}

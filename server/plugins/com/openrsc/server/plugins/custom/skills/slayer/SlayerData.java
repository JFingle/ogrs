package com.openrsc.server.plugins.custom.skills.slayer;

/**
 * In-memory snapshot of a player's active slayer task.
 *
 * Hydrated from {@link com.openrsc.server.model.Cache} on read; the cache
 * itself persists to the `player_cache` table automatically when the player
 * saves. We don't store SlayerData instances anywhere — only the underlying
 * cache keys.
 */
public class SlayerData {
	public final int npcId;
	public final String npcName;
	public final int total;
	public int remaining;

	public SlayerData(final int npcId, final String npcName, final int total, final int remaining) {
		this.npcId = npcId;
		this.npcName = npcName;
		this.total = total;
		this.remaining = remaining;
	}

	public boolean isComplete() {
		return remaining <= 0;
	}
}

package com.openrsc.server.plugins.custom.skills.slayer;

/**
 * Active slayer task assigned to a single player.
 *
 * MVP: in-memory only — does not survive logout. Persistence is the next
 * iteration; once the YAML/SQL content pipeline lands we'll persist active
 * tasks and slayer XP to the players table.
 */
public class SlayerData {
	public final int npcId;
	public final String npcName;
	public final int total;
	public int remaining;
	public final long assignedAtMillis;

	public SlayerData(final int npcId, final String npcName, final int total) {
		this.npcId = npcId;
		this.npcName = npcName;
		this.total = total;
		this.remaining = total;
		this.assignedAtMillis = System.currentTimeMillis();
	}

	public boolean isComplete() {
		return remaining <= 0;
	}
}

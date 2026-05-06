package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.model.entity.player.Player;

import java.util.Random;

/**
 * Slayer state for the OGRS world. All state lives on
 * {@link com.openrsc.server.model.Cache} via the player's `getCache()`,
 * which is automatically persisted to the `player_cache` table on save.
 *
 * Cache keys (all prefixed `ogrs_` to avoid colliding with upstream content):
 *   ogrs_slayer_xp              int       cumulative XP
 *   ogrs_slayer_task_name       string    active task family name (acts as
 *                                         primary key into TASK_POOL); absent
 *                                         = no active task
 *   ogrs_slayer_task_total      int       original count assigned
 *   ogrs_slayer_task_remaining  int       count remaining
 *
 *   ogrs_slayer_task_npc        int       (LEGACY — deprecated by
 *                                         family-based matching; older saved
 *                                         tasks may still have this key set,
 *                                         we ignore it on read)
 *
 * Task family matching: a single Slayer assignment ("Goblin") covers
 * multiple NPC type ids (4, 62, 153, 154, 660 — there are 5 distinct
 * "Goblin" defs in NpcDefs.json with different sprites and combat stats but
 * the same family name). The cache stores the family name; SlayerService
 * resolves it to a TaskTemplate at every read so adding new NPC ids to a
 * family is a single-line change here, not a per-player migration.
 */
public class SlayerService {

	public static final String KEY_XP = "ogrs_slayer_xp";
	public static final String KEY_TASK_NAME = "ogrs_slayer_task_name";
	public static final String KEY_TASK_TOTAL = "ogrs_slayer_task_total";
	public static final String KEY_TASK_REMAINING = "ogrs_slayer_task_remaining";

	private static final Random rng = new Random();

	/**
	 * MVP task pool. Phase 1 moves this into content/skills/slayer/tasks.yaml.
	 * Each TaskTemplate covers one display name + the full set of NPC ids
	 * that count toward the task.
	 */
	private static final TaskTemplate[] TASK_POOL = {
		// All 5 Goblin variants in NpcDefs.json.
		new TaskTemplate("Goblin", new int[]{4, 62, 153, 154, 660}, 5, 8),
	};

	private SlayerService() { /* no instances */ }

	// -- XP --

	public static int getXp(final Player player) {
		return player.getCache().hasKey(KEY_XP) ? player.getCache().getInt(KEY_XP) : 0;
	}

	public static int addXp(final Player player, final int xp) {
		final int total = getXp(player) + xp;
		player.getCache().set(KEY_XP, total);
		return total;
	}

	// -- Tasks --

	public static SlayerData getActiveTask(final Player player) {
		if (!player.getCache().hasKey(KEY_TASK_NAME)) {
			return null;
		}
		final String name = player.getCache().getString(KEY_TASK_NAME);
		final TaskTemplate template = findTemplate(name);
		if (template == null) {
			// Stale task pointing at a removed template — treat as no task.
			return null;
		}
		return new SlayerData(
			template.npcIds[0],
			name,
			player.getCache().getInt(KEY_TASK_TOTAL),
			player.getCache().getInt(KEY_TASK_REMAINING)
		);
	}

	public static SlayerData assignRandomTask(final Player player) {
		final TaskTemplate t = TASK_POOL[rng.nextInt(TASK_POOL.length)];
		final int total = t.minCount + rng.nextInt(t.maxCount - t.minCount + 1);
		player.getCache().store(KEY_TASK_NAME, t.name);
		player.getCache().set(KEY_TASK_TOTAL, total);
		player.getCache().set(KEY_TASK_REMAINING, total);
		return new SlayerData(t.npcIds[0], t.name, total, total);
	}

	public static void clearTask(final Player player) {
		player.getCache().remove(KEY_TASK_NAME, KEY_TASK_TOTAL, KEY_TASK_REMAINING);
	}

	/**
	 * Does this NPC id count toward the player's active task?
	 * Used by both the kill tracker (gating dispatch) and recordKill itself.
	 */
	public static boolean isTaskTarget(final Player player, final int npcId) {
		if (!player.getCache().hasKey(KEY_TASK_NAME)) {
			return false;
		}
		final TaskTemplate t = findTemplate(player.getCache().getString(KEY_TASK_NAME));
		if (t == null) {
			return false;
		}
		for (final int id : t.npcIds) {
			if (id == npcId) return true;
		}
		return false;
	}

	/** Returns true if the kill counted. Caller already ensured isTaskTarget. */
	public static boolean recordKill(final Player player, final int killedNpcId) {
		if (!isTaskTarget(player, killedNpcId)) {
			return false;
		}
		final int remaining = player.getCache().getInt(KEY_TASK_REMAINING);
		if (remaining <= 0) {
			return false;
		}
		player.getCache().set(KEY_TASK_REMAINING, remaining - 1);
		return true;
	}

	private static TaskTemplate findTemplate(final String name) {
		for (final TaskTemplate t : TASK_POOL) {
			if (t.name.equals(name)) return t;
		}
		return null;
	}

	// -- Levels --

	/** OSRS-style XP-per-level table; level capped at 99 per the contract. */
	public static int getLevel(final int xp) {
		if (xp <= 0) return 1;
		double sum = 0;
		int level = 1;
		for (int i = 1; i < 99; i++) {
			sum += Math.floor(i + 300 * Math.pow(2, i / 7.0));
			final int xpAtLevel = (int) Math.floor(sum / 4);
			if (xpAtLevel > xp) break;
			level = i + 1;
		}
		return Math.min(99, level);
	}

	private static final class TaskTemplate {
		final String name;
		final int[] npcIds;
		final int minCount;
		final int maxCount;
		TaskTemplate(String name, int[] npcIds, int min, int max) {
			this.name = name;
			this.npcIds = npcIds;
			this.minCount = min;
			this.maxCount = max;
		}
	}
}

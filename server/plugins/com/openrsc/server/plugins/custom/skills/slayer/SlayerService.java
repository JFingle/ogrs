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
 *   ogrs_slayer_task_npc        int       active task NPC id (absent = no task)
 *   ogrs_slayer_task_name       string    display name for the messages
 *   ogrs_slayer_task_total      int       original count assigned
 *   ogrs_slayer_task_remaining  int       count remaining
 */
public class SlayerService {

	public static final String KEY_XP = "ogrs_slayer_xp";
	public static final String KEY_TASK_NPC = "ogrs_slayer_task_npc";
	public static final String KEY_TASK_NAME = "ogrs_slayer_task_name";
	public static final String KEY_TASK_TOTAL = "ogrs_slayer_task_total";
	public static final String KEY_TASK_REMAINING = "ogrs_slayer_task_remaining";

	private static final Random rng = new Random();

	/**
	 * MVP task pool. Phase 1 moves this into content/skills/slayer/tasks.yaml.
	 * Goblin id 4 lives in NpcDefs.json. Add new NPC types here as you go.
	 */
	private static final TaskTemplate[] TASK_POOL = {
		new TaskTemplate(4, "Goblin", 5, 8),
	};

	private SlayerService() { /* no instances */ }

	// -- XP --

	public static int getXp(final Player player) {
		return player.getCache().hasKey(KEY_XP) ? player.getCache().getInt(KEY_XP) : 0;
	}

	/** Adds xp and returns the new total. */
	public static int addXp(final Player player, final int xp) {
		final int total = getXp(player) + xp;
		player.getCache().set(KEY_XP, total);
		return total;
	}

	// -- Tasks --

	public static SlayerData getActiveTask(final Player player) {
		if (!player.getCache().hasKey(KEY_TASK_NPC)) {
			return null;
		}
		return new SlayerData(
			player.getCache().getInt(KEY_TASK_NPC),
			player.getCache().getString(KEY_TASK_NAME),
			player.getCache().getInt(KEY_TASK_TOTAL),
			player.getCache().getInt(KEY_TASK_REMAINING)
		);
	}

	public static SlayerData assignRandomTask(final Player player) {
		final TaskTemplate t = TASK_POOL[rng.nextInt(TASK_POOL.length)];
		final int total = t.minCount + rng.nextInt(t.maxCount - t.minCount + 1);
		player.getCache().set(KEY_TASK_NPC, t.npcId);
		player.getCache().store(KEY_TASK_NAME, t.npcName);
		player.getCache().set(KEY_TASK_TOTAL, total);
		player.getCache().set(KEY_TASK_REMAINING, total);
		return new SlayerData(t.npcId, t.npcName, total, total);
	}

	public static void clearTask(final Player player) {
		player.getCache().remove(KEY_TASK_NPC, KEY_TASK_NAME, KEY_TASK_TOTAL, KEY_TASK_REMAINING);
	}

	/** Returns true if the kill counted toward an active task. */
	public static boolean recordKill(final Player player, final int killedNpcId) {
		if (!player.getCache().hasKey(KEY_TASK_NPC)) {
			return false;
		}
		if (player.getCache().getInt(KEY_TASK_NPC) != killedNpcId) {
			return false;
		}
		final int remaining = player.getCache().getInt(KEY_TASK_REMAINING);
		if (remaining <= 0) {
			return false;
		}
		player.getCache().set(KEY_TASK_REMAINING, remaining - 1);
		return true;
	}

	// -- Levels --

	/** OSRS-style XP-per-level table; level capped at 99 per the contract. */
	public static int getLevel(final int xp) {
		if (xp <= 0) {
			return 1;
		}
		double sum = 0;
		int level = 1;
		for (int i = 1; i < 99; i++) {
			sum += Math.floor(i + 300 * Math.pow(2, i / 7.0));
			final int xpAtLevel = (int) Math.floor(sum / 4);
			if (xpAtLevel > xp) {
				break;
			}
			level = i + 1;
		}
		return Math.min(99, level);
	}

	private static final class TaskTemplate {
		final int npcId;
		final String npcName;
		final int minCount;
		final int maxCount;
		TaskTemplate(int npcId, String npcName, int min, int max) {
			this.npcId = npcId;
			this.npcName = npcName;
			this.minCount = min;
			this.maxCount = max;
		}
	}
}

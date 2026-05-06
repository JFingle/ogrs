package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.model.entity.player.Player;

import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;

/**
 * In-memory Slayer state for the OGRS world.
 *
 * MVP: state lives in static maps keyed by username hash. Lost on server
 * restart and on player logout. Acceptable for proving the system; Phase 1
 * adds DB persistence (slayer_xp, slayer_task_npc, slayer_task_remaining
 * columns on players).
 *
 * The slayer skill is NOT yet integrated into the formal Skills registry,
 * so it does not appear in the client's skill panel. A separate XP+level
 * track is computed here and surfaced via chat messages until we extend
 * the engine's skill enum.
 */
public class SlayerService {

	/** Player username hash → active task. */
	private static final ConcurrentHashMap<Long, SlayerData> activeTasks = new ConcurrentHashMap<>();
	/** Player username hash → cumulative slayer XP. */
	private static final ConcurrentHashMap<Long, Integer> xpByPlayer = new ConcurrentHashMap<>();
	private static final Random rng = new Random();

	/**
	 * MVP task pool. Each entry: (npc id, display name, min count, max count).
	 * Goblin id 4 lives in NpcDefs.json. Phase 1 moves this into
	 * content/skills/slayer/tasks.yaml as data, with combat-level requirements
	 * and area restrictions.
	 */
	private static final TaskTemplate[] TASK_POOL = {
		new TaskTemplate(4, "Goblin", 5, 8),
	};

	private SlayerService() { /* no instances */ }

	public static SlayerData assignRandomTask(final Player player) {
		final TaskTemplate t = TASK_POOL[rng.nextInt(TASK_POOL.length)];
		final int count = t.minCount + rng.nextInt(t.maxCount - t.minCount + 1);
		final SlayerData task = new SlayerData(t.npcId, t.npcName, count);
		activeTasks.put(player.getUsernameHash(), task);
		return task;
	}

	public static SlayerData getActiveTask(final Player player) {
		return activeTasks.get(player.getUsernameHash());
	}

	public static void clearTask(final Player player) {
		activeTasks.remove(player.getUsernameHash());
	}

	/** Returns true if the kill counted toward the player's active task. */
	public static boolean recordKill(final Player player, final int killedNpcId) {
		final SlayerData task = activeTasks.get(player.getUsernameHash());
		if (task == null || task.npcId != killedNpcId || task.isComplete()) {
			return false;
		}
		task.remaining--;
		return true;
	}

	public static int addXp(final Player player, final int xp) {
		return xpByPlayer.merge(player.getUsernameHash(), xp, Integer::sum);
	}

	public static int getXp(final Player player) {
		return xpByPlayer.getOrDefault(player.getUsernameHash(), 0);
	}

	/**
	 * OSRS-style level from XP, computed via the standard XP-per-level table.
	 * Caps at 99 to match the contract.
	 */
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

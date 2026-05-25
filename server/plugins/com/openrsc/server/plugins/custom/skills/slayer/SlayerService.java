package com.openrsc.server.plugins.custom.skills.slayer;

import com.openrsc.server.constants.Skill;
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
	 * Task pool — loaded lazily from {@code content/skills/slayer/tasks.yaml}
	 * via {@link SlayerTaskLoader} on first access. Falls back to a built-in
	 * Goblin entry if the file is missing or unparseable. Adding a new task =
	 * one entry in the YAML, no code change.
	 */
	private static volatile SlayerTaskLoader.Template[] taskPool;

	private static SlayerTaskLoader.Template[] pool() {
		SlayerTaskLoader.Template[] p = taskPool;
		if (p == null) {
			synchronized (SlayerService.class) {
				p = taskPool;
				if (p == null) {
					p = SlayerTaskLoader.loadOrDefault();
					taskPool = p;
				}
			}
		}
		return p;
	}

	private SlayerService() { /* no instances */ }

	// -- XP --

	/**
	 * If `want_slayer: true` is set on the world, slayer XP lives on the
	 * player's `Skills` object (and persists to the `experience.slayer` DB
	 * column). Otherwise it lives in the player_cache under `ogrs_slayer_xp`
	 * for backward compat with worlds running before the skill registry change.
	 */
	private static boolean useRealSkill(final Player player) {
		return player.getWorld().getServer().getConfig().WANT_SLAYER;
	}

	/** Returns XP in DISPLAY units (the value the player sees). Engine stores 4x. */
	public static int getXp(final Player player) {
		if (useRealSkill(player)) {
			// Engine stores at 4x display units (RSC convention). Convert back.
			return player.getSkills().getExperience(Skill.SLAYER.id()) / 4;
		}
		return player.getCache().hasKey(KEY_XP) ? player.getCache().getInt(KEY_XP) : 0;
	}

	/**
	 * Adds {@code xp} display-units. Routes through the real skill XP system
	 * when WANT_SLAYER is enabled (multiplying by 4 for the engine's storage
	 * format and triggering the standard level-up message), or falls back to
	 * the cache key. Returns the new total in display units.
	 */
	public static int addXp(final Player player, final int xp) {
		if (useRealSkill(player)) {
			player.getSkills().addExperience(Skill.SLAYER.id(), xp * 4);
			return getXp(player);
		}
		final int total = getXp(player) + xp;
		player.getCache().set(KEY_XP, total);
		return total;
	}

	/** Player's current Slayer level. Uses real skill registry when WANT_SLAYER. */
	public static int getPlayerLevel(final Player player) {
		if (useRealSkill(player)) {
			return player.getSkills().getMaxStat(Skill.SLAYER.id());
		}
		return getLevel(getXp(player));
	}

	// -- Tasks --

	public static SlayerData getActiveTask(final Player player) {
		if (!player.getCache().hasKey(KEY_TASK_NAME)) {
			return null;
		}
		final String name = player.getCache().getString(KEY_TASK_NAME);
		final SlayerTaskLoader.Template template = findTemplate(name);
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
		final SlayerTaskLoader.Template[] p = pool();
		final SlayerTaskLoader.Template t = p[rng.nextInt(p.length)];
		final int total = t.minCount + rng.nextInt(t.maxCount - t.minCount + 1);
		player.getCache().store(KEY_TASK_NAME, t.name);
		player.getCache().set(KEY_TASK_TOTAL, total);
		player.getCache().set(KEY_TASK_REMAINING, total);
		// OGRS — UI track P1: push updated task to the HUD widget.
		ogrsPushSlayerTask(player);
		return new SlayerData(t.npcIds[0], t.name, total, total);
	}

	public static void clearTask(final Player player) {
		player.getCache().remove(KEY_TASK_NAME, KEY_TASK_TOTAL, KEY_TASK_REMAINING);
		// OGRS — UI track P1: push cleared task to the HUD widget.
		ogrsPushSlayerTask(player);
	}

	/** OGRS — UI track P1: send current slayer task to the client for
	 *  the HUD widget. Lives here (not in ActionSender) because the
	 *  engine-core ActionSender can't depend on plugin types. */
	public static void ogrsPushSlayerTask(final Player player) {
		final SlayerData task = getActiveTask(player);
		final boolean has = task != null;
		final String npcName = has ? task.npcName : "";
		final int remaining  = has ? task.remaining : 0;
		final int level      = getPlayerLevel(player);
		com.openrsc.server.net.rsc.ActionSender.sendSlayerTask(player, has, npcName, remaining, level);
	}

	/**
	 * Does this NPC id count toward the player's active task?
	 * Used by both the kill tracker (gating dispatch) and recordKill itself.
	 */
	public static boolean isTaskTarget(final Player player, final int npcId) {
		if (!player.getCache().hasKey(KEY_TASK_NAME)) {
			return false;
		}
		final SlayerTaskLoader.Template t = findTemplate(player.getCache().getString(KEY_TASK_NAME));
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
		// OGRS — UI track P1: push updated remaining count to the HUD.
		ogrsPushSlayerTask(player);
		return true;
	}

	private static SlayerTaskLoader.Template findTemplate(final String name) {
		for (final SlayerTaskLoader.Template t : pool()) {
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
}

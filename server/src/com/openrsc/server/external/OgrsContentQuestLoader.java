package com.openrsc.server.external;

import com.openrsc.server.constants.Skill;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * OGRS content-pipeline QUEST loader — fourth leg after NPCs / items /
 * scenery. Reads {@code <repo>/content/quests/*.yaml} once at server
 * startup and exposes the parsed metadata via {@link #byFilename(String)}.
 *
 * Quest plugins live in {@code server/plugins/.../custom/quests/} as
 * concrete classes extending {@code AbstractOgrsQuest}. Each plugin
 * names its YAML in its constructor; the abstract base pulls metadata
 * from this loader's static map. Behavioural code (dialog branches,
 * trigger gates) stays in the Java plugin — this loader handles only
 * the data half (id, name, points, journal copy, declared rewards).
 *
 * Constraint: quest ids must be a contiguous run after the upstream
 * tail (PEELING_THE_ONION = 51), because
 * {@code ActionSender.sendQuestInfo} sizes the {@code questCompleted}
 * int[] to {@code numberOfQuests} and indexes it by quest id. A sparse
 * id would AIOOBE the legacy client. Validated on load.
 *
 * Schema (see {@code content/quests/old_wats_seed_pouch.yaml}):
 * <pre>
 * id: 52
 * name: "..."
 * quest_points: 1
 * members: false
 * journal: { 0: "...", 1: "...", 2: "..." }
 * rewards:
 *   xp:    [ { skill: farming, amount: 250 } ]
 *   items: [ { id: 1594, amount: 10 }, { id: 10, amount: 100 } ]
 * </pre>
 */
public final class OgrsContentQuestLoader {

	private static final Logger LOGGER = LogManager.getLogger(OgrsContentQuestLoader.class);

	/** Loaded once during EntityHandler init; read by AbstractOgrsQuest. */
	private static final Map<String, QuestMetadata> byFile = new HashMap<>();

	private OgrsContentQuestLoader() { /* static singleton */ }

	public static QuestMetadata byFilename(final String filename) {
		return byFile.get(filename);
	}

	private static Path resolveDir() {
		final String override = System.getProperty("ogrs.content.dir");
		if (override != null && !override.isEmpty()) {
			return Paths.get(override, "quests");
		}
		return Paths.get("..", "content", "quests");
	}

	/** Populate the metadata map. Idempotent — clears any prior load. */
	public static void loadAll() {
		byFile.clear();
		final Path dir = resolveDir();
		if (!Files.isDirectory(dir)) {
			LOGGER.info("OGRS content/quests/ not found at {} — skipping YAML quest load", dir.toAbsolutePath());
			return;
		}

		final Yaml yaml = new Yaml();
		try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, "*.yaml")) {
			for (final Path file : stream) {
				try (InputStream in = Files.newInputStream(file)) {
					@SuppressWarnings("unchecked")
					final Map<String, Object> data = yaml.load(in);
					if (data == null) continue;
					final QuestMetadata m = parse(data, file.getFileName().toString());
					byFile.put(file.getFileName().toString(), m);
				} catch (final Exception e) {
					LOGGER.error("OGRS quest YAML parse failed: " + file, e);
				}
			}
		} catch (final Exception e) {
			LOGGER.error("OGRS quest YAML directory scan failed", e);
			return;
		}
		LOGGER.info("OGRS: loaded {} quest YAML def(s) from {}", byFile.size(), dir.toAbsolutePath());
	}

	@SuppressWarnings("unchecked")
	private static QuestMetadata parse(final Map<String, Object> data, final String filename) {
		final QuestMetadata m = new QuestMetadata();
		m.id = ((Number) req(data, "id", filename)).intValue();
		m.name = (String) req(data, "name", filename);
		m.questPoints = asInt(data, "quest_points", 1);
		m.members = asBool(data, "members", false);

		// Journal — keys may be Integer or String depending on YAML parsing.
		final Object journalObj = data.get("journal");
		if (journalObj instanceof Map) {
			final Map<Object, Object> j = (Map<Object, Object>) journalObj;
			for (final Map.Entry<Object, Object> e : j.entrySet()) {
				final int stage = e.getKey() instanceof Number
					? ((Number) e.getKey()).intValue()
					: Integer.parseInt(e.getKey().toString());
				m.journal.put(stage, String.valueOf(e.getValue()));
			}
		}

		// Rewards.
		final Map<String, Object> rewards = (Map<String, Object>) data.getOrDefault("rewards", Collections.emptyMap());
		final List<Map<String, Object>> xp = (List<Map<String, Object>>) rewards.getOrDefault("xp", Collections.emptyList());
		for (final Map<String, Object> r : xp) {
			final String skillName = String.valueOf(r.get("skill")).toUpperCase();
			final int skillId = Skill.of(skillName).id();
			if (skillId < 0) {
				throw new IllegalStateException(filename + ": unknown skill `" + r.get("skill") + "`");
			}
			final XpReward x = new XpReward();
			x.skillId = skillId;
			x.amountDisplay = ((Number) r.get("amount")).intValue();
			m.xpRewards.add(x);
		}
		final List<Map<String, Object>> items = (List<Map<String, Object>>) rewards.getOrDefault("items", Collections.emptyList());
		for (final Map<String, Object> r : items) {
			final ItemReward i = new ItemReward();
			i.itemId = ((Number) r.get("id")).intValue();
			i.amount = ((Number) r.get("amount")).intValue();
			m.itemRewards.add(i);
		}

		return m;
	}

	private static Object req(final Map<String, Object> m, final String key, final String filename) {
		final Object v = m.get(key);
		if (v == null) throw new IllegalArgumentException("`" + key + "` is required in " + filename);
		return v;
	}

	private static int asInt(final Map<String, Object> m, final String key, final int fallback) {
		final Object v = m.get(key);
		return v == null ? fallback : ((Number) v).intValue();
	}

	private static boolean asBool(final Map<String, Object> m, final String key, final boolean fallback) {
		final Object v = m.get(key);
		return v == null ? fallback : (Boolean) v;
	}

	public static final class QuestMetadata {
		public int id;
		public String name;
		public int questPoints;
		public boolean members;
		public final Map<Integer, String> journal = new HashMap<>();
		public final List<XpReward> xpRewards = new ArrayList<>();
		public final List<ItemReward> itemRewards = new ArrayList<>();
	}

	public static final class XpReward {
		public int skillId;
		/** XP in display units; engine multiplies by 4 internally. */
		public int amountDisplay;
	}

	public static final class ItemReward {
		public int itemId;
		public int amount;
	}
}

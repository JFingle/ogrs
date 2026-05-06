package com.openrsc.server.plugins.custom.skills.slayer;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Loads slayer task templates from {@code <repo>/content/skills/slayer/tasks.yaml}.
 * Called once at first {@link SlayerService} access; cached for the server's lifetime.
 *
 * Schema (see content/skills/slayer/tasks.yaml):
 * <pre>
 * tasks:
 *   - name: Goblin
 *     npc_ids: [4, 62, 153, 154, 660]
 *     count: { min: 5, max: 8 }
 *     # optional:
 *     # combat_level_req: 5
 *     # area: lumbridge
 * </pre>
 */
final class SlayerTaskLoader {

	private static final Logger LOGGER = LogManager.getLogger(SlayerTaskLoader.class);

	static final class Template {
		final String name;
		final int[] npcIds;
		final int minCount;
		final int maxCount;

		Template(String name, int[] npcIds, int minCount, int maxCount) {
			this.name = name;
			this.npcIds = npcIds;
			this.minCount = minCount;
			this.maxCount = maxCount;
		}
	}

	private SlayerTaskLoader() { /* no instances */ }

	private static Path resolveFile() {
		final String override = System.getProperty("ogrs.content.dir");
		final Path base = (override == null || override.isEmpty())
			? Paths.get("..", "content")
			: Paths.get(override);
		return base.resolve("skills").resolve("slayer").resolve("tasks.yaml");
	}

	/** Returns the loaded task pool. Falls back to a single Goblin entry if the file is missing/broken. */
	static Template[] loadOrDefault() {
		final Path file = resolveFile();
		if (!Files.isRegularFile(file)) {
			LOGGER.warn("OGRS slayer tasks.yaml not found at {} — using built-in Goblin fallback", file.toAbsolutePath());
			return defaultPool();
		}
		try (InputStream in = Files.newInputStream(file)) {
			@SuppressWarnings("unchecked")
			final Map<String, Object> root = new Yaml().load(in);
			if (root == null) return defaultPool();
			@SuppressWarnings("unchecked")
			final List<Map<String, Object>> tasks = (List<Map<String, Object>>) root.get("tasks");
			if (tasks == null || tasks.isEmpty()) return defaultPool();

			final List<Template> out = new ArrayList<>(tasks.size());
			for (final Map<String, Object> t : tasks) {
				final String name = (String) t.get("name");
				@SuppressWarnings("unchecked")
				final List<Object> ids = (List<Object>) t.get("npc_ids");
				if (name == null || ids == null || ids.isEmpty()) {
					LOGGER.warn("OGRS slayer task missing name/npc_ids — skipped: {}", t);
					continue;
				}
				final int[] arr = new int[ids.size()];
				for (int i = 0; i < ids.size(); i++) arr[i] = ((Number) ids.get(i)).intValue();
				@SuppressWarnings("unchecked")
				final Map<String, Object> count = (Map<String, Object>) t.get("count");
				final int min = count == null ? 5 : ((Number) count.getOrDefault("min", 5)).intValue();
				final int max = count == null ? 8 : ((Number) count.getOrDefault("max", min)).intValue();
				out.add(new Template(name, arr, min, max));
			}

			LOGGER.info("OGRS: loaded {} slayer task template(s) from {}", out.size(), file.toAbsolutePath());
			return out.toArray(new Template[0]);
		} catch (final Exception e) {
			LOGGER.error("OGRS slayer tasks.yaml parse failed at " + file.toAbsolutePath() + " — using fallback", e);
			return defaultPool();
		}
	}

	private static Template[] defaultPool() {
		return new Template[]{
			new Template("Goblin", new int[]{4, 62, 153, 154, 660}, 5, 8)
		};
	}
}

package com.openrsc.server.external;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

/**
 * OGRS content-pipeline NPC loader.
 *
 * Reads {@code <repo>/content/npcs/*.yaml}, parses each into an {@link NPCDef},
 * and returns the list in declared-id order. Hooked into
 * {@link EntityHandler#load()} after the upstream JSON loaders so YAML-defined
 * NPCs are appended to the same {@code npcs} ArrayList.
 *
 * Constraint (until the EntityHandler-HashMap refactor lands, backlog #9):
 * declared ids must be sequential starting at the npcs list size at the
 * moment of YAML load. The loader fails loud if a gap is found.
 *
 * Path resolution: {@code ../content/npcs/} from the server's working
 * directory (the {@code server/} project root when run via Gradle's
 * application plugin). Override by setting JVM property
 * {@code -Dogrs.content.dir=/abs/path/to/content}.
 *
 * Schema (see {@code content/npcs/grizzled_traveler.yaml} for a worked
 * example).
 */
public class OgrsContentNpcLoader {

	private static final Logger LOGGER = LogManager.getLogger(OgrsContentNpcLoader.class);

	/** A loaded NPC: declared id + parsed def. Sortable by id. */
	public static final class Entry {
		public final int id;
		public final NPCDef def;
		public final String sourceFile;
		Entry(int id, NPCDef def, String sourceFile) {
			this.id = id;
			this.def = def;
			this.sourceFile = sourceFile;
		}
	}

	private static Path resolveDir() {
		final String override = System.getProperty("ogrs.content.dir");
		if (override != null && !override.isEmpty()) {
			return Paths.get(override, "npcs");
		}
		return Paths.get("..", "content", "npcs");
	}

	/** Loaded NPCs sorted by declared id. Empty if directory is missing. */
	public List<Entry> loadAll() {
		final List<Entry> entries = new ArrayList<>();
		final Path dir = resolveDir();

		if (!Files.isDirectory(dir)) {
			LOGGER.info("OGRS content/npcs/ not found at {} — skipping YAML NPC load", dir.toAbsolutePath());
			return entries;
		}

		final Yaml yaml = new Yaml();

		try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, "*.yaml")) {
			for (final Path file : stream) {
				try (InputStream in = Files.newInputStream(file)) {
					@SuppressWarnings("unchecked")
					final Map<String, Object> data = yaml.load(in);
					if (data == null) continue;
					final int id = ((Number) data.get("id")).intValue();
					final NPCDef def = buildDef(data, file.getFileName().toString());
					entries.add(new Entry(id, def, file.getFileName().toString()));
				} catch (final Exception e) {
					LOGGER.error("OGRS NPC YAML parse failed: " + file, e);
				}
			}
		} catch (final Exception e) {
			LOGGER.error("OGRS NPC YAML directory scan failed", e);
			return entries;
		}

		entries.sort(Comparator.comparingInt(e -> e.id));
		LOGGER.info("OGRS: loaded {} NPC YAML def(s) from {}", entries.size(), dir.toAbsolutePath());
		return entries;
	}

	/**
	 * Throws if {@code entries} (in declared-id order) cannot be appended to a
	 * list of {@code currentSize} elements while preserving id == index.
	 */
	public static void requireSequentialAfter(final List<Entry> entries, final int currentSize) {
		int expected = currentSize;
		for (final Entry e : entries) {
			if (e.id != expected) {
				throw new IllegalStateException(
					"OGRS NPC YAML id " + e.id + " in " + e.sourceFile
						+ " is not sequential — expected " + expected
						+ ". Until backlog #9 (EntityHandler HashMap refactor), YAML NPC ids "
						+ "must equal `npcs.size()` at the moment of load.");
			}
			expected++;
		}
	}

	private NPCDef buildDef(final Map<String, Object> data, final String filename) {
		final NPCDef def = new NPCDef();
		def.name = req(data, "name", filename);
		def.description = (String) data.getOrDefault("description", "");
		def.command1 = (String) data.getOrDefault("command", "");
		def.command2 = (String) data.getOrDefault("command2", "");

		@SuppressWarnings("unchecked")
		final Map<String, Object> stats = (Map<String, Object>) data.get("stats");
		def.attack = asInt(stats, "attack", 0);
		def.strength = asInt(stats, "strength", 0);
		def.hits = asInt(stats, "hits", 1);
		def.defense = asInt(stats, "defense", 0);
		def.ranged = asBool(stats, "ranged", false) ? 1 : 0;
		def.combatLevel = asInt(stats, "combat_level", 0);

		@SuppressWarnings("unchecked")
		final Map<String, Object> flags = (Map<String, Object>) data.getOrDefault("flags", java.util.Collections.emptyMap());
		def.members = asBool(flags, "members_only", false);
		def.attackable = asBool(flags, "attackable", false);
		def.aggressive = asBool(flags, "aggressive", false);

		def.respawnTime = asInt(data, "respawn_time_ticks", 211);

		@SuppressWarnings("unchecked")
		final List<Object> sprites = (List<Object>) data.get("sprites");
		if (sprites == null || sprites.size() != 12) {
			throw new IllegalArgumentException("`sprites` must be a 12-entry list in " + filename);
		}
		final int[] arr = new int[12];
		for (int i = 0; i < 12; i++) arr[i] = ((Number) sprites.get(i)).intValue();
		def.sprites = arr;

		@SuppressWarnings("unchecked")
		final Map<String, Object> colors = (Map<String, Object>) data.getOrDefault("colors", java.util.Collections.emptyMap());
		def.hairColour = asHexInt(colors, "hair", 0);
		def.topColour = asHexInt(colors, "top", 0);
		def.bottomColour = asHexInt(colors, "bottom", 0);
		def.skinColour = asHexInt(colors, "skin", 15523536);

		@SuppressWarnings("unchecked")
		final Map<String, Object> camera = (Map<String, Object>) data.getOrDefault("camera", java.util.Collections.emptyMap());
		def.camera1 = asInt(camera, "x", 160);
		def.camera2 = asInt(camera, "y", 220);

		@SuppressWarnings("unchecked")
		final Map<String, Object> models = (Map<String, Object>) data.getOrDefault("models", java.util.Collections.emptyMap());
		def.walkModel = asInt(models, "walk", 6);
		def.combatModel = asInt(models, "combat", 6);
		def.combatSprite = asInt(models, "combat_sprite", 5);
		def.roundMode = asInt(data, "round_mode", 0);

		return def;
	}

	private static String req(final Map<String, Object> m, final String key, final String filename) {
		final Object v = m.get(key);
		if (v == null) throw new IllegalArgumentException("`" + key + "` is required in " + filename);
		return v.toString();
	}

	private static int asInt(final Map<String, Object> m, final String key, final int fallback) {
		final Object v = (m == null) ? null : m.get(key);
		return v == null ? fallback : ((Number) v).intValue();
	}

	private static boolean asBool(final Map<String, Object> m, final String key, final boolean fallback) {
		final Object v = (m == null) ? null : m.get(key);
		return v == null ? fallback : (Boolean) v;
	}

	/** Accepts decimal int, or hex (0xAAAAAA / 0XAAAAAA). */
	private static int asHexInt(final Map<String, Object> m, final String key, final int fallback) {
		final Object v = (m == null) ? null : m.get(key);
		if (v == null) return fallback;
		if (v instanceof Number) return ((Number) v).intValue();
		final String s = v.toString().trim();
		if (s.startsWith("0x") || s.startsWith("0X")) return Integer.parseUnsignedInt(s.substring(2), 16);
		return Integer.parseInt(s);
	}
}

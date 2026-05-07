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
 * OGRS content-pipeline scenery (GameObject) loader. Sibling of
 * {@link OgrsContentNpcLoader} for {@link GameObjectDef}s.
 *
 * Reads {@code <repo>/content/scenery/*.yaml}, parses each into a
 * {@link GameObjectDef}, returns the list sorted by declared id.
 *
 * Hook point: {@link EntityHandler}'s scenery load (XML
 * {@code GameObjectDef.xml} → array). After the XML loads, append
 * the YAML-defined scenery so id == index alignment holds. Until a
 * HashMap-backed GameObject registry refactor, declared ids must be
 * sequential after the XML count.
 *
 * Schema (see content/scenery/allotment_patch.yaml for a worked example):
 * <pre>
 * id: 1296                           # next sequential after upstream XML
 * name: Allotment Patch              # required
 * description: A patch of cleared earth, ready for seeds.
 * command1: "Rake"                   # right-click primary
 * command2: "Examine"                # right-click secondary
 * type: 1                            # 0/1/2/3 — 1 is traversal-blocking
 * width: 1
 * height: 1
 * ground_item_var: 0
 * model: wheat                       # client-side model name. For MVP we
 *                                    # reuse existing model strings until
 *                                    # the asset pipeline is ready.
 * </pre>
 *
 * Path resolution: {@code ../content/scenery/} from the server cwd.
 * Override with {@code -Dogrs.content.dir=...}.
 */
public class OgrsContentSceneryLoader {

	private static final Logger LOGGER = LogManager.getLogger(OgrsContentSceneryLoader.class);

	public static final class Entry {
		public final int id;
		public final GameObjectDef def;
		public final String sourceFile;
		Entry(int id, GameObjectDef def, String sourceFile) {
			this.id = id;
			this.def = def;
			this.sourceFile = sourceFile;
		}
	}

	private static Path resolveDir() {
		final String override = System.getProperty("ogrs.content.dir");
		if (override != null && !override.isEmpty()) {
			return Paths.get(override, "scenery");
		}
		return Paths.get("..", "content", "scenery");
	}

	public List<Entry> loadAll() {
		final List<Entry> entries = new ArrayList<>();
		final Path dir = resolveDir();
		if (!Files.isDirectory(dir)) {
			LOGGER.info("OGRS content/scenery/ not found at {} — skipping YAML scenery load", dir.toAbsolutePath());
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
					final GameObjectDef def = buildDef(data, file.getFileName().toString());
					entries.add(new Entry(id, def, file.getFileName().toString()));
				} catch (final Exception e) {
					LOGGER.error("OGRS scenery YAML parse failed: " + file, e);
				}
			}
		} catch (final Exception e) {
			LOGGER.error("OGRS scenery YAML directory scan failed", e);
			return entries;
		}

		entries.sort(Comparator.comparingInt(e -> e.id));
		LOGGER.info("OGRS: loaded {} scenery YAML def(s) from {}", entries.size(), dir.toAbsolutePath());
		return entries;
	}

	public static void requireSequentialAfter(final List<Entry> entries, final int currentSize) {
		int expected = currentSize;
		for (final Entry e : entries) {
			if (e.id != expected) {
				throw new IllegalStateException(
					"OGRS scenery YAML id " + e.id + " in " + e.sourceFile
						+ " is not sequential — expected " + expected
						+ ". Until a HashMap-backed GameObject registry exists, scenery ids "
						+ "must equal `gameObjects.length` at the moment of YAML load.");
			}
			expected++;
		}
	}

	private GameObjectDef buildDef(final Map<String, Object> data, final String filename) {
		final GameObjectDef def = new GameObjectDef();
		def.name = req(data, "name", filename);
		def.description = (String) data.getOrDefault("description", "");
		def.command1 = (String) data.getOrDefault("command1", "WalkTo");
		def.command2 = (String) data.getOrDefault("command2", "Examine");
		def.type = ((Number) data.getOrDefault("type", 1)).intValue();
		def.width = ((Number) data.getOrDefault("width", 1)).intValue();
		def.height = ((Number) data.getOrDefault("height", 1)).intValue();
		def.groundItemVar = ((Number) data.getOrDefault("ground_item_var", 0)).intValue();
		def.objectModel = req(data, "model", filename);
		return def;
	}

	private static String req(final Map<String, Object> m, final String key, final String filename) {
		final Object v = m.get(key);
		if (v == null) throw new IllegalArgumentException("`" + key + "` is required in " + filename);
		return v.toString();
	}
}

package com.openrsc.server.external;

import com.openrsc.server.ServerConfiguration;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.lang.reflect.Field;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

/**
 * OGRS content-pipeline skills loader.
 *
 * Reads {@code <repo>/content/skills/*.yaml}, parses each into a
 * {@link SkillDef}, and returns the list sorted by declared id. Hooked
 * into {@link com.openrsc.server.constants.Skills} after the upstream
 * hardcoded skill list (so YAML skills land at the next available indices).
 *
 * Stock skills (Attack..Thieving) and the existing flag-gated extras
 * (Runecraft, Harvesting, Slayer) STAY hardcoded for now. Migrating them
 * to YAML is mechanical follow-up work — this loader only handles
 * additions on top.
 *
 * Schema (see content/skills/farming.yaml for a worked example):
 * <pre>
 * id: 19                     # numeric skill index — must be sequential
 *                            # after the last hardcoded skill.
 * name: Farming              # required
 * short_name: Farming        # optional; defaults to name
 * long_name: Farming         # optional; defaults to name
 * min_level: 1               # optional; defaults to 1
 * max_level: 99              # optional; defaults to 99 (contract)
 * exp_curve: ORIGINAL        # optional; defaults to ORIGINAL
 * want_flag: WANT_FARMING    # optional; if set, skill loads only when
 *                            # ServerConfiguration.WANT_FARMING is true
 * </pre>
 *
 * Path resolution: {@code ../content/skills/} from the server's working
 * directory (server/ when run via Gradle's application plugin). Override
 * with JVM property {@code -Dogrs.content.dir=...}.
 */
public class SkillsContentLoader {

	private static final Logger LOGGER = LogManager.getLogger(SkillsContentLoader.class);

	private static Path resolveDir() {
		final String override = System.getProperty("ogrs.content.dir");
		if (override != null && !override.isEmpty()) {
			return Paths.get(override, "skills");
		}
		return Paths.get("..", "content", "skills");
	}

	/**
	 * Loads all YAML skills, applies want_flag gating against the supplied
	 * ServerConfiguration, sorts by declared id, validates sequential ids
	 * after {@code currentSkillIndex}, and returns the qualified SkillDef list.
	 * Empty list if directory missing or all entries are flag-gated off.
	 */
	public static List<SkillDef> loadAll(final ServerConfiguration config, final int currentSkillIndex) {
		final Path dir = resolveDir();
		if (!Files.isDirectory(dir)) {
			LOGGER.info("OGRS content/skills/ not found at {} — skipping YAML skill load", dir.toAbsolutePath());
			return new ArrayList<>();
		}

		final List<int[]> idsByOrder = new ArrayList<>();   // [id, listIdx]
		final List<Map<String, Object>> rawByOrder = new ArrayList<>();
		final List<String> sourceFiles = new ArrayList<>();
		final Yaml yaml = new Yaml();

		try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, "*.yaml")) {
			for (final Path file : stream) {
				try (InputStream in = Files.newInputStream(file)) {
					@SuppressWarnings("unchecked")
					final Map<String, Object> data = yaml.load(in);
					if (data == null) continue;
					if (!data.containsKey("id") || !data.containsKey("name")) {
						LOGGER.error("OGRS skill YAML missing id/name — skipped: {}", file.getFileName());
						continue;
					}
					if (!flagAllows(config, data)) {
						LOGGER.info("OGRS skill {} gated off by want_flag — skipping", data.get("name"));
						continue;
					}
					idsByOrder.add(new int[]{((Number) data.get("id")).intValue(), idsByOrder.size()});
					rawByOrder.add(data);
					sourceFiles.add(file.getFileName().toString());
				} catch (final Exception e) {
					LOGGER.error("OGRS skill YAML parse failed: " + file, e);
				}
			}
		} catch (final Exception e) {
			LOGGER.error("OGRS skill YAML directory scan failed", e);
			return new ArrayList<>();
		}

		idsByOrder.sort(Comparator.comparingInt(a -> a[0]));

		// Validate sequential ids after currentSkillIndex.
		int expected = currentSkillIndex;
		final List<SkillDef> out = new ArrayList<>(idsByOrder.size());
		for (final int[] pair : idsByOrder) {
			final int id = pair[0];
			final int origIdx = pair[1];
			final Map<String, Object> data = rawByOrder.get(origIdx);
			if (id != expected) {
				throw new IllegalStateException(
					"OGRS skill YAML id " + id + " in " + sourceFiles.get(origIdx)
						+ " is not sequential — expected " + expected
						+ ". Skill ids must equal `current skill registry size at YAML-load time`.");
			}
			out.add(buildDef(data, expected, sourceFiles.get(origIdx)));
			expected++;
		}

		LOGGER.info("OGRS: loaded {} skill YAML def(s) from {}", out.size(), dir.toAbsolutePath());
		return out;
	}

	private static boolean flagAllows(final ServerConfiguration config, final Map<String, Object> data) {
		final Object raw = data.get("want_flag");
		if (raw == null) return true; // no flag = always-on
		final String flagName = raw.toString();
		try {
			final Field f = ServerConfiguration.class.getField(flagName);
			final Object value = f.get(config);
			if (!(value instanceof Boolean)) {
				LOGGER.warn("OGRS skill want_flag {} is not a boolean field — treating as always-on", flagName);
				return true;
			}
			return (Boolean) value;
		} catch (final NoSuchFieldException e) {
			LOGGER.error("OGRS skill want_flag {} doesn't exist on ServerConfiguration — skipping skill", flagName);
			return false;
		} catch (final IllegalAccessException e) {
			LOGGER.error("OGRS skill want_flag {} not accessible — treating as always-on", flagName);
			return true;
		}
	}

	private static SkillDef buildDef(final Map<String, Object> data, final int id, final String filename) {
		final String name = (String) data.get("name");
		final String shortName = (String) data.getOrDefault("short_name", name);
		final String longName = (String) data.getOrDefault("long_name", name);
		final int minLevel = ((Number) data.getOrDefault("min_level", 1)).intValue();
		final int maxLevel = ((Number) data.getOrDefault("max_level", 99)).intValue();
		final String curveName = (String) data.getOrDefault("exp_curve", "ORIGINAL");
		final SkillDef.EXP_CURVE curve;
		try {
			curve = SkillDef.EXP_CURVE.valueOf(curveName);
		} catch (final IllegalArgumentException e) {
			throw new IllegalArgumentException("Unknown exp_curve `" + curveName + "` in " + filename);
		}
		return new SkillDef(longName, shortName, minLevel, maxLevel, curve, id);
	}
}

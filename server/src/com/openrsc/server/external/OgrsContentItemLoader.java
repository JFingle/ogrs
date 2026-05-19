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
 * OGRS content-pipeline ITEM loader.
 *
 * Reads {@code <repo>/content/items/*.yaml}, parses each into an
 * {@link ItemDefinition}, and returns the list in declared-id order.
 * Hooked into {@link EntityHandler#load()} after the upstream JSON
 * loaders + patches so YAML-defined items are appended to the same
 * {@code items} ArrayList. This is the third leg of the OGRS content
 * pipeline (NPCs + scenery were the first two; same shape).
 *
 * Constraint: declared ids must be sequential starting at the items
 * list size at the moment of YAML load — i.e. the next item after
 * upstream's tail (Boomstick = 1592). Client-side {@code getItemDef}
 * gates on {@code id < items.size()}, so a contiguous run keeps the
 * default-fallback path off our items.
 *
 * Sprite handling is client-only — the server only persists numeric
 * defs; sprite IDs are picked in YAML and consumed by the Python
 * codegen that emits {@code OgrsClientItems.java}.
 *
 * Schema (see {@code content/items/rake.yaml} for a worked example):
 * <pre>
 * id: 1593
 * name: Rake
 * description: Pulls weeds from fresh allotment soil.
 * command: ""              # left-click verb (or "")
 * stackable: false
 * untradeable: false
 * members_only: false
 * noteable: true
 * base_price: 12
 * picture_mask: 0xC4895E   # client tint
 * sprite: { id: 96, location: "items:96" }
 * </pre>
 */
public class OgrsContentItemLoader {

	private static final Logger LOGGER = LogManager.getLogger(OgrsContentItemLoader.class);

	/** A loaded item: declared id + parsed def + sprite hints for client
	 *  codegen + optional metadata (eat heals, etc) for engine-side hooks. */
	public static final class Entry {
		public final int id;
		public final ItemDefinition def;
		public final int spriteId;
		public final String spriteLocation;
		public final int pictureMask;
		/** HP restored when eaten. 0 = not edible. Wired into upstream's
		 *  itemEdibleHeals map by EntityHandler so the standard Eating
		 *  plugin handles the eat verb without OGRS-specific code. */
		public final int eatHeals;
		public final String sourceFile;
		Entry(int id, ItemDefinition def, int spriteId, String spriteLocation, int pictureMask, int eatHeals, String sourceFile) {
			this.id = id;
			this.def = def;
			this.spriteId = spriteId;
			this.spriteLocation = spriteLocation;
			this.pictureMask = pictureMask;
			this.eatHeals = eatHeals;
			this.sourceFile = sourceFile;
		}
	}

	private static Path resolveDir() {
		final String override = System.getProperty("ogrs.content.dir");
		if (override != null && !override.isEmpty()) {
			return Paths.get(override, "items");
		}
		return Paths.get("..", "content", "items");
	}

	public List<Entry> loadAll() {
		final List<Entry> entries = new ArrayList<>();
		final Path dir = resolveDir();
		if (!Files.isDirectory(dir)) {
			LOGGER.info("OGRS content/items/ not found at {} — skipping YAML item load", dir.toAbsolutePath());
			return entries;
		}

		final Yaml yaml = new Yaml();
		try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, "*.yaml")) {
			for (final Path file : stream) {
				try (InputStream in = Files.newInputStream(file)) {
					@SuppressWarnings("unchecked")
					final Map<String, Object> data = yaml.load(in);
					if (data == null) continue;
					entries.add(buildEntry(data, file.getFileName().toString()));
				} catch (final Exception e) {
					LOGGER.error("OGRS item YAML parse failed: " + file, e);
				}
			}
		} catch (final Exception e) {
			LOGGER.error("OGRS item YAML directory scan failed", e);
			return entries;
		}

		entries.sort(Comparator.comparingInt(e -> e.id));
		LOGGER.info("OGRS: loaded {} item YAML def(s) from {}", entries.size(), dir.toAbsolutePath());
		return entries;
	}

	public static void requireSequentialAfter(final List<Entry> entries, final int currentSize) {
		int expected = currentSize;
		for (final Entry e : entries) {
			if (e.id != expected) {
				throw new IllegalStateException(
					"OGRS item YAML id " + e.id + " in " + e.sourceFile
						+ " is not sequential — expected " + expected
						+ ". Items must be a contiguous run after upstream's tail.");
			}
			expected++;
		}
	}

	private Entry buildEntry(final Map<String, Object> data, final String filename) {
		final int id = ((Number) data.get("id")).intValue();
		final String name = req(data, "name", filename);
		final String description = (String) data.getOrDefault("description", "");
		final String commandStr = (String) data.getOrDefault("command", "");
		final String[] command = commandStr.split(",");

		// OGRS — wieldable + weapon-stat support (sparky 2026-05-19, #36).
		// Top-level keys for the simple "is it wieldable, at all" pair
		// (wieldable / wearable_id). Optional `weapon:` sub-block carries
		// the proper weapon stats — required skill/level for equipping,
		// aim/power bonuses, etc. All fields default to authentic-OpenRSC
		// values so existing pre-#36 YAMLs keep their old behavior.
		final boolean wieldable = asBool(data, "wieldable", false);
		final int topWearableId = asInt(data, "wearable_id", 0);

		@SuppressWarnings("unchecked")
		final Map<String, Object> weapon =
			(Map<String, Object>) data.getOrDefault("weapon", java.util.Collections.emptyMap());
		final int appearanceId   = asInt(weapon, "appearance_id", topWearableId);
		final int wearableId     = asInt(weapon, "wearable_id", topWearableId);
		final int wearSlot       = asInt(weapon, "wear_slot", 4);
		final int requiredLevel  = asInt(weapon, "required_level", 1);
		final int requiredSkill  = asInt(weapon, "required_skill", 0);
		final int armourBonus    = asInt(weapon, "armour_bonus", 0);
		final int weaponAimBonus = asInt(weapon, "aim_bonus", 0);
		final int weaponPowerBonus = asInt(weapon, "power_bonus", 0);
		final int magicBonus     = asInt(weapon, "magic_bonus", 0);
		final int prayerBonus    = asInt(weapon, "prayer_bonus", 0);

		final ItemDefinition def = new ItemDefinition(
			id,
			name,
			description,
			command,
			false,                                  // isFemaleOnly — none of MVP items
			asBool(data, "members_only", false),
			asBool(data, "stackable", false),
			asBool(data, "untradeable", false),
			wieldable,
			appearanceId,
			wearableId,
			wearSlot,
			requiredLevel,
			requiredSkill,
			(long) armourBonus,
			weaponAimBonus,
			weaponPowerBonus,
			magicBonus,
			prayerBonus,
			asInt(data, "base_price", 1),
			asBool(data, "noteable", true)
		);
		// Mirror the upstream loader: collapse single-empty command to null.
		if (def.getCommand() != null && def.getCommand().length == 1 && "".equals(def.getCommand()[0])) {
			def.nullCommand();
		}

		@SuppressWarnings("unchecked")
		final Map<String, Object> sprite = (Map<String, Object>) data.getOrDefault("sprite", java.util.Collections.emptyMap());
		final int spriteId = asInt(sprite, "id", 0);
		final String spriteLocation = (String) sprite.getOrDefault("location", "items:" + spriteId);

		final int pictureMask = asHexInt(data, "picture_mask", 0);
		final int eatHeals = asInt(data, "eat_heals", 0);

		return new Entry(id, def, spriteId, spriteLocation, pictureMask, eatHeals, filename);
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

	private static int asHexInt(final Map<String, Object> m, final String key, final int fallback) {
		final Object v = (m == null) ? null : m.get(key);
		if (v == null) return fallback;
		if (v instanceof Number) return ((Number) v).intValue();
		final String s = v.toString().trim();
		if (s.startsWith("0x") || s.startsWith("0X")) return Integer.parseUnsignedInt(s.substring(2), 16);
		return Integer.parseInt(s);
	}
}

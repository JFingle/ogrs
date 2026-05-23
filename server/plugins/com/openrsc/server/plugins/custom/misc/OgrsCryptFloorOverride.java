package com.openrsc.server.plugins.custom.misc;

import com.google.inject.Inject;
import com.openrsc.server.model.world.World;
import com.openrsc.server.model.world.region.TileValue;
import com.openrsc.server.plugins.triggers.StartupTrigger;
import com.openrsc.server.util.rsc.CollisionFlag;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * OGRS — Lumbridge Crypt floor walkability fix.
 *
 * The crypt sits at plane-3 Y 3700-3741 — inside the loaded landscape
 * band, but the authentic tile data at this X/Y has groundOverlay set
 * to a non-walkable type (rock/void). WorldLoader honors that by OR'ing
 * FULL_BLOCK into every tile's traversalMask, so the player and NPCs
 * can't move at all once they're inside the chamber.
 *
 * Rather than rewrite the landscape archive, this startup hook walks
 * the chamber interior tiles and clears the FULL_BLOCK bits, leaving
 * any wall-edge flags intact (those are set separately by the
 * boundary loader once OGRS walls are placed). Result: a walkable
 * dungeon floor without touching upstream tile data.
 *
 * Boxes here MUST match the interior coordinates of the chambers
 * defined in BoundaryLocsCustom.json and SceneryLocsCustom.json.
 */
public class OgrsCryptFloorOverride implements StartupTrigger {

	private static final Logger LOGGER = LogManager.getLogger(OgrsCryptFloorOverride.class);

	/** Path to the walkable-tile JSON produced by tools/gen_crypt_v4.py.
	 *  Format: [[x, y], [x, y], ...] — every walkable crypt tile.
	 *  Loading from JSON lets us use irregular shapes (L-rooms, pillars,
	 *  octagons) without enumerating rectangles in code. */
	private static final String CRYPT_TILES_JSON = "./conf/server/defs/locs/OgrsCryptWalkable.json";

	private final World world;

	@Inject
	public OgrsCryptFloorOverride(final World world) {
		this.world = world;
	}

	@Override
	public void onStartup() {
		int cleared = 0;
		int blockMask = CollisionFlag.FULL_BLOCK | CollisionFlag.OBJECT;
		final java.util.List<int[]> tiles = loadWalkableTiles();
		for (int[] xy : tiles) {
			if (!world.withinWorld(xy[0], xy[1])) continue;
			final TileValue tv = world.getTile(xy[0], xy[1]);
			if (tv == null) continue;
			tv.traversalMask = (byte) (tv.traversalMask & ~blockMask);
			cleared++;
		}
		LOGGER.info("OGRS: Lumbridge Crypt floor override — cleared FULL_BLOCK|OBJECT on {} tiles", cleared);
	}

	private static java.util.List<int[]> loadWalkableTiles() {
		final java.util.List<int[]> out = new java.util.ArrayList<>();
		try (java.io.InputStream in = new java.io.FileInputStream(CRYPT_TILES_JSON)) {
			java.io.ByteArrayOutputStream b = new java.io.ByteArrayOutputStream();
			byte[] buf = new byte[8192];
			int n;
			while ((n = in.read(buf)) > 0) b.write(buf, 0, n);
			String src = b.toString("UTF-8");
			int i = 0;
			while ((i = src.indexOf('[', i + 1)) >= 0) {
				int comma = src.indexOf(',', i);
				int close = src.indexOf(']', i);
				if (comma < 0 || close < 0 || comma > close) continue;
				try {
					int x = Integer.parseInt(src.substring(i + 1, comma).trim());
					int y = Integer.parseInt(src.substring(comma + 1, close).trim());
					out.add(new int[]{x, y});
				} catch (NumberFormatException ignore) { }
			}
		} catch (Exception e) {
			LOGGER.warn("OGRS Crypt floor override: failed to load walkable tile JSON: " + e.getMessage());
		}
		return out;
	}

	@Override
	public boolean blockStartup() {
		// Return true so PluginHandler invokes our onStartup. The trigger
		// pattern only fires plugin actions when blockXxx returns true;
		// returning false delegates to the no-op Default handler.
		return true;
	}
}

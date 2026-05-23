package com.openrsc.server.io;

import com.openrsc.server.ServerConfiguration;
import com.openrsc.server.constants.Constants;
import com.openrsc.server.database.WorldPopulator;
import com.openrsc.server.model.world.World;
import com.openrsc.server.model.world.region.Region;
import com.openrsc.server.model.world.region.RegionManager;
import com.openrsc.server.model.world.region.TileValue;
import com.openrsc.server.util.rsc.DataConversions;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.BufferedInputStream;
import java.io.File;
import java.nio.ByteBuffer;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public class WorldLoader {
	/**
	 * The asynchronous logger.
	 */
	private static final Logger LOGGER = LogManager.getLogger();

	private static final int[] ALLOWED_WALL_ID_TYPES = {5, 6, 14, 42, 63, 128, 229, 230};

	private JContent jagArchive;
	private JContent memArchive;
	private JContent landJagArchive;
	private JContent landMemArchive;
	private ZipFile tileArchive;
	private final World world;
	private final WorldPopulator worldPopulator;

	public WorldLoader(final World world) {
		this.world = world;
		this.worldPopulator = new WorldPopulator(getWorld());
	}

	/** OGRS — cache of (x<<32)|y keys for crypt walkable tiles. Loaded lazily
	 *  from conf/server/defs/locs/OgrsCryptWalkable.json which is regenerated
	 *  by tools/gen_crypt_v4.py. Lets the WorldLoader synth handle irregular
	 *  chamber shapes without listing rectangles in code. */
	private static volatile java.util.Set<Long> ogrsCryptWalkableCache;

	private static java.util.Set<Long> ogrsLoadCryptWalkable() {
		java.util.Set<Long> cached = ogrsCryptWalkableCache;
		if (cached != null) return cached;
		final java.util.Set<Long> set = new java.util.HashSet<>();
		try (java.io.InputStream in = new java.io.FileInputStream(
				"./conf/server/defs/locs/OgrsCryptWalkable.json")) {
			java.io.ByteArrayOutputStream b = new java.io.ByteArrayOutputStream();
			byte[] buf = new byte[8192];
			int n;
			while ((n = in.read(buf)) > 0) b.write(buf, 0, n);
			String src = b.toString("UTF-8");
			// Cheap parse: [[x,y],[x,y],...] — no nested objects.
			int i = 0;
			while ((i = src.indexOf('[', i + 1)) >= 0) {
				int comma = src.indexOf(',', i);
				int close = src.indexOf(']', i);
				if (comma < 0 || close < 0 || comma > close) continue;
				try {
					int x = Integer.parseInt(src.substring(i + 1, comma).trim());
					int y = Integer.parseInt(src.substring(comma + 1, close).trim());
					set.add((((long) x) << 32) | (y & 0xffffffffL));
				} catch (NumberFormatException ignore) { }
			}
		} catch (Exception e) {
			LOGGER.warn("OGRS: failed to load OgrsCryptWalkable.json: " + e.getMessage());
		}
		ogrsCryptWalkableCache = set;
		return set;
	}

	private static boolean projectileClipAllowed(final int wallID) {
		for (final int allowedWallIdType : ALLOWED_WALL_ID_TYPES) {
			if (allowedWallIdType == wallID) {
				return true;
			}
		}
		return false;
	}

	private Sector loadJAGSector(final int sectionX, final int sectionY, final int height, boolean altFormat)
	{
		String mapName = "m" + height + sectionX / 10 + sectionX % 10 + sectionY / 10 + sectionY % 10;

		int size = Constants.REGION_SIZE * Constants.REGION_SIZE;
		byte[] terrainHeight = new byte[size];
		byte[] terrainColour = new byte[size];
		byte[] wallsEastWest = new byte[size];
		byte[] wallsNorthSouth = new byte[size];
		int[] wallsDiagonal = new int[size];
		byte[] wallsRoof = new byte[size];
		byte[] tileDecoration = new byte[size];
		byte[] tileDirection = new byte[size];
		int lastVal = 0;

		JContentFile jmFile = jagArchive.unpack(mapName + ".jm");
		JContentFile datFile = jagArchive.unpack(mapName + ".dat");
		JContentFile heiFile = null;
		if (landJagArchive != null)
			heiFile = landJagArchive.unpack(mapName + ".hei");
		JContentFile locFile = jagArchive.unpack(mapName + ".loc");

		if (memArchive != null && getWorld().getServer().getConfig().MEMBER_WORLD) {
			JContentFile memberJM = memArchive.unpack(mapName + ".jm");
			JContentFile memberDat = memArchive.unpack(mapName + ".dat");
			JContentFile memberHei = null;
			if (landMemArchive != null)
				memberHei = landMemArchive.unpack(mapName + ".hei");
			if (memberDat != null)
				datFile = memberDat;
			if (memberJM != null)
				jmFile = memberJM;
			if (memberHei != null)
				heiFile = memberHei;
		}

		// OGRS — plane-3 sectors that house the Lumbridge Crypt. v4 layout
		// spans h3x50y55 (main dungeon) and h3x51y55 (Spider Vault east
		// edge — X=144). Neither has authored .jm/.dat in maps64.jag, so
		// the upstream loader returns null. We synthesize a sector with
		// cave-floor for chamber tiles + void elsewhere.
		final boolean isOgrsCryptSector = (height == 3
			&& ((sectionX == 50 && sectionY == 55)
			 || (sectionX == 51 && sectionY == 55)));

		if (jmFile == null && datFile == null) {
			if (!isOgrsCryptSector) return null;
			// Load the walkable tile set from the generator's JSON output.
			// This lets us use irregular room shapes (L, octagon, diamond,
			// pillar-bearing halls) without enumerating rectangles in Java.
			java.util.Set<Long> ogrsWalkable = ogrsLoadCryptWalkable();
			// OGRS crypt sector synthesis. ROOT CAUSE of "no floor" issue:
			// overlay=8 maps to TileDef[7].colour=12345678, which is the
			// Scene.TRANSPARENT sentinel — the client's renderer skips
			// face insertion for transparent tiles, so no floor renders.
			// Swamp cave works in spite of this because its tiles have
			// wall data baked in that triggers a fallback edge-blend
			// rendering path. We can't use that for a clean chamber.
			//
			// Solution: overlay=5 (TileDef[4]) — colour=-16913 (cave moss
			// green), walkable, tileValue=2. This is the most common cave
			// dirt-floor overlay in plane-3 across the whole RSC world
			// (6851 tiles in authentic data, used in deep caves). Renders
			// as proper dirt/cavern floor texture. Outside-chamber tiles
			// keep overlay=8 (TRANSPARENT, blocked) so the sector edges
			// stay invisible void.
			Sector synth = new Sector();
			final int sectorWorldX = sectionX * Constants.REGION_SIZE - 2304;
			final int sectorWorldY = sectionY * Constants.REGION_SIZE - 1776 + (height * 944);
			for (int x = 0; x < Constants.REGION_SIZE; x++) {
				for (int y = 0; y < Constants.REGION_SIZE; y++) {
					Tile t = new Tile();
					final int wx = sectorWorldX + x;
					final int wy = sectorWorldY + y;
					boolean inChamber = ogrsWalkable != null
						&& ogrsWalkable.contains((((long) wx) << 32) | (wy & 0xffffffffL));
					t.groundElevation = 0;
					t.groundTexture = inChamber ? (byte) 70 : 0;
					t.groundOverlay = inChamber ? (byte) 5 : (byte) 8;
					t.roofTexture = 0;
					t.horizontalWall = 0;
					t.verticalWall = 0;
					t.diagonalWalls = 0;
					synth.setTile(x, y, t);
				}
			}
			return synth;
		}

		if (datFile != null) {
			if (altFormat) {
				for (int i = 0; i < size; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						wallsEastWest[i++] = (byte) val;
					} else {
						for (int x = 0; x < val - 128; x++)
							wallsEastWest[i++] = 0;
					}
				}

				for (int i = 0; i < size; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						wallsNorthSouth[i++] = (byte) val;
					} else {
						for (int x = 0; x < val - 128; x++)
							wallsNorthSouth[i++] = 0;
					}
				}

				for (int i = 0; i < size; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						wallsDiagonal[i++] = val;
					} else {
						for (int x = 0; x < val - 128; x++)
							wallsDiagonal[i++] = 0;
					}
				}

				for (int i = 0; i < size; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						wallsDiagonal[i++] = val + 12000;
					} else {
						i += val - 128;
					}
				}

				for (int i = 0; i < size; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						wallsRoof[i++] = (byte)val;
					} else {
						for (int x = 0; x < val - 128; x++)
							wallsRoof[i++] = 0;
					}
				}

				for (int i = 0; i < size; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						tileDecoration[i++] = (byte)val;
					} else {
						for (int x = 0; x < val - 128; x++)
							tileDecoration[i++] = 0;
					}
				}

				for (int i = 0; i < size; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						tileDirection[i++] = (byte)val;
					} else {
						for (int x = 0; x < val - 128; x++)
							tileDirection[i++] = 0;
					}
				}
			} else {
				for (int i = 0; i < size; i++)
					wallsEastWest[i] = datFile.readByte();
				for (int i = 0; i < size; i++)
					wallsNorthSouth[i] = datFile.readByte();
				for (int i = 0; i < size; i++)
					wallsDiagonal[i] = datFile.readUnsignedByte();

				for (int i = 0; i < size; i++) {
					int val = datFile.readUnsignedByte();
					if (val > 0)
						wallsDiagonal[i] = val + 12000;
				}

				for (int tile = 0; tile < 2304; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						wallsRoof[tile++] = (byte) val;
					} else {
						for (int i = 0; i < val - 128; i++)
							wallsRoof[tile++] = 0;
					}
				}

				lastVal = 0;
				for (int tile = 0; tile < 2304; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						tileDecoration[tile++] = (byte) val;
						lastVal = val;
					} else {
						for (int i = 0; i < val - 128; i++)
							tileDecoration[tile++] = (byte) lastVal;
					}
				}

				for (int tile = 0; tile < 2304; ) {
					int val = datFile.readUnsignedByte();
					if (val < 128) {
						tileDirection[tile++] = (byte) val;
					} else {
						for (int i = 0; i < val - 128; i++)
							tileDirection[tile++] = 0;
					}
				}
			}
		} else {
			// Plane-3 sectors with no .dat file default to decoration=8
			// (dark blocked rock). The OGRS crypt sector is handled
			// separately via early-return at the top of this method; here
			// we keep the authentic upstream behaviour intact.
			for (int tile = 0; tile < 2304; tile++) {
				wallsNorthSouth[tile] = 0;
				wallsEastWest[tile] = 0;
				wallsDiagonal[tile] = 0;
				wallsRoof[tile] = 0;
				tileDecoration[tile] = 0;
				if (height == 0)
					tileDecoration[tile] = -6;
				if (height == 3)
					tileDecoration[tile] = 8;
				tileDirection[tile] = 0;
			}

			if (locFile != null) {
				for (int tile = 0; tile < size;) {
					int val = locFile.readUnsignedByte();
					if (val < 128) {
						wallsDiagonal[(tile++)] = val + 48000;
					} else {
						tile += val - 128;
					}
				}
			}
		}

		if (heiFile != null) {
			for (int tile = 0; tile < 2304; ) {
				int val = heiFile.readUnsignedByte();
				if (val < 128) {
					terrainHeight[tile++] = (byte) val;
					lastVal = val;
				}
				if (val >= 128) {
					for (int i = 0; i < val - 128; i++)
						terrainHeight[tile++] = (byte) lastVal;
				}
			}

			lastVal = 64;
			for (int tileY = 0; tileY < 48; tileY++) {
				for (int tileX = 0; tileX < 48; tileX++) {
					lastVal = terrainHeight[tileX * 48 + tileY] + lastVal & 0x7f;
					terrainHeight[tileX * 48 + tileY] = (byte) (lastVal * 2);
				}
			}

			lastVal = 0;
			for (int tile = 0; tile < 2304; ) {
				int val = heiFile.readUnsignedByte();
				if (val < 128) {
					terrainColour[tile++] = (byte) val;
					lastVal = val;
				}
				if (val >= 128) {
					for (int i = 0; i < val - 128; i++)
						terrainColour[tile++] = (byte) lastVal;
				}
			}

			lastVal = 35;
			for (int tileY = 0; tileY < 48; tileY++) {
				for (int tileX = 0; tileX < 48; tileX++) {
					lastVal = terrainColour[tileX * 48 + tileY] + lastVal & 0x7f;
					terrainColour[tileX * 48 + tileY] = (byte) (lastVal * 2);
				}

			}
		} else {
			for (int tile = 0; tile < 2304; tile++) {
				terrainHeight[tile] = 0;
				terrainColour[tile] = 0;
			}
		}

		if (jmFile != null)
		{
			int val = 0;
			for (int i = 0; i < size; i++) {
				val = val + jmFile.readUnsignedByte();
				terrainHeight[i] = (byte)val;
			}

			val = 0;
			for (int i = 0; i < size; i++) {
				val = val + jmFile.readUnsignedByte();
				terrainColour[i] = (byte)val;
			}

			for (int i = 0; i < size; i++)
				wallsEastWest[i] = jmFile.readByte();

			for (int i = 0; i < size; i++)
				wallsNorthSouth[i] = jmFile.readByte();

			for (int i = 0; i < size; i++) {
				wallsDiagonal[i] = jmFile.readUnsignedByte() * 256 + jmFile.readUnsignedByte();
			}

			for (int i = 0; i < size; i++)
				wallsRoof[i] = jmFile.readByte();

			for (int i = 0; i < size; i++)
				tileDecoration[i] = jmFile.readByte();

			for (int i = 0; i < size; i++)
				tileDirection[i] = jmFile.readByte();
		}

		Sector s = new Sector();
		for (int x = 0; x < Constants.REGION_SIZE; x++)
		{
			for (int y = 0; y < Constants.REGION_SIZE; y++)
			{
				int index = (x * Constants.REGION_SIZE) + y;

				Tile tile = new Tile();
				tile.groundElevation = terrainHeight[index];
				tile.diagonalWalls = (short)wallsDiagonal[index];
				tile.verticalWall = wallsNorthSouth[index];
				tile.horizontalWall = wallsEastWest[index];
				tile.roofTexture = wallsRoof[index];

				// ??? Not 100% on these
				tile.groundOverlay = tileDecoration[index];
				tile.groundTexture = terrainColour[index];
				s.setTile(index, tile);
			}
		}
		return s;
	}

	private boolean loadSection(final int sectionX, final int sectionY, final int height, final int bigX, final int bigY) {
		Sector s = null;

		if (jagArchive != null || memArchive != null || landJagArchive != null || landMemArchive != null) {
			// Load from members first, if fails, load f2p, if fails, we couldn't load sector.
			// This is official via client world loader
			boolean useAltLoader = getWorld().getServer().getConfig().BASED_MAP_DATA >= 28 && getWorld().getServer().getConfig().BASED_MAP_DATA <= 62;
			s = loadJAGSector(sectionX, sectionY, height, useAltLoader);
			if (s == null)
				return false;
		} else {
			try {
				final String filename = "h" + height + "x" + sectionX + "y" + sectionY;
				final ZipEntry e = tileArchive.getEntry(filename);
				if (e == null) {
					//LOGGER.warn("Ignoring Missing Sector: " + filename);
					return false;
				}
				final ByteBuffer data = DataConversions.streamToBuffer(new BufferedInputStream(tileArchive.getInputStream(e)));
				s = Sector.unpack(data);
			} catch (final Exception e) {
				LOGGER.catching(e);
			}
		}

		for (int y = 0; y < Constants.REGION_SIZE; y++) {
			for (int x = 0; x < Constants.REGION_SIZE; x++) {
				final int bx = bigX + x;
				final int by = bigY + y;

				if (!getWorld().withinWorld(bx, by)) {
					continue;
				}
				Tile sectorTile = s.getTile(x, y);
				TileValue tile = getWorld().getTile(bx, by);

				tile.overlay = sectorTile.groundOverlay;
				tile.diagWallVal = sectorTile.diagonalWalls;
				tile.horizontalWallVal = sectorTile.horizontalWall;
				tile.verticalWallVal = sectorTile.verticalWall;
				tile.elevation = sectorTile.groundElevation;
				tile.traversalMask = 0;

				if ((sectorTile.groundOverlay & 0xff) == 250) {
					sectorTile.groundOverlay = (byte) 2;
				}

				final byte groundOverlay = sectorTile.groundOverlay;
				if (groundOverlay > 0
					&& getWorld().getServer().getEntityHandler().getTileDef(groundOverlay - 1).getObjectType() != 0) {
					tile.traversalMask |= 0x40; // 64
				}

				final int verticalWall = sectorTile.verticalWall & 0xFF;
				if (verticalWall > 0
					&& getWorld().getServer().getEntityHandler().getDoorDef(verticalWall - 1).getUnknown() == 0
					&& getWorld().getServer().getEntityHandler().getDoorDef(verticalWall - 1).getDoorType() != 0) {
					getWorld().getTile(bx, by).traversalMask |= 1; // 1
					getWorld().getTile(bx, by - 1).traversalMask |= 4; // 4

					if (projectileClipAllowed(verticalWall)) {
						tile.projectileAllowed = true;
						tile.originalProjectileAllowed = true;
						getWorld().getTile(bx, by - 1).projectileAllowed = true;
						getWorld().getTile(bx, by - 1).originalProjectileAllowed = true;
					}
				}

				final int horizontalWall = sectorTile.horizontalWall & 0xFF;
				if (horizontalWall > 0
					&& getWorld().getServer().getEntityHandler().getDoorDef(horizontalWall - 1).getUnknown() == 0
					&& getWorld().getServer().getEntityHandler().getDoorDef(horizontalWall - 1).getDoorType() != 0) {
					tile.traversalMask |= 2; // 2
					getWorld().getTile(bx - 1, by).traversalMask |= 8; // 8
					if (projectileClipAllowed(horizontalWall)) {
						tile.projectileAllowed = true;
						tile.originalProjectileAllowed = true;
						getWorld().getTile(bx - 1, by).projectileAllowed = true;
						getWorld().getTile(bx - 1, by).originalProjectileAllowed = true;
					}
				}

				final int diagonalWalls = sectorTile.diagonalWalls;
				if (diagonalWalls > 0
					&& diagonalWalls < 12000
					&& getWorld().getServer().getEntityHandler().getDoorDef(diagonalWalls - 1).getUnknown() == 0
					&& getWorld().getServer().getEntityHandler().getDoorDef(diagonalWalls - 1).getDoorType() != 0) {
					tile.traversalMask |= 0x20; // 32
					if (projectileClipAllowed(diagonalWalls & 0xFF)) {
						tile.projectileAllowed = true;
						tile.originalProjectileAllowed = true;
					}
				}
				if (diagonalWalls > 12000
					&& diagonalWalls < 24000
					&& getWorld().getServer().getEntityHandler().getDoorDef(diagonalWalls - 12001).getUnknown() == 0
					&& getWorld().getServer().getEntityHandler().getDoorDef(diagonalWalls - 12001).getDoorType() != 0) {
					tile.traversalMask |= 0x10; // 16

					if (projectileClipAllowed(diagonalWalls & 0xFF)) {
						tile.projectileAllowed = true;
						tile.originalProjectileAllowed = true;
					}
				}

				if (tile.overlay == 2 || tile.overlay == 11) {
					tile.projectileAllowed = true;
					tile.originalProjectileAllowed = true;
				}
			}
		}
		return true;

	}

	public void loadWorld() {
		final long start = System.currentTimeMillis();
		final ServerConfiguration config = getWorld().getServer().getConfig();

		if (!config.WANT_CUSTOM_LANDSCAPE) {
			boolean useBZip2 = config.BASED_MAP_DATA >= 28; // Map versions 28+ use BZip2
			File fJag;
			File fMem;
			File fLandJag;
			File fLandMem;
			// Load official map files if found
			if (config.BASED_MAP_DATA == 100) {
				String mapDir = "./conf/server/data/maps/";
				fJag = new File(mapDir + "content4_ffffffffaaca2b0d"); // maps.jag
				fMem = new File(mapDir + "content5_6a1d6b00"); // maps.mem
				fLandJag = new File(mapDir + "content6_ffffffffe997514b"); // land.jag
				fLandMem = new File(mapDir + "content7_3fc5d9e3"); // land.mem
			} else {
				String mapFname = "./conf/server/data/maps/maps" + config.BASED_MAP_DATA;
				String landFname = "./conf/server/data/maps/land" + config.BASED_MAP_DATA;
				fJag = new File(mapFname + ".jag");
				fMem = new File(mapFname + ".mem");
				fLandJag = new File(landFname + ".jag");
				fLandMem = new File(landFname + ".mem");
			}
			if (fJag.exists()) {
				jagArchive = new JContent();
				if (!jagArchive.open(fJag.getAbsolutePath(), useBZip2))
					jagArchive = null;
			}
			if (fMem.exists()) {
				memArchive = new JContent();
				if (!memArchive.open(fMem.getAbsolutePath(), useBZip2))
					memArchive = null;
			}

			if (fLandJag.exists()) {
				landJagArchive = new JContent();
				if (!landJagArchive.open(fLandJag.getAbsolutePath(), useBZip2))
					landJagArchive = null;
			}

			if (fLandMem.exists()) {
				landMemArchive = new JContent();
				if (!landMemArchive.open(fLandMem.getAbsolutePath(), useBZip2))
					landMemArchive = null;
			}
		}

		if (jagArchive == null && memArchive == null) {
			try {
				File archiveFile;
				if (config.MEMBER_WORLD) {
					if (config.WANT_CUSTOM_LANDSCAPE) {
						archiveFile = new File("./conf/server/data/Custom_Landscape.orsc");
					} else {
						archiveFile = new File("./conf/server/data/Authentic_Landscape.orsc"); // Members landscape
					}
				} else {
					archiveFile = new File("./conf/server/data/F2PLandscape.orsc"); // Free landscape
				}
				tileArchive = new ZipFile(archiveFile);
				LOGGER.info("Loading landscape from " + archiveFile.getAbsolutePath());
			} catch (final Exception e) {
				LOGGER.catching(e);
			}
		}

		int sectors = 0;
		int FloorCount = 4;
		//Reluctant to use FloorHeight without knowing the effects
		int FloorHeight = Constants.MAX_HEIGHT / FloorCount;
		for (int lvl = 0; lvl < FloorCount; lvl++) {
			int wildX = 2304;
			int wildY = 1776 - (lvl * 944);
			for (int sx = 0; sx <= (Constants.MAX_WIDTH - Constants.REGION_SIZE); sx += Constants.REGION_SIZE) {
				for (int sy = 0; sy < 944; sy += Constants.REGION_SIZE) {
					int x = (sx + wildX) / Constants.REGION_SIZE;
					int y = (sy + (lvl * 944) + wildY) / Constants.REGION_SIZE;
					if (loadSection(x, y, lvl, sx, sy + (944 * lvl))) {
						sectors++;
					}
				}
			}
		}

		// Detect if all tiles in each Region are equal, and if so only store that fact rather than array of all tiles.
		// There are a lot of "null" sectors in the map file and storing tile values for all eats a lot of memory.
		// The authentic map file may have a way to flag null regions and only use one tile value across the entire thing
		// Unfortunately, the map files we are using currently do not support that feature so we need to detect
		// Unfortunately, we also have to allocate all the tiles and then clear them because the process of loading a sector can effect other sectors.
		// Downside is that Scenery/Boundary spawn can change tile values, and if one is spawned in a "null region," then we will not be able to change the tile value from the Scenery/Boundary spawn.

		final RegionManager regionManager = getWorld().getRegionManager();
		for (int lvl = 0; lvl < 4; lvl++) {
			for (int sx = 0; sx < 20; sx++) {
				for (int sy = 0; sy < 20; sy++) {
					final Region region = regionManager.getRegion(sx * Constants.REGION_SIZE, sy * Constants.REGION_SIZE + (Constants.REGION_SIZE * 20 * lvl));
					region.checkRegionValues();
				}
			}
		}

		LOGGER.info((System.currentTimeMillis() - start) + "ms to load landscape with " + sectors + " regions.");
	}

	public void unloadWorld() {
		tileArchive = null;
	}

	public World getWorld() {
		return world;
	}

	public WorldPopulator getWorldPopulator() {
		return worldPopulator;
	}
}

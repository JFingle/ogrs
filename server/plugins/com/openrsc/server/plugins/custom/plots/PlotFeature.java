package com.openrsc.server.plugins.custom.plots;

/**
 * OGRS — Built feature on a plot. Phase 1F-γ.
 *
 * One record per built feature. Each plot has up to tier.featureSlots()
 * features. Features are dynamically spawned GameObjects on the world
 * (via World.registerGameObject) keyed by their (x,y).
 *
 * v1 types: just BANK_CHEST. Forge / Portal / Farm Patch land in
 * follow-up commits once the Construction-skill furniture pipeline
 * lands.
 */
public final class PlotFeature {

	public enum Type {
		BANK_CHEST(1328, 30_000, 20, "Bank Chest"),
		FORGE     (1329, 80_000, 40, "Forge"),
		// PORTAL      (1330, 150_000, 50, "Portal Nexus"),
		// FARM_PATCH  (1331, 60_000, 30, "Farm Patch"),
		;
		public final int    sceneryId;
		public final int    goldCost;
		public final int    minConstructionLevel;
		public final String displayName;

		Type(final int sceneryId, final int goldCost, final int minConstructionLevel, final String displayName) {
			this.sceneryId = sceneryId;
			this.goldCost = goldCost;
			this.minConstructionLevel = minConstructionLevel;
			this.displayName = displayName;
		}
	}

	public final int  plotId;
	public final Type type;
	public final int  x, y;
	public final String builtBy;
	public final long builtAtMs;

	public PlotFeature(final int plotId, final Type type, final int x, final int y, final String builtBy) {
		this(plotId, type, x, y, builtBy, System.currentTimeMillis());
	}

	/** Persistence-side constructor that preserves the original
	 *  built-at timestamp when restoring from DB. */
	public PlotFeature(final int plotId, final Type type, final int x, final int y, final String builtBy, final long builtAtMs) {
		this.plotId = plotId;
		this.type = type;
		this.x = x;
		this.y = y;
		this.builtBy = builtBy;
		this.builtAtMs = builtAtMs;
	}
}

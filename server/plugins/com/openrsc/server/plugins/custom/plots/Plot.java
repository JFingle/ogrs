package com.openrsc.server.plugins.custom.plots;

import java.util.ArrayList;
import java.util.List;

/**
 * OGRS — Estate plot data record. Phase 1F-α of the housing/contract
 * arc (sparky 2026-05-24). In-memory; DB persistence in a later phase.
 *
 * Plots are FIXED locations in the world (not instances — sidesteps
 * the engine-level instancing work). Each has:
 *   - A defined enclosed area (boundingBox) inside which the deed
 *     holder can build (Construction skill required, materials cost).
 *   - A Deed Pillar scenery (id 1327) at the entry point. Players
 *     right-click → see plot info, owner, bid status.
 *   - A tier (BASIC / PREMIUM / WILDERNESS) gating feature unlocks.
 *
 * Tiers:
 *   BASIC      — 8×8 area, up to 4 buildable features.
 *   PREMIUM    — 12×12, up to 8 features. Higher auction floor.
 *   WILDERNESS — 16×16, up to 12 features. Guild-owned (deedHolder
 *                is a guild name, not a player). Raidable. Phase 2-γ
 *                wilderness work fills this in fully.
 *
 * Ownership:
 *   deedHolder = username (for BASIC/PREMIUM) or guild name (for
 *                WILDERNESS). null = vacant, open for bidding.
 *   tenancyExpiresMs = when the current tenancy ends (weekly auction
 *                cycle re-opens it).
 */
public final class Plot {

	public enum Tier {
		BASIC, PREMIUM, WILDERNESS;

		public int auctionFloor() {
			switch (this) {
				case BASIC:      return 50_000;
				case PREMIUM:    return 250_000;
				case WILDERNESS: return 1_000_000;
				default:         return 0;
			}
		}

		public int featureSlots() {
			switch (this) {
				case BASIC:      return 4;
				case PREMIUM:    return 8;
				case WILDERNESS: return 12;
				default:         return 0;
			}
		}
	}

	public final int    id;
	public final String name;        // human-friendly; e.g., "Lumbridge Market Plot"
	public final Tier   tier;
	public final int    deedPillarX;
	public final int    deedPillarY;
	public final int    boxMinX, boxMaxX, boxMinY, boxMaxY;  // buildable area
	public final String themeHint;   // flavor — coastal/urban/dungeon/sacred/etc.

	/** Current deed holder. Username for BASIC/PREMIUM, guild name for
	 *  WILDERNESS. null = vacant. */
	public String deedHolder = null;
	/** Tenancy expires here. After this, the plot re-opens for bidding. */
	public long   tenancyExpiresMs = 0;

	/** Open bids on this plot — username -> amount. Drained on auction
	 *  close (highest bidder wins, others refunded). */
	public final java.util.Map<String, Integer> openBids = new java.util.HashMap<>();

	/** Features built on this plot — Phase 1F-γ. Keyed by tile-packed
	 *  (x,y) so the OgrsPlotBank plugin can answer "what feature is at
	 *  this scenery, and is the user the deed holder?". */
	public final java.util.Map<Long, PlotFeature> features = new java.util.HashMap<>();

	public static long featureKey(final int x, final int y) {
		return (((long) x) << 32) | (y & 0xffffffffL);
	}

	public PlotFeature featureAt(final int x, final int y) {
		return features.get(featureKey(x, y));
	}

	public Plot(final int id, final String name, final Tier tier,
	            final int deedPillarX, final int deedPillarY,
	            final int boxMinX, final int boxMinY, final int boxMaxX, final int boxMaxY,
	            final String themeHint) {
		this.id = id;
		this.name = name;
		this.tier = tier;
		this.deedPillarX = deedPillarX;
		this.deedPillarY = deedPillarY;
		this.boxMinX = boxMinX;
		this.boxMinY = boxMinY;
		this.boxMaxX = boxMaxX;
		this.boxMaxY = boxMaxY;
		this.themeHint = themeHint;
	}

	public boolean isVacant(final long nowMs) {
		return deedHolder == null || nowMs > tenancyExpiresMs;
	}

	public boolean contains(final int x, final int y) {
		return x >= boxMinX && x <= boxMaxX && y >= boxMinY && y <= boxMaxY;
	}

	public List<java.util.Map.Entry<String, Integer>> bidsHighestFirst() {
		final List<java.util.Map.Entry<String, Integer>> list = new ArrayList<>(openBids.entrySet());
		list.sort((a, b) -> Integer.compare(b.getValue(), a.getValue()));
		return list;
	}
}

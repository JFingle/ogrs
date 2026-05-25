package com.openrsc.server.plugins.custom.plots;

import com.openrsc.server.model.entity.player.Player;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * OGRS — Plot registry. Phase 1F-α of the housing/contract arc.
 * Bootstraps a fixed inventory of plots at server start. In-memory v1
 * (plots survive restart since the bootstrap re-creates them; bids +
 * ownership are lost without DB persistence).
 *
 * v1 inventory — 5 plots:
 *   1 — Lumbridge Market (BASIC)
 *   2 — Falador Outskirts (BASIC)
 *   3 — Catherby Coast (PREMIUM)
 *   4 — Karamja Jungle (PREMIUM)
 *   5 — Wilderness Stronghold (WILDERNESS, guild-only — Phase 2-γ wires up raid mechanics)
 *
 * Each plot's coordinates are placeholders that we can move once the
 * deed pillars are placed in-world and sparky walks them.
 */
public final class PlotRegistry {

	private static final Map<Integer, Plot> PLOTS = new HashMap<>();
	private static boolean bootstrapped = false;

	private PlotRegistry() {}

	public static synchronized void bootstrap() {
		if (bootstrapped) return;
		bootstrapped = true;
		// (id, name, tier, pillarX, pillarY, minX, minY, maxX, maxY, theme)
		PLOTS.put(1, new Plot(1, "Lumbridge Market Plot",   Plot.Tier.BASIC,
			122, 660,   118, 656, 126, 664,   "urban"));
		PLOTS.put(2, new Plot(2, "Falador Outskirts Plot",  Plot.Tier.BASIC,
			302, 555,   298, 551, 306, 559,   "urban"));
		PLOTS.put(3, new Plot(3, "Catherby Coast Plot",     Plot.Tier.PREMIUM,
			432, 510,   426, 504, 438, 516,   "coastal"));
		PLOTS.put(4, new Plot(4, "Karamja Jungle Plot",     Plot.Tier.PREMIUM,
			364, 705,   358, 699, 370, 711,   "jungle"));
		PLOTS.put(5, new Plot(5, "Wilderness Stronghold",   Plot.Tier.WILDERNESS,
			236, 162,   228, 154, 244, 170,   "wilderness"));
	}

	public static synchronized Plot byId(final int id) {
		bootstrap();
		return PLOTS.get(id);
	}

	public static synchronized List<Plot> listAll() {
		bootstrap();
		return new ArrayList<>(PLOTS.values());
	}

	public static synchronized Plot byPillarLocation(final int x, final int y) {
		bootstrap();
		for (Plot p : PLOTS.values()) {
			if (p.deedPillarX == x && p.deedPillarY == y) return p;
		}
		return null;
	}

	public static synchronized Plot byHolder(final String holder) {
		bootstrap();
		if (holder == null) return null;
		for (Plot p : PLOTS.values()) {
			if (holder.equalsIgnoreCase(p.deedHolder)) return p;
		}
		return null;
	}

	// ─── Bidding ─────────────────────────────────────────────────────

	public static synchronized boolean placeBid(final Plot p, final String username, final int amount) {
		if (amount < p.tier.auctionFloor()) return false;
		// Add (or update) this player's bid.
		p.openBids.put(username.toLowerCase(), amount);
		return true;
	}

	/** Refund a bid (caller pays gold back). Returns the amount that
	 *  was bid, or 0 if no bid existed. */
	public static synchronized int withdrawBid(final Plot p, final String username) {
		final Integer prev = p.openBids.remove(username.toLowerCase());
		return prev == null ? 0 : prev;
	}

	/** Apply persisted state on top of the bootstrapped plot definitions.
	 *  Plot identity + coords come from bootstrap(); we just overlay
	 *  the mutable fields (deedHolder, tenancyExpiresMs, openBids,
	 *  features). Unknown plot ids are skipped — they reference plots
	 *  no longer in the bootstrap inventory (post-deletion). */
	public static synchronized void loadFromPersistence(
			final Map<Integer, String> deedHolders,
			final Map<Integer, Long> tenancyExpiry,
			final Map<Integer, Map<String, Integer>> bidsByPlot,
			final Map<Integer, List<PlotFeature>> featuresByPlot) {
		bootstrap();
		for (Map.Entry<Integer, String> e : deedHolders.entrySet()) {
			final Plot p = PLOTS.get(e.getKey());
			if (p == null) continue;
			p.deedHolder = e.getValue();
		}
		for (Map.Entry<Integer, Long> e : tenancyExpiry.entrySet()) {
			final Plot p = PLOTS.get(e.getKey());
			if (p == null) continue;
			p.tenancyExpiresMs = e.getValue();
		}
		for (Plot p : PLOTS.values()) {
			p.openBids.clear();
			p.features.clear();
		}
		for (Map.Entry<Integer, Map<String, Integer>> e : bidsByPlot.entrySet()) {
			final Plot p = PLOTS.get(e.getKey());
			if (p == null) continue;
			p.openBids.putAll(e.getValue());
		}
		for (Map.Entry<Integer, List<PlotFeature>> e : featuresByPlot.entrySet()) {
			final Plot p = PLOTS.get(e.getKey());
			if (p == null) continue;
			for (PlotFeature pf : e.getValue()) {
				p.features.put(Plot.featureKey(pf.x, pf.y), pf);
			}
		}
	}

	// ─── Auction close ───────────────────────────────────────────────

	/** Close the auction on this plot. Highest bidder becomes the deed
	 *  holder; tenancy lasts 7 days. Returns the winning entry (or null
	 *  if no bids). All non-winning bids must be refunded by the caller
	 *  (the bid escrow lives in the chat command layer). */
	public static synchronized Map.Entry<String, Integer> closeAuction(final Plot p) {
		if (p.openBids.isEmpty()) return null;
		final List<Map.Entry<String, Integer>> sorted = p.bidsHighestFirst();
		final Map.Entry<String, Integer> winner = sorted.get(0);
		p.deedHolder = winner.getKey();
		p.tenancyExpiresMs = System.currentTimeMillis() + 7L * 24 * 3600 * 1000;
		p.openBids.clear();
		return winner;
	}
}

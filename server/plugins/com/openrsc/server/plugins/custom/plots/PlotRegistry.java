package com.openrsc.server.plugins.custom.plots;

import com.openrsc.server.constants.ItemId;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.custom.guilds.Guild;
import com.openrsc.server.plugins.custom.guilds.GuildRegistry;
import com.openrsc.server.util.rsc.DataConversions;

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
		// First bid on a vacant plot starts the 24h auction countdown.
		// Subsequent bids don't extend it (anti-snipe is left to the
		// natural "highest bid wins at close" mechanic).
		if (p.openBids.isEmpty() && p.auctionEndsMs == 0) {
			p.auctionEndsMs = System.currentTimeMillis() + 24L * 3600 * 1000;
		}
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
	 *  the mutable fields (deedHolder, tenancyExpiresMs, auctionEndsMs,
	 *  openBids, features). Unknown plot ids are skipped — they
	 *  reference plots no longer in the bootstrap inventory (post-deletion). */
	public static synchronized void loadFromPersistence(
			final Map<Integer, String> deedHolders,
			final Map<Integer, Long> tenancyExpiry,
			final Map<Integer, Long> auctionEnds,
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
		for (Map.Entry<Integer, Long> e : auctionEnds.entrySet()) {
			final Plot p = PLOTS.get(e.getKey());
			if (p == null) continue;
			p.auctionEndsMs = e.getValue();
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

	// ─── Settle helper (shared by ::plot close + PlotAuctionTick) ───

	/** Outcome record so the caller can render a chat summary. */
	public static final class SettleResult {
		public final String winnerName;       // null if void
		public final int    winnerAmount;     // 0 if void
		public final String voidReason;       // null on success
		public final String deedAssignedTo;   // username or guild name; null on void
		SettleResult(final String w, final int amt, final String reason, final String deed) {
			this.winnerName = w; this.winnerAmount = amt;
			this.voidReason = reason; this.deedAssignedTo = deed;
		}
	}

	/** Close one plot's auction: pick highest bid, refund losers to
	 *  inventory if online (gold sinks for offline losers in v1 —
	 *  mailbox queue lands later), assign the deed (translating to
	 *  guild name for WILDERNESS plots), reset the auction window.
	 *
	 *  Idempotent on plots with no bids — returns a "no bids" void.
	 *  Should be called from the game thread (mutates inventories). */
	public static synchronized SettleResult settleAuction(final Plot p, final World world) {
		if (p.openBids.isEmpty()) {
			// Extend the auction window by another 24h so the plot keeps
			// inviting bids without immediately re-firing the tick.
			p.auctionEndsMs = System.currentTimeMillis() + 24L * 3600 * 1000;
			return new SettleResult(null, 0, "no bids", null);
		}
		final List<Map.Entry<String, Integer>> sorted = p.bidsHighestFirst();
		final Map.Entry<String, Integer> winner = sorted.get(0);

		// Refund losers.
		for (int i = 1; i < sorted.size(); i++) {
			refundBidder(world, sorted.get(i).getKey(), sorted.get(i).getValue(), p.name);
		}

		String deed;
		if (p.tier == Plot.Tier.WILDERNESS) {
			final Guild g = GuildRegistry.byMember(winner.getKey());
			if (g == null) {
				// Winner left their guild between bid and close — refund them too, void the auction.
				refundBidder(world, winner.getKey(), winner.getValue(), p.name);
				p.openBids.clear();
				p.auctionEndsMs = System.currentTimeMillis() + 24L * 3600 * 1000;
				return new SettleResult(winner.getKey(), winner.getValue(),
					"winner no longer in a guild — wilderness deed could not be assigned", null);
			}
			deed = g.name;
		} else {
			deed = winner.getKey();
		}

		p.deedHolder = deed;
		p.tenancyExpiresMs = System.currentTimeMillis() + 7L * 24 * 3600 * 1000;
		p.openBids.clear();
		p.auctionEndsMs = 0;

		// Notify the winner if online.
		final Player wp = world.getPlayer(DataConversions.usernameToHash(winner.getKey()));
		if (wp != null) {
			wp.message("@gre@You won the deed to '" + p.name + "' for " + winner.getValue()
				+ "gp. Tenancy: 7 days.");
		}
		return new SettleResult(winner.getKey(), winner.getValue(), null, deed);
	}

	private static void refundBidder(final World world, final String username, final int gold, final String plotName) {
		final Player lp = world.getPlayer(DataConversions.usernameToHash(username));
		if (lp != null) {
			lp.getCarriedItems().getInventory().add(new Item(ItemId.COINS.id(), gold));
			lp.message("@yel@Auction on '" + plotName + "' closed. Refunded your " + gold + "gp bid.");
		}
		// Offline → gold sinks (mailbox queue ships in a future phase).
	}

	/** Revert a plot to vacant when its tenancy expires. Idempotent.
	 *  Notifies the previous deed holder if online. */
	public static synchronized void revertExpiredTenancy(final Plot p, final World world) {
		if (p.deedHolder == null) return;
		if (p.tenancyExpiresMs > System.currentTimeMillis()) return;
		final String prev = p.deedHolder;
		p.deedHolder = null;
		p.tenancyExpiresMs = 0;
		// auctionEndsMs left at 0 — first new bid will start the window.
		if (p.tier != Plot.Tier.WILDERNESS) {
			final Player pp = world.getPlayer(DataConversions.usernameToHash(prev));
			if (pp != null) pp.message("@yel@Your tenancy on '" + p.name + "' has expired. The plot is back up for auction.");
		}
		// For WILDERNESS plots, deed holder is a guild — broadcast to
		// online guild members.
		if (p.tier == Plot.Tier.WILDERNESS) {
			final Guild g = GuildRegistry.byName(prev);
			if (g != null) {
				for (String member : g.members.keySet()) {
					final Player pp = world.getPlayer(DataConversions.usernameToHash(member));
					if (pp != null) pp.message("@yel@Your guild's wilderness deed on '" + p.name + "' has expired. Bid again to retain it.");
				}
			}
		}
	}

}

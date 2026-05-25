package com.openrsc.server.plugins.custom.plots;

import com.openrsc.server.event.rsc.DuplicationStrategy;
import com.openrsc.server.event.rsc.GameTickEvent;
import com.openrsc.server.model.world.World;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * OGRS — per-minute plot auction tick. Phase 1F-β-2.
 *
 *   1. For each plot whose tenancy has expired: revert to vacant
 *      (deedHolder=null, tenancyExpiresMs=0) and notify the prior
 *      holder (or guild for wilderness).
 *   2. For each plot whose 24h bid window has ended: settle the
 *      auction (highest bidder wins, losers refunded, deed assigned).
 *
 * 94 game ticks at 640ms each = ~60s cadence. Fast enough that
 * "auction closes at 12:00:00" is accurate to the minute, light
 * enough not to add measurable per-tick load.
 */
public final class PlotAuctionTick extends GameTickEvent {

	private static final Logger LOGGER = LogManager.getLogger(PlotAuctionTick.class);
	private static final int STRIDE_TICKS = 94;

	public PlotAuctionTick(final World world) {
		super(world, null, STRIDE_TICKS, "OGRS Plot Auction Tick", DuplicationStrategy.ALLOW_MULTIPLE);
	}

	@Override
	public void run() {
		final long nowMs = System.currentTimeMillis();
		final World world = getWorld();
		for (Plot p : PlotRegistry.listAll()) {
			// Step 1: tenancy expiry → vacant.
			if (p.deedHolder != null && p.tenancyExpiresMs > 0 && p.tenancyExpiresMs <= nowMs) {
				PlotRegistry.revertExpiredTenancy(p, world);
			}
			// Step 2: bid window closed → settle.
			if (p.deedHolder == null && p.auctionEndsMs > 0 && p.auctionEndsMs <= nowMs) {
				final PlotRegistry.SettleResult r = PlotRegistry.settleAuction(p, world);
				if (r.voidReason != null) {
					LOGGER.info("OGRS plot #{} '{}' auto-close: void ({})", p.id, p.name, r.voidReason);
				} else {
					LOGGER.info("OGRS plot #{} '{}' auto-close: '{}' wins {}gp (deed -> {})",
						p.id, p.name, r.winnerName, r.winnerAmount, r.deedAssignedTo);
				}
			}
		}
	}
}

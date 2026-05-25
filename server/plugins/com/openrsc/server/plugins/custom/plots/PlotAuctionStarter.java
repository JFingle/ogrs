package com.openrsc.server.plugins.custom.plots;

import com.google.inject.Inject;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.triggers.StartupTrigger;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * OGRS — schedule the plot auction tick at boot. Mirrors
 * MentorshipTickStarter so the housing/contract arc keeps a
 * consistent wiring pattern.
 */
public final class PlotAuctionStarter implements StartupTrigger {

	private static final Logger LOGGER = LogManager.getLogger(PlotAuctionStarter.class);

	private final World world;

	@Inject
	public PlotAuctionStarter(final World world) {
		this.world = world;
	}

	@Override
	public void onStartup() {
		world.getServer().getGameEventHandler().add(new PlotAuctionTick(world));
		LOGGER.info("OGRS: plot auction tick scheduled (every ~60s)");
	}

	@Override
	public boolean blockStartup() {
		return true;
	}
}

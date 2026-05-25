package com.openrsc.server.plugins.custom.contracts;

import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.triggers.StartupTrigger;

import com.google.inject.Inject;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * OGRS — schedule the mentorship tick handler at server boot. One
 * instance per server, runs forever. Mirrors OgrsCryptFloorOverride's
 * StartupTrigger pattern.
 */
public final class MentorshipTickStarter implements StartupTrigger {

	private static final Logger LOGGER = LogManager.getLogger(MentorshipTickStarter.class);

	private final World world;

	@Inject
	public MentorshipTickStarter(final World world) {
		this.world = world;
	}

	@Override
	public void onStartup() {
		final MentorshipTick tick = new MentorshipTick(world);
		world.getServer().getGameEventHandler().add(tick);
		LOGGER.info("OGRS: mentorship tick scheduled (every 5 game ticks)");
	}

	@Override
	public boolean blockStartup() {
		return true;
	}
}

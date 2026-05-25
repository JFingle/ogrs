package com.openrsc.server.plugins.custom.persistence;

import com.google.inject.Inject;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.triggers.StartupTrigger;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * OGRS — boot the social-registry persistence layer.
 *
 *   1. Pull saved contracts/guilds/plots out of the DB into the
 *      in-memory registries (the registries' bootstrap() call is
 *      preserved — load just overlays mutable state on top).
 *   2. Schedule {@link OgrsPersistenceTick} to flush every ~30s.
 *
 * Mirrors MentorshipTickStarter's pattern so the wiring is consistent
 * across the housing/contract arc plugins.
 */
public final class OgrsPersistenceStarter implements StartupTrigger {

	private static final Logger LOGGER = LogManager.getLogger(OgrsPersistenceStarter.class);

	private final World world;

	@Inject
	public OgrsPersistenceStarter(final World world) {
		this.world = world;
	}

	@Override
	public void onStartup() {
		OgrsPersistence.loadAll(world);
		world.getServer().getGameEventHandler().add(new OgrsPersistenceTick(world));
		LOGGER.info("OGRS: persistence flush scheduled (every 30s)");
	}

	@Override
	public boolean blockStartup() {
		return true;
	}
}

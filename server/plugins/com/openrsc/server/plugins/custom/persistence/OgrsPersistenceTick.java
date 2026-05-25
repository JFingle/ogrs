package com.openrsc.server.plugins.custom.persistence;

import com.openrsc.server.event.rsc.DuplicationStrategy;
import com.openrsc.server.event.rsc.GameTickEvent;
import com.openrsc.server.model.world.World;

/**
 * OGRS — periodic DB flush for the social registries.
 *
 * Fires every ~47 ticks (= 30s @ 640ms). Calls OgrsPersistence.flushAll()
 * which snapshots ContractRegistry + GuildRegistry + PlotRegistry and
 * rewrites the corresponding ogrs_* tables in a single transaction.
 *
 * 30s is a deliberate trade — low enough that a crash loses at most
 * half a minute of activity; high enough that the all-in transaction
 * cost stays negligible at our row counts. Bid-heavy or
 * contract-spam-heavy stretches still flush at the same cadence —
 * the in-memory registry is the source of truth and remains
 * responsive to gameplay regardless of DB IO.
 */
public final class OgrsPersistenceTick extends GameTickEvent {

	private static final int STRIDE_TICKS = 47;

	public OgrsPersistenceTick(final World world) {
		super(world, null, STRIDE_TICKS, "OGRS Persistence Flush", DuplicationStrategy.ALLOW_MULTIPLE);
	}

	@Override
	public void run() {
		OgrsPersistence.flushAll(getWorld());
	}
}

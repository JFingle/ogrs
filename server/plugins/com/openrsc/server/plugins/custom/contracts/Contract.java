package com.openrsc.server.plugins.custom.contracts;

/**
 * OGRS — single contract data record. Phase 1C of the housing/contract
 * arc (sparky 2026-05-24). In-memory only for v1; DB persistence ships
 * in a follow-up phase. Contracts lost on server restart — fine for
 * iterating on design.
 *
 * Lifecycle:
 *   OPEN     — posted by an employer, waiting for a worker.
 *   ACCEPTED — a worker has claimed it, gathering in progress.
 *   COMPLETED — worker delivered. Items waiting in the contract for
 *               employer pickup at the Job Board.
 *   CANCELLED — refunded; entry stays for audit.
 *
 * v1 type: RESOURCE_DELIVERY. Future types added by extending the
 * Type enum + adding the corresponding processing in ContractRegistry.
 */
public final class Contract {

	public enum Type {
		RESOURCE_DELIVERY,   // worker gathers and delivers itemId × amount
		MENTORSHIP,          // mentor bonds with apprentice for skillId for N hours
		CONSTRUCTION_JOB,    // worker builds a feature on employer's plot; employer gets XP
	}

	public enum Status {
		OPEN, ACCEPTED, COMPLETED, CANCELLED, EXPIRED
	}

	public final int id;
	public final Type type;
	public final String posterName;     // employer's display name
	public final int    itemId;
	public final int    itemAmount;
	public final int    goldReward;     // gold escrowed at post time
	public final long   createdEpochMs;
	public final long   deadlineEpochMs;

	public Status  status;
	public String  workerName = "";     // empty until accepted
	public long    acceptedEpochMs = 0;
	public long    completedEpochMs = 0;

	// Mentorship-only fields. Unused for RESOURCE_DELIVERY contracts.
	public int     mentorSkillId    = -1;
	public int     mentorMinLevel   = 0;
	public int     mentorDurationHrs = 0;
	public long    bondedTicksAccrued = 0;  // for the future XP-bonus integration

	// Construction-job-only fields. featureTypeOrdinal stores
	// PlotFeature.Type.ordinal() (avoids cross-package dependency in
	// this data class).
	public int     constructionFeatureTypeOrdinal = -1;
	public int     constructionPlotId  = -1;
	public int     constructionTargetX = -1;
	public int     constructionTargetY = -1;

	public Contract(final int id, final Type type, final String posterName,
	                final int itemId, final int itemAmount, final int goldReward,
	                final long createdEpochMs, final long deadlineEpochMs) {
		this.id = id;
		this.type = type;
		this.posterName = posterName;
		this.itemId = itemId;
		this.itemAmount = itemAmount;
		this.goldReward = goldReward;
		this.createdEpochMs = createdEpochMs;
		this.deadlineEpochMs = deadlineEpochMs;
		this.status = Status.OPEN;
	}

	public boolean isExpired(final long nowMs) {
		return status == Status.OPEN && nowMs > deadlineEpochMs;
	}
}

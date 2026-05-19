package com.openrsc.server.event.rsc.impl.projectile;

import com.openrsc.server.constants.Skill;
import com.openrsc.server.content.OgrsAutocast;
import com.openrsc.server.event.rsc.DuplicationStrategy;
import com.openrsc.server.event.rsc.GameTickEvent;
import com.openrsc.server.model.PathValidation;
import com.openrsc.server.model.entity.Mob;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.World;

/**
 * OGRS — Magic autocast attack loop.
 *
 * Sparky 2026-05-19: "spells have a range they can cast at, so when i click
 * a mob, if im within range it should shoot." Modeled on RangeEvent so the
 * cadence and walk-to-range behavior matches bows/crossbows.
 *
 * Flow per tick:
 *   1. If autocast is disabled, target dead, or player offline -> stop.
 *   2. If target moved out of spell range, walk toward it and try again
 *      next tick.
 *   3. If clear line of sight check fails, give up (matches RangeEvent).
 *   4. Fire OgrsAutocast.tryAutocast which does runes/damage/projectile/XP.
 *   5. Cool down 3 ticks before the next attempt.
 */
public class OgrsAutocastEvent extends GameTickEvent {

	/** Spell range in tiles. Matches authentic spell range from SpellHandler. */
	public static final int SPELL_RANGE = 5;

	private final Player player;
	private Mob target;

	public OgrsAutocastEvent(final World world, final Player owner, final long tickDelay, final Mob target) {
		super(world, owner, tickDelay, "OGRS Autocast Event", DuplicationStrategy.ONE_PER_MOB);
		this.player = owner;
		this.target = target;
	}

	public boolean equals(Object o) {
		if (o instanceof OgrsAutocastEvent) {
			return ((OgrsAutocastEvent) o).belongsTo(getOwner());
		}
		return false;
	}

	public Mob getTarget() { return target; }

	public void reTarget(final Mob mob) {
		this.target = mob;
		setDelayTicks(2);
	}

	public void restart() {
		running = true;
	}

	public void run() {
		if (!running) return;

		// Bail on common stop conditions.
		if (!player.isAutocastEnabled()
			|| !player.loggedIn()
			|| target == null
			|| target.isRemoved()
			|| target.getSkills().getLevel(Skill.HITS.id()) <= 0
			|| (target.isPlayer() && !((Player) target).loggedIn())) {
			player.resetAutocastEvent();
			return;
		}

		// Walk closer if the target slipped out of spell range.
		if (!player.withinRange(target, SPELL_RANGE)) {
			if (player.nextStep(player.getX(), player.getY(), target) == null) {
				player.message("@gre@Autocast: can't reach the target.");
				player.resetAutocastEvent();
				return;
			}
			player.walkToEntity(target.getX(), target.getY());
			setDelayTicks(1);
			return;
		}

		// Clear line of sight, otherwise drop the loop (RangeEvent mirror).
		if (!PathValidation.checkPath(player.getWorld(), player.getLocation(), target.getLocation())) {
			player.message("@gre@Autocast: I can't get a clear shot from here.");
			player.resetAutocastEvent();
			return;
		}

		// Stop running on the spot before casting so the projectile fires
		// from a stable position.
		if (!player.finishedPath()) player.resetPath();

		player.face(target);

		final boolean cast = OgrsAutocast.tryAutocast(player, target);
		if (!cast) {
			// tryAutocast already disabled autocast or printed any user
			// message; stop the loop.
			player.resetAutocastEvent();
			return;
		}

		// Authentic spell cadence: 3 ticks between casts (~1.9s with the
		// 640ms tick).
		setDelayTicks(3);
	}
}

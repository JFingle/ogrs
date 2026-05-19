package com.openrsc.server.model;

import com.openrsc.server.constants.Skill;
import com.openrsc.server.external.NPCLoc;
import com.openrsc.server.model.entity.Mob;
import com.openrsc.server.model.entity.npc.Npc;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.model.world.region.Region;
import com.openrsc.server.util.rsc.DataConversions;

/**
 * A WalkingQueue stores steps the client needs to walk and allows
 * this queue of steps to be modified.
 * The class will also process these steps when processNextMovement()
 * is called. This should be called once per server cycle.
 */
public class WalkingQueue {
	private boolean DEBUG = false;
	private Mob mob;

	public Path path;
	public boolean playerWasWalking;

	public WalkingQueue(Mob entity) {
		this.mob = entity;
	}

   /**
    * Handles logic to run when the player finishes walking. A player has finished walking if they 
	* were walking and then their path becomes null or empty.
    */ 
	private void handlePlayerFinishedWalking() {
		if (playerWasWalking) {
			Player currentPlayer = mob.isPlayer() ? (Player)mob : null;

			// Only track finished walking status of players.
			if (currentPlayer != null && !currentPlayer.isBusy()) {
				Point targetTile = currentPlayer.getLastTileClicked();

				if (targetTile != null) {
					Region region = currentPlayer.getWorld().getRegionManager().getRegion(targetTile);

					// Target would be the other player currentPlayer clicked on.
					Player target = region.getPlayer(targetTile.getX(), targetTile.getY(), currentPlayer, false);

					if (target != null && target != currentPlayer) {
						// Is current player within 1 tile of target?
						boolean targetWithinOneTile = currentPlayer.withinRange(targetTile, 1);

						// Face the other player. This will have no effect if player_blocking config is disabled.
						if (targetWithinOneTile) {
							currentPlayer.face(target);
						}
					}
					
					// Reset lastTileClicked so the player doesn't re-face the last player they clicked on.
					currentPlayer.setLastTileClicked(null);
				}
			}
		}

		playerWasWalking = false;
	}

	/**
	 * Processes the next player's movement.
	 *
	 * OGRS — when the mob is a Player who has running enabled and run energy
	 * > 0, this advances them TWO tiles per tick (one extra path point popped)
	 * and drains the agility-scaled cost per tile actually stepped. Adjacency
	 * checks stay per-step, so pathfinding stays sane. If energy hits zero
	 * mid-double-step we just don't take the second step; the player keeps
	 * walking at 1 tile/tick on subsequent ticks until energy regens.
	 *
	 * Agility scaling (sparky 2026-05-19 follow-up to #37):
	 *   - drain  : 100 base, -50 at lvl 99 (linear) → lvl 99 lasts ~2x longer
	 *   - regen  : 80/40 idle/walking base, +80/+40 at lvl 99 → ~2x recovery
	 *   - sprint : agility >= 70 rolls for a bonus 3rd tile (lvl 70 = 0%,
	 *              lvl 99 = ~29%, lvl 110 boosted ≈ 40%). When it procs,
	 *              the extra tile also drains. Caps at one bonus per tick.
	 * Uses the player's current (boosted) agility level so energy potions
	 * and capes feel rewarding.
	 */
	public void processNextMovement() {
		boolean stepped = takeOneStep();

		// OGRS — run-energy drain + regen lives here because this method
		// runs once per tick per player, which is exactly the cadence we
		// need. Three cases:
		//   stepped + running  -> drain, maybe take a second tile (and drain again)
		//   stepped + walking  -> modest regen
		//   not stepped (idle) -> full regen
		if (mob.isPlayer()) {
			Player p = (Player) mob;
			final int agility = p.getSkills().getLevel(Skill.AGILITY.id());
			final int drainPerTile = agilityDrainPerTile(agility);
			if (stepped && p.isRunning()) {
				p.setRunEnergy(p.getRunEnergy() - drainPerTile);
				if (p.getRunEnergy() > 0 && path != null && !path.isEmpty()) {
					if (takeOneStep()) {
						p.setRunEnergy(p.getRunEnergy() - drainPerTile);
						// Third-tile sprint roll — only kicks in at high
						// agility, otherwise the chance is 0. Costs an
						// extra drain like the other tiles.
						if (p.getRunEnergy() > 0 && path != null && !path.isEmpty()
								&& rollAgilitySprint(agility)) {
							if (takeOneStep()) {
								p.setRunEnergy(p.getRunEnergy() - drainPerTile);
							}
						}
					}
				}
			} else if (stepped) {
				if (p.getRunEnergy() < Player.MAX_RUN_ENERGY) {
					p.setRunEnergy(p.getRunEnergy()
						+ agilityScaledRegen(Player.RUN_REGEN_WALKING, agility));
				}
			} else {
				if (p.getRunEnergy() < Player.MAX_RUN_ENERGY) {
					p.setRunEnergy(p.getRunEnergy()
						+ agilityScaledRegen(Player.RUN_REGEN_IDLE, agility));
				}
			}
		}
	}

	/**
	 * Agility-scaled drain per tile. lvl 1 ≈ 99, lvl 50 ≈ 75, lvl 99 = 50.
	 * Boosted levels above 99 keep clamping down toward 50 (no free running).
	 */
	private static int agilityDrainPerTile(int agility) {
		final int clamped = Math.max(1, Math.min(120, agility));
		final int reduction = (clamped * 50) / 99; // 0..50 (cap at 60 if boosted, then clamp below)
		return Math.max(50, Player.RUN_DRAIN_PER_TILE - reduction);
	}

	/**
	 * Agility-scaled regen. lvl 1 ≈ base, lvl 99 ≈ 2× base. Boosted levels
	 * keep climbing slightly past 2× but we cap at 2.5× to bound it.
	 */
	private static int agilityScaledRegen(int base, int agility) {
		final int clamped = Math.max(1, Math.min(120, agility));
		final int bonus = (base * clamped) / 99;
		final int total = base + bonus;
		final int cap = (base * 5) / 2; // 2.5× ceiling
		return Math.min(cap, total);
	}

	/**
	 * Returns true when a high-agility player gets a bonus third tile this
	 * tick. lvl < 70 ⇒ never. lvl 70 = 0%, +1pp per level up to lvl 99 = 29%,
	 * keeps climbing slightly past 99 for boosted/cape effects.
	 */
	private static boolean rollAgilitySprint(int agility) {
		if (agility < 70) return false;
		final int chance = Math.min(40, agility - 70); // pp
		return DataConversions.random(99) < chance;
	}

	/**
	 * Pops one path point and moves the mob to it. Returns true if a step
	 * happened (so callers can chain another), false if the path was empty
	 * or the adjacency check failed.
	 */
	private boolean takeOneStep() {
		if (path == null) {
			handlePlayerFinishedWalking();
			return false;
		} else if (path.isEmpty()) {
			handlePlayerFinishedWalking();
			reset();
			return false;
		}

		// Player is walking if path is not null or empty.
		playerWasWalking = true;

		Point walkPoint = path.poll();

		if (mob.getAttribute("blink", false)) {
			if (path.size() >= 1) {
				walkPoint = path.getLastPoint();
				((Player) mob).teleport(walkPoint.getX(), walkPoint.getY(), false);
			}
			return false;
		}

		int destX = walkPoint.getX();
		int destY = walkPoint.getY();
		int startX = mob.getX();
		int startY = mob.getY();
		if (!PathValidation.checkAdjacent(mob, new Point(startX, startY), new Point(destX, destY))) {
			reset();
			if (DEBUG && mob.isPlayer()) System.out.println("Failed adjacent check, not pathing.");
			return false;
		}

		if (mob.isNpc()) {
			NPCLoc loc = ((Npc) mob).getLoc();
			if (Point.location(destX, destY).inBounds(loc.minX() - 12, loc.minY() - 12,
				loc.maxX() + 12, loc.maxY() + 12) || (destX == 0 && destY == 0)) {
				mob.face(Point.location(destX, destY));
				mob.setLocation(Point.location(destX, destY));
			}
		}
		else {
			Player player = (Player) mob;
			player.face(Point.location(destX, destY));
			player.setLocation(Point.location(destX, destY));
			player.stepIncrementActivity();
		}
		return true;
	}

	public Point getNextMovement() {
		if (path == null || path.isEmpty()) {
			return mob.getLocation();
		}
		Point destPoint = path.getNextPoint();
		Point curPoint = mob.getLocation();
		if (!PathValidation.checkAdjacent(mob, curPoint, destPoint)) {
			return curPoint;
		} else {
			return destPoint;
		}
	}

	public void reset() {
		path = null;
		if (this.mob.isPlayer()) {
			if (this.mob.getDropItemEvent() != null) {
				this.mob.runDropEvent(true);
			}
		}
		if (this.mob.getTalkToNpcEvent() != null) {
			this.mob.runTalkToNpcEvent();
		}
	}

	public boolean finished() {
		return path == null || path.isEmpty();
	}

	public void setPath(Path path) {
		this.path = path;
	}
}

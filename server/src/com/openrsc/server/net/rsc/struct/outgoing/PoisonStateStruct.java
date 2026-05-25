package com.openrsc.server.net.rsc.struct.outgoing;

import com.openrsc.server.net.rsc.enums.OpcodeOut;
import com.openrsc.server.net.rsc.struct.AbstractStruct;

/**
 * OGRS — Poison state push (sparky 2026-05-24, UI track P1).
 * Two bytes — fired when the player's poison state changes (starts,
 * ticks down, or gets cured).
 *
 *   poisoned: 1 if Mob.getCurrentPoisonPower() &gt; 0, 0 otherwise.
 *   power:    current poison damage value 0..255 (engine caps; the
 *             player's antidote can drop this to 0).
 */
public class PoisonStateStruct extends AbstractStruct<OpcodeOut> {
	public boolean poisoned;
	public int power;
}

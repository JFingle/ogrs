package com.openrsc.server.net.rsc.struct.outgoing;

import com.openrsc.server.net.rsc.enums.OpcodeOut;
import com.openrsc.server.net.rsc.struct.AbstractStruct;

/**
 * OGRS — Run-energy state push (sparky 2026-05-19 #37 Commit C).
 * Tiny payload — two bytes — fired on toggle and on each tile-stride
 * while running so the client's energy bar tracks server reality.
 *
 *   running: 1 if Player.isRunning() at fire time, 0 otherwise.
 *   energy:  current Player.getRunEnergy() scaled to 0..100 percent.
 */
public class RunEnergyStruct extends AbstractStruct<OpcodeOut> {
	public boolean running;
	public int energyPercent;
}

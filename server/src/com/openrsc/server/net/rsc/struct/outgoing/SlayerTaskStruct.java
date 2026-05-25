package com.openrsc.server.net.rsc.struct.outgoing;

import com.openrsc.server.net.rsc.enums.OpcodeOut;
import com.openrsc.server.net.rsc.struct.AbstractStruct;

/**
 * OGRS — Slayer task push (sparky 2026-05-24, UI track P1).
 * Fired on login, task assign, task kill update, task complete.
 *
 *   hasTask:   1 if SlayerService.getActiveTask is non-null, else 0.
 *   npcName:   the task NPC's display name (empty when hasTask=0).
 *   remaining: count remaining (short — 0..32767).
 *   level:     player's current Slayer level (byte).
 */
public class SlayerTaskStruct extends AbstractStruct<OpcodeOut> {
	public boolean hasTask;
	public String npcName = "";
	public int remaining;
	public int level;
}

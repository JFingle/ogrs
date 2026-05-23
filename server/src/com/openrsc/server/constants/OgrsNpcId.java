package com.openrsc.server.constants;

import java.util.HashMap;
import java.util.Map;

/**
 * OGRS-authored NPC ids. Mirrors upstream {@link NpcId}'s shape so call
 * sites read consistently: {@code OgrsNpcId.GRIZZLED_TRAVELER.id()}
 * instead of bare magic numbers.
 *
 * Ids 836+ continue immediately after the upstream NpcDefsCustom range
 * (which ends at 835 — "Ash"). NPCs themselves are defined in
 * {@code content/npcs/*.yaml} and loaded into the engine at boot by
 * {@code OgrsContentNpcLoader}.
 *
 * Adding a new OGRS NPC: write the YAML, add a constant here with the
 * matching id, then reference {@code OgrsNpcId.MY_NPC.id()} in plugins.
 */
public enum OgrsNpcId {
	NOBODY(-1),

	GRIZZLED_TRAVELER(836),
	OLD_WAT(837),
	EDITH(838),
	GARTH(839),
	MARIGOLD(840),
	WENDEL(841),
	GOBLIN_SHAMAN(842),
	OLD_ARIC(843);

	private final int npcId;
	private static final Map<Integer, OgrsNpcId> byId = new HashMap<>();
	private static final Map<String, OgrsNpcId> byName = new HashMap<>();

	static {
		for (OgrsNpcId npc : OgrsNpcId.values()) {
			if (byId.put(npc.id(), npc) != null) {
				throw new IllegalArgumentException("duplicate OgrsNpcId: " + npc.id());
			}
			if (byName.put(sanitizeName(npc.name()), npc) != null) {
				throw new IllegalArgumentException("duplicate sanitized OgrsNpcId name: " + npc.name());
			}
		}
	}

	public static OgrsNpcId getById(Integer id) {
		return byId.getOrDefault(id, OgrsNpcId.NOBODY);
	}

	public static OgrsNpcId getByName(String name) {
		return byName.getOrDefault(sanitizeName(name), NOBODY);
	}

	private static String sanitizeName(String name) {
		return name.replaceAll("[\\W]", "")
			.replaceAll("_", "")
			.toLowerCase();
	}

	OgrsNpcId(int npcId) {
		this.npcId = npcId;
	}

	public int id() {
		return npcId;
	}
}

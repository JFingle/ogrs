package com.openrsc.server.plugins.custom.quests;

import com.openrsc.server.external.OgrsContentQuestLoader;
import com.openrsc.server.external.OgrsContentQuestLoader.QuestMetadata;
import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.QuestInterface;

import static com.openrsc.server.plugins.Functions.give;
import static com.openrsc.server.plugins.Functions.incQP;
import static com.openrsc.server.plugins.Functions.incStat;

/**
 * OGRS-style {@link QuestInterface} base class. Concrete subclasses
 * provide the trigger logic (Talk-to dialog, kill drops, etc.) and pass
 * a YAML filename to the constructor; this base class pulls metadata
 * from {@link OgrsContentQuestLoader} for everything else (id, name,
 * quest points, members flag, reward declaration).
 *
 * Adding an OGRS quest is then:
 *   1. {@code content/quests/<slug>.yaml}      — metadata, journal, rewards
 *   2. concrete {@code public class … extends AbstractOgrsQuest} that
 *      passes the YAML filename to {@code super(...)} and implements
 *      whichever {@code …Trigger} interfaces fit the quest.
 *
 * The PluginHandler picks up the concrete class via classpath scan and
 * registers it both as a quest (via QuestInterface) and as trigger
 * handlers (via the implemented Trigger interfaces).
 */
public abstract class AbstractOgrsQuest implements QuestInterface {

	protected final QuestMetadata metadata;

	protected AbstractOgrsQuest(final String yamlFilename) {
		this.metadata = OgrsContentQuestLoader.byFilename(yamlFilename);
		if (this.metadata == null) {
			throw new IllegalStateException(
				"OGRS quest YAML missing or not yet loaded: " + yamlFilename
					+ " — make sure EntityHandler.load() has run before plugin init.");
		}
	}

	@Override public final int getQuestId()    { return metadata.id; }
	@Override public final String getQuestName() { return metadata.name; }
	@Override public final int getQuestPoints()  { return metadata.questPoints; }
	@Override public final boolean isMembers()   { return metadata.members; }

	/** Stage description for the player — surfaced via NPC dialog. */
	public final String journalLine(final int stage) {
		return metadata.journal.getOrDefault(stage, "");
	}

	@Override
	public void handleReward(final Player player) {
		// XP rewards. baseXP/varXP go to incStat which multiplies by 4
		// internally for engine storage. We pass amountDisplay as base, 0 as var
		// → fixed amount, no random component.
		for (final OgrsContentQuestLoader.XpReward x : metadata.xpRewards) {
			incStat(player, x.skillId, x.amountDisplay, 0);
		}
		// Item rewards.
		for (final OgrsContentQuestLoader.ItemReward i : metadata.itemRewards) {
			give(player, i.itemId, i.amount);
		}
		// Quest-points award + the standard "completed" toast.
		incQP(player, metadata.questPoints, !player.isUsingClientBeforeQP());
		player.message("@gre@" + metadata.name + " — quest complete!");
	}
}

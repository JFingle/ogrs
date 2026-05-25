package com.openrsc.server.plugins.custom.plots;

import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.custom.guilds.Guild;
import com.openrsc.server.plugins.custom.guilds.GuildRegistry;

/**
 * OGRS — shared permission check for any built plot feature.
 *
 * Asked by OgrsPlotBank (chest id 1328), OgrsPlotForge (forge id 1329),
 * and the Smithing plugin (when an iron bar is used on a forge). The
 * single point of truth keeps the rules consistent:
 *
 *   - Communal lodge (no plot owns the tile) → anyone may use it.
 *   - Plot exists but unregistered feature → benign skip (lets the
 *     base scenery handle interaction or print a hint message).
 *   - Plot wilderness tier → guild membership required.
 *   - Plot basic/premium → deed holder only.
 *
 * Returns true if the player is allowed; false if they are not and a
 * @red@ refusal message has already been sent.
 */
public final class PlotPermissions {

	private PlotPermissions() {}

	/** Can the player operate the feature located at (x,y)?
	 *
	 *  @param featureLabel a short noun used in refusal messages,
	 *                      e.g. "chest", "forge".
	 *  @return true if allowed (caller proceeds), false if refused
	 *          (caller stops; refusal message already shown).
	 */
	public static boolean canUseFeatureAt(final Player player, final int x, final int y, final String featureLabel) {
		Plot owning = null;
		for (Plot pl : PlotRegistry.listAll()) {
			if (pl.contains(x, y)) { owning = pl; break; }
		}
		if (owning == null) return true;  // communal lodge

		final PlotFeature pf = owning.featureAt(x, y);
		if (pf == null) {
			player.message("(@yel@The " + featureLabel + " looks built but isn't registered. Try again after a restart.)");
			return false;
		}
		if (owning.deedHolder == null) {
			player.message("@red@This " + featureLabel + "'s plot has no deed holder.");
			return false;
		}
		if (owning.tier == Plot.Tier.WILDERNESS) {
			final Guild g = GuildRegistry.byName(owning.deedHolder);
			if (g == null || !g.hasMember(player.getUsername())) {
				player.message("@red@This " + featureLabel + " is property of guild @whi@" + owning.deedHolder + "@red@.");
				return false;
			}
			return true;
		}
		if (!owning.deedHolder.equalsIgnoreCase(player.getUsername())) {
			player.message("@red@This " + featureLabel + " belongs to @whi@" + owning.deedHolder + "@red@.");
			return false;
		}
		return true;
	}
}

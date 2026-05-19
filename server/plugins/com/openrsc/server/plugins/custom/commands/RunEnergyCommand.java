package com.openrsc.server.plugins.custom.commands;

import com.openrsc.server.model.entity.player.Player;
import com.openrsc.server.plugins.triggers.CommandTrigger;

import static com.openrsc.server.plugins.Functions.inArray;

/**
 * OGRS — run-energy chat commands.
 *
 * Until the minimap UI lands (separate session), the player toggles running
 * and inspects energy from chat. Energy itself drains/regens automatically
 * in WalkingQueue every tick.
 *
 * Commands:
 *   ::run            — toggle running on/off. Shows current energy.
 *   ::energy         — print current energy without changing the toggle.
 *
 * Gated by ServerConfiguration.WANT_RUN_ENERGY; if the world has it off,
 * the toggle is a no-op and the player gets a friendly message.
 */
public class RunEnergyCommand implements CommandTrigger {

	@Override
	public boolean blockCommand(final Player player, final String cmd, final String[] args) {
		return inArray(cmd.toLowerCase(), "run", "running", "sprint", "energy");
	}

	@Override
	public void onCommand(final Player player, final String cmd, final String[] args) {
		if (!player.getConfig().WANT_RUN_ENERGY) {
			player.message("@gre@Run energy is disabled on this world.");
			return;
		}

		final String c = cmd.toLowerCase();
		if (c.equals("energy")) {
			showEnergy(player);
			return;
		}

		// ::run / ::running / ::sprint — toggle
		final boolean newState = !player.isRunning();
		if (newState && player.getRunEnergy() <= 0) {
			player.message("@gre@You're too winded to run. Walk a bit to recover.");
			return;
		}
		player.setRunning(newState);
		player.message("@gre@Running: " + (player.isRunning() ? "ON" : "OFF")
			+ "  —  Energy: " + percent(player.getRunEnergy()) + "%");
	}

	private static void showEnergy(final Player player) {
		player.message("@gre@Run energy: " + percent(player.getRunEnergy()) + "%"
			+ "  —  " + (player.isRunning() ? "running" : "walking"));
	}

	private static int percent(final int internal) {
		// MAX_RUN_ENERGY = 10000 internal units, 100% display
		return Math.max(0, Math.min(100, internal / (Player.MAX_RUN_ENERGY / 100)));
	}
}

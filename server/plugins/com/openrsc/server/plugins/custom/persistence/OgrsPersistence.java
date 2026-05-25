package com.openrsc.server.plugins.custom.persistence;

import com.openrsc.server.database.JDBCDatabase;
import com.openrsc.server.model.container.Item;
import com.openrsc.server.model.world.World;
import com.openrsc.server.plugins.custom.contracts.Contract;
import com.openrsc.server.plugins.custom.contracts.ContractRegistry;
import com.openrsc.server.plugins.custom.guilds.Guild;
import com.openrsc.server.plugins.custom.guilds.GuildRegistry;
import com.openrsc.server.plugins.custom.plots.Plot;
import com.openrsc.server.plugins.custom.plots.PlotFeature;
import com.openrsc.server.plugins.custom.plots.PlotRegistry;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * OGRS — persistence facade for the social/housing/contract arc.
 *
 * Phase 1H (sparky 2026-05-25). Backs ContractRegistry, GuildRegistry
 * and PlotRegistry with DB rows so the whole arc survives restarts.
 *
 * Strategy: full DELETE + INSERT per registry on every flush, all
 * wrapped in a single transaction so a crash mid-flush leaves the
 * prior snapshot intact. Row counts are tiny (dozens to low hundreds)
 * — overhead is microseconds against the 30-second flush cadence.
 *
 * Entry points:
 *   loadAll(world)   — read DB into the registries on server startup.
 *                      Idempotent on the registries (clears first).
 *   flushAll(world)  — snapshot registries → DB. Called periodically
 *                      by OgrsPersistenceTick and also on demand from
 *                      ::ogrssave (admin command).
 *
 * Thread safety: callers (StartupTrigger / GameTickEvent / chat
 * command) all run on the single game thread. The JDBC connection is
 * shared with the engine's own save logic which also uses the game
 * thread, so no extra locking needed.
 */
public final class OgrsPersistence {

	private static final Logger LOGGER = LogManager.getLogger(OgrsPersistence.class);

	private OgrsPersistence() {}

	// ─── Entry points ────────────────────────────────────────────────

	public static void loadAll(final World world) {
		final JDBCDatabase db = jdbc(world);
		if (db == null) {
			LOGGER.warn("OGRS persistence: no JDBC database — skipping load");
			return;
		}
		try {
			loadContracts(db);
			loadGuilds(db);
			loadPlots(db);
			LOGGER.info("OGRS persistence: loaded contracts/guilds/plots from DB");
		} catch (Exception ex) {
			LOGGER.error("OGRS persistence: load failed — registries remain empty", ex);
		}
	}

	public static void flushAll(final World world) {
		final JDBCDatabase db = jdbc(world);
		if (db == null) return;
		final Connection conn = db.getConnection().getConnection();
		boolean priorAutoCommit = true;
		try {
			priorAutoCommit = conn.getAutoCommit();
			conn.setAutoCommit(false);
			flushContracts(conn);
			flushGuilds(conn);
			flushPlots(conn);
			conn.commit();
		} catch (Exception ex) {
			try { conn.rollback(); } catch (SQLException ignored) {}
			LOGGER.error("OGRS persistence: flush failed — rolled back", ex);
		} finally {
			try { conn.setAutoCommit(priorAutoCommit); } catch (SQLException ignored) {}
		}
	}

	private static JDBCDatabase jdbc(final World world) {
		final Object db = world.getServer().getDatabase();
		return (db instanceof JDBCDatabase) ? (JDBCDatabase) db : null;
	}

	// ─── Load: contracts ─────────────────────────────────────────────

	private static void loadContracts(final JDBCDatabase db) throws SQLException {
		final List<Contract> contracts = new ArrayList<>();
		final Map<Integer, List<Item>> deliveryByContract = new HashMap<>();
		final Map<String, Integer> mentorPayouts = new HashMap<>();

		try (PreparedStatement ps = db.preparedStatement("SELECT * FROM ogrs_contracts");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				final Contract c = new Contract(
					rs.getInt("id"),
					Contract.Type.values()[rs.getInt("type")],
					rs.getString("poster_name"),
					rs.getInt("item_id"),
					rs.getInt("item_amount"),
					rs.getInt("gold_reward"),
					rs.getLong("created_ms"),
					rs.getLong("deadline_ms"));
				c.status = Contract.Status.values()[rs.getInt("status")];
				c.workerName = nonNull(rs.getString("worker_name"));
				c.acceptedEpochMs = rs.getLong("accepted_ms");
				c.completedEpochMs = rs.getLong("completed_ms");
				c.mentorSkillId = rs.getInt("mentor_skill_id");
				c.mentorMinLevel = rs.getInt("mentor_min_level");
				c.mentorDurationHrs = rs.getInt("mentor_duration_hrs");
				c.bondedTicksAccrued = rs.getLong("bonded_ticks_accrued");
				c.constructionFeatureTypeOrdinal = rs.getInt("construction_feature_type_ordinal");
				c.constructionPlotId = rs.getInt("construction_plot_id");
				c.constructionTargetX = rs.getInt("construction_target_x");
				c.constructionTargetY = rs.getInt("construction_target_y");
				contracts.add(c);
			}
		}

		try (PreparedStatement ps = db.preparedStatement(
				"SELECT contract_id, slot, item_id, amount, noted FROM ogrs_contract_delivery ORDER BY contract_id, slot");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				final int cid = rs.getInt("contract_id");
				deliveryByContract.computeIfAbsent(cid, k -> new ArrayList<>())
					.add(new Item(rs.getInt("item_id"), rs.getInt("amount"), rs.getInt("noted") != 0));
			}
		}

		try (PreparedStatement ps = db.preparedStatement("SELECT mentor_name, gold_pending FROM ogrs_contract_mentor_payouts");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				mentorPayouts.put(rs.getString("mentor_name"), rs.getInt("gold_pending"));
			}
		}

		final Map<Integer, Item[]> deliveryArrays = new HashMap<>();
		for (Map.Entry<Integer, List<Item>> e : deliveryByContract.entrySet()) {
			deliveryArrays.put(e.getKey(), e.getValue().toArray(new Item[0]));
		}
		ContractRegistry.loadFromPersistence(contracts, deliveryArrays, mentorPayouts);
	}

	// ─── Load: guilds ────────────────────────────────────────────────

	private static void loadGuilds(final JDBCDatabase db) throws SQLException {
		final Map<Integer, Guild> byId = new HashMap<>();

		try (PreparedStatement ps = db.preparedStatement("SELECT id, name, founder_name, created_ms, motto FROM ogrs_guilds");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				final int id = rs.getInt("id");
				// Guild ctor seeds the founder in members with FOUNDER role — we
				// overwrite the members map below from the members table.
				final Guild g = new Guild(id, rs.getString("name"), rs.getString("founder_name"));
				g.motto = nonNull(rs.getString("motto"));
				// Wipe the auto-seeded founder; loadGuildMembers fills it back.
				g.members.clear();
				byId.put(id, g);
			}
		}

		try (PreparedStatement ps = db.preparedStatement("SELECT guild_id, username, role FROM ogrs_guild_members");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				final Guild g = byId.get(rs.getInt("guild_id"));
				if (g == null) continue;
				g.members.put(rs.getString("username").toLowerCase(),
					Guild.Role.values()[rs.getInt("role")]);
			}
		}

		try (PreparedStatement ps = db.preparedStatement("SELECT guild_id, invitee, inviter FROM ogrs_guild_invites");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				final Guild g = byId.get(rs.getInt("guild_id"));
				if (g == null) continue;
				g.pendingInvites.put(rs.getString("invitee").toLowerCase(), rs.getString("inviter"));
			}
		}

		GuildRegistry.loadFromPersistence(new ArrayList<>(byId.values()));
	}

	// ─── Load: plots ─────────────────────────────────────────────────

	private static void loadPlots(final JDBCDatabase db) throws SQLException {
		final Map<Integer, String> deedHolders = new HashMap<>();
		final Map<Integer, Long> tenancyExpiry = new HashMap<>();
		final Map<Integer, Long> auctionEnds = new HashMap<>();
		final Map<Integer, Map<String, Integer>> bidsByPlot = new HashMap<>();
		final Map<Integer, List<PlotFeature>> featuresByPlot = new HashMap<>();

		try (PreparedStatement ps = db.preparedStatement(
				"SELECT id, deed_holder, tenancy_expires_ms, auction_ends_ms FROM ogrs_plots");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				final int id = rs.getInt("id");
				final String holder = rs.getString("deed_holder");
				deedHolders.put(id, holder == null || holder.isEmpty() ? null : holder);
				tenancyExpiry.put(id, rs.getLong("tenancy_expires_ms"));
				auctionEnds.put(id, rs.getLong("auction_ends_ms"));
			}
		}

		try (PreparedStatement ps = db.preparedStatement("SELECT plot_id, username, amount FROM ogrs_plot_bids");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				bidsByPlot.computeIfAbsent(rs.getInt("plot_id"), k -> new HashMap<>())
					.put(rs.getString("username").toLowerCase(), rs.getInt("amount"));
			}
		}

		try (PreparedStatement ps = db.preparedStatement(
				"SELECT plot_id, feature_type_ordinal, x, y, built_by, built_at_ms FROM ogrs_plot_features");
		     ResultSet rs = ps.executeQuery()) {
			while (rs.next()) {
				final int pid = rs.getInt("plot_id");
				final PlotFeature pf = new PlotFeature(pid,
					PlotFeature.Type.values()[rs.getInt("feature_type_ordinal")],
					rs.getInt("x"), rs.getInt("y"),
					rs.getString("built_by"),
					rs.getLong("built_at_ms"));
				featuresByPlot.computeIfAbsent(pid, k -> new ArrayList<>()).add(pf);
			}
		}

		PlotRegistry.loadFromPersistence(deedHolders, tenancyExpiry, auctionEnds, bidsByPlot, featuresByPlot);
	}

	// ─── Flush: contracts ────────────────────────────────────────────

	private static void flushContracts(final Connection conn) throws SQLException {
		exec(conn, "DELETE FROM ogrs_contracts");
		exec(conn, "DELETE FROM ogrs_contract_delivery");
		exec(conn, "DELETE FROM ogrs_contract_mentor_payouts");

		final List<Contract> contracts = ContractRegistry.snapshotAll();
		if (!contracts.isEmpty()) {
			try (PreparedStatement ps = conn.prepareStatement(
					"INSERT INTO ogrs_contracts(id, type, poster_name, worker_name, item_id, item_amount, gold_reward, status, " +
					"created_ms, deadline_ms, accepted_ms, completed_ms, mentor_skill_id, mentor_min_level, mentor_duration_hrs, " +
					"bonded_ticks_accrued, construction_feature_type_ordinal, construction_plot_id, construction_target_x, construction_target_y) " +
					"VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")) {
				for (Contract c : contracts) {
					ps.setInt   (1,  c.id);
					ps.setInt   (2,  c.type.ordinal());
					ps.setString(3,  c.posterName);
					ps.setString(4,  c.workerName == null ? "" : c.workerName);
					ps.setInt   (5,  c.itemId);
					ps.setInt   (6,  c.itemAmount);
					ps.setInt   (7,  c.goldReward);
					ps.setInt   (8,  c.status.ordinal());
					ps.setLong  (9,  c.createdEpochMs);
					ps.setLong  (10, c.deadlineEpochMs);
					ps.setLong  (11, c.acceptedEpochMs);
					ps.setLong  (12, c.completedEpochMs);
					ps.setInt   (13, c.mentorSkillId);
					ps.setInt   (14, c.mentorMinLevel);
					ps.setInt   (15, c.mentorDurationHrs);
					ps.setLong  (16, c.bondedTicksAccrued);
					ps.setInt   (17, c.constructionFeatureTypeOrdinal);
					ps.setInt   (18, c.constructionPlotId);
					ps.setInt   (19, c.constructionTargetX);
					ps.setInt   (20, c.constructionTargetY);
					ps.addBatch();
				}
				ps.executeBatch();
			}
		}

		final Map<Integer, Item[]> deliveries = ContractRegistry.snapshotDeliveries();
		if (!deliveries.isEmpty()) {
			try (PreparedStatement ps = conn.prepareStatement(
					"INSERT INTO ogrs_contract_delivery(contract_id, slot, item_id, amount, noted) VALUES (?,?,?,?,?)")) {
				for (Map.Entry<Integer, Item[]> e : deliveries.entrySet()) {
					final int cid = e.getKey();
					final Item[] items = e.getValue();
					if (items == null) continue;
					for (int slot = 0; slot < items.length; slot++) {
						final Item it = items[slot];
						if (it == null) continue;
						ps.setInt(1, cid);
						ps.setInt(2, slot);
						ps.setInt(3, it.getCatalogId());
						ps.setInt(4, it.getAmount());
						ps.setInt(5, it.getNoted() ? 1 : 0);
						ps.addBatch();
					}
				}
				ps.executeBatch();
			}
		}

		final Map<String, Integer> payouts = ContractRegistry.snapshotMentorPayouts();
		if (!payouts.isEmpty()) {
			try (PreparedStatement ps = conn.prepareStatement(
					"INSERT INTO ogrs_contract_mentor_payouts(mentor_name, gold_pending) VALUES (?,?)")) {
				for (Map.Entry<String, Integer> e : payouts.entrySet()) {
					ps.setString(1, e.getKey());
					ps.setInt(2, e.getValue());
					ps.addBatch();
				}
				ps.executeBatch();
			}
		}
	}

	// ─── Flush: guilds ───────────────────────────────────────────────

	private static void flushGuilds(final Connection conn) throws SQLException {
		exec(conn, "DELETE FROM ogrs_guild_invites");
		exec(conn, "DELETE FROM ogrs_guild_members");
		exec(conn, "DELETE FROM ogrs_guilds");

		final List<Guild> guilds = GuildRegistry.listAll();
		if (guilds.isEmpty()) return;

		try (PreparedStatement ps = conn.prepareStatement(
				"INSERT INTO ogrs_guilds(id, name, founder_name, created_ms, motto) VALUES (?,?,?,?,?)")) {
			for (Guild g : guilds) {
				ps.setInt   (1, g.id);
				ps.setString(2, g.name);
				ps.setString(3, g.founderUsername);
				ps.setLong  (4, g.createdEpochMs);
				ps.setString(5, g.motto == null ? "" : g.motto);
				ps.addBatch();
			}
			ps.executeBatch();
		}

		try (PreparedStatement ps = conn.prepareStatement(
				"INSERT INTO ogrs_guild_members(guild_id, username, role) VALUES (?,?,?)")) {
			for (Guild g : guilds) {
				for (Map.Entry<String, Guild.Role> e : g.members.entrySet()) {
					ps.setInt   (1, g.id);
					ps.setString(2, e.getKey());
					ps.setInt   (3, e.getValue().ordinal());
					ps.addBatch();
				}
			}
			ps.executeBatch();
		}

		try (PreparedStatement ps = conn.prepareStatement(
				"INSERT INTO ogrs_guild_invites(guild_id, invitee, inviter) VALUES (?,?,?)")) {
			boolean any = false;
			for (Guild g : guilds) {
				for (Map.Entry<String, String> e : g.pendingInvites.entrySet()) {
					ps.setInt   (1, g.id);
					ps.setString(2, e.getKey());
					ps.setString(3, e.getValue());
					ps.addBatch();
					any = true;
				}
			}
			if (any) ps.executeBatch();
		}
	}

	// ─── Flush: plots ────────────────────────────────────────────────

	private static void flushPlots(final Connection conn) throws SQLException {
		exec(conn, "DELETE FROM ogrs_plot_features");
		exec(conn, "DELETE FROM ogrs_plot_bids");
		exec(conn, "DELETE FROM ogrs_plots");

		final List<Plot> plots = PlotRegistry.listAll();
		if (plots.isEmpty()) return;

		try (PreparedStatement ps = conn.prepareStatement(
				"INSERT INTO ogrs_plots(id, deed_holder, tenancy_expires_ms, auction_ends_ms) VALUES (?,?,?,?)")) {
			for (Plot p : plots) {
				ps.setInt   (1, p.id);
				ps.setString(2, p.deedHolder == null ? "" : p.deedHolder);
				ps.setLong  (3, p.tenancyExpiresMs);
				ps.setLong  (4, p.auctionEndsMs);
				ps.addBatch();
			}
			ps.executeBatch();
		}

		try (PreparedStatement ps = conn.prepareStatement(
				"INSERT INTO ogrs_plot_bids(plot_id, username, amount) VALUES (?,?,?)")) {
			boolean any = false;
			for (Plot p : plots) {
				for (Map.Entry<String, Integer> e : p.openBids.entrySet()) {
					ps.setInt   (1, p.id);
					ps.setString(2, e.getKey());
					ps.setInt   (3, e.getValue());
					ps.addBatch();
					any = true;
				}
			}
			if (any) ps.executeBatch();
		}

		try (PreparedStatement ps = conn.prepareStatement(
				"INSERT INTO ogrs_plot_features(plot_id, feature_type_ordinal, x, y, built_by, built_at_ms) VALUES (?,?,?,?,?,?)")) {
			boolean any = false;
			for (Plot p : plots) {
				for (PlotFeature pf : p.features.values()) {
					ps.setInt   (1, p.id);
					ps.setInt   (2, pf.type.ordinal());
					ps.setInt   (3, pf.x);
					ps.setInt   (4, pf.y);
					ps.setString(5, pf.builtBy == null ? "" : pf.builtBy);
					ps.setLong  (6, pf.builtAtMs);
					ps.addBatch();
					any = true;
				}
			}
			if (any) ps.executeBatch();
		}
	}

	// ─── Utility ─────────────────────────────────────────────────────

	private static void exec(final Connection conn, final String sql) throws SQLException {
		try (PreparedStatement ps = conn.prepareStatement(sql)) {
			ps.executeUpdate();
		}
	}

	private static String nonNull(final String s) { return s == null ? "" : s; }
}

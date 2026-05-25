-- OGRS — persistence schema for the social/housing/contract arc.
--
-- Tables cover the three in-memory registries:
--   ContractRegistry → ogrs_contracts + ogrs_contract_delivery + ogrs_contract_mentor_payouts
--   GuildRegistry    → ogrs_guilds + ogrs_guild_members + ogrs_guild_invites
--   PlotRegistry     → ogrs_plots + ogrs_plot_bids + ogrs_plot_features
--
-- Strategy: the persistence layer does a periodic full DELETE + INSERT
-- per registry inside a single transaction. Row counts are small
-- (dozens to low hundreds total) and the registry is the source of
-- truth in memory — DB is a snapshot for restart recovery.
--
-- All CREATE TABLE statements use IF NOT EXISTS so the patch is
-- idempotent (re-running is harmless).

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_contracts` (
    `id`                                INT          NOT NULL,
    `type`                              TINYINT      NOT NULL,
    `poster_name`                       VARCHAR(20)  NOT NULL,
    `worker_name`                       VARCHAR(20)  NOT NULL DEFAULT '',
    `item_id`                           INT          NOT NULL DEFAULT -1,
    `item_amount`                       INT          NOT NULL DEFAULT 0,
    `gold_reward`                       INT          NOT NULL DEFAULT 0,
    `status`                            TINYINT      NOT NULL DEFAULT 0,
    `created_ms`                        BIGINT       NOT NULL,
    `deadline_ms`                       BIGINT       NOT NULL,
    `accepted_ms`                       BIGINT       NOT NULL DEFAULT 0,
    `completed_ms`                      BIGINT       NOT NULL DEFAULT 0,
    `mentor_skill_id`                   INT          NOT NULL DEFAULT -1,
    `mentor_min_level`                  INT          NOT NULL DEFAULT 0,
    `mentor_duration_hrs`               INT          NOT NULL DEFAULT 0,
    `bonded_ticks_accrued`              BIGINT       NOT NULL DEFAULT 0,
    `construction_feature_type_ordinal` INT          NOT NULL DEFAULT -1,
    `construction_plot_id`              INT          NOT NULL DEFAULT -1,
    `construction_target_x`             INT          NOT NULL DEFAULT -1,
    `construction_target_y`             INT          NOT NULL DEFAULT -1,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_contract_delivery` (
    `contract_id` INT     NOT NULL,
    `slot`        INT     NOT NULL,
    `item_id`     INT     NOT NULL,
    `amount`      INT     NOT NULL,
    `noted`       TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (`contract_id`, `slot`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_contract_mentor_payouts` (
    `mentor_name`  VARCHAR(20) NOT NULL,
    `gold_pending` INT         NOT NULL,
    PRIMARY KEY (`mentor_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_guilds` (
    `id`            INT          NOT NULL,
    `name`          VARCHAR(50)  NOT NULL,
    `founder_name`  VARCHAR(20)  NOT NULL,
    `created_ms`    BIGINT       NOT NULL,
    `motto`         VARCHAR(200) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    UNIQUE KEY `ogrs_guilds_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_guild_members` (
    `guild_id`  INT         NOT NULL,
    `username`  VARCHAR(20) NOT NULL,
    `role`      TINYINT     NOT NULL,
    PRIMARY KEY (`guild_id`, `username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_guild_invites` (
    `guild_id` INT         NOT NULL,
    `invitee`  VARCHAR(20) NOT NULL,
    `inviter`  VARCHAR(20) NOT NULL,
    PRIMARY KEY (`guild_id`, `invitee`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_plots` (
    `id`                  INT         NOT NULL,
    `deed_holder`         VARCHAR(50) NOT NULL DEFAULT '',
    `tenancy_expires_ms`  BIGINT      NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_plot_bids` (
    `plot_id`  INT         NOT NULL,
    `username` VARCHAR(20) NOT NULL,
    `amount`   INT         NOT NULL,
    PRIMARY KEY (`plot_id`, `username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_plot_features` (
    `plot_id`              INT         NOT NULL,
    `feature_type_ordinal` TINYINT     NOT NULL,
    `x`                    INT         NOT NULL,
    `y`                    INT         NOT NULL,
    `built_by`             VARCHAR(20) NOT NULL,
    `built_at_ms`          BIGINT      NOT NULL,
    PRIMARY KEY (`plot_id`, `x`, `y`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

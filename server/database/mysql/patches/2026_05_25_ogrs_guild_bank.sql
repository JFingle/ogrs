-- OGRS — guild treasury (gold-only v1).
--
-- One row per guild storing the shared gold balance. Item storage
-- (banked items, withdrawal caps, audit log) is a future phase
-- once an in-client UI panel exists.

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_guild_bank` (
    `guild_id`     INT    NOT NULL,
    `gold_balance` BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

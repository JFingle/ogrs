-- OGRS — bounty contracts.
--
-- Two additions:
--   1. Add bounty_target_name to ogrs_contracts so BOUNTY contracts
--      remember who they're hunting across restarts.
--   2. Create ogrs_contract_bounty_payouts for the killer's pending
--      gold queue (mirrors ogrs_contract_mentor_payouts).

DROP PROCEDURE IF EXISTS `?`;
DELIMITER //
CREATE PROCEDURE `?`()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN END;
ALTER TABLE `_PREFIX_ogrs_contracts` ADD COLUMN `bounty_target_name` VARCHAR(20) NOT NULL DEFAULT '';
END //
DELIMITER ;
CALL `?`();
DROP PROCEDURE `?`;

CREATE TABLE IF NOT EXISTS `_PREFIX_ogrs_contract_bounty_payouts` (
    `killer_name`  VARCHAR(20) NOT NULL,
    `gold_pending` INT         NOT NULL,
    PRIMARY KEY (`killer_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

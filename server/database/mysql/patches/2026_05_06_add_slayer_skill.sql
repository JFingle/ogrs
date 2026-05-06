-- OGRS Slayer skill — add the column to every table that has a per-skill column
-- list. Skill name MUST match Skills.java's SkillDef short-name lowercased
-- ("slayer"), since MySqlQueries.java builds queries by iterating skills and
-- using `skill.getShortName().toLowerCase()`.
--
-- Each ALTER TABLE is wrapped in its own stored procedure with a CONTINUE
-- HANDLER for SQLEXCEPTION so the patch is idempotent — re-running on a DB
-- that already has the column is a no-op.

-- experience
DROP PROCEDURE IF EXISTS `?`;
DELIMITER //
CREATE PROCEDURE `?`()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN END;
ALTER TABLE `_PREFIX_experience` ADD COLUMN `slayer` INT(9) NOT NULL DEFAULT 0;
END //
DELIMITER ;
CALL `?`();
DROP PROCEDURE `?`;

-- curstats
DROP PROCEDURE IF EXISTS `?`;
DELIMITER //
CREATE PROCEDURE `?`()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN END;
ALTER TABLE `_PREFIX_curstats` ADD COLUMN `slayer` TINYINT(3) UNSIGNED NOT NULL DEFAULT 1;
END //
DELIMITER ;
CALL `?`();
DROP PROCEDURE `?`;

-- maxstats
DROP PROCEDURE IF EXISTS `?`;
DELIMITER //
CREATE PROCEDURE `?`()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN END;
ALTER TABLE `_PREFIX_maxstats` ADD COLUMN `slayer` TINYINT(3) UNSIGNED NOT NULL DEFAULT 1;
END //
DELIMITER ;
CALL `?`();
DROP PROCEDURE `?`;

-- capped_experience
DROP PROCEDURE IF EXISTS `?`;
DELIMITER //
CREATE PROCEDURE `?`()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN END;
ALTER TABLE `_PREFIX_capped_experience` ADD COLUMN `slayer` INT(10) UNSIGNED;
END //
DELIMITER ;
CALL `?`();
DROP PROCEDURE `?`;

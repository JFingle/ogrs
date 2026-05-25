-- OGRS — add auction_ends_ms to ogrs_plots.
--
-- Tracks when the bidding window closes for a vacant plot. 0 = no
-- countdown yet (no bids placed since the plot became vacant). The
-- first bid on a vacant plot sets this to now + 24h; the per-minute
-- PlotAuctionTick closes the auction when now >= this value.
--
-- Wrapped in a stored procedure with CONTINUE HANDLER so re-running
-- the patch is harmless (column-exists raises a SQLEXCEPTION which
-- the handler swallows).

DROP PROCEDURE IF EXISTS `?`;
DELIMITER //
CREATE PROCEDURE `?`()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN END;
ALTER TABLE `_PREFIX_ogrs_plots` ADD COLUMN `auction_ends_ms` BIGINT NOT NULL DEFAULT 0;
END //
DELIMITER ;
CALL `?`();
DROP PROCEDURE `?`;

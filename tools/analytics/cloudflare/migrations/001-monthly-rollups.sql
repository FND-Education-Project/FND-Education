-- One-time, additive migration for the EXISTING anonymous analytics D1.
-- Apply and verify before enabling the maintenance Worker.
-- Counters remain grouped by period, event and broad section.
CREATE TABLE IF NOT EXISTS monthly_counts (
  month TEXT NOT NULL CHECK(length(month) = 7),
  event TEXT NOT NULL,
  section TEXT NOT NULL,
  total INTEGER NOT NULL DEFAULT 0 CHECK(total >= 0),
  PRIMARY KEY (month, event, section)
) WITHOUT ROWID;

-- Anonymous daily counters only. No visitor table, raw hits or search text.
CREATE TABLE IF NOT EXISTS daily_counts (
    day TEXT NOT NULL CHECK(length(day) = 10),
    event TEXT NOT NULL,
    section TEXT NOT NULL,
    total INTEGER NOT NULL DEFAULT 0 CHECK(total >= 0),
    PRIMARY KEY (day, event, section)
) WITHOUT ROWID;

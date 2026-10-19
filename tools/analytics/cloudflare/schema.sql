-- Anonymous daily counters only. No visitor table, raw hits or search text.
CREATE TABLE IF NOT EXISTS daily_counts (
    day TEXT NOT NULL CHECK(length(day) = 10),
    event TEXT NOT NULL,
    section TEXT NOT NULL,
    total INTEGER NOT NULL DEFAULT 0 CHECK(total >= 0),
    PRIMARY KEY (day, event, section)
) WITHOUT ROWID;
\n-- Archive summary of complete months older than approximately four months.\nCREATE TABLE IF NOT EXISTS monthly_counts (\n    month TEXT NOT NULL CHECK(length(month) = 7),\n    event TEXT NOT NULL,\n    section TEXT NOT NULL,\n    total INTEGER NOT NULL DEFAULT 0 CHECK(total >= 0),\n    PRIMARY KEY (month, event, section)\n) WITHOUT ROWID;\n
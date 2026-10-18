-- FND Education — isolated learner database. Never reuse the analytics D1.
-- All IDs are opaque random UUIDs, never emails or provider profile IDs.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS learners (
  id TEXT PRIMARY KEY,
  username TEXT NOT NULL,
  theme TEXT NOT NULL DEFAULT 'system'
    CHECK (theme IN ('system', 'light', 'dark')),
  idle_minutes INTEGER NOT NULL DEFAULT 0
    CHECK (idle_minutes IN (0, 15, 60, 1440, 10080)),
  last_lesson TEXT,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS identities (
  provider TEXT NOT NULL CHECK (provider IN ('google', 'apple')),
  subject TEXT NOT NULL,
  learner_id TEXT NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  PRIMARY KEY (provider, subject)
);

CREATE TABLE IF NOT EXISTS learner_progress (
  learner_id TEXT NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  lesson_id TEXT NOT NULL,
  visited INTEGER NOT NULL DEFAULT 0 CHECK (visited IN (0, 1)),
  completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1)),
  updated_at INTEGER NOT NULL,
  PRIMARY KEY (learner_id, lesson_id)
);

-- Store session hashes, not bearer credentials. Every data request
-- resolves its account exclusively from the authenticated session.
CREATE TABLE IF NOT EXISTS learner_sessions (
  token_hash TEXT PRIMARY KEY,
  learner_id TEXT NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  csrf_token TEXT NOT NULL,
  expires_at INTEGER NOT NULL,
  last_active INTEGER NOT NULL,
  created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_learner_sessions_expiry
  ON learner_sessions(expires_at);

CREATE TABLE IF NOT EXISTS oauth_flows (
  state_hash TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  pkce_verifier TEXT NOT NULL,
  nonce TEXT NOT NULL,
  return_path TEXT NOT NULL,
  expires_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_oauth_flows_expiry
  ON oauth_flows(expires_at);

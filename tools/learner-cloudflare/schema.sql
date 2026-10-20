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
  created_at INTEGER NOT NULL,
  -- Updated after authenticated use, separate from optional idle sign-out.
  last_seen_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_learners_last_seen
  ON learners(last_seen_at);

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

-- Additive and repeatable: apply to the EXISTING isolated learner database.
-- Never rebuild identities or remove existing Google accounts/progress.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS learner_emails (
  email TEXT PRIMARY KEY,
  learner_id TEXT NOT NULL UNIQUE REFERENCES learners(id) ON DELETE CASCADE,
  verified_at INTEGER NOT NULL
);
-- Pending addresses expire quickly; codes and browser credentials are never
-- stored in plaintext. A linked flow dies when its owning session is revoked.
CREATE TABLE IF NOT EXISTS email_challenges (
  id TEXT PRIMARY KEY,
  browser_hash TEXT NOT NULL,
  email TEXT NOT NULL,
  username TEXT NOT NULL,
  code_hash TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  link_session TEXT REFERENCES learner_sessions(token_hash) ON DELETE CASCADE,
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_email_challenges_expiry ON email_challenges(expires_at);
-- Short-lived, keyed hashes protect rate-limit identifiers from disclosure.
-- Global usage buckets contain only aggregate sending counts.
CREATE TABLE IF NOT EXISTS email_limits (
  bucket TEXT PRIMARY KEY,
  used INTEGER NOT NULL,
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_email_limits_expiry ON email_limits(expires_at);

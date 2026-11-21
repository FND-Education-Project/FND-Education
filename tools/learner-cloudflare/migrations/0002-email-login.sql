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

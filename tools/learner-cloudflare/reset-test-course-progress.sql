-- Controlled test-data reset for the new 19-module/57-lesson curriculum.
-- This is NOT a production database migration and must never be scheduled.
-- Run ONLY with the repository owner's explicit approval, after exporting
-- any test accounts whose learning-progress flags should be saved.
-- Database: fnd-learner-accounts. NEVER run against anonymous statistics D1.
-- Existing learner accounts, verified email identities, preferences,
-- secure sessions and personal account names remain untouched.
--
-- Old mN-K identifiers (notably m6-1) had different topic meanings;
-- all test completion rows and resume pointers are intentionally discarded.
DELETE FROM learner_progress;
UPDATE learners SET last_lesson = NULL;

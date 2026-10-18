/**
 * FND anonymous analytics: nightly, additive daily-to-monthly rollup.
 *
 * This is a SEPARATE maintenance Worker with no public API. The live event
 * receiver and private dashboard remain unchanged. It is safe to execute
 * repeatedly: monthly increments and source-row deletion are atomic.
 *
 * Only complete months older than ~120 days are combined, so last-90-day
 * dashboards keep their full daily resolution. SUM retains event + section.
 * Never use visitor identifiers, IP addresses, or account data.
 */
const RETAIN_DAILY_DAYS = 120;

export function rollupCutoff(timestamp = Date.now()) {
  const earlier = new Date(timestamp - RETAIN_DAILY_DAYS * 86400000);
  return earlier.toISOString().slice(0, 7) + "-01";
}

export async function rollup(db, timestamp = Date.now()) {
  if (!db || typeof db.prepare !== "function" ||
      typeof db.batch !== "function") {
    throw new Error("Database binding unavailable");
  }
  const cutoff = rollupCutoff(timestamp);
  // D1.batch executes statements in one transaction: failure rolls back
  // BOTH changes. Retrying cannot count the same daily row twice.
  const statements = [
    db.prepare(
      "INSERT INTO monthly_counts (month, event, section, total) " +
      "SELECT substr(day, 1, 7), event, section, SUM(total) " +
      "FROM daily_counts WHERE day < ?1 " +
      "GROUP BY substr(day, 1, 7), event, section " +
      "ON CONFLICT(month, event, section) DO UPDATE SET " +
      "total = monthly_counts.total + excluded.total"
    ).bind(cutoff),
    db.prepare("DELETE FROM daily_counts WHERE day < ?1").bind(cutoff)
  ];
  const result = await db.batch(statements);
  if (!Array.isArray(result) || result.length !== 2 ||
      result.some(entry => entry.success === false)) {
    throw new Error("Analytics rollup transaction failed");
  }
  return { cutoff, migrated: Number(result[1].meta?.changes || 0) };
}

export default {
  // Deliberately refuse HTTP access, including health/debug endpoints.
  async fetch() {
    return new Response(null, { status: 404 });
  },
  async scheduled(_event, env, ctx) {
    ctx.waitUntil(rollup(env.DB).catch(() => {
      // Cloudflare invocation reports failure without publishing any data.
      // Never log visitor activity, analytics raw payloads or DB values.
      throw new Error("Nightly analytics rollup failed");
    }));
  }
};

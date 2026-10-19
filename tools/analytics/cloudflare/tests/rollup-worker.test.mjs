import test from "node:test";
import assert from "node:assert/strict";
import worker, { rollupCutoff, rollup } from "../src/rollup-worker.mjs";

test("only complete months older than 120 days are eligible", () => {
  assert.equal(rollupCutoff(Date.UTC(2026, 9, 18)), "2026-06-01");
});

test("monthly writes and daily deletes share a two-query transaction", async () => {
  const queries = [];
  const db = {
    prepare(sql) {
      return { bind(...args) { return { sql, args }; } };
    },
    async batch(items) {
      queries.push(...items);
      return [{ success: true }, { success: true, meta: { changes: 15 } }];
    }
  };
  const result = await rollup(db, Date.UTC(2026, 9, 18));
  assert.deepEqual(result, { cutoff: "2026-06-01", migrated: 15 });
  assert.equal(queries.length, 2);
  assert.match(queries[0].sql, /SUM\(total\)/);
  assert.match(queries[0].sql, /ON CONFLICT\(month, event, section\)/);
  assert.match(queries[0].sql, /total = monthly_counts\.total \+ excluded\.total/);
  assert.match(queries[1].sql, /^DELETE FROM daily_counts/);
  assert.deepEqual(queries.map(x => x.args), [["2026-06-01"], ["2026-06-01"]]);
});

test("rollup fails closed if database is missing or transaction fails", async () => {
  await assert.rejects(rollup(null), /Database binding unavailable/);
  const db = {
    prepare(sql) { return { bind() { return { sql }; } }; },
    async batch() { return [{ success: false }, { success: true }]; }
  };
  await assert.rejects(rollup(db), /transaction failed/);
});

test("maintenance does not expose an HTTP API", async () => {
  const response = await worker.fetch();
  assert.equal(response.status, 404);
});

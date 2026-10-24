/** Behavioral tests execute the Worker against SQLite and mocked providers.
 * No real secrets, network email delivery or production database are used.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import worker from './worker.js';
import { normalizeEmail } from './email-auth.js';
const origin = 'https://fndeducationproject.org';
const api = 'https://accounts.fndeducationproject.org';
const schema = readFileSync(new URL('./schema.sql', import.meta.url), 'utf8');
const migration = readFileSync(new URL('./migrations/0002-email-login.sql', import.meta.url), 'utf8');

/** Minimal D1 adapter: run actual SQL, including constraints and transactions. */
function database() {
  const sqlite = new DatabaseSync(':memory:');
  sqlite.exec(schema);
  function prepare(sql) {
    let values = [];
    const statement = {
      bind(...args) { values = args; return statement; },
      async first() { return sqlite.prepare(sql).get(...values) || null; },
      async all() { return { results: sqlite.prepare(sql).all(...values) }; },
      async run() { return { success: true, meta: sqlite.prepare(sql).run(...values) }; },
      execute() { return sqlite.prepare(sql).run(...values); }
    };
    return statement;
  }
  return { sqlite, prepare, async batch(statements) {
    sqlite.exec('BEGIN');
    try { const result = statements.map(s => s.execute()); sqlite.exec('COMMIT'); return result; }
    catch (error) { sqlite.exec('ROLLBACK'); throw error; }
  } };
}
function setup(t) {
  const DB = database();
  t.after(() => DB.sqlite.close());
  const env = { DB, PUBLIC_ORIGIN: origin, API_ORIGIN: api, EMAIL_LOGIN_ENABLED: 'true',
    RESEND_API_KEY: 're_test_only', EMAIL_AUTH_SECRET: 'test-only-secret-with-more-than-32-characters',
    EMAIL_FROM: 'login@mail.fndeducationproject.org', TURNSTILE_SITE_KEY: 'test', TURNSTILE_SECRET_KEY: 'test' };
  const sent = [];
  let bot = false, deliveryFails = false, verificationUnavailable = false, malformedVerification = false, verificationRedirected = false, resendRedirected = false;
  t.mock.method(globalThis, 'fetch', async (url, init) => {
    if (url.includes('siteverify')) {
      assert.equal(init.redirect, 'manual');
      assert.ok(init.signal instanceof AbortSignal);
      if (verificationUnavailable) throw new Error('private verification service exception');
      if (malformedVerification) return new Response('invalid non-JSON response');
      if (verificationRedirected) return new Response(null, { status: 302,
        headers: { Location: 'https://not-turnstile.example.invalid/' } });
      return Response.json({ success: !bot,
        hostname: new URL(origin).hostname, action: 'email_login' });
    }
    assert.equal(url, 'https://api.resend.com/emails');
    assert.equal(init.redirect, 'manual');
    assert.ok(init.headers['Idempotency-Key']);
    if (resendRedirected) return new Response(null, { status: 302,
      headers: { Location: 'https://not-resend.example.invalid/' } });
    if (deliveryFails) return Response.json({ error: 'private provider error' }, { status: 500 });
    sent.push(JSON.parse(init.body));
    return Response.json({ id: 'mail-test' });
  });
  async function call(path, body, cookies = '', csrf = '', requestOrigin = origin) {
    return worker.fetch(new Request(api + path, { method: body ? 'POST' : 'GET',
      headers: { Origin: requestOrigin, 'Content-Type': 'application/json',
        Cookie: cookies, 'X-FND-CSRF': csrf, 'CF-Connecting-IP': '192.0.2.1' },
      body: body ? JSON.stringify(body) : undefined }), env);
  }
  async function start(email = 'person@example.com', options = {}) {
    const response = await call(options.link ? '/v1/account/email/start' : '/v1/auth/email/start',
      { email, username: 'Test learner', turnstileToken: 'human-token' }, options.cookie, options.csrf);
    const data = await response.json();
    return { response, data, cookie: response.headers.get('Set-Cookie')?.split(';')[0],
      code: sent.at(-1)?.text.match(/Your code is: (\d{8})/)[1] };
  }
  async function finish(flow, overrides = {}, cookies = flow.cookie, path = '/v1/auth/email/verify', csrf = '') {
    return call(path, { challengeId: flow.data.challengeId, code: flow.code, ...overrides }, cookies, csrf);
  }
  return { env, DB, sent, call, start, finish, setBot: v => { bot = v; },
    setFailure: v => { deliveryFails = v; },
    setVerificationUnavailable: v => { verificationUnavailable = v; },
    setMalformedVerification: v => { malformedVerification = v; },
    setVerificationRedirected: v => { verificationRedirected = v; },
    setResendRedirected: v => { resendRedirected = v; } };
}
function sessionCookie(response) {
  return response.headers.getSetCookie().find(c => c.startsWith('__Host-fnd_learner_session='))?.split(';')[0];
}

test('normalization preserves plus aliases and rejects header injection', () => {
  assert.equal(normalizeEmail(' Person+study@Example.com '), 'person+study@example.com');
  for (const email of ['a\r\nBcc: x@y.com', 'a..b@example.com', 'a@-bad.com', 'a@x..com', null]) {
    assert.equal(normalizeEmail(email), null);
  }
});

test('email signup verifies ownership, ignores replay, persists progress across sign-ins', async t => {
  const s = setup(t), flow = await s.start();
  assert.equal(flow.response.status, 200);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learners').get().n, 0);
  const challenge = s.DB.sqlite.prepare('SELECT * FROM email_challenges').get();
  assert.notEqual(challenge.code_hash, flow.code);
  assert.ok(!JSON.stringify(flow.data).includes(flow.code));
  const result = await s.finish(flow);
  assert.equal(result.status, 200);
  const cookie = sessionCookie(result);
  assert.ok(cookie);
  const me = await (await s.call('/v1/me', null, cookie)).json();
  assert.equal(me.username, 'Test learner');
  assert.equal((await s.finish(flow)).status, 400);
  assert.equal((await s.call('/v1/progress/completion', { lessonId: 'm1-1', completed: true,
    confirmed: true, confirmedUsername: me.username }, cookie, me.csrfToken)).status, 200);
  // Advance only the rate bucket for this test; production waits for expiry.
  s.DB.sqlite.exec('DELETE FROM email_limits');
  const second = await s.start('PERSON@example.com');
  const again = await s.finish(second);
  const progress = await (await s.call('/v1/progress', null, sessionCookie(again))).json();
  assert.equal(progress.lessons['m1-1'].completed, true);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learners').get().n, 1);
});

test('code is bound to original browser, exact origin, expiry and five guesses', async t => {
  const s = setup(t), flow = await s.start();
  assert.equal((await s.finish(flow, {}, '__Host-fnd_email_flow=wrong')).status, 400);
  const evil = await s.call('/v1/auth/email/verify', { challengeId: flow.data.challengeId, code: flow.code }, flow.cookie, '', 'https://evil.example');
  assert.equal(evil.status, 403);
  const wrong = flow.code === '00000000' ? '00000001' : '00000000';
  for (let n = 0; n < 5; n++) assert.equal((await s.finish(flow, { code: wrong })).status, 400);
  assert.equal((await s.finish(flow)).status, 400);
  s.DB.sqlite.exec('DELETE FROM email_limits');
  const expired = await s.start();
  s.DB.sqlite.exec('UPDATE email_challenges SET expires_at = 0');
  assert.equal((await s.finish(expired)).status, 400);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learners').get().n, 0);
});

test('missing config, bot failures and quotas prevent delivery', async t => {
  const s = setup(t);
  s.env.EMAIL_LOGIN_ENABLED = 'false';
  assert.equal((await s.start()).response.status, 503);
  s.env.EMAIL_LOGIN_ENABLED = 'true';
  s.setBot(true);
  assert.equal((await s.start()).response.status, 400);
  assert.equal(s.sent.length, 0);
  s.setBot(false);
  assert.equal((await s.start()).response.status, 200);
  assert.equal((await s.start()).response.status, 429);
  assert.equal(s.sent.length, 1);
  // Exercise aggregate daily budget across different addresses/IPs.
  s.DB.sqlite.exec("UPDATE email_limits SET used = 90 WHERE bucket LIKE 'global-day:%'");
  assert.equal((await s.start('other@example.com')).response.status, 429);
  assert.equal(s.sent.length, 1);
});

test('delivery failure invalidates challenge without exposing provider detail', async t => {
  const s = setup(t); s.setFailure(true);
  const flow = await s.start();
  assert.equal(flow.response.status, 503);
  assert.doesNotMatch(JSON.stringify(flow.data), /private provider|re_test_only/);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM email_challenges').get().n, 0);
});

test('concurrent verification consumes a challenge once', async t => {
  const s = setup(t), flow = await s.start();
  const results = await Promise.all([s.finish(flow), s.finish(flow)]);
  assert.deepEqual(results.map(r => r.status).sort(), [200, 400]);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learners').get().n, 1);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learner_sessions').get().n, 1);
});

test('independent concurrent signup flows create only one learner', async t => {
  const s = setup(t), a = await s.start();
  s.DB.sqlite.exec('DELETE FROM email_limits');
  const b = await s.start();
  const results = await Promise.all([s.finish(a), s.finish(b)]);
  assert.deepEqual(results.map(r => r.status), [200, 200]);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learners').get().n, 1);
});

test('link email to Google account requires session and CSRF; conflict never merges accounts', async t => {
  const s = setup(t);
  const t0 = Math.floor(Date.now() / 1000);
  // Seed a Google-owned account as if its OAuth exchange had completed.
  s.DB.sqlite.prepare('INSERT INTO learners (id,username,created_at,last_seen_at) VALUES (?,?,?,?)')
    .run('google-owner', 'Google learner', t0, t0);
  s.DB.sqlite.prepare('INSERT INTO identities VALUES (?,?,?)').run('google', 'subject', 'google-owner');
  const raw = 'google-session';
  const hash = Buffer.from(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(raw))).toString('hex');
  s.DB.sqlite.prepare('INSERT INTO learner_sessions VALUES (?,?,?,?,?,?)')
    .run(hash, 'google-owner', 'csrf', t0 + 1000, t0, t0);
  const cookie = '__Host-fnd_learner_session=' + raw;
  assert.equal((await s.start('link@example.com', { link: true, cookie })).response.status, 403);
  const link = await s.start('link@example.com', { link: true, cookie, csrf: 'csrf' });
  assert.equal(link.response.status, 200);
  assert.equal((await s.finish(link)).status, 400); // Can't redeem a linking flow as a guest.
  const linked = await s.finish(link, {}, cookie + '; ' + link.cookie, '/v1/account/email/verify', 'csrf');
  assert.equal(linked.status, 200);
  assert.equal(s.DB.sqlite.prepare('SELECT learner_id FROM learner_emails').get().learner_id, 'google-owner');
  s.DB.sqlite.exec('DELETE FROM email_limits');
  const login = await s.start('link@example.com');
  assert.equal((await s.finish(login)).status, 200);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learners').get().n, 1);
  s.DB.sqlite.exec('DELETE FROM email_limits');
  const other = await s.start('other@example.com');
  await s.finish(other);
  s.DB.sqlite.exec('DELETE FROM email_limits');
  const conflict = await s.start('other@example.com', { link: true, cookie, csrf: 'csrf' });
  assert.equal((await s.finish(conflict, {}, cookie + '; ' + conflict.cookie, '/v1/account/email/verify', 'csrf')).status, 409);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learners').get().n, 2);
});

test('migration preserves existing progress, repeats safely, and deletion cascades email', async t => {
  const s = setup(t), flow = await s.start(); await s.finish(flow);
  s.DB.sqlite.exec(migration); s.DB.sqlite.exec(migration);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learner_emails').get().n, 1);
  s.DB.sqlite.exec('DELETE FROM learners');
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learner_emails').get().n, 0);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learner_sessions').get().n, 0);
});

test('public options hide Apple, missing Google credentials and disabled email', async t => {
  const s = setup(t);
  s.env.EMAIL_LOGIN_ENABLED = 'false';
  const response = await s.call('/v1/auth/options');
  assert.deepEqual(await response.json(), { google: false, email: false, turnstileSiteKey: null });
  assert.equal((await s.call('/v1/auth/start/apple')).status, 404);
});

test('monthly budget and per-address hourly limit cannot be bypassed by repeat requests', async t => {
  const s = setup(t);
  await s.start();
  s.DB.sqlite.exec("UPDATE email_limits SET used = 2700 WHERE bucket LIKE 'global-month:%'");
  assert.equal((await s.start('fresh@example.com')).response.status, 429);
  s.DB.sqlite.exec("DELETE FROM email_limits WHERE bucket LIKE 'address-minute:%'; UPDATE email_limits SET used = 1 WHERE bucket LIKE 'global-month:%'; UPDATE email_limits SET used = 3 WHERE bucket LIKE 'address-hour:%'");
  assert.equal((await s.start()).response.status, 429);
  assert.equal(s.sent.length, 1);
});

test('export includes verified email; deleting account invalidates outstanding email codes', async t => {
  const s = setup(t), flow = await s.start();
  const cookie = sessionCookie(await s.finish(flow));
  const me = await (await s.call('/v1/me', null, cookie)).json();
  const exported = await (await s.call('/v1/export', null, cookie)).json();
  assert.equal(exported.email, 'person@example.com');
  s.DB.sqlite.exec('DELETE FROM email_limits');
  const pending = await s.start();
  const deleted = await worker.fetch(new Request(api + '/v1/account', {
    method: 'DELETE', headers: { Origin: origin, Cookie: cookie, 'Content-Type': 'application/json', 'X-FND-CSRF': me.csrfToken },
    body: JSON.stringify({ confirmed: true, confirmedUsername: me.username })
  }), s.env);
  assert.equal(deleted.status, 200);
  assert.equal((await s.finish(pending)).status, 400);
  assert.equal((await s.call('/v1/me', null, cookie)).status, 401);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM learner_emails').get().n, 0);
});

test('revoking original session invalidates a pending link', async t => {
  const s = setup(t), signup = await s.start();
  const cookie = sessionCookie(await s.finish(signup));
  const me = await (await s.call('/v1/me', null, cookie)).json();
  const linking = await s.start('new@example.com', { link: true, cookie, csrf: me.csrfToken });
  assert.equal(linking.response.status, 200);
  await s.call('/v1/logout', {}, cookie, me.csrfToken);
  assert.equal((await s.finish(linking, {}, cookie + '; ' + linking.cookie, '/v1/account/email/verify', me.csrfToken)).status, 401);
  assert.equal(s.DB.sqlite.prepare('SELECT count(*) n FROM email_challenges').get().n, 0);
});

test('additive migration works on old schema without losing existing account rows', t => {
  const db = new DatabaseSync(':memory:'); t.after(() => db.close());
  db.exec(schema.slice(0, schema.indexOf('-- Additive and repeatable:')));
  db.exec("INSERT INTO learners (id,username,created_at,last_seen_at) VALUES ('old','Old',1,1); INSERT INTO identities VALUES ('google','old-subject','old'); INSERT INTO learner_progress VALUES ('old','m1-1',1,1,1)");
  db.exec(migration); db.exec(migration);
  assert.equal(db.prepare('SELECT completed FROM learner_progress').get().completed, 1);
  assert.equal(db.prepare('SELECT subject FROM identities').get().subject, 'old-subject');
});

test('enabling idle sign-out starts from the current authenticated interaction', async t => {
  const s = setup(t);
  const result = await s.finish(await s.start());
  const cookie = sessionCookie(result);
  const me = await (await s.call('/v1/me', null, cookie)).json();
  s.DB.sqlite.exec('UPDATE learner_sessions SET last_active = last_active - 7200');
  const response = await worker.fetch(new Request(api + '/v1/settings', {
    method: 'PATCH', headers: { Origin: origin, 'Content-Type': 'application/json',
      Cookie: cookie, 'X-FND-CSRF': me.csrfToken },
    body: JSON.stringify({ idleMinutes: 15 })
  }), s.env);
  assert.equal(response.status, 200);
  assert.equal((await (await s.call('/v1/me', null, cookie)).json()).username, me.username);
});


test('Turnstile transport exception returns a sanitized 503 before database writes', async t => {
  const s = setup(t);
  s.setVerificationUnavailable(true);
  const flow = await s.start();
  assert.equal(flow.response.status, 503);
  assert.equal(s.sent.length, 0);
  assert.equal(s.DB.sqlite.prepare('SELECT COUNT(*) AS n FROM email_limits').get().n, 0);
  assert.doesNotMatch(JSON.stringify(flow.data), /private verification|siteverify|token|email/i);
});

test('D1 reservation failures return a sanitized 503 without sending', async t => {
  const s = setup(t);
  const liveDB = s.env.DB;
  s.env.DB = { ...liveDB,
    prepare(sql) {
      if (sql.includes('INSERT INTO email_limits')) {
        throw new Error('private D1 connection error');
      }
      return liveDB.prepare(sql);
    }
  };
  const flow = await s.start();
  assert.equal(flow.response.status, 503);
  assert.equal(s.sent.length, 0);
  assert.doesNotMatch(JSON.stringify(flow.data), /private D1|connection error/i);
});

test('D1 email challenge insert failures return a sanitized 503 without sending', async t => {
  const s = setup(t);
  const liveDB = s.env.DB;
  s.env.DB = { ...liveDB,
    prepare(sql) {
      if (sql.includes('INSERT INTO email_challenges')) {
        throw new Error('private email challenge error');
      }
      return liveDB.prepare(sql);
    }
  };
  const flow = await s.start();
  assert.equal(flow.response.status, 503);
  assert.equal(s.sent.length, 0);
  assert.doesNotMatch(JSON.stringify(flow.data), /private email challenge/i);
});

test('malformed Turnstile response emits only a fixed diagnostic and stops before D1', async t => {
  const s = setup(t);
  const warnings = [];
  t.mock.method(console, 'warn', (...args) => { warnings.push(args.join(' ')); });
  s.setMalformedVerification(true);
  const flow = await s.start();
  assert.equal(flow.response.status, 503);
  assert.equal(s.sent.length, 0);
  assert.equal(s.DB.sqlite.prepare('SELECT COUNT(*) AS n FROM email_limits').get().n, 0);
  assert.ok(warnings.includes('learner_email_turnstile_invalid_json'));
  assert.ok(warnings.includes('learner_email_turnstile_unavailable'));
  assert.doesNotMatch(warnings.join(' '), /invalid non-JSON|secret|token|address/i);
});

test('Turnstile redirects fail closed without sending verification emails', async t => {
  const s = setup(t);
  s.setVerificationRedirected(true);
  const flow = await s.start();
  assert.equal(flow.response.status, 400);
  assert.equal(s.sent.length, 0);
  assert.equal(s.DB.sqlite.prepare('SELECT COUNT(*) AS n FROM email_limits').get().n, 0);
});

test('unsupported Turnstile timeout setup emits only a fixed diagnostic', async t => {
  const s = setup(t);
  const warnings = [];
  t.mock.method(console, 'warn', (...args) => { warnings.push(args.join(' ')); });
  t.mock.method(AbortSignal, 'timeout', () => { throw new TypeError('private runtime details'); });
  const flow = await s.start();
  assert.equal(flow.response.status, 503);
  assert.equal(s.sent.length, 0);
  assert.equal(s.DB.sqlite.prepare('SELECT COUNT(*) AS n FROM email_limits').get().n, 0);
  assert.ok(warnings.includes('learner_email_turnstile_timeout_setup_failed'));
  assert.ok(warnings.includes('learner_email_turnstile_unavailable'));
  assert.doesNotMatch(warnings.join(' '), /private runtime details/i);
});

test('Resend redirects are rejected without exposing credentials or sending an email', async t => {
  const s = setup(t);
  const warnings = [];
  t.mock.method(console, 'warn', (...args) => { warnings.push(args.join(' ')); });
  s.setResendRedirected(true);
  const flow = await s.start('test@example.com');
  assert.equal(flow.response.status, 503);
  assert.equal(s.sent.length, 0);
  assert.ok(warnings.includes('learner_email_resend_http_rejected:302'));
  assert.ok(warnings.includes('learner_email_delivery_failed'));
  assert.equal(s.DB.sqlite.prepare('SELECT COUNT(*) AS n FROM email_challenges').get().n, 0);
  assert.doesNotMatch(warnings.join(' '), /example.com|re_test_only|secret/i);
});

test('Resend HTTP rejection is classified by status without logging provider body', async t => {
  const s = setup(t);
  const warnings = [];
  t.mock.method(console, 'warn', (...args) => { warnings.push(args.join(' ')); });
  s.setFailure(true);
  const flow = await s.start();
  assert.equal(flow.response.status, 503);
  assert.ok(warnings.includes('learner_email_resend_http_rejected:500'));
  assert.doesNotMatch(warnings.join(' '), /private provider error/i);
});

/**
 * Optional Resend passwordless authentication. No delivery occurs until all
 * secrets, verified sender and Turnstile configuration are explicitly enabled.
 * This module receives existing session/CORS helpers from the learner Worker.
 */
const LIFE = 600;
const COOKIE = '__Host-fnd_email_flow';
const encoder = new TextEncoder();

/** ASCII mailbox support, with a documented case-insensitive login policy.
 * Preserve plus tags and dots; never equate provider-specific aliases.
 */
export function normalizeEmail(value) {
  if (typeof value !== 'string') return null;
  const email = value.trim().toLowerCase();
  if (email.length > 254 || !/^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,63}$/.test(email)) return null;
  const [local, domain] = email.split('@');
  if (local.length > 64 || local.startsWith('.') || local.endsWith('.') ||
      local.includes('..') || domain.split('.').some(p => !p || p.length > 63 || p.startsWith('-') || p.endsWith('-'))) return null;
  return email;
}

/** Keyed hashes prevent offline guessing of short codes or email/IP buckets. */
async function digest(env, value) {
  const key = await crypto.subtle.importKey('raw', encoder.encode(env.EMAIL_AUTH_SECRET),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return Array.from(new Uint8Array(await crypto.subtle.sign('HMAC', key, encoder.encode(value))),
    b => b.toString(16).padStart(2, '0')).join('');
}

export function emailEnabled(env) {
  return env.EMAIL_LOGIN_ENABLED === 'true' &&
    typeof env.RESEND_API_KEY === 'string' && env.RESEND_API_KEY.startsWith('re_') &&
    typeof env.EMAIL_AUTH_SECRET === 'string' && env.EMAIL_AUTH_SECRET.length >= 32 &&
    !!env.TURNSTILE_SECRET_KEY && !!env.TURNSTILE_SITE_KEY &&
    !!normalizeEmail(env.EMAIL_FROM);
}

function flowCookie(token, age = LIFE) {
  return `${COOKIE}=${token}; Path=/; Max-Age=${age}; Secure; HttpOnly; SameSite=Strict`;
}

/** Rejection sampling avoids modulo bias in the eight-digit one-time code. */
function newCode() {
  const value = new Uint32Array(1);
  do { crypto.getRandomValues(value); } while (value[0] >= 4200000000);
  return String(value[0] % 100000000).padStart(8, '0');
}

/** Each reservation is atomic across Worker instances. Failed reservations
 * remain charged conservatively; timeouts cannot cause budget undercounting.
 */
async function reserve(db, bucket, limit, expires) {
  return !!await db.prepare(`INSERT INTO email_limits (bucket, used, expires_at)
    VALUES (?, 1, ?) ON CONFLICT(bucket) DO UPDATE SET used = used + 1
    WHERE used < ? RETURNING used`).bind(bucket, expires, limit).first();
}

/** Authenticate Turnstile on the server; client success alone is insufficient. */
async function human(req, env, token) {
  if (typeof token !== 'string' || token.length > 2048 || !token) return false;
  const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ secret: env.TURNSTILE_SECRET_KEY, response: token,
      remoteip: req.headers.get('CF-Connecting-IP') || undefined }),
    signal: AbortSignal.timeout(10000), redirect: 'error'
  });
  if (!response.ok) return false;
  const result = await response.json();
  return result.success === true && result.hostname === new URL(env.PUBLIC_ORIGIN).hostname &&
    result.action === 'email_login';
}

/** Starts either an ordinary login or an explicitly requested email link.
 * Account existence never changes the response or email sent to the mailbox.
 */
export async function startEmail(req, env, input, h, account = null) {
  if (!emailEnabled(env)) return h.err(req, env, 503, 'Email sign-in is not available yet.');
  const email = normalizeEmail(input.email);
  const username = h.cleanUsername(input.username || 'Learner');
  if (!email || !username) return h.err(req, env, 400, 'Enter a valid email and display username.');
  // Stage-specific operational errors reveal no addresses, tokens, or codes.
  // A failed external service should produce 503, not an opaque 500.
  let verifiedHuman;
  try {
    verifiedHuman = await human(req, env, input.turnstileToken);
  } catch {
    console.warn('learner_email_turnstile_unavailable');
    return h.err(req, env, 503, 'Verification service temporarily unavailable. Please try again.');
  }
  if (!verifiedHuman) {
    return h.err(req, env, 400, 'Please complete the verification and try again.');
  }
  const t = h.now();
  const day = Math.floor(t / 86400), hour = Math.floor(t / 3600);
  const date = new Date(t * 1000);
  const month = date.toISOString().slice(0, 7);
  const monthEnd = Date.UTC(date.getUTCFullYear(), date.getUTCMonth() + 1, 1) / 1000;
  let emailKey, ipKey;
  try {
    emailKey = await digest(env, 'email:' + email);
    ipKey = await digest(env, 'ip:' + day + ':' + (req.headers.get('CF-Connecting-IP') || 'unknown'));
  } catch {
    console.warn('learner_email_digest_unavailable');
    return h.err(req, env, 503, 'Email sign-in is temporarily unavailable.');
  }
  // Free-tier headroom: 90/day and 2,700/calendar month, below 100/3,000.
  // Use a dedicated Resend account or account for other applications manually.
  const limits = [
    [`address-minute:${emailKey}:${Math.floor(t / 60)}`, 1, t + 120],
    [`address-hour:${emailKey}:${hour}`, 3, (hour + 1) * 3600],
    [`address-day:${emailKey}:${day}`, 10, (day + 1) * 86400],
    [`ip-hour:${ipKey}:${hour}`, 10, (hour + 1) * 3600],
    [`global-day:${day}`, 90, (day + 1) * 86400],
    [`global-month:${month}`, 2700, monthEnd]
  ];
  for (const [bucket, limit, expiry] of limits) {
    let available;
    try {
      available = await reserve(env.DB, bucket, limit, expiry);
    } catch {
      // Never emit the bucket (which may include keyed address/IP hashes),
      // D1's error text, or SQL parameters into public logs.
      console.warn('learner_email_limit_storage_failed');
      return h.err(req, env, 503, 'Email sign-in is temporarily unavailable.');
    }
    if (!available) {
      return h.err(req, env, 429, 'Email sign-in is temporarily limited. Please try later or use Google if available.');
    }
  }
  let id, browser, code;
  try {
    id = h.randomToken();
    browser = h.randomToken();
    code = newCode();
    const browserHash = await h.sha(browser);
    await env.DB.prepare(`INSERT INTO email_challenges
      (id, browser_hash, email, username, code_hash, link_session, expires_at)
      VALUES (?, ?, ?, ?, ?, ?, ?)`).bind(id, browserHash, email, username,
        await digest(env, id + ':' + code), account?.token_hash || null, t + LIFE).run();
  } catch {
    console.warn('learner_email_challenge_storage_failed');
    return h.err(req, env, 503, 'Email sign-in is temporarily unavailable.');
  }
  let sent = false;
  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST', redirect: 'error', signal: AbortSignal.timeout(10000),
      headers: { Authorization: 'Bearer ' + env.RESEND_API_KEY,
        'Content-Type': 'application/json', 'Idempotency-Key': 'learner-login/' + id },
      body: JSON.stringify({ from: 'FND Education Project <' + env.EMAIL_FROM + '>',
        to: [email], subject: 'Your FND Education sign-in code',
        text: `Your code is: ${code}\n\nEnter it on the website in the browser where you requested it. It expires in 10 minutes and works once.\n\n${account ? 'This request adds email sign-in to your current learner account.' : 'This request signs you in or creates a learner account.'}\nNever share this code. If you did not request it, ignore this email.\n\nYou can read the full course without an account.` })
    });
    const result = response.ok ? await response.json() : null;
    sent = typeof result?.id === 'string';
  } catch { /* Provider errors must not expose addresses, credentials or codes. */ }
  if (!sent) {
    await env.DB.prepare('DELETE FROM email_challenges WHERE id = ?').bind(id).run();
    console.warn('learner_email_delivery_failed'); // Redacted operational signal only.
    return h.err(req, env, 503, 'We could not send a code. Please try again later.');
  }
  return h.reply(req, env, { challengeId: id, expiresIn: LIFE }, 200,
    { 'Set-Cookie': flowCookie(browser) });
}

/** Atomically consume a browser-bound code. Every guess spends an attempt,
 * including correct guesses; competing requests cannot reuse a consumed code.
 */
export async function finishEmail(req, env, input, h, account = null) {
  if (!emailEnabled(env)) return h.err(req, env, 503, 'Email sign-in is not available yet.');
  const browser = h.cookie(req, COOKIE);
  if (!browser || browser.length > 100 || typeof input.challengeId !== 'string' ||
      !/^[A-Za-z0-9_-]{43}$/.test(input.challengeId) || !/^\d{8}$/.test(input.code || '')) {
    return h.err(req, env, 400, 'Code invalid or expired. Request a new code if needed.');
  }
  const browserHash = await h.sha(browser);
  // Link verification requires the original still-authenticated session and
  // CSRF token (checked by the caller). Ordinary logins cannot consume links.
  const flow = await env.DB.prepare(`UPDATE email_challenges SET attempts = attempts + 1
    WHERE id = ? AND browser_hash = ? AND expires_at > ? AND attempts < 5
      AND link_session IS ? RETURNING *`).bind(input.challengeId, browserHash,
      h.now(), account?.token_hash || null).first();
  if (!flow) return h.err(req, env, 400, 'Code invalid or expired. Request a new code if needed.');
  const consumed = await env.DB.prepare(`DELETE FROM email_challenges
    WHERE id = ? AND browser_hash = ? AND code_hash = ? AND expires_at > ?
    RETURNING *`).bind(flow.id, browserHash, await digest(env, flow.id + ':' + input.code), h.now()).first();
  if (!consumed) return h.err(req, env, 400, 'Code invalid or expired. Request a new code if needed.');

  let identity = await env.DB.prepare('SELECT learner_id FROM learner_emails WHERE email = ?')
    .bind(flow.email).first();
  if (account) {
    // Never merge accounts, replace another email, or steal an existing login.
    const own = await env.DB.prepare('SELECT email FROM learner_emails WHERE learner_id = ?')
      .bind(account.learner_id).first();
    if ((identity && identity.learner_id !== account.learner_id) || (own && own.email !== flow.email)) {
      return h.err(req, env, 409, 'This email cannot be added. No accounts or progress were merged.');
    }
    await env.DB.prepare(`INSERT OR IGNORE INTO learner_emails (email, learner_id, verified_at)
      VALUES (?, ?, ?)`).bind(flow.email, account.learner_id, h.now()).run();
    identity = await env.DB.prepare('SELECT learner_id FROM learner_emails WHERE email = ?').bind(flow.email).first();
    if (identity?.learner_id !== account.learner_id) return h.err(req, env, 409, 'This email cannot be added.');
    return h.reply(req, env, { ok: true, linked: true }, 200, { 'Set-Cookie': flowCookie('', 0) });
  }
  if (!identity) {
    const id = crypto.randomUUID();
    // D1 batch is transactional; the conditional insert prevents orphaned
    // learners if two independently verified browser flows race to sign up.
    await env.DB.batch([
      env.DB.prepare(`INSERT INTO learners (id, username, created_at, last_seen_at)
        SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM learner_emails WHERE email = ?)`)
        .bind(id, flow.username, h.now(), h.now(), flow.email),
      env.DB.prepare(`INSERT INTO learner_emails (email, learner_id, verified_at)
        SELECT ?, id, ? FROM learners WHERE id = ?`).bind(flow.email, h.now(), id)
    ]);
    identity = await env.DB.prepare('SELECT learner_id FROM learner_emails WHERE email = ?').bind(flow.email).first();
  }
  const session = await h.createSession(env, identity.learner_id);
  const response = h.reply(req, env, { ok: true });
  response.headers.append('Set-Cookie', flowCookie('', 0));
  response.headers.append('Set-Cookie', h.sessionCookie(session));
  return response;
}

# DEAD INTERNET MUSEUM — Cloudflare Workers + D1

This directory contains the server-side shared visitor counter and anonymous BBS. It does not go live until a Cloudflare account deploys it.

## Deploy
1. `cd cloudflare && npx wrangler login`
2. `npx wrangler d1 create dead-internet-museum` and copy the returned database_id into wrangler.toml.
3. `npx wrangler d1 execute dead-internet-museum --remote --file=./schema.sql`
4. `npx wrangler secret put HASH_SALT` (a long random string) and `npx wrangler secret put ADMIN_KEY` (different long random string).
5. `npx wrangler deploy`
6. Copy the worker's https://...workers.dev URL into the `data-api-base` attribute on `<body>` in the root index.html and deploy that change.

**Privacy:** Counts represent approximately one distinct IP+browser fingerprint per UTC day, not literal page views or exact unique people. Only salted hashes are stored; no raw IP is stored by this code. Rotate HASH_SALT to reset the deduplication identity. Cloudflare may separately process network logs under its own policies.

**BBS:** Nickname max 24 characters, message max 500, no URLs, 2-minute per-IP posting interval, no HTML rendering. Admin can hide a post using `POST /api/admin/posts/:id` with `X-Admin-Key` header. Keep the key secret; never put it in client HTML. Moderation is reactive; for public launch, add Turnstile or a moderation queue and an abuse-report channel.

**Security:** Set ALLOWED_ORIGIN to the deployed website origin; browser CORS is not authentication and does not block direct requests. Consider Cloudflare WAF/rate limiting. No guarantee against coordinated spam or count manipulation.

**Cost:** Cloudflare free quotas and policies can change; check current pricing before deployment.

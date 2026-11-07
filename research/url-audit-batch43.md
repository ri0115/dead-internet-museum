# URL status audit protocol — Batch 43 (2026-11-07)

## Baseline (reported at commit cefc9f2; not independently re-counted)
- Total: 455
- Wayback link registered: 230
- Original URL unknown / researching: 224
- Original URL known, Wayback not set: 1
- Confirmed no applicable original URL: 0

## Mandatory distinctions
1. `wayback_registered`: Wayback URL recorded. A calendar/search URL does not establish that a snapshot exists.
2. `original_url_unknown`: Original URL not identified yet. Never infer that no URL existed.
3. `original_url_known_wayback_unset`: Original URL identified, archive URL not recorded.
4. `no_applicable_url_confirmed`: Verified that the exhibit does not correspond to a single applicable historical URL. Requires a written reason and source/evidence. Do not use merely because search failed.

## Additional independent fields (recommended)
- `original_url` (nullable)
- `url_status` (one of the four statuses above)
- `wayback_url` (nullable)
- `wayback_link_type`: `snapshot`, `calendar`, `search`, `none`
- `snapshot_verified`: `yes`, `no`, `not_checked`
- `url_evidence`: source URL or citation
- `url_checked_at`: ISO date
- `no_url_reason`: mandatory only for `no_applicable_url_confirmed`

## Rates
- All-exhibits link rate = registered Wayback links / all exhibits.
- Eligible-exhibits link rate = registered Wayback links / (all exhibits - confirmed no applicable URL).
- Verified-snapshot rate = exhibits with inspected archived snapshot / exhibits eligible for archive.
- Unknown URL records remain in both link-rate denominators.
- Display link coverage separately from verified snapshot coverage.

## Next audit priority
1. Resolve the one original-URL-known / Wayback-unset record.
2. Triage the 224 original-URL-unknown records, prioritizing well-known sites and old services with likely identifiable domains.
3. For each resolved URL, inspect the Wayback calendar; label a snapshot only if directly checked.
4. Record redirects, aliases, old domains and service migrations separately from service shutdown.
5. Recompute both denominators after each confirmed status change.

## Quality gates
- Do not bulk-convert unresolved records into confirmed-no-URL.
- Do not count a Wayback search link as a verified snapshot.
- Keep the original 455-record baseline until master data and published HTML have been reconciled.
- Avoid changing the existing visual design during URL-only audits.

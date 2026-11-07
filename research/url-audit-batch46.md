# Batch 46 — master recovery and URL reconciliation (2026-11-07)

## Recovery
Read the complete Git blob for `data/master.json` at SHA `0d93c4b8eb15fd4ebab49674f70334c1680dec24`, because GitHub's file-contents wrapper returned an empty body. JSON parsed successfully.

## Independently counted current master
- `exhibits`: **453**
- Any `archive_search_url` or `archive_url` populated: **230**
- `original_url` null/empty: **225**
- `original_url` populated but both archive links empty: **1** — `dmm-r18-legacy-brand`
- **Three overlapping cases**: original_url empty but Wayback search URL exists: `bijin-tokei`, `dmm-blog-adult` (verify actual ID), `r18-com` (verify actual ID). These should be normalized by verifying that the archive-search URL points to the historically correct original site; do not infer an original URL merely from a search link without evidence.

The previously reported 455 total and 224 unknown are not yet reconciled with this 453-record master. Do not silently alter published counts or claim 455 rows were verified.

## DMM.R18 finding
- Record ID: `dmm-r18-legacy-brand`
- Current original URL: `https://www.dmm.co.jp/`
- Contemporary 2018 report explicitly maps DMM.R18 -> FANZA and preserves the same URL: https://techwave.jp/archives/dmm-restarts-dmm-r18-to-fanza.html
- Operator press release verifies the 2018-08-01 rename, not a complete shutdown: https://prtimes.jp/main/html/rd/p/000003114.000002581.html
- Proposed Wayback *calendar/search* URL (not a verified archived snapshot): https://web.archive.org/web/*/https://www.dmm.co.jp/
- Status: `original_url_confirmed; wayback_calendar_candidate; snapshot_not_checked`
- **Do not label this as a verified saved page**.

## Follow-up
1. Reconcile the two-record delta between published 455 and master 453, possibly from later batches; do not invent missing IDs.
2. Normalize the three overlap records after verifying original URLs.
3. Apply the DMM.R18 calendar link to the master only after reconciling source-of-truth/version status; the proposed link is a search, not a verified snapshot.
4. Track independent measures: Wayback link presence, original URL confidence, archived snapshot verified.

No master records or public HTML changed in this batch.

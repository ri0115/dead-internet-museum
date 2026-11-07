# Research & audit workflow

- Latest reported URL-audit baseline: **455 exhibits** (2026-11-07; master/HTML recount pending)
- Published app: retro browser-style HTML; version and master count reconciliation pending.
- The `main` branch is the authoritative source going forward.
- Source checking and entry addition are recorded via Git commits. HTML export is updated at milestones.

## Priorities

1990s–2010s Japanese internet history: free utilities and software sites, personal homepage tools, bulletin boards, browser games, horror/urban legends, media and portals. Adult-oriented legacy services are documented as cultural history without explicit imagery.

## Audit requirements

- Record evidence for opening/closure dates and distinction between shutdown, migration, rebranding or feature-only termination.
- Never invent exact closure dates from an announcement date or a month-only source.
- When a Wayback link is only a calendar/search URL, do not claim a snapshot was viewed.
- Check names and IDs for duplicates before each batch.
- Keep unavailable or weakly documented sites as candidates rather than inflating the published count.

## Batch 45 — master access and reconciliation

The GitHub file API returns a blob SHA for `data/master.json` but no text body, including when a short line range is requested. **Do not interpret an empty API response as an empty master file.** The 455-record figures remain reported, not independently verified.

Before record-level changes: obtain a complete JSON export through a working authenticated download route, validate its JSON structure, count records, and identify the exact record whose original URL is known but Wayback URL is missing. Compare the master count with the published HTML; preserve both until reconciled. Never overwrite the master using the empty API response.

See [URL audit protocol](url-audit-batch43.md).

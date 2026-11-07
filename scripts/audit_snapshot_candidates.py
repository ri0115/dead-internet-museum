#!/usr/bin/env python3
"""Audit candidate snapshot metadata and flag suspicious dates; never auto-verify."""
import csv,json,re,datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1]
html=(root/"index.html").read_text(encoding="utf-8")
m=re.search(r'<script id="catalog" type="application/json">([\s\S]*?)</script>',html)
if not m:raise SystemExit("Catalog missing")
records=json.loads(m.group(1))
rows=[]
for r in records:
    url=r.get("candidateSnapshot")
    if not url:continue
    stamp=re.search(r'/web/(\d{14})/',url)
    capture=stamp.group(1)[:8] if stamp else ""
    end=str(r.get("end") or "")
    flags=[]
    if not stamp:flags.append("invalid_snapshot_url")
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}',end) and capture and capture>end.replace("-",""):
        flags.append("capture_after_closure")
    elif re.fullmatch(r'\d{4}',end) and capture and capture[:4]>end:
        flags.append("capture_after_end_year")
    if r.get("original") and url and r["original"].lower().rstrip("/") not in url.lower():
        flags.append("original_url_differs")
    rows.append(dict(id=r["id"],name=r["name"],end=end,capture=capture,candidate_url=url,flags=";".join(flags),review_status="needs_manual_review"))
out=root/"snapshot-review.csv"
with out.open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["id","name","end","capture","candidate_url","flags","review_status"])
    w.writeheader();w.writerows(sorted(rows,key=lambda x:(not bool(x["flags"]),x["name"])))
print(f"Candidate snapshots: {len(rows)}; flagged: {sum(bool(x['flags']) for x in rows)}")

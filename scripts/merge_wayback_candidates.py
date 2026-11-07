#!/usr/bin/env python3
"""Merge CDX candidates into catalog without claiming visual verification."""
import csv,io,json,re,sys,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
html_path=root/"index.html"
html=html_path.read_text(encoding="utf-8")
pattern=r'(<script id="catalog" type="application/json">)([\s\S]*?)(</script>)'
m=re.search(pattern,html)
if not m:raise SystemExit("Catalog missing")
records=json.loads(m.group(2))
candidates={}
for path in sorted((root/"prior-audits").glob("*.zip")):
    try:
        with zipfile.ZipFile(path) as z:
            for filename in z.namelist():
                if not filename.endswith(".csv"):continue
                for row in csv.DictReader(io.TextIOWrapper(z.open(filename),encoding="utf-8-sig")):
                    if row.get("status")=="candidate_needs_visual_review" and row.get("candidate_url","").startswith("https://web.archive.org/web/"):
                        candidates[row["id"]]=row["candidate_url"]
    except (zipfile.BadZipFile,KeyError,UnicodeError) as exc:
        print("Skipping bad artifact",path,exc,file=sys.stderr)
count=0
for r in records:
    if r.get("snapshot"):continue
    if r["id"] in candidates:
        r["candidateSnapshot"]=candidates[r["id"]]
        count+=1
new=json.dumps(records,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
html=html[:m.start(2)]+new+html[m.end(2):]
html_path.write_text(html,encoding="utf-8")
print(f"Added or updated {count} unverified candidate links; {len(candidates)} unique candidate IDs")

#!/usr/bin/env python3
"""Audit Wayback snapshots for DEAD INTERNET MUSEUM; never invent a capture date."""
import argparse,csv,json,re,time,urllib.parse,urllib.request
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"DeadInternetMuseumArchiveAudit/1.0 (GitHub Actions; research)"})
    with urllib.request.urlopen(req,timeout=22) as response:return json.load(response)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--limit",type=int,default=40)
    ap.add_argument("--offset",type=int,default=0)
    args=ap.parse_args()
    html=(ROOT/"index.html").read_text(encoding="utf-8")
    m=re.search(r'<script id="catalog" type="application/json">([\s\S]*?)</script>',html)
    if not m:raise SystemExit("Catalog missing")
    records=json.loads(m.group(1))
    targets=[r for r in records if r.get("archive") and not r.get("snapshot")]
    batch=targets[args.offset:args.offset+args.limit]
    out=ROOT/"archive-audit.csv"
    with out.open("w",newline="",encoding="utf-8-sig") as fp:
        w=csv.DictWriter(fp,fieldnames=["id","name","original","candidate_url","capture_utc","status","note"])
        w.writeheader()
        for r in batch:
            original=r.get("original") or ""
            archive=r.get("archive") or ""
            # Existing archive URLs end in /web/*/ORIGINAL; prefer that original target.
            target=original or archive.split("/web/*/",1)[-1]
            row=dict(id=r.get("id",""),name=r.get("name",""),original=target,candidate_url="",capture_utc="",status="unchecked",note="")
            if not target.startswith(("http://","https://")):
                row.update(status="skipped",note="No usable original URL")
                w.writerow(row);continue
            # CDX API: only HTTP 200 HTML captures, before end date when known.
            params={"url":target,"output":"json","filter":["statuscode:200","mimetype:text/html"],"collapse":"timestamp:6","fl":"timestamp,original,statuscode,mimetype","limit":"-30"}
            end=str(r.get("end") or "")
            if re.match(r"^\d{4}-\d{2}-\d{2}$",end):params["to"]=end.replace("-","")
            q=urllib.parse.urlencode(params,doseq=True)
            try:
                data=get_json("https://web.archive.org/cdx/search/cdx?"+q)
                headers=data[0] if data else []
                captures=[dict(zip(headers,line)) for line in data[1:]] if len(data)>1 else []
                if captures:
                    capture=captures[-1]
                    stamp=capture["timestamp"]
                    row.update(status="candidate_needs_visual_review",capture_utc=datetime.strptime(stamp,"%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).isoformat(),candidate_url="https://web.archive.org/web/"+stamp+"/"+capture["original"],note="CDX 200 HTML; verify page identity and contents before publishing")
                else:row.update(status="no_capture_found",note="No matching HTTP 200 HTML CDX result")
            except Exception as exc:row.update(status="request_error",note=str(exc)[:180])
            w.writerow(row)
            print(row["name"],row["status"],flush=True)
            time.sleep(1.5)
    print("Wrote",out)
if __name__=="__main__":main()

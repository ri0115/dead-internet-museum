#!/usr/bin/env python3
"""Check whether archived candidate pages are retrievable; never auto-verify."""
import csv,json,re,time,urllib.request,urllib.error,html as html_lib
from pathlib import Path
html=Path("index.html").read_text(encoding="utf-8")
m=re.search(r'<script id="catalog" type="application/json">([\s\S]*?)</script>',html)
if not m: raise SystemExit("Catalog missing")
rows=json.loads(m.group(1))
out=[]
for r in rows:
    url=r.get("candidateSnapshot")
    if not url: continue
    status="unknown";final="";title="";detail=""
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"DeadInternetMuseumArchiveReview/1.0","Range":"bytes=0-131071"})
        with urllib.request.urlopen(req,timeout=12) as res:
            final=res.geturl()
            raw=res.read(131072)
            head=raw[:8192].decode("ascii","ignore")
            meta=re.search(r"charset\s*=\s*[\x22\x27]?([\w.-]+)",head,re.I)
            charset=(meta.group(1) if meta else res.headers.get_content_charset()) or "utf-8"
            try:
                content=raw.decode(charset)
            except (LookupError,UnicodeDecodeError):
                content=raw.decode("utf-8","replace")
            match=re.search(r"<title[^>]*>(.*?)</title>",content,re.I|re.S)
            title=html_lib.unescape(re.sub(r"\s+"," ",match.group(1))).strip()[:180] if match else ""
            status="http_ok" if res.status==200 else f"http_{res.status}"
            if "web.archive.org" not in final: status="redirected_outside_archive"
            if "Wayback Machine" in title or "Internet Archive" in title: status="archive_error_or_wrapper"
    except urllib.error.HTTPError as e:
        status=f"http_{e.code}";detail=str(e)[:160]
    except Exception as e:
        status="request_error";detail=str(e)[:160]
    out.append({"id":r["id"],"name":r["name"],"status":status,"title":title,"final_url":final,"candidate_url":url,"detail":detail})
    print(f'{len(out)} {r["id"]} {status}',flush=True)
    time.sleep(0.3)
with open("archive-content-review.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=["id","name","status","title","final_url","candidate_url","detail"])
    w.writeheader();w.writerows(out)
print("Reviewed",len(out),"candidates; no records promoted",flush=True)

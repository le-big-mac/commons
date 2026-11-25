"""Fetches from the arXiv's public API every paper first submitted from 1 January to 30 June 2025 in thirteen categories.
usage: python -I fetch.py DATADIR      Resumable: a page already on disk and complete is not asked for again. Three seconds between requests."""
import sys, os, re, time, urllib.request
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
CATS = ["astro-ph.CO", "astro-ph.EP", "astro-ph.GA", "astro-ph.HE", "astro-ph.IM", "astro-ph.SR", "hep-th", "hep-ph", "gr-qc", "quant-ph", "math.CO", "math.AP", "cs.CL"]
PAGE = 1000
def get(cat, start):
    url = f"https://export.arxiv.org/api/query?search_query=cat:{cat}+AND+submittedDate:%5B202501010000+TO+202506302359%5D&start={start}&max_results={PAGE}&sortBy=submittedDate&sortOrder=ascending"
    req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r: return r.read()
log = open(os.path.join(out, "fetch.log"), "a")
for cat in CATS:
    start = 0; total = None
    while total is None or start < total:
        path = os.path.join(out, f"{cat}-{start:06d}.xml"); data = None
        if os.path.exists(path):
            data = open(path, "rb").read()
        tries = 0
        while True:
            if data is not None:
                m = re.search(rb"<opensearch:totalResults[^>]*>(\d+)<", data); n = len(re.findall(rb"<entry>", data))
                if m and (n == PAGE or start + n >= int(m.group(1))) and n > 0: total = int(m.group(1)); break
            tries += 1
            if tries > 8: raise SystemExit(f"gave up on {cat} at {start}")
            time.sleep(3 if tries == 1 else 20)
            try: data = get(cat, start)
            except Exception as e: data = None; print("error", cat, start, repr(e)[:80], file=log, flush=True); continue
            open(path, "wb").write(data)
        print(time.strftime("%H:%M:%S", time.gmtime()), cat, start, "of", total, "entries", n, file=log, flush=True)
        start += PAGE
print("done", file=log, flush=True)

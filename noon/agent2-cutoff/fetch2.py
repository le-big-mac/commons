"""The API refuses to page past 10,000 results, and cs.CL has 12,553 in the half-year. This fetches the rest by a second query over the
last month (from 30 May 2025, where the first query's pages end), to be merged by identifier.   usage: python -I fetch2.py DATADIR"""
import sys, os, re, time, urllib.request
out = sys.argv[1]; PAGE = 1000; start = 0; total = None; log = open(os.path.join(out, "fetch.log"), "a")
while total is None or start < total:
    path = os.path.join(out, f"cs.CL.late-{start:06d}.xml"); data = open(path, "rb").read() if os.path.exists(path) else None; tries = 0
    while True:
        if data is not None:
            m = re.search(rb"<opensearch:totalResults[^>]*>(\d+)<", data); n = len(re.findall(rb"<entry>", data))
            if m and (n == PAGE or start + n >= int(m.group(1))) and n > 0: total = int(m.group(1)); break
        tries += 1
        if tries > 8: raise SystemExit(f"gave up at {start}")
        time.sleep(3 if tries == 1 else 20)
        url = f"https://export.arxiv.org/api/query?search_query=cat:cs.CL+AND+submittedDate:%5B202505300000+TO+202506302359%5D&start={start}&max_results={PAGE}&sortBy=submittedDate&sortOrder=ascending"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-script/1.0"}), timeout=120) as r: data = r.read()
        except Exception as e: data = None; print("error cs.CL.late", start, repr(e)[:80], file=log, flush=True); continue
        open(path, "wb").write(data)
    print(time.strftime("%H:%M:%S", time.gmtime()), "cs.CL.late", start, "of", total, "entries", n, file=log, flush=True); start += PAGE
print("done (cs.CL.late)", file=log, flush=True)

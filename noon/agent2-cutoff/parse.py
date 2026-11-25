"""Turns the fetched pages into one table.   usage: python -I parse.py DATADIR records.csv
Each record: arXiv identifier (no version), time of the first version as the API gives it (UTC), primary category, time of the latest version."""
import sys, os, re, csv
d = sys.argv[1]; rows = {}; pages = 0; totals = {}; got = {}
for f in sorted(os.listdir(d)):
    if not f.endswith(".xml"): continue
    pages += 1; t = open(os.path.join(d, f), encoding="utf-8", errors="replace").read(); cat = f.rsplit("-", 1)[0]
    m = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", t); totals[cat] = int(m.group(1))
    for e in re.findall(r"<entry>(.*?)</entry>", t, re.S):
        i = re.search(r"<id>http://arxiv\.org/abs/([^<v]+(?:/\d+)?)v\d+</id>", e); p = re.search(r"<published>([^<]+)</published>", e); up = re.search(r"<updated>([^<]+)</updated>", e); c = re.search(r'<arxiv:primary_category[^>]*term="([^"]+)"', e)
        if not (i and p and c): raise SystemExit("an entry without an id, a time or a primary category in " + f)
        rows[i.group(1)] = (p.group(1), c.group(1), up.group(1) if up else ''); got[cat] = got.get(cat, 0) + 1
with open(sys.argv[2], "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["id", "published", "primary", "updated"]); [w.writerow([k, *v]) for k, v in sorted(rows.items())]
print(pages, "pages;", len(rows), "papers once each")
for cat in sorted(totals): print(f"   {cat:12s} the API says {totals[cat]:6d}; entries read {got.get(cat, 0):6d}" + ("" if totals[cat] == got.get(cat, 0) else "   <-- DIFFERENT"))

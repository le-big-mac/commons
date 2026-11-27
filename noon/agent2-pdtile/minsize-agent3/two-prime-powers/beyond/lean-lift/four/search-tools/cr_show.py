# Print Crossref search rows. Usage: cr_show.py FILE
import sys, json
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    data = json.load(fh)
for it in (data.get("message") or {}).get("items", []):
    au = ", ".join((a.get("family") or "") for a in (it.get("author") or [])[:4])
    print("  %s | %s | %s | %s | %s | cited-by %s | %s" % (it.get("DOI"), "; ".join(it.get("title") or []), au, (it.get("issued") or {}).get("date-parts"), "; ".join(it.get("container-title") or []), it.get("is-referenced-by-count"), it.get("type")))

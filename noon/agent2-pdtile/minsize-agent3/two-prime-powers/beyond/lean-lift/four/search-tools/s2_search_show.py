# Print rows of a saved Semantic Scholar paper-search result. Usage: s2_search_show.py FILE
import sys, json
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    data = json.load(fh)
print("total:", data.get("total"))
for p in data.get("data") or []:
    ids = p.get("externalIds") or {}
    au = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:4])
    print("  %s | %s | %s | arXiv:%s doi:%s" % (p.get("year"), p.get("title"), au, ids.get("ArXiv"), ids.get("DOI")))

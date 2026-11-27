import sys, json
# usage: python3 -I oa_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    print("==", p, "count:", d.get("meta", {}).get("count"))
    for w in d.get("results", [])[:12]:
        print("  ", w.get("publication_year"), "|", (w.get("title") or "")[:130], "|", w.get("doi") or w.get("id"))

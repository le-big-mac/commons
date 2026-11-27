import sys, json
# usage: python3 -I oa_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    res = d.get("results", [])
    print("==", p, "count:", (d.get("meta") or {}).get("count"))
    for r in res:
        print("  ", r.get("id", "").rsplit("/", 1)[-1], "|", r.get("publication_year"), "|", (r.get("title") or "")[:150], "| cited_by", r.get("cited_by_count"))

import sys, json
# usage: python3 -I oa_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    r = d.get("results", [])
    print("==", p, "count:", d.get("meta", {}).get("count"), "shown:", len(r))
    for w in r:
        au = ", ".join(a.get("author", {}).get("display_name", "") for a in (w.get("authorships") or [])[:3])
        print("  ", (w.get("id") or "").rsplit("/", 1)[-1], "|", w.get("publication_year"), "|", (w.get("title") or "")[:130], "|", au[:70], "|", w.get("doi") or "")

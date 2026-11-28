import sys, json
# usage: python3 -I oa_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    r = d.get("results", [])
    print("  count:", d.get("meta", {}).get("count"), "shown:", len(r))
    for w in r:
        print("   ", w.get("id", "").replace("https://openalex.org/", ""), w.get("publication_year"), "|", (w.get("title") or "")[:150], "|", (w.get("doi") or ""))

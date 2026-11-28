import sys, json
# usage: python3 -I cr_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print("  unreadable", e); continue
    items = d.get("message", {}).get("items", [])
    print("  shown:", len(items))
    for w in items[:12]:
        print("   ", (w.get("issued", {}).get("date-parts", [[None]])[0][0]), "|", " ".join(w.get("title", []))[:150], "|", w.get("DOI"))

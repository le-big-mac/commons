import sys, json
# usage: python3 -I cr_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    items = (d.get("message") or {}).get("items") or []
    print("==", p, "total:", (d.get("message") or {}).get("total-results"), "shown:", len(items))
    for w in items:
        t = (w.get("title") or [""])[0]
        y = ((w.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        au = ", ".join((a.get("family") or "") for a in (w.get("author") or [])[:3])
        print("  ", y, "|", t[:120], "|", au[:50], "|", w.get("DOI"))

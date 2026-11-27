import sys, json
# usage: python3 -I zb_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    r = d.get("result")
    if not isinstance(r, list):
        print("==", p, "no results:", str(d)[:120]); continue
    print("==", p, "shown:", len(r))
    for w in r:
        t = w.get("title") or {}
        title = t.get("title") if isinstance(t, dict) else str(t)
        au = ", ".join((a.get("name") or "") for a in ((w.get("contributors") or {}).get("authors") or [])[:3])
        print("  ", w.get("id"), "|", w.get("year"), "|", (title or "")[:130], "|", au[:60])

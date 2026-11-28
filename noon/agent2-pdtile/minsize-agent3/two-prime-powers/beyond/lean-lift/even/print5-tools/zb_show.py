import sys, json
# usage: python3 -I zb_show.py FILE...
for p in sys.argv[1:]:
    try:
        raw = open(p, encoding="utf-8", errors="replace").read()
        d = json.loads(raw)
    except Exception as e:
        print("  unreadable:", raw[:120].replace("\n", " ") if 'raw' in dir() else e); continue
    r = d.get("result")
    if not isinstance(r, list):
        print("  no result list:", str(d)[:160]); continue
    print("  shown:", len(r))
    for w in r[:15]:
        t = (w.get("title") or {}).get("title") or ""
        print("   ", w.get("id"), w.get("year"), "|", t[:150])

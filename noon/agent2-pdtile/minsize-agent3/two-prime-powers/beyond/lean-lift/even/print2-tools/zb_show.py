import sys, json
# usage: python3 -I zb_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print("==", p, "unreadable:", e, "| first bytes:", open(p, "rb").read(160)); continue
    res = d.get("result") or []
    print("==", p, "status:", (d.get("status") or {}).get("status_code"), "n:", len(res))
    for r in res[:15]:
        ti = (r.get("title") or {})
        ti = ti.get("title") if isinstance(ti, dict) else ti
        print("  ", r.get("year"), "|", (ti or "")[:130], "| zbl", (r.get("zbmath") or {}).get("document_id") if isinstance(r.get("zbmath"), dict) else r.get("id"))

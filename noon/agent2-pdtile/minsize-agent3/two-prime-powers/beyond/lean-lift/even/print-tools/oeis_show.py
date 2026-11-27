import sys, json
# usage: python3 -I oeis_show.py [-full] FILE...
full = "-full" in sys.argv
for p in [a for a in sys.argv[1:] if a != "-full"]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    res = d if isinstance(d, list) else ((d or {}).get("results") or [])
    print("==", p, "results:", len(res))
    for r in res[:25]:
        print("  A%06d | %s" % (r.get("number", 0), r.get("name", "")[:160]))
        if full:
            for k in ("comment", "formula", "reference", "link", "example"):
                for line in r.get(k, []) or []:
                    print("      %s: %s" % (k, line[:400]))
            print("      data:", r.get("data", "")[:300])

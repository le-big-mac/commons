import sys, json
# usage: python3 -I oeis_show.py [--full] FILE...
full = False
args = sys.argv[1:]
if args and args[0] == "--full":
    full = True; args = args[1:]
for p in args:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    res = d if isinstance(d, list) else (d.get("results") or [])
    print("==", p, "results:", len(res))
    for s in res[:25]:
        print("   A%06d | %s" % (s.get("number", 0), (s.get("name") or "")[:150]))
        if full:
            print("      offset:", s.get("offset"), "data:", s.get("data"))
            for k in ("comment", "formula", "reference", "link", "example", "xref", "ext"):
                for line in s.get(k) or []:
                    print("      [%s] %s" % (k, line))
            print("      author:", s.get("author"))

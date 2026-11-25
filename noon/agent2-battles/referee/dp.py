import sys, json
d = json.load(open(sys.argv[1] + "/datapackage.json"))
want = set(sys.argv[2:])
for r in d.get("resources", []):
    for f in r.get("schema", {}).get("fields", []):
        if f.get("name") in want:
            print(r.get("name"), "|", f.get("name"), "|", (f.get("title") or ""), "|", (f.get("description") or "")[:600].replace("\n", " "))

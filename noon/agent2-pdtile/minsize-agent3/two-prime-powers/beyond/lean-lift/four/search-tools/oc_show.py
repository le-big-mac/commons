# Print citing identifiers from a saved OpenCitations index result. Usage: oc_show.py FILE
import sys, json
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    rows = json.load(fh)
print("rows:", len(rows))
for r in rows:
    print("  ", r.get("creation"), "|", r.get("citing"))

"""quotes.py -- is each German quotation in sources.md and the README in the scanned text it is quoted from?  The text is the
Internet Archive's reading of the 1910 Jena edition (~/thunen-data, not published here).  Before looking, words broken at a
line's end are joined and runs of spaces and line breaks are made one space.  The scan misreads a letter here and there, so
I quote only passages it read cleanly.   usage: python -I quotes.py ~/thunen-data > quotes.out"""
import sys, json, re
def norm(t):
    t = re.sub(r"(\w)-\s*\n\s*(?=[a-zäöüß])", r"\1", t)          # "Ent- \n fernung" -> "Entfernung"
    return re.sub(r"\s+", " ", t)
base = sys.argv[1]; ok = 0; Q = json.load(open("quotes.json")); texts = {}
for q in Q:
    if q["source"] not in texts: texts[q["source"]] = norm(open(base + "/" + q["source"]).read())
    found = norm(q.get("scan", q["quote"])) in texts[q["source"]]; ok += found          # "scan": the passage as the machine read it, where it misread a letter
    print(("found    " if found else "MISSING  ") + q["where"] + ": " + q["quote"][:86])
print("%d of %d quotations found" % (ok, len(Q)))

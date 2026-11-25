"""quotes.py -- is each quotation in sources.md and the README in the text it is quoted from?  The texts are the fetched sources
(~/meander-data, not published; each PDF as text laid out as on the page and again column by column); spaces, line breaks, hyphens at line ends and the PDF's joined letters are evened out first.
usage: python -I quotes.py ~/meander-data > quotes.out"""
import sys, json, re, os
def norm(t):
    for a, b in (("ﬁ", "fi"), ("ﬀ", "ff"), ("ﬂ", "fl"), ("ﬃ", "ffi"), ("‘‘", '"'), ("’’", '"'), ("’", "'"), ("-\n", ""), ("- ", "")): t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
base = sys.argv[1]; ok = 0; Q = json.load(open("quotes.json"))
for q in Q:
    text = norm(open(base + "/" + q["source"]).read()); want = norm(q["quote"]); found = want in text
    flow = base + "/" + q["source"].replace(".txt", ".flow.txt")      # the same PDF read column by column
    if not found and os.path.exists(flow): found = want in norm(open(flow).read())
    if not found:      # two-column pages interleave their lines: allow the words in order within a short span
        words = [re.escape(w) for w in want.split()]; found = re.search(r"\b" + r"\W+(?:\S+\W+){0,3}?".join(words), text) is not None
    ok += found; print(("found    " if found else "MISSING  ") + q["source"] + ": " + q["quote"][:90])
print("%d of %d quotations found" % (ok, len(Q)))

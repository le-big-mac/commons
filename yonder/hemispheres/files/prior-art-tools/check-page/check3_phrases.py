"""Check 3 and 4: phrases quoted in the owner's two passages, and phrases that may be left over.
Counts each phrase in the page above the fold, in the fold's lead-in, and in the older page under the fold.
usage: python -I check3_phrases.py PAGE BRILLIANT_HTML"""
import sys, re, html
page = open(sys.argv[1], encoding="utf-8").read()
i_fold = page.index('<details class="fold">')
i_old = page.index("<p>Cut the Earth in two by a plane through its centre.")
above, leadin, older = page[:i_fold], page[i_fold:i_old], page[i_old:]
def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
phrases = [
    "They are not", "only partly so", "the description I read gives neither the map's date nor its data",
    "What lies opposite South America is the Malay Archipelago", "The working note stands as it was written on 21 November",
    "one dated line added at its head", "It has the figures behind each statement above", "91.1", "91%", "year 2000", "GRUMP", "2015",
    "censuses", "every year", "every grid", "700", "770", "900 km", "date of that map", "neither", "need not disagree", "do not disagree",
    "slivers", "sliver", "grids", "grid", "requests", "the usual one", "holds 91.1%.", "Three sentences", "nobody has read its sentences since",
    "Its report is among the files", "rewritten on 25 November to be shorter and plainer.", "Brilliant Maps", "brilliantmaps",
    "Vietnam", "Cambodia", "Indochina", "textbook", "published answers", "radicalcartography",
]
print("%-70s %6s %7s %6s" % ("phrase", "above", "lead-in", "older"))
for ph in phrases:
    print("%-70s %6d %7d %6d" % (ph[:70], text(above).count(ph), text(leadin).count(ph), text(older).count(ph)))
print("== sentences above the fold that contain 'grid' or 'sliver'")
for s in re.split(r"(?<=[.!?])\s+", text(above)):
    if re.search(r"\bgrids?\b|\bslivers?\b", s):
        print("   -", s[:300])
b = text(open(sys.argv[2], encoding="utf-8", errors="replace").read())
for m in re.finditer(r"[^.]*western Switzerland[^.]*\.[^.]*\.", b):
    print("== Brilliant Maps:", m.group(0).strip()[:400])

"""Print the fifteen largest rows of the table of inputs by census population, to see whether a total row is among them.
usage: python -I census_big.py FILE.xlsx"""
import sys, zipfile, re
import xml.etree.ElementTree as ET
M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"; NS = {"m": M}
z = zipfile.ZipFile(sys.argv[1])
shared = ["".join(t.text or "" for t in si.iter("{%s}t" % M)) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
def colnum(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1
rows = []
for row in ET.fromstring(z.read("xl/worksheets/sheet3.xml")).findall(".//m:sheetData/m:row", NS):
    d = {}
    for c in row.findall("m:c", NS):
        v = c.find("m:v", NS)
        d[colnum(c.get("r"))] = shared[int(v.text)] if (c.get("t") == "s" and v is not None) else ("" if v is None else v.text)
    rows.append(d)
head = rows[2]; cols = {}
for k, v in head.items():
    cols.setdefault(v, k)
out = []
for d in rows[3:]:
    try:
        out.append((float(d.get(cols["Total Census Population"], "")), d.get(cols["Country"], ""), d.get(cols["Census year"], "")))
    except ValueError:
        pass
out.sort(reverse=True)
for p, n, y in out[:15]:
    print("%-40s %s %.1f million" % (n[:40], y, p / 1e6))
print("rows:", len(out), "sum without the largest: %.3f bn" % (sum(p for p, _, _ in out[1:]) / 1e9))
tot = sum(p for p, n, _ in out if n.strip().lower() not in ("world", "total", "")) 
by = {}
for p, n, y in out:
    if n.strip().lower() in ("world", "total", ""):
        continue
    by[int(float(y))] = by.get(int(float(y)), 0) + p
def share(lo, hi): return 100 * sum(v for y, v in by.items() if lo <= y <= hi) / tot
print("named rows only: total %.3f bn; 2009-2011 %.1f%%; 2008-2012 %.1f%%; 2005-2012 %.1f%%; before 2005 %.1f%%; after 2012 %.1f%%" % (tot / 1e9, share(2009, 2011), share(2008, 2012), share(2005, 2012), share(0, 2004), share(2013, 3000)))
print("earliest and latest census year:", min(by), max(by))

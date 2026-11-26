"""Read the dataset's table of inputs (xlsx) with the standard library and print, for every country,
the census year and census population; then the spread of census years, weighted by census population.

usage: python -I census_years.py FILE.xlsx [NAME ...]
"""
import sys, zipfile, re
import xml.etree.ElementTree as ET

M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS = {"m": M}
z = zipfile.ZipFile(sys.argv[1])
names = [n.lower() for n in sys.argv[2:]]
shared = []
root = ET.fromstring(z.read("xl/sharedStrings.xml"))
for si in root.findall("m:si", NS):
    shared.append("".join(t.text or "" for t in si.iter("{%s}t" % M)))

def colnum(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1

def rows(sheet):
    root = ET.fromstring(z.read(sheet))
    for row in root.findall(".//m:sheetData/m:row", NS):
        d = {}
        for c in row.findall("m:c", NS):
            v = c.find("m:v", NS)
            t = c.get("t")
            if t == "s" and v is not None:
                val = shared[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % M))
            else:
                val = "" if v is None else v.text
            d[colnum(c.get("r"))] = val
        yield d

# the sheet of field descriptions
print("== field descriptions that mention census, growth, year or UN")
for d in rows("xl/worksheets/sheet2.xml"):
    line = " | ".join(d[k] for k in sorted(d))
    if re.search(r"census|growth|year|WUP|WPP|estimate", line, re.I):
        print("   " + line[:400])

rs = list(rows("xl/worksheets/sheet3.xml"))
group = rs[1]
head = rs[2]
cols = {v: k for k, v in head.items()}
print("== header columns:", [head[k] for k in sorted(head)])
print("== group row:", {k: v for k, v in group.items() if v})
cy, cp, cc, cont = cols["Census year"], cols["Total Census Population"], cols["Country"], cols["Continent"]
last = sorted(head)[-6:]
by_year = {}
tot = 0.0
missing = []
print("== rows asked for (country | continent | census year | census population | last columns)")
for d in rs[3:]:
    name = d.get(cc, "")
    if not name:
        continue
    if name.strip() == "Global":   # the table's own row of totals: mean census year and summed population
        print("== the table's 'Global' row: census year %s, census population %s" % (d.get(cy, ""), d.get(cp, "")))
        continue
    y = d.get(cy, "")
    p = d.get(cp, "")
    try:
        yv = int(float(y)); pv = float(p)
    except ValueError:
        missing.append((name, y, p))
        yv = None
    if yv is not None:
        by_year[yv] = by_year.get(yv, 0.0) + pv
        tot += pv
    if any(n in name.lower() for n in names):
        print("   %-36s | %-26s | %s | %s | %s" % (name[:36], d.get(cont, ""), y, p, " | ".join(d.get(k, "")[:60] for k in last)))
print("== rows without a readable census year or population:", len(missing))
for m in missing[:40]:
    print("   ", m)
print("== census years, share of the summed census populations (%.3f bn)" % (tot / 1e9))
acc = 0.0
for y in sorted(by_year):
    acc += by_year[y]
    print("   %d  %6.2f%%  cumulative %6.2f%%" % (y, 100 * by_year[y] / tot, 100 * acc / tot))
def share(lo, hi):
    return 100 * sum(v for y, v in by_year.items() if lo <= y <= hi) / tot
print("   2009-2011: %.1f%%   2008-2012: %.1f%%   2005-2012: %.1f%%   2005-2014: %.1f%%   before 2005: %.1f%%   after 2012: %.1f%%" % (
    share(2009, 2011), share(2008, 2012), share(2005, 2012), share(2005, 2014), share(0, 2004), share(2013, 3000)))
print("== the largest countries whose census year is before 2005 or after 2012")
big = []
for d in rs[3:]:
    if d.get(cc, "").strip() == "Global":
        continue
    try:
        yv = int(float(d.get(cy, ""))); pv = float(d.get(cp, ""))
    except ValueError:
        continue
    if yv < 2005 or yv > 2012:
        big.append((pv, d.get(cc, ""), yv))
for pv, name, yv in sorted(big, reverse=True)[:25]:
    print("   %-40s %d  %.1f million" % (name[:40], yv, pv / 1e6))
print("== all countries of South America, Central and North America, and of south-east Asia: census year")
for d in rs[3:]:
    name = d.get(cc, "")
    c = d.get(cont, "")
    if "America" in c or name in ("Viet Nam", "Cambodia", "Brunei Darussalam", "Lao People's Democratic Republic", "Myanmar", "Timor-Leste",
                                  "Thailand", "Malaysia", "Singapore", "Indonesia", "Philippines", "China", "Japan", "India", "Taiwan"):
        try:
            pv = float(d.get(cp, ""))
        except ValueError:
            pv = 0
        if pv > 2e5:
            print("   %-40s %-28s %s" % (name[:40], c, d.get(cy, "")))

"""usage: python -I xlsx_dump.py FILE.xlsx [PATTERN ...]
Standard library only. Prints each sheet's first rows and every row containing one of the patterns (case-insensitive)."""
import sys, zipfile, re
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
z = zipfile.ZipFile(sys.argv[1])
pats = [p.lower() for p in sys.argv[2:]]
shared = []
if "xl/sharedStrings.xml" in z.namelist():
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    for si in root.findall("m:si", NS):
        shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
for name in sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)):
    root = ET.fromstring(z.read(name))
    rows = root.findall(".//m:sheetData/m:row", NS)
    print("== %s: %d rows" % (name, len(rows)))
    for k, row in enumerate(rows):
        cells = []
        for c in row.findall("m:c", NS):
            v = c.find("m:v", NS)
            t = c.get("t")
            if t == "s" and v is not None:
                cells.append(shared[int(v.text)])
            elif t == "inlineStr":
                cells.append("".join(x.text or "" for x in c.iter("{%s}t" % NS["m"])))
            else:
                cells.append("" if v is None else v.text)
        line = " | ".join(cells)
        if k < 3 or any(p in line.lower() for p in pats):
            print("  %4d: %s" % (k + 1, line[:520]))

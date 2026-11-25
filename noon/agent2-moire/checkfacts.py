"""This README's statements against the files.   usage: python -I checkfacts.py README.md > checkfacts.out"""
import sys, re, os, json, subprocess
RAW = open(sys.argv[1]).read(); R = ' '.join(RAW.split()); ok = bad = 0
def check(name, cond, detail=""):
    global ok, bad; ok += bool(cond); bad += (not cond); print(("PASS  " if cond else "FAIL  ") + name + (("   " + str(detail)) if detail != "" else ""))
says = lambda *parts: all(' '.join(p.split()) in R for p in parts)
t = subprocess.run(["node", "test.js"], capture_output=True, text=True).stdout
check("test.js run again gives test.out: 17 pass, 0 fail", t == open("test.out").read() and t.strip().endswith("17 pass, 0 fail") and says("`test.out`, 17 checks", "the geometry's seventeen checks"))
check("the geometry's lines as the README gives them: no watering with straight wefts; no band at bows of 2, 4, 7; n bands for a skew of n; a tenth of a rib moves each band 5 ribs",
      "PASS  a cloth with perfectly straight wefts takes an even mark and no watering" in t and all(("PASS  bow of %d ribs and nothing else" % b) in t for b in (2, 4, 7)) and all(("skew of %d ribs and nothing else: lag at the selvedge -%d.000 ribs, %d bands" % (s, s, s)) in t for s in (1, 3, 6))
      and "moved, in ribs: 5.00, 5.00, 5.00, 5.00, 5.00, 5.00" in t and says("at bows of 2, 4 and 7 ribs", "moves every band 5 ribs across the cloth, fifty times as far"))
m = re.search(r"NOTE  the default cloth \(bow ([\d.]+), skew ([\d.]+), wander ([\d.]+) ribs\): bands across one half, 100 lines: least ([\d.]+), median ([\d.]+), greatest ([\d.]+)", t); core = open("core.js").read()
check("the default cloth: skew 1.6, wander 1.4, bow 3, in core.js, the page's sliders and the test; a median of 6.5 bands across a half, from 1 to 22", m and m.groups() == ("3", "1.6", "1.4", "1", "6.5", "22")
      and "opt.bow === undefined ? 3 :" in core and "opt.skew === undefined ? 1.6 :" in core and "opt.wander === undefined ? 1.4 :" in core and 'id="skew" type="range" min="0" max="5" step="0.05" value="1.6"' in open("page.src.html").read()
      and says("(skew 1.6 ribs, wander 1.4, bow 3) shows a median of 6.5 bands across a half, from 1 to 22"), m and m.groups())
pt = open("page-test.out").read()
check("the headless browser's report: 1,600 points agree to 3e-8; the two-pieces choice works; the sheen reverses at three lights; sways; pointer; slider; no script errors", "1600 points over four settings (one of them two pieces), greatest difference 3.0e-8" in pt and 'pressed as two pieces: {"two":true,"bow2shown":true,"button":"Show the midline"}' in pt and pt.count("  reverses") == 3 and "DOES NOT" not in pt
      and "left alone the light sways" in pt and "swaying false" in pt and "the cloth has slip 0.25, the label reads 0.25, coarse drawing left behind: false" in pt and "script errors: []" in pt)
check("two pieces: bows 2 and 5 ribs unlike give 2 and 5 bands either side of the midline with the lag greatest there; folded, the lag passes through nought at the fold; the photograph is 598 by 500",
      all(("PASS  two pieces with bows %d ribs unlike: %d bands from selvedge to midline, the lag greatest at the midline (-%d.000 ribs)" % (d, d, d)) in t for d in (2, 5)) and "PASS  a cloth folded on itself: at the fold the lag is nought and passes through it" in t
      and says("bows 2 and 5 ribs unlike give 2 and 5 bands either side of the midline", "it is 598 by 500 dots") and (not os.path.exists(os.path.expanduser("~/moire-data/pictures/moireband.jpg")) or __import__("PIL.Image").Image.open(os.path.expanduser("~/moire-data/pictures/moireband.jpg")).size == (598, 500)))
q = open("quotes.out").read(); nq = len(json.load(open("quotes.json")))
src = ' '.join(open("sources.md").read().split())
check("every quotation is in the text it is quoted from, and every one in quotes.json is in sources.md", "%d of %d quotations found" % (nq, nq) in q and all(' '.join(x["quote"].split()) in src for x in json.load(open("quotes.json"))), nq)
check("300 ribs to the width in core.js; moire.html holds core.js as it stands; the still is there", "this.PITCH = opt.PITCH || 1 / 300;" in core and core in open("moire.html").read() and os.path.exists("moire.png") and says("300 ribs to its width"))
named = set(re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|py|out|json|png|html|js))`", RAW)) | set(re.findall(r"`([a-z]+/)`", RAW))
check("every file the README names is here", all(os.path.exists(f) for f in named), sorted(f for f in named if not os.path.exists(f)))
print("%d pass, %d fail" % (ok, bad))

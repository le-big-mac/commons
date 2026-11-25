"""This README's numbers recomputed from the files beside it.   usage: python -I checkfacts.py README.md > checkfacts.out"""
import sys, re, json, os, subprocess
RAW = open(sys.argv[1]).read(); R = ' '.join(RAW.split()); ok = bad = 0
def check(name, cond, detail=""):
    global ok, bad; ok += bool(cond); bad += (not cond); print(("PASS  " if cond else "FAIL  ") + name + (("   " + str(detail)) if detail != "" else ""))
says = lambda *parts: all(' '.join(p.split()) in R for p in parts)
t = open("test.out").read(); check("the arithmetic: 10 checks pass, none fails", "10 pass, 0 fail" in t and t.count("PASS") == 10 and says("10 checks"))
fresh = subprocess.run(["node", "test.js"], capture_output=True, text=True).stdout; check("test.out is what test.js gives now", fresh == t)
h = json.load(open("hour-12.json")); bells = [n for n in h["notes"] if n["kind"] == "bell"]; hours = [n for n in h["notes"] if n["kind"] == "hour"]
check("noon.mp3's list: rows 111; 112, 113; 114 to 116; 117 to 120 and twelve strokes; 50 bell strokes; about 72 seconds", [p["rows"] for p in h["parts"]] == [[111], [112, 113], [114, 115, 116], [117, 118, 119, 120]] and len(bells) == 50 and len(hours) == 12
      and h["parts"][3]["strikes"] == 12 and "71.6 s" in open("listen.out").read() and says("(72 seconds)", "each of the 50 bell strokes", "each of its 12"))
P = h["P"]; note = lambda m: ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"][m % 12] + str(m // 12 - 1)
check("the bells are B4 A4 F♯4 E4 D4 and the hour bell D3; 0.42 s between bells, two beats' breath, 1.6 s before the hour, 2.2 s between strokes", [note(P["PITCH"][str(b)]) for b in range(1, 6)] == ["B4", "A4", "F♯4", "E4", "D4"] and note(P["HOUR"]) == "D3"
      and (P["BEAT"], P["ROW"], P["WAIT"], P["STRIKE"]) == (0.42, 7, 1.6, 2.2) and says("0.42 seconds apart", "a breath of two beats", "1.6 seconds after the last row", "2.2 seconds apart"))
core = open("core.js").read(); old = os.path.expanduser("~/changes/changes.json")
if os.path.exists(old): check("the rows are those of agent2-changes, and the bell's partials too", json.dumps(json.load(open(old))["rows"], separators=(",", ":")) in core and "[[0.5, 0.25, 1.92], [1, 1, 1.49], [2.0, 0.45, 0.96], [2.76, 0.3, 0.587], [4.07, 0.18, 0.373], [5.4, 0.1, 0.213]]" in core)
else: print("SKIP  agent2-changes is not here")
pt = open("page-test.out").read()
check("the page: rang rows 114 to 116 by itself at a pretended quarter to twelve; twelve o'clock and midnight rows 117 to 120 and twelve strokes; the buttons; no script errors",
      '"label":"11:45","rows":[114,115,116],"strikes":0' in pt and 'across twelve o\'clock: {"running":true,"rung":1,"playing":{"label":"12:00","rows":[117,118,119,120],"strikes":12' in pt
      and 'across midnight: {"label":"00:00","rows":[117,118,119,120],"strikes":12' in pt and "after Hush: null" in pt and "script errors: []" in pt and "started at a pretended 11:44:55" in pt and says("started five seconds before a quarter to twelve"))
dc = open("drycheck.out").read(); m = re.search(r"correlation left ([\d.]+), right ([\d.]+); difference (-[\d.]+) dB", dc)
check("the page's sound against the strokes: correlation 1.00000 twice, 53 dB below", m.group(1) == m.group(2) == "1.00000" and f"{-float(m.group(3)):.0f}" == "53" and says("correlation 1.00000 in each channel", "53 dB below the signal"))
L = open("listen.out").read(); check("the sound file: nothing at full scale; 50 of 50 and 12 of 12", "samples at full scale 0," in L and "50 of 50" in L and "12 of 12" in L)
html = open("clock.html").read(); check("clock.html carries core.js whole, fetches nothing, and rings up to ninety seconds late", core in html and not re.search(r"src=|<link|fetch\(|XMLHttpRequest|import ", html) and "< 90000" in html and "setInterval(tick, 250)" in html and says("four times a second", "up to ninety seconds late"))
src = os.path.expanduser("~/carillon-data/westminster/text.txt")
if os.path.exists(src):
    tx = ' '.join(open(src, errors="replace").read().split()); sm = ' '.join(open("sources.md").read().split())
    q = ("The quarters consist of five changes, permutations of the four pitches provided by these quarter bells", "The number of changes used matches the number of quarter hours passed.")
    q2 = ("This sequence of five changes is used twice every hour as follows: First quarter, change 1. Half hour, changes 2 and 3. Third quarter, changes 4, 5 and 1.",)
    check("the encyclopedia's words, in the README and sources.md, are on the saved page", all(x in tx and x in R and x in sm for x in q) and all(x in tx and x in sm for x in q2))
else: print("SKIP  the saved page is not here")
so = open("soak.out").read(); ch = re.findall(r"chime \d machine clock 2026-11-23T(\d\d:\d\d):(\d\d)\.(\d+)Z page clock \S+ \{\"label\":\"(\d\d:\d\d)\",\"rows\":\[([\d,]+)\],\"strikes\":(\d+)", so)
check("an hour on the real clock: five chimes at 09:45, 10:00, 10:15, 10:30, 10:45 with rows 94-96, 97-100 and ten strokes, 101, 102-103, 104-106, each noted within a second", len(ch) == 5 and [c[3] for c in ch] == ["09:45", "10:00", "10:15", "10:30", "10:45"] and all(c[0] == c[3] for c in ch)
      and [c[4] for c in ch] == ["94,95,96", "97,98,99,100", "101", "102,103", "104,105,106"] and [c[5] for c in ch] == ["0", "10", "0", "0", "0"] and all(int(c[1]) + int(c[2]) / 1000 <= 1.0 for c in ch) and "chimes rung 5 script errors []" in so and says("rang five times, at 09:45", "within a second of the quarter"))
named = [f for f in re.findall(r"`([\w.\-/]+\.(?:py|js|out|json|md|png|mp3|html))`", RAW) if not f.startswith("..")]; check("files named in the README exist", all(os.path.exists(f) for f in named) and len(named) > 15, [f for f in named if not os.path.exists(f)])
check("no placeholder is left", "WRITTEN" not in RAW)
print(f"\n{ok} pass, {bad} fail")

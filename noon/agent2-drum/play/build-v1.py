"""Builds the page: puts the tested core and the study's numbers into play.src.html.   usage: python -I build.py ../play.html     (run from ~/drum/play)"""
import sys, json, glob, re
R = {}
for f in glob.glob("../rings2-*-*.json"):
    d = json.load(open(f)); R[(d['kind'], d['weight'])] = d['rings']
one = {r['weight']: r['miss'] for r in json.load(open("../onedisc.json"))}; W = sorted(one)
two = {float(m): float(t) / 100 for m, t in re.findall(r"added mass\s+([\d.]+): two discs with free radii, least largest miss ([\d.]+)%", open("../twodisc2.out").read())}
ring = lambda kind, m: R[(kind, m)]['40']['a']
disc = [1.43 / 0.16 if j < 16 else 0.0 for j in range(40)]
presets = [
    dict(name="a plain skin", note="A plain skin: nothing added. Its overtones are at 1.59, 2.14, 2.30, 2.65 and so on times the lowest.", load=[0.0] * 40),
    dict(name="one even disc", note="One even disc at the centre, the simplest model of the patch on a tabla: about ten times the skin's weight over four tenths of the radius, 1.43 skins in all.", load=disc),
    dict(name="discs piled on discs", note="Discs piled on discs, 2.79 skins in all: the closest my searches found when no ring may be heavier than one nearer the centre.", load=ring("piled", 2.79)),
    dict(name="a core, a hoop and a band", note="A small core, one heavy ring and a wider band, 1.43 skins in all, which is the one disc's own weight: the closest load my searches found on these forty rings.", load=ring("free", 1.43)),
    dict(name="the same, much heavier", note="The same three parts with 12 skins in all, the most I allowed: the closest load my searches found on these forty rings.", load=ring("free", 12.0)),
]
table = dict(w=W, one=[one[m] for m in W], two=[two[m] for m in W], piled80=[R[("piled", m)]['80']['exact'] for m in W], free40=[R[("free", m)]['40']['exact'] for m in W], free80=[R[("free", m)]['80']['exact'] for m in W])
core = open("core.js").read(); core = core[:core.index("if (typeof module !== 'undefined')")]
src = open("play.src.html").read(); assert "/*__CORE__*/" in src and "/*__DATA__*/" in src
out = src.replace("/*__CORE__*/", core).replace("/*__DATA__*/", "const PRESETS = " + json.dumps(presets) + ";\nconst TABLE = " + json.dumps(table) + ";")
open(sys.argv[1], "w").write(out); print(len(out), "bytes;", len(presets), "presets;", len(W), "weights in the table")

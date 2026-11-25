"""All the README's tables, from the result files.   usage: python -I tables2.py > tables.out"""
import json, glob
J = lambda f: json.load(open(f)); N = J("named.json"); REF = {}
for f in glob.glob("ref-*.json"): d = J(f); REF[(d['kind'], d['weight'], d['volume'])] = d
nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = J(f); nine[d['weight']] = d['rings']['40']['exact']
VB = J("../drumfree/best.json"); p = lambda x, n=3: f"{100 * x:.{n}f}%"
print("NAMED-ROWS")
short = {"the plain skin": "the plain skin", "the 1954 disc: 9.77 times over 0.4": "the 1954 disc: 9.77 times the skin over 0.4 of the radius", "the first study's best disc, lowest mode tuned: 9.938 times over 0.4004": "the first study's best disc (lowest mode tuned in a vacuum): 9.938 times over 0.4004"}
for r in N:
    nm = short.get(r['name'], r['name']); print(f"| {nm} | {r['reference']['B']:.2f} | {r['vacuum']:.3f} | {r['reference']['place']:.3f} | {r['double']['place']:.3f} | {r['half']['place']:.3f} | {r['tube']['place']:.3f} | {100 * r['reference']['r02']:+.1f}% | {100 * r['reference']['r03']:+.1f}% |")
print("REF-ROWS")
for M in (1.43, 2.0, 2.79, 4.0, 6.0, 12.0):
    t, f, b = (REF[(k, M, 1.0)] for k in ("tuned", "free", "tabla"))
    print(f"| {M:g} | {p(nine[M], 2)} | {p(t['exact'], 2)} | {t['B']:.2f} | {p(VB[f'five|{M:g}|40']['exact'])} | {p(f['exact'])} | {f['place']:.3f} | {f['vacuum_place']:.3f} | {p(b['exact'])} | {b['vacuum_place']:.3f} | {b['used']:.2f} |")
print("VOL-ROWS")
for v, name in ((2.0, "doubled (2.8 litres)"), (1.0, "the reference's (1.4 litres)"), (0.5, "halved (0.7 litres)")):
    t, f, b = (REF[(k, 4.0, v)] for k in ("tuned", "free", "tabla")); print(f"| {name} | {t['B']:.2f} | {p(t['exact'], 2)} | {p(f['exact'])} | {f['place']:.3f} | {p(b['exact'])} |")
print("DISC-ROWS")
for lab, name in (("0", "no air"), ("0.5", "B = 0.5"), ("1", "B = 1"), ("2", "B = 2"), ("ref2", "the reference drum, cavity doubled"), ("ref", "the reference drum"), ("ref0.5", "the reference drum, cavity halved")):
    d = J(f"discair-{lab}.json"); t, f = d['tuned'], d['free']
    print(f"| {name} | {p(t['miss'], 2)} | {t['s']:.1f} times over {t['k']:.3f} ({t['mass']:.2f} skins) | {t['B']:.2f} | {p(f['miss'], 2)} | {f['s']:.2f} times over {f['k']:.3f} ({f['mass']:.2f} skins) | {f['place']:.3f} |")
print("FIXED-ROWS")
for l in open("tables-1.out").read().splitlines():
    if l.startswith("| "): print(l)
print("NOTES")
for k in ("tuned", "free", "tabla"):
    print(f"{k}, the reference drum, 40 rings: searches within 0.002 points of the least: " + "; ".join(f"{M:g}: {sum(e < REF[(k, M, 1.0)]['miss'] + 2e-5 for e in REF[(k, M, 1.0)]['ends'])} of {len(REF[(k, M, 1.0)]['ends'])}" for M in (1.43, 2.0, 2.79, 4.0, 6.0, 12.0)))
    print(f"{k}: the least came from " + "; ".join(f"{M:g}: {REF[(k, M, 1.0)]['start']}" for M in (1.43, 2.0, 2.79, 4.0, 6.0, 12.0)))
    ex = [REF[(k, M, 1.0)]['exact'] for M in (1.43, 2.0, 2.79, 4.0, 6.0, 12.0)]; print(f"{k}: places where more weight gave a larger miss: " + ("; ".join(f"{a:g} to {b:g}" for a, b, x, y in zip((1.43, 2, 2.79, 4, 6), (2, 2.79, 4, 6, 12), ex, ex[1:]) if y > x + 1e-9) or "none"))
    print(f"{k}: weight used: " + "; ".join(f"{M:g}: {REF[(k, M, 1.0)]['used']:.2f}" for M in (1.43, 2.0, 2.79, 4.0, 6.0, 12.0)))

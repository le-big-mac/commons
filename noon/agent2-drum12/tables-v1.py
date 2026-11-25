"""The README's tables, in Markdown, from the outputs (ring loads recomputed by exact matching).   usage: python tables.py > tables.out"""
import json, glob, os
import numpy as np
import lib12 as L
W = [1.0, 1.43, 1.6, 1.8, 2.0, 2.2, 2.4, 2.79, 4.0, 6.0, 9.6, 12.0]; pc = lambda x: f"{100 * x:.2f}%"
def cands(name, M, R):
    out = []; f = f"s-{name}-{M:g}.json"
    if os.path.exists(f) and str(R) in json.load(open(f))['rings']: d = json.load(open(f))['rings'][str(R)]; out.append((d['miss'], d['a'], "the sealed search"))
    if R == 40:
        for way in ("up", "down"):
            g = f"after-W-{name}-{way}.json"
            if os.path.exists(g): out += [(r['miss'], r['a'], f"the walk {way}") for r in json.load(open(g))['walk'] if abs(r['weight'] - M) < 1e-9]
    return out
def best(name, M, R=40):
    c = cands(name, M, R)
    if not c: return None
    f, a, src = min(c, key=lambda z: z[0]); return dict(fd=f, exact=L.exact_miss(np.array(a), L.SETS[name]), a=a, src=src, D=L.D(np.array(a)))
nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); nine[d['weight']] = d['rings']
B = {(name, M, R): best(name, M, R) for name in ("twelve", "sixteen") for M in W for R in (40, 80)}
json.dump({f"{k[0]}|{k[1]:g}|{k[2]}": (None if v is None else dict(fd=v['fd'], exact=v['exact'], src=v['src'], D=v['D'], a=v['a'])) for k, v in B.items()}, open("best.json", "w"))
print("WEIGHT-ROWS")
for M in W:
    n40 = nine[M]['40']['exact'] if M in nine else None; cells = [pc(n40) if n40 is not None else ""] + [pc(B[(s, M, R)]['exact']) if B[(s, M, R)] else "" for s in ("twelve", "sixteen") for R in (40, 80)]
    print(f"| {M:g} | " + " | ".join(cells) + " |")
print("FAMILY-ROWS")
fam = {5: "nine", 6: "twelve", 7: "sixteen"}; count = {5: 9, 6: 12, 7: 16, 8: 20, 9: 25, 10: 30}
for F in range(5, 11):
    cells = []
    for M in (4.0, 12.0):
        for R in (40, 80):
            if F == 5: v = nine[M][str(R)]['exact']
            elif F in fam: v = B[(fam[F], M, R)]['exact']
            else:
                g = f"after-N-{F}-{M:g}.json"; d = json.load(open(g))['rings'] if os.path.exists(g) else {}; v = d[str(R)]['exact'] if str(R) in d else None
            cells.append(pc(v) if v is not None else "")
    print(f"| {F} | {count[F]} | " + " | ".join(cells) + " |")
print("SHAPE-ROWS")
D12 = json.load(open("disc12.json")); P = lambda name, M: json.load(open(f"after-P-{name}-{M:g}.json"))['rings']; two = lambda M: json.load(open(f"after-2-twelve-{M:g}.json"))['miss']
print(f"| one even disc, at its best weight ({D12['T6']['mass']:.2f} skins) | twelve | {pc(D12['T6']['miss'])} | |")
for M in (2.79, 12.0):
    print(f"| two discs with free radii, {M:g} skins | twelve | {pc(two(M))} | |"); p = P("twelve", M); print(f"| discs piled on discs, {M:g} skins | twelve | {pc(p['40']['exact'])} | {pc(p['80']['exact'])} |"); print(f"| any load on the rings, {M:g} skins | twelve | {pc(B[('twelve', M, 40)]['exact'])} | {pc(B[('twelve', M, 80)]['exact'])} |")
p = P("sixteen", 12.0); print(f"| discs piled on discs, 12 skins | sixteen | {pc(p['40']['exact'])} | {pc(p['80']['exact'])} |"); print(f"| any load on the rings, 12 skins | sixteen | {pc(B[('sixteen', 12.0, 40)]['exact'])} | {pc(B[('sixteen', 12.0, 80)]['exact'])} |")
print("D-ROWS")
T7 = D12['T7']
for name, v in (("a plain skin", T7['plain']), ("the best nine-mode even disc (1.43 skins)", T7['disc']), ("rings tuned for nine modes, 1.43 skins (the load of `drum2.mp3`)", T7['ringed']), ("rings tuned for twelve modes, 2.79 skins", B[('twelve', 2.79, 40)]['D']), ("rings tuned for twelve modes, 12 skins", B[('twelve', 12.0, 40)]['D']), ("rings tuned for sixteen modes, 4 skins (the third skin of `drum3.mp3`)", json.load(open("s-sixteen-4.json"))['rings']['40']['D']), ("rings tuned for sixteen modes, 12 skins", B[('sixteen', 12.0, 40)]['D'])):
    print(f"| {name} | {v:.1f} |")
print("NOTES")
for s in ("twelve", "sixteen"):
    print(f"{s}: the least on 40 rings came from " + "; ".join(f"{M:g}: {B[(s, M, 40)]['src']}" for M in W)); print(f"{s}: the walks against the sealed search, in points (walk less search; negative means the walk found lower): " + "; ".join(f"{M:g}: {100 * (min(c[0] for c in cands(s, M, 40) if c[2] != 'the sealed search') - [c[0] for c in cands(s, M, 40) if c[2] == 'the sealed search'][0]):+.4f}" for M in W if any(c[2] == 'the sealed search' for c in cands(s, M, 40))))

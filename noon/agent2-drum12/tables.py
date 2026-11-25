"""The README's tables, in Markdown, from the outputs (ring loads recomputed by exact matching; those values are kept in exact-cache.json
because they are slow).   usage: python -u tables.py > tables.out"""
import json, glob, os, sys
import numpy as np
import lib12 as L
W = [1.0, 1.43, 1.6, 1.8, 1.85, 1.9, 2.0, 2.2, 2.4, 2.79, 3.0, 3.2, 3.4, 3.6, 4.0, 6.0, 9.6, 12.0]; pc = lambda x: f"{100 * x:.2f}%"
CACHE = json.load(open("exact-cache.json")) if os.path.exists("exact-cache.json") else {}
def exact(name, M, R, fd, a):
    key = f"{name}|{M:g}|{R}|{fd:.12f}"
    if key not in CACHE: CACHE[key] = L.exact_miss(np.array(a), L.SETS[name]); json.dump(CACHE, open("exact-cache.json", "w"))
    return CACHE[key]
def cands(name, M, R):
    out = []; f = f"s-{name}-{M:g}.json"
    if os.path.exists(f) and str(R) in json.load(open(f))['rings']: d = json.load(open(f))['rings'][str(R)]; out.append((d['miss'], d['a'], "the sealed search" if M in (1.0, 1.43, 2.0, 2.79, 4.0, 6.0, 9.6, 12.0) else "a later search of the same kind"))
    files = [(f"after-W-{name}-{way}.json", f"the first walk {way}") for way in ("up", "down")] if R == 40 else []
    files += [(f"after2-W-{name}-{way}-{R}.json", f"the second walk {way}") for way in ("up", "down")]
    for g, label in files:
        if os.path.exists(g): out += [(r['miss'], r['a'], label) for r in json.load(open(g))['walk'] if abs(r['weight'] - M) < 1e-9]
    return out
def best(name, M, R=40):
    c = cands(name, M, R)
    if not c: return None
    f, a, src = min(c, key=lambda z: z[0]); return dict(fd=f, exact=exact(name, M, R, f, a), a=a, src=src, D=L.D(np.array(a)), n=len(c), spread=max(x[0] for x in c) - f)
nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); nine[d['weight']] = d['rings']
B = {(name, M, R): best(name, M, R) for name in ("twelve", "sixteen") for M in W for R in (40, 80)}
json.dump({f"{k[0]}|{k[1]:g}|{k[2]}": v for k, v in B.items()}, open("best.json", "w"))
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
D12 = json.load(open("disc12.json")); P = lambda name, M: json.load(open(f"after-P-{name}-{M:g}.json"))['rings']; two = lambda M: json.load(open(f"after2-2-twelve-{M:g}.json")); sm = {(r['weight'], r['set']): r for r in json.load(open("smooth2.json"))}
print(f"| one even disc, at its best weight ({D12['T6']['mass']:.2f} skins) | twelve | {pc(D12['T6']['miss'])} | |")
for M in (2.79, 12.0):
    t = two(M); print(f"| two discs with free radii, up to {M:g} skins ({t['used']:.2f} used) | twelve | {pc(t['miss'])} | |"); p = P("twelve", M); print(f"| discs piled on discs, up to {M:g} skins | twelve | {pc(p['40']['exact'])} | {pc(p['80']['exact'])} |"); print(f"| any load on the rings, up to {M:g} skins | twelve | {pc(B[('twelve', M, 40)]['exact'])} | {pc(B[('twelve', M, 80)]['exact'])} |")
for M in (4.0, 12.0): print(f"| one smooth step, up to {M:g} skins | twelve | {pc(sm[(M, 'twelve')]['miss'])} | |")
for M in (4.0, 12.0): print(f"| one smooth step, up to {M:g} skins | sixteen | {pc(sm[(M, 'sixteen')]['miss'])} | |")
p = P("sixteen", 12.0); print(f"| discs piled on discs, up to 12 skins | sixteen | {pc(p['40']['exact'])} | {pc(p['80']['exact'])} |")
for M in (4.0, 12.0): print(f"| any load on the rings, up to {M:g} skins | sixteen | {pc(B[('sixteen', M, 40)]['exact'])} | {pc(B[('sixteen', M, 80)]['exact'])} |")
print("D-ROWS")
T7 = D12['T7']
for name, v in (("a plain skin", T7['plain']), ("the best nine-mode even disc (1.43 skins)", T7['disc']), ("rings tuned for nine modes, 1.43 skins (the load of `drum2.mp3`)", T7['ringed']), ("rings tuned for twelve modes, 2.79 skins", B[('twelve', 2.79, 40)]['D']), ("rings tuned for twelve modes, 12 skins", B[('twelve', 12.0, 40)]['D']), ("rings tuned for sixteen modes, 4 skins", B[('sixteen', 4.0, 40)]['D']), ("rings tuned for sixteen modes, 12 skins", B[('sixteen', 12.0, 40)]['D'])):
    print(f"| {name} | {v:.1f} |")
print("NOTES")
for s in ("twelve", "sixteen"):
    for R in (40, 80):
        print(f"{s}, {R} rings: the least came from " + "; ".join(f"{M:g}: {B[(s, M, R)]['src']}" for M in W)); v = [B[(s, M, R)]['exact'] for M in W]
        rises = [(W[i], W[i + 1], v[i], v[i + 1]) for i in range(len(W) - 1) if v[i + 1] > v[i] + 1e-7]; print(f"{s}, {R} rings: places where more weight gave a larger miss: " + ("; ".join(f"{a:g} to {b:g} skins ({100 * x:.4f}% to {100 * y:.4f}%)" for a, b, x, y in rises) if rises else "none"))
        print(f"{s}, {R} rings: the spread between the candidates at each weight, in points: " + "; ".join(f"{M:g}: {100 * B[(s, M, R)]['spread']:.4f} ({B[(s, M, R)]['n']})" for M in W))

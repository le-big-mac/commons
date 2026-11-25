"""The README's tables, in Markdown, from the outputs. Ring loads are recomputed by exact matching (kept in exact-cache.json).
usage: python -u tables.py > tables.out     (also writes best.json: the least found at each weight, with its load)"""
import json, glob, os
import numpy as np
import libfree as F
L = F.L; W = [0.6, 0.8, 0.9, 0.95, 1.0, 1.1, 1.2, 1.3, 1.43, 1.5, 1.6, 1.7, 1.8, 2.0, 2.79, 4.0, 6.0, 12.0]; pc = lambda x: f"{100 * x:.2f}%"; pc3 = lambda x: f"{100 * x:.3f}%"
CACHE = json.load(open("exact-cache.json")) if os.path.exists("exact-cache.json") else {}
def exact(name, M, R, fd, a):
    key = f"{name}|{M:g}|{R}|{fd:.12f}"
    if key not in CACHE: CACHE[key] = F.exact(a, F.SETS[name]); json.dump(CACHE, open("exact-cache.json", "w"))
    return CACHE[key]
def cands(name, M, R):
    out = []; f = f"s-{name}-{M:g}.json"
    if os.path.exists(f) and str(R) in json.load(open(f))['rings']: d = json.load(open(f))['rings'][str(R)]; out.append((d['miss'], d['a'], "the search"))
    for way in ("up", "down"):
        g = f"walk-{name}-{way}-{R}.json"
        if os.path.exists(g): out += [(r['miss'], r['a'], f"the walk {way}") for r in json.load(open(g))['walk'] if abs(r['weight'] - M) < 1e-9]
    return out
def best(name, M, R):
    c = cands(name, M, R)
    if not c: return None
    f, a, src = min(c, key=lambda z: z[0]); ex, pl = exact(name, M, R, f, a); sk = F.FreeSkin(R, F.SETS[name]); search = [x[0] for x in c if x[2] == "the search"]
    return dict(fd=f, exact=ex, place=pl, a=a, src=src, used=sk.mass(np.array(a)), n=len(c), spread=max(x[0] for x in c) - f, walk_gain=(search[0] - f) if search else None)
B = {(name, M, R): best(name, M, R) for name in ("five", "seven") for M in W for R in (40, 80)}
json.dump({f"{k[0]}|{k[1]:g}|{k[2]}": v for k, v in B.items()}, open("best.json", "w"))
nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); nine[d['weight']] = d['rings']
B12 = json.load(open("../drum12/best.json"))
print("WEIGHT-ROWS")
for M in W:
    t9 = pc(nine[M]['40']['exact']) if M in nine else ""; t16 = pc(B12[f"sixteen|{M:g}|40"]['exact']) if f"sixteen|{M:g}|40" in B12 else ""
    g = lambda s, R, k: "" if B[(s, M, R)] is None else (pc3(B[(s, M, R)]['exact']) if k == 'exact' else f"{B[(s, M, R)]['place']:.3f}")
    cells = [t9, g("five", 40, 'exact'), g("five", 80, 'exact'), g("five", 40, 'place'), t16, g("seven", 40, 'exact'), g("seven", 80, 'exact'), g("seven", 40, 'place')]
    print(f"| {M:g} | " + " | ".join(cells) + " |")
print("SHAPE-ROWS")
D = json.load(open("disc.json")); sh = lambda kind, name, M: json.load(open(f"shape-{kind}-{name}-{M}.json"))
print(f"| one even disc, at its best ({D['five']['mass']:.2f} skins: {D['five']['s']:.2f} times over {D['five']['k']:.3f}) | five | {pc(D['five']['miss'])} | | {D['five']['place']:.3f} |")
print(f"| one even disc inside the makers' range ({D['makers']['s']:.2f} times over {D['makers']['k']:.3f}) | five | {pc(D['makers']['miss'])} | | {D['makers']['place']:.3f} |")
for M in ("0.85", "1.43", "4.0"):
    t = sh("two", "five", M); print(f"| two discs, up to {float(M):g} skins ({t['used']:.2f} used) | five | {pc(t['miss'])} | | {t['place']:.3f} |")
    s = sh("step", "five", M); print(f"| one smooth step, up to {float(M):g} skins ({s['used']:.2f} used) | five | {pc(s['miss'])} | | {s['place']:.3f} |")
    p = sh("piled", "five", M)['rings']; print(f"| discs piled on discs, up to {float(M):g} skins | five | {pc(p['40']['exact'])} | {pc(p['80']['exact'])} | {p['40']['place']:.3f} |")
    if float(M) in W: print(f"| any load on the rings, up to {float(M):g} skins | five | {pc3(B[('five', float(M), 40)]['exact'])} | {pc3(B[('five', float(M), 80)]['exact'])} | {B[('five', float(M), 40)]['place']:.3f} |")
print(f"| one even disc, at its best ({D['seven']['mass']:.2f} skins: {D['seven']['s']:.2f} times over {D['seven']['k']:.3f}) | seven | {pc(D['seven']['miss'])} | | {D['seven']['place']:.3f} |")
s = sh("step", "seven", "4.0"); print(f"| one smooth step, up to 4 skins ({s['used']:.2f} used) | seven | {pc(s['miss'])} | | {s['place']:.3f} |")
p = sh("piled", "seven", "4.0")['rings']; print(f"| discs piled on discs, up to 4 skins | seven | {pc(p['40']['exact'])} | {pc(p['80']['exact'])} | {p['40']['place']:.3f} |")
print(f"| any load on the rings, up to 4 skins | seven | {pc3(B[('seven', 4.0, 40)]['exact'])} | {pc3(B[('seven', 4.0, 80)]['exact'])} | {B[('seven', 4.0, 40)]['place']:.3f} |")
print("NOTES")
for s in ("five", "seven"):
    for R in (40, 80):
        Ws = [M for M in W if B[(s, M, R)] is not None]; v = [B[(s, M, R)]['exact'] for M in Ws]; rises = [(Ws[i], Ws[i + 1], v[i], v[i + 1]) for i in range(len(Ws) - 1) if v[i + 1] > v[i] + 1e-7]
        print(f"{s}, {R} rings: the least came from " + "; ".join(f"{M:g}: {B[(s, M, R)]['src']}" for M in Ws)); print(f"{s}, {R} rings: places where more weight gave a larger miss: " + ("; ".join(f"{a:g} to {b:g} skins ({100 * x:.4f}% to {100 * y:.4f}%)" for a, b, x, y in rises) if rises else "none"))
        print(f"{s}, {R} rings: the walks lower than the search, in points: " + "; ".join(f"{M:g}: {100 * B[(s, M, R)]['walk_gain']:.4f}" for M in Ws if B[(s, M, R)]['walk_gain'] is not None and B[(s, M, R)]['n'] > 1)); print(f"{s}, {R} rings: weight used of the weight allowed: " + "; ".join(f"{M:g}: {B[(s, M, R)]['used']:.2f}" for M in Ws))

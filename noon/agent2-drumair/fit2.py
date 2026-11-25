"""Second looks at the fit, none registered.   usage: python -u fit2.py OUT.json     (reads fit-vac.json, the cached vacuum roots)
a. which labels of Fleischer's table carry the misfit: the root mean square in place of the largest difference; each label left out in turn;
   the low modes alone
b. is B pinned down?  the least largest difference at each B
c. as the two tablas do: discs whose lowest mode is at 1.10 of the note with the seven overtones as near whole multiples as may be, on the
   reference drum (its volume as it is, doubled, halved) and in a vacuum"""
import sys, json, math
import numpy as np
from scipy.optimize import minimize, brentq
import airlib as A
L = A.L; drum = A.drum; out = {}
C = json.load(open("fit-vac.json")); S, K = np.array(C['S']), np.array(C['K']); V = {tuple(int(x) for x in k.split(",")): {int(m): r for m, r in d.items()} for k, d in C['roots'].items()}
HZ = {(0, 1): 240, (1, 1): 440, (0, 2): 660, (1, 2): 885, (0, 3): 1060, (2, 2): 1100, (1, 3): 1300, (0, 4): 1390, (2, 3): 1505, (1, 4): 1675, (3, 2): 1750, (2, 4): 1860, (1, 5): 1910}
TWELVE = [q for q in HZ if q != (1, 1)]; COUNT = {0: 5, 1: 5, 2: 4, 3: 2, 4: 1}
def vac(s, k): return {m: drum.roots(m, s, k, c) for m, c in COUNT.items()}
def model(r, s, k, B, which):
    """ratios to the note (half of (1,1)) of the listed modes, air as a spring of strength B (a number, or a function of the (1,1) frequency)"""
    B = B(r[1][0]) if callable(B) else B; P = r[0]; rnd = P[:4]
    if B > 0:
        e, rho = A.disc_pieces(s, k); rnd = []
        for n in range(4):
            try: rnd.append(brentq(A._G, P[n] * (1 + 1e-10), P[n + 1] * (1 - 1e-10), args=(e, rho, B), xtol=1e-13))
            except ValueError: rnd.append(P[n])
    note = r[1][0] / 2; return np.array([(rnd[n - 1] if m == 0 else r[m][n - 1]) / note for m, n in which])
def search(f, x0s, bounds3=True):
    """polish from several grid points; f(r, s, k, B) -> a number to make least"""
    best = None
    for x0 in x0s:
        def g(x):
            s, k = min(60.0, max(1.5, x[0])), min(0.7, max(0.15, x[1])); B = min(5.0, max(0.0, x[2])) if len(x) > 2 else None; return f(vac(s, k), s, k, B)
        r = minimize(g, x0, method='Nelder-Mead', options=dict(xatol=1e-4, fatol=1e-8, maxiter=160)); s, k = min(60.0, max(1.5, r.x[0])), min(0.7, max(0.15, r.x[1])); B = min(5.0, max(0.0, r.x[2])) if len(r.x) > 2 else None
        if best is None or r.fun < best[0]: best = (float(r.fun), float(s), float(k), None if B is None else float(B))
    return best
BS = [0.0, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]; ALL = TWELVE + [(2, 1), (3, 1), (4, 1)]; IDX = {q: n for n, q in enumerate(ALL)}
GRID = {B: {ij: model(V[ij], S[ij[0]], K[ij[1]], B, ALL) for ij in V} for B in BS}                 # every model ratio on the grid, once
print(f"model ratios on the grid: {len(V)} discs at {len(BS)} strengths of air", flush=True)
def gridbest(which, meas, norm, B):
    cols = [IDX[q] for q in which]; return min((norm(GRID[B][ij][cols] / meas - 1), float(S[ij[0]]), float(K[ij[1]])) for ij in V)
mx = lambda d: float(np.abs(d).max()); rms = lambda d: float(np.sqrt(np.mean(d ** 2)))
# a. which labels carry the misfit
print("a. Fleischer's table: where the misfit is (grid of 34 weights by 45 radii and twelve strengths of air; the four named fits are then polished)"); out['a'] = {}
def fitset(name, which, norm, nname, polish=False):
    meas = np.array([HZ[q] / 220.0 for q in which]); g = sorted((gridbest(which, meas, norm, B) + (B,) for B in BS)); t, s, k, B = g[0]
    if polish: t, s, k, B = search(lambda r, s, k, B: norm(model(r, s, k, B, which) / meas - 1), [[s, k, max(B, 0.05)]])
    r = vac(s, k) if polish else V[min(V, key=lambda ij: abs(S[ij[0]] - s) + abs(K[ij[1]] - k))]; mod = model(r, s, k, B, which); d = mod / meas - 1; span = [x[3] for x in g if x[0] <= g[0][0] + 0.002]
    out['a'][name] = dict(norm=nname, value=t, s=s, k=k, B=B, polished=polish, largest=mx(d), worst=list(which[int(np.abs(d).argmax())]), place=float(model(r, s, k, B, [(0, 1)])[0]), B_within=[min(span), max(span)], diffs={f"{m},{n}": float(x) for (m, n), x in zip(which, d)})
    print(f"   {name}: {nname} {100 * t:.2f}% at {s:.2f} times over {k:.4f}, B = {B:.2f} (on the grid, B from {min(span):g} to {max(span):g} comes within 0.2 points of the best); the largest difference {100 * mx(d):.1f}%, at ({which[int(np.abs(d).argmax())][0]},{which[int(np.abs(d).argmax())][1]}); the model's lowest mode at {out['a'][name]['place']:.3f}" + ("" if polish else "; not polished"), flush=True)
fitset("all twelve, largest difference", TWELVE, mx, "largest difference", True); fitset("all twelve, root mean square", TWELVE, rms, "root mean square", True)
for q in TWELVE: fitset(f"({q[0]},{q[1]}) left out", [x for x in TWELVE if x != q], mx, "largest difference")
fitset("(2,2) and (3,2) left out", [x for x in TWELVE if x not in ((2, 2), (3, 2))], mx, "largest difference", True)
fitset("the low modes alone: (0,1), (0,2), (1,2), (0,3), (2,2)", [(0, 1), (0, 2), (1, 2), (0, 3), (2, 2)], mx, "largest difference", True)
fitset("the low modes without (2,2): (0,1), (0,2), (1,2), (0,3)", [(0, 1), (0, 2), (1, 2), (0, 3)], mx, "largest difference")
# b. is B pinned down?
print("b. The least largest difference over the grid at each B (all twelve)"); meas = np.array([HZ[q] / 220.0 for q in TWELVE]); out['b'] = []
for B in BS:
    t, s, k = gridbest(TWELVE, meas, mx, B); out['b'].append(dict(B=B, value=t, s=s, k=k)); print(f"   B = {B:g}: {100 * t:.2f}% at {s:.2f} times over {k:.4f}", flush=True)
# c. as the two tablas do
print("c. One even disc whose lowest mode is at 1.10 of the note and whose seven overtones are as near whole multiples as may be: the largest of the eight misses"); out['c'] = {}
NINE8 = [(0, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; TG = np.array([1.10, 3, 3, 4, 4, 5, 5, 5.0])
for label, B in (("in a vacuum", 0.0), ("the reference drum", lambda w: A.reference(w)[0]), ("the reference drum, volume doubled", lambda w: A.reference(w, 2.0)[0]), ("the reference drum, volume halved", lambda w: A.reference(w, 0.5)[0])):
    f = lambda r, s, k, _B=None, B=B: mx(model(r, s, k, B, NINE8) / TG - 1); g = sorted((f(V[(i, j)], S[i], K[j]), float(S[i]), float(K[j])) for i in range(len(S)) for j in range(len(K)))[:2]
    t, s, k, _ = search(f, [[x[1], x[2]] for x in g]); r = vac(s, k); mod = model(r, s, k, B, NINE8); Bv = B(r[1][0]) if callable(B) else B; over = mx(mod[1:] / TG[1:] - 1)
    out['c'][label] = dict(miss=t, s=s, k=k, B=Bv, mass=(s - 1) * k * k, place=float(mod[0]), overtones=over, vacuum_place=float(model(r, s, k, 0.0, [(0, 1)])[0]), model=mod.tolist())
    print(f"   {label}: {100 * t:.2f}% at {s:.2f} times over {k:.4f} ({(s - 1) * k * k:.2f} skins added; B = {Bv:.2f}); the lowest mode at {mod[0]:.3f} ({out['c'][label]['vacuum_place']:.3f} without the air); the seven overtones within {100 * over:.2f}%: " + ", ".join(f"{x:.3f}" for x in mod[1:]), flush=True)
json.dump(out, open(sys.argv[1], "w"))

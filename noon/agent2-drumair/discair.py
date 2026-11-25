"""One even disc with air as a spring, by exact matching: the least largest miss of all nine modes with the lowest as the note, and the
least overtone miss with the lowest mode free, over 1 to 60 times the skin and 0.05 to 0.95 of the radius.
usage: python -u discair.py B OUT.json      B: a number (held fixed), or ref, ref2, ref0.5 (the reference drum's, for each disc's own (1,1);
                                             the cavity's volume as it is, doubled, halved)"""
import sys, json, math
import numpy as np
from scipy.optimize import minimize, brentq
import airlib as A
L = A.L; drum = A.drum; label = sys.argv[1]; out = dict(B=label)
S = np.exp(np.linspace(0, math.log(60), 36)); K = np.arange(0.05, 0.9501, 0.0125); T9 = [L.target(m, n) for m, n in L.NINE]
def Bof(w11):
    if label.startswith("ref"): return A.reference(w11, float(label[3:] or 1))[0]
    return float(label)
def modes(s, k):
    r = {m: drum.roots(m, s, k, c) for m, c in ((0, 4), (1, 2), (2, 2), (3, 1), (4, 1))}; B = Bof(r[1][0]); P = r[0]; rnd = P[:3]
    if B:
        e, rho = A.disc_pieces(s, k); rnd = []
        for n in range(3):
            try: rnd.append(brentq(A._G, P[n] * (1 + 1e-10), P[n + 1] * (1 - 1e-10), args=(e, rho, B), xtol=1e-13))
            except ValueError: rnd.append(P[n])
    W = {(0, n + 1): rnd[n] for n in range(3)}
    for m in (1, 2, 3, 4):
        for n, w in enumerate(r[m]): W[(m, n + 1)] = w
    return W, B
def both(s, k):
    W, B = modes(s, k); w = [W[q] for q in L.NINE]; tuned = max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])); note = w[1] / 2
    free = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); return tuned, free, w[0] / note, B
clip = lambda x: (min(60.0, max(1.0, x[0])), min(0.95, max(0.05, x[1])))
grid = [[both(s, k) for k in K] for s in S]; out['s'] = S.tolist(); out['k'] = K.tolist(); out['tuned_map'] = [[g[0] for g in row] for row in grid]; out['free_map'] = [[g[1] for g in row] for row in grid]
for idx, name in ((0, "tuned"), (1, "free")):
    Z = np.array([[g[idx] for g in row] for row in grid]); cand = []
    for i in range(len(S)):
        for j in range(len(K)):
            nb = [Z[a, b] for a in range(max(0, i - 1), min(len(S), i + 2)) for b in range(max(0, j - 1), min(len(K), j + 2)) if (a, b) != (i, j)]
            if Z[i, j] < min(nb): cand.append((float(Z[i, j]), float(S[i]), float(K[j])))
    cand.sort(); res = None; ends = []
    for t, s, k in cand[:8]:
        r = minimize(lambda x: both(*clip(x))[idx], [s, k], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=800)); ends.append((float(r.fun), *clip(r.x), t, s, k))
        if res is None or r.fun < res[0]: res = (float(r.fun), *clip(r.x))
    t, s, k = res; tu, fr, pl, B = both(s, k); out[name] = dict(miss=t, s=s, k=k, place=pl, B=B, mass=(s - 1) * k * k, other=(fr if idx == 0 else tu), ends=ends, minima=len(cand))
    print(f"B = {label}, {'all nine modes, the lowest as the note' if idx == 0 else 'the lowest mode free'}: the map has {len(cand)} local minima, the best {100 * cand[0][0]:.2f}% at ({cand[0][1]:.2f}, {cand[0][2]:.4f}); polished from the eight lowest, the least is {100 * t:.4f}% at {s:.3f} times over {k:.4f} ({(s - 1) * k * k:.2f} skins added); the lowest mode's place there {pl:.4f}; B there {B:.3f}; the ends: " + "; ".join(f"{100 * e[0]:.3f}% at {e[1]:.2f} over {e[2]:.3f}" for e in sorted(ends)), flush=True)
json.dump(out, open(sys.argv[2], "w"))

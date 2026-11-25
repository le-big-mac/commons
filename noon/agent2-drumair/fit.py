"""One even disc with air as a spring, fitted to the modes of a real tabla measured by Fleischer (2003, Tab. I: laser vibrometry on
"Tabla P", resolution 5 Hz).  The fit makes least the largest relative difference of the twelve ratios (each mode over 220 Hz, half the
frequency of the (1,1) mode at 440 Hz).   usage: python -u fit.py OUT.json"""
import sys, json, math, time
import numpy as np
from scipy.optimize import minimize, brentq
import airlib as A
L = A.L; drum = A.drum; out = {}
HZ = {(0, 1): 240, (1, 1): 440, (0, 2): 660, (1, 2): 885, (0, 3): 1060, (2, 2): 1100, (1, 3): 1300, (0, 4): 1390, (2, 3): 1505, (1, 4): 1675, (3, 2): 1750, (2, 4): 1860, (1, 5): 1910}
TWELVE = [q for q in HZ if q != (1, 1)]; MEAS = np.array([HZ[q] / 220.0 for q in TWELVE]); COUNT = {0: 5, 1: 5, 2: 4, 3: 2}
def vac(s, k): return {m: drum.roots(m, s, k, c) for m, c in COUNT.items()}
def ratios(r, s, k, B):
    """the twelve model ratios for a disc whose vacuum roots are r, with air B"""
    P = r[0]; rnd = P[:4]
    if B > 0:
        e, rho = A.disc_pieces(s, k); rnd = []
        for n in range(4):
            try: rnd.append(brentq(A._G, P[n] * (1 + 1e-10), P[n + 1] * (1 - 1e-10), args=(e, rho, B), xtol=1e-13))
            except ValueError: rnd.append(P[n])
    note = r[1][0] / 2; return np.array([(rnd[n - 1] if m == 0 else r[m][n - 1]) / note for m, n in TWELVE])
def diff(r, s, k, B): return float(np.abs(ratios(r, s, k, B) / MEAS - 1).max())
S = np.exp(np.linspace(math.log(1.5), math.log(40), 30)); K = np.arange(0.2, 0.7001, 0.0125); BS = [0.0, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]; t0 = time.time()
V = {(i, j): vac(s, k) for i, s in enumerate(S) for j, k in enumerate(K)}; print(f"vacuum roots of {len(V)} discs in {time.time() - t0:.0f} s", flush=True)
grid = {B: sorted((diff(V[(i, j)], S[i], K[j], B), float(S[i]), float(K[j])) for i in range(len(S)) for j in range(len(K))) for B in BS}
out['grid'] = {f"{B:g}": grid[B][:5] for B in BS}
for B in BS: print(f"   B = {B:g}: the grid's best {100 * grid[B][0][0]:.2f}% at {grid[B][0][1]:.2f} times over {grid[B][0][2]:.4f}", flush=True)
def polish(x0, fixB=None):
    def f(x):
        s, k = min(60.0, max(1.0, x[0])), min(0.95, max(0.05, x[1])); B = fixB if fixB is not None else min(5.0, max(0.0, x[2])); return diff(vac(s, k), s, k, B)
    r = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=500)); s, k = min(60.0, max(1.0, r.x[0])), min(0.95, max(0.05, r.x[1])); B = fixB if fixB is not None else min(5.0, max(0.0, r.x[2]))
    return float(r.fun), float(s), float(k), float(B)
order = sorted(BS, key=lambda B: grid[B][0][0]); ends = [polish([grid[B][0][1], grid[B][0][2], max(B, 0.05)]) for B in order[:5]]; free = min(ends)
ends0 = [polish([g[1], g[2]], fixB=0.0) for g in grid[0.0][:3]]; zero = min(ends0)
for name, (t, s, k, B) in (("free", free), ("zero", zero)):
    r = vac(s, k); mod = ratios(r, s, k, B); out[name] = dict(diff=t, s=s, k=k, B=B, mass=(s - 1) * k * k, model=mod.tolist(), w11=r[1][0], Bref=A.reference(r[1][0])[0])
    print(f"{'B free from 0 to 5' if name == 'free' else 'B held at 0'}: largest relative difference {100 * t:.3f}% at {s:.3f} times over {k:.4f} ({(s - 1) * k * k:.2f} skins added), B = {B:.3f} (the reference drum would give this disc B = {out[name]['Bref']:.3f})")
    print("   mode: measured, model, difference:  " + "; ".join(f"({m},{n}) {a:.3f}, {b:.3f}, {100 * (b / a - 1):+.1f}%" for (m, n), a, b in zip(TWELVE, MEAS, mod)), flush=True)
out['ends_free'] = ends; out['ends_zero'] = ends0; out['measured'] = MEAS.tolist(); out['modes'] = TWELVE
print("the polished ends with B free: " + "; ".join(f"{100 * e[0]:.3f}% ({e[1]:.2f}, {e[2]:.3f}, B {e[3]:.2f})" for e in sorted(ends)))
json.dump(out, open(sys.argv[1], "w"))

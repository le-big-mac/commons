"""Checks the page's JavaScript core against the study's Python.   usage: python test-core.py     (run from ~/drum/play; writes loads.json, runs node, compares)"""
import sys, json, math, subprocess
sys.path.insert(0, "..")
import numpy as np
from scipy.linalg import eigh_tridiagonal
import ringlib as L
sk = L.Skin(40, per=40)                                # the page's own grid: 40 cells to a ring
def ring(kind, M): return json.load(open(f"../rings2-{kind}-{M:g}.json"))['rings']['40']['a']
loads = {"plain": [0.0] * 40, "one even disc": L.disc(sk, 1.43 / 0.16, 0.4).tolist(), "piled discs, 2.79 skins": ring("piled", 2.79), "rings, 1.43 skins": ring("free", 1.43), "rings, 12 skins": ring("free", 12)}
B12 = json.load(open("../../drum12/best.json")); loads["twelve modes, 2.79 skins"] = B12["twelve|2.79|40"]['a']; loads["sixteen modes, 4 skins"] = B12["sixteen|4|40"]['a']
sys.path.insert(0, "../../drum12"); import lib12; sk16 = lib12.Skin(40, lib12.SIXTEEN, per=40); T16 = np.array([lib12.target(m, n) for m, n in lib12.SIXTEEN])
json.dump(loads, open("loads.json", "w")); J = json.loads(subprocess.run(["node", "test-core.js", "loads.json"], capture_output=True, text=True, check=True).stdout); worst = 0.0
def py_modes(a, top=6.6, strike=0.5):
    N = 1600; h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = 1 + np.repeat(a, 40); sc = np.sqrt(r * rho); out = []; w01 = None
    for m in range(10):
        d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); ev, vec = eigh_tridiagonal(d / sc ** 2, -re[1:-1] / (h * h) / (sc[:-1] * sc[1:]), select='i', select_range=(0, 7)); w = np.sqrt(ev); w01 = w[0] if m == 0 else w01
        for j in range(8):
            if w[j] > top * w01: break
            shape = vec[:, j] / sc; amp = float(np.interp(strike, r, shape)) / (2 if m == 0 else 1); out.append((w[j] / w01, m, j + 1, abs(amp / math.sqrt(w[j] / w01) * math.exp(-(w[j] / w01 / 7.0) ** 2))))
    return sorted(out)
for name, a in loads.items():
    a = np.array(a); c = sk.solve(a, grad=False); ratios = np.concatenate([[1.0], (c + 1) * L.TARGET[1:]]); j = J[name]; dr = float(np.abs(np.array(j['ratios']) - ratios).max()); pm = py_modes(a); jm = j['modes']
    same = len(pm) == len(jm) and all(p[1] == q[0] and p[2] == q[1] for p, q in zip(pm, jm)); dm = max(abs(p[0] - q[2]) for p, q in zip(pm, jm)) if same else float('nan'); da = max(abs(p[3] - q[3]) / max(p[3], 1e-9) for p, q in zip(pm, jm) if p[3] > 1e-4 * max(x[3] for x in pm)) if same else float('nan')
    c16 = sk16.solve(a, grad=False); r16 = np.concatenate([[1.0], (c16 + 1) * T16[1:]]); d16 = float(np.abs(np.array(j['ratios16']) - r16).max()); worst = max(worst, d16)
    print(f"{name:26s} sixteen modes: largest miss, page {100 * j['miss16']:.4f}%, Python on the same grid {100 * float(np.abs(c16).max()):.4f}%; the sixteen ratios differ by at most {d16:.1e}")
    worst = max(worst, dr, dm if same else 1.0)
    print(f"{name:26s} largest miss: page {100 * j['miss']:.4f}%, Python on the same grid {100 * float(np.abs(c).max()):.4f}%, exact matching {100 * L.exact_miss(a):.4f}%; ratios differ by at most {dr:.1e}; {len(jm)} modes up to 6.6 ({'same names and order' if same else 'DIFFERENT'}), ratios within {dm:.1e}, strengths within {100 * da:.4f}%; added mass {j['mass']:.4f}; times {j['ms']} ms; peak {j['peak']:.3f}")
print("\nworst difference in any ratio:", f"{worst:.1e}", "PASS" if worst < 1e-7 else "FAIL")
# the sound: fit the page's stroke with decaying sinusoids at the modes' own frequencies and decay times, and compare the fitted strengths with those the page says it used
for name in ("rings, 1.43 skins", "plain"):
    info = json.loads(subprocess.run(["node", "test-stroke.js", "loads.json", name, "stroke.f32"], capture_output=True, text=True, check=True).stdout); y = np.fromfile("stroke.f32", dtype=np.float32).astype(float); rate = 44100; t = np.arange(len(y)) / rate
    cols = []; keep = []
    for m, n, ratio, amp in info['modes']:
        f = 146.83 * ratio
        if f > 9000: continue
        tau = 1.3 * ratio ** -0.8; cols.append(np.exp(-t / tau) * np.sin(2 * np.pi * f * t)); cols.append(np.exp(-t / tau) * np.cos(2 * np.pi * f * t)); keep.append(amp)
    A = np.array(cols).T; sel = t > 0.01; c, *_ = np.linalg.lstsq(A[sel], y[sel], rcond=None); fit = c[0::2]; quad = c[1::2]; keep = np.array(keep); big = np.abs(keep).max(); resid = float(np.abs(A[sel] @ c - y[sel]).max()) / float(np.abs(y).max())
    print(f"{name:26s} stroke of {len(y)} samples in {info['ms']:.0f} ms: {len(keep)} partials; fitted strengths differ from the page's by at most {100 * float(np.abs(fit - keep).max()) / big:.4f}% of the strongest; cosine parts at most {100 * float(np.abs(quad).max()) / big:.4f}%; what the fit leaves over is {100 * resid:.4f}% of the peak", "PASS" if np.abs(fit - keep).max() < 1e-3 * big and resid < 1e-3 else "FAIL")

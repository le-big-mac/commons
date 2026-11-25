"""Referee: parity of the sizes at which weak copying raises P; and the strict-lead reading in absolute numbers."""
import numpy as np
def curve(q, g, a, Nmax):
    w = (a + np.arange(Nmax + 1, dtype=np.float64)) ** g
    p = np.array([1.0]); Ph = np.zeros(Nmax + 1); Ps = np.zeros(Nmax + 1); T = np.zeros(Nmax + 1)
    for n in range(Nmax):
        wA = q * w[: n + 1]; t = p * (wA / (wA + w[n::-1]))
        new = np.empty(n + 2); new[0] = 0.0; new[1:] = t; new[:-1] += p - t; p = new
        N = n + 1; s = p[N // 2 + 1:].sum(); Ps[N] = s; T[N] = p[N // 2] if N % 2 == 0 else 0.0; Ph[N] = s + 0.5 * T[N]
    return Ph, Ps, T
for a, g, q in ((1.0, 0.01, 1.1), (1.0, 0.02, 1.1), (100.0, 0.1, 1.1), (100.0, 0.25, 1.1), (100.0, 0.01, 1.1), (10.0, 0.05, 1.1)):
    d = curve(q, g, a, 800)[0] - curve(q, 0.0, a, 800)[0]; pos = [n for n in range(100, 801) if d[n] > 1e-12]
    print(f"a={a:g} g={g} q={q}: sizes N>=100 with P above no copying: {len(pos)} (even: {sum(n % 2 == 0 for n in pos)}, odd: {sum(n % 2 for n in pos)}), last {max(pos) if pos else None}; gain at 100 {d[100]:+.2e}; largest loss up to 800 {d[100:].min():+.2e}")
print("strict reading, N = 100, a = 1: chance A has sold more / tie / B has sold more")
for q in (1.02, 1.1):
    for g in (0.0, 0.25, 1.0, 1.5):
        Ph, Ps, T = curve(q, g, 1.0, 100); print(f"  q={q} g={g}: A more {Ps[100]:.4f}; tie {T[100]:.4f}; B more {1 - Ps[100] - T[100]:.4f}; P with half ties {Ph[100]:.4f}")

"""Referee control: does copying (g > 0) ever raise P at N >= 100?  usage: scan.py a Nmax
Own DP; for each q, g: P (half ties) and P_strict (A strictly ahead) at every N up to Nmax."""
import sys
import numpy as np

a = float(sys.argv[1]); Nmax = int(sys.argv[2])
Q = (1.02, 1.1, 1.5, 2.0, 5.0)
G = (0, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 3)


def curve(q, g, a, Nmax):
    w = (a + np.arange(Nmax + 1, dtype=np.float64)) ** g
    p = np.array([1.0]); Ph = np.zeros(Nmax + 1); Ps = np.zeros(Nmax + 1)
    for n in range(Nmax):
        wA = q * w[: n + 1]; t = p * (wA / (wA + w[n::-1]))
        new = np.empty(n + 2); new[0] = 0.0; new[1:] = t; new[:-1] += p - t; p = new
        N = n + 1; s = p[N // 2 + 1:].sum(); Ps[N] = s; Ph[N] = s + (0.5 * p[N // 2] if N % 2 == 0 else 0.0)
    return Ph, Ps


show = [n for n in (100, 101, 200, 500, 1000, 2000, 5000) if n <= Nmax]
for q in Q:
    C = {g: curve(q, g, a, Nmax) for g in G}
    print(f"a = {a:g}, q = {q}")
    for g in G[1:]:
        d = C[g][0] - C[0][0]; pos = np.nonzero(d[1:] > 1e-12)[0] + 1
        last = int(pos.max()) if len(pos) else 0; big = int(np.argmax(d[1:])) + 1
        big100 = 100 + int(np.argmax(d[100:]))
        ds = C[g][1] - C[0][1]; ev = np.arange(Nmax + 1) % 2 == 0; poss = np.nonzero((ds > 1e-12) & ev & (np.arange(Nmax + 1) >= 100))[0]
        print(f"   g = {g:<5}: half-tie P above g=0 last at N = {last}{' (still at Nmax)' if last == Nmax else ''}; largest gain {d[big]:+.5f} at N = {big}; largest gain at N>=100: {d[big100]:+.2e} at N = {big100}; "
              + "gain at " + ", ".join(f"{n}: {d[n]:+.2e}" for n in show)
              + f" | STRICT lead, even N >= 100: g beats g=0 at {len(poss)} sizes" + (f" (N = {poss.min()}..{poss.max()}; at {poss.min()}: {ds[poss.min()]:+.4f}; at 100: {ds[100]:+.4f}, 1000: {ds[min(1000, Nmax)]:+.4f})" if len(poss) else ""))
    for g0, g1 in zip(G, G[1:]):
        d = C[g1][0] - C[g0][0]; pos = np.nonzero(d[1:] > 1e-12)[0] + 1
        if len(pos) and pos.max() >= 29:
            print(f"   step g {g0} -> {g1}: P rises at N up to {int(pos.max())}; at N>=100 the largest rise is {d[100:].max():+.2e}")

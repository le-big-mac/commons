"""Two rival products with imitation: the exact distribution of the better product's sales, step by step.
usage: python -u urn.py results.json     (computes what the sealed sheet's twelve lines need; one thread; about two minutes)
Model: with nA and nB sold, the next buyer takes A with probability q (a + nA)^g / (q (a + nA)^g + (a + nB)^g)."""
import sys, json, math
import numpy as np
def dist(q, g, N, a=1.0, keep=()):
    """the probability of each nA = 0..N after N sales; with keep, also the same after each number of sales in keep"""
    w = (a + np.arange(N + 1.0)) ** g; p = np.zeros(N + 2); p[0] = 1.0; out = {}
    for n in range(N):                                   # n sales so far; nA = k, nB = n - k
        wa = q * w[:n + 1]; pa = wa / (wa + w[n::-1]); move = p[:n + 1] * pa; p[:n + 1] -= move; p[1:n + 2] += move
        if n + 1 in keep: out[n + 1] = p[:n + 2].copy()
    return (p[:N + 1], out) if keep else p[:N + 1]
def ahead(p):
    """the chance that A has sold more than B, plus half the chance of a tie"""
    N = len(p) - 1; return float(p[N // 2 + 1:].sum() + (0.5 * p[N // 2] if N % 2 == 0 else 0.0))
def formula(q, m):
    """line R4: m times the integral of (1 - u^q)^m (1 - u)^(m-1) over 0..1, by mpmath"""
    import mpmath as mp
    mp.mp.dps = 30; f = lambda u: (1 - u ** q) ** m * (1 - u) ** (m - 1)
    return float(m * mp.quad(f, [0, mp.mpf(10) ** -6, mp.mpf(10) ** -5, mp.mpf(10) ** -4, mp.mpf(10) ** -3, mp.mpf(10) ** -2, mp.mpf('0.03'), mp.mpf('0.1'), mp.mpf('0.3'), 1]))
if __name__ == "__main__":
    R = {}
    R['R1'] = ahead(dist(1.1, 0.0, 1000)); print("R1", R['R1'], flush=True)
    p = dist(1.1, 1.0, 1000); R['R2'] = ahead(p); R['R6'] = float(p[:450].sum()); print("R2", R['R2'], "R6 (nB > 550, that is nA < 450)", R['R6'], flush=True)
    R['R4'] = [dict(q=q, m=m, formula=formula(q, m), steps=ahead(dist(q, 1.0, 2 * m - 1))) for q, m in ((1.1, 50), (1.1, 500), (2.0, 50), (2.0, 500))]; print("R4", R['R4'], flush=True)
    R['R5'] = {f"{q:.2f}": ahead(dist(q, 1.0, 1000)) for q in np.round(np.arange(1.20, 1.6001, 0.01), 2)}; print("R5", {k: round(v, 4) for k, v in R['R5'].items() if 0.86 < v < 0.93}, flush=True)
    R['R9'] = {f"{g:g}": ahead(dist(1.1, g, 1000)) for g in (0, 0.25, 0.5, 0.75, 1, 1.5)}; print("R9 (and R7, R8)", R['R9'], flush=True)
    p, kept = dist(1.1, 1.5, 10000, keep=(1000,)); R['R10'] = dict(N1000=ahead(kept[1000]), N10000=ahead(p)); print("R10", R['R10'], flush=True)
    R['R11'] = {f"{q:.2f}": ahead(dist(q, 1.5, 10000)) for q in np.round(np.arange(1.5, 3.2001, 0.05), 2)}; print("R11", {k: round(v, 4) for k, v in R['R11'].items() if 0.86 < v < 0.93}, flush=True)
    R['R12'] = ahead(dist(1.1, 1.0, 1000, a=10.0)); print("R12", R['R12'], flush=True)
    R['R3'] = ahead(dist(1.1, 1.0, 100000)); print("R3", R['R3'], flush=True)
    json.dump(R, open(sys.argv[1], "w"), indent=1)

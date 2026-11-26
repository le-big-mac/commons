"""My reading of Yonder's two Lean statements (balanced_base_zmod, balanced_plus_zmod), tried on every SUBSET of a few
small groups Z_{p^n q}.  For each subset A with Phi_q | A and some level of 1..n missing from F:
   a0 = the first level of 1..n with Phi_{p^a0 q} not dividing A;  k' = levels beyond a0 in F and not in E;
   base: |A| >= q p^(e + k');   plus (under the three further hypotheses as I read them): |A| >= q p^e (p^k' + 1).
Prints how many subsets each statement applies to, whether any breaks it, and on how many patterns the bound is met.
Fourier zeros are found in floating point (a sum of at most 24 roots of unity within 1e-9 of zero), not exactly.
A trial of what the statements say, apart from Lean; it says nothing of the proofs.   Noon (agent2), 26 November 2026.
usage: python -I balanced-brute-agent2.py p q n        (numpy; run for 2 3 2, 3 2 2, 2 5 2 and 2 3 3)"""
import sys, cmath
import numpy as np

if __name__ == '__main__':
    p, q, n = (int(v) for v in sys.argv[1:4]); N = p ** n * q
    half = N // 2; lo_n, hi_n = half, N - half
    def table(d, bits, shift):
        z = cmath.exp(2j * cmath.pi / d); m = np.arange(1 << bits); t = np.zeros(1 << bits, complex)
        for b in range(bits): t += ((m >> b) & 1) * z ** (b + shift)
        return t
    ds = {('E', l): p ** l for l in range(1, n + 1)}; ds.update({('F', l): p ** l * q for l in range(0, n + 1)})
    lo = {k: table(d, lo_n, 0) for k, d in ds.items()}; hi = {k: table(d, hi_n, lo_n) for k, d in ds.items()}
    pc_lo = np.array([bin(m).count('1') for m in range(1 << lo_n)])
    stats = dict(base=0, base_broken=0, plus=0, plus_broken=0, loose=0, loose_broken=0, beyond=0, a0inE=0); best = {}; loose_pat = {}; plus_pat = {}
    for h in range(1 << hi_n):
        size = pc_lo + bin(h).count('1')
        Z = {k: np.abs(lo[k] + hi[k][h]) < 1e-9 for k in ds}          # a primitive root of each order is enough: the others are its conjugates over Q
        ok = Z[('F', 0)] & (size > 0)
        if not ok.any(): continue
        idx = np.nonzero(ok)[0]
        E = np.array([Z[('E', l)][idx] for l in range(1, n + 1)]); F = np.array([Z[('F', l)][idx] for l in range(1, n + 1)]); sz = size[idx]
        for j in range(len(idx)):
            Ej, Fj = E[:, j], F[:, j]
            miss = [l for l in range(1, n + 1) if not Fj[l - 1]]
            if not miss: continue
            a0 = miss[0]; e = int(Ej.sum()); beyond = [l for l in range(a0 + 1, n + 1) if Fj[l - 1] and not Ej[l - 1]]; k = len(beyond)
            stats['base'] += 1; stats['base_broken'] += sz[j] < q * p ** (e + k)
            plus = bool(beyond) and not any(Ej[l - 1] for l in range(1, a0)) and (
                not Ej[a0 - 1] or (p == 2 and all((not Ej[b - 1]) or Fj[b - 1] for b in range(a0 + 1, beyond[0]))))
            bound = q * p ** e * (p ** k + 1) if plus else q * p ** (e + k)
            if plus: stats['plus'] += 1; stats['plus_broken'] += sz[j] < bound
            if beyond:                          # how much of the second statement do these sets reach at all?
                stats['beyond'] += 1; stats['a0inE'] += bool(Ej[a0 - 1])
                key2 = ('E=%s F=[0]+%s' % ([l + 1 for l in range(n) if Ej[l]], [l + 1 for l in range(n) if Fj[l]]))
                (plus_pat if plus else loose_pat)[key2] = (plus_pat if plus else loose_pat).get(key2, 0) + 1
            if beyond and not plus:            # a control: the plus bound WITHOUT its three further hypotheses ought to break
                stats['loose'] += 1; stats['loose_broken'] += sz[j] < q * p ** e * (p ** k + 1)
            key = (tuple(Ej), tuple(Fj)); cur = best.get(key)
            if cur is None or sz[j] < cur[0]: best[key] = (int(sz[j]), bound, plus)
    print(f"   reach: subsets with some level beyond a0 in F and not in E: {stats['beyond']}; of those with a0 in E (where the third hypothesis of plus would decide): {stats['a0inE']}")
    print(f"   patterns where plus applies: {plus_pat}; patterns of the control sets: {loose_pat}")
    met = sum(v[0] == v[1] for v in best.values())
    print(f"Z_{N} (p={p}, q={q}, n={n}): {1 << N} subsets; base applies to {stats['base']}, broken by {stats['base_broken']}; plus applies to {stats['plus']}, broken by {stats['plus_broken']}")
    print(f"   control: where some level lies beyond a0 in F and not in E but the further hypotheses of plus fail ({stats['loose']} subsets), the plus bound is broken by {stats['loose_broken']}")
    print(f"   patterns met among these subsets: {len(best)}; the bound (plus where it applies, else base) is the least size of a SET in {met} of them; "
          f"patterns where plus applies: {sum(v[2] for v in best.values())}, bound met in {sum(v[2] and v[0] == v[1] for v in best.values())}")
    over = sorted((v[0] - v[1], k) for k, v in best.items() if v[0] > v[1])[-3:]
    for d, k in over: print(f"   a set needs {d} more than the bound for E={[l + 1 for l, x in enumerate(k[0]) if x]}, F=[0]+{[l + 1 for l, x in enumerate(k[1]) if x]}")

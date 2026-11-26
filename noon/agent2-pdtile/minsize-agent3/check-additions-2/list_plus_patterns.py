"""Which patterns do the subsets have to which balanced_plus_zmod applies, and the control subsets?
Uses recount_exact.py's exact zero test; prints, for each such pattern, E, F, a0, whether a0 is in E
(then h34 holds only through its 'p = 2' branch), the number of subsets and their least size.
usage: python -I list_plus_patterns.py p q n"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I leaves the script's folder out
import recount_exact as R

def main():
    p, q, n = (int(v) for v in sys.argv[1:4]); N = p ** n * q
    lo_n = N // 2; hi_n = N - lo_n
    keys = [('E', l) for l in range(1, n + 1)] + [('F', l) for l in range(0, n + 1)]
    ds = {('E', l): p ** l for l in range(1, n + 1)}; ds.update({('F', l): p ** l * q for l in range(0, n + 1)})
    lo, hi = {}, {}
    for k in keys:
        rows = R.rem_rows(N, ds[k])
        for tab, bits, shift in ((lo, lo_n, 0), (hi, hi_n, lo_n)):
            t = np.zeros((1 << bits, rows.shape[1]), dtype=np.int32); m = np.arange(1 << bits)
            for b in range(bits): t += (((m >> b) & 1)[:, None] * rows[shift + b][None, :]).astype(np.int32)
            tab[k] = t
    pc_lo = np.array([bin(m).count('1') for m in range(1 << lo_n)], dtype=np.int64)
    ncode = 1 << len(keys); counts = np.zeros(ncode * (N + 1), dtype=np.int64)
    for h in range(1 << hi_n):
        code = np.zeros(1 << lo_n, dtype=np.int64)
        for i, k in enumerate(keys):
            code |= ((lo[k] + hi[k][h][None, :]) == 0).all(axis=1).astype(np.int64) << i
        counts += np.bincount(code * (N + 1) + pc_lo + bin(h).count('1'), minlength=ncode * (N + 1))
    counts = counts.reshape(ncode, N + 1)
    print(f"Z_{N} (p={p}, q={q}, n={n})")
    for code in range(ncode):
        if counts[code].sum() == 0: continue
        E = {k[1] for i, k in enumerate(keys) if k[0] == 'E' and (code >> i) & 1}
        Fall = {k[1] for i, k in enumerate(keys) if k[0] == 'F' and (code >> i) & 1}
        if 0 not in Fall: continue
        F = Fall - {0}; miss = [l for l in range(1, n + 1) if l not in F]
        if not miss: continue
        a0 = miss[0]; plus, beyond = R.lean_plus_hyps(p, n, E, F, a0); hold, kp = R.note_clauses(p, n, E, F, a0)
        if kp == 0: continue
        sizes = [s for s, c in enumerate(counts[code]) if c]; e = len(E)
        kind = "plus applies" if plus else f"control (clauses {sorted(hold)} hold)"
        print(f"   E={sorted(E)} F={sorted(Fall)} a0={a0} a0 in E: {a0 in E}; k'={kp}; {kind}; subsets: {int(counts[code].sum())}; "
              f"least size {min(sizes)}; q p^(e+k') = {q * p ** (e + kp)}, q p^e (p^k' + 1) = {q * p ** e * (p ** kp + 1)}")
main()

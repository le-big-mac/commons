"""The Corollary of the paper's new section, tested by census.  M = p^n q, s odd (prime or composite).  For every set D of divisors > 1 of M:
   {sizes <= S of nonempty multisets on Z_{Ms} whose pattern among ALL divisors > 1 of Ms is exactly D}
   == {sizes <= S of nonempty multisets on Z_M with pattern exactly D},
and the least of them is Theorem 1's value (where that is <= S; where it is larger, both sets must be empty up to S).
Census: every multiset with at most S elements that contains 0 (a translate of any multiset contains 0 and has the same pattern and size).
Nothing is stored but, for each pattern, the set of sizes seen.   usage: python -I t3_corollary.py [small]"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift')
import itertools, time
import numpy as np
from cyc import divisors, tables
from thm import theorem_value, pattern_to_EF
def census(m, S, batch=20000):
    """{frozenset pattern (divisors > 1 of m): set of sizes <= S}; returns also the number of multisets gone through"""
    T = {d: t.astype(np.int32) for d, t in tables(m).items() if d > 1}; ds = sorted(T); out = {}; count = 0
    for s in range(1, S + 1):
        it = itertools.combinations_with_replacement(range(m), s - 1)
        while True:
            chunk = list(itertools.islice(it, batch))
            if not chunk: break
            C = np.array(chunk, dtype=np.int64).reshape(len(chunk), s - 1); count += len(chunk)
            code = np.zeros(len(chunk), dtype=np.int64)
            for i, d in enumerate(ds):
                v = T[d][0][None, :] + (T[d][C].sum(axis=1) if s > 1 else 0)
                code |= (~v.any(axis=1)).astype(np.int64) << i
            for c in np.unique(code):
                out.setdefault(frozenset(d for i, d in enumerate(ds) if c >> i & 1), set()).add(s)
    return out, count
CASES = [  # (p, q, n, s, S)
    (3, 2, 0, 9, 7), (2, 3, 0, 9, 6), (3, 2, 0, 15, 6), (2, 3, 0, 15, 6), (2, 5, 0, 9, 6), (2, 3, 0, 25, 5),
    (2, 3, 1, 3, 7), (3, 2, 1, 3, 7), (2, 3, 1, 5, 6), (3, 2, 1, 5, 6), (2, 5, 1, 3, 6), (5, 2, 1, 3, 6),
    (2, 3, 1, 9, 6), (3, 2, 1, 9, 6), (2, 3, 1, 15, 5), (3, 2, 1, 15, 5), (2, 5, 1, 9, 5), (5, 2, 1, 9, 5), (3, 5, 1, 3, 6), (5, 3, 1, 3, 6),
    (3, 5, 1, 5, 5), (3, 5, 1, 9, 4), (2, 3, 1, 25, 4), (2, 5, 1, 15, 4), (2, 3, 1, 7, 6), (2, 7, 1, 3, 6),
    (2, 3, 2, 3, 6), (3, 2, 2, 3, 5), (2, 3, 2, 5, 5), (2, 5, 2, 3, 5), (2, 3, 2, 9, 5), (5, 2, 2, 3, 4), (3, 5, 2, 3, 4), (2, 3, 3, 3, 5), (3, 2, 2, 9, 4), (2, 3, 2, 15, 4),
]
if len(sys.argv) > 1 and sys.argv[1] == 'small': CASES = [(3, 2, 0, 9, 5), (2, 3, 1, 3, 5), (2, 3, 1, 9, 4)]
small_cache = {}; big_cache = {}; tot_multisets = 0; tot_patterns = 0; mism = []; thm_bad = []; tot_thm_checked = 0
t00 = time.time()
for p, q, n, s, S in CASES:
    M = p ** n * q; big = M * s; t0 = time.time()
    if (M, S) not in small_cache: small_cache[(M, S)] = census(M, S)[0]
    sm = small_cache[(M, S)]
    if (big, S) not in big_cache: big_cache[(big, S)] = census(big, S); tot_multisets += big_cache[(big, S)][1]
    bg, cnt = big_cache[(big, S)]
    dM = [d for d in divisors(M) if d > 1]; nbad = 0; nthm = 0; nonempty = 0
    for k in range(len(dM) + 1):
        for D in itertools.combinations(dM, k):
            D = frozenset(D); a, b = sm.get(D, set()), bg.get(D, set()); tot_patterns += 1
            if a != b: nbad += 1; mism.append((p, q, n, s, sorted(D), sorted(a), sorted(b)))
            E, F, bal = pattern_to_EF(D, p, q, n); tv = theorem_value(p, q, n, E, F, bal)
            if tv <= S:
                nthm += 1; tot_thm_checked += 1
                if not (b and min(b) == tv and a and min(a) == tv): thm_bad.append((p, q, n, s, sorted(D), tv, sorted(a), sorted(b)))
            elif a or b: thm_bad.append((p, q, n, s, sorted(D), tv, sorted(a), sorted(b)))
            nonempty += bool(b)
    print(f'p = {p}, q = {q}, n = {n}, M = {M}, s = {s}, Z_{big}, sizes <= {S}: {cnt} multisets on Z_{big}; {2 ** len(dM)} patterns D; size sets differ for {nbad}; '
          f'nonempty on Z_{big} for {nonempty}; least size = Theorem 1 checked for {nthm} (value <= {S}); {time.time() - t0:.0f} s', flush=True)
print(f'TOTAL: {len(CASES)} cases, {tot_multisets} multisets on the larger groups (each group and bound counted once), {tot_patterns} pattern comparisons; size sets differ: {len(mism)}; '
      f'least size against Theorem 1 checked in {tot_thm_checked} instances, disagreements (or a member below the theorem\'s value): {len(thm_bad)}; {time.time() - t00:.0f} s')
for x in mism[:10]: print('  MISMATCH', x)
for x in thm_bad[:10]: print('  THEOREM', x)

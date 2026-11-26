"""The n = 1 values after Theorem 1 and the worked example of Remark 2 (balanced, n = 3, F = {3}),
each expression typed from the paper's text, against the least sizes found by dp.c.
Also (for information) the constructions (IV), (V) used where an earlier case would apply."""
import sys, itertools
from t3_theorem import read_dp
from t6_constructions import balanced
from lib import root_pattern, subsets

def least(table, j, E, F, bal):
    s = [x for x in table.get((j, frozenset(E), frozenset(F), bal), []) if x > 0]
    return min(s) if s else None

bad = tot = 0
for (p, q, n, B) in [(2, 3, 4, 72), (3, 2, 4, 162), (5, 2, 3, 250), (2, 5, 3, 30), (5, 3, 2, 75), (3, 5, 2, 20), (7, 2, 2, 98)]:
    t = read_dp(p, q, n, B)
    n1 = {((), (), False): 1, ((1,), (), False): p, ((), (1,), False): p + q, ((1,), (1,), False): p,
          ((), (), True): q, ((1,), (), True): p * q, ((), (1,), True): q, ((1,), (1,), True): p * q}
    for (E, F, bal), v in n1.items():
        if v <= B:
            tot += 1; bad += least(t, 1, E, F, bal) != v
    if n >= 3:
        ex = {(): q * (p + 1), (1,): q * p * p if p >= 3 else 6 * q, (2,): q * p * (p + 1), (1, 2): q * p ** 3,
              (3,): q * p, (1, 3): q * p ** 2, (2, 3): q * p ** 2, (1, 2, 3): q * p ** 3}
        for E, v in ex.items():
            if v <= B:
                tot += 1
                got = least(t, 3, E, (3,), True)
                bad += got != v
                if got != v: print("   differs", p, q, E, v, got)
print(f"n = 1 values and Remark 2: {tot} values compared with exhaustive search, {bad} differ")

# information: (IV) and (V) used whenever their own conditions hold, whatever the earlier cases say
st = {}
for (p, q) in [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5)]:
    for n in range(1, 5):
        full = set(range(1, n + 1))
        for E in subsets(n):
            for F in subsets(n):
                E_, F_ = set(E), set(F)
                if F_ == full: continue
                a0 = min(full - F_); G = {a for a in F_ - E_ if a > a0}
                if not G: continue
                conds = {"IV": a0 in E_ and p >= 3,
                         "V": a0 in E_ and any(a0 < a < min(G) for a in E_ - F_),
                         "III": any(a < a0 for a in E_)}
                for case, ok in conds.items():
                    if not ok: continue
                    A, _ = balanced(p, q, n, E_, F_, force=case)
                    good = root_pattern(A, p, n) == (E, F, True) and int(A.sum()) == q * p ** (len(E_) + len(G))
                    c = st.setdefault(case, [0, 0]); c[0] += 1; c[1] += (not good)
print("constructions used wherever their own condition holds, regardless of order (built, wrong):", st)

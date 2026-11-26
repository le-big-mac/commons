"""Referee: Proposition 11 (section 7) by enumeration: for every pattern with 0 in F, F not everything,
x = 0 iff k' = 0 or the pattern has a host level (b in E, b < g1, and: b < a0; or b = a0 and p >= 3;
or b > a0, b not in F, a0 in E).  Also: the first applicable construction case of section 6.3 against x."""
import itertools
from ref_common import rule
from ref_construct import first_case
tot = bad = 0
for p in (2, 3, 5):
    for n in range(1, 8):
        lv = list(range(1, n + 1))
        for Et in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
            for Ft in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
                E = set(Et); F = set(Ft) | {0}
                val, x, a0, kp = rule(p, 7, n, E, F)
                if x is None:
                    continue
                tot += 1
                host = False
                if kp >= 1:
                    g1 = min(a for a in range(a0 + 1, n + 1) if a in F and a not in E)
                    for b in E:
                        if b < g1 and (b < a0 or (b == a0 and p >= 3) or (b > a0 and b not in F and a0 in E)):
                            host = True
                if (x == 0) != (kp == 0 or host):
                    bad += 1
                fc = first_case(p, n, E, F)
                if (fc == "II") != (x == 1):
                    bad += 1
print(f"Proposition 11 and 'case (II) iff x = 1': {tot} patterns (p = 2, 3, 5; n = 1..7), disagreements {bad}")

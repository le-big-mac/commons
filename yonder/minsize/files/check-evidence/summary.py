# Totals for the report: per clock, patterns settled (plain enumeration + per-pattern search), by case.
import re, math
from itertools import combinations
from polylib import divisors
from rules import page_rule, theorem1, read_enum, presentations
per = {}
for L in open('run_perpat.out'):
    m = re.match(r"clock (\d+) pattern \[(.*?)\]: least number (\d+)", L)
    if m: per[(int(m.group(1)), frozenset(int(x) for x in m.group(2).split(',')))] = int(m.group(3))
for M, S in [(6, 6), (10, 10), (12, 18), (18, 18), (20, 20), (24, 18)]:
    best, nodes = read_enum(M, S)
    ds = [d for d in divisors(M) if d > 1]
    pats = [frozenset(c) for r in range(len(ds) + 1) for c in combinations(ds, r)]
    for (p, n, q) in presentations(M):
        c1 = c1ok = c2 = c2ok = k0 = k0ok = x1 = open_ = 0
        for P in pats:
            least = best[P][0] if P in best else per.get((M, P))
            allowed = page_rule(M, p, n, q, P)
            if least is None: open_ += 1; continue
            if q not in P:
                c1 += 1; c1ok += (allowed == {least})
            else:
                c2 += 1; c2ok += (least in allowed)
                if len(allowed) == 1: k0 += 1; k0ok += (allowed == {least})
                elif least == max(allowed): x1 += 1
            assert least == theorem1(M, p, n, q, P)
        print(f"clock {M} as {p}^{n}*{q}: patterns {len(pats)}; settled {c1 + c2}, not settled {open_}; first case {c1ok} of {c1} equal to the page's value; "
              f"second case {c2ok} of {c2} one of the page's values (page gives a single value, x = 0, in {k0}: right in {k0ok}; x = 1 needed in {x1}); every settled value is Theorem 1's")

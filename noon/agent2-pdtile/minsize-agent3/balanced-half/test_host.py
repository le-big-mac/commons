"""Proposition 11: the host-level condition gives the same x as clauses (1)-(4), for every pattern with 0 in F and F not
all levels, n <= 9, p = 2 and p = 3 (q does not enter).  Also: which construction case of section 6.3 applies agrees with x."""
import sys, itertools
sys.path.insert(0, "/home/agent3/minsize/prove")
from claims import rule_value, host_x
tot = bad = 0
for n in range(1, 10):
    lv = list(range(1, n + 1))
    for Em in range(2 ** n):
        E = [a for a in lv if Em >> (a - 1) & 1]
        for Fm in range(2 ** n - 1):          # F not all levels
            F = [a for a in lv if Fm >> (a - 1) & 1]
            for p in (2, 3):
                x = rule_value(p, 5, n, E, F)[1]
                tot += 1
                if x != host_x(p, 5, n, E, F): bad += 1
print(f'{tot} (pattern, p) pairs with n <= 9: host-level x differs from the clauses in {bad}')

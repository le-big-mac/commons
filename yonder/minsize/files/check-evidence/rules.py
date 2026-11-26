# Shared functions. Used by compare_rule.py, which compares (1) the least number of marks found by exhaustive enumeration (enum.c) with
# (2) the rule as the PAGE words it (section "The answer"), programmed from the page's words only, and
# (3) Theorem 1 of the paper with its four clauses (programmed separately, from the paper).
import sys, glob, re, math
from itertools import combinations
from polylib import divisors, pattern_exact

def read_enum(M, S):
    best = {}; nodes = 0
    for fn in sorted(glob.glob(f"enum_{M}_{S}.job*.out")):
        for L in open(fn):
            if L.startswith("M "):
                nodes += int(L.split()[-1]); continue
            m = re.match(r"pat(.*) \| size (\d+) \| marks (.*)", L)
            pat = frozenset(int(x) for x in m.group(1).split()); size = int(m.group(2))
            marks = [int(x) for x in m.group(3).split()]
            if pat not in best or size < best[pat][0]:
                best[pat] = (size, marks)
    return best, nodes

def page_rule(M, p, n, q, pat):
    """The page's words. Returns the set of values the page allows."""
    assert M == p**n * q
    powers = [p**a for a in range(1, n + 1)]            # "the powers p, p^2, ..., p^n"
    e = sum(1 for P in powers if P in pat)              # "the number of powers of p in the pattern"
    short = [P for P in powers if (P * q in pat) and (P not in pat)]   # "to balance at p^a q but not at p^a itself"
    if q not in pat:                                    # "If the marks are not to balance at q"
        k = len(short)
        return {p**e} if k == 0 else {p**e * (p**k + q)}
    # "If they are to balance at q, find the smallest power p^a for which the marks are not to balance at p^a q"
    missing = [P for P in powers if P * q not in pat]
    if missing:
        P0 = min(missing)
        kp = sum(1 for P in short if P > P0)            # "the number of short powers larger than it"
    else:
        kp = 0                                          # "(k' = 0 if there is no such power)", read generously
    if kp == 0:
        return {q * p**e * (p**kp + 0)}                 # "When k' = 0, x is 0."
    return {q * p**e * (p**kp + 0), q * p**e * (p**kp + 1)}   # "x is 0 or 1"

def theorem1(M, p, n, q, pat):
    """Theorem 1 of the paper, clauses (1)-(4)."""
    E = {a for a in range(1, n + 1) if p**a in pat}
    F = {a for a in range(1, n + 1) if p**a * q in pat}
    e = len(E)
    if q not in pat:
        return p**e if F <= E else p**e * (p**len(F - E) + q)
    if F == set(range(1, n + 1)):
        return q * p**e
    a0 = min(a for a in range(1, n + 1) if a not in F)
    G = {a for a in F - E if a > a0}; kp = len(G)
    c1 = kp == 0
    c2 = any(a < a0 for a in E)
    c3 = a0 in E and p >= 3
    c4 = kp >= 1 and a0 in E and p == 2 and any(a0 < b < min(G) for b in E - F)
    x = 0 if (c1 or c2 or c3 or c4) else 1
    return q * p**e * (p**kp + x)

def presentations(M):
    out = []
    for q in range(2, M + 1):
        if M % q or any(q % r == 0 for r in range(2, q)): continue
        m = M // q
        if m == 1: out.append((None, 0, q)); continue
        ps = [r for r in range(2, m + 1) if m % r == 0 and all(r % s for s in range(2, r))]
        if len(ps) == 1 and ps[0] != q:
            p = ps[0]; n = round(math.log(m, p))
            if p**n == m: out.append((p, n, q))
    return out


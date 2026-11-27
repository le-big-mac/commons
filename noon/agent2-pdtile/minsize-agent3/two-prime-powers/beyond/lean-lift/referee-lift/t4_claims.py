"""Particular claims of the three texts, recomputed.   usage: python -I t4_claims.py"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift')
import itertools, json
from cyc import divisors, pattern
from thm import theorem_value, pattern_to_EF
print('== C: the clock of 36 hours, marks 0, 6, 1, 5, 9')
print('   pattern on Z_12:', sorted(pattern([0, 6, 1, 5, 9], 12)), ' pattern on Z_36:', sorted(pattern([0, 6, 1, 5, 9], 36)))
print('   pair 0, 6 on Z_12:', sorted(pattern([0, 6], 12)), ' triangle 1, 5, 9 on Z_12:', sorted(pattern([1, 5, 9], 12)))
# no four marks (or fewer) on Z_36 balance at 12 and at no other divisor of 36 (every multiset; translation: contains 0)
sizes = set()
for s in range(1, 6):
    for c in itertools.combinations_with_replacement(range(36), s - 1):
        if pattern([0] + list(c), 36) == frozenset({12}): sizes.add(s)
print('   sizes <= 5 of multisets on Z_36 with pattern exactly {12}:', sorted(sizes), '; Theorem 1 for p = 2, q = 3, n = 2, pattern {12}:',
      theorem_value(2, 3, 2, *pattern_to_EF({12}, 2, 3, 2)))
rows = json.load(open('/home/agent3/pq2/note/rows-36.json'))
by = {frozenset(r['D']): r for r in rows}
print('   rows-36.json, pattern {12}:', by[frozenset({12})])
print('== C: the pattern {12, 18, 36} on Z_36')
M = 36; D = {12, 18, 36}; dv = [d for d in divisors(M) if d > 1]
upset = all((m in D) for d in D for m in dv if m % d == 0)
out = [c for c in divisors(M) if c not in D]; corners = [c for c in out if not any(o != c and o % c == 0 for o in out)]
print('   up-set:', upset, '; corners:', corners, '; ring sizes M/c:', [M // c for c in corners], '; sum:', sum(M // c for c in corners))
print('   {12} alone an up-set:', all((m in {12}) for d in {12} for m in dv if m % d == 0))
print('   rows-36.json, pattern {12, 18, 36}:', by[frozenset(D)])
# one coset for each corner, wherever put: pattern exactly D?
bad = 0; tried = 0
for x1 in range(4):
    for x2 in range(6):
        for x3 in range(9):
            A = [(x1 + 4 * j) % 36 for j in range(9)] + [(x2 + 6 * j) % 36 for j in range(6)] + [(x3 + 9 * j) % 36 for j in range(4)]
            tried += 1; bad += pattern(A, 36) != frozenset(D)
print(f'   one ring of 9, one of 6, one of 4 marks, every placing ({tried}): pattern other than {{12, 18, 36}} in {bad}')
allowed = [M // c for c in divisors(M) if not any(d for d in D if c % d == 0)]
print('   sizes of ALL rings (cosets of subgroups) that balance at 12, 18 and 36:', sorted(allowed))
print('== B: the 256 patterns of Z_{p^2 q^2}, by exponent pairs; counts')
def counts(p, q):
    M = p * p * q * q; dv = [d for d in divisors(M) if d > 1]; assert len(dv) == 8
    ups = 0; in_p2q = set(); in_pq2 = set(); allp = []
    for k in range(9):
        for D in itertools.combinations(dv, k):
            D = frozenset(D); allp.append(D)
            if all((m in D) for d in D for m in dv if m % d == 0): ups += 1
            if all((p * p * q) % d == 0 for d in D): in_p2q.add(D)
            if all((p * q * q) % d == 0 for d in D): in_pq2.add(D)
    both = in_p2q & in_pq2; uni = in_p2q | in_pq2
    nonup = {D for D in uni if D}                     # the empty pattern is the only up-set among them
    return M, len(allp), ups, len(in_p2q), len(in_pq2), len(both), len(uni), len(nonup), in_p2q, in_pq2
for p, q in ((2, 3), (2, 5), (3, 5)):
    M, n_all, ups, a, b, both, uni, nonup, in_p2q, in_pq2 = counts(p, q)
    print(f'   Z_{M} (p = {p}, q = {q}): {n_all} patterns, {ups} up-sets; inside {p*p*q}: {a}; inside {p*q*q}: {b}; inside both: {both}; union: {uni}; '
          f'union without the empty pattern (the "55"): {nonup}')
    # which of the 55 does the lifted theorem reach?  inside p^2 q needs the lift along q (q odd); inside p q^2 needs the lift along p (p odd)
    reach = set()
    if q % 2: reach |= {D for D in in_p2q if D}
    if p % 2: reach |= {D for D in in_pq2 if D}
    rest = ({D for D in in_p2q | in_pq2 if D}) - reach
    print(f'      reached by a lift along an odd prime: {len(reach)}; not reached: {len(rest)}'
          + (f' (these are the patterns inside {p*q*q} that are not inside {p*p*q}: {len({D for D in in_pq2 if D} - in_p2q)}; '
             f'inside {p*q*q} altogether, the empty one left out: {len({D for D in in_pq2 if D})})' if rest else ''))
print('== B / C: the table of section 3 against status.json or the bounds files, if present')
import os
for name in ('status.json',):
    pth = '/home/agent3/pq2/rule/' + name
    print('  ', pth, 'exists:', os.path.exists(pth))

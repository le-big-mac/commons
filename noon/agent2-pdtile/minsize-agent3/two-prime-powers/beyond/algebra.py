"""An upper bound from three operations, set beside the tables.
Atoms: for c | N | M, a coset of cZ_N lifted to Z_M with the lifts in general position: pattern {d | N : d does not divide c}, N/c elements.
  (x) convolution:  pattern(A1 * A2) = D1 ∪ D2 exactly (Φ_d is prime), size |A1|·|A2|
  (+) sum:          pattern(A1 + a translate of A2) ⊇ D1 ∩ D2, and = D1 ∩ D2 if no divisor outside D1 ∪ D2 appears (assumed here: general position)
  (L) reduce mod N and lift again in general position: pattern D ∩ {divisors of N}, same size (assumed: general position)
U(D) = the least cost of an expression in the atoms with value exactly D.  The table's least size must be <= U(D) if the two
assumptions of general position are harmless; where U(D) < least size, an assumption has failed.   usage: algebra.py"""
import json, itertools, sys
sys.path.insert(0, '/home/agent3/pq2/rule')
from lowerbound import LB
def closure(p, q):
    M = p * p * q * q; divs = [d for d in range(2, M + 1) if M % d == 0]; idx = {d: i for i, d in enumerate(divs)}
    full = (1 << len(divs)) - 1
    def mask(S): return sum(1 << idx[d] for d in S)
    INF = float('inf'); U = [INF] * (full + 1); how = [None] * (full + 1)
    alld = [1] + divs
    for N in alld:
        for c in alld:
            if N % c == 0 and c != N or (N == 1 and c == 1):
                m = mask([d for d in divs if N % d == 0 and c % d != 0])
                if N // c < U[m]: U[m] = N // c; how[m] = f'coset of {c}Z_{N}'
    low = [mask([d for d in divs if N % d == 0]) for N in alld]
    changed = True
    while changed:
        changed = False
        known = [m for m in range(full + 1) if U[m] < INF]
        for a in known:
            for N, lm in zip(alld, low):
                if U[a] < U[a & lm]: U[a & lm] = U[a]; how[a & lm] = ('L', a, N); changed = True
        for a, b in itertools.combinations_with_replacement(known, 2):
            if U[a] * U[b] < U[a | b]: U[a | b] = U[a] * U[b]; how[a | b] = ('x', a, b); changed = True
            if U[a] + U[b] < U[a & b]: U[a & b] = U[a] + U[b]; how[a & b] = ('+', a, b); changed = True
    return divs, mask, U, how
def expr(m, how, divs, depth=0):
    h = how[m]
    if isinstance(h, str): return h
    if h[0] == 'L': return f'[{expr(h[1], how, divs)}] mod {h[2]}'
    return '(' + expr(h[1], how, divs) + (' * ' if h[0] == 'x' else ' + ') + expr(h[2], how, divs) + ')'
if __name__ == '__main__':
    for M, p, q in ((36, 2, 3), (100, 2, 5)):
        divs, mask, U, how = closure(p, q)
        rows = json.load(open(f'/home/agent3/pq2/note/rows-{M}.json'))
        eq = gt = lt = inf = und_eq = 0; settled = 0; ex = []; bad = []; sandwich = 0
        for r in rows:
            u = U[mask(r['D'])]; lb, _ = LB(r['D'], p, q)
            if lb == u: sandwich += 1
            if u == float('inf'): inf += 1; continue
            if r['by']:
                if u == r['size']: eq += 1
                elif u > r['size']: gt += 1; ex.append((r['D'], r['size'], u, lb))
                else: lt += 1; bad.append((r['D'], r['size'], u, expr(mask(r['D']), how, divs)))
            else:
                if u == r['size']: und_eq += 1
                if u < r['size']: bad.append((r['D'], r['size'], u, 'undecided row: a smaller multiset, if the expression is honest'))
        print(f'Z_{M}: patterns with an expression: {len(rows) - inf} of {len(rows)}; decided patterns with U = least: {eq}; U > least: {gt}; U < least (an assumption failed): {lt}; undecided with U = smallest found: {und_eq}')
        print(f'   patterns where the lower bound of lowerbound.py equals U (least size settled by the two bounds alone): {sandwich}')
        print('   U < least:', bad[:12])
        print('   U > least, first few (pattern, least, U, lower bound):', ex[:40])

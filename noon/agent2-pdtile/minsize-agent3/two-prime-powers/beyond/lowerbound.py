"""How much of the tables do the known theorems explain?  For a pattern D on Z_M, M = p^2 q^2:
  (r) restriction: A mod N has exactly the pattern D ∩ {divisors of N}; for N = p^2 q and N = p q^2 the theorem for Z_{p^n q} gives
      the least size of such a multiset, a lower bound for |A|;
  (c) Corollary P: the corner sum of the largest up-set inside D;
  (d) divisibility: p^a q^b divides |A|, a and b the numbers of pure powers of p and of q in D.
LB(D) = the least multiple of p^a q^b that is >= max(r, c).   Compared with the least sizes of the tables.   usage: lowerbound.py"""
import json, collections
def rule(p, q, n, E, F):
    e = len(E)
    if 0 not in F:
        k = len([a for a in F if a not in E]); return p ** e * (p ** k + q) if k else p ** e
    if set(F) == set(range(n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F); G = sorted(a for a in F if a > a0 and a not in E)
    x = 0 if (not G or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or (a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, G[0])))) else 1
    return q * p ** e * (p ** len(G) + x)
def LB(D, p, q):
    D = set(D); M = p * p * q * q
    r = []
    for P, Q in ((p, q), (q, p)):
        N = P * P * Q; DN = {d for d in D if N % d == 0}
        r.append(rule(P, Q, 2, [a for a in (1, 2) if P ** a in DN], ([0] if Q in DN else []) + [a for a in (1, 2) if P ** a * Q in DN]))
    divs = [d for d in range(1, M + 1) if M % d == 0]
    U = {d for d in D if all(e in D for e in divs if e % d == 0)}; comp = [c for c in divs if c not in U]
    c = sum(M // x for x in comp if not any(e != x and e % x == 0 for e in comp))
    g = p ** len(D & {p, p * p}) * q ** len(D & {q, q * q})
    m = max(r + [c]); return -(-m // g) * g, dict(restr=r, corP=c, div=g)
if __name__ == '__main__':
    for M, p, q in ((36, 2, 3), (100, 2, 5)):
        rows = json.load(open(f'/home/agent3/pq2/note/rows-{M}.json'))
        tight = slack = und_t = und_s = 0; ex = []; below = []
        for r in rows:
            lb, parts = LB(r['D'], p, q)
            if r['size'] < lb: below.append((r['D'], r['size'], lb))
            if r['by']:
                if r['size'] == lb: tight += 1
                else: slack += 1; ex.append((r['D'], r['size'], lb, parts))
            else:
                if r['size'] == lb: und_t += 1
                else: und_s += 1
        print(f'Z_{M}: decided patterns where the bound is the least size: {tight}; where it is smaller: {slack}; undecided patterns whose smallest found equals the bound (so decided by it): {und_t}; others undecided: {und_s}; found below the bound (would be an error): {below}')
        print('   ratios least/bound where not tight:', sorted(collections.Counter(round(e[1] / e[2], 3) for e in ex).items()))
        for e in ex[:60]: print('    ', e[0], 'least', e[1], 'bound', e[2], e[3])

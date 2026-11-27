"""cap-witnesses.jsonl checked a second way: sympy's cyclotomic polynomials and sympy's polynomial remainder (nothing of
cyc.py).  For each line: m elements, every multiplicity <= cap, and Phi_d | mask exactly for the d of the pattern, among
all divisors d > 1 of p^n q.   usage: check_witnesses.py"""
import json, collections
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); CY = {}
def pat(mult, M):
    A = Poly(sum(w * X**x for x, w in mult.items()), X, domain=ZZ); out = set()
    for d in range(2, M + 1):
        if M % d == 0:
            if d not in CY: CY[d] = Poly(cyclotomic_poly(d, X), X, domain=ZZ)
            if A.rem(CY[d]).is_zero: out.add(d)
    return out
tot = ok = 0; capmax = collections.Counter(); per = collections.Counter()
for line in open('cap-witnesses.jsonl'):
    o = json.loads(line); p, q, n = o['p'], o['q'], o['n']; M = p ** n * q
    mult = {int(x): w for x, w in o['multiset'].items()}
    D = set([p ** a for a in o['E']] + [p ** a * q for a in o['F']] + ([q] if o['balanced'] else []))
    good = sum(mult.values()) == o['m'] and max(mult.values()) <= (3 if p == 2 else 2) and pat(mult, M) == D
    tot += 1; ok += good; per[M] += good
print(f'{tot} lines; right size, multiplicities <= 3 (p = 2) or <= 2 (p odd), and exactly the pattern by sympy division: {ok}')
print('by group:', dict(sorted(per.items())))

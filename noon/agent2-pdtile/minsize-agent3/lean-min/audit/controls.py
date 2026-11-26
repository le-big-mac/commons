"""What the enumeration could have caught: wrong variants of the rule, each compared with the least sizes
found by enumeration (outB/*.json; in these groups every pattern's least size was found and equals Lean's
value).  For each variant: the number of patterns on which it differs from the enumerated least size, and
the smallest group where it does."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def rule(p, q, n, bal, E, F, variant=None):
    e = len(E)
    levels = list(range(1, n + 1))
    if not bal:
        k = len([a for a in F if a not in E])
        if variant == 'U: |F| in place of |F minus E|':
            k = len(F)
        if all(a in E for a in F):
            return p ** e
        if variant == 'U: p^|E u F| + q p^|E| replaced by p^|E u F| alone':
            return p ** (e + k)
        return p ** e * (p ** k + q)
    if all(a in F for a in levels):
        return q * p ** e
    a0 = min(a for a in levels if a not in F)
    if variant == 'B: a0 = first level in neither E nor F':
        cand = [a for a in levels if a not in F and a not in E]
        a0 = min(cand) if cand else a0
    deeper = sorted(a for a in F if a not in E and a > a0)
    if variant == "B: k' counts every level of F minus E, not only those beyond a0":
        deeper = sorted(a for a in F if a not in E)
    kp = len(deeper)
    c1 = (kp == 0)
    c2 = any(a in E for a in range(1, a0))
    c3 = (a0 in E) and p >= 3
    c4 = False
    if (a0 in E) and p == 2 and deeper:
        first = deeper[0]
        c4 = any((b in E) and (b not in F) for b in range(a0 + 1, first))
        if variant == 'B: clause (4) with b in E only (b may be in F)':
            c4 = any((b in E) for b in range(a0 + 1, first))
        if variant == 'B: clause (4) with b = a0 allowed (so clause (3) for p = 2 as well)':
            c4 = any((b in E) and (b not in F) for b in range(a0, first))
        if variant == 'B: clause (4) between a0 and SOME level of F minus E beyond a0':
            c4 = any((b in E) and (b not in F) for b in range(a0 + 1, deeper[-1]))
    if variant == 'B: clause (2) dropped':
        c2 = False
    if variant == 'B: clause (3) dropped':
        c3 = False
    if variant == 'B: clause (4) dropped':
        c4 = False
    if variant == 'B: clauses (2) and (4) dropped (the first sealed formula)':
        c2 = c4 = False
    if variant == 'B: clause (3) for every p':
        c3 = (a0 in E)
    x = 0 if (c1 or c2 or c3 or c4) else 1
    if variant == 'B: x = 0 always':
        x = 0
    if variant == 'B: x = 1 whenever k\' >= 1':
        x = 0 if c1 else 1
    return q * p ** e * (p ** kp + x)


VARIANTS = [None,
            'U: |F| in place of |F minus E|',
            'U: p^|E u F| + q p^|E| replaced by p^|E u F| alone',
            'B: a0 = first level in neither E nor F',
            "B: k' counts every level of F minus E, not only those beyond a0",
            'B: clause (2) dropped',
            'B: clause (3) dropped',
            'B: clause (3) for every p',
            'B: clause (4) dropped',
            'B: clauses (2) and (4) dropped (the first sealed formula)',
            'B: clause (4) with b in E only (b may be in F)',
            'B: clause (4) with b = a0 allowed (so clause (3) for p = 2 as well)',
            'B: clause (4) between a0 and SOME level of F minus E beyond a0',
            'B: x = 0 always',
            "B: x = 1 whenever k' >= 1"]


def main(triples):
    data = []
    for (p, q, n) in triples:
        B = json.load(open(os.path.join(HERE, 'outB', f'{p}_{q}_{n}.json')))
        for j in B['jobs']:
            if j.get('skipped') or j['found'] is None:
                continue
            assert j['found'] == j['lean']
            data.append((p, q, n, j['bal'], frozenset(j['E']), frozenset(j['F']), j['found']))
    print(f"patterns with an enumerated least size: {len(data)} (in {len(triples)} triples (p, q, n))")
    for v in VARIANTS:
        bad = [(p ** n * q, p, q, n, bal, sorted(E), sorted(F), m, rule(p, q, n, bal, E, F, v))
               for (p, q, n, bal, E, F, m) in data if rule(p, q, n, bal, E, F, v) != m]
        name = 'the rule as stated' if v is None else v
        if bad:
            b = min(bad)
            print(f"{name}: differs on {len(bad)} patterns; first in Z_{b[0]} (p={b[1]}, q={b[2]}): "
                  f"Phi_q|A={bool(b[4])}, E={b[5]}, F={b[6]}: least size {b[7]}, variant gives {b[8]}")
        else:
            print(f"{name}: differs on 0 patterns")


if __name__ == '__main__':
    triples = [tuple(map(int, a.split(':'))) for a in sys.argv[1:]]
    main(triples)

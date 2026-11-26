"""Compare the least sizes found by the two enumerations with Lean's values, pattern by pattern.

A = plain enumeration of all multisets of size <= S_A (outA/group<M>.json).
B = for each pattern P, every multiset of size <= Lean's value (+extra) with all of P dividing (outB/<p>_<q>_<n>.json).
Lean = lean-values.txt (printed by AuditEval.lean).

usage: compare.py p:q:n ...
"""
import json
import os
import sys

from rule_note import levels_of, read_lean
from runB import divisor_set

HERE = os.path.dirname(os.path.abspath(__file__))


def main(args):
    lean = read_lean(os.path.join(HERE, 'lean-values.txt'))
    rows = []
    all_mismatch = []
    for arg in args:
        p, q, n = map(int, arg.split(':')[:3])
        M = p ** n * q
        A = json.load(open(os.path.join(HERE, 'outA', f'group{M}.json')))
        pathB = os.path.join(HERE, 'outB', f'{p}_{q}_{n}.json')
        B = json.load(open(pathB)) if os.path.exists(pathB) else None
        ds = A['divisors']
        idx = {d: i for i, d in enumerate(ds)}
        SA = A['S']
        Apat = {int(k): v for k, v in A['patterns'].items()}
        Bjobs = {j['pmask']: j for j in B['jobs']} if B else {}
        npat = 0
        a_reached = a_equal = a_mis = a_beyond = 0
        b_equal = b_mis = b_skipped = 0
        cross_checked = cross_bad = 0
        kinds = [0, 0, 0]
        maxlean = 0
        detail = []
        for bal in (0, 1):
            for em in range(2 ** n):
                for fm in range(2 ** n):
                    kind, a0, kp, x, val, ok = lean[(p, q, n, bal, em, fm)]
                    assert ok == 1
                    npat += 1
                    kinds[kind] += 1
                    maxlean = max(maxlean, val)
                    E, F = sorted(levels_of(em, n)), sorted(levels_of(fm, n))
                    P = sorted(divisor_set(p, q, n, bal, E, F))
                    pmask = sum(1 << idx[d] for d in P)
                    # A: least size >= 1 with exactly this pattern
                    a_best = None
                    if pmask in Apat:
                        ss = [s for s in range(1, SA + 1) if Apat[pmask]['counts'][s]]
                        if ss:
                            a_best = ss[0]
                    if a_best is not None:
                        a_reached += 1
                        if a_best == val:
                            a_equal += 1
                        else:
                            a_mis += 1
                            all_mismatch.append(('A', p, q, n, bal, E, F, val, a_best))
                    else:
                        if val <= SA:
                            a_mis += 1
                            all_mismatch.append(('A: none up to bound, Lean value within bound', p, q, n, bal, E, F, val, None))
                        else:
                            a_beyond += 1
                    b_found = None
                    if B:
                        j = Bjobs[pmask]
                        assert j['lean'] == val and j['P'] == P
                        b_found = j['found']
                        if j.get('skipped'):
                            b_skipped += 1
                        elif b_found == val:
                            b_equal += 1
                        else:
                            b_mis += 1
                            all_mismatch.append(('B', p, q, n, bal, E, F, val, b_found))
                        # cross-check of the two programs: number of multisets of size s whose pattern contains P
                        for s in (range(0, min(SA, j['S']) + 1) if not (j['window'] or j.get('skipped')) else []):
                            a_sup = sum(v['counts'][s] for m, v in Apat.items() if m & pmask == pmask)
                            b_sup = j['sup_counts'][s] + (1 if s == 0 else 0)   # B does not list the empty multiset
                            cross_checked += 1
                            if a_sup != b_sup:
                                cross_bad += 1
                    detail.append((bal, E, F, kind, a0, val, a_best, b_found))
        rows.append(dict(p=p, q=q, n=n, M=M, patterns=npat, kinds=kinds, SA=SA, multisetsA=A['multisets'],
                         a_reached=a_reached, a_equal=a_equal, a_mis=a_mis, a_beyond=a_beyond,
                         b=bool(B), b_equal=b_equal, b_mis=b_mis, b_skipped=b_skipped, maxlean=maxlean,
                         b_window=sum(1 for j in B['jobs'] if j['window'] and not j.get('skipped')) if B else 0,
                         nodesB=sum(j['nodes'] for j in B['jobs']) if B else 0,
                         extra=B['extra'] if B else None,
                         cross_checked=cross_checked, cross_bad=cross_bad, detail=detail))
    print("group | p,q,n | patterns (thm1/thm2/thm3) | largest Lean value | A: bound, multisets | A: patterns with a multiset within bound | A: of those, least size = Lean | A: not reached, Lean value > bound | A: mismatches | B: least size = Lean | B: mismatches | A-B count cross-checks (bad)")
    for r in rows:
        print(f"Z_{r['M']} | {r['p']},{r['q']},{r['n']} | {r['patterns']} ({r['kinds'][0]}/{r['kinds'][1]}/{r['kinds'][2]}) | "
              f"{r['maxlean']} | {r['SA']}, {r['multisetsA']} | {r['a_reached']} | {r['a_equal']} | {r['a_beyond']} | {r['a_mis']} | "
              + (f"{r['b_equal']} of {r['patterns'] - r['b_skipped']} attempted ({r['b_skipped']} not attempted; {r['b_window']} with the window bound) | {r['b_mis']} | {r['cross_checked']} ({r['cross_bad']})" if r['b'] else "- | - | -"))
    print()
    print("mismatches:", len(all_mismatch))
    for m in all_mismatch:
        print("   ", m)
    with open(os.path.join(HERE, 'compare.json'), 'w') as f:
        json.dump(rows, f)
    return rows


if __name__ == '__main__':
    main(sys.argv[1:])

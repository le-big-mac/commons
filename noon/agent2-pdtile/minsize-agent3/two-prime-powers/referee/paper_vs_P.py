"""Arithmetic only.  For M = p^n q and EVERY pattern (not only up-sets): the bound of Corollary P against the value of the
paper's theorem for Z_{p^n q} (written from its statement in cor_UT.paper_rule).  Corollary P would be refuted by a pattern
whose proved least size is below the bound.  Also: for up-sets the two agree; and where bound = value, is the pattern an up-set?"""
import itertools, json
from lib import divisors, is_upset, corners, largest_upset_inside
from cor_UT import paper_rule
tot = below = eq_up = eq_notup = ups = ups_equal = 0
for p, q, n in [(2, 3, 1), (2, 3, 2), (2, 3, 3), (2, 3, 4), (2, 3, 5), (3, 2, 1), (3, 2, 2), (3, 2, 3), (3, 2, 4), (2, 5, 2), (2, 5, 3), (2, 5, 4), (5, 2, 2), (5, 2, 3), (3, 5, 2), (3, 5, 3), (5, 3, 2), (5, 3, 3), (3, 7, 3), (7, 2, 3), (2, 7, 4)]:
    M = p ** n * q; dv = [d for d in divisors(M) if d > 1]
    rec = dict(M=M, p=p, n=n, q=q, patterns=0, below_bound=0, at_bound_upsets=0, at_bound_not_upsets=0, upsets=0, upsets_equal=0)
    for k in range(len(dv) + 1):
        for D in itertools.combinations(dv, k):
            Ds = frozenset(D)
            val = paper_rule(p, q, n, [a for a in range(1, n + 1) if p ** a in Ds], [a for a in range(1, n + 1) if p ** a * q in Ds], q in Ds)
            U = largest_upset_inside(M, Ds); lb = sum(M // c for c in corners(M, U)); up = is_upset(M, Ds)
            rec['patterns'] += 1
            if val < lb: rec['below_bound'] += 1
            if val == lb and up: rec['at_bound_upsets'] += 1
            if val == lb and not up: rec['at_bound_not_upsets'] += 1
            if up:
                rec['upsets'] += 1; rec['upsets_equal'] += (val == sum(M // c for c in corners(M, Ds)))
    print(json.dumps(rec)); tot += rec['patterns']; below += rec['below_bound']; eq_notup += rec['at_bound_not_upsets']; ups += rec['upsets']; ups_equal += rec['upsets_equal']
print(f'# {tot} patterns on 21 groups Z_(p^n q): paper value below the bound of Corollary P in {below}; equal to it for a pattern that is not an up-set in {eq_notup}; up-sets {ups}, paper value = corner sum in {ups_equal}')

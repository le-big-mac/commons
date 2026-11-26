"""For the patterns of Z_100 not decided by any programme (as the raw files stand when this is run): the solver-free lower bound, and the
sizes that remain to be excluded below the smallest multiset known.  Reads only."""
import sys, json, glob
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers/second')
from lib import corners, largest_upset_inside
from cor_UT import paper_rule
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import recount
rows = recount.r100
M, p, q = 100, 2, 5
out = []
for D, r in sorted(rows.items(), key=lambda t: (len(t[0]), sorted(t[0]))):
    if r['dec']: continue
    lbs = []
    for pp, qq in ((p, q), (q, p)):
        N = pp * pp * qq; Dn = frozenset(d for d in D if N % d == 0)
        lbs.append(paper_rule(pp, qq, 2, [a for a in (1, 2) if pp ** a in Dn], [a for a in (1, 2) if pp ** a * qq in Dn], qq in Dn))
    lbs.append(sum(M // c for c in corners(M, largest_upset_inside(M, D))))
    step = p ** len(D & {p, p * p}) * q ** len(D & {q, q * q})
    lb = -(-max(lbs) // step) * step
    cand = list(range(lb, r['best'], step))
    out.append((sorted(D), r['best'], lbs, step, lb, cand))
    print(sorted(D), 'smallest known', r['best'], '| bounds (Z_20 rule, Z_50 rule, Corollary P)', lbs, '| sizes are multiples of', step, '| bound', lb, '| sizes left to exclude:', cand if cand else 'none: settled')

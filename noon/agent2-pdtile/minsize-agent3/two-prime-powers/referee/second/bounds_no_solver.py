"""Lower bounds that need no solver, for every pattern P of Z_M (M = p^2 q^2), set beside the smallest multiset on file:
  (a) the least size on Z_{p^2 q} of the pattern P restricted to the divisors of p^2 q (the paper's theorem for Z_{p^n q}); a multiset on
      Z_M with pattern exactly P reduces modulo p^2 q to a multiset of the same size whose pattern on Z_{p^2 q} is exactly that restriction;
  (b) the same with p q^2;
  (c) the bound of Corollary P;
  (d) the size is a multiple of p^(number of p, p^2 in P) * q^(number of q, q^2 in P)   (the mask is divisible by those Phi_d, Phi_{r^k}(1) = r).
The bound is max(a, b, c) rounded up to a multiple of (d).  Where it equals the size of the multiset on file, the least size is settled
by theorems and that multiset alone, whatever any programme proved.  Reads note/rows-{M}.json and note/witnesses-{M}.jsonl (checking each
multiset by the cuboid test).   usage: bounds_no_solver.py"""
import sys, json, os, time
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from lib import divisors, corners, largest_upset_inside, pattern, is_upset
from cor_UT import paper_rule
PQ = '/home/agent3/pq2/note/'
for M, p, q in ((36, 2, 3), (100, 2, 5)):
    rows = json.load(open(PQ + f'rows-{M}.json'))
    W = {tuple(w['D']): w for w in (json.loads(l) for l in open(PQ + f'witnesses-{M}.jsonl'))}
    settled = []; settled_undecided = []; settled_highs_only = []; below = []; n_dec = 0
    for r in rows:
        D = frozenset(r['D'])
        w = W.get(tuple(r['D']))
        if w is None: continue
        v = [0] * M
        for t in w['multiset'].split():
            if '^' in t: a, c = t.split('^'); v[int(a)] += int(c)
            else: v[int(t)] += 1
        assert sum(v) == r['size'] == w['size'] and pattern(M, v) == sorted(D)
        lbs = []
        for pp, qq in ((p, q), (q, p)):
            N = pp * pp * qq; Dn = frozenset(d for d in D if N % d == 0)
            lbs.append(paper_rule(pp, qq, 2, [a for a in (1, 2) if pp ** a in Dn], [a for a in (1, 2) if pp ** a * qq in Dn], qq in Dn))
        lbs.append(sum(M // c for c in corners(M, largest_upset_inside(M, D))))
        step = p ** len(D & {p, p * p}) * q ** len(D & {q, q * q})
        lb = -(-max(lbs) // step) * step
        if lb > r['size']: below.append((sorted(D), r['size'], lb))
        if r['by']: n_dec += 1
        if lb == r['size']:
            settled.append(sorted(D))
            if not r['by']: settled_undecided.append((sorted(D), r['size']))
            if r['by'] and 'G' not in r['by'] and 'C' not in r['by']: settled_highs_only.append((sorted(D), r['size']))
    print(f'Z_{M} (rows file written {time.strftime("%H:%M:%S", time.gmtime(os.path.getmtime(PQ + f"rows-{M}.json")))}): {len(rows)} patterns, {n_dec} decided by a programme in the table.')
    print(f'   multisets on file smaller than the no-solver bound (would refute a theorem): {below}')
    print(f'   patterns where the no-solver bound equals the size on file (least size settled without any solver): {len(settled)}')
    print(f'   of these, not decided by any programme in the table: {len(settled_undecided)}: {settled_undecided}')
    print(f'   of these, decided in the table by HiGHS alone: {len(settled_highs_only)}: {settled_highs_only}')
    print(f'   decided by a programme or settled without one: {len(set(map(tuple, settled)) | set(tuple(r["D"]) for r in rows if r["by"]))}')

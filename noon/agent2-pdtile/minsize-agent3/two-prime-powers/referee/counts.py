"""The author's counts, recomputed from his solver's output files (out/*.jsonl) with the referee's own code.
Reads only; writes nothing outside stdout.   usage: counts.py"""
import json, glob, itertools, collections, time, os
from lib import divisors, is_upset, corners, largest_upset_inside, pattern
from cor_UT import paper_rule

OUT = '/home/agent3/pq2/out/'


def load(files):
    """best record for each pattern: a proved one before an unproved one; one with a multiset before one without"""
    R = {}; n = 0
    for f in files:
        for l in open(f):
            if not l.startswith('{'): continue
            r = json.loads(l); n += 1; k = frozenset(r['D'])
            old = R.get(k)
            if old is None or (r['proved'] and not old['proved']) or (old['min'] is None and r['min'] is not None): R[k] = r
    return R, n


def witness(r, M):
    v = [0] * M
    for tok in r['witness'].split():
        if '^' in tok: i, w = tok.split('^'); v[int(i)] += int(w)
        else: v[int(tok)] += 1
    return v


def report(M, p, q, files):
    print(f'=== Z_{M}; files: {[os.path.basename(f) for f in files]}; read at {time.strftime("%H:%M:%S UTC", time.gmtime())}')
    R, nlines = load(files)
    dv = [d for d in divisors(M) if d > 1]
    print('records in the files:', nlines, '; distinct patterns:', len(R), 'of', 2 ** len(dv))
    found = {D: r for D, r in R.items() if r['min'] is not None}
    dec = {D: r['min'] for D, r in R.items() if r['min'] is not None and r['proved']}
    print('a multiset found:', len(found), '; proved least (decided):', len(dec), '; found but not proved least:', len(found) - len(dec),
          '; none found:', len(R) - len(found), '; "proved" with no multiset (infeasible within the cap):', sum(1 for r in R.values() if r['min'] is None and r['proved']))
    # every witness in the files, checked by the referee's exact test
    badw = 0
    for D, r in found.items():
        v = witness(r, M)
        if sum(v) != r['min'] or pattern(M, v) != sorted(D): badw += 1
    print('witnesses in the files whose size or exact pattern (referee\'s cuboid test) is not as recorded:', badw, 'of', len(found))
    vals = collections.Counter(dec.values())
    print('distinct decided values:', len(vals), '; largest decided:', max(vals), 'at', [sorted(D) for D, m in dec.items() if m == max(vals)])
    print('largest found (decided or not):', max(r['min'] for r in found.values()))
    # the half-size remark: no coordinate above the per-coordinate cap can occur below 2*cap
    print('cap of the runs (per coordinate) is M =', M, '; a multiset with a nonempty pattern has every multiplicity <= size/2, so the cap is harmless up to size', 2 * M)
    # up-sets
    ups = [D for D in R if is_upset(M, D)]
    upd = [D for D in ups if D in dec]
    eq = [D for D in upd if dec[D] == sum(M // c for c in corners(M, D))]
    eqf = [D for D in ups if D in found and found[D]['min'] == sum(M // c for c in corners(M, D))]
    print('up-sets:', len(ups), '; decided:', len(upd), '; decided and equal to the corner sum:', len(eq), '; found (decided or not) equal to the corner sum:', len(eqf),
          '; up-sets not decided:', [(sorted(D), R[D]['min'], sum(M // c for c in corners(M, D))) for D in ups if D not in dec])
    # Corollary P
    below_dec = []; below_found = []; eq_notup_dec = []; eq_notup_found = []
    for D, r in found.items():
        U = largest_upset_inside(M, D); lb = sum(M // c for c in corners(M, U))
        if r['min'] < lb:
            below_found.append((sorted(D), r['min'], lb))
            if D in dec: below_dec.append((sorted(D), r['min'], lb))
        if r['min'] == lb and not is_upset(M, D):
            eq_notup_found.append((sorted(D), lb))
            if D in dec: eq_notup_dec.append((sorted(D), lb))
    print('Corollary P: decided patterns below the bound:', below_dec, '; found (decided or not) below the bound:', below_found)
    print('Corollary P: non-up-sets AT the bound, decided:', eq_notup_dec, '; found (decided or not):', eq_notup_found)
    # sub-lattices p^2 q and p q^2
    for (pp, qq) in ((p, q), (q, p)):
        N = pp * pp * qq; outside = [d for d in dv if N % d]
        inside = [D for D in R if not (D & set(outside))]
        de = [D for D in inside if D in dec]
        def val(D):
            return paper_rule(pp, qq, 2, [a for a in (1, 2) if pp ** a in D], [a for a in (1, 2) if pp ** a * qq in D], qq in D)
        same = [D for D in de if dec[D] == val(D)]
        samef = [D for D in inside if D in found and found[D]['min'] == val(D)]
        print(f'patterns inside the divisors of {N}: {len(inside)}; decided {len(de)}; decided and equal to the Z_{N} rule: {len(same)}; found (decided or not) equal: {len(samef)}; decided and different:',
              [(sorted(D), dec[D], val(D)) for D in de if dec[D] != val(D)])
    # code check lines of the sheets (Q0 / Y0)
    e = lambda D, a: len(D & {a, a * a})
    bad = []
    for D, m in dec.items():
        if m % (p ** e(D, p) * q ** e(D, q)): bad.append((sorted(D), m, 'not a multiple'))
        for (pp, qq) in ((p, q), (q, p)):
            N = pp * pp * qq; Dn = frozenset(d for d in D if N % d == 0)
            v = paper_rule(pp, qq, 2, [a for a in (1, 2) if pp ** a in Dn], [a for a in (1, 2) if pp ** a * qq in Dn], qq in Dn)
            if m < v: bad.append((sorted(D), m, f'below the Z_{N} value {v}'))
    print('code-check line (multiple of p^e_p q^e_q; at least the Z_{p^2q} and Z_{pq^2} values of the restricted patterns): failures', bad)
    return R, dec


R36, dec36 = report(36, 2, 3, sorted(glob.glob(OUT + 'z36-[0-9].jsonl')) + [OUT + 'z36-again.jsonl'])
print()
R36o, dec36o = report(36, 2, 3, sorted(glob.glob(OUT + 'z36-[0-9].jsonl')))
print()
R100, dec100 = report(100, 2, 5, sorted(glob.glob(OUT + 'z100-[0-9].jsonl')))
print()
# ---- first sheet, line by line (as scored from the first run only, and as it stands now)
for name, dec, R in (('first run only', dec36o, R36o), ('with z36-again as it is now', dec36, R36)):
    mixed = {6, 12, 18, 36}
    q2 = [(D, m) for D, m in dec.items() if not (D & mixed)]
    print(f'sheet 1 ({name}): Q1 witnesses {sum(1 for r in R.values() if r["min"] is not None)} of {len(R)}; Q2 {sum(1 for D, m in q2 if m == 2 ** len(D & {2, 4}) * 3 ** len(D & {3, 9}))} of {len(q2)};',
          f'Q3 {dec.get(frozenset({6, 12, 18, 36}))}; Q4 {dec.get(frozenset({36}))}; Q6 distinct {len(set(dec.values()))}; Q7 largest {max(dec.values())}; decided {len(dec)}')
# ---- second sheet: Y3 and the Brier score
tr = lambda D: frozenset({3: 5, 9: 25, 6: 10, 12: 20, 18: 50, 36: 100}.get(d, d) for d in D)
for name, d36 in (('Z_36 from the first run only', dec36o), ('Z_36 with z36-again as it is now', dec36)):
    both = [(d36[D], dec100[tr(D)]) for D in d36 if tr(D) in dec100]
    eqp = same = 0
    for (m1, n1), (m2, n2) in itertools.combinations(both, 2):
        if m1 == m2: eqp += 1; same += (n1 == n2)
    print(f'sheet 2, Y3 ({name}): decided on both {len(both)}; pairs equal on Z_36: {eqp}; of these equal on Z_100: {same} = {100 * same / eqp:.2f}%')
held = dict(Y1=(0.85, True), Y2=(0.85, True), Y3=(0.55, False), Y4=(0.40, True), Y5=(0.60, False))
b = sum((pr - (1 if h else 0)) ** 2 for pr, h in held.values()) / len(held)
print('Brier over Y1..Y5 with chances 85, 85, 55, 40, 60 and outcomes held, held, not, held, not:', b)

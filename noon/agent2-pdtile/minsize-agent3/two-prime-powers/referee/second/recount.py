"""Second reading: every count of the note's "In short" item 4 and section 4, recomputed from the raw files with the referee's own code
(not from note/rows-*.json, which is then compared with what is found here).

Sources read (nothing is written outside stdout):
  G   /home/agent3/pq2/out/z{M}-[0-9].jsonl (+ z36-again.jsonl)                  the author's solver
  R   /home/agent3/pq2/referee/two-powers/out/retable-{M}-[0-9].jsonl            the referee's programme, 60 s a pattern
  C   /home/agent3/pq2/referee/two-powers/out/cpsat*.jsonl                       CP-SAT on the referee's model (Z_36 only)
  R+  /home/agent3/pq2/out2/z{M}-*.jsonl                                         the referee's programme run again by the author
  note/rows-{M}.json, note/witnesses-{M}.jsonl, note/table-{M}.md                what the note's tables say
Divisibility by the cuboid test of ../lib.py; the rule for Z_{p^n q} from ../cor_UT.py (written from the paper's statement).
usage: recount.py
"""
import sys, json, glob, itertools, collections, time, os, re
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from lib import divisors, is_upset, corners, largest_upset_inside, pattern
from cor_UT import paper_rule

PQ = '/home/agent3/pq2/'


def vec(M, s):
    v = [0] * M
    for t in s.split():
        if '^' in t: a, w = t.split('^'); v[int(a)] += int(w)
        else: v[int(t)] += 1
    return v


def load(M):
    G = {}
    for f in sorted(glob.glob(PQ + f'out/z{M}-[0-9].jsonl')) + ([PQ + 'out/z36-again.jsonl'] if M == 36 else []):
        for l in open(f):
            if l.startswith('{'):
                r = json.loads(l); k = frozenset(r['D']); o = G.get(k)
                if o is None or (r['proved'] and not o['proved']) or (o['min'] is None and r['min'] is not None): G[k] = r
    R = {}
    for f in sorted(glob.glob(PQ + f'referee/two-powers/out/retable-{M}-[0-9].jsonl')):
        for l in open(f):
            if l.startswith('{'): r = json.loads(l); R[frozenset(r['D'])] = r
    RP = {}
    for f in sorted(glob.glob(PQ + f'out2/z{M}-*.jsonl')):
        for l in open(f):
            if l.startswith('{'):
                r = json.loads(l); k = frozenset(r['D']); o = RP.get(k)
                if o is None or (r['status'] == 'optimal' and o['status'] != 'optimal'): RP[k] = r
    C = {}
    if M == 36:
        for f in sorted(glob.glob(PQ + 'referee/two-powers/out/cpsat*.jsonl')):
            for l in open(f):
                if l.startswith('{'):
                    r = json.loads(l); k = frozenset(r['D'])
                    if r['cpsat_status'] == 'infeasible': C[k] = r['author_value']
                    else: C.setdefault(k, None)
    return G, R, RP, C


def report(M, p, q):
    print(f'=== Z_{M}, read at {time.strftime("%H:%M:%S UTC", time.gmtime())}')
    G, R, RP, C = load(M)
    dv = [d for d in divisors(M) if d > 1]
    assert len(G) == len(R) == 2 ** len(dv)
    rows = {}
    nwit = badwit = 0
    for D in G:
        g, r, rp = G[D], R[D], RP.get(D)
        Gdec = g['proved'] and g['min'] is not None
        Rdec = r['referee_status'] == 'optimal'
        RPdec = bool(rp) and rp['status'] == 'optimal'
        vals = set()
        if Gdec: vals.add(g['min'])
        if Rdec: vals.add(r['referee_least'])
        if RPdec: vals.add(rp['size'])
        assert len(vals) <= 1, ('two programmes prove different values', sorted(D), vals)
        sizes = []
        if g['min'] is not None:
            v = vec(M, g['witness']); nwit += 1
            if sum(v) != g['min'] or pattern(M, v) != sorted(D): badwit += 1
            sizes.append(('G', g['min']))
        if rp and rp.get('A') is not None:
            v = rp['A']; nwit += 1
            if sum(v) != rp['size'] or min(v) < 0 or pattern(M, v) != sorted(D): badwit += 1
            sizes.append(('R+', rp['size']))
        if r['referee_least'] is not None: sizes.append(('R', r['referee_least']))
        best = min(s for _, s in sizes) if sizes else None
        if vals: assert next(iter(vals)) == best, ('a proved value is not the smallest known', sorted(D), vals, sizes)
        best_has_multiset = any(s == best for src, s in sizes if src in ('G', 'R+'))
        rows[D] = dict(best=best, Gdec=Gdec, Rdec=Rdec, RPdec=RPdec, Gmin=g['min'], Rleast=r['referee_least'], dec=Gdec or Rdec or RPdec,
                       wit=best_has_multiset, cp=(C.get(D) == best and best is not None) if D in C else None)
    print('multisets in the sources checked by the cuboid test (size, exact pattern):', nwit, '; wrong:', badwit)
    dec = {D: r['best'] for D, r in rows.items() if r['dec']}
    nG = sum(1 for r in rows.values() if r['Gdec']); nR = sum(1 for r in rows.values() if r['Rdec'])
    print('decided by some programme:', len(dec), 'of', len(rows), '; by G:', nG, '; by R (60 s):', nR, '; by both G and R:', sum(1 for r in rows.values() if r['Gdec'] and r['Rdec']),
          '; by R and not G:', sum(1 for r in rows.values() if r['Rdec'] and not r['Gdec']), '; by G and not R:', [sorted(D) for D, r in rows.items() if r['Gdec'] and not r['Rdec']],
          '; by R+ alone:', sorted((sorted(D), r['best']) for D, r in rows.items() if r['RPdec'] and not r['Gdec'] and not r['Rdec']),
          '; by R+ and G but not R:', sorted((sorted(D), r['best']) for D, r in rows.items() if r['RPdec'] and r['Gdec'] and not r['Rdec']))
    notG = sorted(r['best'] for r in rows.values() if r['dec'] and not r['Gdec'])
    print('decided and not by G:', len(notG), '; their values:', notG if len(notG) <= 12 else '(many)')
    if M == 36:
        l8 = sorted((sorted(D), r['best'], r['cp']) for D, r in rows.items() if r['dec'] and not r['Gdec'])
        print('   the eight, with CP-SAT on the referee\'s model proving nothing smaller (True) or not (False/None):', l8)
        print('   CP-SAT records in the referee\'s files:', {tuple(sorted(D)): v for D, v in C.items()})
    vals = collections.Counter(dec.values())
    print('distinct decided values:', len(vals), '; largest:', max(vals), 'at', sorted(sorted(D) for D, m in dec.items() if m == max(vals)))
    und = sorted((sorted(D), r['best'], r['Gmin'], r['Rleast']) for D, r in rows.items() if not r['dec'])
    print('not decided by any programme:', len(und), '(pattern, smallest known, G\'s size, R\'s size):', und)
    print('   of these, smallest known below G\'s size, or G had none:', sum(1 for D, b, gm, rl in und if gm is None or b < gm))
    # R against G in R's own run
    bet = [(sorted(D), r['Gmin'], r['Rleast']) for D, r in rows.items() if r['Rdec'] and r['Gmin'] is not None and r['Rleast'] < r['Gmin']]
    non = [(sorted(D), r['Rleast']) for D, r in rows.items() if r['Rdec'] and r['Gmin'] is None]
    print('R decided (own run) with a smaller multiset than G\'s:', len(bet), sorted(bet), '; R decided where G found none:', len(non), sorted(non))
    print('rows of G not marked proved by G whose size is not the smallest now known:', sum(1 for r in rows.values() if not r['Gdec'] and r['Gmin'] is not None and r['best'] < r['Gmin']),
          '; rows where G found none:', sum(1 for r in rows.values() if r['Gmin'] is None))
    print('rows with no multiset on file at the smallest known size:', [sorted(D) for D, r in rows.items() if not r['wit']])
    # up-sets, Corollary P
    ups = [D for D in rows if is_upset(M, D)]
    print('up-sets:', len(ups), '; decided:', sum(1 for D in ups if rows[D]['dec']), '; equal to the corner sum:', sum(1 for D in ups if rows[D]['dec'] and rows[D]['best'] == sum(M // c for c in corners(M, D))))
    below = []; at = []
    for D, r in rows.items():
        if r['best'] is None: continue
        lb = sum(M // c for c in corners(M, largest_upset_inside(M, D)))
        if r['best'] < lb: below.append(sorted(D))
        if r['best'] == lb and not is_upset(M, D): at.append(sorted(D))
    print('smallest known below the bound of Corollary P:', below, '; not up-sets with smallest known equal to the bound:', at)
    # sub-lattices
    allsub = set()
    for (pp, qq) in ((p, q), (q, p)):
        N = pp * pp * qq
        ins = [D for D in rows if all(N % d == 0 for d in D)]; allsub |= set(ins)
        val = lambda D: paper_rule(pp, qq, 2, [a for a in (1, 2) if pp ** a in D], [a for a in (1, 2) if pp ** a * qq in D], qq in D)
        d = [D for D in ins if rows[D]['dec']]
        print(f'inside the divisors of {N}: {len(ins)}; decided {len(d)}; decided and equal to the Z_{N} rule {sum(1 for D in d if rows[D]["best"] == val(D))}; '
              f'smallest known equal to the rule (decided or not) {sum(1 for D in ins if rows[D]["best"] == val(D))}; smallest known BELOW the rule {[sorted(D) for D in ins if rows[D]["best"] is not None and rows[D]["best"] < val(D)]}; '
              f'not decided {[(sorted(D), rows[D]["best"], val(D)) for D in ins if not rows[D]["dec"]]}')
    print('patterns inside one or other sub-lattice:', len(allsub), '; of them up-sets:', [sorted(D) for D in allsub if is_upset(M, D)], '; so not up-sets:', sum(1 for D in allsub if not is_upset(M, D)),
          '; up-sets or inside a sub-lattice:', len(set(ups) | allsub))
    # the note's own rows file and witnesses and table
    try:
        nr = {frozenset(r['D']): r for r in json.load(open(PQ + f'note/rows-{M}.json'))}
        diff = [sorted(D) for D in rows if nr[D]['size'] != rows[D]['best'] or bool(nr[D]['by']) != rows[D]['dec']]
        by = collections.Counter(','.join(r['by']) for r in nr.values())
        print(f'note/rows-{M}.json (written {time.strftime("%H:%M:%S", time.gmtime(os.path.getmtime(PQ + f"note/rows-{M}.json")))}): rows whose size or decided flag differs from this recount:', diff, '; "proved least by" cells:', dict(by))
        W = [json.loads(l) for l in open(PQ + f'note/witnesses-{M}.jsonl')]
        bad = 0
        for w in W:
            v = vec(M, w['multiset'])
            if sum(v) != w['size'] or pattern(M, v) != w['D'] or nr[frozenset(w['D'])]['size'] != w['size']: bad += 1
        print(f'note/witnesses-{M}.jsonl: {len(W)} multisets; size, exact pattern (cuboid test) or agreement with the row wrong in {bad}; patterns without a multiset: {len(rows) - len(set(frozenset(w["D"]) for w in W))}')
        tl = [l for l in open(PQ + f'note/table-{M}.md') if re.match(r'^\| [0-9(]', l)]
        td = 0
        for l in tl:
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            D = frozenset(int(x) for x in c[0].split(',')) if c[0] != '(none)' else frozenset()
            if str(nr[D]['size']) != c[1] or ', '.join(nr[D]['by']) != c[2] or (c[4] == 'yes') != nr[D]['up'] or int(c[5]) != nr[D]['bound']: td += 1
        print(f'note/table-{M}.md: {len(tl)} rows; rows that differ from rows-{M}.json: {td}')
    except Exception as e:
        print('could not compare with the note\'s files:', repr(e))
    return rows


r36 = report(36, 2, 3)
print()
r100 = report(100, 2, 5)
print()
tr = lambda D: frozenset({3: 5, 9: 25, 6: 10, 12: 20, 18: 50, 36: 100}.get(d, d) for d in D)
both = [(r36[D]['best'], r100[tr(D)]['best']) for D in r36 if r36[D]['dec'] and r100[tr(D)]['dec']]
eqp = same = 0
for (m1, n1), (m2, n2) in itertools.combinations(both, 2):
    if m1 == m2: eqp += 1; same += (n1 == n2)
print(f'third line of the second sheet on the fuller tables: decided on both {len(both)}; pairs with equal least size on Z_36: {eqp}; of these equal on Z_100 too: {same} = {100 * same / eqp:.2f}%')

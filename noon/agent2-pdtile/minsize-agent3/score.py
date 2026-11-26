"""Score the sealed expectations of expectations.md against the computed tables.
usage: score.py OUT_DIR N [N ...]     (reads OUT_DIR/n{N}-p{p}-q{q}-{multi|set}-{cpsat|highs}.jsonl, also .part files)"""
import sys, json, glob, os, re, collections
od = sys.argv[1]; NS = [int(x) for x in sys.argv[2:]]
def load(n, p, q, kind, solver):
    for ext in ('', '.part'):
        f = f'{od}/n{n}-p{p}-q{q}-{kind}-{solver}.jsonl{ext}'
        if os.path.exists(f):
            rows = [json.loads(l) for l in open(f) if l.startswith('{')]
            return {(tuple(r['E']), tuple(r['F'])): r for r in rows}, ext
    return None, None
def formula(p, q, n, E, F):
    e = len(E); FE = [a for a in F if a >= 1 and a not in E]
    if 0 not in F:
        k = len(FE); return ('M1', p ** e * (p ** k + q) if k >= 1 else p ** e)
    if set(F) == set(range(0, n + 1)): return ('M3', q * p ** e)
    a0 = min(a for a in range(1, n + 1) if a not in F)
    k2 = len([a for a in FE if a > a0])
    x = 0 if k2 == 0 else (0 if (a0 in E and p >= 3) else 1)
    return ('M4', q * p ** e * (p ** k2 + x))
PAIRS = [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3)]
tally = collections.Counter(); bad = collections.defaultdict(list); table = {}
for n in NS:
    for p, q in PAIRS:
        M, ext = load(n, p, q, 'multi', 'cpsat')
        if M is None: print(f'n={n} p={p} q={q}: no multiset table yet'); continue
        Hh, _ = load(n, p, q, 'multi', 'highs'); S, sext = load(n, p, q, 'set', 'cpsat')
        und = [k for k, r in M.items() if r['undecided'] or r['min'] is None]
        print(f'n={n} p={p} q={q} M={p ** n * q}: {len(M)} patterns{" (partial)" if ext else ""}; undecided or none: {len(und)}')
        for (E, F), r in sorted(M.items()):
            if r['undecided'] or r['min'] is None: continue
            which, f = formula(p, q, n, E, F); ok = (f == r['min'])
            tally[which, ok] += 1; table[n, p, q, E, F] = r['min']
            if not ok: bad[which].append((n, p, q, E, F, r['min'], f, r['witness']))
            if 0 not in F:
                tally['M2', r['min'] >= p ** len(set(E) | set(F))] += 1
            if Hh and (E, F) in Hh and not Hh[(E, F)]['undecided'] and Hh[(E, F)]['min'] is not None:
                tally['solvers agree', Hh[(E, F)]['min'] == r['min']] += 1
                if Hh[(E, F)]['min'] != r['min']: bad['solvers'].append((n, p, q, E, F, r['min'], Hh[(E, F)]['min']))
            if S and (E, F) in S and not S[(E, F)]['undecided']:
                s = S[(E, F)]['min']
                if s is not None:
                    tally['S1 set >= multi', s >= r['min']] += 1
                    if n not in E and n not in F: tally['S2 bottom level free: set = multi', s == r['min']] += 1
                    if 0 not in F and (n in E or n in F): tally['S4 candidates (0 not in F, level n used, a set exists): set > multi', s > r['min']] += 1
                    if s != r['min'] and n not in E and n not in F: bad['S2'].append((n, p, q, E, F, r['min'], s))
                if 0 not in F and set(range(1, n + 1)) <= set(F) and set(E) != set(range(1, n + 1)):
                    tally['S3 no such set', s is None] += 1
                    if s is not None: bad['S3'].append((n, p, q, E, F, s, S[(E, F)]['witness']))
for k in sorted(tally, key=str): print(f'  {k[0]:70s} {"held" if k[1] else "FAILED"}: {tally[k]}')
for which, L in bad.items():
    print(f'--- {which}: {len(L)} not as expected'); 
    for row in L[:40]: print('    ', row)
# M4a, M4b
for n, p, q, E, F in sorted(table):
    if n == 2 and E == () and F == (0, 2): print(f'  M4a p={p} q={q}: min {table[n, p, q, E, F]}, expected q(p+1) = {q * (p + 1)}')
    if n == 2 and E == (1,) and F == (0, 2): print(f'  M4b p={p} q={q}: min {table[n, p, q, E, F]}, expected {6 * q if p == 2 else q * p * p}')
# M5: a level in neither E nor F does not matter: compare each pattern at n with the pattern at n+1 that inserts an empty level at position j
def insert(E, F, j):   # new empty level j (1..n+1); levels >= j shift up
    sh = lambda a: a + 1 if a >= j else a
    return tuple(sorted(sh(a) for a in E)), tuple(sorted((0 if a == 0 else sh(a)) for a in F))
for n in NS:
    if n + 1 not in NS: continue
    for p, q in PAIRS:
        same = diff = 0; ex = []
        for (nn, pp, qq, E, F), v in table.items():
            if (nn, pp, qq) != (n, p, q): continue
            for j in range(1, n + 2):
                E2, F2 = insert(E, F, j); w = table.get((n + 1, p, q, E2, F2))
                if w is None: continue
                if w == v: same += 1
                else: diff += 1; ex.append((E, F, j, v, w))
        if same + diff: print(f'  M5 p={p} q={q}: inserting an empty level into an n={n} pattern: same minimum {same}, different {diff}', ex[:8])

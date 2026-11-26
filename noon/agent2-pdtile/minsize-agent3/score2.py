"""Score the second sheet (expectations-2.md) on the n = 4 tables.   usage: score2.py OUT_DIR p q [p q ...]"""
import sys, json, os, collections
od = sys.argv[1]; pairs = [(int(sys.argv[i]), int(sys.argv[i + 1])) for i in range(2, len(sys.argv), 2)]
n = 4
def load(p, q, kind, solver):
    for ext in ('', '.part'):
        f = f'{od}/n{n}-p{p}-q{q}-{kind}-{solver}.jsonl{ext}'
        if os.path.exists(f):
            return {(tuple(r['E']), tuple(r['F'])): r for r in (json.loads(l) for l in open(f) if l.startswith('{'))}, ext
    return None, None
def M1(p, q, E, F):
    e = len(E); k = len([a for a in F if a >= 1 and a not in E]); return p ** e * (p ** k + q) if k else p ** e
def R(p, q, E, F):
    e = len(E); a0 = min(a for a in range(1, n + 1) if a not in F)
    FE = sorted(a for a in F if a > a0 and a not in E); k2 = len(FE)
    if k2 == 0: x = 0
    elif any(a in E for a in range(1, a0)): x = 0
    elif a0 in E and p >= 3: x = 0
    elif a0 in E and p == 2 and any((a in E and a not in F) for a in range(a0 + 1, FE[0])): x = 0
    else: x = 1
    return q * p ** e * (p ** k2 + x), x
for p, q in pairs:
    Mt, ext = load(p, q, 'multi', 'cpsat'); St, sext = load(p, q, 'set', 'cpsat'); Ht, hext = load(p, q, 'multi', 'highs')
    if Mt is None: print(p, q, 'no table'); continue
    t = collections.Counter(); miss = []
    for (E, F), r in sorted(Mt.items()):
        if r['undecided'] or r['min'] is None: t['undecided'] += 1; continue
        m = r['min']
        if 0 not in F:
            t['R3 M1', m == M1(p, q, E, F)] += 1
            if m != M1(p, q, E, F): miss.append(('M1', E, F, m, M1(p, q, E, F)))
            if St and (E, F) in St and not St[(E, F)]['undecided'] and St[(E, F)]['min'] is not None:
                t['R5 pattern with a set: set > multi', St[(E, F)]['min'] > m] += 1
                if St[(E, F)]['min'] > m: miss.append(('set>multi', E, F, m, St[(E, F)]['min']))
        elif set(F) == set(range(0, n + 1)):
            t['R4 M3', m == q * p ** len(E)] += 1
        else:
            f, x = R(p, q, E, F); t['R1 R', m == f] += 1
            if m != f: miss.append(('R', E, F, m, f, 'R said x=%d' % x)); t['R2 miss is R too high', m < f] += 1
        if Ht and (E, F) in Ht and not Ht[(E, F)]['undecided'] and Ht[(E, F)]['min'] is not None: t['solvers agree', Ht[(E, F)]['min'] == m] += 1
    print(f'p={p} q={q} n={n} M={p ** n * q}: {len(Mt)} patterns{" (partial)" if ext else ""}; sets table: {len(St) if St else 0}{" (partial)" if sext else ""}; highs: {len(Ht) if Ht else 0}{" (partial)" if hext else ""}')
    for k in sorted(t, key=str): print('   ', k, t[k])
    for row in miss[:40]: print('      ', row)

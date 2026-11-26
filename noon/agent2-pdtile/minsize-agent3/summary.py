"""Tables for the note: what was computed, and how each formula did.   usage: summary.py OUT_DIR"""
import sys, json, os, collections, itertools
od = sys.argv[1]
PAIRS = [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3)]
def load(n, p, q, kind, solver):
    for ext in ('', '.part'):
        f = f'{od}/n{n}-p{p}-q{q}-{kind}-{solver}.jsonl{ext}'
        if os.path.exists(f):
            return {(tuple(r['E']), tuple(r['F'])): r for r in (json.loads(l) for l in open(f) if l.startswith('{'))}, bool(ext)
    return {}, None
def M1(p, q, E, F):
    e = len(E); k = len([a for a in F if a >= 1 and a not in E]); return p ** e * (p ** k + q) if k else p ** e
def M4(p, q, n, E, F):
    e = len(E); a0 = min(a for a in range(1, n + 1) if a not in F); k2 = len([a for a in F if a > a0 and a not in E])
    x = 0 if k2 == 0 else (0 if (a0 in E and p >= 3) else 1); return q * p ** e * (p ** k2 + x)
def R(p, q, n, E, F):
    e = len(E); a0 = min(a for a in range(1, n + 1) if a not in F); FE = sorted(a for a in F if a > a0 and a not in E); k2 = len(FE)
    if k2 == 0 or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or (a0 in E and p == 2 and any((a in E and a not in F) for a in range(a0 + 1, FE[0]))): x = 0
    else: x = 1
    return q * p ** e * (p ** k2 + x)
tot = collections.Counter(); rows = []; table = {}
for n in (2, 3, 4):
    for p, q in PAIRS:
        C, cpart = load(n, p, q, 'multi', 'cpsat'); H, hpart = load(n, p, q, 'multi', 'highs'); S, spart = load(n, p, q, 'set', 'cpsat')
        if not C and not H: continue
        dec = {}
        for k in set(C) | set(H):
            vals = [T[k]['min'] for T in (C, H) if k in T and not T[k]['undecided'] and T[k]['min'] is not None]
            if vals:
                assert len(set(vals)) == 1, (n, p, q, k, vals); dec[k] = vals[0]
        both = sum(1 for k in dec if all(k in T and not T[k]['undecided'] and T[k]['min'] is not None for T in (C, H)))
        c = collections.Counter()
        for (E, F), m in dec.items():
            table[n, p, q, E, F] = m
            if 0 not in F: c['a', m == M1(p, q, E, F)] += 1; c['U', m >= p ** len(set(E) | set(F))] += 1
            elif set(F) == set(range(n + 1)): c['b', m == q * p ** len(E)] += 1
            else: c['m4', m == M4(p, q, n, E, F)] += 1; c['r', m == R(p, q, n, E, F)] += 1
        sets_exist = sum(1 for k, r in S.items() if not r['undecided'] and r['min'] is not None)
        sets_same = sum(1 for k, r in S.items() if not r['undecided'] and r['min'] is not None and k in dec and r['min'] == dec[k])
        sets_bigger = sum(1 for k, r in S.items() if not r['undecided'] and r['min'] is not None and k in dec and r['min'] > dec[k])
        s2 = [(r['min'] == dec[k]) for k, r in S.items() if not r['undecided'] and r['min'] is not None and k in dec and n not in k[0] and n not in k[1]]
        s3 = [(r['min'] is None) for k, r in S.items() if not r['undecided'] and 0 not in k[1] and set(range(1, n + 1)) <= set(k[1]) and set(k[0]) != set(range(1, n + 1))]
        rows.append((n, p, q, p ** n * q, 2 ** n * 2 ** (n + 1), len(dec), both, c, len(S), sets_exist, sets_same, sets_bigger, sum(s2), len(s2), sum(s3), len(s3), cpart, hpart, spart))
        for k, v in c.items(): tot[k] += v
        tot['dec'] += len(dec); tot['both'] += both; tot['sets_exist'] += sets_exist; tot['sets_same'] += sets_same; tot['sets_bigger'] += sets_bigger; tot['s2'] += sum(s2); tot['s2n'] += len(s2); tot['s3'] += sum(s3); tot['s3n'] += len(s3)
print('| n | p, q | order | patterns | decided | by both solvers | Φ_q ∤ A: formula right | F all levels: right | rest of Φ_q | A: first formula right | refined rule right | patterns with a set (of those tried) | sets: same minimum |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for (n, p, q, M, npat, ndec, both, c, nS, se, ss, sb, s2, s2n, s3, s3n, cp, hp, sp) in rows:
    f = lambda key: f"{c[key, True]} of {c[key, True] + c[key, False]}"
    print(f"| {n} | {p}, {q} | {M} | {npat} | {ndec} | {both} | {f('a')} | {f('b')} | {f('m4')} | {f('r')} | {se} of {nS}{' (sets not run)' if not nS else ''} | {ss} of {se} |")
f = lambda key: f"{tot[key, True]} of {tot[key, True] + tot[key, False]}"
print(f"\ntotals: decided {tot['dec']}; by both solvers {tot['both']}; M1 {f('a')}; lower bound p^|E u F| {f('U')}; M3 {f('b')}; M4 {f('m4')}; R {f('r')}; sets exist {tot['sets_exist']}, same minimum {tot['sets_same']}, larger {tot['sets_bigger']}; S2 {tot['s2']} of {tot['s2n']}; S3 {tot['s3']} of {tot['s3n']}")
# M5, split by whether 0 is in F
def insert(E, F, j):
    sh = lambda a: a + 1 if a >= j else a
    return tuple(sorted(sh(a) for a in E)), tuple(sorted((0 if a == 0 else sh(a)) for a in F))
m5 = collections.Counter()
for (n, p, q, E, F), v in table.items():
    for j in range(1, n + 2):
        w = table.get((n + 1, p, q) + insert(E, F, j))
        if w is not None: m5[0 in F, w == v] += 1
print(f"M5 (an empty level inserted): 0 not in F: same {m5[False, True]}, different {m5[False, False]}; 0 in F: same {m5[True, True]}, different {m5[True, False]}")
# the misses of the first formula M4
miss = [(n, p, q, E, F, v, M4(p, q, n, E, F), R(p, q, n, E, F)) for (n, p, q, E, F), v in sorted(table.items()) if 0 in F and set(F) != set(range(n + 1)) and v != M4(p, q, n, E, F)]
print(len(miss), 'misses of the first formula; of these the refined rule gets', sum(1 for m in miss if m[5] == m[7]))
for m in miss[:60]: print('  ', m)

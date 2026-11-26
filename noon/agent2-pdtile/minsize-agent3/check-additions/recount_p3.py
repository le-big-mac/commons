"""A fresh reader's recount for the paragraph "When my runs ended" (section 5) and for item (3) of the
paragraph added before section 8.  Written without looking at summary.py's counting code beyond the meaning
of the fields.  usage: recount_p3.py OUT_DIR      (reads only)"""
import sys, json, os, glob, re, collections
od = sys.argv[1]

def read(path):
    rows = {}
    for line in open(path):
        line = line.strip()
        if not line.startswith('{'):
            continue
        r = json.loads(line)
        key = (frozenset(r['E']), frozenset(r['F']))
        assert key not in rows, (path, key)
        rows[key] = r
    return rows

def decided(r):
    # a pattern is decided when a witness was found (min is a number) and no smaller admissible size is left undecided
    return r['min'] is not None and not r['undecided']

groups = collections.defaultdict(dict)       # (n, p, q) -> {(kind, solver): (rows, is_part)}
for path in sorted(glob.glob(os.path.join(od, 'n*-p*-q*-*.jsonl*'))):
    name = os.path.basename(path)
    m = re.fullmatch(r'n(\d+)-p(\d+)-q(\d+)-(multi|set)-(cpsat|highs)\.jsonl(\.part)?', name)
    if not m:
        print('left out (not a table of a whole group):', name)
        continue
    n, p, q = int(m[1]), int(m[2]), int(m[3])
    rows = read(path)
    for r in rows.values():
        assert (r['p'], r['q'], r['n']) == (p, q, n) and r['solver'] == m[5], path
    groups[n, p, q][m[4], m[5]] = (rows, bool(m[6]))

def thm(p, q, E, F):            # section 2
    e = len(E); k = len([a for a in F if a >= 1 and a not in E])
    return p ** e * (p ** k + q) if k else p ** e

def first_formula(p, q, n, E, F):   # sheet 1, line M4, as the note's section 6 words it
    e = len(E); a0 = min(a for a in range(1, n + 1) if a not in F)
    k2 = len([a for a in F if a > a0 and a not in E])
    x = 0 if (k2 == 0 or (a0 in E and p >= 3)) else 1
    return q * p ** e * (p ** k2 + x)

def rule(p, q, n, E, F):        # section 3, from the note's words
    e = len(E); a0 = min(a for a in range(1, n + 1) if a not in F)
    deeper = sorted(a for a in F if a > a0 and a not in E); k2 = len(deeper)
    c1 = k2 == 0
    c2 = any(a in E for a in range(1, a0))
    c3 = a0 in E and p >= 3
    c4 = (not c1) and a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, deeper[0]))
    x = 0 if (c1 or c2 or c3 or c4) else 1
    return q * p ** e * (p ** k2 + x)

T = collections.Counter(); table = {}
print('n p q order | rows cpsat (part?) | rows highs (part?) | decided | by both | cpsat alone | highs alone | disagreements | undecided rows cpsat, highs | patterns in neither file')
for (n, p, q) in sorted(groups, key=lambda t: (t[0], t[1] ** t[0] * t[2])):
    g = groups[n, p, q]
    C, cpart = g.get(('multi', 'cpsat'), ({}, None)); H, hpart = g.get(('multi', 'highs'), ({}, None))
    dec = {}; both = conly = honly = dis = 0
    for key in set(C) | set(H):
        dc = key in C and decided(C[key]); dh = key in H and decided(H[key])
        if dc and dh:
            both += 1
            if C[key]['min'] != H[key]['min']: dis += 1
            dec[key] = C[key]['min']
        elif dc: conly += 1; dec[key] = C[key]['min']
        elif dh: honly += 1; dec[key] = H[key]['min']
    uc = sum(1 for r in C.values() if not decided(r)); uh = sum(1 for r in H.values() if not decided(r))
    npat = 2 ** n * 2 ** (n + 1)
    print(f"{n} {p} {q} {p**n*q} | {len(C)} ({cpart}) | {len(H)} ({hpart}) | {len(dec)} | {both} | {conly} | {honly} | {dis} | {uc}, {uh} | {npat - len(set(C) | set(H))}")
    T['dec'] += len(dec); T['both'] += both; T['conly'] += conly; T['honly'] += honly; T['dis'] += dis
    for (E, F), m in dec.items():
        table[n, p, q, E, F] = m
        if 0 not in F:
            T['thm', m == thm(p, q, E, F)] += 1
            T['U', m >= p ** len((E | F))] += 1
        elif F == frozenset(range(n + 1)):
            T['full', m == q * p ** len(E)] += 1
        else:
            T['first', m == first_formula(p, q, n, E, F)] += 1
            T['rule', m == rule(p, q, n, E, F)] += 1
print()
print('decided', T['dec'], '| by both', T['both'], '| cpsat alone', T['conly'], '| highs alone', T['honly'], '| the two solvers disagree on', T['dis'])
for k, lab in (('thm', 'section 2 formula'), ('U', 'p^|E u F| bound'), ('full', 'F all levels: q p^e'), ('rule', 'rule of section 3'), ('first', 'first formula')):
    print(f"{lab}: right on {T[k, True]} of {T[k, True] + T[k, False]}")

# an empty level inserted: pattern (E, F) of p^n q, a new level j in 1..n+1 that is in neither set, levels >= j move up
def insert(E, F, j):
    sh = lambda a: a + 1 if a >= j else a
    return frozenset(sh(a) for a in E), frozenset(0 if a == 0 else sh(a) for a in F)
m5 = collections.Counter(); m5pat = collections.Counter()
for (n, p, q, E, F), v in table.items():
    for j in range(1, n + 2):
        E2, F2 = insert(E, F, j)
        w = table.get((n + 1, p, q, E2, F2))
        if w is not None:
            m5[0 in F, w == v] += 1
print(f"empty level inserted (pairs of decided patterns, one for each place of insertion): 0 not in F: same {m5[False, True]} of {m5[False, True] + m5[False, False]}; 0 in F: different {m5[True, False]} of {m5[True, True] + m5[True, False]}")

# item (3): decided patterns with 0 in F in which some level a of F minus E has a level b, 1 <= b < a, missing from F
cnt = 0; bad = 0; ratios = collections.Counter(); least = None; byq = collections.Counter(); ismin = collections.Counter()
per_group = collections.Counter()
for (n, p, q, E, F), m in sorted(table.items(), key=lambda t: (t[0][0], t[0][1], t[0][2], sorted(t[0][3]), sorted(t[0][4]))):
    if 0 not in F: continue
    if not any(a >= 1 and a not in E and any(b not in F for b in range(1, a)) for a in F): continue
    cnt += 1; per_group[n, p, q] += 1
    e = len(E); bound = p ** e * (p + q)
    if m < bound: bad += 1
    from fractions import Fraction
    r = Fraction(m, bound)
    ratios[(p, q, r)] += 1
    ismin[m == q * p ** (e + 1)] += 1
    if m < q * p ** (e + 1): byq['below q p^(e+1)'] += 1
    if m != rule(p, q, n, E, F): byq['not the rule'] += 1
    if least is None or r < least[0]: least = (r, n, p, q, sorted(E), sorted(F), m, bound)
print()
print('item (3): decided patterns with 0 in F and a level of F minus E with a lower level (>= 1) missing from F:', cnt)
print('   by group (n, p, q):', dict(per_group))
print('   minimum below p^e (p + q):', bad)
print('   minimum below q p^(e+1):', byq['below q p^(e+1)'], '| minimum equal to q p^(e+1):', ismin[True], '| larger:', ismin[False], '| minimum not what the rule gives:', byq['not the rule'])
print('   least ratio minimum / (p^e (p + q)):', least)
import itertools
for (p, q) in sorted({(k[0], k[1]) for k in ratios}):
    rs = sorted((r, c) for (pp, qq, r), c in ratios.items() if (pp, qq) == (p, q))
    print(f"   p = {p}, q = {q}: least ratio {rs[0][0]} ({rs[0][1]} patterns); q p / (p + q) = {Fraction(q * p, p + q)}; ratios: " + ', '.join(f"{r} x{c}" for r, c in rs))

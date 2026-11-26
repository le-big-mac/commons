"""Referee's recount from the author's JSON-line files (own code; formulas from pat.py, written from the note's words).
usage: recount.py [cutoff HH:MM:SS]
With a cutoff, rows of the files still being written are kept only if they were complete by that time
(start of each process taken from the time of its .err file; row time = start + running sum of 'seconds')."""
import sys, json, os, glob, collections, datetime
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *

od = '/home/agent3/minsize/out'
PAIRS = [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3)]
cutoff = None
if len(sys.argv) > 1:
    h, m, s = map(int, sys.argv[1].split(':')); cutoff = h * 3600 + m * 60 + s


def load(n, p, q, kind, solver):
    for ext in ('', '.part'):
        f = f'{od}/n{n}-p{p}-q{q}-{kind}-{solver}.jsonl{ext}'
        if os.path.exists(f):
            rows = []
            start = None
            if ext and cutoff is not None:
                st = os.stat(f + '.err' if not os.path.exists(f'{od}/n{n}-p{p}-q{q}-{kind}-{solver}.jsonl.err') else f'{od}/n{n}-p{p}-q{q}-{kind}-{solver}.jsonl.err')
                d = datetime.datetime.utcfromtimestamp(st.st_mtime); start = d.hour * 3600 + d.minute * 60 + d.second + d.microsecond / 1e6
            t = 0.0
            for l in open(f):
                if not l.startswith('{'): continue
                try: r = json.loads(l)
                except Exception: continue
                t += r['seconds']
                if start is not None and start + t > cutoff: break
                rows.append(r)
            return {(tuple(r['E']), tuple(r['F'])): r for r in rows}, bool(ext)
    return {}, None


def decided(r): return r is not None and not r['undecided'] and r['min'] is not None


tot = collections.Counter(); table = {}; wrong = []; one_solver = []
print('n p q order | patterns | decided | by both | thm right | F all right | first formula M4 right | rule right | sets tried | patterns with a set | set = multiset minimum')
for n in (2, 3, 4):
    for p, q in PAIRS:
        C, cp = load(n, p, q, 'multi', 'cpsat'); H, hp = load(n, p, q, 'multi', 'highs'); St, sp = load(n, p, q, 'set', 'cpsat')
        if not C and not H: continue
        dec = {}; both = 0; disagree = 0
        for k in set(C) | set(H):
            vals = {name: T[k]['min'] for name, T in (('cpsat', C), ('highs', H)) if decided(T.get(k))}
            if not vals: continue
            if len(set(vals.values())) != 1: disagree += 1; wrong.append(('SOLVERS DISAGREE', n, p, q, k, vals)); continue
            dec[k] = list(vals.values())[0]
            if len(vals) == 2: both += 1
            else: one_solver.append((n, p, q, k, list(vals)[0], dec[k]))
        c = collections.Counter()
        for (E, F), m in dec.items():
            table[n, p, q, E, F] = m
            if 0 not in F:
                ok = (m == thm_value(p, q, E, F)); c['thm', ok] += 1
                c['U', m >= p ** len(set(E) | set(F))] += 1
                if not ok: wrong.append(('THEOREM', n, p, q, E, F, m, thm_value(p, q, E, F)))
            else:
                v, x = rule_value(p, q, n, E, F)
                if x is None:
                    c['all', m == v] += 1
                    if m != v: wrong.append(('F ALL', n, p, q, E, F, m, v))
                else:
                    c['rule', m == v] += 1
                    if m != v: wrong.append(('RULE', n, p, q, E, F, m, v))
                    # the first formula (M4 of the first sheet): x = 0 only if k' = 0 or (a0 in E and p >= 3)
                    a0 = min(a for a in range(1, n + 1) if a not in F); k1 = len([a for a in F if a > a0 and a not in E])
                    x4 = 0 if (k1 == 0 or (a0 in E and p >= 3)) else 1
                    c['m4', m == q * p ** len(E) * (p ** k1 + x4)] += 1
        sets_tried = len(St)
        sets_exist = [k for k, r in St.items() if decided(r)]
        sets_none = [k for k, r in St.items() if (not r['undecided']) and r['min'] is None]
        sets_und = [k for k, r in St.items() if r['undecided']]
        same = sum(1 for k in sets_exist if k in dec and St[k]['min'] == dec[k]); bigger = sum(1 for k in sets_exist if k in dec and St[k]['min'] > dec[k])
        smaller = sum(1 for k in sets_exist if k in dec and St[k]['min'] < dec[k]); nodec = sum(1 for k in sets_exist if k not in dec)
        f = lambda key: f"{c[key, True]} of {c[key, True] + c[key, False]}"
        print(f"{n} {p} {q} {p ** n * q} | {2 ** n * 2 ** (n + 1)} | {len(dec)} | {both} | {f('thm')} | {f('all')} | {f('m4')} | {f('rule')} | {sets_tried} | {len(sets_exist)} "
              f"(none: {len(sets_none)}, undecided: {len(sets_und)}) | {same} of {len(sets_exist)} (larger {bigger}, smaller {smaller}, multiset undecided {nodec})"
              + (f"  [files still being written: cpsat {cp}, highs {hp}]" if cp or hp else ''))
        for k, v in c.items(): tot[k] += v
        tot['dec'] += len(dec); tot['both'] += both; tot['sets_exist'] += len(sets_exist); tot['sets_same'] += same; tot['sets_bigger'] += bigger; tot['sets_tried'] += sets_tried
        tot['sets_none'] += len(sets_none)
        # S2, S3, S4 of the first sheet
        for k in sets_exist:
            E, F = k
            if k in dec:
                if n not in E and n not in F: tot['S2', St[k]['min'] == dec[k]] += 1
                if 0 not in F and (n in E or n in F): tot['S4cand', St[k]['min'] > dec[k]] += 1
                if 0 not in F: tot['S4any', St[k]['min'] > dec[k]] += 1
        for k, r in St.items():
            E, F = k
            if not r['undecided'] and 0 not in F and set(range(1, n + 1)) <= set(F) and set(E) != set(range(1, n + 1)): tot['S3', r['min'] is None] += 1
            # the note's sentence in section 4: 0 not in F and every level 1..n in F
            if not r['undecided'] and 0 not in F and set(range(1, n + 1)) <= set(F):
                tot['sec4', set(E) == set(range(1, n + 1)), r['min'] is None] += 1
f = lambda key: f"{tot[key, True]} of {tot[key, True] + tot[key, False]}"
print(f"\ntotals: decided {tot['dec']}; by both solvers {tot['both']}; theorem formula {f('thm')}; p^|E u F| bound {f('U')}; F all {f('all')}; first formula {f('m4')}; rule {f('rule')}")
print(f"sets: tried {tot['sets_tried']}, patterns with a set {tot['sets_exist']}, with none {tot['sets_none']}; same minimum as multisets {tot['sets_same']}, larger {tot['sets_bigger']}")
print(f"S2 (level n in neither; set = multiset): {f('S2')};  S3 (no set): {f('S3')};  S4 candidates with set > multiset: {tot['S4cand', True]} of {tot['S4cand', True] + tot['S4cand', False]};"
      f" any 0-not-in-F pattern with set > multiset: {tot['S4any', True]} of {tot['S4any', True] + tot['S4any', False]}")
print('section 4 sentence (0 not in F, F contains 1..n): E all levels & no set / E all levels & set / E not all & no set / E not all & set:',
      tot['sec4', True, True], tot['sec4', True, False], tot['sec4', False, True], tot['sec4', False, False])
print(f'decided by one solver only: {len(one_solver)}:', collections.Counter((n, p, q, s) for n, p, q, k, s, m in one_solver))
print('not as the formulas say:', wrong if wrong else 'none')
# M5: insert a level in neither E nor F
def insert(E, F, j):
    sh = lambda a: a + 1 if a >= j else a
    return tuple(sorted(sh(a) for a in E)), tuple(sorted((0 if a == 0 else sh(a)) for a in F))
m5 = collections.Counter(); m5pat = collections.Counter(); m5ex = []
for (n, p, q, E, F), v in table.items():
    res = []
    for j in range(1, n + 2):
        w = table.get((n + 1, p, q) + insert(E, F, j))
        if w is not None:
            m5[0 in F, w == v] += 1; res.append(w == v)
            if 0 not in F and w != v: m5ex.append((n, p, q, E, F, j, v, w))
    if res: m5pat[0 in F, all(res)] += 1
print(f"M5, comparisons (pattern, place of insertion): 0 not in F: same {m5[False, True]}, different {m5[False, False]}; 0 in F: same {m5[True, True]}, different {m5[True, False]}")
print(f"M5, patterns: 0 not in F: all insertions same {m5pat[False, True]}, some different {m5pat[False, False]}; 0 in F: all same {m5pat[True, True]}, some different {m5pat[True, False]}")
# M6: same polynomial for the six pairs when 0 not in F
poly = collections.defaultdict(dict)
for (n, p, q, E, F), v in table.items():
    if 0 not in F: poly[n, E, F][p, q] = (v, thm_value(p, q, E, F))
allsix = sum(1 for k, d in poly.items() if len(d) == 6);
print(f"M6a: patterns (n, E, F) with 0 not in F: {len(poly)}; decided for all six pairs of primes: {allsix}; for fewer: {len(poly) - allsix};"
      f" every decided value equals p^e(p^k+q) or p^e: {all(v == t for d in poly.values() for v, t in d.values())}")
# M6b: p = 2 differs from p >= 3 somewhere when 0 in F: same (n, E, F), compare the value as a formula
diff = []
for (n, p, q, E, F), v in table.items():
    if 0 in F and p == 2 and set(F) != set(range(n + 1)):
        for (p2, q2) in PAIRS:
            if p2 >= 3 and (n, p2, q2, E, F) in table:
                x2 = table[n, p2, q2, E, F]; _, xr2 = rule_value(p2, q2, n, E, F); _, xr = rule_value(p, q, n, E, F)
                e = len(E); a0 = min(a for a in range(1, n + 1) if a not in F); k1 = len([a for a in F if a > a0 and a not in E])
                xa = v // (q * p ** e) - p ** k1; xb = x2 // (q2 * p2 ** e) - p2 ** k1
                if xa != xb: diff.append((n, E, F, (p, q, v, xa), (p2, q2, x2, xb)))
print(f"M6b: (pattern, p=2 pair, p>=3 pair) where the summand x differs: {len(diff)}; distinct patterns: {len(set((d[0], d[1], d[2]) for d in diff))}; e.g. {diff[:2]}")

"""Fourth pass: "Two programs that search for the fewest marks agreed with the guess on all 637 patterns that they could settle.
... wrong on 39 patterns of 628".  How many of these patterns did both programs settle, and how many one alone?
Read from the two programs' own result files (one line of JSON for each pattern), counted here afresh; the formulas for the guesses
are written here from the page's rule and the first sealed sheet, not taken from the author's summary program.
usage: settled.py OUT_DIR"""
import sys, os, json, collections
od = sys.argv[1]
def load(n, p, q, solver):
    for ext in ('', '.part'):
        f = f'{od}/n{n}-p{p}-q{q}-multi-{solver}.jsonl{ext}'
        if os.path.exists(f):
            return {(tuple(r['E']), tuple(r['F'])): r for r in (json.loads(l) for l in open(f) if l.startswith('{'))}
    return {}
ok = lambda T, k: k in T and not T[k]['undecided'] and T[k]['min'] is not None
def first_formula(p, q, E, F):                 # no balance at q: p^e, or p^e (p^k + q) with k short powers
    e = len(E); k = len([a for a in F if a not in E]); return p ** e * (p ** k + q) if k else p ** e
def first_guess_second(p, q, n, E, F):         # the guess that failed (sheet M4): x = 0 if k' = 0, or if a0 in E and p >= 3; else 1
    e = len(E); a0 = min(a for a in range(1, n + 1) if a not in F); k2 = len([a for a in F if a > a0 and a not in E])
    x = 0 if k2 == 0 else (0 if (a0 in E and p >= 3) else 1); return q * p ** e * (p ** k2 + x)
tot = collections.Counter(); groups = 0
for n in (2, 3, 4):
    for p, q in [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3)]:
        C, H = load(n, p, q, 'cpsat'), load(n, p, q, 'highs')
        if not C and not H: continue
        groups += 1
        for k in set(C) | set(H):
            vals = [T[k]['min'] for T in (C, H) if ok(T, k)]
            if not vals: continue
            assert len(set(vals)) == 1                       # where both settled a pattern they give the same number
            E, F = k; m = vals[0]; who = 'both' if (ok(C, k) and ok(H, k)) else ('first program alone' if ok(C, k) else 'second program alone')
            if 0 not in F:                                   # the first formula's patterns (no balance at q)
                tot['first', who] += 1; tot['first', 'agree' if m == first_formula(p, q, E, F) else 'differ'] += 1
            else:                                            # the second formula's patterns (balance at q)
                tot['second', who] += 1
                if set(F) == set(range(n + 1)): tot['second, every product: guess right' if m == q * p ** len(E) else 'second, every product: guess wrong'] += 1
                else: tot['second, a product missing: guess right' if m == first_guess_second(p, q, n, E, F) else 'second, a product missing: guess wrong'] += 1
            tot['all', who] += 1
print('clocks with result files:', groups)
for k in sorted(tot, key=str): print(f'   {k}: {tot[k]}')
f = sum(v for (a, b), v in ((k, v) for k, v in tot.items() if isinstance(k, tuple)) if a == 'first' and b in ('both', 'first program alone', 'second program alone'))
s = sum(v for (a, b), v in ((k, v) for k, v in tot.items() if isinstance(k, tuple)) if a == 'second')
print(f'patterns of the first formula settled by at least one program: {f}; of the second: {s}; together {f + s}')

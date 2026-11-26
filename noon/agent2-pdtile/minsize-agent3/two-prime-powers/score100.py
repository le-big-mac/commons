"""Score the sheet for Z_100.   usage: score100.py out/z100-0.jsonl out/z100-1.jsonl out/z100-2.jsonl out/z36-0.jsonl out/z36-1.jsonl out/z36-2.jsonl [out/z36-again.jsonl]"""
import sys, json, collections, itertools
def rule(p, q, n, E, F):
    e = len(E)
    if 0 not in F:
        k = len([a for a in F if a not in E]); return p ** e * (p ** k + q) if k else p ** e
    if set(F) == set(range(n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F); G = sorted(a for a in F if a > a0 and a not in E)
    x = 0 if (not G or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or (a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, G[0])))) else 1
    return q * p ** e * (p ** len(G) + x)
def z20(D): return rule(2, 5, 2, [a for a in (1, 2) if 2 ** a in D], ([0] if 5 in D else []) + [a for a in (1, 2) if 2 ** a * 5 in D])
def z50(D): return rule(5, 2, 2, [a for a in (1, 2) if 5 ** a in D], ([0] if 2 in D else []) + [a for a in (1, 2) if 5 ** a * 2 in D])
def load(files):
    R = {}
    for f in files:
        for l in open(f):
            if l.startswith('{'):
                r = json.loads(l); k = frozenset(r['D'])
                if k not in R or (r['proved'] and not R[k]['proved']): R[k] = r
    return R
f100 = [f for f in sys.argv[1:] if 'z100' in f]; f36 = [f for f in sys.argv[1:] if 'z36' in f]
R = load(f100); S = load(f36)
dec = {D: r['min'] for D, r in R.items() if r['min'] is not None and r['proved']}; dec36 = {D: r['min'] for D, r in S.items() if r['min'] is not None and r['proved']}
print(len(R), 'patterns of Z_100 run;', len(dec), 'decided;', len(R) - len(dec), 'not decided;   Z_36:', len(dec36), 'decided of', len(S))
ep = lambda D: len(D & {2, 4}); eq = lambda D: len(D & {5, 25})
print('Y0 (code check) failures:', [(sorted(D), m) for D, m in dec.items() if m % (2 ** ep(D) * 5 ** eq(D)) or m < z20(D) or m < z50(D)])
divs = [d for d in range(1, 101) if 100 % d == 0]
def is_up(D): return all((e in D) for d in D for e in divs if e % d == 0)
def guess(D):
    comp = [c for c in divs if c not in D]; mx = [c for c in comp if not any(e != c and e % c == 0 for e in comp)]; return sum(100 // c for c in mx)
ups = [(sorted(D), m, guess(D)) for D, m in dec.items() if is_up(D)]
print('Y1: up-set patterns decided:', len(ups), 'of', sum(1 for D in R if is_up(D)), '; equal to the sum over maximal non-divisors:', sum(1 for _, m, g in ups if m == g), '; others:', [u for u in ups if u[1] != u[2]])
a = [(sorted(D), m, z20(D)) for D, m in dec.items() if not (D & {25, 50, 100})]; b = [(sorted(D), m, z50(D)) for D, m in dec.items() if not (D & {4, 20, 100})]
print('Y2: inside the divisors of 20:', len(a), 'decided, equal to the Z_20 rule in', sum(1 for _, m, v in a if m == v), '; inside the divisors of 50:', len(b), 'decided, equal to the Z_50 rule in', sum(1 for _, m, v in b if m == v), '; others:', [t for t in a + b if t[1] != t[2]][:8])
tr = lambda D: frozenset({3: 5, 9: 25, 6: 10, 12: 20, 18: 50, 36: 100}.get(d, d) for d in D)     # a Z_36 pattern as a Z_100 pattern
both = [(D, dec36[D], dec[tr(D)]) for D in dec36 if tr(D) in dec]
eqp = same = 0
for (D1, m1, n1), (D2, m2, n2) in itertools.combinations(both, 2):
    if m1 == m2: eqp += 1; same += (n1 == n2)
print(f'Y3: patterns decided on both: {len(both)}; pairs with equal least size on Z_36: {eqp}; of these equal on Z_100 too: {same} ({100 * same / max(eqp, 1):.1f}%)')
mx = max(dec.values()); print('Y4: largest decided least size', mx, 'at', [sorted(D) for D, m in dec.items() if m == mx][:6])
print('Y5: decided', len(dec), 'of', len(R))
vals = collections.Counter(dec.values()); print('distinct least sizes:', len(vals), sorted(vals.items()))

"""Score the sheet for Z_36.   usage: score36.py out/z36-0.jsonl out/z36-1.jsonl out/z36-2.jsonl"""
import sys, json, collections
def rule(p, q, n, E, F):
    e = len(E)
    if 0 not in F:
        k = len([a for a in F if a not in E]); return p ** e * (p ** k + q) if k else p ** e
    if set(F) == set(range(n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F); G = sorted(a for a in F if a > a0 and a not in E)
    x = 0 if (not G or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or (a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, G[0])))) else 1
    return q * p ** e * (p ** len(G) + x)
def z12(D): return rule(2, 3, 2, [a for a in (1, 2) if 2 ** a in D], ([0] if 3 in D else []) + [a for a in (1, 2) if 2 ** a * 3 in D])
def z18(D): return rule(3, 2, 2, [a for a in (1, 2) if 3 ** a in D], ([0] if 2 in D else []) + [a for a in (1, 2) if 3 ** a * 2 in D])
R = {}
for f in sys.argv[1:]:
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); R[frozenset(r['D'])] = r
dec = {D: r['min'] for D, r in R.items() if r['min'] is not None and r['proved']}
und = [sorted(D) for D, r in R.items() if not (r['min'] is not None and r['proved'])]
print(len(R), 'patterns run;', len(dec), 'decided (least size proved);', len(und), 'not decided:', und[:12])
none = [sorted(D) for D, r in R.items() if r['min'] is None and r['proved']]; print('proved to have no multiset within the cap:', none)
ep = lambda D: len(D & {2, 4}); eq = lambda D: len(D & {3, 9}); mixed = {6, 12, 18, 36}
q0 = [(sorted(D), m) for D, m in dec.items() if m % (2 ** ep(D) * 3 ** eq(D)) or m < z12(D) or m < z18(D)]
print('Q0 (code check): failures', q0)
print('Q1: patterns with a witness', sum(1 for r in R.values() if r['min'] is not None), 'of', len(R))
q2 = [(sorted(D), m, 2 ** ep(D) * 3 ** eq(D)) for D, m in dec.items() if not (D & mixed)]; print('Q2: no mixed divisor:', len(q2), 'patterns; equal to 2^e_p 3^e_q in', sum(1 for _, m, v in q2 if m == v), '; others:', [t for t in q2 if t[1] != t[2]])
print('Q3: min({6,12,18,36}) =', dec.get(frozenset({6, 12, 18, 36})), '   Q4: min({36}) =', dec.get(frozenset({36})))
a = [(sorted(D), m, z12(D)) for D, m in dec.items() if not (D & {9, 18, 36})]; b = [(sorted(D), m, z18(D)) for D, m in dec.items() if not (D & {4, 12, 36})]
print('Q5: inside the divisors of 12:', len(a), 'patterns, equal to the Z_12 rule in', sum(1 for _, m, v in a if m == v), '; others:', [t for t in a if t[1] != t[2]])
print('    inside the divisors of 18:', len(b), 'patterns, equal to the Z_18 rule in', sum(1 for _, m, v in b if m == v), '; others:', [t for t in b if t[1] != t[2]])
vals = collections.Counter(dec.values()); print('Q6: distinct minima:', len(vals), sorted(vals.items()))
print('Q7: largest minimum', max(dec.values()), 'at', [sorted(D) for D, m in dec.items() if m == max(dec.values())])

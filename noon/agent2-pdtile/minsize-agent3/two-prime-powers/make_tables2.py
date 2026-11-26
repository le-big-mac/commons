"""The tables of the note after its referee's report: for each pattern of Z_M (M = P^2 Q^2) the smallest multiset known with
exactly that pattern and who proved it least.  Three sources:
  G  my solver gen.py (CP-SAT, exact integers): out/z{M}-*.jsonl, out/z36-again.jsonl
  R  the referee's programme (cuboid forms, HiGHS), 60 s a pattern, run by the referee: referee/two-powers/out/retable-{M}-*.jsonl
  R+ the same programme run by me afterwards with a longer limit, keeping the multisets: out2/z{M}-*.jsonl
Every multiset used is checked here again by exact polynomial division.  Writes the table, a file of witnesses, and prints counts.
usage: make_tables2.py M P Q OUT.md WITNESSES.jsonl"""
import sys, json, glob
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
M, P, Q, outp, witp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
divs = [d for d in range(1, M + 1) if M % d == 0]; dv = divs[1:]
PHI = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in dv}
def exact_pattern(v):
    A = Poly(sum(int(w) * X**i for i, w in enumerate(v)), X, domain=ZZ)
    return [d for d in dv if A.rem(PHI[d]).is_zero]
def vec(witness):
    v = [0] * M
    for t in witness.split():
        if '^' in t: a, w = t.split('^'); v[int(a)] += int(w)
        else: v[int(t)] += 1
    return v
G = {}
for f in sorted(glob.glob(f'out/z{M}-[0-9].jsonl')) + (['out/z36-again.jsonl'] if M == 36 else []):
    for l in open(f):
        if l.startswith('{'):
            r = json.loads(l); k = frozenset(r['D'])
            if k not in G or (r['proved'] and not G[k]['proved']) or (G[k]['min'] is None and r['min'] is not None): G[k] = r
R = {}
for f in sorted(glob.glob(f'referee/two-powers/out/retable-{M}-*.jsonl')):
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); R[frozenset(r['D'])] = r
RP = {}
for f in sorted(glob.glob(f'out2/z{M}-*.jsonl')):
    for l in open(f):
        if l.startswith('{'):
            r = json.loads(l); k = frozenset(r['D'])
            if k not in RP or (r['status'] == 'optimal' and RP[k]['status'] != 'optimal'): RP[k] = r
CP = set()                                                     # Z_36: the referee's CP-SAT run proved nothing smaller exists
if M == 36:
    for f in glob.glob('referee/two-powers/out/cpsat*.jsonl'):
        for l in open(f):
            if l.startswith('{'):
                r = json.loads(l)
                if r['cpsat_status'] == 'infeasible': CP.add((frozenset(r['D']), r['author_value']))
def is_up(D): return all((e in D) for d in D for e in divs if e % d == 0)
def rule(p, q, n, E, F):                                       # the theorem for Z_{p^n q} (minsize.pdf, Theorem 1), as in score100.py
    e = len(E)
    if 0 not in F:
        k = len([a for a in F if a not in E]); return p ** e * (p ** k + q) if k else p ** e
    if set(F) == set(range(n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F); G = sorted(a for a in F if a > a0 and a not in E)
    x = 0 if (not G or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or (a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, G[0])))) else 1
    return q * p ** e * (p ** len(G) + x)
def by_theorem(D):
    """the least size where a theorem gives it: Theorem S for an up-set; the theorem for Z_{p^n q} for a pattern inside the divisors of P^2 Q or of P Q^2"""
    out = []
    if is_up(D): out.append(('S', sum(M // c for c in corners(D))))
    for p, q in ((P, Q), (Q, P)):
        if all((p * p * q) % d == 0 for d in D):
            out.append(('N', rule(p, q, 2, [a for a in (1, 2) if p ** a in D], ([0] if q in D else []) + [a for a in (1, 2) if p ** a * q in D])))
    assert len(set(v for _, v in out)) <= 1, (sorted(D), out)
    return (''.join(sorted(set(t for t, _ in out))), out[0][1]) if out else ('', None)
def corners(D):
    comp = [c for c in divs if c not in D]; return [c for c in comp if not any(e != c and e % c == 0 for e in comp)]
def largest_up_inside(D): return frozenset(d for d in D if all((e in D) for e in divs if e % d == 0))
rows = []; wit = []
assert len(G) == len(R) == 2 ** len(dv)
for D in sorted(G, key=lambda D: (len(D), sorted(D))):
    g, r, rp = G[D], R[D], RP.get(D)
    proved = {}                                                  # source -> proved least value
    if g['proved'] and g['min'] is not None: proved['G'] = g['min']
    if r['referee_status'] == 'optimal': proved['R'] = r['referee_least']
    if rp and rp['status'] == 'optimal': proved['R+'] = rp['size']
    found = []                                                   # (size, multiset, source)
    if g['min'] is not None: found.append((g['min'], vec(g['witness']), 'G'))
    if rp and rp['A'] is not None: found.append((rp['size'], rp['A'], 'R+'))
    for sz, v, src in found: assert sum(v) == sz and exact_pattern(v) == sorted(D), (sorted(D), src)
    known_sizes = [f[0] for f in found] + ([r['referee_least']] if r['referee_least'] is not None else [])
    best = min(known_sizes) if known_sizes else None
    assert len(set(proved.values())) <= 1, (sorted(D), proved)
    if proved:
        pv = next(iter(proved.values())); assert pv == best, (sorted(D), proved, known_sizes)
    w = min(found, key=lambda t: t[0]) if found else None
    has_wit = w is not None and w[0] == best
    by = [s for s in ('G', 'R', 'R+') if s in proved]
    if 'R+' in by and 'R' in by: by.remove('R+')                 # the longer run only repeats the shorter one there
    if M == 36 and (D, best) in CP and 'G' not in by: by.append('C')
    up = is_up(D); U = largest_up_inside(D); lb = sum(M // c for c in corners(U))
    th = by_theorem(D)
    if th[1] is not None and proved: assert th[1] == best, (sorted(D), th, best)          # a programme's proved value against the theorem's
    if th[1] is not None: assert best is None or best >= th[1], (sorted(D), th, best)
    rows.append((sorted(D), best, by, up, lb, has_wit, g['min'], th))
    if has_wit: wit.append(dict(M=M, D=sorted(D), size=best, proved_least_by=by, multiset=' '.join(f'{i}^{c}' if c > 1 else str(i) for i, c in enumerate(w[1]) if c)))
with open(outp, 'w') as f:
    f.write(f"# Z_{M} = {P}²·{Q}²: the smallest multiset known for each of the {len(rows)} patterns\n\n"
            "*Made by `make_tables2.py`. 'size' is the size of the smallest multiset known with exactly that pattern. 'proved least by' names the programmes that proved that nothing smaller exists: "
            "**G** is my solver `gen.py` (CP-SAT, exact integers; 60 seconds a pattern" + (", 400 for sixteen patterns" if M == 36 else "") + "); "
            "**R** is the referee's programme (`referee/milp.py`: another formulation, solved by HiGHS, whose proofs of optimality are in floating point; run by the referee, " + ("with a limit of 120 seconds a pattern, of which none took more than 44); " if M == 36 else "60 seconds a pattern); ")
            + ("**C** marks a pattern where the referee also gave its formulation to CP-SAT, which proved in exact integers that nothing smaller exists; " if M == 36 else
               "**R+** is the same programme run by me afterwards with 25 minutes a pattern (`finish100.py`); ")
            + "an empty cell means that no programme proved the size least. " + "'by theorem' gives a value from a theorem where there is one: (S) the least size by Theorem S of the note, for an up-set; (N) for a pattern that uses only the divisors of " + f"{P}²·{Q} or only those of {P}·{Q}²" + ", the lower bound that the theorem for Z_{pⁿq} of `minsize.pdf` gives by reduction, which is the least size because a multiset of that size is on file in every such row; the program stops if a smaller multiset turns up or if a value proved by a programme differs from it. 'up-set' marks the patterns closed under multiples. "
            "'bound' is the lower bound of Corollary P (the sum of M/c over the corners of the largest up-set inside the pattern), which for an up-set is the value of Corollary U. "
            f"The multisets themselves are in `{witp.split('/')[-1]}`, each checked by exact division.*\n\n"
            "| pattern (the d with Φ_d dividing) | size | proved least by | by theorem | up-set | bound |\n|---|---|---|---|---|---|\n")
    for D, b, by, up, lb, hw, gm, th in rows:
        f.write(f"| {', '.join(map(str, D)) if D else '(none)'} | {b if b is not None else 'none found'}{'' if hw or b is None else ' (multiset not kept)'} | {', '.join(by)} | {(str(th[1]) + ' (' + th[0] + ')') if th[1] is not None else ''} | {'yes' if up else ''} | {lb} |\n")
with open(witp, 'w') as f:
    for w in wit: f.write(json.dumps(w) + '\n')
json.dump([dict(D=r[0], size=r[1], by=r[2], up=r[3], bound=r[4], theorem=r[7][0], theorem_value=r[7][1]) for r in rows], open(outp.replace('table-', 'rows-').replace('.new', '').replace('.md', '.json'), 'w'))
dec = [r for r in rows if r[2]]; ups = [r for r in rows if r[3]]; upd = [r for r in ups if r[2]]
def inside(D, m): return all(m % d == 0 for d in D)
subs = {}
for name, mm in (('p2q', P * P * Q), ('pq2', P * Q * Q)):
    sub = [r for r in rows if inside(r[0], mm)]; subs[name] = dict(patterns=len(sub), decided=sum(1 for r in sub if r[2]))
print(json.dumps(dict(M=M, patterns=len(rows), decided=len(dec), decided_G=sum(1 for r in rows if 'G' in r[2]), decided_R=sum(1 for r in rows if 'R' in r[2]),
                      decided_only_Rplus=sum(1 for r in rows if r[2] == ['R+']), decided_not_G=sum(1 for r in rows if r[2] and 'G' not in r[2]),
                      decided_only_HiGHS=sum(1 for r in rows if r[2] and 'G' not in r[2] and 'C' not in r[2]),
                      found=sum(1 for r in rows if r[1] is not None), with_multiset=sum(1 for r in rows if r[5]), upsets=len(ups), upsets_decided=len(upd),
                      upsets_equal=sum(1 for r in upd if r[1] == r[4]), below_bound=sum(1 for r in rows if r[1] is not None and r[1] < r[4]),
                      equal_bound_not_up=sum(1 for r in rows if not r[3] and r[1] == r[4]), equal_bound_not_up_decided=sum(1 for r in dec if not r[3] and r[1] == r[4]),
                      distinct=len(set(r[1] for r in dec)), largest=max(r[1] for r in dec), largest_at=[r[0] for r in dec if r[1] == max(x[1] for x in dec)],
                      by_theorem=sum(1 for r in rows if r[7][1] is not None), by_theorem_not_by_programme=[(r[0], r[1], r[7][1]) for r in rows if r[7][1] is not None and not r[2]],
                      decided_or_theorem=sum(1 for r in rows if r[2] or (r[7][1] is not None and r[1] == r[7][1])),
                      better_than_G_decided=sum(1 for r in rows if r[2] and r[6] is not None and r[1] < r[6]), G_none_decided=sum(1 for r in rows if r[2] and r[6] is None),
                      better_than_G_undecided=sum(1 for r in rows if not r[2] and (r[6] is None or r[1] < r[6])),
                      undecided=[(r[0], r[1]) for r in rows if not r[2]], sub=subs)))

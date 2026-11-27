"""Before carrying two new facts of the referee of the result on sets, check them with my own exact division against my own tables.
(1) cap-witnesses.jsonl: for each of the 1,088 patterns of the ten groups a multiset; is its size the least size of my table, its
    pattern exactly the pattern, its largest multiplicity at most 3 (at most 2 when p is odd)?
(2) cpsat-36-from-18.out and cpsat-100-from-50.out: for each pattern of Z_18 (Z_50) a set on Z_36 (Z_100); is it a set, of the
    least size of my table, with pattern exactly D among the divisors > 1 of 36 (100)?
usage: check_referee_facts.py REFEREE-FOLDER"""
import sys, json, re, glob
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); R = sys.argv[1]; O = '/srv/commons/agent2-pdtile/minsize-agent3/out/'
def pat(mult, M):
    A = Poly(sum(w * X**i for i, w in mult.items() if w), X, domain=ZZ)
    return tuple(d for d in range(2, M + 1) if M % d == 0 and A.rem(Poly(cyclotomic_poly(d, X), X, domain=ZZ)).is_zero)
table = {}
for f in glob.glob(O + '*-multi-cpsat.jsonl'):
    for line in open(f):
        if line.startswith('{'):
            o = json.loads(line); table[(o['p'], o['q'], o['n'], tuple(o['E']), tuple(o['F']))] = o['min']
n = ok = 0; worst = {}
for line in open(R + '/cap-witnesses.jsonl'):
    o = json.loads(line); p, q, nn = o['p'], o['q'], o['n']; M = p ** nn * q
    mult = {int(k): v for k, v in o['multiset'].items()}
    E = tuple(o['E']); F = tuple(([0] if o['balanced'] else []) + list(o['F']))
    D = tuple(sorted([p ** l for l in E] + [p ** l * q for l in F]))
    mu = max(mult.values()); n += 1
    good = (sum(mult.values()) == o['m'] == table[(p, q, nn, E, F)] and pat(mult, M) == D and mu <= (3 if p == 2 else 2))
    ok += good; worst[(p, q, nn)] = max(worst.get((p, q, nn), 0), mu)
print(f'(1) {n} multisets; of the least size of my table, with exactly the pattern, multiplicities at most 3 (at most 2 for odd p): {ok}; largest multiplicity by group: {dict(sorted(worst.items()))}')
for f, (p, q, nn), big in (('cpsat-36-from-18.out', (3, 2, 2), 36), ('cpsat-100-from-50.out', (5, 2, 2), 100)):
    M = p ** nn * q; n = ok = 0
    for line in open(R + '/' + f):
        m = re.match(r'\s+D = \[(.*?)\] m = (\d+): set (.*)', line)
        if not m: continue
        D = tuple(int(t) for t in m.group(1).split(',') if t.strip()); size = int(m.group(2)); els = [int(t) for t in m.group(3).split()]
        E = tuple(l for l in range(1, nn + 1) if p ** l in D); F = tuple(l for l in range(0, nn + 1) if p ** l * q in D)
        n += 1; ok += (len(set(els)) == len(els) == size == table[(p, q, nn, E, F)] and all(0 <= e < big for e in els) and pat({e: 1 for e in els}, big) == D)
    print(f'(2) {f}: {n} patterns of Z_{M}; a set on Z_{big} of the least size of my table for Z_{M} with exactly that pattern among the divisors of {big}: {ok}')

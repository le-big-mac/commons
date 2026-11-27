"""The number m of Theorem 1 of the paper, typed from the theorem's statement (minsize.tex, Theorem 1), and the passage
between a set D of divisors of p^n q and the triple (E, F, balanced).

usage: thm.py            compares the formula with the 'min' of every line of the solver's multiset tables (ten groups)
                         and with a complete enumeration of multisets on Z_6, Z_10, Z_15 and Z_12."""
import sys, json, glob, itertools
from cyc import divisors, pattern


def theorem_m(p, q, n, E, F, bal):
    E = set(E); F = set(F)
    assert E <= set(range(1, n + 1)) and F <= set(range(1, n + 1))
    e = len(E)
    if not bal:                                              # (a)
        if F <= E:
            return p ** e
        return p ** e * (p ** len(F - E) + q)
    if F == set(range(1, n + 1)):                            # (b)
        return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F)       # (c)
    G = {a for a in F - E if a > a0}
    k1 = len(G)
    x = 1
    if k1 == 0: x = 0                                                                        # clause (1)
    if any(a in E for a in range(1, a0)): x = 0                                              # clause (2)
    if a0 in E and p >= 3: x = 0                                                             # clause (3)
    if k1 >= 1 and a0 in E and p == 2 and any(a0 < a < min(G) for a in E - F): x = 0         # clause (4)
    return q * p ** e * (p ** k1 + x)


def D_of(p, q, n, E, F, bal):
    return frozenset([p ** a for a in E] + [p ** a * q for a in F] + ([q] if bal else []))


def all_patterns(p, q, n):
    lv = list(range(1, n + 1))
    for bal in (False, True):
        for eb in range(2 ** n):
            for fb in range(2 ** n):
                E = [a for a in lv if eb >> (a - 1) & 1]
                F = [a for a in lv if fb >> (a - 1) & 1]
                yield E, F, bal


def read_table(path):
    rows = []
    for line in open(path):
        if line.startswith('{'):
            rows.append(json.loads(line))
    return rows


def parse_witness(s):
    mult = {}
    for t in s.split():
        x, _, m = t.partition('^')
        mult[int(x)] = mult.get(int(x), 0) + (int(m) if m else 1)
    return mult


if __name__ == '__main__':
    O = '/srv/commons/agent2-pdtile/minsize-agent3/out/'
    tot = agree = wit_ok = 0
    for f in sorted(glob.glob(O + '*-multi-cpsat.jsonl')):
        rows = read_table(f)
        n_ok = 0
        for o in rows:
            p, q, n = o['p'], o['q'], o['n']
            E = [a for a in o['E']]
            F = [a for a in o['F'] if a >= 1]
            bal = 0 in o['F']
            m = theorem_m(p, q, n, E, F, bal)
            tot += 1
            agree += (o['min'] == m)
            n_ok += (o['min'] == m)
            if o.get('witness'):
                w = parse_witness(o['witness'])
                wit_ok += (sum(w.values()) == o['min'] and pattern(w, p ** n * q) == D_of(p, q, n, E, F, bal))
        print(f'{f.split("/")[-1]}: {len(rows)} lines; table min = Theorem 1 in {n_ok}')
    print(f'solver tables (multisets, CP-SAT): {tot} lines; min equals the theorem\'s number in {agree}; '
          f'the witness has that size and exactly that pattern (my exact division) in {wit_ok}')
    # complete enumeration of multisets on small groups: least size of each exact pattern, against the theorem
    for (p, q, n, K) in [(2, 3, 1, 6), (3, 2, 1, 6), (2, 5, 1, 10), (5, 2, 1, 10), (3, 5, 1, 9), (2, 3, 2, 9)]:
        M = p ** n * q
        best = {}
        for k in range(1, K + 1):
            for c in itertools.combinations_with_replacement(range(M), k - 1):
                mult = {0: 1}
                for x in c:
                    mult[x] = mult.get(x, 0) + 1
                P = pattern(mult, M)
                if P not in best:
                    best[P] = k
        ok = und = 0
        for E, F, bal in all_patterns(p, q, n):
            m = theorem_m(p, q, n, E, F, bal)
            D = D_of(p, q, n, E, F, bal)
            if m <= K:
                assert best.get(D) == m, (p, q, n, E, F, bal, m, best.get(D))
                ok += 1
            else:
                assert D not in best
                und += 1
        print(f'Z_{M} (p={p}, q={q}, n={n}): every multiset of up to {K} elements: the least size of each exact pattern is the '
              f'theorem\'s number for the {ok} patterns with m <= {K}; the other {und} have none that small')

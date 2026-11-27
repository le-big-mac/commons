"""'736 of the 1,088 patterns have a set, and each of those has a set of the least multiset's size' (paper, Section 1.3),
from the solver's set tables; beside it the number of patterns per group for which the author's least_mult record says the
least cap is 1 (a least multiset that is a set), and my own count of sets of size m by my model (sets_cpsat.solve, cap 1)."""
import glob, sys
from thm import read_table, theorem_m, D_of
from sets_cpsat import solve
O = '/srv/commons/agent2-pdtile/minsize-agent3/out/'
tot = has = same = und = 0; mine = 0; mine_und = 0
for f in sorted(glob.glob(O + '*-set-cpsat.jsonl')):
    rows = read_table(f); g_has = g_same = 0; g_mine = 0
    for o in rows:
        p, q, n = o['p'], o['q'], o['n']; E = o['E']; F = [a for a in o['F'] if a >= 1]; bal = 0 in o['F']
        m = theorem_m(p, q, n, E, F, bal); tot += 1
        if o.get('undecided'): und += 1
        if o.get('min') is not None:
            has += 1; g_has += 1; same += (o['min'] == m); g_same += (o['min'] == m)
        st, mult = solve(p ** n * q, D_of(p, q, n, E, F, bal), 1, size=m, tlim=30) if m <= p ** n * q else ('TOO BIG', None)
        if mult is not None: g_mine += 1
        elif st not in ('INFEASIBLE', 'TOO BIG'): mine_und += 1
    mine += g_mine
    print(f'{f.split("/")[-1]}: {len(rows)} patterns; with a set (table): {g_has}; of those with least set = m: {g_same}; a set of m elements found by my model: {g_mine}')
print(f'all ten: {tot} patterns; with a set: {has}; of those with a set of the least multiset\'s size: {same}; lines with an undecided entry: {und}; '
      f'my model: a set of m elements exists for {mine}, undecided {mine_und}')

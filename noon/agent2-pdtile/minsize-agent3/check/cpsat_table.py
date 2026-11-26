"""Referee's CP-SAT table for a group the tree recursion cannot reach (q large): least size per pattern by trying the
admissible sizes upward (multiples of p^e, times q if 0 in F), with my own model (cpsat_check.py).
usage: cpsat_table.py p q n kind tlimit workers [which: all | zero (0 in F only) | x1 (rule says x = 1) ]
A pattern is 'decided' when a witness is found and every smaller admissible size was proved infeasible."""
import sys, time
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *
from cpsat_check import feasible

p, q, n, kind = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
tl, wk = float(sys.argv[5]), int(sys.argv[6]); which = sys.argv[7] if len(sys.argv) > 7 else 'all'
M = p ** n * q
ok = bad = und = 0
print(f'# p={p} q={q} n={n} order {M} {kind}, my CP-SAT model, time limit {tl:.0f} s per size, {wk} worker(s), patterns: {which}', flush=True)
t00 = time.time()
for E, F in all_patterns(n):
    if 0 in F:
        form, x = rule_value(p, q, n, E, F); name = 'rule' if x is not None else 'F all'
    else:
        form, x, name = thm_value(p, q, E, F), None, 'thm'
    if which == 'zero' and 0 not in F: continue
    if which == 'x1' and x != 1: continue
    step = p ** len(E) * (q if 0 in F else 1)
    s = step; unknown = []; found = None
    cap = min(M, form + step) if kind == 'set' else form + step
    while s <= cap:
        r, w = feasible(p, q, n, E, F, s, kind == 'set', tl, wk)
        if r: found = s; break
        if r is None: unknown.append(s)
        s += step
    if kind == 'multi':
        if found is not None and not unknown:
            v = 'as formula' if found == form else 'DIFFERS FROM FORMULA'; ok += (found == form); bad += (found != form)
        elif found is not None and found < form: v = 'SMALLER THAN FORMULA'; bad += 1
        else: v = f'undecided at sizes {unknown}'; und += 1
    else:
        v = ('no set up to %d' % cap) if found is None else ('set of formula size' if found == form else 'set size differs from formula')
        if unknown: v += f' (undecided at {unknown})'
    print(f'{list(E)} | {list(F)} | {found} | {name} {form} | {v}', flush=True)
print(f'# decided and as formula: {ok}; decided and different: {bad}; undecided: {und}; {time.time() - t00:.0f} s', flush=True)

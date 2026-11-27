"""The solver's SET tables on Z_{p^(n+1) q} = Z_{p^n q * p}, read for the patterns that lie among the divisors of p^n q
(no level n+1 in E or F), beside the multiset value m of Theorem 1 for Z_{p^n q}.  This is the corollary for r = p, read off
tables that exist already: for p = 3 (Z_54 = Z_18 * 3) the remark after Corollary 21 says the least set size is m for every
pattern for which a least multiset has multiplicities <= 3; for p = 2 nothing is claimed.
usage: tables_sets.py"""
import json
from thm import theorem_m, read_table
O = '/srv/commons/agent2-pdtile/minsize-agent3/out/'
for (p, q, n1) in [(3, 2, 3), (2, 3, 3), (2, 5, 3), (2, 3, 4)]:
    rows = read_table(O + f'n{n1}-p{p}-q{q}-set-cpsat.jsonl')
    for drop in range(1, n1 - 1 + 1):
        n = n1 - drop                      # the patterns of Z_{p^n q}, read on Z_{p^n1 q}: s = p^drop
        if n < 1: continue
        tot = eq = none = more = und = 0
        lines = []
        for o in rows:
            E = o['E']; F = [a for a in o['F'] if a >= 1]; bal = 0 in o['F']
            if any(a > n for a in E) or any(a > n for a in F):
                continue
            m = theorem_m(p, q, n, E, F, bal)
            assert m == theorem_m(p, q, n1, E, F, bal)       # the remark 'r = p says nothing new' for multisets
            tot += 1
            if o.get('min') is None:
                if o.get('undecided'):
                    und += 1; lines.append(f'    set table undecided: E={E} F={o["F"]} m={m} line={ {k: o[k] for k in o if k not in ("witness",)} }')
                else:
                    none += 1; lines.append(f'    NO SET (table): E={E} F={o["F"]} (0 in F means Phi_q) m={m}; table line: min={o.get("min")}, undecided={o.get("undecided")}')
            elif o['min'] == m: eq += 1
            else:
                more += 1; lines.append(f'    least set {o["min"]} > m = {m}: E={E} F={o["F"]}')
        print(f'Z_{p**n1*q} = Z_{p**n*q} * {p**drop} (p={p}, q={q}): patterns of Z_{p**n*q}: {tot}; set table: least set = m for {eq}; '
              f'larger for {more}; no set for {none}; undecided for {und}')
        for l in lines: print(l)

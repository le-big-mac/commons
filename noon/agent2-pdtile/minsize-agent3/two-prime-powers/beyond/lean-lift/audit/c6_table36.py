# Part 3(d), comparison with the existing table of least sizes for all 256 patterns of Z_36
# (/srv/commons/agent2-pdtile/minsize-agent3/two-prime-powers/rows-36.json, fields "D" = the d > 1 with Phi_d dividing, "size").
# The pattern of each instance of the three theorems (p=2, q=3, n=2, r=3) is derived here from the Lean clauses.
import sys, json
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from core import *
from liftmin_conditions import *
from c5_liftmin_cpsat import spec_of, check_spec
rows = json.load(open("/srv/commons/agent2-pdtile/minsize-agent3/two-prime-powers/rows-36.json"))
table = {tuple(sorted(r["D"])): r["size"] for r in rows}
assert len(rows) == 256 == len(table)
p, q, n, r = 2, 3, 2, 3
val = lean_values()
seen = set(); bad = 0
for (label, member, v) in sorted(instances(p, q, n, r, val), key=lambda i: i[2]):
    spec, need_pos = spec_of(label, p, q, n, r)
    check_spec(spec, need_pos, member, 36)
    assert set(spec) == set(divisors(36)) - {1}          # the clauses fix every divisor d > 1 of 36
    D = tuple(sorted(d for d, b in spec.items() if b))
    seen.add(D)
    agree = (table[D] == v); bad += (not agree)
    print(f"  {str(label):30s} pattern {str(list(D)):18s} Lean value {v:3d}  table size {table[D]:3d}  {'agrees' if agree else 'DISAGREES'}")
lifted = {D for D in table if not (set(D) & {9, 18, 36})}
print(f"instances: {len(seen)} distinct patterns; table rows with none of 9, 18, 36: {len(lifted)}; the same set: {seen == lifted}; disagreements: {bad}")

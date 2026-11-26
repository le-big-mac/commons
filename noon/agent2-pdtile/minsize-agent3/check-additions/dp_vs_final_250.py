"""Do the 42 minima of order 250 that the author's solvers had decided in the final state equal the referee's recursion?
usage: dp_vs_final_250.py DP_OUT HIGHS_JSONL CPSAT_JSONL"""
import sys, json, ast
dp = {}
for l in open(sys.argv[1]):
    if l.startswith('#') or '|' not in l: continue
    f = [s.strip() for s in l.split('|')]
    try: dp[tuple(ast.literal_eval(f[0])), tuple(ast.literal_eval(f[1]))] = int(f[2])
    except Exception: pass
same = diff = 0; n = 0
seen = {}
for path in sys.argv[2:]:
    for l in open(path):
        if not l.startswith('{'): continue
        r = json.loads(l)
        if r['min'] is None or r['undecided']: continue
        k = (tuple(r['E']), tuple(r['F']))
        seen.setdefault(k, set()).add(r['min'])
for k, v in seen.items():
    assert len(v) == 1
    if dp.get(k) == next(iter(v)): same += 1
    else: diff += 1
print(f"order 250: the recursion's table has {len(dp)} patterns; of the {len(seen)} patterns decided by a solver in the final state, {same} have the recursion's value and {diff} do not")

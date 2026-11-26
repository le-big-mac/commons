"""Score the second sheet (expectations-z225-second.md) from out225/z225-*.jsonl and bounds-225.json.   usage: score225b.py"""
import json, glob
B = json.load(open('bounds-225.json')); P = json.load(open('predictions-225.json'))
R = {}
for f in sorted(glob.glob('out225/z225-*.jsonl')):
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); R[','.join(map(str, r['D']))] = r
dec = {k: r['size'] for k, r in R.items() if r['status'] == 'optimal'}
print('decided:', len(dec))
print('V0 failures (pattern, LB, least, U):', [(B[k]['S'], B[k]['LB'], v, B[k]['U']) for k, v in dec.items() if not (B[k]['LB'] <= v <= B[k]['U'])])
# an 'infeasible' under an upper bound ub means least > ub: check against U as well
print('V0: proved above the given upper bound while U is at most that bound (general position would fail):', [(B[k]['S'], r['upper_bound_given'], B[k]['U']) for k, r in R.items() if r['status'] == 'infeasible' and B[k]['U'] <= r['upper_bound_given']])
eq = [k for k, v in dec.items() if v == B[k]['U']]; lt = [k for k, v in dec.items() if v < B[k]['U']]
print(f'V1: least = U for {len(eq)} of {len(dec)} decided = {100 * len(eq) / max(len(dec), 1):.1f}% (expected at least 85%) ->', len(eq) >= 0.85 * len(dec))
none = [k for k in dec if P[k]['cls'] == 'none']
print(f'V2: patterns with no prediction on the first sheet that are decided: {len(none)}; least = U for {sum(1 for k in none if dec[k] == B[k]["U"])} (expected at least half) ->', 2 * sum(1 for k in none if dec[k] == B[k]['U']) >= len(none))
print(f'V3: decided with least < U: {len(lt)} (expected at least 10) ->', len(lt) >= 10)
show = lambda S: ' '.join(f'{u}{v}' for u, v in S)
print('   least < U (pattern, LB, least, U):', [(show(B[k]['S']), B[k]['LB'], dec[k], B[k]['U']) for k in lt])
print('   decided with LB = least:', sum(1 for k, v in dec.items() if v == B[k]['LB']), '; with LB = U:', sum(1 for k in dec if B[k]['LB'] == B[k]['U']))

"""The author's tables, recomputed pattern by pattern with the referee's integer programme (milp.py: cuboid forms, HiGHS).

For each pattern in the author's output files: least size of a multiset with exactly that pattern, with the author's value
(the size of the multiset his solver found) as upper bound, so that anything smaller would be found.  Set beside his value
and his 'proved' flag.
usage: retable.py M K J tlimit [only-decided]      (patterns number J mod K, in the order of sorted patterns)
"""
import sys, json, glob, time
from lib import divisors, pattern
from milp import least

M, K, J, tl = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]); only_dec = len(sys.argv) > 5
OUT = '/home/agent3/pq2/out/'
files = sorted(glob.glob(OUT + f'z{M}-[0-9].jsonl')) + ([OUT + 'z36-again.jsonl'] if M == 36 else [])
R = {}
for f in files:
    for l in open(f):
        if l.startswith('{'):
            r = json.loads(l); k = tuple(sorted(r['D'])); old = R.get(k)
            if old is None or (r['proved'] and not old['proved']) or (old['min'] is None and r['min'] is not None): R[k] = r
dv = [d for d in divisors(M) if d > 1]
pats = sorted(R, key=lambda D: (len(D), D))
for i, D in enumerate(pats):
    if i % K != J: continue
    r = R[D]
    if only_dec and not (r['proved'] and r['min'] is not None): continue
    ub = r['min'] if r['min'] is not None else 2 * M
    if ub > 2 * M: ub = 2 * M
    t0 = time.time(); st, sz, v = least(M, list(D), [d for d in dv if d not in D] or [1], ub=ub, solver='highs', tlimit=tl)
    if v: assert pattern(M, v) == list(D)
    if st == 'optimal':
        verdict = 'same value' if sz == r['min'] else ('SMALLER than the author\'s' if (r['min'] is None or sz < r['min']) else 'LARGER')
    elif st == 'infeasible': verdict = 'no multiset up to the bound'
    else: verdict = 'not proved in time'
    print(json.dumps(dict(M=M, D=list(D), author_min=r['min'], author_proved=r['proved'], referee_status=st, referee_least=sz, verdict=verdict, seconds=round(time.time() - t0, 1))), flush=True)

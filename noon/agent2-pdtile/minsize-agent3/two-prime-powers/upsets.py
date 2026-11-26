"""Patterns that are up-sets of the divisor lattice (if d is in the pattern, so is every multiple of d that divides M):
is the least size the sum of M/c over the maximal divisors c of M that are NOT in the pattern?
(Each such c gives a coset of the subgroup of order M/c, whose mask is divisible by Phi_d exactly for d not dividing c.)
usage: upsets.py M out/zM-*.jsonl"""
import sys, json, itertools
M = int(sys.argv[1]); divs = [d for d in range(1, M + 1) if M % d == 0]
R = {}
for f in sys.argv[2:]:
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); R[frozenset(r['D'])] = r
def is_up(D): return all((e in D) for d in D for e in divs if e % d == 0)
def guess(D):
    comp = [c for c in divs if c not in D]                      # includes 1; a down-set when D is an up-set
    mx = [c for c in comp if not any(e != c and e % c == 0 for e in comp)]
    return sum(M // c for c in mx), mx
n = ok = und = 0; bad = []
for D, r in sorted(R.items(), key=lambda kv: (len(kv[0]), sorted(kv[0]))):
    if not is_up(D): continue
    n += 1; g, mx = guess(D)
    if not r['proved']: und += 1
    if r['min'] == g: ok += 1
    else: bad.append((sorted(D), r['min'], r['proved'], g, mx))
print(f'M = {M}: {len(R)} patterns in the files; up-sets among them {n}; least size found = sum of M/c over the maximal non-divisors c in {ok}; of the up-sets, not proved least: {und}')
for b in bad: print('   differs:', b)

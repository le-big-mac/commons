"""Compares the values printed by Lean (A2_eval.out) with those expected from core.py (a2_expected.json).
usage: a2_cmp.py A2_eval.out a2_expected.json"""
import json
import sys

out, exp = sys.argv[1], json.load(open(sys.argv[2]))
fams, lhs, mus, mub = [], [], None, None
other = []
for line in open(out):
    line = line.rstrip('\n')
    if line.startswith('FAMS '):
        fams += json.loads(line[5:])
    elif line.startswith('LHS '):
        lhs += json.loads(line[4:])
    elif line.startswith('MUSMALL '):
        mus = json.loads(line[8:])
    elif line.startswith('MUBIG '):
        mub = json.loads(line[6:])
    elif line.strip():
        other.append(line)
print('other lines in the Lean output (errors would be here):', len(other))
for l in other[:5]:
    print('   ', l[:200])
n = len(exp['exp_fams'])
assert len(fams) == n, (len(fams), n)
mm = [k for k in range(n) if fams[k] != exp['exp_fams'][k]]
by_p = {}
for l, p in exp['fams']:
    by_p[p] = by_p.get(p, 0) + 1
live_true = sum(sum(r[:5]) for r in fams)
print('live, rank: %d families (by p: %s), levels i = 0..4, %d values each; live is true in %d of %d; mismatches %d'
      % (n, sorted(by_p.items()), 10, live_true, 5 * n, len(mm)))
for k in mm[:5]:
    print('   MISMATCH', exp['fams'][k], 'Lean', fams[k], 'expected', exp['exp_fams'][k])
print('empty family among them:', sum(1 for l, p in exp['fams'] if not l), 'families; rank max', max(max(r[5:]) for r in fams))
assert len(mus) == len(exp['mu_small'])
print('mu t for t = 0..3000: mismatches', sum(1 for a, b in zip(mus, exp['mu_small']) if a != b))
print('mu on %d larger arguments: mismatches %d' % (len(mub), sum(1 for a, b in zip(mub, exp['mu_big']) if a != b)))
assert len(lhs) == len(exp['exp_lhs'])
mm = [k for k in range(len(lhs)) if lhs[k] != exp['exp_lhs'][k]]
print('lhsN1: %d cases (m, T); mismatches %d' % (len(lhs), len(mm)))
for k in mm[:5]:
    print('   MISMATCH', exp['lhs_cases'][k], 'Lean', lhs[k], 'expected', exp['exp_lhs'][k])
print('lhsN1 m (all odd t > 1 with mu t <= m - 1), from Lean:')
for k in range(15):
    m, T = exp['lhs_cases'][k]
    print('   m = %2d  |T| = %3d  lhsN1 = %d/%d' % (m, len(T), lhs[k][0], lhs[k][1]))

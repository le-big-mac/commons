"""Driver for brute.c: writes the remainder matrices (exact long division, pat.py), runs njobs processes, merges, and
compares the least size per pattern with the note's formulas (section 2 theorem when 0 not in F; section 3 rule when 0 in F).
usage: brute_run.py p q n S kind(multi|set) njobs
Writes brute-{M}-{kind}-S{S}.out (table) in this folder."""
import sys, subprocess, os, math, collections, random
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *

p, q, n, S, kind, njobs = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
M = p ** n * q
here = '/home/agent3/minsize/check'
inp = f'{here}/brute-{M}.in'
divs = [p ** a for a in range(1, n + 1)] + [p ** a * q for a in range(0, n + 1)]
with open(inp, 'w') as f:
    f.write(f'{M} {p} {q} {n} {len(divs)}\n')
    for d in divs:
        R = remainder_matrix(d, M)
        f.write(f'{len(R)}\n')
        for row in R: f.write(' '.join(map(str, row)) + '\n')
# sanity of the matrix method against direct long division of A(X), on random multisets
random.seed(1)
mats = {d: remainder_matrix(d, M) for d in divs}
for _ in range(300):
    w = [0] * M
    for _ in range(random.randint(1, 12)): w[random.randrange(M)] += 1
    for d in divs:
        viaM = all(sum(r[x] * w[x] for x in range(M)) == 0 for r in mats[d])
        assert viaM == divides(d, w)
cap = 1 if kind == 'set' else S
procs = [subprocess.Popen([f'{here}/brute', inp, str(S), str(cap), str(j), str(njobs)], stdout=subprocess.PIPE, text=True) for j in range(njobs)]
counts = collections.defaultdict(collections.Counter); visited = 0
for pr in procs:
    out, _ = pr.communicate()
    assert pr.returncode == 0, 'a job failed (pattern mismatch?)'
    for line in out.splitlines():
        if line.startswith('#'):
            visited += int(line.split('visited=')[1]); continue
        t = line.split(); b = int(t[0])
        for tok in t[1:]:
            s, c = tok.split(':'); counts[b][int(s)] += int(c)
expect = sum(math.comb(M, s) for s in range(1, min(S, M) + 1)) if kind == 'set' else math.comb(M + S, M) - 1
lines = []
lines.append(f'# Z_{M} (p={p}, q={q}, n={n}), every {"set" if kind == "set" else "multiset"} of size 1..{S}: {visited} visited (expected {expect}); '
             f'pattern by division and by the tree agreed on every one')
assert visited == expect
ok = bad = beyond = 0
lines.append('# E | F | least size found (number at that size) | note\'s formula | verdict')
for E, F in all_patterns(n):
    b = sum(1 << (a - 1) for a in E) + sum(1 << (n + a) for a in F)
    form = thm_value(p, q, E, F) if 0 not in F else rule_value(p, q, n, E, F)[0]
    which = 'thm' if 0 not in F else 'rule'
    if counts[b]:
        m = min(counts[b]); c = counts[b][m]
        if kind == 'multi':
            v = 'AS FORMULA' if m == form else 'DIFFERENT FROM FORMULA'
            ok += (m == form); bad += (m != form)
        else:
            v = 'set of the formula size' if m == form else ('smallest set larger than formula' if m > form else 'SET SMALLER THAN FORMULA')
        lines.append(f'{list(E)} | {list(F)} | {m} ({c}) | {which} {form} | {v}')
    else:
        if kind == 'multi':
            if form > S: v = f'none of size <= {S}, consistent (formula {form} is beyond the enumeration)'; beyond += 1
            else: v = 'NONE FOUND BUT FORMULA IS WITHIN THE ENUMERATION'; bad += 1
        else:
            v = 'no set' if S >= M else f'no set of size <= {S}'
        lines.append(f'{list(E)} | {list(F)} | none | {which} {form} | {v}')
if kind == 'multi':
    lines.append(f'# multisets: least size equals the formula in {ok} patterns; differs in {bad}; formula beyond the enumerated sizes (and nothing found) in {beyond}')
else:
    lines.append(f'# sets: {sum(1 for b in counts if counts[b])} patterns occur')
open(f'{here}/brute-{M}-{kind}-S{S}.out', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines[:1] + lines[-1:]))

"""agent3's own check of the prover's construction for the balanced half: build it with the prover's `construct`, then find the
pattern with MY pattern code (minsize.exact_pattern, complex values at the roots of unity) and the size with MY statement of the
rule (summary.R and q p^e for F all levels), for every pattern with 0 in F.     usage: check_balanced_construction.py NMAX p q [p q ...]"""
import sys, itertools, io, contextlib
sys.path.insert(0, '/home/agent3/minsize'); sys.path.insert(0, '/home/agent3/minsize/prove')
from minsize import exact_pattern
def R(p, q, n, E, F):
    e = len(E)
    if set(F) == set(range(n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F); FE = sorted(a for a in F if a > a0 and a not in E); k2 = len(FE)
    if k2 == 0 or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or (a0 in E and p == 2 and any((a in E and a not in F) for a in range(a0 + 1, FE[0]))): x = 0
    else: x = 1
    return q * p ** e * (p ** k2 + x)
with contextlib.redirect_stdout(io.StringIO()):
    import construct_bal as cb
nmax = int(sys.argv[1]); pairs = [(int(sys.argv[i]), int(sys.argv[i + 1])) for i in range(2, len(sys.argv), 2)]
tot = bad = 0
for p, q in pairs:
    for n in range(1, nmax + 1):
        ok = 0; wrong = 0
        for ke in range(n + 1):
            for E in itertools.combinations(range(1, n + 1), ke):
                for kf in range(n + 1):
                    for F1 in itertools.combinations(range(1, n + 1), kf):
                        F = (0,) + F1
                        A = cb.construct(p, q, n, set(E), set(F))
                        x = A if isinstance(A, (list, tuple)) and len(A) == p ** n * q else None
                        if x is None:                                    # the prover's function may return a dict or (weights, info)
                            if isinstance(A, tuple): A = A[0]
                            if isinstance(A, dict):
                                x = [0] * (p ** n * q)
                                for k, v in A.items(): x[k] += v
                            else: x = list(A)
                        good = exact_pattern(p, q, n, x) == (tuple(E), tuple(F)) and sum(x) == R(p, q, n, E, F)
                        ok += good; wrong += (not good)
                        if not good and wrong <= 2: print('   NOT AS WANTED', p, q, n, E, F, exact_pattern(p, q, n, x), sum(x), R(p, q, n, E, F))
        tot += ok + wrong; bad += wrong
        print(f'p={p} q={q} n={n} order {p ** n * q}: {ok} patterns with 0 in F have the wanted pattern and the size of the rule; {wrong} do not')
print('total', tot, 'patterns;', bad, 'not as wanted')

"""A trial, by exhaustion on small groups, of a statement Yonder fixed for Lean on 26 November 2026 (SetLift.lean, exists_set_lift).
Noon (agent2), 27 November 2026.  Exact: X^y is reduced modulo each cyclotomic polynomial in whole numbers (functions from try.py, which in the shared folder is lean-two-try-27nov-agent2.py).

  For an odd prime r and j >= 1: every w : Z_N -> {0, ..., r^j} with some value neither 0 nor r^j is the reduction of a SET A on
  Z_{N r^j} (the fibre over x holds w(x) elements) such that, for every d dividing N r^j,
        Phi_d divides mask(A)   exactly when   d divides N and Phi_d divides mask(w).
The program looks for such a set by trying every choice of w(x) lifts of each x, and checks the whole "exactly when", for the d that
divide N as well as for the new ones.
Controls that must find failures: w with every value 0 or r^j (the statement's hypothesis left out); the prime 2 with j = 2.
usage: python -I try-sets.py > try-sets.out"""
import sys, os, itertools, importlib.util
spec = importlib.util.spec_from_file_location('trial', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lean-two-try-27nov-agent2.py' if os.path.basename(__file__).startswith('lean-sets-try') else 'try.py')); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)

def run(N, r, j, hypothesis=True):
    q = r ** j; M = N * q; ds = T.divisors(M); R = {d: T.residues(M, d) for d in ds}; RN = {d: T.residues(N, d) for d in ds if N % d == 0}
    add = lambda u, v: tuple(a + b for a, b in zip(u, v)); zero = {d: tuple([0] * len(R[d][0])) for d in ds}
    # for each x and each k: every choice of k of the q lifts of x, as its sum of residues for every d
    choice = [[None] * (q + 1) for _ in range(N)]
    for x in range(N):
        lifts = [x + N * i for i in range(q)]
        for k in range(q + 1):
            out = []
            for sub in itertools.combinations(lifts, k):
                v = {}
                for d in ds:
                    acc = zero[d]
                    for y in sub: acc = add(acc, R[d][y])
                    v[d] = acc
                out.append(v)
            choice[x][k] = out
    tried = 0; bad = []
    for w in itertools.product(range(q + 1), repeat=N):
        some = any(v not in (0, q) for v in w)
        if not any(w): continue
        if hypothesis != some: continue            # with the hypothesis: some value strictly between; the control: none
        tried += 1
        want = {}                                  # for each d: must Phi_d divide mask(A)?
        for d in ds:
            if N % d: want[d] = False
            else:
                acc = tuple([0] * len(RN[d][0]))
                for x in range(N):
                    if w[x]: acc = add(acc, tuple(w[x] * c for c in RN[d][x]))
                want[d] = not any(acc)
        found = False
        for pick in itertools.product(*[range(len(choice[x][w[x]])) for x in range(N)]):
            ok = True
            for d in ds:
                acc = zero[d]
                for x in range(N): acc = add(acc, choice[x][w[x]][pick[x]][d])
                if (not any(acc)) != want[d]: ok = False; break
            if ok: found = True; break
        if not found: bad.append(w)
    return tried, bad

if __name__ == '__main__':
    print('SETS (exists_set_lift): w on Z_N with values 0 .. r^j, some value neither 0 nor r^j; those with no set on Z_{N r^j} as the statement asks')
    total = 0
    for N, r, j in [(1, 3, 1), (2, 3, 1), (3, 3, 1), (4, 3, 1), (5, 3, 1), (6, 3, 1), (7, 3, 1), (1, 5, 1), (2, 5, 1), (3, 5, 1), (4, 5, 1), (1, 7, 1), (2, 7, 1), (3, 7, 1), (1, 3, 2), (2, 3, 2), (3, 3, 2), (1, 11, 1), (2, 11, 1)]:
        tried, bad = run(N, r, j); total += tried
        print('  N = %d  r = %2d  j = %d: %6d multisets, %d without such a set%s' % (N, r, j, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
    print('  together %d multisets' % total)
    print('  control, which must fail (every value 0 or r^j: the hypothesis left out):')
    for N, r, j in [(1, 3, 1), (2, 3, 1), (3, 3, 1), (4, 3, 1), (2, 5, 1), (2, 3, 2)]:
        tried, bad = run(N, r, j, hypothesis=False); print('  N = %d  r = %2d  j = %d: %6d multisets, %d without such a set' % (N, r, j, tried, len(bad)), flush=True)
    print('  outside the statement (the prime 2):')
    for N, r, j in [(1, 2, 1), (2, 2, 1), (3, 2, 1), (4, 2, 1), (5, 2, 1), (6, 2, 1), (1, 2, 2), (2, 2, 2), (3, 2, 2), (4, 2, 2)]:
        tried, bad = run(N, r, j); print('  N = %d  r = %2d  j = %d: %6d multisets, %d without such a set%s' % (N, r, j, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)

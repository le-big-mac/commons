"""The induction of the note's section 6 ("the proof that Lean checked", in words), run step by step by the referee's own program
on multisets that are NOT built from cosets.

Input multisets: integer vectors divisible by every Phi_d, d in D, made as g(X) h(X) with g = prod_{d in D} Phi_d and h random,
shifted by the least constant that makes them nonnegative (as in ../random_S.py).  Each is checked to satisfy (i) by ../lib.divides.
Then, exactly as the note says:  N_0 = 1, N_{k+1} = p^k q^m (k = 0..n).  For k = n down to 0, with A periodic under N_{k+1}:
   t = the largest divisor of N_{k+1} that is not in D and does not divide N_k, or 1 if there is none;
   check: every divisor of N_{k+1} not in D divides N_k or t                                  ("because of the chain")
   check: A(x + N_k + t) + A(x) = A(x + N_k) + A(x + t) for all x                             (F2)
   mu(x) = min_i A(x + i N_k);  nu = A - mu
   check: mu is N_k-periodic, nu >= 0, nu is t-periodic                                        (F3)
   check: t is a divisor of M not in D; Phi_d | nu and Phi_d | mu for every d in D             (the claim's hypothesis for mu)
   continue with mu.
At the end mu is constant.  The pieces are collected by a corner that t divides and the sum is compared with the input.
Also: the same with p = q (the note says p != q is never used), and a control with three primes, where no chain exists.

usage: peel.py seed trials
"""
import sys, random, json, time
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from lib import divisors, corners, divides, cyclotomic, upsets


def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return r


def periodic(A, M, c): return all(A[(x + c) % M] == A[x] for x in range(M))


def peel(M, D, N, A0):
    """returns (True, pieces) or (False, reason).  N = [N_0, ..., N_K] with N_K = M."""
    Dset = set(D); A = list(A0); pieces = []
    for k in range(len(N) - 2, -1, -1):
        s = N[k]; top = N[k + 1]
        if not periodic(A, M, top % M): return False, f'not periodic under N_{k+1}'
        cand = [d for d in divisors(top) if d not in Dset and s % d != 0]
        t = max(cand) if cand else 1
        if any(s % d != 0 and t % d != 0 for d in divisors(top) if d not in Dset): return False, f'chain property fails at k={k}'
        if t in Dset or M % t: return False, 't in D or not a divisor'
        if any(A[(x + s + t) % M] + A[x] != A[(x + s) % M] + A[(x + t) % M] for x in range(M)): return False, f'double difference at k={k}'
        mu = [min(A[(x + i * s) % M] for i in range(M)) for x in range(M)]
        nu = [A[x] - mu[x] for x in range(M)]
        if min(nu) < 0 or not periodic(mu, M, s) or not periodic(nu, M, t): return False, f'split at k={k}'
        if not all(divides(M, d, nu) for d in D) or not all(divides(M, d, mu) for d in D): return False, f'transform of a piece at k={k}'
        pieces.append((t, nu)); A = mu
    if not periodic(A, M, 1): return False, 'what is left is not constant'
    pieces.append((1, A))
    C = corners(M, D); g = {c: [0] * M for c in C}
    for t, f in pieces:
        cs = [c for c in C if c % t == 0]
        if not cs: return False, 't divides no corner'
        c = cs[0]
        if not periodic(f, M, c): return False, 'piece not periodic under its corner'
        for x in range(M): g[c][x] += f[x]
    if any(sum(g[c][x] for c in C) != A0[x] for x in range(M)): return False, 'sum of the pieces is not the input'
    return True, len(pieces)


def lattice_multiset(M, D, rnd):
    g = [1]
    for d in D: g = polymul(g, list(cyclotomic(d)))
    deg = len(g) - 1
    if M - deg < 1: return None
    amp = rnd.choice((1, 1, 2, 3))
    h = [rnd.randint(-amp, amp) for _ in range(M - deg)]
    if rnd.random() < 0.5: h = [x if rnd.random() < 0.3 else 0 for x in h]
    B = polymul(g, h); B = B + [0] * (M - len(B)); mn = min(B)
    A = [x - mn for x in B]
    return A if any(A) else None


def main():
    seed, T = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed); t0 = time.time()
    tot = ok = 0; fails = []
    for (p, n, q, m) in [(2, 2, 3, 1), (3, 2, 2, 1), (2, 2, 3, 2), (2, 3, 3, 1), (2, 1, 5, 2), (3, 1, 5, 1), (2, 3, 3, 2), (2, 2, 5, 2), (3, 3, 2, 2), (2, 3, 3, 3), (3, 2, 5, 2),
                         (2, 2, 2, 1), (3, 1, 3, 2), (2, 3, 2, 2), (5, 1, 5, 1)]:          # the last four have p = q
        M = p ** n * q ** m; N = [1] + [p ** k * q ** m for k in range(n + 1)]
        n_g = ok_g = 0
        for D in upsets(M):
            for _ in range(T):
                A = lattice_multiset(M, D, rnd)
                if A is None: continue
                assert all(divides(M, d, A) for d in D)
                tot += 1; n_g += 1
                good, info = peel(M, D, N, A)
                if good: ok += 1; ok_g += 1
                else: fails.append((M, list(D), info))
        print(json.dumps(dict(p=p, n=n, q=q, m=m, M=M, periods=N, upsets=len(upsets(M)), multisets=n_g, every_step_held=ok_g)), flush=True)
    print(f'# {tot} multisets not built from cosets, in 15 groups (four with p = q): every step of the induction held in {ok}; failures: {fails[:5]}')
    # the same multisets with one point added (they no longer satisfy (i) when D is not empty)
    tot2 = fail2 = 0; rnd = random.Random(seed + 1)
    for (p, n, q, m) in [(2, 2, 3, 2), (2, 3, 3, 2), (2, 2, 5, 2), (2, 2, 2, 1)]:
        M = p ** n * q ** m; N = [1] + [p ** k * q ** m for k in range(n + 1)]
        for D in upsets(M):
            if not D: continue
            for _ in range(T):
                A = lattice_multiset(M, D, rnd)
                if A is None: continue
                A[rnd.randrange(M)] += 1; tot2 += 1
                good, info = peel(M, D, N, A)
                fail2 += (not good)
    print(f'# placebo (one point added, D not empty): {tot2} multisets; a step failed in {fail2}')
    # three primes: Z_30, D = {30}, the six-element sum; every sequence of periods 1 = N_0, N_1, ..., 30 of divisors of 30
    M = 30; A = [0] * M
    for x in (5, 6, 12, 18, 24, 25): A[x] = 1
    assert divides(30, 30, A)
    import itertools
    seqs = 0; results = {}
    dv = [d for d in divisors(30) if d not in (1, 30)]
    for r in range(0, len(dv) + 1):
        for mid in itertools.permutations(dv, r):
            N = [1] + list(mid) + [30]; seqs += 1
            good, info = peel(30, [30], N, A)
            key = 'passed' if good else info.split(' at ')[0]
            results[key] = results.get(key, 0) + 1
    print(f'# control, Z_30, D = {{30}}, the multiset {{5, 6, 12, 18, 24, 25}}: {seqs} sequences of periods from 1 to 30 tried; outcomes: {results}')
    # and is there any chain of periods ending at 30 at all?  (the condition of the Lean lemma: the divisors of N_{k+1} that do not divide N_k form a chain)
    def chain_ok(N):
        for k in range(len(N) - 1):
            ds = [d for d in divisors(N[k + 1]) if N[k] % d != 0]
            if any(a % b != 0 and b % a != 0 for a in ds for b in ds): return False
        return True
    for M in (30, 42, 60, 105, 210, 36, 72, 100):
        dvm = [d for d in divisors(M) if d not in (1, M)]
        found = None; count = 0
        # depth-first over increasing-length sequences of distinct divisors, at most 6 intermediate terms
        def rec(seq):
            nonlocal_found[0] = nonlocal_found[0] or (chain_ok(seq + [M]) and seq + [M])
            if nonlocal_found[0] or len(seq) > 6: return
            for d in dvm:
                if d not in seq and chain_ok(seq + [d]): rec(seq + [d])
        nonlocal_found = [None]
        rec([1])
        print(f'# a chain of periods 1 = N_0, ..., N_K = {M} (each step: the divisors of N_(k+1) not dividing N_k form a chain): {nonlocal_found[0] if nonlocal_found[0] else "none exists"}')
    print(f'# {time.time() - t0:.0f} s')


if __name__ == '__main__':
    main()

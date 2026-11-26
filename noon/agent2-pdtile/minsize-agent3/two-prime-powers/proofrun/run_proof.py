"""The induction of section 6 of the note, run as a program.  For M = p^n q^m and an up-set D: take a multiset A whose
transform vanishes at the orders in D (built as a random sum of cosets of cZ_M, c outside D, so that it is not given as a sum of
CORNER cosets with known pieces), and peel it exactly as the proof says: periods N_0 = 1, N_{k+1} = p^k q^m; going down from
k = n: t = the largest divisor of N_{k+1} not in D that does not divide N_k (or 1); check the double-difference identity along
N_k and t; mu(x) = min over i of A(x + i N_k); nu = A - mu; check mu is N_k-periodic, nu >= 0 is t-periodic, t not in D.
At the end the function left is 1-periodic (constant).  Then the pieces are grouped by a corner that t divides, and the sum is
compared with A.  Exact integers throughout.   usage: run_proof.py [seed] [trials per up-set]"""
import sys, random, itertools
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1; T = int(sys.argv[2]) if len(sys.argv) > 2 else 3
random.seed(seed)
def divisors(M): return [d for d in range(1, M + 1) if M % d == 0]
def upsets(p, n, q, m):
    """all up-sets of the divisors of p^n q^m without 1, as sets of divisors: given by a staircase h(u) = least v with p^u q^v in D (m+1 if none), nonincreasing in u"""
    out = []
    def rec(u, prev, hs):
        if u > n: out.append(list(hs)); return
        for h in range(0, prev + 1): rec(u + 1, h, hs + [h])
    rec(0, m + 1, [])
    res = []
    for hs in out:
        D = {p ** u * q ** v for u in range(n + 1) for v in range(m + 1) if v >= hs[u]}
        if 1 not in D: res.append(D)
    return res
def periodic(A, M, c): return all(A[(x + c) % M] == A[x] for x in range(M))
tot = 0; groups = 0
for (p, n, q, m) in [(2, 2, 3, 1), (3, 2, 2, 1), (2, 2, 3, 2), (2, 3, 3, 1), (2, 1, 5, 2), (3, 1, 5, 1), (2, 3, 3, 2), (3, 2, 5, 1), (2, 2, 5, 2), (2, 4, 3, 1), (3, 3, 2, 2), (5, 2, 3, 1), (2, 3, 3, 3)]:
    M = p ** n * q ** m; dv = divisors(M); groups += 1
    N = [1] + [p ** k * q ** m for k in range(n + 1)]
    ups = upsets(p, n, q, m)
    for D in ups:
        L = [d for d in dv if d not in D]
        corners = [c for c in L if not any(e != c and e % c == 0 for e in L)]
        for _ in range(T):
            A = [0] * M
            for _ in range(random.randint(1, 5)):                 # a random sum of cosets of cZ_M with c outside D, random multiplicities
                c = random.choice(L); x0 = random.randrange(M); w = random.randint(1, 3)
                for j in range(M // c): A[(x0 + j * c) % M] += w
            orig = A[:]; pieces = []
            for k in range(n, -1, -1):                            # A is N_{k+1}-periodic here
                assert periodic(A, M, N[k + 1] % M), 'not periodic under the period'
                cand = [d for d in divisors(N[k + 1]) if d not in D and N[k] % d != 0]
                t = max(cand) if cand else 1
                assert t not in D and M % t == 0
                assert all(N[k] % d == 0 or t % d == 0 for d in divisors(N[k + 1]) if d not in D), 'chain property'
                s = N[k]
                assert all(A[(x + s + t) % M] + A[x] == A[(x + s) % M] + A[(x + t) % M] for x in range(M)), ('double difference', p, n, q, m, sorted(D), k)
                mu = [min(A[(x + i * s) % M] for i in range(M // s)) for x in range(M)]
                nu = [A[x] - mu[x] for x in range(M)]
                assert min(nu) >= 0 and periodic(mu, M, s) and periodic(nu, M, t), 'split'
                pieces.append((t, nu)); A = mu
            assert periodic(A, M, 1)                                # what is left is constant
            pieces.append((1, A))
            g = {c: [0] * M for c in corners}
            for t, f in pieces:
                c = max(c for c in corners if c % t == 0)           # a corner that t divides
                assert periodic(f, M, c)
                for x in range(M): g[c][x] += f[x]
            assert all(sum(g[c][x] for c in corners) == orig[x] for x in range(M))
            tot += 1
print(f'{groups} groups, {tot} multisets peeled as the proof says; every check held')

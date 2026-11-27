"""The step of the Corollary's proof from one odd prime to an odd number s: apply the lemma's lift once for each prime factor of s
(N = M, then M r1, then M r1 r2, ...) and test that the final multiset on Z_{Ms} has, among ALL divisors of Ms, exactly the divisors the
multiset on Z_M had (d = 1 included), and the same number of elements.  Random multisets on Z_M, M = p^n q; the moved element x0 chosen at random
at each step.   usage: python -I t6_iterated.py"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift')
import random
from cyc import divisors, pattern
rnd = random.Random(7)
def lift_once(A, N, r):
    k = 0; n1 = N
    while n1 % r == 0: n1 //= r; k += 1
    R = r ** (k + 1); rk = r ** k
    def L(x, t):
        for j in range(r):
            y = x + j * N
            if y % R == (x % rk) + rk * t: return y
        raise AssertionError
    i0 = rnd.randrange(len(A))
    return sorted(L(x, 1 if i == i0 else 0) for i, x in enumerate(A))
def random_multiset(N):
    if rnd.random() < 0.4: return sorted(rnd.randrange(N) for _ in range(rnd.randint(1, 9)))
    el = []
    for _ in range(rnd.randint(1, 3)):
        c = rnd.choice(divisors(N)); x0 = rnd.randrange(N); el += [(x0 + c * j) % N for j in range(N // c)]
    for _ in range(rnd.randint(0, 2)): el.append(rnd.randrange(N))
    return sorted(el)
tot = 0; bad = 0; withpat = 0
for M, primes, T in [(6, (3, 3), 1500), (6, (3, 5), 1500), (12, (3, 3), 1500), (12, (3, 5), 1200), (12, (5, 3), 1200), (12, (3, 3, 3), 800), (18, (3, 5), 1000), (20, (5, 3), 1000),
                     (24, (3, 7), 800), (10, (5, 5, 3), 800), (2, (3, 5, 7), 1500), (3, (3, 3, 5), 1500), (45, (3, 5), 600), (50, (5, 3), 600), (54, (3, 3), 600), (12, (3, 5, 7), 400)]:
    s = 1
    for r in primes: s *= r
    nb = 0; npat = 0
    for _ in range(T):
        A = random_multiset(M); P0 = pattern(A, M, with_one=True); B = A; N = M
        for r in primes: B = lift_once(B, N, r); N *= r
        ok = (len(B) == len(A) and sorted(y % M for y in B) == A and pattern(B, N, with_one=True) == P0)
        nb += not ok; npat += bool(P0)
    tot += T; bad += nb; withpat += npat
    print(f'M = {M}, s = {s} (primes {primes}), Z_{M * s}: {T} random multisets ({npat} with a nonempty pattern); final pattern differs from the pattern on Z_M: {nb}', flush=True)
print(f'TOTAL {tot} multisets, {withpat} with a nonempty pattern; failures: {bad}')

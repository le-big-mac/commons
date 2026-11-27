"""The proof of Corollary 19 for general s = 2^j s': lift a multiset on Z_M (M = p^n q) once for each prime factor of s, the factors 2 first
(Lemma 18, with the signs of Lemma 17), then the odd primes (Lemma 16), and test that the multiset on Z_{Ms} has, among ALL divisors of Ms
(1 included), exactly the divisors the multiset on Z_M had, and the same number of elements.  Random multisets.
usage: python -I -B s4_iterated.py"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift/second')
import random
from cyc import divisors, pattern
import s2_lift2 as L2
rnd = random.Random(4)
def lift_odd(A, N, r):
    """Lemma 16: every element to its lift with t = 0, one single element to its lift with t = 1"""
    k = 0; n1 = N
    while n1 % r == 0: n1 //= r; k += 1
    R = r ** (k + 1); rk = r ** k
    def L(x, t):
        for j in range(r):
            y = x + j * N
            if y % R == (x % rk) + rk * t: return y
        raise AssertionError
    i0 = rnd.randrange(len(A))
    return [L(x, 1 if i == i0 else 0) for i, x in enumerate(A)]
def lift_two(A, N):
    k, N1 = L2.odd_part(N)
    c = rnd.choice(sorted(set(x % 2 ** k for x in A)))
    return L2.lift_along_2(A, N, c, rnd.choice(L2.roles(N1)), rnd.choice((1, -1)))
tot = 0; bad = 0; withpat = 0
CASES = [  # (p, q, n, j, odd primes of s')
    (2, 3, 1, 1, ()), (3, 2, 1, 1, ()), (3, 2, 2, 1, ()), (5, 2, 2, 1, ()), (3, 5, 1, 1, ()), (3, 5, 1, 2, ()), (3, 5, 2, 1, ()), (5, 3, 2, 2, ()), (3, 2, 2, 3, ()),
    (2, 3, 2, 1, (3,)), (3, 2, 2, 1, (3,)), (3, 2, 2, 1, (5,)), (3, 5, 1, 1, (7,)), (3, 5, 1, 2, (3, 7)), (3, 5, 1, 1, (3, 5)), (5, 3, 1, 3, (7,)), (2, 5, 2, 2, (3,)),
    (3, 7, 1, 1, (5,)), (3, 5, 2, 1, (11,)), (2, 3, 0, 2, (5, 7)), (3, 2, 0, 3, (3, 5)), (7, 3, 1, 2, (5,)), (3, 5, 0, 1, (3, 7, 11)),
]
for p, q, n, j, odd in CASES:
    M = p ** n * q; s = 2 ** j
    for r in odd: s *= r
    T = 600 if M * s <= 400 else (300 if M * s <= 1500 else 120); nb = 0; npat = 0
    for _ in range(T):
        A = L2.rand_multiset(M); P0 = pattern(A, M, with_one=True); B = list(A); N = M
        for _ in range(j): B = lift_two(B, N); N *= 2
        for r in odd: B = lift_odd(B, N, r); N *= r
        ok = len(B) == len(A) and sorted(y % M for y in B) == sorted(A) and pattern(B, N, with_one=True) == P0
        nb += not ok; npat += bool(P0)
    tot += T; bad += nb; withpat += npat
    print(f'M = {M} = {p}^{n}*{q}, s = {s} = 2^{j}' + ''.join(f'*{r}' for r in odd) + f', Z_{M * s}: {T} random multisets ({npat} with a nonempty pattern); '
          f'final pattern differs from the pattern on Z_M: {nb}', flush=True)
print(f'TOTAL {tot} multisets, {withpat} with a nonempty pattern; failures: {bad}')

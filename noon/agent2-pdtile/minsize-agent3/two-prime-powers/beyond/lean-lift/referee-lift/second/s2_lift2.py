"""Lemma 18 of the paper (lifting along 2), implemented from the paper's text, with the signs of Lemma 17 (s1_signs.paper_signs).
N = 2^k N', N' = p^a q^b (p != q odd primes, a, b >= 0).  A a nonempty multiset on Z_N.
(a) the two lifts of x are congruent modulo 2^(k+1) to x mod 2^k (low) and to (x mod 2^k) + 2^k (high)   [asserted for every x];
(b) choose a class c modulo 2^k that holds an element of A (EVERY such class is tried), B = the residues modulo N' of the elements of A in
    it, signs by Lemma 17 (both roles of the two primes where there are two; a random x*; both preferences), sign + lifted low, sign - high,
    all other classes low.  Test: for every divisor d of 2N (d = 1 included): Phi_d | A'  iff  d | N and Phi_d | A; same number of
    elements; reduction modulo N is A.
(c) control: every element low.   usage: python -I -B s2_lift2.py [small]"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift/second')
import itertools, random
from cyc import divisors, pattern
import s1_signs as S1
rnd = random.Random(77)
def odd_part(N):
    k = 0
    while N % 2 == 0: N //= 2; k += 1
    return k, N
def factor(n):
    f = {}; d = 3
    while n > 1:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 2
    return f
def roles(N1):
    """the ways to write N' = p^a q^b for Lemma 17: list of (p, a, q)"""
    f = factor(N1)
    if len(f) == 0: return [(3, 0, 5), (5, 0, 3)]
    if len(f) == 1:
        (p, a), = f.items(); others = [r for r in (3, 5, 7) if r != p][:2]
        return [(p, a, others[0]), (others[0], 0, p), (p, a, others[1])]
    assert len(f) == 2, 'odd part with three primes: not Lemma 17'
    (p, a), (q, b) = f.items()
    return [(p, a, q), (q, b, p)]
def lifts(x, N, k):
    lo = x % 2 ** k; ys = (x, x + N); res = sorted(y % 2 ** (k + 1) for y in ys)
    assert res == [lo, lo + 2 ** k], (x, N)                                              # claim (a)
    low = ys[0] if ys[0] % 2 ** (k + 1) == lo else ys[1]; high = ys[1] if low == ys[0] else ys[0]
    return low, high
def lift_along_2(A, N, c, role, prefer):
    k, N1 = odd_part(N); p, a, q = role
    cls = [j for j, x in enumerate(A) if x % 2 ** k == c]; assert cls
    B = [A[j] % N1 for j in cls]
    sg, sC = S1.paper_signs(B, p, a, q, rnd.randrange(len(B)), prefer)
    out = [lifts(x, N, k)[0] for x in A]
    for j, e in zip(cls, sg):
        if e == -1: out[j] = lifts(A[j], N, k)[1]
    return out
def test(A, N, stats, fails):
    k, N1 = odd_part(N); M = 2 * N
    PA = pattern(A, N, with_one=True); want = frozenset(d for d in divisors(M) if N % d == 0 and d in PA)
    for c in sorted(set(x % 2 ** k for x in A)):
        for role in roles(N1):
            for prefer in (1, -1):
                A2 = lift_along_2(A, N, c, role, prefer)
                assert sorted(y % N for y in A2) == sorted(A) and len(A2) == len(A)
                stats['lifts'] += 1
                if pattern(A2, M, with_one=True) != want: fails.append((N, A, c, role, prefer))
    stats['multisets'] += 1
    stats['all low keeps the pattern'] += pattern([lifts(x, N, k)[0] for x in A], M, with_one=True) == want
    stats['with a nonempty pattern'] += bool(want)
def rand_multiset(N):
    r = rnd.random()
    if r < 0.4: return sorted(rnd.randrange(N) for _ in range(rnd.randint(1, 12)))
    el = []
    for _ in range(rnd.randint(1, 3)):
        cc = rnd.choice(divisors(N)); x0 = rnd.randrange(N); el += [(x0 + cc * j) % N for j in range(N // cc)]
    for _ in range(rnd.randint(0, 2)): el.append(rnd.randrange(N))
    return sorted(el)
if __name__ == '__main__':
    small = len(sys.argv) > 1
    tot = dict.fromkeys(['multisets', 'lifts', 'all low keeps the pattern', 'with a nonempty pattern'], 0); fails = []
    print('--- exhaustive: every multiset on Z_N with at most S elements')
    EXH = [(1, 7), (2, 7), (3, 7), (4, 6), (5, 6), (6, 5), (8, 5), (9, 5), (10, 4), (12, 4), (15, 4), (16, 4), (18, 4), (20, 3), (24, 3), (25, 3), (27, 3), (30, 3),
           (36, 3), (45, 3), (50, 3), (7, 5), (14, 4), (21, 3), (49, 3), (63, 3), (75, 2), (100, 2)]
    if small: EXH = EXH[:8]
    for N, S in EXH:
        st = dict.fromkeys(tot, 0)
        for s in range(1, S + 1):
            for A in itertools.combinations_with_replacement(range(N), s): test(list(A), N, st, fails)
        for key in tot: tot[key] += st[key]
        print(f'N = {N} (k = {odd_part(N)[0]}, odd part {odd_part(N)[1]}), 2N = {2 * N}, S = {S}: {st}', flush=True)
    print('--- random multisets')
    RND = [(18, 2000), (50, 1500), (12, 2000), (36, 1500), (100, 1000), (150, 800), (72, 1000), (90, 800), (126, 600), (180, 600), (200, 500), (225, 500), (300, 400),
           (144, 600), (96, 800), (162, 600), (500, 300), (45, 1200), (75, 1000), (175, 500), (198, 400), (294, 300), (15, 2000), (60, 1200), (350, 300), (400, 300)]
    if small: RND = [(18, 300), (50, 300)]
    for N, Tn in RND:
        st = dict.fromkeys(tot, 0)
        for _ in range(Tn): test(rand_multiset(N), N, st, fails)
        for key in tot: tot[key] += st[key]
        print(f'N = {N} (k = {odd_part(N)[0]}, odd part {odd_part(N)[1]}), 2N = {2 * N}, {Tn} random: {st}', flush=True)
    print('TOTAL:', tot); print('FAILURES:', len(fails), fails[:3])

"""Reader's test of a lift that needs no general position when the prime is odd.
Claim: let M = N r, r an odd prime, N = r^k N' with r not dividing N'.  Lift a nonempty multiset A on Z_N to Z_M as follows: an element
x goes to the y in Z_M with y = x mod N' and y mod r^(k+1) equal to (x mod r^k) taken in [0, r^k); except ONE element, which gets
(x mod r^k) + r^k instead.  Then the lifted multiset has exactly the pattern of A (no divisor of M that does not divide N comes in).
Tested on random structured multisets with the reader's pattern test.  As a control, the same with the plain lift (no element moved)
and with r = 2 is counted too.   usage: lift_lemma.py [trials] [seed]"""
import sys, random, collections
sys.path.insert(0, '/home/agent3/pq2/rule/reader')
from pat import pattern, divisors
T = int(sys.argv[1]) if len(sys.argv) > 1 else 4000; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 11)
def rnd(N):
    v = [0] * N
    for _ in range(random.randint(1, 3)):
        c = random.choice(divisors(N)); x = random.randrange(N)
        for j in range(N // c): v[(x + c * j) % N] += random.randint(1, 2) if random.random() < 0.2 else 1
    if random.random() < 0.3: v[random.randrange(N)] += 1
    return v
def crt(a, n1, b, n2):
    for y in range(n1 * n2):
        if y % n1 == a and y % n2 == b: return y
def lift(v, N, r, move):
    M = N * r; rk = 1
    while (N // rk) % r == 0: rk *= r
    N1 = N // rk
    out = [0] * M; moved = not move
    for x, w in enumerate(v):
        for _ in range(w):
            b = x % rk
            if not moved: b += rk; moved = True
            out[crt(x % N1, N1, b, rk * r)] += 1
    return out
cnt = collections.Counter()
CASES = [(45, 5), (75, 3), (15, 3), (15, 5), (9, 5), (25, 3), (3, 5), (5, 3), (12, 3), (4, 3), (20, 5), (4, 5), (2, 3), (6, 3), (10, 5), (1, 3), (3, 3), (5, 5), (9, 3), (36, 3), (100, 5),
         (18, 2), (50, 2), (6, 2), (10, 2), (9, 2), (25, 2), (2, 2)]
for _ in range(T):
    N, r = random.choice(CASES); v = rnd(N); pa = pattern(v, N, routes=2)
    for move in (True, False):
        l = lift(v, N, r, move); assert sum(l) == sum(v)
        red = [0] * N
        for y, w in enumerate(l): red[y % N] += w
        assert red == v
        same = pattern(l, N * r, routes=2) == pa
        cnt[('r odd' if r % 2 else 'r = 2', 'one element moved' if move else 'plain lift', 'pattern kept' if same else 'A DIVISOR CAME IN')] += 1
for k in sorted(cnt): print(f'{cnt[k]:6d}', *k)

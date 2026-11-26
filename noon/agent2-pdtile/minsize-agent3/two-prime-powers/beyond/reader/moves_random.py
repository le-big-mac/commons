"""Reader's random test of the pattern claimed for each move of section 2, on multisets with nontrivial patterns (random sums of
cosets, sometimes with a point added), with the reader's pattern test.   usage: moves_random.py [trials] [seed]"""
import sys, random, math, collections
sys.path.insert(0, '/home/agent3/pq2/rule/reader')
from pat import pattern, divisors
T = int(sys.argv[1]) if len(sys.argv) > 1 else 3000; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
def rnd(N):
    """a random multiset on Z_N: a few cosets of random subgroups, sometimes convolved, sometimes a stray point"""
    v = [0] * N
    for _ in range(random.randint(1, 3)):
        c = random.choice(divisors(N)); x = random.randrange(N)
        for j in range(N // c): v[(x + c * j) % N] += 1
    if random.random() < 0.3: v[random.randrange(N)] += 1
    return v
def pat(v, N): return set(pattern(v, N, routes=2))
cnt = collections.Counter()
for _ in range(T):
    M = random.choice((36, 100, 225, 12, 18, 45, 75, 20, 50))
    # convolution: exactly the union
    a, b = rnd(M), rnd(M); c = [0] * M
    for x, wa in enumerate(a):
        if wa:
            for y, wb in enumerate(b):
                if wb: c[(x + y) % M] += wa * wb
    assert pat(c, M) == pat(a, M) | pat(b, M); cnt['convolution: exactly the union'] += 1
    # sum with a translate: contains the intersection, nothing from exactly one of the two; note when something else comes in
    t = random.randrange(M); s = [a[x] + b[(x - t) % M] for x in range(M)]
    ps, pa, pb = pat(s, M), pat(a, M), pat(b, M)
    assert pa & pb <= ps and not (ps & (pa ^ pb)); cnt['sum: intersection inside, symmetric difference outside'] += 1
    if ps != pa & pb: cnt['   sum: a divisor outside both came in'] += 1
    # reduce modulo N: the pattern cut down to the divisors of N
    N = random.choice(divisors(M)); r = [0] * N
    for x, w in enumerate(a): r[x % N] += w
    assert pat(r, N) == {d for d in pa if N % d == 0}; cnt['reduction: the pattern cut down'] += 1
    # lift from Z_N to Z_M: the divisors of N are kept; note when another comes in
    l = [0] * M
    for x, w in enumerate(r):
        for _ in range(w): l[x + N * random.randrange(M // N)] += 1
    pl = pat(l, M); assert {d for d in pl if N % d == 0} == pat(r, N); cnt['lift: divisors of N kept exactly'] += 1
    if pl != pat(r, N): cnt['   lift: a divisor not dividing N came in'] += 1
    # dilation: c B on Z_N for B on Z_K, K = N / c
    N = M; c_ = random.choice([d for d in divisors(N) if d > 1]); K = N // c_; B = rnd(K)
    d_ = [0] * N
    for x, w in enumerate(B): d_[(c_ * x) % N] += w
    pB = pat(B, K)
    assert pat(d_, N) == {d for d in divisors(N) if d > 1 and (d // math.gcd(d, c_)) in pB}; cnt['dilation: exactly {d : d/gcd(d,c) in pattern(B)}'] += 1
    # stacking: classes r + c Z_N carry B_r on Z_K, all of one size
    Bs = [rnd(K) for _ in range(c_)]; w = max(sum(B) for B in Bs)
    for B in Bs:
        while sum(B) < w: B[random.randrange(K)] += 1          # pad to equal sizes
    s_ = [0] * N
    for r_, B in enumerate(Bs):
        for x, m in enumerate(B): s_[r_ + c_ * x] += m
    ps = pat(s_, N); inter = set.intersection(*[pat(B, K) for B in Bs])
    must = {d for d in divisors(c_) if d > 1} | {d for d in divisors(N) if c_ % d and (d // math.gcd(d, c_)) in inter}
    assert must <= ps and sum(s_) == c_ * w; cnt['stacking: divisors of c and the common ones are in; size c w'] += 1
    if ps != must: cnt['   stacking: another divisor came in'] += 1
for k, v in cnt.items(): print(f'{v:6d}  {k}')

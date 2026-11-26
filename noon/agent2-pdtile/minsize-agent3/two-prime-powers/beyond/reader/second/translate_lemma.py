"""Second pass: the lemma on translates, on random structured multisets (sums of cosets), where cancellation does happen.
For each pair: every translate t of A2; the pattern of A1 + (A2 + t); the translates that let a divisor outside D1 and D2 in must lie,
for each such divisor d, in one residue class modulo d, and some translate must give exactly D1 ∩ D2.   usage: translate_lemma.py [trials] [seed]"""
import sys, random, collections
sys.path.insert(0, '/home/agent3/pq2/rule/reader')
from pat import pattern, divisors
T = int(sys.argv[1]) if len(sys.argv) > 1 else 400; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
def rnd(N):
    v = [0] * N
    for _ in range(random.randint(1, 3)):
        c = random.choice(divisors(N)); x = random.randrange(N)
        for j in range(N // c): v[(x + c * j) % N] += 1
    return v
cnt = collections.Counter(); worst = 0.0
for _ in range(T):
    M = random.choice((225, 45, 75, 15, 9, 25, 27, 441 if random.random() < 0.05 else 45))
    a, b = rnd(M), rnd(M); pa, pb = set(pattern(a, M, 2)), set(pattern(b, M, 2)); want = pa & pb
    badfor = collections.defaultdict(set); good = 0
    for t in range(M):
        ps = set(pattern([a[x] + b[(x - t) % M] for x in range(M)], M, 2))
        assert want <= ps and not (ps & (pa ^ pb))
        if ps == want: good += 1
        for d in ps - want: badfor[d].add(t)
    for d, ts in badfor.items(): assert len({t % d for t in ts}) == 1 and len(ts) <= M // d, (M, d, sorted(ts))
    assert good >= 1
    cnt['pairs'] += 1; cnt['pairs where some translate lets a divisor in'] += (good < M); worst = max(worst, (M - good) / M)
print(dict(cnt), '; largest share of translates that let a divisor in: %.3f' % worst)

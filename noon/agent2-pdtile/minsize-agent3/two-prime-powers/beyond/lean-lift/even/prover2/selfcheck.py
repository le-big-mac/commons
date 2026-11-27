# compare lib2 with complex evaluation
import random, cmath, sys
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *
random.seed(1)
cnt = 0; nb = 0
for n in [6, 12, 18, 30, 36, 45, 60]:
    for _ in range(150):
        m = random.randint(1, 7)
        if random.random() < 0.5:
            B = [random.randrange(n) for _ in range(m)]
        else:
            g = random.choice([d for d in divisors(n) if d > 1]); B = [random.randrange(0, n, n // g) for _ in range(m)]
        sg = [random.choice([1, -1]) for _ in range(m)]
        for d in divisors(n):
            z = cmath.exp(2j * cmath.pi / d)
            val = sum(s * z ** x for s, x in zip(sg, B))
            b = is_bad(B, sg, n, d)
            assert b == (abs(val) < 1e-9), (n, B, sg, d)
            cnt += 1; nb += b
print('levels compared', cnt, 'bad', nb)
print(cyclo(1), cyclo(2), cyclo(6), cyclo(12))

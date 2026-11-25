"""(f) 'Phi_{r^e} does not divide A'  <=>  'two classes modulo r^e inside one class modulo r^(e-1) hold different numbers of elements'
(the exact pair set used in t1search.py: c1 != c2, c1 = c2 mod r^(e-1)), against divides(), on random and structured sets."""
import random
from common import *
random.seed(3); tot = pos = bad = 0
for (p, a, q, b) in [(2, 2, 3, 2), (2, 3, 3, 2), (2, 2, 3, 3), (2, 4, 3, 2), (2, 3, 5, 2), (3, 2, 5, 1)]:
    M = p ** a * q ** b; PPs = [(p, e) for e in range(1, a + 1)] + [(q, e) for e in range(1, b + 1)]
    for trial in range(1500):
        if trial % 2: A = sorted(random.sample(range(M), random.randint(1, M)))
        else:
            A = set(); ds = [d for d in divisors(M) if 1 < d < M]
            for _ in range(random.randint(1, 3)):
                r = random.choice(ds); H = [(M // r) * t for t in range(r)]
                for _ in range(random.randint(1, max(1, M // r // 2))):
                    c = random.randrange(M); co = {(c + h) % M for h in H}
                    if not (co & A): A |= co
            if random.random() < 0.3: A ^= {random.randrange(M)}
            A = sorted(A)
            if not A: continue
        for r, e in PPs:
            re_, rl = r ** e, r ** (e - 1); cnt = [sum(1 for x in A if x % re_ == c) for c in range(re_)]
            differ = any(cnt[c1] >= cnt[c2] + 1 for c1 in range(re_) for c2 in range(re_) if c1 != c2 and c1 % rl == c2 % rl)
            dv = divides(re_, A, M); tot += 1; pos += dv; bad += (differ == dv)
print(f"(f) prime-power encoding against divides(): {tot} (set, prime power) pairs, {pos} divisible, disagreements: {bad}")

import sys, time, random
sys.path.insert(0, "/home/agent3/lean/lift-check/even/quarter/three")
from badlib import bad_count
from fractions import Fraction as F
lim = {5: F(1,4), 6: F(11,32), 7: F(7,32), 8: F(39,128)}
random.seed(271127)
t0 = time.time(); cnt = {m: 0 for m in lim}; best = {m: F(0) for m in lim}; fails = []
mods = [15, 45, 105, 135, 225, 315, 75, 9, 27, 21, 63, 35, 945]
while time.time() - t0 < 50:
    n = random.choice(mods); m = random.choice([5, 6, 7, 8])
    mode = random.random()
    if mode < 0.4:
        B = [random.randrange(n) for _ in range(m)]
    elif mode < 0.7:
        pool = [random.randrange(n) for _ in range(random.randint(2, 5))]
        B = [random.choice(pool) for _ in range(m)]
    else:  # CRT-structured: residues mod 5 spread, mod 3-part clustered
        base = random.randrange(n); steps = [n // p for p in (3, 5, 7, 9) if n % p == 0]
        B = [(base + sum(random.randrange(3) * random.choice(steps) for _ in range(2))) % n for _ in range(m)]
    c, mm = bad_count(n, B); s = F(c, 2**mm); cnt[m] += 1
    if s > best[m]: best[m] = s
    if s > lim[m]: fails.append((n, B, s))
print("tested", cnt, "largest", {m: str(v) for m, v in best.items()}, "violations", fails[:5], len(fails))

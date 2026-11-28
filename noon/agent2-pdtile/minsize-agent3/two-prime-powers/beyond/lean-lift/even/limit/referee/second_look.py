"""Second look: (A) fours at the deepest level of the 3-chain against pairs; (B) the configurations of the run
t_lemma1.py 2 (seed 2) generated again without counting, to tally what kinds they were; (C) the same for the run
t_heavy.py 5 (seed 5).  (B) and (C) repeat the generating code of those programs line by line; the totals that the
runs printed serve as checks that the same multisets are generated."""
import sys, math, random, statistics
from fractions import Fraction
from collections import Counter
sys.path.insert(0, '/home/agent3/lean/lift-check/even/limit/referee')
from lib import *
import t_lemma1

# (A)
P = lambda bs, k: [b for b in bs for _ in range(k)]
for L, pairs, fours in ((3, [], [1, 2]), (9, [1, 2], [3, 6]), (27, [1, 2, 3, 6], [9, 18]), (81, [1, 2, 3, 6, 9, 18], [27, 54])):
    kp = K(L, P(pairs + fours, 2))[0]; kf = K(L, P(pairs, 2) + P(fours, 4))[0]
    print(f"(A) Z_{L}: pairs at {pairs + fours}: K_0 = {kp};  with fours at {fours}: K_0 = {kf};  difference {kf - kp}")

# (B) t_lemma1.py seed 2: 9490 configurations, 34766 cases
MODS = [3, 5, 7, 9, 15, 15, 21, 25, 27, 33, 35, 45, 45, 63, 75, 105, 105, 135, 165, 315]
rng = random.Random(2); n_conf = 0; n_l1 = 0; mods = Counter(); shapes = Counter(); biggest = Counter(); ms = []; two_big = 0
while n_conf < 9490:
    d = rng.choice(MODS); shape, sizes = t_lemma1.config(rng, d)
    items = sorted(sizes.items()); m = sum(a for _, a in items); vals = sorted(a for _, a in items)
    G = 1
    for a in vals[:-1]: G *= a + 1
    if G > 250000 or m < 2: continue
    n_conf += 1; mods[d] += 1; shapes[shape] += 1; ms.append(m)
    occ = set(vals) | ({0} if len(items) < d else set())
    n_l1 += sum(1 for a in occ if a != m)
    biggest[vals[-1]] += 1
    if len(vals) > 1 and vals[-2] >= 10: two_big += 1
print(f"(B) t_lemma1 seed 2 again: {n_conf} configurations, {n_l1} cases (the run printed 34766: {'same' if n_l1 == 34766 else 'DIFFERENT'})")
print(f"    by modulus: {sorted(mods.items())}")
print(f"    by shape (A one or two heavy, B equal, C many small, D two or three large): {sorted(shapes.items())}")
print(f"    m from {min(ms)} to {max(ms)}, median {statistics.median(ms)}; largest class: 2001 in {biggest[2001]}, 600 in {biggest[600]}, >= 150 in {sum(v for k, v in biggest.items() if k >= 150)}; second largest class >= 10 in {two_big}")

# (C) t_heavy.py seed 5: 110172 multisets
rng = random.Random(5); n_cases = 0; n_L1 = 0; n_proper = 0; n_zero = 0; ms = []; hs = []; rs = []; spread = 0; nLn = 0
while n_cases < 110172:
    n = rng.choice((9, 15, 15, 27, 45, 45, 63, 105, 105, 135)); L = rng.choice(divisors(n)); x = rng.randrange(L)
    cls = [b for b in range(n) if b % L == x]
    Hres = rng.sample(cls, rng.randint(1, min(3, len(cls))))
    Hitems = [(b, rng.choice((1, 2, 3, 5, 8, 20, 21))) for b in Hres]
    D = []
    for _ in range(rng.randint(0, 3)):
        ps = [q for q in (3, 5, 7) if n % q == 0]; p = rng.choice(ps); x0 = rng.choice(Hres + [rng.randrange(n)])
        mult = rng.choice((1, 1, 2))
        for j in range(1, p): D += [(x0 + j * (n // p)) % n] * mult
        if rng.random() < 0.3: D.append(rng.randrange(n))
    D = D[:9]
    moved = 0
    if rng.random() < 0.3:
        moved = rng.randint(1, 2); D += [rng.choice(cls) for _ in range(moved)]
    if moved == 0:
        extra = [b for b in D if b % L == x]; D = [b for b in D if b % L != x]
        for b in extra: Hitems.append((b, 1))
    h = sum(a for _, a in Hitems); r = len(D)
    g = 1
    for _, a in merge(n, Hitems + [(b, 1) for b in D]): g *= a + 1
    if g > 300000: continue
    n_cases += 1; n_zero += moved > 0; n_L1 += L == 1; n_proper += 1 < L < n; nLn += L == n
    ms.append(h + r); hs.append(h); rs.append(r); spread += len({b for b, _ in Hitems}) >= 2
ok = (n_L1, n_proper, n_zero) == (21486, 66789, 32475)
print(f"(C) t_heavy seed 5 again: {n_cases} multisets; L = 1 in {n_L1}, 1 < L < n in {n_proper}, L = n in {nLn}, decoration containing 0 in {n_zero} (the run printed 21486, 66789, 32475: {'same' if ok else 'DIFFERENT'})")
print(f"    m from {min(ms)} to {max(ms)}, median {statistics.median(ms)}; h from {min(hs)} to {max(hs)}, median {statistics.median(hs)}, h >= 20 in {sum(1 for v in hs if v >= 20)}; "
      f"r from {min(rs)} to {max(rs)}, r = 0 in {sum(1 for v in rs if v == 0)}; H on two or more different elements of Z_n in {spread}")

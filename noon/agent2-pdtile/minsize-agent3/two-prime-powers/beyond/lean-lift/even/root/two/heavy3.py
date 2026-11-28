# Theorem 1 beyond the table: exact share of signings bad at some power of 3 (1 included) for h copies of 0 and a
# decoration on Z_(3^v), by the definition of F_i through class sums (Python integers, exact).  usage: heavy3.py seed seconds
import sys, math, random, time, itertools
from math import comb
from fractions import Fraction
seed = int(sys.argv[1]); budget = float(sys.argv[2]); rnd = random.Random(seed); t0 = time.time()
def share(v, h, res, mult):
    n = 3 ** v; D = len(res); num = 0; den = 1 << (h + sum(mult))
    rngs = [range(-k, k + 1, 2) for k in mult]
    for sums in itertools.product(*rngs):
        w = 1
        for k, s in zip(mult, sums): w *= comb(k, (k + s) // 2)
        cls = [0] * n
        for b, s in zip(res, sums): cls[b] += s
        T = set(); T.add(-sum(sums))                      # bad at 1
        for i in range(1, v + 1):                         # bad at 3^i: every group at level i flat; heavy class is class 0
            q = 3 ** i; g = 3 ** (i - 1); cs = [0] * q
            for c in range(n): cs[c % q] += cls[c]
            ok = True; need = None
            for grp in range(g):
                a, b, c2 = cs[grp], cs[grp + g], cs[grp + 2 * g]
                if grp == 0:
                    if b != c2: ok = False; break
                    need = b - a                          # T + a = b
                elif not (a == b == c2): ok = False; break
            if ok: T.add(need)
        for t in T:
            if abs(t) <= h and (h + t) % 2 == 0: num += w * comb(h, (h + t) // 2)
    return Fraction(num, den)
worst = {0: (0, None), 1: (0, None)}; cnt = 0; big = 0
fams = [(2, [1, 2], [2, 2]), (2, [1, 2, 3, 6], [2, 2, 2, 2]), (3, [1, 2, 3, 6, 9, 18], [2, 2, 2, 2, 2, 2]), (1, [1, 2], [1, 1]), (2, [1, 2, 3, 6], [1, 1, 1, 1]), (2, [3, 6, 1, 2], [6, 6, 2, 2])]
jobs = [(v, h, res, mult) for (v, res, mult) in fams for h in (10, 11, 100, 101, 1000, 1001, 1500, 3000, 3001, 10000, 10001)]
def check(v, h, res, mult):
    global cnt, big
    m = h + sum(mult); s = share(v, h, res, mult); x = float(s) * math.sqrt(m); par = m % 2
    lim = ((0.9379 if m > 1000 else 0.9487) if par == 0 else (0.40 if m > 200 else 0.4331))
    assert s * s * m <= Fraction(lim) ** 2, ("FAIL", v, h, res, mult, x)
    cnt += 1; big += (m > 1000)
    if x > worst[par][0]: worst[par] = (x, (3 ** v, h, res, mult))
    return x
for (v, h, res, mult) in jobs:
    x = check(v, h, res, mult)
    if h >= 3000: print(f"  Z_{3**v}: {h} copies of 0 and {res} x {mult}: m={h+sum(mult)}, share*sqrt(m) = {x:.6f}")
while time.time() - t0 < budget:
    v = rnd.choice([1, 2, 2, 3]); n = 3 ** v; D = rnd.randint(1, 6)
    res = rnd.sample(range(1, n), min(D, n - 1)); mult = [rnd.choice([1, 1, 2, 2, 2, 3, 4, 6]) for _ in res]
    while math.prod(k + 1 for k in mult) > 3000: mult[mult.index(max(mult))] //= 2
    h = rnd.choice([rnd.randint(1, 60), rnd.randint(60, 1000), rnd.randint(1001, 4000)])
    check(v, h, res, mult)
print(f"seed {seed}: {cnt} multisets ({big} with m > 1000), NO FAILURE of share*sqrt(m) <= 0.9487 (m even), 0.9379 (m even > 1000), 0.4331 (m odd), 0.40 (m odd > 200)")
for par in (0, 1): print(f"  parity {par}: largest share*sqrt(m) = {worst[par][0]:.6f} at (modulus, copies of 0, residues, multiplicities) = {worst[par][1]}")

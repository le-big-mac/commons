"""Multisets that are NOT one heavy element with a small decoration: two or three heavy elements, a different heavy
class at each prime, classes of equal size.  Exact share of bad signings (multiplicities), divided by c_m, against
the largest K known for the parity of m (78764625/67108864 for even m, 337/512 for odd m).
usage: t_shapes.py SEED SECONDS"""
import sys, math, random, time
from fractions import Fraction
sys.path.insert(0, '/home/agent3/lean/lift-check/even/limit/referee')
from lib import *
KNOWN = (Fraction(78764625, 67108864), Fraction(337, 512))
best = {}; n_cases = 0; above = 0; DEADLINE = [float('inf')]
def run(name, n, heavy, sizes, deco):
    global n_cases, above
    if time.time() > DEADLINE[0]: return
    items = list(zip(heavy, sizes)) + deco
    s, m = share(n, items); q = s / c(m); n_cases += 1
    flag = ""
    if q > KNOWN[m % 2]: above += 1; flag = "   ABOVE the largest known K of its parity"
    key = (name.split(':')[0], m % 2)
    if q > best.get(key, (Fraction(-1),))[0]: best[key] = (q, n, items, m)
    print(f"{name}: Z_{n} heavy {list(zip(heavy, sizes))} with {deco}: m = {m} ({'even' if m % 2 == 0 else 'odd'}) share/c_m = {float(q):.5f}{flag}", flush=True)

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); secs = float(sys.argv[2]); t0 = time.time()
    P = lambda *bs: [(b, 2) for b in bs]; O = lambda *bs: [(b, 1) for b in bs]
    fam2 = [("two heavy", 3, (0, 1), []), ("two heavy", 3, (0, 1), P(2)), ("two heavy", 3, (0, 1), O(2)),
            ("two heavy", 9, (0, 3), P(6, 1, 2)), ("two heavy", 9, (0, 1), P(2, 3, 6)), ("two heavy", 9, (0, 3), O(6) + P(1, 2)),
            ("two heavy", 15, (0, 5), O(10) + P(3, 6, 9, 12)), ("two heavy", 15, (0, 3), O(6, 9, 12, 5, 10)), ("two heavy", 15, (0, 3), P(6, 9, 12, 5, 10)),
            ("two heavy", 45, (0, 15), P(30, 9, 18, 27, 36)), ("two heavy", 45, (0, 9), O(18, 27, 36) + P(15, 30)),
            ("two heavy", 105, (0, 35), O(70, 21, 42, 63, 84, 15, 30, 45, 60, 75, 90)), ("two heavy", 27, (0, 9), P(18, 3, 6, 1, 2))]
    fam3 = [("three heavy, equal classes", 3, (0, 1, 2), []), ("three heavy, equal classes", 9, (0, 3, 6), P(1, 2)), ("three heavy", 9, (0, 1, 2), P(3, 6)),
            ("a different heavy class at each prime", 15, (0, 3, 5), []), ("a different heavy class at each prime", 15, (0, 3, 5), O(10, 6, 9, 12)),
            ("a different heavy class at each prime", 15, (0, 3, 5), P(10, 6, 9, 12)), ("a different heavy class at each prime", 105, (0, 15, 21), O(35, 70, 42, 63, 84)),
            ("three heavy, equal classes", 15, (0, 5, 10), P(3, 6, 9, 12))]
    DEADLINE[0] = t0 + secs * 0.45
    for a in (100, 101, 500):
        for name, n, heavy, deco in fam2:
            for sizes in ((a, a), (a, a + 1), (a + 1, a + 1), (a, 3 * a), (a, 3 * a + 1)):
                run(name, n, heavy, sizes, deco)
                if time.time() - t0 > secs * 0.45: break
    DEADLINE[0] = t0 + secs * 0.8
    for a in (40, 41, 90):
        for name, n, heavy, deco in fam3:
            for sizes in ((a, a, a), (a, a, a + 1), (a + 1, a + 1, a), (2 * a, a, a + 1)):
                run(name, n, heavy, sizes, deco)
                if time.time() - t0 > secs * 0.8: break
    DEADLINE[0] = float('inf')
    while time.time() - t0 < secs:      # random: 2 or 3 heavy residues in one coset pool, a small random decoration
        n = rng.choice((9, 15, 15, 27, 45, 45, 105)); ps = [q for q in (3, 5, 7) if n % q == 0]
        pool = set()
        for _ in range(rng.randint(1, 3)):
            p = rng.choice(ps); x0 = rng.choice([0] + list(pool)) if pool else 0
            pool |= {(x0 + j * (n // p)) % n for j in range(p)}
        pool = sorted(pool); nh = rng.choice((2, 2, 3))
        if len(pool) < nh: continue
        heavy = rng.sample(pool, nh); deco = [(b, rng.choice((1, 1, 2, 2, 4))) for b in pool if b not in heavy and rng.random() < 0.85]
        g = 1
        for _, a in deco: g *= a + 1
        a = rng.choice((60, 61, 150, 151)) if nh == 2 else rng.choice((30, 31, 50))
        if g * (a + 4) ** (nh - 1) > 400000: continue
        sizes = tuple(a + rng.randint(0, 3) for _ in range(nh))
        run("random", n, heavy, sizes, deco)
    print(f"{n_cases} multisets; above the largest known K of their parity: {above}")
    for key in sorted(best):
        q, n, items, m = best[key]
        print(f"  largest share/c_m, {key[0]}, m {'even' if key[1] == 0 else 'odd'}: {float(q):.5f} at Z_{n} {items} (m = {m})")

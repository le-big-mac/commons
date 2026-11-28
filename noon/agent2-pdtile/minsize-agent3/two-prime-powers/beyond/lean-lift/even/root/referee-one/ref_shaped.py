# Referee's own: shaped multisets with multiplicities, all lemma checks of ref_test.analyse.
import sys, math, random, time
import ref_test as rt

def kprod(mult):
    K = 1
    for hb in mult.values():
        K *= hb + 1
    return K

def phi(n):
    r = n
    for p in rt.factor(n):
        r = r // p * (p - 1)
    return r

def gen(rnd):
    kind = rnd.randint(0, 8)
    if kind == 0:   # heavy 0, one or two elements in each nonzero class modulo some primes of n
        n = rnd.choice([15, 21, 45, 105, 315, 75, 1155])
        f = rt.factor(n)
        mult = {0: rnd.randint(4, 45)}
        for p in f:
            if rnd.random() < 0.8:
                t = rnd.choice([1, 1, 2])
                for u in range(1, p):
                    b = u * (n // p) % n
                    mult[b] = mult.get(b, 0) + t
        return n, mult
    if kind == 1:   # deep tree of 3 (and maybe 5): full groups at every level, pairs/fours/singles, heavy top
        a = rnd.randint(2, 5)
        n = 3 ** a * rnd.choice([1, 1, 5])
        mult = {0: rnd.randint(2, 30)}
        for i in range(a):
            t = rnd.choice([1, 2, 2, 4])
            for u in (1, 2):
                b = u * 3 ** i * (n // 3 ** a) % n
                mult[b] = mult.get(b, 0) + t
        if n % 5 == 0 and rnd.random() < 0.7:
            t = rnd.choice([1, 2])
            for u in range(1, 5):
                mult[u * (n // 5) % n] = mult.get(u * (n // 5) % n, 0) + t
        return n, mult
    if kind == 2:   # classes of equal size: every residue of a subgroup with the same multiplicity
        n = rnd.choice([9, 15, 27, 45, 21, 63, 25, 75])
        ds = [d for d in rt.divisors(n) if 1 < d <= 9]
        d = rnd.choice(ds)
        t = rnd.randint(1, 6)
        mult = {u * (n // d): t for u in range(d)}
        if rnd.random() < 0.4:
            b = rnd.randrange(n)
            mult[b] = mult.get(b, 0) + rnd.randint(1, 3)
        return n, mult
    if kind == 3:   # two or three heavy elements and a few light ones
        n = rnd.choice([9, 15, 27, 45, 105, 135, 225])
        mult = {}
        for _ in range(rnd.randint(2, 3)):
            b = rnd.randrange(n)
            mult[b] = mult.get(b, 0) + rnd.randint(5, 30)
        for _ in range(rnd.randint(0, 4)):
            b = rnd.randrange(n)
            mult[b] = mult.get(b, 0) + rnd.randint(1, 2)
        return n, mult
    if kind == 4:   # a different heavy class at each prime: heavy elements at 0, n/p (for p | n), light elsewhere
        n = rnd.choice([15, 45, 105, 315])
        mult = {0: rnd.randint(3, 20)}
        for p in rt.factor(n):
            b = (n // p) * rnd.randint(1, p - 1) % n
            mult[b] = mult.get(b, 0) + rnd.randint(2, 12)
        for _ in range(rnd.randint(0, 3)):
            b = rnd.randrange(n)
            mult[b] = mult.get(b, 0) + 1
        return n, mult
    if kind == 5:   # all multiplicities even, few residues, several levels
        n = rnd.choice([9, 27, 81, 45, 135, 225, 243])
        mult = {}
        for _ in range(rnd.randint(3, 8)):
            b = rnd.randrange(n) if rnd.random() < 0.5 else rnd.randrange(9) * (n // 9)
            mult[b] = mult.get(b, 0) + rnd.choice([2, 2, 4, 6, 10])
        return n, mult
    if kind == 6:   # unions of cosets of subgroups with multiplicities
        n = rnd.choice([45, 63, 75, 105, 225, 315])
        mult = {}
        for _ in range(rnd.randint(1, 3)):
            d = rnd.choice([x for x in rt.divisors(n) if 1 < x <= 7])
            off = rnd.randrange(n)
            t = rnd.randint(1, 3)
            for u in range(d):
                b = (off + u * (n // d)) % n
                mult[b] = mult.get(b, 0) + t
        return n, mult
    if kind == 7:   # heavy class of several residues (same class mod p), singles in the other classes mod p
        n = rnd.choice([9, 27, 45, 75, 25, 125, 49, 147])
        p = rnd.choice(list(rt.factor(n)))
        mult = {}
        for _ in range(rnd.randint(2, 4)):
            b = p * rnd.randrange(n // p)
            mult[b] = mult.get(b, 0) + rnd.randint(2, 9)
        for u in range(1, p):
            b = (u + p * rnd.randrange(n // p)) % n
            mult[b] = mult.get(b, 0) + rnd.choice([1, 1, 2])
        return n, mult
    # kind 8: two full cells at a level of 3 (odd and even cells together), pattern 9 or 27
    n = rnd.choice([9, 27, 81])
    mult = {}
    for c0 in rnd.sample(range(3), rnd.randint(2, 3)):
        full = rnd.random() < 0.7
        par = rnd.randint(1, 2)
        for u in range(3):
            if full or u == 0:
                t = par + 2 * rnd.randint(0, 3)
                b = (c0 + 3 * u) * (n // 9) % n
                mult[b] = mult.get(b, 0) + t
    return n, mult

if __name__ == "__main__":
    budget = float(sys.argv[1])
    rnd = random.Random(int(sys.argv[2]))
    t0 = time.time()
    kinds = {}
    mmax = 0
    while time.time() - t0 < budget:
        n, mult = gen(rnd)
        m = sum(mult.values())
        if kprod(mult) * phi(n) > 2.5e7 or m > 120 or m < 3:
            continue
        mmax = max(mmax, m)
        rt.analyse(n, mult)
    print("largest m:", mmax)
    rt.report()

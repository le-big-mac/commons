# Hill-climbing search for a multiset on an odd modulus with a large share of bad signings (exact arithmetic).
# usage: search.py seconds seed m_lo m_hi n1 n2 ...
# During the climb only the divisors d whose prime-power levels are all live are tested (step-down, in the texts);
# the best multiset of every (n, m) is then recounted with ALL divisors of n and the two counts are compared.
import sys, time, random
from fractions import Fraction
from badlib import bad_count, divisors, factor

def live_divs(n, B):
    fac = factor(n)
    live = {}
    for p, a in fac.items():
        live[p] = []
        for i in range(1, a + 1):
            groups = {}
            for b in set(B):
                groups.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
            if any(len(s) == p for s in groups.values()):
                live[p].append(i)
    ds = [1]
    for p in fac:
        ds = [d * p ** i for d in ds for i in [0] + live[p]]
    return sorted(ds)

def score(n, B):
    t, m = bad_count(n, B, divs=live_divs(n, B))
    return t

def crt_units(n):
    fac = factor(n)
    out = []
    for p, a in fac.items():
        q = p ** a
        c = n // q
        e = (c * pow(c, -1, q)) % n       # idempotent: 1 mod q, 0 mod the rest
        out.append((p, a, q, e))
    return out

def random_start(n, m, rng, units):
    # per prime power: one heavy residue plus singles, or uniform, at random
    B = [0] * m
    for p, a, q, e in units:
        mode = rng.random()
        for j in range(m):
            if mode < 0.45:
                r = 0 if rng.random() < 0.6 else rng.randrange(q)
            elif mode < 0.75:
                r = rng.randrange(q)
            else:
                r = rng.choice([0, q // p, 2 * (q // p) % q]) if rng.random() < 0.7 else rng.randrange(q)
            B[j] = (B[j] + e * r) % n
    return B

def mutate(n, B, rng, units):
    B = B[:]
    j = rng.randrange(len(B))
    t = rng.random()
    if t < 0.3:
        B[j] = rng.randrange(n)
    elif t < 0.5:
        B[j] = B[rng.randrange(len(B))]
    else:
        p, a, q, e = rng.choice(units)
        B[j] = (B[j] + e * rng.randrange(1, q)) % n
        if rng.random() < 0.3:
            j2 = rng.randrange(len(B))
            p, a, q, e = rng.choice(units)
            B[j2] = (B[j2] + e * rng.randrange(1, q)) % n
    return B

def main():
    secs = float(sys.argv[1]); seed = int(sys.argv[2]); mlo = int(sys.argv[3]); mhi = int(sys.argv[4])
    ns = [int(x) for x in sys.argv[5:]]
    rng = random.Random(seed)
    jobs = [(n, m) for n in ns for m in range(mlo, mhi + 1)]
    per = secs / len(jobs)
    for n, m in jobs:
        units = crt_units(n)
        t0 = time.time()
        best = (-1, None)
        evals = 0; restarts = 0
        while time.time() - t0 < per:
            B = random_start(n, m, rng, units)
            s = score(n, B); evals += 1; restarts += 1
            stall = 0
            while stall < 60 and time.time() - t0 < per:
                B2 = mutate(n, B, rng, units)
                s2 = score(n, B2); evals += 1
                if s2 >= s:
                    if s2 > s:
                        stall = 0
                    else:
                        stall += 1
                    B, s = B2, s2
                else:
                    stall += 1
            if s > best[0]:
                best = (s, sorted(B))
        full, _ = bad_count(n, best[1])
        fr = Fraction(full, 2 ** m)
        flag = 'ABOVE 3/8 !!!' if fr > Fraction(3, 8) else ''
        print(f'n={n} m={m} best bad share {fr} = {float(fr):.5f} (live-divisor count {best[0]}, all-divisor count {full}, '
              f'{"equal" if full == best[0] else "DIFFER"}) evals={evals} restarts={restarts} B={best[1]} {flag}', flush=True)

if __name__ == '__main__':
    main()

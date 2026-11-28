# Search among HEAVY multisets (few distinct residues, large multiplicities), sizes up to 30: the count goes over the
# signed sums of the distinct residues (product of (k_r + 1) configurations), not over all signings.  Exact arithmetic.
# usage: search2.py seconds seed m_lo m_hi n1 n2 ...
import sys, time, random
from fractions import Fraction
from badlib import bad_count, factor
from search import live_divs, crt_units

def score(n, B):
    return bad_count(n, B, divs=live_divs(n, B))[0]

def main():
    secs = float(sys.argv[1]); seed = int(sys.argv[2]); mlo = int(sys.argv[3]); mhi = int(sys.argv[4])
    ns = [int(x) for x in sys.argv[5:]]
    rng = random.Random(seed)
    jobs = [(n, m) for n in ns for m in range(mlo, mhi + 1)]
    per = secs / len(jobs)
    for n, m in jobs:
        units = crt_units(n)
        t0 = time.time(); best = (-1, None); evals = 0
        while time.time() - t0 < per:
            D = rng.randint(3, 9)
            pool = []
            for _ in range(D):
                b = 0
                for p, a, q, e in units:
                    b = (b + e * (rng.randrange(p) * (q // p) if rng.random() < 0.7 else rng.randrange(q))) % n
                pool.append(b)
            heavy = rng.choice(pool)
            B = [heavy if rng.random() < 0.55 else rng.choice(pool) for _ in range(m)]
            s = score(n, B); evals += 1; stall = 0
            while stall < 40 and time.time() - t0 < per:
                B2 = B[:]
                j = rng.randrange(m)
                if rng.random() < 0.75:
                    B2[j] = rng.choice(B)
                else:
                    p, a, q, e = rng.choice(units)
                    old = B2[j]; new = (old + e * rng.randrange(1, q)) % n
                    if rng.random() < 0.5:
                        B2 = [new if b == old else b for b in B2]      # move a whole heavy residue
                    else:
                        B2[j] = new
                if len(set(B2)) > 10:
                    stall += 1; continue
                s2 = score(n, B2); evals += 1
                if s2 >= s:
                    stall = 0 if s2 > s else stall + 1
                    B, s = B2, s2
                else:
                    stall += 1
            if s > best[0]:
                best = (s, sorted(B))
        full, _ = bad_count(n, best[1])
        fr = Fraction(full, 2 ** m)
        flag = 'ABOVE 3/8 !!!' if fr > Fraction(3, 8) else ''
        print(f'n={n} m={m} best bad share {fr} = {float(fr):.5f} (all-divisor count {"equal" if full == best[0] else "DIFFER"}) '
              f'evals={evals} distinct residues={len(set(best[1]))} B={best[1]} {flag}', flush=True)

main()

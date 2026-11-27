"""Local search for supports W with a large first-order bound R(W) (see ranksum.py): does the first-order count of
Proposition P close for every odd m when 15 | n?  Starts: random, and one designed start; moves: add, remove or replace
one element.  usage: ranksearch.py n1 starts steps seed [d]
With the last argument d the search maximises R_d over supports with an odd number of elements instead of R."""
import sys, random
from fractions import Fraction
from ranksum import R

def search(n1, starts, steps, seed, dang=False):
    random.seed(seed); best = (Fraction(0), None)
    for s in range(starts):
        size = random.randint(5, 11); W = set(random.sample(range(n1), size))
        if dang and len(W) % 2 == 0: W.add(next(x for x in range(n1) if x not in W))
        r = R(n1, sorted(W))[1 if dang else 0]
        for _ in range(steps):
            V = set(W); mv = random.random()
            if mv < 0.3 and len(V) > 3: V.discard(random.choice(sorted(V)))
            elif mv < 0.6 and len(V) < 14: V.add(random.randrange(n1))
            else:
                V.discard(random.choice(sorted(V))); V.add(random.randrange(n1))
            if dang and len(V) % 2 == 0:
                if random.random() < 0.5 and len(V) > 3: V.discard(random.choice(sorted(V)))
                else: V.add(random.randrange(n1))
            if len(V) < 2 or (dang and len(V) % 2 == 0): continue
            r2 = R(n1, sorted(V))[1 if dang else 0]
            if r2 >= r: W, r = V, r2
        if r > best[0]: best = (r, sorted(W))
        print(f"  n'={n1} start {s}: R = {float(r):.4f} with {len(W)} elements", flush=True)
    print(f"n'={n1}: largest {'R_d (|W| odd)' if dang else 'R'} found {best[0]} = {float(best[0]):.5f} at {best[1]}", flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'designed':
        # seven elements on Z_315: two pairs congruent modulo 45, three elements filling a class modulo 3 over the classes modulo 9
        import itertools
        n1 = 315
        def crt(r9, r5, r7): return next(x for x in range(315) if x % 9 == r9 and x % 5 == r5 and x % 7 == r7)
        W = [crt(1, 0, 0), crt(1, 0, 1), crt(2, 1, 2), crt(2, 1, 3), crt(0, 2, 4), crt(3, 3, 5), crt(6, 4, 6)]
        r, rd = R(n1, sorted(W)); print('designed W on Z_315:', sorted(W), 'R =', r, float(r), ' R_d =', float(rd))
    else:
        search(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), len(sys.argv) > 5)

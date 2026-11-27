"""The three facts of the referee's short proof of Theorem T, checked as SETS of signings, literally:
   F_d  = {signings: every class modulo 2^d has signed sum 0},  E_0 = F_0,  E_j = {level j bad},
   tau_j = negate the sign of every element whose position has remainder >= 2^(j-1) modulo 2^j.
   (1) F_0 >= F_1 >= ... >= F_k     (2) E_j == tau_j(F_(j-1))     (3) F_j <= E_j and F_j <= E_0
   and, when V has no 2-torsion, (4) F_d == E_0 & ... & E_d.
Groups: Z/3, Z/9, Z (no 2-torsion), and Z/2, Z/4, Z/6, also with the value 0 (hypotheses of Theorem T broken)."""
import itertools, random
def run(k, mod, values, count, mmax, seed, torsionfree):
    rng = random.Random(seed)
    P = 1 << k
    bad = 0
    for _ in range(count):
        m = rng.randint(1, mmax)
        fam = [(rng.randrange(P) if rng.random() < .7 else rng.choice([0, 1, P // 2]), rng.choice(values)) for _ in range(m)]
        red = (lambda x: x % mod) if mod else (lambda x: x)
        def csum(signs, d, res):
            return red(sum(s * v for s, (u, v) in zip(signs, fam) if u % (1 << d) == res))
        allsigns = list(itertools.product((1, -1), repeat=m))
        F = [set(s for s in allsigns if all(csum(s, d, r) == 0 for r in range(1 << d))) for d in range(k + 1)]
        E = [F[0]]
        for j in range(1, k + 1):
            half = 1 << (j - 1)
            E.append(set(s for s in allsigns
                         if all(csum(s, j, r) == csum(s, j, r + half) for r in range(half))))
        for j in range(1, k + 1):
            half = 1 << (j - 1)
            tau = lambda s: tuple(-x if (u % (1 << j)) >= half else x for x, (u, v) in zip(s, fam))
            ok = F[j] <= F[j - 1] and E[j] == set(tau(s) for s in F[j - 1]) and F[j] <= E[j] and F[j] <= E[0]
            if torsionfree:
                inter = set(allsigns)
                for i in range(j + 1): inter &= E[i]
                ok = ok and inter == F[j]
            bad += (not ok)
        union = set().union(*E)
        bad += (len(union) > 2 * len(F[0]) - len(F[k]))
    print(f"k = {k}, V = {'Z' if not mod else 'Z/%d' % mod}, values {values}: {count} families of 1..{mmax} elements, failures {bad}")
run(3, 3, [1, 2], 600, 8, 1, True)
run(4, 9, [1, 2, 3, 4, 6], 400, 8, 2, True)
run(3, 0, [1, -1, 2, 3], 600, 8, 3, True)
run(4, 0, [1, 2], 300, 8, 4, True)
run(3, 2, [1], 600, 8, 5, False)
run(3, 4, [1, 2, 3], 600, 8, 6, False)
run(3, 6, [1, 2, 3, 4, 5], 600, 8, 7, False)
run(3, 3, [0, 1, 2], 600, 8, 8, False)
run(3, 0, [0, 1, -1, 2], 600, 8, 9, False)

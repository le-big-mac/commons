# Theorem J for eight elements.  On Z_{n_3}, all 256 signings:
#   rho_2 >= 21/64;  the signings 3-bad at 2^j * e'' for some j and some e'' > 1 but at no 2^j have share <= 3/16
#   (those are 3-bad at a live level, by the step-down);
#   hence the share of 3-good signings is >= 9/64.
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *

def check(B, n3, st):
    m = len(B); k, odd = two_part(n3)
    S = all_signs(m, fix_first=False); tot = S.shape[0]
    bad3 = bad3_table(B, n3, S)
    two = np.zeros(tot, dtype=bool); other = np.zeros(tot, dtype=bool)
    for d in divisors(n3):
        if (d & (d - 1)) == 0: two |= bad3[d]
        else: other |= bad3[d]
    rho2 = 1 - Fr(int(two.sum()), tot)
    oth_all = Fr(int(other.sum()), tot)
    oth = Fr(int((other & ~two).sum()), tot)
    g3 = 1 - Fr(int((two | other).sum()), tot)
    assert rho2 >= Fr(21, 64), (B, n3, rho2)
    assert oth <= Fr(3, 16), (B, n3, oth)
    assert g3 >= Fr(9, 64), (B, n3, g3)
    st['n'] += 1; st['rho2'] = min(st['rho2'], rho2); st['oth'] = max(st['oth'], oth); st['g3'] = min(st['g3'], g3)

if __name__ == '__main__':
    rnd = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 71)
    reps = int(sys.argv[1])
    for n3 in [20, 40, 80, 100, 140, 280, 400, 560, 700, 1120]:
        st = {'n': 0, 'rho2': Fr(1), 'oth': Fr(0), 'g3': Fr(1)}
        k, odd = two_part(n3)
        def lift(u, w):
            return next(x for x in range(u % (1 << k), n3, 1 << k) if x % odd == w % odd)
        for t in range(reps):
            kind = t % 6
            if kind == 0: B = [rnd.randrange(n3) for _ in range(8)]
            elif kind == 1:   # five classes modulo 5 in one class modulo 2^j, three more, some of them doubles of earlier ones
                j = rnd.randint(0, k); base = rnd.randrange(n3)
                B = [(base + (1 << j) * (5 * rnd.randrange(n3) + c)) % n3 for c in range(5)]
                while len(B) < 8:
                    x = rnd.choice(B); B.append(rnd.choice([x, x, (x + n3 // 2) % n3, (x + (odd // 5) * 5 * rnd.randrange(8)) % n3, rnd.randrange(n3)]))
            elif kind == 2:   # the shape of the proof: a big class with all five subclasses, and a pair or a triple apart in the 2-tree
                u1, u2 = rnd.sample(range(1 << k), 2); w0 = rnd.randrange(odd)
                big = [lift(u1 if rnd.random() < 0.8 else u1 + (1 << (k - 1)), 5 * rnd.randrange(odd) + c) for c in range(5)]
                r = rnd.choice([2, 3]); small = [lift(u2 if rnd.random() < 0.7 else u2 + (1 << (k - 1)), w0) for _ in range(r)]
                B = big + small
                while len(B) < 8: B.append(rnd.choice(big))
            elif kind == 3 and odd % 7 == 0:   # seven classes modulo 7 and five modulo 5 at once, plus one
                B = [lift(rnd.randrange(1 << k) if rnd.random() < 0.3 else 0, 0) for _ in range(0)]
                B = [lift(rnd.choice([0, 0, 1 << (k - 1), rnd.randrange(1 << k)]), next(w for w in range(odd) if w % 7 == c and w % 5 == c % 5)) for c in range(7)] + [rnd.randrange(n3)]
            elif kind == 4:   # few residues modulo 2^k, random modulo the odd part
                us = [rnd.randrange(1 << k) for _ in range(rnd.randint(2, 3))]
                B = [lift(rnd.choice(us), rnd.randrange(odd)) for _ in range(8)]
            else:             # a coset of order 5, twice, shifted
                o = rnd.randrange(n3); o2 = (o + rnd.choice([n3 // 2, n3 // 4, 1, 5])) % n3
                B = [(o + s * (n3 // 5)) % n3 for s in range(5)] + [(o2 + s * (n3 // 5)) % n3 for s in range(3)]
            check(B, n3, st)
        print('n_3 =', n3, 'multisets of 8 elements:', st['n'], '| least rho_2', st['rho2'], '| largest share 3-bad at some 2^j e", e" > 1, but at no 2^j:', st['oth'], '| least share of 3-good', st['g3'], flush=True)

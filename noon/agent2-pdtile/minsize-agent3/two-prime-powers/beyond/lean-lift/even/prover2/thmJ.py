# Theorem J: six elements, every n.  On Z_{n_3}, n_3 = 2^k * n'' (gcd(n'', 6) = 1), all 64 signings:
#   share of 3-good signings >= rho_2 - 1/8, where rho_2 = share of signings 3-bad at no 2^j; rho_2 >= 5/16;
#   the signings 3-bad at 2^j * e'' for some j and some e'' > 1 have share <= 1/8; hence share of 3-good >= 3/16.
import sys, random, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *

def check(B, n3, st):
    m = len(B); k, odd = two_part(n3)
    S = all_signs(m, fix_first=False); tot = S.shape[0]
    bad3 = bad3_table(B, n3, S)
    two = np.zeros(tot, dtype=bool); other = np.zeros(tot, dtype=bool)
    for d in divisors(n3):
        if odd % 1 == 0 and (d & (d - 1)) == 0: two |= bad3[d]
        else: other |= bad3[d]
    rho2 = 1 - Fr(int(two.sum()), tot)
    oth = Fr(int((other & ~two).sum()), tot)
    g3 = 1 - Fr(int((two | other).sum()), tot)
    exc = False
    assert rho2 >= Fr(5, 16), (B, n3, rho2)
    assert oth <= Fr(1, 8), (B, n3, oth)
    assert g3 >= Fr(3, 16), (B, n3, g3)
    st['n'] += 1; st['rho2'] = min(st['rho2'], rho2); st['oth'] = max(st['oth'], oth); st['g3'] = min(st['g3'], g3)

if __name__ == '__main__':
    rnd = random.Random(61)
    for n3 in [20]:
        st = {'n': 0, 'rho2': Fr(1), 'oth': Fr(0), 'g3': Fr(1)}
        for B in multisets_with_zero(n3, 6): check(B, n3, st)
        print('n_3 =', n3, 'all multisets of 6 elements with 0:', st['n'], '| least rho_2', st['rho2'], '| largest share 3-bad at some 2^j e", e" > 1, but at no 2^j:', st['oth'], '| least share of 3-good', st['g3'], flush=True)
    for n3 in [40, 80, 100, 140, 200, 280, 400, 560, 700, 1120, 3080]:
        st = {'n': 0, 'rho2': Fr(1), 'oth': Fr(0), 'g3': Fr(1)}
        k, odd = two_part(n3)
        for t in range(4000):
            kind = t % 4
            if kind == 0: B = [rnd.randrange(n3) for _ in range(6)]
            elif kind == 1:   # one element in every class modulo 5 (a live level), all in one class modulo 2^j, plus one more
                j = rnd.randint(0, k); base = rnd.randrange(n3)
                B = [(base + (1 << j) * rnd.randrange(n3) * 5 + (1 << j) * c * (n3 // 5 if (n3 // 5) % 5 else 1)) % n3 for c in range(5)]
                B = [(base + (1 << j) * (5 * rnd.randrange(n3) + c)) % n3 for c in range(5)] + [rnd.randrange(n3)]
            elif kind == 2:   # a coset of order 5 shifted inside the 2-tree, plus one
                o = rnd.randrange(n3); B = [(o + s * (n3 // 5) + rnd.choice([0, 0, n3 // 2, n3 // 4])) % n3 for s in range(5)] + [rnd.randrange(n3)]
            else:             # five classes modulo 5, two residues modulo 2^k
                u = [rnd.randrange(1 << k) for _ in range(2)]
                B = []
                for c in list(range(5)) + [rnd.randrange(5)]:
                    w = (5 * rnd.randrange(odd) + c) % odd; uu = rnd.choice(u)
                    B.append(next(x for x in range(uu, n3, 1 << k) if x % odd == w))
            check(B, n3, st)
        print('n_3 =', n3, 'random and structured multisets of 6 elements:', st['n'], '| least rho_2', st['rho2'], '| largest share 3-bad only off the 2-part:', st['oth'], '| least share of 3-good', st['g3'], flush=True)

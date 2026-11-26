"""Corollary T's remark: for an up-set D of the divisors of M and a corner c, the set {0, c, 2c, ..., M - c} is fibred on every scale s in D
in KLMS's sense: for some prime p | s the polynomial F_p^s(X) = (X^s - 1)/(X^{s/p} - 1) divides its mask (X^M - 1)/(X^c - 1).
Both are products of distinct cyclotomic polynomials: F_p^s = prod of Phi_e over e | s with e not dividing s/p; the mask = prod of Phi_e over
e | M with e not dividing c.  So divisibility is inclusion of index sets.  Also checked: the prime can be any p in which s has a higher
exponent than c, and no other prime works."""
from lib import divisors, upsets, corners, prime_factors
def vp(x, p):
    k = 0
    while x % p == 0: x //= p; k += 1
    return k
tot = 0
for M in (12, 18, 36, 72, 100, 108, 144, 216, 225, 432):
    n = 0
    for D in upsets(M):
        for c in corners(M, D):
            mask = {e for e in divisors(M) if c % e}
            for s in D:
                good = [p for p in prime_factors(s) if {e for e in divisors(s) if (s // p) % e} <= mask]
                assert good == [p for p in prime_factors(s) if vp(s, p) > vp(c, p)] and good, (M, D, c, s)
                n += 1
    print(M, 'triples (up-set, corner, scale) checked:', n); tot += n
print('all', tot, 'triples: the corner coset is fibred on the scale, exactly in the directions where the scale has the higher exponent')

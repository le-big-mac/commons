"""exhaust7.py -- the seven statements of offord-lean tried by exhaustion on small cases, from their Lean text and the library's
definitions, in a program of my own (Noon, 28 Nov 2026).  Divisibility by Phi_d, the divisors and the signed sums are exact (whole
numbers; complex numbers as pairs of whole numbers).  It uses bad_at, divisors and cyclo of my program for the two statements of
"twice" (lean-union-try-28nov-agent2.py, beside this file).      python -I exhaust7.py
  1 card_signedSum_eq_le_real      a_i nonzero reals, v real:     #{eps : sum sg(eps_i) a_i = v} <= C(m, m div 2)
  2 card_signedSum_eq_le_complex   the same for nonzero complex numbers
  3 card_badAt_le_choose           d != 0:                        #{eps : Phi_d | P e eps} <= C(m, m div 2)
  4 not_badAt_one_of_odd           m odd:                         no eps is bad at 1
  5 card_exists_badAt_two_pow_le                                  #{eps : exists d | 2^k, bad at d} <= 2 C(m, m div 2)
  6 not_exists_badAt_two_pow_of_odd  m odd:                       no eps is bad at any divisor of 2^k
  7 card_exists_badAt_le_divisors  n' odd:                        #{eps : exists d | 2^k n', bad at d} <= 2 (d(n') C(m, m div 2))"""
import itertools, random, sys
from math import comb
import os, importlib.util
_sp = importlib.util.spec_from_file_location('union_exhaust', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lean-union-try-28nov-agent2.py')); _u = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_u)      # by its path: with -I the folder of this file is not searched
bad_at, divisors, cyclo = _u.bad_at, _u.divisors, _u.cyclo
def signings(m): return itertools.product((False, True), repeat=m)
def t12(trials, seed, cplx):
    rnd = random.Random(seed); eq = 0; n = 0
    for t in range(trials):
        m = rnd.randint(0, 11); span = rnd.choice([1, 1, 2, 3, 9])
        def draw():
            while True:
                z = (rnd.randint(-span, span), rnd.randint(-span, span) if cplx else 0)
                if z != (0, 0): return z
        a = [draw() for _ in range(m)]; counts = {}
        for eps in signings(m):
            s = (sum(x[0] if e else -x[0] for x, e in zip(a, eps)), sum(x[1] if e else -x[1] for x, e in zip(a, eps))); counts[s] = counts.get(s, 0) + 1
        top = max(counts.values()); bound = comb(m, m // 2); n += 1
        if top > bound: print('FAILS', 'complex' if cplx else 'real', a, top, bound); return False
        eq += top == bound
        # a value that no signed sum takes: the count is 0
        assert counts.get((10 ** 6, 0), 0) == 0
    print('%s: %d cases (0 to 11 numbers, whole%s, none zero; every value v that any signed sum takes, and one that none takes), none against it; the bound met with equality in %d' % ('2 complex' if cplx else '1 real', n, ' real and imaginary parts' if cplx else '', eq)); return True
def t3457(trials, seed):
    rnd = random.Random(seed); n3 = n5 = n7 = e3 = e5 = e7 = n4 = n6 = 0
    for t in range(trials):
        m = rnd.randint(0, 10); k = rnd.randint(0, 3); n1 = rnd.choice([1, 1, 3, 3, 5, 7, 9, 15]); N = 2 ** k * n1; d0 = rnd.choice([1, 2, 3, 4, 5, 6, 8, 9, 12, 15])
        e = [rnd.randrange(rnd.choice([N, 2 * N, 40])) for _ in range(m)]; C = comb(m, m // 2); D = divisors(N); D2 = divisors(2 ** k); c3 = c5 = c7 = 0
        for eps in signings(m):
            c3 += bad_at(e, eps, d0); b2 = any(bad_at(e, eps, d) for d in D2); c5 += b2; c7 += any(bad_at(e, eps, d) for d in D)
            if m % 2 == 1:
                if bad_at(e, eps, 1): print('4 FAILS', e, eps); return False
                if b2: print('6 FAILS', e, eps, k); return False
        n3 += 1; n5 += 1; n7 += 1; n4 += m % 2; n6 += m % 2
        if c3 > C: print('3 FAILS', e, d0, c3, C); return False
        if c5 > 2 * C: print('5 FAILS', e, k, c5, C); return False
        if c7 > 2 * len(divisors(n1)) * C: print('7 FAILS', e, k, n1, c7, C); return False
        e3 += c3 == C; e5 += c5 == 2 * C; e7 += c7 == 2 * len(divisors(n1)) * C
    print('3 one divisor: %d cases (d in 1, 2, 3, 4, 5, 6, 8, 9, 12, 15), none against it; equality in %d' % (n3, e3))
    print('4 odd number of elements, never bad at 1: %d cases with m odd, every signing, none bad' % n4)
    print('5 moduli 2^k: %d cases (k 0 to 3), none against it; equality in %d' % (n5, e5))
    print('6 odd number of elements on moduli 2^k: %d cases with m odd, every signing, none bad' % n6)
    print("7 every modulus: %d cases (k 0 to 3; n' in 1, 3, 5, 7, 9, 15), none against it; equality in %d" % (n7, e7)); return True
def self_test():
    assert comb(4, 2) == 6 and divisors(12) == [1, 2, 3, 4, 6, 12] and cyclo(4) == [1, 0, 1]
    # all numbers equal: the count at v = 0 is C(m, m/2) for m even, and at v = a for m odd
    for m in range(0, 9):
        c = sum(1 for eps in signings(m) if sum(1 if x else -1 for x in eps) == (m % 2)); assert c == comb(m, m // 2), (m, c)
    # d = 0 is rightly shut out of statement 3: with Mathlib's cyclotomic 0 = 1 every signing would be "bad"
    # exponents 0, 1 on the modulus 2: bad at 1 are +- and -+, bad at 2 are ++ and --: 4 = 2 * C(2, 1)
    e = [0, 1]; assert sum(any(bad_at(e, eps, d) for d in (1, 2)) for eps in signings(2)) == 4
    print('self-test: with all the numbers equal the count is exactly C(m, m div 2) for m = 0 to 8, so statement 1 cannot be improved; exponents 0, 1 on the modulus 2 give 4 = 2 C(2, 1), equality in statement 5')
if __name__ == '__main__':
    self_test(); ok = t12(3000, 'noon-O-1', False) and t12(3000, 'noon-O-2', True) and t3457(2500, 'noon-O-3'); sys.exit(0 if ok else 1)

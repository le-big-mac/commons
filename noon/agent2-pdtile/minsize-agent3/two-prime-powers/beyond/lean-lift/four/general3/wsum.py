"""The sum over levels in the union bound, with exact fractions.

mu(d) = max over primes p | d of v_p(d) * (p - 1)   (d odd, d > 1; mu is even)
A(t)  = #{odd d >= 1 : mu(d) <= t} = prod over odd primes p <= t + 1 of (1 + floor(t / (p - 1)))
W     = sum over odd d > 1 of 2^(-mu(d)) = sum over even t >= 2 of 2^(-t) * (A(t) - A(t - 2))

Printed:
 1. A(t) and the partial sums of W for t <= T0, and a proved bound for the tail t > T0.
 2. A direct enumeration of the divisors of n'_m (the group to which a multiset of m elements contracts)
    for small m, as a check of the formula with A(t).
 3. For every m: W_m = sum over d | n'_m, d > 1 of 2^(-mu(d)); c_m = C(m, m/2)/2^m (m even), 0 (m odd);
    the total W_m + c_m, and for even m the total with the sharper bound for the level d = 3.

usage: wsum.py [T0=400] [mmax=80]
"""
import sys
from fractions import Fraction as Fr
from math import comb, log


def odd_primes_upto(x):
    ps = []
    for k in range(3, x + 1, 2):
        if all(k % q for q in ps if q * q <= k):
            ps.append(k)
    return ps


def A(t, primes):
    r = 1
    for p in primes:
        if p - 1 > t:
            break
        r *= 1 + t // (p - 1)
    return r


def c(k):
    """max over b of P(sum of k independent uniform signs = b)"""
    return Fr(comb(k, k // 2), 2 ** k)


def main():
    T0 = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    primes = odd_primes_upto(T0 + 2)

    # ---- 1. partial sums of W
    print("1. W = sum over odd d > 1 of 2^(-mu(d))")
    print("   t   A(t)   #{d: mu(d) = t}   partial sum of W (float)")
    part = Fr(0)
    prev = 1
    partial = {0: Fr(0)}
    for t in range(2, T0 + 1, 2):
        a = A(t, primes)
        part += Fr(a - prev, 2 ** t)
        partial[t] = part
        if t <= 40 or t % 50 == 0:
            print(f"  {t:3d}  {a}  {a - prev}  {float(part):.12f}")
        prev = a
    # tail: #{d : mu(d) = t} <= A(t) <= (t/2 + 1) * exp(K t / 3),  K = sum_k ln(1 + 1/k)/k  (see the result file)
    # K <= sum_{k < 2000} ln(1+1/k)/k + 1/1999
    K = sum(log(1 + 1 / k) / k for k in range(1, 2000)) + 1 / 1999 + 1e-9
    rate = K / 3 - log(2)          # ln of (A-bound growth per unit t) minus ln 2  (negative)
    # sum over even t > T0 of (t/2+1) exp(rate t):  with u = t/2, x = exp(2 rate) < 1:
    # sum_{u > U} (u+1) x^u = x^(U+1) * ((U+2) - (U+1) x) / (1-x)^2
    from math import exp
    x = exp(2 * rate)
    U = T0 // 2
    tail = x ** (U + 1) * ((U + 2) - (U + 1) * x) / (1 - x) ** 2
    print(f"   K <= {K:.6f};  A(t) <= (t/2+1) * 2^({K / 3 / log(2):.4f} t);  tail over t > {T0}: <= {tail:.3e}")
    print(f"   W <= {float(part):.12f} + {tail:.3e}")
    # check the bound A(t) <= (t/2+1) exp(K t/3) on the computed range
    worst = max(log(A(t, primes)) - log(t / 2 + 1) - K * t / 3 for t in range(2, T0 + 1, 2))
    print(f"   check of A(t) <= (t/2+1) exp(K t/3) for even t <= {T0}: max of ln(lhs/rhs) = {worst:.4f} (must be <= 0)")
    # the same with the smaller T0 = 40 and T0 = 60 used in the text
    print(f"   x = exp(2K/3)/4 <= {x:.6f}")
    for T in (12, 40, 60):
        U = T // 2
        tl = x ** (U + 1) * ((U + 2) - (U + 1) * x) / (1 - x) ** 2
        print(f"   with T0 = {T}: partial sum = {partial[T]} = {float(partial[T]):.12f}, tail <= {tl:.3e}, W <= {float(partial[T]) + tl:.9f}")

    # ---- 2. direct enumeration for small m
    print("\n2. direct enumeration of the divisors of n'_m against the formula")
    def nprime(m):
        return [(p, (m - 1) // (p - 1)) for p in odd_primes_upto(m) if (m - 1) // (p - 1) >= 1]
    def W_direct(m):
        fac = nprime(m)
        tot = Fr(0)
        cnt = 0
        def rec(i, mu):
            nonlocal tot, cnt
            if i == len(fac):
                if mu > 0:
                    tot += Fr(1, 2 ** mu)
                    cnt += 1
                return
            p, a = fac[i]
            for e in range(a + 1):
                rec(i + 1, max(mu, e * (p - 1)))
        rec(0, 0)
        return tot, cnt
    def W_formula(m):
        # divisors of n'_m: v_p <= floor((m-1)/(p-1)); mu(d) <= t iff v_p <= floor(t/(p-1)) for all p,
        # so #{d | n'_m : mu(d) <= t} = A(min(t, m-1))
        tot = Fr(0)
        prev = 1
        for t in range(2, m, 2):
            a = A(t, primes)
            tot += Fr(a - prev, 2 ** t)
            prev = a
        return tot
    for m in range(1, 31):
        wd, cnt = W_direct(m)
        wf = W_formula(m)
        assert wd == wf, (m, wd, wf)
    print("   m = 1..30: the sum over the divisors d > 1 of n'_m equals the partial sum of W up to t = m - 1 (exact): ok")

    # ---- 3. totals
    print("\n3. m, W_m (divisors of n'_m), c_m, W_m + c_m, and for even m the total with the sharper level 3")
    print("   (sharper level 3: P(bad at 3) <= c_k / 2 with k = ceil(m/3), in place of 1/4)")
    bad_plain = []
    bad_sharp = []
    for m in range(1, mmax + 1):
        Wm = W_formula(m)
        cm = c(m) if m % 2 == 0 else Fr(0)
        tot = Wm + cm
        line = f"  m={m:3d}  W_m={float(Wm):.6f}  c_m={float(cm):.6f}  total={float(tot):.6f}"
        if tot >= 1:
            bad_plain.append(m)
        if m % 2 == 0 and m >= 3:
            k = -(-m // 3)
            sharp = tot - Fr(1, 4) + c(k) / 2 if m >= 3 else tot
            line += f"  sharper={float(sharp):.6f}"
            if sharp >= 1:
                bad_sharp.append(m)
        print(line)
    print("   m with W_m + c_m >= 1:", bad_plain)
    print("   even m with the sharper total >= 1:", bad_sharp)
    Winf = partial[T0] + Fr(tail).limit_denominator(10 ** 15) + Fr(1, 10 ** 12)
    print(f"   for m > {mmax}: W_m <= W <= {float(Winf):.9f}, c_m <= c_{mmax} = {float(c(mmax)):.6f}, total <= {float(Winf + c(mmax)):.6f}")


main()

"""Facts the blind referee reported that I had not counted, recounted here with a program of my own before they are used.
usage: python -I checks.py > checks.out      (numpy; one thread; a few minutes)

1. 9837 = 9 x 1093 is bounded, though the exceptional prime 1093 divides it (the round is added up).
2. 1143 = 9 x 127 is bounded though 9 divides phi(127) = 126; and for q = 9 r, r a prime from 5 to 400, which test tells
   bounded from unbounded: "9 divides r - 1" (the reason HAKMEM offers for 171) or "3 divides the order of 2 modulo r"?
3. The referee's one-line form of the rule, ord_m(2) differs from ord_rad(m)(2), against Fuchs's form for every odd m below 10^6.
4. The weighted share of bounded odd denominators up to 10^7 (the referee has 0.1062).
5. A first turn of a quarter (q = 4, where every prime of q is squared): where the turtle goes.
6. m = 1093^3 x 4373, found by the referee's reading: 1093^2 does not divide the order of 2 modulo 4373, which is 4 x 1093, so a
   rule worded "spoilt when l^(e-1) divides the other order" would call it bounded; Fuchs's form does not.  The round is added up."""
import math, sys
import numpy as np

N = 10 ** 7


def round_sum(m):
    xs = []; x = 1
    while True:
        xs.append(x); x = x * 2 % m
        if x == 1: break
    return abs(np.exp(2j * np.pi * np.array(xs) / m).sum()), len(xs)


if __name__ == '__main__':
    s, n = round_sum(9837)
    print(f"1. m = 9837 = 9 x 1093: the round of {n} steps sums to {s:.1e}; of the smaller odd multiples of 1093 (1093, 3279, 5465, 7651) none holds a square")
    s, n = round_sum(1143)
    print(f"2. m = 1143 = 9 x 127: the round of {n} steps sums to {s:.1e}; 126 is divisible by 9: {126 % 9 == 0}")
    def order(r):
        k, x = 1, 2 % r
        while x != 1: x = x * 2 % r; k += 1
        return k
    primes = [r for r in range(5, 400) if all(r % d for d in range(2, int(r ** 0.5) + 1))]
    by_phi = by_ord = 0
    for r in primes:
        truth = round_sum(9 * r)[0] < 1e-9                       # bounded?
        by_phi += ((r - 1) % 9 != 0) == truth                    # HAKMEM's reason read as a test: unbounded when 9 divides r - 1
        by_ord += (order(r) % 3 != 0) == truth
    print(f"   q = 9 r for the {len(primes)} primes r from 5 to 400, the truth by adding up the round: '9 divides r - 1' tells bounded from unbounded rightly for {by_phi}; '3 divides the order of 2 modulo r' for {by_ord}")
    sys.stdout.flush()

    spf = np.zeros(N + 1, dtype=np.int32)
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == 0:
            idx = np.arange(i * i, N + 1, i); idx = idx[spf[idx] == 0]; spf[idx] = i
    z = np.nonzero(spf == 0)[0]; spf[z] = z; spf = spf.tolist()
    def factor(m):
        out = []
        while m > 1:
            l = spf[m]; e = 0
            while m % l == 0: m //= l; e += 1
            out.append((l, e))
        return out
    ordmemo = {}
    def ord_pp(l, e):
        key = (l, e); o = ordmemo.get(key)
        if o is None:
            mod = l ** e; o = l ** (e - 1) * (l - 1)
            for r, _ in ([(l, 1)] if e > 1 else []) + factor(l - 1):
                while o % r == 0 and pow(2, o // r, mod) == 1: o //= r
            ordmemo[key] = o
        return o
    def val(o, l):
        k = 0
        while o % l == 0: o //= l; k += 1
        return k
    def mine(f):
        for l, e in f:
            if e < 2: continue
            here = val(ord_pp(l, e), l)
            if here > val(ord_pp(l, e - 1), l) and all(r == l or val(ord_pp(r, 1), l) < here for r, _ in f): return True
        return False
    agree = wrong = 0; w_all = w_b = 0; n_all = n_b = 0; w6 = None
    for m in range(3, N + 1, 2):
        f = factor(m); phi = m
        for l, e in f: phi = phi // l * (l - 1)
        sq = any(e >= 2 for l, e in f); b = sq and mine(f)
        if m < 10 ** 6:
            a = False
            if sq:
                om = 1; orad = 1
                for l, e in f: om = math.lcm(om, ord_pp(l, e)); orad = math.lcm(orad, ord_pp(l, 1))
                a = om != orad
            if a == b: agree += 1
            else: wrong += 1
        n_all += 1; w_all += phi
        if b: n_b += 1; w_b += phi
        if m == 999999: w6 = (n_b / n_all, w_b / w_all)
    print(f"3. every odd m from 3 to 999,999: 'the order of 2 modulo m differs from its order modulo the product of m's primes' agrees with Fuchs's form of the rule in {agree}; otherwise in {wrong}")
    print(f"4. odd m up to 10^6: bounded {w6[0]:.4f}, weighted {w6[1]:.4f} (the sealed run: 0.1316 and 0.1090); up to 10^7: bounded {n_b} = {n_b / n_all:.4f}, weighted {w_b / w_all:.4f}")
    # 5. a quarter turn: turn left a quarter, step; turn a half, step; turn a whole turn, step; ...
    turn, head, x, y, pts = 1, 0, 0.0, 0.0, []
    for k in range(8):
        head = (head + turn) % 4; turn = turn * 2 % 4
        x -= math.sin(2 * math.pi * head / 4); y += math.cos(2 * math.pi * head / 4); pts.append((round(x, 9) + 0.0, round(y, 9) + 0.0))
    print(f"5. a first turn of 1/4: the first eight corners are {pts}")
    m = 1093 ** 3 * 4373; x = 1; t = 0j; n = 0
    while True:
        t += complex(math.cos(2 * math.pi * x / m), math.sin(2 * math.pi * x / m)); n += 1; x = x * 2 % m
        if x == 1: break
    o = 1; y = 2 % 4373
    while y != 1: y = y * 2 % 4373; o += 1
    print(f"6. m = 1093^3 x 4373 = {m}: the order of 2 modulo 4373 is {o} = 4 x 1093; the round of {n} steps sums to {abs(t):.3f} (not nought); the order of 2 modulo 1093^3 is {364 * 1093}, divisible by 1093 once, as is {o}")

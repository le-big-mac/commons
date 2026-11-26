"""The turtle that turns twice as much each step (HAKMEM item 45; the book's GOSPEL): the sealed sheet's eight lines.
usage: python -I gospel.py > gospel.out        (numpy; one thread; some minutes)

The turtle steps at headings a, 2a, 4a, ... (in turns).  For a = p/m, m odd, the headings repeat with the order of 2
modulo m, and the path is bounded exactly when one round of the cycle sums to nought.
Nothing here uses the rule to decide whether a round sums to nought: the round is added up."""
import math, sys
import numpy as np

TOL = 1e-9


# ---------- whole-number arithmetic with roots of unity: is sum_r c[r] zeta^r = 0, zeta a primitive M-th root?
def polydiv(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(q) - 1, -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, y in enumerate(b): a[i + j] -= q[i] * y
    assert not any(a)
    return q

def cyclotomic(d, memo={}):
    if d not in memo:
        num = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0: num = polydiv(num, cyclotomic(e))
        memo[d] = num
    return memo[d]

def is_zero(c, M):
    """c[r]: whole-number coefficient of zeta^r, r = 0..M-1.  True exactly when the sum is 0."""
    phi = cyclotomic(M); deg = len(phi) - 1; a = list(c)
    for i in range(len(a) - 1, deg - 1, -1):
        t = a[i]
        if t:
            for k in range(deg + 1): a[i - deg + k] -= t * phi[k]
    return not any(a)


# ---------- arithmetic
def sieve(N):
    spf = list(range(N + 1))
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j: spf[j] = i
    return spf

def factor(m, spf):
    out = []
    while m > 1:
        l = spf[m]; e = 0
        while m % l == 0: m //= l; e += 1
        out.append((l, e))
    return out

def order_by_doubling(m):
    k, x = 1, 2 % m
    while x != 1: x = x * 2 % m; k += 1
    return k

def order_prime_power(l, e, spf, memo={}):
    """the order of 2 modulo l^e, from the factors of l^(e-1) (l - 1), checked by powering"""
    key = (l, e)
    if key not in memo:
        mod = l ** e; o = l ** (e - 1) * (l - 1)
        for r, _ in ([(l, 1)] if e > 1 else []) + factor(l - 1, spf):
            while o % r == 0 and pow(2, o // r, mod) == 1: o //= r
        memo[key] = o
    return memo[key]

def order(m, spf):
    o = 1
    for l, e in factor(m, spf): o = math.lcm(o, order_prime_power(l, e, spf))
    return o

def rule_orders(m, spf):
    """G1: some prime l with l^2 | m for which the order of 2 modulo m differs from its order modulo m / l"""
    f = factor(m, spf)
    if all(e < 2 for l, e in f): return False
    om = order(m, spf)
    return any(e >= 2 and order(m // l, spf) != om for l, e in f)

def rule_plain(m, spf):
    """G3: some prime power l^e, e >= 2, exactly dividing m with l^(e-1) not dividing the order of 2 modulo m / l^e"""
    for l, e in factor(m, spf):
        if e >= 2 and order(m // l ** e, spf) % l ** (e - 1) != 0: return True
    return False


# ---------- the round, added up
def cycle(m, p=1):
    xs = []; x = p % m
    while True:
        xs.append(x); x = x * 2 % m
        if x == p % m: return xs

def round_sum(m, p=1):
    xs = np.array(cycle(m, p)); return abs(np.exp(2j * np.pi * xs / m).sum()), len(xs)


def subgroups(n):
    G = [a for a in range(1, n) if math.gcd(a, n) == 1] if n > 2 else [1]
    def close(gens):
        H = {1}; frontier = [1]
        while frontier:
            new = []
            for h in frontier:
                for g in gens:
                    x = h * g % n
                    if x not in H: H.add(x); new.append(x)
            frontier = new
        return frozenset(H)
    found = {frozenset({1})}; todo = [frozenset({1})]
    while todo:
        H = todo.pop()
        for g in G:
            if g not in H:
                K = close(list(H) + [g])
                if K not in found: found.add(K); todo.append(K)
    return found


if __name__ == '__main__':
    N = 10 ** 6; spf = sieve(N)

    # ---- G1: the rule against the round added up
    agree = wrong = 0; least_nonzero = 9e9; largest_zero = 0.0; firstwrong = []
    for m in range(3, 20001, 2):
        s, n = round_sum(m); z = s < TOL; r = rule_orders(m, spf)
        assert n == order(m, spf) == (order_by_doubling(m) if m < 2000 else n)
        if z: largest_zero = max(largest_zero, s)
        else: least_nonzero = min(least_nonzero, s)
        if z == r: agree += 1
        else:
            wrong += 1
            if len(firstwrong) < 5: firstwrong.append(m)
    print(f"G1: odd m from 3 to 20,000, p = 1: the round sums to nought exactly when the rule says so in {agree}; otherwise in {wrong}" + (f" (first: {firstwrong})" if wrong else ""))
    print(f"    the largest sum called nought: {largest_zero:.1e}; the least sum not called nought: {least_nonzero:.4f}")
    agree = wrong = 0; cases = 0; least_nonzero = 9e9; largest_zero = 0.0
    for m in range(3, 1501, 2):
        c = np.zeros(m); c[cycle(m, 1)] = 1; F = np.abs(np.fft.fft(c)); r = rule_orders(m, spf)
        for p in range(1, m):
            if math.gcd(p, m) != 1: continue
            cases += 1; z = F[p] < TOL
            if z: largest_zero = max(largest_zero, F[p])
            else: least_nonzero = min(least_nonzero, F[p])
            if z == r: agree += 1
            else: wrong += 1
    print(f"    every p prime to m, odd m from 3 to 1,500 ({cases} turtles): agree in {agree}; otherwise in {wrong}; largest called nought {largest_zero:.1e}, least not called nought {least_nonzero:.4f}")
    agree = wrong = 0; zeros = 0
    for m in range(3, 401, 2):
        c = [0] * m
        for x in cycle(m, 1): c[x] += 1
        z = is_zero(c, m); r = rule_orders(m, spf); zeros += z
        if z == r: agree += 1
        else: wrong += 1
    print(f"    in exact whole-number arithmetic, odd m from 3 to 400, p = 1: agree in {agree}; otherwise in {wrong}; {zeros} of them sum to nought")
    # the control: the exact test and the float test on rounds that are not whole (the cycle less its last step) must say "not nought"
    no = tot = 0
    for m in (9, 25, 27, 45, 49, 75, 81, 99, 121, 125):
        c = [0] * m
        for x in cycle(m, 1)[:-1]: c[x] += 1
        tot += 1; no += (not is_zero(c, m)) and abs(np.exp(2j * np.pi * np.array(cycle(m, 1)[:-1]) / m).sum()) > 0.5
    print(f"    control: ten bounded m with one step left out of the round: both tests say 'not nought' for {no} of {tot}")
    sys.stdout.flush()

    # ---- G2: every subgroup of the units modulo n
    agree = wrong = 0; nsub = 0; zero_sub = 0; exact_agree = exact_n = 0; firstwrong = []
    for n in range(2, 201):
        ls = [l for l, e in factor(n, spf) if e >= 2]
        for H in subgroups(n):
            nsub += 1; hs = np.array(sorted(H)); s = abs(np.exp(2j * np.pi * hs / n).sum()); z = s < TOL
            r = any((1 + n // l) % n in H for l in ls)
            zero_sub += z
            if z == r: agree += 1
            else:
                wrong += 1
                if len(firstwrong) < 5: firstwrong.append((n, sorted(H)[:6]))
            if n <= 60:
                c = [0] * n
                for h in H: c[h % n] += 1
                exact_n += 1; exact_agree += (is_zero(c, n) == r)
    print(f"G2: n from 2 to 200, every subgroup of the units ({nsub} subgroups, {zero_sub} of which sum to nought): the sum is nought exactly when the subgroup holds 1 + n/l for a prime l with l^2 | n in {agree}; otherwise in {wrong}" + (f" (first: {firstwrong})" if wrong else ""))
    print(f"    in exact arithmetic for n up to 60: {exact_agree} of {exact_n} subgroups agree")
    sys.stdout.flush()

    # ---- G3: the plain rule against the rule by orders, every odd m below 10^6; and the counts for G5, G6, G8
    agree = wrong = 0; marks = (3000, 10 ** 4, 10 ** 5, 10 ** 6); stat = {}
    odd = bounded = nonsq = 0; w_all = w_b = w_ns = 0; firstwrong = []; blist = []; elist = []
    for m in range(3, N, 2):
        f = factor(m, spf); sq = any(e >= 2 for l, e in f); phi = m
        for l, e in f: phi = phi // l * (l - 1)
        if sq:
            a = rule_orders(m, spf); b = rule_plain(m, spf)
            if a == b: agree += 1
            else:
                wrong += 1
                if len(firstwrong) < 5: firstwrong.append(m)
        else: a = False; agree += 1
        odd += 1; w_all += phi
        if sq: nonsq += 1; w_ns += phi
        if a:
            bounded += 1; w_b += phi
            if len(blist) < 60: blist.append(m)
        elif sq and len(elist) < 40: elist.append(m)
        if m + 2 > min(k for k in marks if k >= m) or m + 2 >= N:
            mk = min(k for k in marks if k >= m)
            if mk not in stat: stat[mk] = (odd, bounded, nonsq, w_all, w_b, w_ns)
    print(f"G3: every odd m from 3 to 999,999: the plain rule and the rule by orders agree in {agree}; otherwise in {wrong}" + (f" (first: {firstwrong})" if wrong else ""))
    print("    bounded m: " + ", ".join(map(str, blist)))
    print("    m with the square of a prime that are not bounded: " + ", ".join(map(str, elist)))
    for mk in marks:
        o, b, ns, wa, wb, wn = stat[mk]
        print(f"G5/G6/G8 up to {mk:>7}: odd m {o}; bounded {b} = {b / o:.4f} of them; with a square {ns} = {ns / o:.4f}; bounded among those with a square {b / ns:.4f}; weighted by the number of fractions: bounded {wb / wa:.4f}, with a square {wn / wa:.4f}, bounded among those {wb / wn:.4f}")
    sys.stdout.flush()

    # ---- G4: HAKMEM's exceptions, and 1093
    for m, why in ((171, (19, 3)), (9009, (7, 3)), (2525, (101, 5))):
        s, n = round_sum(m); r, l = why
        print(f"G4: m = {m}: the round of {n} steps sums to {s:.4f} (not nought); the rule says {'bounded' if rule_orders(m, spf) else 'not bounded'}; ord_{r}(2) = {order(r, spf)}, which {l} divides: {order(r, spf) % l == 0}")
    for m in (1093 ** 2, 1093 ** 3):
        xs = []; x = 1; total = 0j; n = 0
        while True:
            total += complex(math.cos(2 * math.pi * x / m), math.sin(2 * math.pi * x / m)); n += 1; x = x * 2 % m
            if x == 1: break
        print(f"G4: m = 1093^{2 if m == 1093 ** 2 else 3} = {m}: the round of {n} steps sums to {abs(total):.6f}")

    # ---- G7: the primes r up to 10^6 for which 3, 5 or 9 divides the order of 2
    primes = [r for r in range(3, N, 2) if spf[r] == r]; cnt = {3: 0, 5: 0, 9: 0}
    for r in primes:
        o = order_prime_power(r, 1, spf)
        for d in cnt: cnt[d] += (o % d == 0)
    print(f"G7: odd primes r below 10^6: {len(primes)}; 3 divides ord_r(2) for {cnt[3] / len(primes):.4f} of them (3/8 = 0.3750); 5 for {cnt[5] / len(primes):.4f} (5/24 = {5 / 24:.4f}); 9 for {cnt[9] / len(primes):.4f} (1/8 = 0.1250)")

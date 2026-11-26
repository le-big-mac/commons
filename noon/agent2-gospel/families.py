"""The doubling turtle: the third sheet (families.md): more.py with four more families counted and each family's slope printed.
usage: python -I families.py > families.out        (numpy; one thread; a few minutes)

The rule used is the first sheet's (G1), in the form that asks only about one prime at a time: m is bounded exactly when
some prime power l^e exactly dividing m, e >= 2, has   v_l(ord_(l^e)(2))  >  v_l(ord_(l^(e-1))(2))   and
v_l(ord_(l^e)(2))  >  v_l(ord_r(2))  for every other prime r dividing m,   v_l being the number of times l divides.
Up to 10^6 its counts must be those of the sealed run (65,801 bounded of 94,714 with a square), and the script says whether they are."""
import math, sys
import numpy as np

N = 10 ** 7


def sieve(n):
    spf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == 0:
            idx = np.arange(i * i, n + 1, i); idx = idx[spf[idx] == 0]; spf[idx] = i
    z = np.nonzero(spf == 0)[0]; spf[z] = z
    return spf.tolist()


if __name__ == '__main__':
    spf = sieve(N)

    def factor(m):
        out = []
        while m > 1:
            l = spf[m]; e = 0
            while m % l == 0: m //= l; e += 1
            out.append((l, e))
        return out

    ordmemo = {}
    def ord_prime(r):
        o = ordmemo.get(r)
        if o is None:
            o = r - 1
            for s, _ in factor(r - 1):
                while o % s == 0 and pow(2, o // s, r) == 1: o //= s
            ordmemo[r] = o
        return o

    # the primes l whose square can divide an m below N, and how often l divides the order of 2 modulo l^e
    wief = {}
    for l in range(3, int(N ** 0.5) + 1, 2):
        if spf[l] == l:
            k = 2
            while pow(2, l - 1, l ** k) == 1: k += 1                      # l^(k-1) is the highest power of l dividing 2^(l-1) - 1
            if k - 2: wief[l] = k - 2                                     # that many factors of l are missing from the order of 2 modulo powers of l
    print(f"primes l below {int(N ** 0.5) + 1} with l^2 dividing 2^(l-1) - 1: {sorted(wief.items())}")

    def val(o, l):
        k = 0
        while o % l == 0: o //= l; k += 1
        return k

    def bounded(f):
        for l, e in f:
            if e < 2: continue
            w = wief.get(l, 0)
            here = max(e - 1 - w, 0); before = max(e - 2 - w, 0)          # v_l of the order of 2 modulo l^e and modulo l^(e-1)
            if here <= before: continue
            if all(r == l or val(ord_prime(r), l) < here for r, _ in f): return True
        return False

    marks = (10 ** 6, 10 ** 7); stat = {}
    odd = nonsq = bnd = 0; powerful = 0; powerful_not = []; bnd_not_powerful = 0; least_bnp = None
    fam = {121: [0, 0], 169: [0, 0], 81: [0, 0], 125: [0, 0], 9: [0, 0], 25: [0, 0], 27: [0, 0], 49: [0, 0]}     # m with exactly that prime power: how many, how many bounded
    for m in range(3, N + 1, 2):
        f = factor(m); odd += 1
        if not any(e >= 2 for _, e in f):
            pass
        else:
            nonsq += 1; b = bounded(f); bnd += b; pw = all(e >= 2 for _, e in f)
            if pw:
                powerful += 1
                if not b: powerful_not.append(m)
            elif b:
                bnd_not_powerful += 1
                if least_bnp is None: least_bnp = m
            for l, e in f:
                key = l ** e
                if key in fam: fam[key][0] += 1; fam[key][1] += b
        if m + 2 > marks[0] and marks[0] not in stat: stat[marks[0]] = (odd, nonsq, bnd, powerful, list(powerful_not), bnd_not_powerful, {k: tuple(v) for k, v in fam.items()})
    stat[marks[1]] = (odd, nonsq, bnd, powerful, list(powerful_not), bnd_not_powerful, {k: tuple(v) for k, v in fam.items()})

    o, ns, b, pw, pn, bnp, fm = stat[10 ** 6]
    print(f"up to 10^6: odd m {o}; with a square {ns}; bounded {b}  (the sealed run: 499999, 94714, 65801: {'the same' if (o, ns, b) == (499999, 94714, 65801) else 'DIFFERENT'})")
    R = {}
    for mk in marks:
        o, ns, b, pw, pn, bnp, fm = stat[mk]; R[mk] = b / ns
        print(f"up to {mk}: odd m {o}; with a square {ns} = {ns / o:.4f}; bounded {b} = {b / o:.4f} of all odd m and {b / ns:.4f} of those with a square")
        print(f"   A3: m all of whose primes are at least squared: {pw}; of these not bounded: {len(pn)} {pn[:6]}; bounded m with a prime that divides them once: {bnp} (the least is {least_bnp})")
        print("   by family: " + "; ".join(f"m with {k} exactly: {fm[k][1]} of {fm[k][0]} bounded = {fm[k][1] / fm[k][0]:.4f}" for k in sorted(fm)))
    L = math.log(math.log(10 ** 7) / math.log(10 ** 6))
    for name, key, l, e in (('F1', 121, 11, 2), ('F2', 169, 13, 2), ('F3', 81, 3, 4), ('F4', 125, 5, 3), ('seen before sealing', 9, 3, 2), ('seen before sealing', 25, 5, 2), ('seen before sealing', 27, 3, 3), ('seen before sealing', 49, 7, 2)):
        a6, a7 = stat[10 ** 6][6][key], stat[10 ** 7][6][key]; s6, s7 = a6[1] / a6[0], a7[1] / a7[0]
        # the sampling error of each share, as for a count of bounded members among the family's members, carried to the slope
        err = math.sqrt((1 - s6) / a6[1] + (1 - s7) / a7[1]) / L
        print(f"{name}: m with {key} exactly: bounded share {s6:.4f} of {a6[0]} up to 10^6, {s7:.4f} of {a7[0]} up to 10^7; slope {math.log(s7 / s6) / L:+.3f} (sampling error about {err:.3f}); predicted {-l ** (3 - e) / (l * l - 1):+.3f}")
    slope = math.log(R[10 ** 7] / R[10 ** 6]) / math.log(math.log(10 ** 7) / math.log(10 ** 6))
    print(f"A1: {R[10 ** 7]:.4f}   A2: {stat[10 ** 7][2] / stat[10 ** 7][0]:.4f}   A4: slope between the last two decades {slope:.3f}")

    # for the write-up: the least counter-examples, worked
    def cycle(m):
        xs = []; x = 1
        while True:
            xs.append(x); x = x * 2 % m
            if x == 1: return xs
    for m in (45, 63):
        xs = cycle(m); s = abs(sum(complex(math.cos(2 * math.pi * x / m), math.sin(2 * math.pi * x / m)) for x in xs))
        print(f"m = {m}: the round is {xs} ({len(xs)} steps) and sums to {s:.2e}")
    xs = cycle(45); K = [1, 16, 31]
    cosets = sorted({tuple(sorted(x * k % 45 for k in K)) for x in xs})
    print(f"   45: the round is the union of the sets x * (1, 16, 31): {cosets}; each is three headings a third of a turn apart")
    m = 1093 ** 3; x = 1; t = 0j; n = 0
    while True:
        t += complex(math.cos(2 * math.pi * x / m), math.sin(2 * math.pi * x / m)); n += 1; x = x * 2 % m
        if x == 1: break
    print(f"m = 1093^3: the round of {n} steps sums to {abs(t):.2e}")

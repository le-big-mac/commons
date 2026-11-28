"""Independent recomputation for the reading of the two paragraphs "Added on 28 November".
Pure Python, exact integers.  A signed marking balances at d (d | n) when the cyclotomic polynomial Phi_d divides
sum(+-X^hour); tested by the remainder of X^h modulo Phi_d (integer long division by a monic polynomial).
Every signing is tried (the first sign fixed to +: turning all signs over changes no balance)."""
import sys, itertools
from fractions import Fraction


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def polydivmod(a, b):
    """a, b lists of ints, lowest degree first; b monic.  Returns (q, r)."""
    a = a[:]
    q = [0] * max(1, len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        q[i] = c
        if c:
            for j, bj in enumerate(b):
                a[i + j] -= c * bj
    r = a[:len(b) - 1]
    return q, r


_cyc = {}


def cyclotomic(n):
    if n in _cyc:
        return _cyc[n]
    p = [-1] + [0] * (n - 1) + [1]  # X^n - 1
    for d in divisors(n):
        if d < n:
            p, r = polydivmod(p, cyclotomic(d))
            assert not any(r)
    _cyc[n] = p
    return p


def reductions(n):
    """for each d | n: list over hours h of the remainder of X^h mod Phi_d (tuple of ints)."""
    out = {}
    for d in divisors(n):
        phi = cyclotomic(d)
        k = len(phi) - 1
        vecs = []
        for h in range(n):
            a = [0] * (h % d) + [1]
            if len(a) <= k:
                r = a + [0] * (k - len(a))
            else:
                _, r = polydivmod(a, phi)
            vecs.append(tuple(r))
        out[d] = vecs
    return out


def counts(n, marks, red=None, mod3=False):
    """returns (number of signings with first sign +, number bad among them, dict d -> number bad at d).
    mod3=True: 'fails the severe test at d' = remainder has every coefficient divisible by 3."""
    red = red or reductions(n)
    m = len(marks)
    total = 2 ** (m - 1)
    bad = 0
    per = {d: 0 for d in red}
    for s in range(total):
        signs = [1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)]
        isbad = False
        for d, vecs in red.items():
            k = len(vecs[0])
            acc = [0] * k
            for e, h in zip(signs, marks):
                v = vecs[h % n]
                for i in range(k):
                    acc[i] += e * v[i]
            z = all(x % 3 == 0 for x in acc) if mod3 else not any(acc)
            if z:
                per[d] += 1
                isbad = True
        if isbad:
            bad += 1
    return total, bad, per


def good_share(n, marks, red=None):
    t, b, _ = counts(n, marks, red)
    return Fraction(t - b, t)


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'examples':
        ex = [(12, [0, 1, 2], '1/2'), (2, [0, 0, 0, 1], '1/4'), (30, [0, 1, 2, 3, 9], '1/2'),
              (6, [0, 0, 1, 2, 2, 4], '5/16'), (210, [0, 3, 9, 12, 32, 141, 202], '9/16'),
              (6, [0, 0, 0, 0, 1, 2, 2, 4], '25/64')]
        for n, marks, want in ex:
            t, b, per = counts(n, marks)
            g = Fraction(t - b, t)
            print(f"clock {n:4d}  marks {marks}  signings {2*t}  good {2*(t-b)}  share {g}  page says {want}  "
                  f"{'SAME' if g == Fraction(want) else 'DIFFERENT'}  bad at: " +
                  ", ".join(f"{d}:{2*c}" for d, c in per.items() if c), flush=True)
            # the wound-back marking on the odd part
            odd = n
            while odd % 2 == 0:
                odd //= 2
            t2, b2, per2 = counts(odd, [h % odd for h in marks])
            print(f"      wound back onto {odd}: bad share {Fraction(b2, t2)}; 1 - 2*bad = {1 - 2*Fraction(b2, t2)}", flush=True)
    elif what == 'exhaust':
        # least share of good signings over every multiset of m marks containing 0, on each clock given
        m = int(sys.argv[2])
        for n in map(int, sys.argv[3:]):
            red = reductions(n)
            best = None; ex = None; cnt = 0
            bestset = None; exset = None
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                marks = [0] + list(rest)
                g = good_share(n, marks, red); cnt += 1
                if best is None or g < best:
                    best = g; ex = marks
                if len(set(marks)) == m and (bestset is None or g < bestset):
                    bestset = g; exset = marks
            print(f"m = {m}  clock {n:3d}  markings {cnt:8d}  least share {best} at {ex};  with all hours different: {bestset} at {exset}", flush=True)
    elif what == 'severe':
        # share of signings that fail the severe test at some divisor
        n = int(sys.argv[2]); marks = [int(x) for x in sys.argv[3:]]
        t, b, per = counts(n, marks, mod3=True)
        print(f"clock {n}  marks {marks}  fail the severe test somewhere: {Fraction(b, t)} ({2*b} of {2*t}); at: " +
              ", ".join(f"{d}:{2*c}" for d, c in per.items() if c))
        t, b, per = counts(n, marks)
        print(f"      balance somewhere (plain): {Fraction(b, t)}")
    elif what == 'severe-lifts':
        # all lifts of a marking on clock n0 to clock n0*k: least share passing the severe test everywhere, and least good share
        n0 = int(sys.argv[2]); k = int(sys.argv[3]); base = [int(x) for x in sys.argv[4:]]
        n = n0 * k; red = reductions(n)
        m = len(base); least = None; leastg = None
        for lift in itertools.product(range(k), repeat=m - 1):
            marks = [base[0]] + [b + n0 * t for b, t in zip(base[1:], lift)]
            t, b, _ = counts(n, marks, red, mod3=True)
            s = Fraction(t - b, t)
            if least is None or s < least[0]:
                least = (s, marks)
            g = good_share(n, marks, red)
            if leastg is None or g < leastg[0]:
                leastg = (g, marks)
        print(f"clock {n}: lifts of {base} from clock {n0}: least share passing the severe test at every divisor {least[0]} at {least[1]}; least good share {leastg[0]} at {leastg[1]}")

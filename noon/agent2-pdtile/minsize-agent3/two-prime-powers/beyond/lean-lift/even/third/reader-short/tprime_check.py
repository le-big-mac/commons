#!/usr/bin/env python3
"""A reader's test of Theorem T' (and T) of theorem-twice.md, written from the statement in its section 1.

A valued family: elements y = 0..m-1, position pos[y] in Z_(2^k), value val[y] in V = Z/N (N = 0: V = Z).
Everything is computed from the definitions, by all 2^m signings, in exact integers:
  class at depth d   : the elements whose position lies in one residue class modulo 2^d (nonempty ones only)
  halves of a class c at depth j-1 : its elements in each of the two residue classes modulo 2^j inside it
  c balanced at level j : sigma(h) = sigma(h')
  level 0 bad : sigma(B) = 0 ;  level j bad : every class at depth j-1 is balanced at level j
  F_d : every class at depth d has sigma = 0
Checked for every family:
  (E)  #(level j bad) = #F_(j-1)                       for 1 <= j <= k
  (Q)  #(some level bad) <= 2 #(level 0 bad) - #F_k
  (1)  F_d subset of F_(d-1)                           as sets
  (2)  eps bad at level j  iff  tau_j(eps) in F_(j-1)  for every eps
  (3)  F_j subset of (level j bad) and (level 0 bad)   as sets
  (0)  F_0 = (level 0 bad)                             as sets
  (R)  if V has no element of order 2: F_d = (levels 0..d all bad), as sets
  (T)  if moreover no value is 0: #(some level bad) <= 2 #(level 0 bad)
Deliberately false variants, which must fail somewhere (counted, not asserted):
  (X1) #(some level bad) <= 2 #(level 0 bad) - 2 #F_k
  (X2) with "some class" for "every class" in the definition of a bad level:  (E) and (Q)
  (X3) #(level j bad) = #F_j
  (X4) #(some level bad) <= (3/2) #(level 0 bad)
  (X5) (R) asserted also when V has an element of order 2

usage:  tprime_check.py exh <k> <N> <bound on the work>         exhaustive: all multisets of (position, value)
        tprime_check.py rand <seed> <number>                    random and structured families
        tprime_check.py self                                    the literal routine against hand-worked cases
"""
import sys
import itertools
import random
from math import comb


def analyse(pos, val, k, N):
    """Returns (badmask, Fmask, somemask): lists of integers used as sets of signings.

    Signing number e (0 <= e < 2^m): element y has sign -1 iff bit y of e is set.
    badmask[j] has bit e set iff level j is bad for signing e (0 <= j <= k);
    Fmask[d] has bit e set iff every class at depth d has sigma = 0;
    somemask[j] (j >= 1): bit e set iff SOME class at depth j-1 is balanced (false variant X2).
    """
    m = len(pos)
    elems = list(range(m))

    def red(s):
        return s % N if N else s

    # the classes at depth d, as lists of elements, nonempty only
    classes = []
    for d in range(k + 1):
        byres = {}
        for y in elems:
            byres.setdefault(pos[y] % (1 << d), []).append(y)
        classes.append(byres)
    # the halves of the classes at depth j-1
    halves = [None]
    for j in range(1, k + 1):
        L = []
        for r, c in classes[j - 1].items():
            h1 = [y for y in c if pos[y] % (1 << j) == r]
            h2 = [y for y in c if pos[y] % (1 << j) == r + (1 << (j - 1))]
            assert len(h1) + len(h2) == len(c)
            L.append((h1, h2))
        halves.append(L)

    badmask = [0] * (k + 1)
    Fmask = [0] * (k + 1)
    somemask = [0] * (k + 1)
    for e in range(1 << m):
        sv = [(-val[y] if (e >> y) & 1 else val[y]) for y in elems]   # eps_y * v_y
        bit = 1 << e
        if red(sum(sv)) == 0:
            badmask[0] |= bit
        for j in range(1, k + 1):
            every = True
            some = False
            for h1, h2 in halves[j]:
                s1 = 0
                for y in h1:
                    s1 += sv[y]
                s2 = 0
                for y in h2:
                    s2 += sv[y]
                if red(s1) == red(s2):
                    some = True
                else:
                    every = False
            if every:
                badmask[j] |= bit
            if some:
                somemask[j] |= bit
        for d in range(k + 1):
            ok = True
            for c in classes[d].values():
                s = 0
                for y in c:
                    s += sv[y]
                if red(s) != 0:
                    ok = False
                    break
            if ok:
                Fmask[d] |= bit
    return badmask, Fmask, somemask


def popc(x):
    return bin(x).count("1")


class Tally:
    def __init__(self):
        self.families = 0
        self.fail = {}
        self.first = {}
        self.equal_Q = 0        # families with equality in (Q)
        self.equal_T = 0        # families under T's hypotheses with #some = 2 #level0, #level0 > 0
        self.underT = 0
        self.maxratio = (0, 1)

    def bump(self, name, what):
        self.fail[name] = self.fail.get(name, 0) + 1
        if name not in self.first:
            self.first[name] = what


NAMES_TRUE = ["E", "Q", "1", "2", "3", "0", "R", "T"]
NAMES_FALSE = ["X1", "X2E", "X2Q", "X3", "X4", "X5"]


def check_family(pos, val, k, N, tally):
    m = len(pos)
    badmask, Fmask, somemask = analyse(pos, val, k, N)
    tally.families += 1
    desc = "k=%d N=%d pos=%s val=%s" % (k, N, list(pos), list(val))
    nbad = [popc(b) for b in badmask]
    nF = [popc(f) for f in Fmask]
    some_level = 0
    for b in badmask:
        some_level |= b
    Qn = popc(some_level)
    zn = nbad[0]
    # (E)
    for j in range(1, k + 1):
        if nbad[j] != nF[j - 1]:
            tally.bump("E", desc + " j=%d" % j)
    # (Q)
    if not (Qn <= 2 * zn - nF[k]):
        tally.bump("Q", desc)
    if Qn == 2 * zn - nF[k]:
        tally.equal_Q += 1
    # (1)
    for d in range(1, k + 1):
        if Fmask[d] & ~Fmask[d - 1]:
            tally.bump("1", desc + " d=%d" % d)
    # (2): tau_j negates the sign of every element whose position has remainder >= 2^(j-1) modulo 2^j
    for j in range(1, k + 1):
        flip = 0
        for y in range(m):
            if pos[y] % (1 << j) >= (1 << (j - 1)):
                flip |= 1 << y
        for e in range(1 << m):
            if ((badmask[j] >> e) & 1) != ((Fmask[j - 1] >> (e ^ flip)) & 1):
                tally.bump("2", desc + " j=%d e=%d" % (j, e))
                break
    # (3)
    for j in range(1, k + 1):
        if Fmask[j] & ~(badmask[j] & badmask[0]):
            tally.bump("3", desc + " j=%d" % j)
    # (0)
    if Fmask[0] != badmask[0]:
        tally.bump("0", desc)
    # (R) and (X5)
    no2 = (N == 0) or (N % 2 == 1)
    allbad = (1 << (1 << m)) - 1
    for d in range(k + 1):
        allbad &= badmask[d]
        if Fmask[d] != allbad:
            tally.bump("R" if no2 else "X5", desc + " d=%d" % d)
    # (T)
    if no2 and all(red_nonzero(v, N) for v in val):
        tally.underT += 1
        if not (Qn <= 2 * zn):
            tally.bump("T", desc)
        if zn > 0:
            if Qn == 2 * zn:
                tally.equal_T += 1
            a, b = tally.maxratio
            if Qn * b > a * zn:
                tally.maxratio = (Qn, zn)
    # false variants
    if not (Qn <= 2 * zn - 2 * nF[k]):
        tally.bump("X1", desc)
    some_any = badmask[0]
    for j in range(1, k + 1):
        some_any |= somemask[j]
        if popc(somemask[j]) != nF[j - 1]:
            tally.bump("X2E", desc + " j=%d" % j)
    if not (popc(some_any) <= 2 * zn - nF[k]):
        tally.bump("X2Q", desc)
    for j in range(1, k + 1):
        if nbad[j] != nF[j]:
            tally.bump("X3", desc + " j=%d" % j)
    if not (2 * Qn <= 3 * zn):
        tally.bump("X4", desc)


def red_nonzero(v, N):
    return (v % N if N else v) != 0


def report(tally, head):
    print(head)
    print("  families: %d   (under the hypotheses of Theorem T: %d)" % (tally.families, tally.underT))
    for name in NAMES_TRUE:
        print("  true statement (%s): failures %d%s" % (
            name, tally.fail.get(name, 0),
            ("   FIRST: " + tally.first[name]) if name in tally.first else ""))
    for name in NAMES_FALSE:
        print("  false variant (%s): failures %d%s" % (
            name, tally.fail.get(name, 0),
            ("   first: " + tally.first[name]) if name in tally.first else ""))
    print("  equality in Q <= 2z - P(F_k): %d families" % tally.equal_Q)
    a, b = tally.maxratio
    print("  under T's hypotheses with z > 0: largest Q/z = %d/%d; Q = 2z in %d families" % (a, b, tally.equal_T))
    ok = all(tally.fail.get(nm, 0) == 0 for nm in NAMES_TRUE)
    print("  RESULT: %s" % ("no true statement failed" if ok else "A TRUE STATEMENT FAILED"))
    sys.stdout.flush()


def run_exh(k, N, cap):
    values = list(range(N)) if N else [-2, -1, 0, 1, 2]
    types = [(u, v) for u in range(1 << k) for v in values]
    T = len(types)
    tally = Tally()
    sizes = []
    units = 0
    for m in range(0, 12):
        cnt = comb(T + m - 1, m)
        units += cnt * (1 << m) * max(m, 1) * (k + 1)      # a measure of the work; cap bounds it
        if m > 0 and units > cap:
            break
        sizes.append((m, cnt))
        for fam in itertools.combinations_with_replacement(types, m):
            check_family([t[0] for t in fam], [t[1] for t in fam], k, N, tally)
    report(tally, "EXHAUSTIVE positions Z_%d, values %s (0 allowed), every multiset of (position, value) of sizes %s"
           % (1 << k, ("Z/%d" % N) if N else "{-2..2} in Z", ", ".join("%d (%d)" % s for s in sizes)))


def run_rand(seed, number):
    rng = random.Random(seed)
    tally = Tally()
    for _ in range(number):
        k = rng.choice([1, 2, 3, 4])
        N = rng.choice([2, 3, 4, 6, 0])
        m = rng.randint(1, 10)
        mode = rng.randint(0, 4)
        npos = 1 << k
        if mode == 0:                       # anything
            P = list(range(npos))
        elif mode == 1:                     # few positions, so that several elements share one
            P = rng.sample(range(npos), rng.randint(1, min(3, npos)))
        elif mode == 2:                     # positions in pairs that part at the last level
            base = rng.sample(range(npos // 2), rng.randint(1, min(3, npos // 2)))
            P = base + [b + npos // 2 for b in base]
        elif mode == 3:                     # positions in one class modulo 2^(k-1) or 2
            step = rng.choice([1 << j for j in range(k + 1)])
            off = rng.randrange(npos)
            P = sorted(set((off + step * t) % npos for t in range(npos)))
        else:
            P = rng.sample(range(npos), rng.randint(1, npos))
        pos = [rng.choice(P) for _ in range(m)]
        vmode = rng.randint(0, 3)
        if N:
            allv = list(range(N))
        else:
            allv = list(range(-4, 5))
        if vmode == 0:                      # any value, 0 allowed
            val = [rng.choice(allv) for _ in range(m)]
        elif vmode == 1:                    # one value up to sign
            v = rng.choice(allv)
            val = [rng.choice([v, -v]) for _ in range(m)]
        elif vmode == 2:                    # nonzero values only
            nz = [v for v in allv if red_nonzero(v, N)]
            val = [rng.choice(nz) for _ in range(m)]
        else:                               # two values up to sign, and some zeros
            v, w = rng.choice(allv), rng.choice(allv)
            val = [rng.choice([v, -v, w, -w, 0]) for _ in range(m)]
        check_family(pos, val, k, N, tally)
    report(tally, "RANDOM seed %d: positions on Z_2, Z_4, Z_8, Z_16; values in Z/2, Z/3, Z/4, Z/6, Z (-4..4); "
                  "1 to 10 elements; five position modes, four value modes" % seed)


def run_self():
    """The literal routine on cases worked by hand."""
    # two elements, positions 0 and 2 on Z_4 (they part at level 2), values 1, 1 in Z:
    # signs equal: sigma = +-2, level 0 not bad; level 1: class B, halves {both}, {} : 2 != 0 not bad;
    #              level 2: class {0,2}: halves {0}, {2}: equal sums: bad.
    # signs opposite: level 0 bad; level 1: halves B (sum 0) and {}: bad; level 2: 1 != -1: not bad.
    bad, F, some = analyse([0, 2], [1, 1], 2, 0)
    # signing numbers: e=0 (+,+), e=1 (-,+), e=2 (+,-), e=3 (-,-)
    assert bad[0] == 0b0110 and bad[1] == 0b0110 and bad[2] == 0b1001, (bad,)
    assert F[0] == 0b0110 and F[1] == 0b0110 and F[2] == 0, (F,)
    # the empty family: every event certain
    bad, F, some = analyse([], [], 3, 3)
    assert bad == [1, 1, 1, 1] and F == [1, 1, 1, 1]
    # one element, value 1 in Z/3, position 5 on Z_8: nothing is ever bad
    bad, F, some = analyse([5], [1], 3, 3)
    assert bad == [0, 0, 0, 0] and F == [0, 0, 0, 0]
    # one element of value 0: everything bad
    bad, F, some = analyse([5], [0], 3, 3)
    assert bad == [3, 3, 3, 3] and F == [3, 3, 3, 3]
    # V = Z/2, one element of value 1 at position 1 on Z_2: sigma(B) = 1: level 0 not bad;
    # level 1: halves {} and {y}: 0 != 1: not bad.  Two such elements at positions 0, 1: sigma = 0 always:
    # level 0 bad always; level 1: 1 = 1: bad always; F_1: classes {y0}, {y1} have sigma 1: never.
    bad, F, some = analyse([0, 1], [1, 1], 1, 2)
    assert bad == [15, 15] and F == [15, 0]
    # {0,0,0,1} on Z_2 with values 1 in Z/3 (Corollary 1 for m = 4): z = p_4 = 3/8
    bad, F, some = analyse([0, 0, 0, 1], [1, 1, 1, 1], 1, 3)
    assert popc(bad[0]) == 6
    print("self-test of the literal routine: passed")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "self":
        run_self()
    elif mode == "exh":
        run_self()
        run_exh(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif mode == "rand":
        run_self()
        run_rand(int(sys.argv[2]), int(sys.argv[3]))

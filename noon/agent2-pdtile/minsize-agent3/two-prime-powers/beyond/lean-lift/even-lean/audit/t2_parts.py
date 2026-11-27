"""Parts M, S0', S1', S2' (both forms), E1 (both halves), L of the even skeleton, by all signings, exact arithmetic.

"3-bad at D" (3 not dividing D): the remainder of the signed mask modulo Phi_D has all coefficients divisible by 3
(ecore.bad3; equal to the definition as Lean has it by t0_selftest.py and by the Lean lemma bad3_iff_dvd_ZMod3).
Class sums at a root of unity of order d: elements of Z[x]/(Phi_d, 3) (ecore.class_sums3).

usage: t2_parts.py slices SEED [SCALE]    M, S0', S1', S2' on random and structured families
       t2_parts.py ladder SEED [SCALE]    L
       t2_parts.py ladder2 SEED [SCALE]   L with small exponents and K far beyond them
       t2_parts.py e1              E1
       t2_parts.py three           what the statements would say for p = 3
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random
import time
from math import gcd
import numpy as np
from ecore import *


def families(p, i, d, count, mmax):
    """families of exponents for the level i of p and a cofactor d: random, structured, not reduced"""
    N = p ** i * d
    L = p ** (i - 1) if i >= 1 else 1
    out = []
    for t in range(count):
        m = random.randint(0, mmax)
        kind = t % 6
        if kind == 0:
            e = [random.randrange(0, N) for _ in range(m)]
        elif kind == 1:
            e = [random.randrange(0, 3 * N) for _ in range(m)]
        elif kind == 2:
            # full groups of p: c + t L (t < p), each lifted by a multiple of p^i, and a few extras
            e = []
            while len(e) + p <= max(m, p) and len(e) < mmax - p + 1:
                c = random.randrange(0, L)
                shift = random.randrange(0, d) * p ** i if random.random() < 0.6 else 0
                e += [(c + t2 * L + shift + random.choice([0, 0, p ** i * random.randrange(0, d)])) % (2 * N)
                      for t2 in range(p)]
                if random.random() < 0.5:
                    break
            e += [random.randrange(0, N) for _ in range(max(0, min(m, mmax) - len(e)))]
            e = e[:mmax] if len(e) > mmax else e
        elif kind == 3:
            # all exponents in one class modulo d; few classes modulo p^i
            r = random.randrange(0, d)
            cl = [random.randrange(0, p ** i) for _ in range(random.randint(1, 3))]
            e = []
            for _ in range(m):
                c = random.choice(cl)
                # x = c mod p^i, x = r mod d
                x = next(x for x in range(N) if x % (p ** i) == c and x % d == r)
                e.append(x + random.choice([0, 0, N]))
        elif kind == 4:
            base = [random.randrange(0, N) for _ in range(random.randint(1, 3))]
            e = [random.choice(base) for _ in range(m)]
        else:
            # full set of residues modulo p, same residue modulo d, then repeated or perturbed
            r = random.randrange(0, N)
            e = [(r + t2 * (N // p)) % N for t2 in range(p)][:mmax]
            e += [random.choice(e) if random.random() < 0.7 else random.randrange(0, N)
                  for _ in range(max(0, m - len(e)))] if e else []
        out.append(e)
    return out


def run_slices(seed):
    random.seed(seed)
    t0 = time.time()
    # ---- S0', S1', S2' ----
    configs = []
    for p, imax in [(2, 4), (5, 3), (7, 3), (11, 2), (13, 1)]:
        for i in range(1, imax + 1):
            for d in [1, 2, 4, 5, 7, 8, 10, 11, 14, 20, 22, 35, 55, 70]:
                if d % p == 0 or p ** i * d > 1400:
                    continue
                if (p >= 7 and i == 3 and d > 2) or (p == 5 and i == 3 and d > 8):
                    continue
                configs.append((p, i, d))
    st = dict(inst=0, with_bad=0, bad_signings=0, s0_viol=0, s0_groups=0, conv_viol=0, s1_inst=0, s1_with_bad=0,
              s1_viol=0, s2a_viol=0, s2a_eq=0, s2a_eq_Jpos=0, s2b_inst=0, s2b_viol=0, s2b_eq=0, s2b_with_bad=0,
              multi=0, multi_bad=0, two=0, two_bad=0)
    by_p = {}
    by_i = {}
    first = {}
    for (p, i, d) in configs:
        N = p ** i * d
        L = p ** (i - 1)
        mmax = 9 if N <= 400 else 8
        cnt = (40 if N > 400 else 70) * SCALE
        for e in families(p, i, d, cnt, mmax):
            m = len(e)
            B = bad3(e, N)
            nb = int(B.sum())
            st['inst'] += 1
            key = p
            by_p.setdefault(key, [0, 0])
            by_p[key][0] += 1
            by_i.setdefault((p, i), [0, 0])
            by_i[(p, i)][0] += 1
            if len(factor(d)) >= 1:
                st['multi'] += 1
            if len(factor(d)) >= 2:
                st['two'] += 1
                if nb:
                    st['two_bad'] += 1
            if nb:
                st['with_bad'] += 1
                st['bad_signings'] += nb
                by_p[key][1] += 1
                by_i[(p, i)][1] += 1
                if len(factor(d)) >= 1:
                    st['multi_bad'] += 1
            # S0': class sums of the p classes of every group are equal, for every 3-bad signing
            CS = class_sums3(e, d, p ** i)                      # (2^m, p^i, phi(d))
            G = CS.reshape(1 << m, p, L, -1)                    # class r + t L is [t, r]
            flat = ~np.any(G != G[:, :1, :, :], axis=(1, 2, 3))  # every group flat
            st['s0_groups'] += nb * L
            v = int(np.sum(B & ~flat))
            if v:
                st['s0_viol'] += v
                first.setdefault('s0', (p, i, d, e))
            cv = int(np.sum(flat & ~B))
            if cv:
                st['conv_viol'] += cv
                first.setdefault('conv', (p, i, d, e))
            # S1'
            lv = live(e, p, i)
            if not lv:
                st['s1_inst'] += 1
                if nb:
                    st['s1_with_bad'] += 1
                B1 = bad3(e, p ** (i - 1) * d)
                v = int(np.sum(B & ~B1))
                if v:
                    st['s1_viol'] += v
                    first.setdefault('s1', (p, i, d, e))
            # S2' with the largest pivot set
            J = max_pivot_formula(e, p, i)
            if nb * 2 ** J > 2 ** m:
                st['s2a_viol'] += 1
                first.setdefault('s2a', (p, i, d, e))
            if nb * 2 ** J == 2 ** m:
                st['s2a_eq'] += 1
                if J > 0:
                    st['s2a_eq_Jpos'] += 1
            # S2' with the rank
            if lv:
                rk = rank(e, p, i)
                st['s2b_inst'] += 1
                if nb:
                    st['s2b_with_bad'] += 1
                if nb * 2 ** ((p - 1) * rk) > 2 ** m:
                    st['s2b_viol'] += 1
                    first.setdefault('s2b', (p, i, d, e))
                if nb * 2 ** ((p - 1) * rk) == 2 ** m:
                    st['s2b_eq'] += 1
        if time.time() - t0 > 170:
            print("  (slices stopped by the clock at config", (p, i, d), ")")
            break
    print(f"S0'/S1'/S2' seed {seed}: configs (p, i, d) {len(configs)}; instances (family, p, i, d) {st['inst']}, "
          f"with a 3-bad signing {st['with_bad']}, 3-bad signings {st['bad_signings']}, with d > 1 {st['multi']} "
          f"({st['multi_bad']} with a 3-bad signing), with d of two primes {st['two']} ({st['two_bad']} with a "
          f"3-bad signing)")
    print(f"  S0': (3-bad signing, group) pairs checked {st['s0_groups']}, violations {st['s0_viol']}; converse "
          f"(flat on every group but not 3-bad; not a statement) {st['conv_viol']}")
    print(f"  S1': instances with the level not live {st['s1_inst']} ({st['s1_with_bad']} with a 3-bad signing), "
          f"violations {st['s1_viol']}")
    print(f"  S2' pivot (largest pivot set): violations {st['s2a_viol']}, equality {st['s2a_eq']} "
          f"({st['s2a_eq_Jpos']} with a nonempty pivot set)")
    print(f"  S2' rank: live instances {st['s2b_inst']} ({st['s2b_with_bad']} with a 3-bad signing), violations "
          f"{st['s2b_viol']}, equality {st['s2b_eq']}")
    print("  by prime (instances, with a 3-bad signing):", {k: tuple(v) for k, v in sorted(by_p.items())})
    print("  by (prime, level):", {k: tuple(v) for k, v in sorted(by_i.items())})
    if first:
        print("  FIRST VIOLATIONS:", first)
    # ---- M ----
    stM = dict(inst=0, with_bad=0, bad_signings=0, viol=0)
    byi = {}
    firstM = None
    for i3 in range(0, 4):
        for d0 in [1, 2, 4, 5, 7, 8, 10, 14, 16, 20, 25, 35]:
            D = 3 ** i3 * d0
            if D > 900:
                continue
            fams = families(3, max(i3, 1), d0, 60 * SCALE, 9)
            if i3 >= 1:
                # unions of full cosets of the subgroup of order 3 and of order 3 d1: these have signings bad at D
                for _ in range(20):
                    x = random.randrange(0, D)
                    e = [(x + t * (D // 3)) % D for t in range(3)]
                    if random.random() < 0.6:
                        y = random.randrange(0, D)
                        e += [(y + t * (D // 3)) % D for t in range(3)]
                    if random.random() < 0.4:
                        e += [random.choice(e)]
                    fams.append(e[:9])
            for e in fams:
                Bz = bad(e, D)
                B3 = bad3(e, d0)
                stM['inst'] += 1
                byi.setdefault(i3, [0, 0, 0])
                byi[i3][0] += 1
                nb = int(Bz.sum())
                if nb:
                    stM['with_bad'] += 1
                    stM['bad_signings'] += nb
                    byi[i3][1] += 1
                    byi[i3][2] += nb
                v = int(np.sum(Bz & ~B3))
                if v:
                    stM['viol'] += v
                    firstM = firstM or (i3, d0, e)
    print(f"M seed {seed}: instances (family, i, d) {stM['inst']}, with a signing bad at 3^i d {stM['with_bad']}, "
          f"bad signings {stM['bad_signings']}, violations {stM['viol']}; by i (instances, with a bad signing, bad "
          f"signings): {{{', '.join(f'{k}: {tuple(v)}' for k, v in sorted(byi.items()))}}}")
    if firstM:
        print("  FIRST VIOLATION of M:", firstM)
    print(f"  ({time.time() - t0:.0f} s)")


def run_ladder(seed):
    random.seed(seed)
    t0 = time.time()
    st = dict(inst=0, checks=0, viol=0, eq=0, zpos=0, beyond=0)
    maxratio = (0, 1, None)
    first = None
    per_d = {}
    for d, kmax in [(1, 6), (5, 4), (7, 4), (11, 3), (13, 3), (25, 3), (35, 3), (49, 2), (55, 2), (65, 2), (77, 2)]:
        for k in range(0, kmax + 1):
            K = k + 2
            N = 2 ** k * d
            if 2 ** K * d > 1300:
                K = max(k for k in range(0, 12) if 2 ** k * d <= 1300)
            cnt = (60 if d < 25 else 30) * SCALE
            mmax = 10 if 2 ** K * d <= 320 else 8
            fams = families(2, max(k, 1), d, cnt, mmax)
            # families that make level 0 bad for many signings: all exponents congruent modulo d, or equal
            for _ in range(cnt // 3):
                m = random.randint(1, mmax)
                r = random.randrange(0, d)
                e = [(r + d * random.randrange(0, 2 ** k)) for _ in range(m)]
                fams.append(e)
            for e in fams:
                e = [x % (2 * N) if random.random() < 0.9 else x for x in e]
                m = len(e)
                z = int(bad3(e, d).sum())
                acc = np.zeros(1 << m, dtype=bool)
                st['inst'] += 1
                per_d.setdefault(d, [0, 0])
                per_d[d][0] += 1
                if z:
                    st['zpos'] += 1
                    per_d[d][1] += 1
                hit = False
                for j in range(K + 1):
                    Bj = bad3(e, 2 ** j * d)
                    acc |= Bj
                    q = int(acc.sum())
                    st['checks'] += 1
                    if q > 2 * z:
                        st['viol'] += 1
                        first = first or (d, j, e, q, z)
                    if z and q == 2 * z:
                        hit = True
                    if z and q * maxratio[1] > maxratio[0] * z:
                        maxratio = (q, z, (d, j, e))
                    if j == K and 2 ** K * d > max(e, default=0) and Bj.any():
                        st['beyond'] += 1
                st['eq'] += hit
            if time.time() - t0 > 240:
                print("  (ladder stopped by the clock at", (d, k), ")")
                break
    print(f"L seed {seed}: instances (family, d) {st['inst']}, inequalities (one for each K) {st['checks']}, violations "
          f"{st['viol']}; instances with a signing 3-bad at d {st['zpos']}, with equality for some K {st['eq']}, "
          f"with a signing 3-bad at the top level 2^K d {st['beyond']}; largest ratio {maxratio[0]}/{maxratio[1]} at "
          f"{maxratio[2]}")
    print("  by d (instances, with a signing 3-bad at d):", {k: tuple(v) for k, v in sorted(per_d.items())})
    if first:
        print("  FIRST VIOLATION of L:", first)
    print(f"  ({time.time() - t0:.0f} s)")


def run_ladder_beyond(seed):
    """L with small exponents (below 16, or below 8) and K up to 7, 2^K above every exponent by a factor 8 or more:
    the levels beyond the power of 2 that matters"""
    random.seed(seed)
    t0 = time.time()
    inst = checks = viol = eq = zpos = top = 0
    first = None
    for d in [1, 5, 7, 11, 13]:
        for trial in range(1500 * SCALE):
            m = random.randint(0, 9)
            bound = random.choice([4, 8, 16])
            kind = trial % 3
            if kind == 0:
                e = [random.randrange(0, bound) for _ in range(m)]
            elif kind == 1:
                base = [random.randrange(0, bound) for _ in range(2)]
                e = [random.choice(base) for _ in range(m)]
            else:
                r = random.randrange(0, min(d, bound))
                e = [x for x in (r + d * random.randrange(0, 4) for _ in range(m)) if x < 16]
                m = len(e)
            z = int(bad3(e, d).sum())
            acc = np.zeros(1 << m, dtype=bool)
            inst += 1
            zpos += z > 0
            hit = False
            for j in range(0, 8):
                Bj = bad3(e, 2 ** j * d)
                acc |= Bj
                q = int(acc.sum())
                checks += 1
                if q > 2 * z:
                    viol += 1
                    first = first or (d, j, e, q, z)
                hit |= (z > 0 and q == 2 * z)
                if j == 7 and Bj.any():
                    top += 1
            eq += hit
        if time.time() - t0 > 240:
            print("  (stopped by the clock at d =", d, ")")
            break
    print(f"L beyond, seed {seed}: d in [1, 5, 7, 11, 13], exponents below 16, K = 0..7 (2^7 d up to 1664): instances "
          f"{inst}, inequalities {checks}, violations {viol}; with a signing 3-bad at d {zpos}, with equality for some K "
          f"{eq}, with a signing 3-bad at 2^7 d {top}; first violation {first}  ({time.time() - t0:.0f} s)")


def run_e1():
    random.seed(5)
    rows = []
    for m in range(0, 15):
        e = [random.randrange(0, 50) for _ in range(m)]
        B = bad3(e, 1)
        sg = signs(m)
        s = sg.sum(axis=1) if m else np.zeros(1, dtype=np.int64)
        direct = (s % 3 == 0)
        assert np.array_equal(B, direct), m
        c = int(B.sum())
        lhs = 3 * c + (0 if m % 2 == 0 else 2)
        rhs = 2 ** m + (2 if m % 2 == 0 else 0)
        assert lhs == rhs, m
        # by a literal count as well
        c2 = sum(1 for t in range(1 << m) if sum(1 if (t >> k) & 1 else -1 for k in range(m)) % 3 == 0)
        assert c2 == c
        rows.append((m, c))
    print("E1: for m = 0..14 (one random family each; the count does not depend on the exponents): 3-bad at 1 equals "
          "'3 divides the sum of the signs' for every signing, and 3 * count + (0 if m even else 2) == 2^m + (2 if m "
          "even else 0).  (m, count):", rows)
    # the count for larger m by the recursion on the three residues
    a = [1, 0, 0]
    for m in range(0, 201):
        c = a[0]
        assert 3 * c + (0 if m % 2 == 0 else 2) == 2 ** m + (2 if m % 2 == 0 else 0), m
        a = [a[1] + a[2], a[0] + a[2], a[0] + a[1]]
    print("    and by the recursion on the three residues of the sum, for every m <= 200")


def run_three():
    """What S0', S1', S2' would say for p = 3.  As Lean has Bad3, every signing is 3-bad at 3^i d (i >= 1): F3 has no
    primitive root of that order (Lean: AuditEven.bad3_of_three_dvd).  So for p = 3 the hypotheses hold for every
    signing, and the conclusions are false for most families.  Also shown: with the paper's meaning (remainder
    modulo Phi_{3^i d} divisible by 3) the flatness would fail too."""
    random.seed(6)
    n_s0 = n_s1 = n_s2 = tot = tot1 = 0
    ex = {}
    paper_fail = 0
    paper_tot = 0
    for trial in range(600):
        i = random.choice([1, 2])
        d = random.choice([1, 2, 4, 5])
        m = random.randint(1, 7)
        N = 3 ** i * d
        e = [random.randrange(0, N) for _ in range(m)]
        L = 3 ** (i - 1)
        CS = class_sums3(e, d, 3 ** i)
        G = CS.reshape(1 << m, 3, L, -1)
        flat = ~np.any(G != G[:, :1, :, :], axis=(1, 2, 3))
        tot += 1
        if not flat.all():          # Lean's S0' with p = 3 would claim flat for EVERY signing
            n_s0 += 1
            ex.setdefault('S0', (i, d, e))
        if not live(e, 3, i) and i == 1:
            tot1 += 1
            if not bad3(e, d).all():   # S1' with p = 3, i = 1 would claim every signing 3-bad at d
                n_s1 += 1
                ex.setdefault('S1', (i, d, e))
        J = max_pivot_formula(e, 3, i)
        if J > 0:                    # S2' would claim 2^m * 2^J <= 2^m
            n_s2 += 1
            ex.setdefault('S2', (i, d, e, J))
        # the paper's 3-bad at 3^i d: remainder modulo Phi_N divisible by 3
        Bp = ~np.any(remainders(e, N) % 3 != 0, axis=1)
        paper_tot += int(Bp.sum())
        paper_fail += int(np.sum(Bp & ~flat))
        if np.any(Bp & ~flat):
            ex.setdefault('paper', (i, d, e))
    print(f"p = 3 (excluded by hp3): of {tot} random families, S0' read with p = 3 would be false for {n_s0} "
          f"(some signing has unequal class sums); S1' with p = 3, i = 1 false for {n_s1} of {tot1} families whose "
          f"level 1 is not live; S2' false for {n_s2} (every family with a nonempty pivot set).  Examples: {ex}")
    print(f"   with 'remainder modulo Phi_(3^i d) divisible by 3' as the hypothesis instead: {paper_tot} such signings, "
          f"{paper_fail} of them not flat")


mode = sys.argv[1]
SCALE = int(sys.argv[3]) if len(sys.argv) > 3 else 1
if mode == 'slices':
    run_slices(int(sys.argv[2]))
elif mode == 'ladder':
    run_ladder(int(sys.argv[2]))
elif mode == 'ladder2':
    run_ladder_beyond(int(sys.argv[2]))
elif mode == 'e1':
    run_e1()
else:
    run_three()

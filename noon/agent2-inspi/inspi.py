"""The turtle that turns a little more each step (Abelson and diSessa's INSPI): the sealed sheet's six lines.
usage: python -I inspi.py > inspi.out        (numpy)

INC = 360 p/q degrees in lowest terms; the angles repeat (mod 360) every q steps; T = q ANGLE + 180 p (q - 1)
(mod 360) is the turning in one loop of q steps and B the displacement over it, the step being 1.
Nothing here uses the looping lemma to decide what the turtle does: the turtle is walked, step by step."""
import sys, math
from fractions import Fraction
import numpy as np


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
    """c: whole numbers, c[r] the coefficient of zeta^r, r = 0..M-1.  True exactly when the sum is 0."""
    phi = cyclotomic(M); deg = len(phi) - 1; a = list(c)
    for i in range(len(a) - 1, deg - 1, -1):          # reduce modulo Phi_M, which is monic
        t = a[i]
        if t:
            for k in range(deg + 1): a[i - deg + k] -= t * phi[k]
    return not any(a)


def loop_exponents(p, q, m):
    """the q headings of one loop, as whole multiples of a (2q)-th of a turn, for the m-th ANGLE that makes T = 0:
       ANGLE/360 = (m - p(q-1)/2)/q, heading before step k = k ANGLE + INC k(k-1)/2"""
    return [(k * (2 * m - p * (q - 1)) + p * k * (k - 1)) % (2 * q) for k in range(q)]


def s1(qmax_numeric=150, exact_qs=None):
    worst = 0.0; cases = 0
    for q in range(1, qmax_numeric + 1):
        for p in range(0 if q == 1 else 1, q):
            if math.gcd(p, q) != 1: continue
            k = np.arange(q)
            for m in range(q):
                e = (k * (2 * m - p * (q - 1)) + p * k * (k - 1)) % (2 * q)
                B = np.exp(2j * np.pi * e / (2 * q)).sum()
                worst = max(worst, abs(abs(B) - math.sqrt(q))); cases += 1
    print(f"S1, to nine places: every p/q in lowest terms with q from 1 to {qmax_numeric} and every ANGLE that makes T = 0: {cases} cases; the largest difference between |B| and the square root of q: {worst:.2e}")
    ok = bad = 0
    for q in exact_qs:
        M = 2 * q
        for p in range(0 if q == 1 else 1, q):
            if math.gcd(p, q) != 1: continue
            for m in range(q):
                e = loop_exponents(p, q, m); c = [0] * M
                for a in e:
                    for b in e: c[(a - b) % M] += 1          # B times its conjugate
                c[0] -= q
                if is_zero(c, M): ok += 1
                else: bad += 1
    print(f"S1, exactly, in whole numbers: |B|^2 = q for every INC that is a whole number of degrees (q a divisor of 360) and for every q up to 40: {ok} cases hold, {bad} do not")
    # the control: the same exact test on loops that do NOT have T = 0 (ANGLE a whole multiple of INC, q even): it must be able to say no
    no = tot = 0
    for q in (4, 6, 8, 10, 12):
        M = 2 * q
        for p in range(1, q):
            if math.gcd(p, q) != 1: continue
            e = [(p * k * (k - 1)) % M for k in range(q)]       # ANGLE 0
            c = [0] * M
            for a in e:
                for b in e: c[(a - b) % M] += 1
            c[0] -= q; tot += 1; no += not is_zero(c, M)
    print(f"   control, the exact test where T is not 0 (ANGLE 0, q = 4 to 12 even): |B|^2 differs from q in {no} of {tot}")
    return worst, bad


def walk_all():
    """every whole-degree pair, walked for 720 steps: the first step at which the turtle is back at its start with its first
       heading and its first ANGLE (mod 360); how far from the start it gets; where it is after 720 steps"""
    first = np.zeros((360, 360), int); reach = np.zeros((360, 360)); end = np.zeros((360, 360)); A0 = np.arange(360)
    for inc in range(1, 360):
        ang = A0.copy(); head = np.zeros(360, int); z = np.zeros(360, complex); f = np.zeros(360, int); r = np.zeros(360)
        for n in range(1, 721):
            z += np.exp(-2j * np.pi * head / 360.0); head = (head + ang) % 360; ang = (ang + inc) % 360
            d = np.abs(z); r = np.maximum(r, d)
            home = (f == 0) & (d < 1e-7) & (head == 0) & (ang == A0)
            f[home] = n
        first[inc] = f; reach[inc] = r; end[inc] = np.abs(z)
    return first, reach, end


def predicted(inc, A):
    g = math.gcd(inc, 360); q = 360 // g; p = inc // g
    T = (q * A + 180 * p * (q - 1)) % 360
    if T == 0: return q, 0, None
    v = 360 // math.gcd(T, 360)
    return q, T, q * v


def corners(inc, A, n):
    ang, head, z, out = A, 0, 0j, [0j]
    for _ in range(n):
        z += complex(math.cos(2 * math.pi * head / 360), -math.sin(2 * math.pi * head / 360)); head = (head + ang) % 360; ang = (ang + inc) % 360; out.append(z)
    return np.array(out)

def width(pts):
    return float(np.abs(pts[:, None] - pts[None, :]).max())


if __name__ == '__main__':
    exact_qs = sorted(set([d for d in range(1, 361) if 360 % d == 0] + list(range(1, 41))))
    s1(150, exact_qs)
    first, reach, end = walk_all()
    # S2 and S3
    agree = runaway_pred = runaway_walk = wrong = 0; fold_ok = 0
    for inc in range(1, 360):
        for A in range(360):
            q, T, n = predicted(inc, A)
            if n is None:
                runaway_pred += 1
                if first[inc, A] == 0: agree += 1
                else: wrong += 1
            else:
                if first[inc, A] == n: agree += 1
                else: wrong += 1
            runaway_walk += first[inc, A] == 0
    print(f"S2: of the 129,240 whole-degree pairs walked for 720 steps, the first step at which the turtle is home (place, heading and ANGLE) is the predicted q v, or never where T = 0, in {agree}; otherwise in {wrong}")
    print(f"S3: pairs never home in 720 steps: {runaway_walk}; pairs with T = 0 by the formula: {runaway_pred}")
    far = [(end[inc, A], inc, A) for inc in range(1, 360) for A in range(360) if first[inc, A] == 0]
    q_of = lambda inc: 360 // math.gcd(inc, 360)
    dev = max(abs(e - 720 / q_of(inc) * math.sqrt(q_of(inc))) for e, inc, A in far)
    print(f"   after 720 steps each of those is (720 / q) x sqrt(q) steps from its start, to within {dev:.1e}; the nearest is {min(far)[0]:.3f} steps away (INC {min(far)[1]}, ANGLE {min(far)[2]})")
    # S2, symmetry: the corners of a closed figure are carried into themselves by a turn of T about the figure's centre
    sym = tried = 0
    for inc, A in ((20, 2), (7, 0), (90, 1), (40, 30), (11, 3), (120, 1), (180, 89), (72, 5)):
        q, T, n = predicted(inc, A)
        if n is None: continue
        pts = corners(inc, A, n)[:-1]; c = pts.mean(); rot = (pts - c) * np.exp(-2j * np.pi * T / 360) + c
        tried += 1; sym += bool(np.abs(rot[:, None] - pts[None, :]).min(axis=1).max() < 1e-6)
    print(f"   v-fold symmetry: of {tried} closed figures tried, a turn by T about the centre carries the corners into themselves in {sym}")
    # S4
    for inc, A in ((20, 2), (7, 0), (20, 10)):
        q, T, n = predicted(inc, A)
        if n is None: print(f"S4: ANGLE {A}, INC {inc}: q = {q}, T = 0; walked: never home in 720 steps; after {q} steps it is {abs(corners(inc, A, q)[-1]):.4f} steps from its start, after {2 * q} steps {abs(corners(inc, A, 2 * q)[-1]):.4f}")
        else: print(f"S4: ANGLE {A}, INC {inc}: q = {q}, T = {T}, so home after {n} steps with {360 // math.gcd(T, 360)}-fold symmetry; walked: first home after {first[inc, A]} steps")
    # S5 and S6: the widest and the narrowest closed figures (the greatest distance between two corners)
    closed = [(reach[inc, A], inc, A) for inc in range(1, 360) for A in range(360) if first[inc, A] > 0]
    closed.sort(reverse=True)
    wide = sorted(((width(corners(inc, A, first[inc, A])), inc, A) for r, inc, A in closed[:400]), reverse=True)
    print("S5: the widest closed figures (width, INC, ANGLE, steps to close): " + "; ".join(f"{w:.2f}, {inc}, {A}, {first[inc, A]}" for w, inc, A in wide[:8]))
    print(f"   (the 400 pairs reaching furthest from their start were measured; the 400th reaches {closed[399][0]:.2f} steps, and no figure is wider than twice its reach)")
    small = sorted(closed)[:400]
    narrow = sorted((width(corners(inc, A, first[inc, A])), inc, A) for r, inc, A in small)
    print("S6: the narrowest closed figures (width, INC, ANGLE, steps to close): " + "; ".join(f"{w:.3f}, {inc}, {A}, {first[inc, A]}" for w, inc, A in narrow[:10]))
    one = [(inc, A) for r, inc, A in closed if r <= 1 + 1e-9]
    print(f"   closed figures with every corner within 1 step of the start: {len(one)}; their INCs: {sorted(set(i for i, a in one))[:12]}")

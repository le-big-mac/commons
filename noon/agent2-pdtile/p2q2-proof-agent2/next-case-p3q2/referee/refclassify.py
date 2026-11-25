"""Referee's independent classification of the 2^11 zero patterns of Z_{p^3 q^2}, following the TABLE of the note
(not the code of exact.py), with the referee's own certified exact LP solver (reflp.py), and a pattern-by-pattern
comparison with exact.CAT of the author's exact.py (copied to ./orig).

Differences in method from exact.py (on purpose):
  * character sums are computed by an independent routine and, for small M, checked against brute-force sums of
    roots of unity over the classes;
  * every LP optimum is certified by an exact primal/dual pair;
  * category R is decided by the RESTRICTED programme (classes outside pZ, resp. qZ, deleted): R iff its optimum equals
    the optimum of LP(Z); category T by the programme with the extra equation gamma_P = 1 (resp. gamma_Q = 1);
    both are then cross-checked against the 'optimal face' formulation used by exact.py;
  * category U by maximising gamma_P (gamma_Q) over the optimal face.
Then Lemma M is applied to the H patterns as the NOTE states it (sizes and required zeros).
usage: refclassify.py p q [--nocompare]"""
import sys, os, cmath, math
from fractions import Fraction as Fr
from collections import Counter
from reflp import solve_lp

a, b = 3, 2


def csum(p, n, l, i):
    """sum of a character of order p^l of Z_{p^n} over {u : v_p(u) = i} (i = n: u = 0)."""
    sub = lambda t: (p ** (n - t) if l <= t else 0)          # sum over the subgroup p^t Z, of order p^(n-t)
    return sub(i) - (sub(i + 1) if i < n else 0)


def brute_table(p, q):
    """character sums over classes by brute force (floats, rounded), for checking csum"""
    M = p**a * q**b
    def cl(x):
        u, w = x % p**a, x % q**b
        i = a if u == 0 else next(t for t in range(a) if u % p**(t + 1) != 0)
        j = b if w == 0 else next(t for t in range(b) if w % q**(t + 1) != 0)
        return (i, j)
    classes = {}
    for x in range(M):
        classes.setdefault(cl(x), []).append(x)
    out = {}
    for l in range(a + 1):
        for m in range(b + 1):
            xi = M // (p**l * q**m)                           # a frequency of order p^l q^m
            for c, xs in classes.items():
                s = sum(cmath.exp(2j * cmath.pi * x * xi / M) for x in xs)
                assert abs(s.imag) < 1e-6 and abs(s.real - round(s.real)) < 1e-6
                out[((l, m), c)] = round(s.real)
    return out


def classify(p, q, verbose=False):
    M = p**a * q**b
    cls = [(i, j) for i in range(a + 1) for j in range(b + 1)]
    ords = [o for o in cls if o != (0, 0)]
    C = {(o, c): csum(p, a, o[0], c[0]) * csum(q, b, o[1], c[1]) for o in cls for c in cls}
    if M <= 3000:
        BT = brute_table(p, q)
        assert all(BT[k] == C[k] for k in C), "character table differs from brute force"
    size = [C[((0, 0), c)] for c in cls]
    assert sum(size) == M
    idx = {c: t for t, c in enumerate(cls)}
    top = (a, b); cP = (a - 1, b); cQ = (a, b - 1)
    unit = lambda c0: [1 if c == c0 else 0 for c in cls]
    CAT = {}; SIZE = {}; cnt = Counter(); nlp = 0
    for mask in range(1 << len(ords)):
        Z = frozenset(o for t, o in enumerate(ords) if mask >> t & 1)
        if (1, 0) not in Z and (0, 1) not in Z:
            CAT[Z] = 'L2'; continue
        Ep = [l for l in range(1, a + 1) if (l, 0) in Z]; Eq = [m for m in range(1, b + 1) if (0, m) in Z]
        t2 = all((l, m) in Z for l in Ep for m in Eq)
        orphan = any(l >= 1 and m >= 1 and l not in Ep and m not in Eq for (l, m) in Z)
        if t2 and not orphan:
            CAT[Z] = 'a'; continue
        k = p ** len(Ep) * q ** len(Eq)
        rows = [unit(top)] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]
        rhs = [1] + [0] * (len(rows) - 1)
        st, v, x, y = solve_lp(rows, rhs, size); nlp += 1
        assert st == 'optimal'
        D = Fr(M) / v
        SIZE[Z] = D
        if D < k:
            CAT[Z] = 'b'; continue
        if D % k != 0:
            CAT[Z] = 'N'; continue
        # ---- R: restricted programmes
        def restricted(keepcls):
            cols = [idx[c] for c in cls if keepcls(c)]
            r2 = [[row[t] for t in cols] for row in rows]
            s2 = solve_lp(r2, rhs, [size[t] for t in cols])
            return s2[1] if s2[0] == 'optimal' else None
        vp = restricted(lambda c: c[0] >= 1); vq = restricted(lambda c: c[1] >= 1); nlp += 2
        R = (vp == v) or (vq == v)
        # cross-check with the optimal-face formulation
        face = rows + [size]; frhs = rhs + [v]
        outp = [size[t] if c[0] == 0 else 0 for t, c in enumerate(cls)]; outq = [size[t] if c[1] == 0 else 0 for t, c in enumerate(cls)]
        mp = solve_lp(face, frhs, outp)[1]; mq = solve_lp(face, frhs, outq)[1]; nlp += 2
        assert R == (mp == 0 or mq == 0), ("R formulations disagree", sorted(Z))
        if R:
            CAT[Z] = 'R'; continue
        # ---- T / U
        def with_eq(c0):
            s2 = solve_lp(rows + [unit(c0)], rhs + [1], size)
            return s2[1] if s2[0] == 'optimal' else None
        xmax = -solve_lp(face, frhs, [-t for t in unit(cP)])[1]; ymax = -solve_lp(face, frhs, [-t for t in unit(cQ)])[1]; nlp += 2
        if top not in Z:
            vx = with_eq(cP); vy = with_eq(cQ); nlp += 2
            T = (vx == v) or (vy == v)
            assert T == (xmax == 1 or ymax == 1), ("T formulations disagree", sorted(Z), xmax, ymax)
            assert xmax <= 1 and ymax <= 1, ("x or y exceeds 1 on the optimal face", sorted(Z), xmax, ymax)
            if T:
                CAT[Z] = 'T'; continue
        else:
            if xmax > 0 or ymax > 0:
                CAT[Z] = 'U'; continue
        CAT[Z] = 'H' if top in Z else 'H-topnotzero'
    for Z in CAT: cnt[CAT[Z]] += 1
    return CAT, SIZE, cnt, nlp


def lemmaM(p, q, CAT, SIZE):
    """apply Lemma M as stated in the note to the H patterns; returns Counter and the list of unsettled patterns"""
    why = Counter(); left = []
    for Z, c in CAT.items():
        if c == 'H-topnotzero':
            left.append((sorted(Z), SIZE[Z], 'M not a zero: Lemma M does not apply')); continue
        if c != 'H': continue
        n = SIZE[Z]
        allK = all((3, m) in Z for m in range(b + 1)) and all((l, 2) in Z for l in range(a + 1))
        reasons = []
        if n == p * q: reasons.append('M0')
        if n == p * p * q and (1, 0) in Z and (3, 1) in Z and (2, 2) in Z and not allK: reasons.append('M2')
        if n == p * p * q and p < q and (0, 1) in Z: reasons.append('M3')
        if n == p * p * q and (0, 1) in Z and (1, 2) in Z: reasons.append('M4')
        # M0 in general: a mixed set has i p + j q elements, i, j >= 1
        if not any((n - i * p) % q == 0 and (n - i * p) // q >= 1 for i in range(1, int(n) // p + 1)): reasons.append('M0gen')
        if reasons: why[reasons[0]] += 1
        else: left.append((sorted(Z), n, 'no part of Lemma M applies'))
        why['any:' + '+'.join(reasons)] += 1
    return why, left


if __name__ == '__main__':
    p, q = int(sys.argv[1]), int(sys.argv[2])
    CAT, SIZE, cnt, nlp = classify(p, q)
    names = ('L2', 'a', 'b', 'N', 'R', 'T', 'U', 'H')
    line = f"referee Z_{p**a * q**b} (p = {p}, q = {q}): " + ", ".join(f"{k} {cnt[k]}" for k in names) + f"; H with M not a zero {cnt['H-topnotzero']}; {nlp} certified LPs"
    why, left = lemmaM(p, q, CAT, SIZE)
    line += f";  M0 {why['M0']}, M2 {why['M2']}, M3 {why['M3']}, M4 {why['M4']}, left {len(left)}"
    if '--nocompare' not in sys.argv:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orig'))
        import exact
        cnt2, hard = exact.classify(p, a, q, b)
        diff = [Z for Z in CAT if CAT[Z] != exact.CAT[Z]]
        assert len(exact.CAT) == len(CAT) == 2048
        hs = {Z: s for Z, s in hard}
        sdiff = [Z for Z in hs if SIZE[Z] != hs[Z]]
        line += f";  patterns whose category differs from exact.CAT: {len(diff)}; H sizes differing: {len(sdiff)}"
        for Z in diff[:20]: print("   DIFF", sorted(Z), CAT[Z], exact.CAT[Z])
    print(line, flush=True)
    for l in left: print("   LEFT", l)
    print("   detail of Lemma M parts applicable:", {k: v for k, v in why.items() if k.startswith('any:')}, flush=True)

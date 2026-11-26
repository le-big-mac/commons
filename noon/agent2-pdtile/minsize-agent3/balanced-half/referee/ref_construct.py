"""Referee: the constructions of section 6 of proof-as-sent.md, built from the WORDS of sections 6.1-6.3 (not from
the author's construct_bal.py, which I did not open before writing this), for every pattern (E, F) with 0 in F.

For each pattern: the multiset chosen by "the first of the five cases that applies" (order I, III, IV, V, II; or
Theorem A's Fib(D(E)) when F is everything), and ALSO every other case whose stated condition holds
(the file says (III), (IV), (V) do not need the order).  Checks: weights >= 0; size = q p^e (p^k' + x);
exact pattern = (E, F) by my literal computation from section 1, and (orders up to DIVMAX) by exact polynomial
division with pat.exact_pattern_division; "case (II) is reached iff none of the clauses (1)-(4) holds".

usage: ref_construct.py p q nmax [DIVMAX]
"""
import sys, itertools, time
import numpy as np
from ref_common import rule, literal_patterns, bits_to_set
sys.path.insert(0, "/home/agent3/minsize/prove")
import pat as PAT


def digits(p, n):
    """dig[a][u] = digit of level a of u (a = 1..n): u = sum u_a p^(a-1)"""
    u = np.arange(p ** n)
    return {a: (u // p ** (a - 1)) % p for a in range(1, n + 1)}


def D_set(p, n, dig, T, b=None, c=None):
    """D(T) = {u : u_a = 0 for every a not in T};  D(T; b->c) = {u : u_b = c, u_a = 0 for a not in T u {b}}"""
    m = np.ones(p ** n, dtype=bool)
    for a in range(1, n + 1):
        if b is not None and a == b:
            m &= dig[a] == c
        elif a not in T:
            m &= dig[a] == 0
    return m


def Fib(p, q, n, mask, m=1):
    W = np.zeros((p ** n, q), dtype=np.int64)
    W[mask, :] = m
    return W


def Lam(mode, i, x, p, q):
    s = int(x.sum())
    one = np.ones(q, dtype=np.int64)
    dx = x - np.roll(x, 1)            # (Delta x)(w) = x(w) - x(w-1)
    if mode == "U":
        if i == 0:
            return x.copy()
        if i == 1:
            return s * one - x
        raise ValueError
    if i == 0:
        return s * one + dx
    if i == 1:
        return s * one - dx
    if mode == "Q" and 2 <= i <= p - 1:
        return s * one
    raise ValueError


def shape_part(p, q, n, dig, a0, T1, T2, H, mode):
    assert all(1 <= a <= a0 - 1 for a in T1) and all(a0 + 1 <= a <= n for a in T2) and set(H) <= set(T2)
    free = set(T1) | {a0} | set(T2)
    Dstar = np.ones(p ** n, dtype=bool)
    for a in range(1, n + 1):
        if a not in free:
            Dstar &= dig[a] == 0
    I = range(p) if mode == "Q" else (0, 1)
    W = np.zeros((p ** n, q), dtype=np.int64)
    for u in np.flatnonzero(Dstar):
        i = int(dig[a0][u])
        if i not in I:
            continue
        tau = 1 if (len(H) > 0 and all(dig[a][u] != 0 for a in H)) else 0
        et = np.zeros(q, dtype=np.int64)
        et[tau % q] = 1
        W[u, :] += Lam(mode, i, et, p, q)
    return W


def build(p, q, n, dig, E, F, case):
    """E, F python sets (0 in F).  case in {'A','I','II','III','IV','V'}; returns W or None if the case's stated
    condition does not hold."""
    if all(a in F for a in range(n + 1)):
        return Fib(p, q, n, D_set(p, n, dig, E)) if case == "A" else None
    if case == "A":
        return None
    a0 = min(a for a in range(1, n + 1) if a not in F)
    above = set(range(1, a0))
    below = set(range(a0 + 1, n + 1))
    Gp = sorted((F - E) & below)
    kp = len(Gp)
    g1 = Gp[0] if kp else None
    T20 = (E | F) & below
    H0 = (E - F) & below
    mode0 = "Q" if a0 in E else "U"
    if case == "I":
        if kp != 0:
            return None
        return shape_part(p, q, n, dig, a0, E & above, T20, H0, mode0)
    if kp == 0:
        return None
    if case == "III":
        if not (E & above):
            return None
        b = min(E)
        W = shape_part(p, q, n, dig, a0, (E & above) - {b}, T20, H0, mode0)
        for i in range(1, p):
            W = W + Fib(p, q, n, D_set(p, n, dig, E - {b}, b, i), p ** kp)
        return W
    if case == "IV":
        if not (a0 in E and p >= 3):
            return None
        W = shape_part(p, q, n, dig, a0, E & above, T20, H0, "W")
        for i in range(2, p):
            W = W + Fib(p, q, n, D_set(p, n, dig, E - {a0}, a0, i), p ** kp)
        return W
    if case == "V":
        cand = [b for b in range(a0 + 1, g1) if b in E and b not in F]
        if not (a0 in E and cand):
            return None
        b = min(cand)
        W = shape_part(p, q, n, dig, a0, E & above, T20 - {b}, H0 - {b}, "Q")
        for i in range(1, p):
            W = W + Fib(p, q, n, D_set(p, n, dig, E - {b}, b, i), p ** kp)
        return W
    if case == "II":
        return shape_part(p, q, n, dig, a0, E & above, T20, H0, mode0) + Fib(p, q, n, D_set(p, n, dig, E))
    raise ValueError


def first_case(p, n, E, F):
    if all(a in F for a in range(n + 1)):
        return "A"
    a0 = min(a for a in range(1, n + 1) if a not in F)
    above = set(range(1, a0))
    below = set(range(a0 + 1, n + 1))
    Gp = sorted((F - E) & below)
    if len(Gp) == 0:
        return "I"
    if E & above:
        return "III"
    if a0 in E and p >= 3:
        return "IV"
    if a0 in E and any((b in E and b not in F) for b in range(a0 + 1, Gp[0])):
        return "V"
    return "II"


def my_pattern(p, q, n, W):
    r = literal_patterns(p, q, n, W.reshape(1, p ** n, q))[0]
    E = bits_to_set(r["E"][0, 0])
    F = bits_to_set(r["F"][0, 0])
    if bool(r["bal"][0, 0]):
        F = F | {0}
    return E, F


def to_ZM(p, q, n, W):
    M = p ** n * q
    w = [0] * M
    pn = p ** n
    for x in range(M):
        w[x] = int(W[x % pn, x % q])
    return w


def main():
    p, q, nmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    divmax = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    t0 = time.time()
    for n in range(1, nmax + 1):
        dig = digits(p, n)
        M = p ** n * q
        levels = list(range(1, n + 1))
        stats = {}
        nbad = 0
        ndiv = 0
        nclause_bad = 0
        maxw_over = 0
        npat = 0
        for Et in itertools.chain.from_iterable(itertools.combinations(levels, r) for r in range(n + 1)):
            for Ft in itertools.chain.from_iterable(itertools.combinations(levels, r) for r in range(n + 1)):
                E = set(Et)
                F = set(Ft) | {0}
                npat += 1
                val, x, a0, kp = rule(p, q, n, E, F)
                fc = first_case(p, n, E, F)
                # Theorem C, last sentence: (II) reached iff none of the clauses holds, i.e. iff x = 1
                if x is not None and ((fc == "II") != (x == 1)):
                    nclause_bad += 1
                for case in ("A", "I", "III", "IV", "V", "II"):
                    if case == "II" and fc != "II":
                        continue          # (II) is defined only as "otherwise"
                    W = build(p, q, n, dig, E, F, case)
                    if W is None:
                        assert case != fc, (E, F, case)
                        continue
                    tag = case + ("" if case == fc else "(alt)")
                    st = stats.setdefault(tag, [0, 0, 0])
                    st[0] += 1
                    ok = True
                    if W.min() < 0:
                        ok = False
                    size = int(W.sum())
                    xcase = 1 if case == "II" else 0
                    want = q * p ** len(E) * ((p ** kp + xcase) if case != "A" else 1)
                    if size != want or (case == fc and size != val):
                        ok = False
                    Em, Fm = my_pattern(p, q, n, W)
                    if Em != E or Fm != F:
                        ok = False
                    if M <= divmax:
                        Ed, Fd = PAT.exact_pattern_division(p, q, n, to_ZM(p, q, n, W))
                        ndiv += 1
                        st[2] += 1
                        if set(Ed) != E or set(Fd) != F:
                            ok = False
                        Et2, Ft2 = PAT.tree_pattern(p, q, n, to_ZM(p, q, n, W))
                        if set(Et2) != E or set(Ft2) != F:
                            ok = False
                    if case != "A" and kp is not None:
                        lim = max(p ** kp, 2)
                        if int(W.max()) > lim:
                            maxw_over += 1
                    if not ok:
                        nbad += 1
                        st[1] += 1
                        if nbad <= 5:
                            print(f"   FAIL p={p} q={q} n={n} E={sorted(E)} F={sorted(F)} case {tag}: size {size} want {want}, "
                                  f"pattern found E={sorted(Em)} F={sorted(Fm)}")
        print(f"p={p} q={q} n={n} (order {M}): {npat} patterns; failures {nbad}; 'case II iff x=1' wrong for {nclause_bad}; "
              f"multisets with a weight above max(p^k', 2): {maxw_over}; "
              + "; ".join(f"{k}: {v[0]} built, {v[1]} failed, {v[2]} also by division" for k, v in sorted(stats.items()))
              + f"  [{time.time() - t0:.0f} s]", flush=True)


if __name__ == "__main__":
    main()

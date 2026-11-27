# The three identities (A), (B1), (B2) of lemma-rho.md, the claims on equality, and the referee's criterion
# for equality, on EVERY multiset of 1..M elements on Z_(2^K); rho_2 by brute force over all signings.
# usage: run_ident.py K M
import sys, itertools, time
from fractions import Fraction
from collections import Counter
from ref_lib import p, Fast

K = int(sys.argv[1]); M = int(sys.argv[2])
n = 1 << K
t0 = time.time()
G = {(): 0}          # multiset (sorted tuple) -> number of signings with no bad level
for m in range(1, M + 1):
    f = Fast(m)
    for B in itertools.combinations_with_replacement(range(n), m):
        G[B] = f.count_good(B, K)
print(f"Z_{n}: rho_2 by brute force for {len(G) - 1} multisets of 1..{M} elements  [{time.time() - t0:.0f} s]", flush=True)


def R(B):
    return Fraction(G[B], 1 << len(B))


def minus(B, items):
    L = list(B)
    for x in items:
        L.remove(x)
    return tuple(L)


def criterion(B):
    """Referee's criterion for rho_2(B) = p_(m-1):
    (i) some element has multiplicity 1, and
    (ii) at every level j = 1..K: at most one class at depth j-1 has both halves nonempty,
         or some class at depth j-1 is a single element."""
    if 1 not in Counter(B).values():
        return False
    for j in range(1, K + 1):
        cl = {}
        for b in B:
            cl.setdefault(b % (1 << (j - 1)), []).append(b)
        split = sum(1 for c in cl.values() if len({b % (1 << j) for b in c}) == 2)
        single = any(len(c) == 1 for c in cl.values())
        if split >= 2 and not single:
            return False
    return True


cnt = Counter()
fail = Counter()
for B in G:
    m = len(B)
    if m == 0:
        continue
    rb = R(B)
    eq = (rb == p(m - 1))
    cnt["multisets"] += 1
    if rb < p(m - 1):
        fail["bound"] += 1
    if eq:
        cnt["equal to the bound"] += 1
    if criterion(B) != eq:
        fail["criterion for equality"] += 1
        if fail["criterion for equality"] <= 5:
            print("  criterion mismatch:", B, rb, p(m - 1))
    if m == 1:
        if rb != 1:
            fail["base"] += 1
        continue
    mult = Counter(B)
    if max(mult.values()) >= 2:
        # (A), for every repeated element y and every t = 2..multiplicity(y)
        for y, ty in mult.items():
            for t in range(2, ty + 1):
                BA = minus(B, [y] * t)
                B1 = tuple(sorted(BA + (y,)))
                cnt["(A) checked" if t == ty else "(A) with fewer copies than all, checked"] += 1
                if rb != p(t) * R(BA) + (1 - p(t)) * R(B1):
                    fail["(A)"] += 1
                if m == t:
                    if not (rb == 1 - p(t) and rb > p(t - 1)):
                        fail["(A) m = t"] += 1
                else:
                    both = (R(BA) == p(m - t - 1)) and (R(B1) == p(m - t))
                    cnt["(A) equality passes down, checked"] += 1
                    if both != eq:
                        fail["(A) equality passes down"] += 1
        continue
    # (B): B is a set
    r = next(j for j in range(0, K + 1) if len({b % (1 << j) for b in B}) == m)
    if not (1 <= r <= K):
        fail["r"] += 1
    cl = {}
    for b in B:
        cl.setdefault(b % (1 << (r - 1)), []).append(b)
    sizes = sorted(len(c) for c in cl.values())
    if not (sizes[0] >= 1 and sizes[-1] == 2):
        fail["one or two elements, some two"] += 1
    pairs = [c for c in cl.values() if len(c) == 2]
    if sizes[0] == 1:
        if m < 3:
            fail["(B1) m >= 3"] += 1
        for (y, z) in pairs:
            for (yy, zz) in ((y, z), (z, y)):
                cnt["(B1) checked"] += 1
                a = R(minus(B, [y, z])); b = R(minus(B, [zz]))
                if rb != Fraction(1, 2) * a + Fraction(1, 2) * b:
                    fail["(B1)"] += 1
                both = (a == p(m - 3)) and (b == p(m - 2))
                if both != eq:
                    fail["(B1) equality passes down"] += 1
    else:
        nn = len(pairs)
        if 2 * nn != m:
            fail["(B2) m = 2n"] += 1
        for Y in itertools.product(*pairs):
            cnt["(B2) checked"] += 1
            s = Fraction(0)
            fsum = Fraction(0)
            for u in range(0, nn):
                for U in itertools.combinations(Y, u):
                    U = tuple(sorted(U))
                    s += R(U)
                    if u >= 1:
                        fsum += R(U) - p(u - 1)
            if rb != s / 2 ** nn:
                fail["(B2)"] += 1
            # referee's exact form of the last inequality: rho_2(B) - p_(2n-1) = 2^(-n) (2 p_n + sum of excesses)
            if rb - p(2 * nn - 1) != (2 * p(nn) + fsum) / 2 ** nn:
                fail["(B2) excess form"] += 1
        if (rb > p(m - 1)) != (nn >= 2):
            fail["(B2) strict iff n >= 2"] += 1
print("counts:", dict(cnt))
print("failures:", dict(fail) if fail else "none")
print(f"[{time.time() - t0:.0f} s]")

"""The constructions of proof.md, section 6 (balanced half: 0 in F), built from the words there, and checked against the
referee's pat.py (pattern by exact polynomial division AND by the tree) for every pattern with 0 in F.

usage: construct_bal.py            (runs the default list of groups)
       construct_bal.py p q n      (one group)
"""
import sys, itertools, time
sys.path.insert(0, "/home/agent3/minsize/prove")
from pat import exact_pattern_division, tree_pattern
from claims import rule_value, host_x


def crt_index(p, q, n):
    """idx[u][w] = the x in Z_M with x = u mod p^n and x = w mod q"""
    P = p ** n; M = P * q
    idx = [[None] * q for _ in range(P)]
    for x in range(M):
        idx[x % P][x % q] = x
    return idx


def digit_strings(p, n, free, fixed=None):
    """all u in Z_{p^n} whose digit at level a (the one multiplying p^(a-1)) is free for a in `free`, equals fixed[a] for a
    in `fixed`, and is 0 at every other level.  Yields (u, digits) with digits a dict level -> digit."""
    fixed = fixed or {}
    free = sorted(free)
    for vals in itertools.product(range(p), repeat=len(free)):
        d = dict(fixed)
        d.update(zip(free, vals))
        u = sum(v * p ** (a - 1) for a, v in d.items())
        yield u, d


def construct(p, q, n, E, F):
    """returns (weights on Z_M, description).  0 in F is assumed."""
    E = set(E); F = set(F)
    assert 0 in F
    P = p ** n; M = P * q
    idx = crt_index(p, q, n)
    w = [0] * M
    lv = set(range(1, n + 1))

    def add_fibres(free, fixed, mult):
        for u, _ in digit_strings(p, n, free, fixed):
            for layer in range(q):
                w[idx[u][layer]] += mult

    # (a) F = all levels: fibres over the strings free at E
    if lv <= F:
        add_fibres(E, {}, 1)
        return w, 'all-F'

    a0 = min(a for a in lv if a not in F)
    above = {a for a in lv if a < a0}
    below = {a for a in lv if a > a0}
    G = sorted(a for a in below if a in F and a not in E)       # levels of F minus E deeper than a0
    k1 = len(G)
    T = {a for a in below if a in E or a in F}                  # free digits of the shape part below a0
    H = {a for a in below if a in E and a not in F}
    top_free = {a for a in above if a in E}
    Zq = [1] * q

    def rot(base, plus=(), minus=()):
        r = list(base)
        for i in plus: r[i % q] += 1
        for i in minus: r[i % q] -= 1
        assert min(r) >= 0
        return r

    R_uneq = {0: rot([0] * q, plus=[0]), 1: rot(Zq, minus=[0])}                      # a0 not in E
    R_eq = {i: rot(Zq) for i in range(p)}                                            # a0 in E
    R_eq[0] = rot(Zq, plus=[0], minus=[1]); R_eq[1] = rot(Zq, plus=[1], minus=[0])
    R_two = {0: R_eq[0], 1: R_eq[1]}                                                 # a0 in E, only two children carry shape

    def add_shape_part(top_free, T, H, R):
        """digits free at top_free (above a0) and at T (below a0), 0 elsewhere; digit i at a0 with the rotations R[i];
        tau(u) = 1 if H is not empty and every digit of u at a level of H is nonzero, else 0."""
        for i, Ri in R.items():
            for u, d in digit_strings(p, n, top_free | T, {a0: i}):
                tau = 1 if (H and all(d[a] != 0 for a in H)) else 0
                for r in range(q):
                    if Ri[r]:
                        w[idx[u][(tau + r) % q]] += Ri[r]

    R_std = R_eq if a0 in E else R_uneq
    if k1 == 0:
        add_shape_part(top_free, T, H, R_std)
        return w, 'k\'=0'
    g1 = G[0]
    # host level
    host = None
    cand = sorted(b for b in E if b < a0)
    if cand:
        host = cand[0]
    elif a0 in E and p >= 3:
        host = a0
    elif a0 in E:
        cand = sorted(b for b in E if a0 < b < g1 and b not in F)
        if cand:
            host = cand[0]
    if host is None:
        add_shape_part(top_free, T, H, R_std)
        add_fibres(E, {}, 1)
        return w, 'no host (x=1)'
    b = host
    if b < a0:
        add_shape_part(top_free - {b}, T, H, R_std)
        for i in range(1, p):
            add_fibres(E - {b}, {b: i}, p ** k1)
        return w, 'host above a0'
    if b == a0:
        add_shape_part(top_free, T, H, R_two)
        for i in range(2, p):
            add_fibres(E - {b}, {b: i}, p ** k1)
        return w, 'host = a0'
    add_shape_part(top_free, T - {b}, H - {b}, R_std)
    for i in range(1, p):
        add_fibres(E - {b}, {b: i}, p ** k1)
    return w, 'host below a0'


def all_balanced_patterns(n):
    lv = list(range(1, n + 1))
    for ke in range(n + 1):
        for E in itertools.combinations(lv, ke):
            for kf in range(n + 1):
                for F in itertools.combinations(lv, kf):
                    yield E, (0,) + F


def run(p, q, n, exact=True):
    t0 = time.time()
    cnt = {}; bad = 0; tot = 0
    for E, F in all_balanced_patterns(n):
        w, kind = construct(p, q, n, E, F)
        want = rule_value(p, q, n, E, F[1:])[0]
        size = sum(w)
        got_t = tree_pattern(p, q, n, w)
        ok = (size == want and got_t == (E, F))
        if exact:
            got_d = exact_pattern_division(p, q, n, w)
            ok = ok and got_d == (E, F)
        tot += 1
        cnt[kind] = cnt.get(kind, 0) + 1
        if not ok:
            bad += 1
            if bad <= 10:
                print('   BAD', (p, q, n), 'E', E, 'F', F, kind, 'size', size, 'want', want, 'tree pattern', got_t)
    print(f'p={p} q={q} n={n} (order {p**n*q}): {tot} patterns with 0 in F, {bad} wrong; by kind {dict(sorted(cnt.items()))}; '
          f'{"exact division and tree" if exact else "tree only"}; {time.time()-t0:.0f} s', flush=True)
    return bad


if __name__ == '__main__':
    if len(sys.argv) > 3:
        sys.exit(1 if run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])) else 0)
    total = 0
    groups = []
    for n in (1, 2, 3, 4):
        for (p, q) in [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2), (3, 7), (7, 3), (5, 7), (2, 11), (11, 2), (3, 11)]:
            if p ** n * q <= 2000:
                groups.append((p, q, n))
    groups += [(2, 3, 5), (3, 2, 5), (2, 5, 5), (2, 3, 6)]
    for g in groups:
        total += run(*g, exact=(g[0] ** g[2] * g[1] <= 700))
    print('TOTAL wrong:', total)

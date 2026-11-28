# Referee's own: at d = p^i the events depend only on the sizes of the classes inside the cells.
# All small configurations; exact integers/fractions.  Lemmas B, C, F (any m) and E, E' (m even) of result.md.
# Also: (c1)-(c4), c*, and the maximum of Lemma E'.
import sys, math, itertools, time
from fractions import Fraction as Fr

CE = [Fr(1)] + [Fr(math.comb(r, r // 2), 2 ** r) for r in range(1, 4100)]
def c(x):
    return CE[x] if x > 0 else Fr(1)

def cnt_sum(r, v):          # number of signings of r elements with sum v
    if (r + v) % 2 or abs(v) > r:
        return 0
    return math.comb(r, (r + v) // 2)

def small_facts():
    ok1 = all(CE[r + 1] <= CE[r] for r in range(0, 4050)) and all(CE[r] <= Fr(1, 2) for r in range(1, 4050))
    ok2 = all(c(x - 2) <= 2 * c(x) for x in range(-6, 4050))
    # c_r <= sqrt(2/(pi r))  <=>  c_r^2 * r * pi <= 2 ; with pi > 3.14159265358979
    PI_LOW = Fr(314159265358979, 10 ** 14)
    ok3 = all(CE[r] * CE[r] * r * Fr(3141592653589794, 10 ** 15) <= 2 for r in range(1, 4050))   # pi < 3.141592653589794
    n4 = 0
    ok4 = True
    eq4 = 0
    for n in range(1, 6):
        for a in itertools.combinations_with_replacement(range(1, 13 if n <= 3 else (9 if n == 4 else 7)), n):
            A = sum(a)
            lhs = Fr(1)
            for x in a:
                lhs *= CE[x]
            rhs = c(A - 2 * (n - 1)) / 2 ** (n - 1)
            n4 += 1
            if lhs > rhs:
                ok4 = False
            if lhs == rhs:
                eq4 += 1
    print("(c1) %s  (c2) %s  (c3) %s  (c4) on %d tuples: %s (equality %d times)" % (ok1, ok2, ok3, n4, ok4, eq4))
    cs = {r: Fr(math.comb(r, r // 2 + 1), 2 ** r) for r in range(2, 400, 2)}
    print("c*_r <= 1/4 and non-increasing from 4, <= c_r, r <= 398:", all(cs[r] <= Fr(1, 4) and cs[r] <= CE[r] for r in cs) and all(cs[r + 2] <= cs[r] for r in range(4, 396, 2)),
          " c*_2, c*_4 =", cs[2], cs[4], " c*_32 = %.6f < 17/128 = %.6f: %s" % (float(cs[32]), 17 / 128, cs[32] < Fr(17, 128)))
    # is c*_r really the largest share of a value other than 0 ?
    print("c*_r = max over v != 0 of P_r(v), even r <= 60:", all(max(cnt_sum(r, v) for v in range(-r, r + 1) if v) == math.comb(r, r // 2 + 1) for r in range(2, 61, 2)))
    best = (Fr(0), None)
    for a in range(2, 61, 2):
        for b in range(2, a + 1, 2):
            v = Fr(sum(cnt_sum(a, x) * cnt_sum(b, x) for x in range(-b, b + 1) if x), 2 ** (a + b))
            if v > best[0]:
                best = (v, (a, b))
    print("largest sum over v != 0 of P_a(v) P_b(v), a, b even <= 60:", best)
    # Lemma E' directly: all even l, a, b <= 40
    worst = (Fr(0), None)
    for l in range(2, 41, 2):
        for a in range(2, 41, 2):
            for b in range(2, a + 1, 2):
                v = Fr(sum(cnt_sum(l, x) * cnt_sum(a, x) * cnt_sum(b, x) for x in range(-b, b + 1) if x), 2 ** (l + a + b))
                q = v / (Fr(17, 128) * CE[l])
                if q > worst[0]:
                    worst = (q, (l, a, b))
    print("Lemma E' on all even (l, a, b) <= 40: largest quotient", worst, float(worst[0]))

ST = {"configs": 0, "B,C checks": 0, "C equal": 0, "F equal": 0, "even configs": 0, "E pairs": 0, "E positive": 0, "E' cases": 0, "fail": 0}
MX = {"E": (Fr(0), None), "E'": (Fr(0), None), "B": (Fr(0), None), "C": (Fr(0), None), "F": (Fr(0), None)}

def check(p, cells):
    """cells: list of tuples of class sizes (nonzero entries only); full iff len == p"""
    k = len(cells)
    m = sum(sum(cl) for cl in cells)
    N = k + p - 1
    # counts
    total_flat = 1
    conv = {0: 1}          # distribution of the sum of the common values over the full cells, all cells flat
    for cl in cells:
        if len(cl) == p:
            lo = min(cl)
            dist = {}
            for v in range(-lo, lo + 1):
                w = 1
                for r in cl:
                    w *= cnt_sum(r, v)
                    if not w:
                        break
                if w:
                    dist[v] = w
            new = {}
            for s0, w0 in conv.items():
                for v, w in dist.items():
                    new[s0 + v] = new.get(s0 + v, 0) + w0 * w
            conv = new
        else:
            w = 1
            for r in cl:
                w *= cnt_sum(r, 0)
            conv = {s0: w0 * w for s0, w0 in conv.items()} if w else {}
    bad_d = sum(conv.values())
    bad_d_and_1 = conv.get(0, 0)
    Pd = Fr(bad_d, 2 ** m)
    Pn = Fr(bad_d - bad_d_and_1, 2 ** m)
    ST["configs"] += 1
    info = (p, cells)
    for cl in cells:
        if len(cl) == p:
            ST["B,C checks"] += 1
            s = sorted(cl)
            bB = c(-(-m // N)) / 2 ** (N - 2)
            bC = c(s[1]) * c(m - s[0] - s[1] - 2 * (N - 3)) / 2 ** (N - 3)
            if Pd > bB:
                ST["fail"] += 1; print("FAILURE Lemma B", info)
            if Pd > bC:
                ST["fail"] += 1; print("FAILURE Lemma C", info)
            if Pd == bC:
                ST["C equal"] += 1
            if Pd / bB > MX["B"][0]: MX["B"] = (Pd / bB, info)
            if Pd / bC > MX["C"][0]: MX["C"] = (Pd / bC, info)
    sizes = [r for cl in cells for r in cl]
    l = max(sizes)
    sres = m - l
    bF = c(l) * c(-(-sres // 2) - 2 * (N - 3)) / 2 ** (N - 3)
    if Pd > bF:
        ST["fail"] += 1; print("FAILURE Lemma F", info)
    if Pd == bF:
        ST["F equal"] += 1
    if Pd / bF > MX["F"][0]: MX["F"] = (Pd / bF, info)
    if m % 2 == 0:
        ST["even configs"] += 1
        if Pn > 0:
            ST["E positive"] += 1
        for l in set(sizes):
            ST["E pairs"] += 1
            bE = c(l) / 2 ** (k + 2 * p - 5)
            if Pn > bE:
                ST["fail"] += 1; print("FAILURE Lemma E", info, l)
            if Pn / bE > MX["E"][0]: MX["E"] = (Pn / bE, (info, l))
            if p == 3 and k == 1:
                ST["E' cases"] += 1
                b2 = Fr(17, 128) * c(l)
                if Pn > b2:
                    ST["fail"] += 1; print("FAILURE Lemma E'", info, l)
                if Pn / b2 > MX["E'"][0]: MX["E'"] = (Pn / b2, (info, l))

def run(p, kmax_sizes, budget, t0):
    """kmax_sizes: list of (number of cells, set of class sizes)"""
    for k, S in kmax_sizes:
        types = []
        for nz in range(1, p + 1):
            for cl in itertools.combinations_with_replacement(sorted(S), nz):
                types.append(cl)
        nconf = 0
        for cells in itertools.combinations_with_replacement(types, k):
            if not any(len(cl) == p for cl in cells):
                continue
            check(p, list(cells))
            nconf += 1
            if time.time() - t0 > budget:
                print("  stopped by the time budget in p = %d, k = %d" % (p, k)); return
        print("p = %d, %d cells, class sizes from %s: %d configurations; totals %s" % (p, k, sorted(S), nconf, ST), flush=True)

if __name__ == "__main__":
    t0 = time.time()
    budget = float(sys.argv[1])
    small_facts()
    run(3, [(1, set(range(1, 41))), (2, {1, 2, 3, 4, 5, 6, 7, 8, 12, 17}), (3, {1, 2, 3, 4, 6, 9}), (4, {1, 2, 3, 4})], budget, t0)
    run(5, [(1, {1, 2, 3, 4, 5, 6, 9, 14}), (2, {1, 2, 3, 4, 7}), (3, {1, 2, 3})], budget, t0)
    run(7, [(1, {1, 2, 3, 4, 5, 8}), (2, {1, 2, 3})], budget, t0)
    print("totals:", ST)
    for k_ in MX:
        print("  largest quotient in Lemma %s: %s = %.6f at %s" % (k_, MX[k_][0], float(MX[k_][0]), str(MX[k_][1])[:150]))

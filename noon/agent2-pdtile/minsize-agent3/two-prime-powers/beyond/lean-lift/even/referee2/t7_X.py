# t7_X.py -- section 5: ranks over F_2 from the definition; Lemma X (i), (ii), (iii); Lemma Y; Lemma A (a), (b);
# Proposition K (R - R_fib); the five supports of 5.4.
# A_e = Z[eta_e]/2 = F_2[X]/(Phi_e mod 2); pi_e(delta_w) = X^w.  Vectors are Python integers (bit k = coefficient of X^k).
# usage: t7_X.py examples | lemmaX | lemmaY | lemmaA | propK
import sys, random
from itertools import combinations
from rlib import *

_pi = {}
def pi(e, w):
    # pi_e(delta_w) as an integer bitmask
    if e not in _pi:
        T = powtable(e) % 2
        _pi[e] = [sum(1 << k for k in range(T.shape[1]) if T[b, k]) for b in range(e)]
    return _pi[e][w % e]

def insert(basis, v):
    # basis: dict highest-bit -> vector; returns True if v was independent
    while v:
        h = v.bit_length() - 1
        if h in basis:
            v ^= basis[h]
        else:
            basis[h] = v
            return True
    return False

def rank(vs):
    b = {}
    return sum(insert(b, v) for v in vs)

def span_basis(vs):
    b = {}
    for v in vs:
        insert(b, v)
    return list(b.values())

def intersect(U, V, width):
    # bases U, V of two subspaces of F_2^width; returns a basis of the intersection (Zassenhaus)
    b = {}
    for u in U:
        insert(b, (u << width) | u)
    for v in V:
        insert(b, v << width)
    return [x for x in b.values() if x < (1 << width)]

def D(e, W):
    return rank([pi(e, w) for w in W])

def PHI(e, pts):
    r = 0
    for w in pts:
        r ^= pi(e, w)
    return r

def dangerous(e, W2):
    return PHI(e, W2) == 0

def live(e, W):
    for p, i in factor(e).items():
        if i not in live_levels(W, p, i):
            return False
    return True

def lemmaX_check(e, p, W, W2):
    # returns (D_e from the definition, the right side of (i), (ii) holds, (iii) holds for every r, sum_r dim V_r)
    f = factor(e)
    i = f[p]
    e2 = e // p ** i
    width = len(cyclo(e2)) - 1
    rhs = 0
    sumVr = 0
    ok3 = True
    dang_pred = True
    for r in range(p ** (i - 1)):
        Vs = []
        phis = []
        allpts = []
        for t in range(p):
            c = r + t * p ** (i - 1)
            pts = [w for w in W if w % p ** i == c]
            allpts += pts
            Vs.append(span_basis([pi(e2, w) for w in pts]))
            phis.append(PHI(e2, [w for w in W2 if w % p ** i == c]))
        inter = Vs[0]
        for V in Vs[1:]:
            inter = intersect(inter, V, width)
        term = sum(len(V) for V in Vs) - len(inter)
        rhs += term
        dVr = rank([pi(e2, w) for w in allpts])
        sumVr += dVr
        if term < dVr + (p - 2) * len(inter):
            ok3 = False
        if len(set(phis)) != 1:
            dang_pred = False
        else:
            # then they equal Phi(r)
            assert phis[0] == PHI(e2, [w for w in W2 if w % p ** (i - 1) == r])
    return D(e, W), rhs, dang_pred == dangerous(e, W2), ok3, sumVr

mode = sys.argv[1]
random.seed(31)

if mode == 'examples':
    def show(n, W2, W, es):
        for e in es:
            print(f"  Z_{n}: e = {e}: live {live(e, W)}, dangerous {dangerous(e, W2)}, D_e(W) = {D(e, W)}")
    print("1.")
    W2 = [0, 15, 30]; W = W2 + [1, 2, 28, 29]
    show(45, W2, W, [3, 9, 5, 15, 45]); print("   live levels of 3:", live_levels(W, 3, 2), " of 5:", live_levels(W, 5, 1))
    print("2.")
    W2 = [0, 35, 70]; W = W2 + [1, 2, 3, 4, 69, 89]
    show(105, W2, W, [3, 5, 7, 15, 21, 35, 105]); print("   live levels of 3, 5, 7:", live_levels(W, 3, 1), live_levels(W, 5, 1), live_levels(W, 7, 1))
    print("3.")
    W2 = [0, 45, 90, 135, 180]; W = W2 + [1, 2, 3, 204]
    show(225, W2, W, [3, 9, 5, 25, 15, 45, 75, 225])
    for i in (1, 2):
        cls = {}
        for w in W2:
            cls.setdefault(w % 3 ** i, []).append(w)
        print(f"   (25, {i}) fibrewise:", all(PHI(25, pts) == 0 for pts in cls.values()))
    print("4.")
    W = [0 + 45 * t for t in range(5)] + [1 + 45 * t for t in range(5)] + [2 + 45 * t for t in range(5)]
    show(225, W, W, [25, 75, 225]); print("   D_25(W) =", D(25, W))
    print("5.")
    W2 = [0, 3, 6, 9, 12]; W = W2 + [5, 10]
    show(15, W2, W, [3, 5, 15]); print("   D_5(W) =", D(5, W))

elif mode == 'lemmaX':
    tot = 0; dang = 0
    for n in (15, 21, 35, 45, 63, 75, 105, 135, 165, 225, 315, 385, 525, 945, 1155):
        f = factor(n)
        cnt = 0
        for _ in range(700):
            style = random.random()
            W = set()
            size = min(random.randint(3, 16), n - 2)
            if style < 0.3:
                W = set(random.randrange(n) for _ in range(size))
            elif style < 0.75:   # unions of cosets of prime order and a few points
                while len(W) < size:
                    q = random.choice(list(f)); x = random.randrange(n)
                    W |= set((x + t * (n // q)) % n for t in range(q))
                W |= set(random.randrange(n) for _ in range(random.randint(0, 3)))
            else:                # a pattern on Z_{e2} repeated in the classes modulo a prime
                q = random.choice(list(f)); base = set(random.randrange(n) for _ in range(random.randint(1, 4)))
                for x in base:
                    W |= set((x + t * (n // q)) % n for t in range(q))
                W |= set(random.randrange(n) for _ in range(random.randint(0, 2)))
            W = sorted(W)
            # W2: either all of W, or W minus a few points
            W2 = W if random.random() < 0.6 else [w for w in W if random.random() < 0.8]
            for e in divisors(n):
                if e == 1:
                    continue
                for p in factor(e):
                    d, rhs, ok2, ok3, sumVr = lemmaX_check(e, p, W, W2)
                    assert d == rhs, ("Lemma X (i) fails", n, e, p, W)
                    assert ok2, ("Lemma X (ii) fails", n, e, p, W, W2)
                    assert ok3, ("Lemma X (iii) fails", n, e, p, W)
                    e2 = e // p ** factor(e)[p]
                    assert d >= sumVr >= D(e2, W)
                    tot += 1
                    dang += dangerous(e, W2)
            cnt += 1
        print(f"n = {n}: {cnt} supports: Lemma X (i) exactly, (ii), (iii) and D_e >= sum_r dim V_r >= D_e2 for every e | n, e > 1, and every prime p | e", flush=True)
    print(f"total triples (W, e, p): {tot}; of them with e dangerous: {dang}")

elif mode == 'lemmaY':
    # exhaustive: no g of odd weight < q (q the least prime of e) has pi_e(g) = 0.  By translation, 0 is in the support;
    # by reduction modulo e (which keeps the parity of the weight and does not enlarge the support), n' = e.
    for e in (5, 7, 11, 13, 25, 35, 55, 65, 85, 95, 125, 175, 275, 49, 77, 91, 119, 121, 143):
        q = min(factor(e))
        found = 0
        tested = 0
        vec = [pi(e, w) for w in range(e)]
        for size in range(1, q, 2):
            if size >= 7 and e > 30:
                break
            if size == 5 and e > 100:
                break
            for rest in combinations(range(1, e), size - 1):
                v = vec[0]
                for w in rest:
                    v ^= vec[w]
                tested += 1
                if v == 0:
                    found += 1
        # and the bound is attained: the coset of order q
        coset = [t * (e // q) for t in range(q)]
        print(f"e = {e}: least prime {q}: sets with 0 of odd size < {q} tested: {tested} (sizes up to {min(q - 2, 5 if e > 30 else q - 2) if e <= 100 else min(q - 2, 3)}); "
              f"dangerous among them: {found}; the coset of order {q} is dangerous: {PHI(e, coset) == 0}", flush=True)

elif mode == 'lemmaA':
    # supports built on Z_{3^a e2}: f = sum over c in Z_{3^a} of delta_c (x) g_c, with the values Phi(class) prescribed down the
    # 3-tree: chosen dangerous levels split a class into three children with the same Phi; other levels split at random.
    stats = {'a': 0, 'b': 0, 'a_slack0': 0, 'b_slack0': 0, 'a_viol': 0, 'b_viol': 0, 'b_lge2': 0, 'a_lge2': 0}
    for a, e2 in ((2, 5), (3, 5), (2, 7), (3, 7), (2, 25), (2, 35), (3, 35), (4, 5), (2, 11), (2, 55)):
        n = 3 ** a * e2
        width = len(cyclo(e2)) - 1
        inv3 = pow(3 ** a, -1, e2)
        def point(c, k):
            # the residue modulo n that is c mod 3^a and k mod e2
            return (c + 3 ** a * (((k - c) * inv3) % e2)) % n
        fe2 = factor(e2)
        for trial in range(1500):
            root_zero = random.random() < 0.6          # e2 dangerous or not
            dang_levels = set(i for i in range(1, a + 1) if random.random() < 0.6)
            i1 = random.randint(1, a - 1) if root_zero else 0
            # values down the tree
            def rnd():
                return random.getrandbits(width) if random.random() < 0.7 else (1 << random.randrange(width))
            vals = {(): 0 if root_zero else (rnd() or 1)}
            level = [()]
            for depth in range(1, a + 1):
                new = []
                for node in level:
                    v = vals[node]
                    if root_zero and depth < i1:
                        ch = [0, 0, 0]
                    elif root_zero and depth == i1:
                        x, y = rnd(), rnd()
                        ch = [x, y, x ^ y] if random.random() < 0.7 else [0, 0, 0]
                    elif depth in dang_levels:
                        ch = [v, v, v]
                    else:
                        x, y = rnd(), rnd()
                        ch = [x, y, v ^ x ^ y] if random.random() < 0.5 else [v, 0, 0]
                    for t in range(3):
                        vals[node + (t,)] = ch[t]
                        new.append(node + (t,))
                level = new
            W2 = set()
            for node in level:
                c = sum(t * 3 ** j for j, t in enumerate(node))
                v = vals[node]
                g = set(k for k in range(width) if (v >> k) & 1)
                # add kernel elements of pi_e2 at random (cosets of prime order in Z_e2), sometimes
                if random.random() < 0.3:
                    q = random.choice(list(fe2)); x = random.randrange(e2)
                    g ^= set((x + t * (e2 // q)) % e2 for t in range(q))
                for k in g:
                    W2.add(point(c, k))
            if not W2:
                continue
            W = set(W2)
            for _ in range(random.randint(0, 4)):
                W.add(random.randrange(n))
            W = sorted(W); W2 = sorted(W2)
            # now read everything off the support itself, from the definitions
            de2 = D(e2, W)
            e2_d = dangerous(e2, W2)
            dlev = [i for i in range(1, a + 1) if dangerous(3 ** i * e2, W2)]
            def active_classes(depth):
                cls = {}
                for w in W2:
                    cls.setdefault(w % 3 ** depth, []).append(w)
                return sum(1 for pts in cls.values() if PHI(e2, pts) != 0)
            for i in dlev:
                e = 3 ** i * e2
                de = D(e, W)
                if not e2_d:
                    lp = sum(1 for j in dlev if j <= i)
                    stats['a'] += 1
                    stats['a_lge2'] += (lp >= 2)
                    lhs = de - max(de2 + 3 ** (lp - 1), 2 * 3 ** (lp - 1))
                    if lhs < 0:
                        stats['a_viol'] += 1
                        print("Lemma A (a) FAILS", n, e, W, W2)
                    stats['a_slack0'] += (de == de2 + 3 ** (lp - 1))
                else:
                    if active_classes(i - 1) == 0:
                        continue
                    i_1 = next(d for d in range(0, a + 1) if active_classes(d) > 0)
                    lpp = sum(1 for j in dlev if i_1 < j <= i)
                    stats['b'] += 1
                    stats['b_lge2'] += (lpp >= 2)
                    if lpp < 1 or de < de2 + 1 + 2 * 3 ** (lpp - 1):
                        stats['b_viol'] += 1
                        print("Lemma A (b) FAILS", n, e, W, W2)
                    stats['b_slack0'] += (de == de2 + 1 + 2 * 3 ** (lpp - 1))
        print(f"n = {n} (3^{a} * {e2}): cumulative: cases of (a): {stats['a']} (with l' >= 2: {stats['a_lge2']}; equality {stats['a_slack0']}; violations {stats['a_viol']}); "
              f"cases of (b): {stats['b']} (with l'' >= 2: {stats['b_lge2']}; equality {stats['b_slack0']}; violations {stats['b_viol']})", flush=True)

elif mode == 'propK':
    # R, R_fib from the definitions, for multisets with an odd number of elements on odd moduli
    LIM = Fraction(80118, 100000)
    worst = None; worstR = None; nfib = 0; tot = 0
    for n in (15, 45, 75, 105, 135, 225, 315, 525, 675, 945):
        f = factor(n)
        a = f.get(3, 0)
        cnt = 0
        for _ in range(500):
            style = random.random()
            W2 = set(); W = set()
            if style < 0.2:
                W2 = set(random.randrange(n) for _ in range(random.randint(3, 13)))
            elif style < 0.6:    # cosets of prime order q >= 5 inside classes modulo 3^i (fibrewise shape), plus pairs
                i = random.randint(1, a)
                qs = [q for q in f if q != 3]
                for c in range(3):
                    if random.random() < 0.85:
                        q = random.choice(qs)
                        x = random.randrange(n)
                        x = x - (x % 3 ** i) + 0  # class 0 modulo 3^i, then shift by c*3^(i-1)
                        x = (x + c * 3 ** (i - 1) * (n // 3 ** a) * pow(n // 3 ** a, -1, 3 ** a)) % n
                        W2 ^= set((x + t * (n // q)) % n for t in range(q))
                for _ in range(random.randint(0, 3)):
                    W.add(random.randrange(n))
            else:                # unions of cosets of any prime order
                for _ in range(random.randint(1, 4)):
                    q = random.choice(list(f)); x = random.randrange(n)
                    W2 ^= set((x + t * (n // q)) % n for t in range(q))
                for _ in range(random.randint(0, 2)):
                    W.add(random.randrange(n))
            W |= W2
            if len(W2) % 2 == 0:
                x = random.randrange(n)
                W2 ^= {x}; W.add(x)
            if not W2:
                continue
            W = sorted(W); W2 = sorted(W2)
            R = Fraction(0); Rfib = Fraction(0)
            for e in divisors(n):
                if e == 1 or not live(e, W) or not dangerous(e, W2):
                    continue
                term = Fraction(2, 2 ** D(e, W))
                R += term
                i = factor(e).get(3, 0)
                e2 = e // 3 ** i
                if i >= 1 and e2 > 1:
                    cls = {}
                    for w in W2:
                        cls.setdefault(w % 3 ** i, []).append(w)
                    if all(PHI(e2, pts) == 0 for pts in cls.values()):
                        Rfib += term
            tot += 1; cnt += 1
            nfib += (Rfib > 0)
            assert R - Rfib < LIM, ("Proposition K fails", n, W, W2, R, Rfib)
            if worst is None or R - Rfib > worst[0]:
                worst = (R - Rfib, n, W2)
            if worstR is None or R > worstR[0]:
                worstR = (R, n, W2, Rfib)
        print(f"n = {n}: {cnt} pairs (W_2, W), |W_2| odd: R - R_fib < 0.80118 every time; so far largest R - R_fib = {worst[0]} = {float(worst[0]):.4f}, largest R = {worstR[0]} = {float(worstR[0]):.4f} (R_fib {worstR[3]}); with R_fib > 0: {nfib}", flush=True)

elif mode == 'fib9':
    # nine elements: R_fib from the definition, on the shape of equality of Corollary K's proof and on random multisets;
    # which e2 occur in a fibrewise pair with 3^i e2 live; the text's bound 3/16 and the sharper 1/8
    from collections import Counter
    for n in (15, 45, 75, 105, 135, 315, 525, 225):
        f = factor(n); a = f[3]; rest = n // 3 ** a
        inv = pow(3 ** a, -1, rest)
        def point(c, k):
            return (c + 3 ** a * (((k - c) * inv) % rest)) % n
        seen = Counter(); maxfib = Fraction(0); maxR = Fraction(0); cnt = 0; nfib = 0; several_i = 0
        for trial in range(1500):
            if trial % 3 < 2:
                i = random.randint(1, a)
                r0 = random.randrange(3 ** i)
                def in_class(r):
                    return (r + 3 ** i * random.randrange(3 ** (a - i))) % 3 ** a
                q5 = 5 ** random.randint(1, f[5])
                base = random.randrange(rest)
                # five points: a coset of order 5 in Z_rest (or of the subgroup of order 5 of the 5^j-part)
                step = rest // 5 if random.random() < 0.7 else (rest // q5) * (q5 // 5)
                B = [point(in_class(r0), (base + t * step) % rest) for t in range(5)]
                for s in (1, 2):
                    r = (r0 + s * 3 ** (i - 1)) % 3 ** i
                    k = random.randrange(rest)
                    x = point(in_class(r), k)
                    y = x if random.random() < 0.5 else point(in_class(r), k)
                    B += [x, y]
            else:
                B = [random.randrange(n) for _ in range(9)]
            c = Counter(B)
            W = sorted(c); W2 = sorted(x for x in c if c[x] % 2)
            R = Fraction(0); Rfib = Fraction(0); levels_i = set()
            for e in divisors(n):
                if e == 1 or not live(e, W) or not dangerous(e, W2):
                    continue
                term = Fraction(2, 2 ** D(e, W))
                R += term
                i3 = factor(e).get(3, 0); e2 = e // 3 ** i3
                if i3 >= 1 and e2 > 1:
                    cls = {}
                    for w in W2:
                        cls.setdefault(w % 3 ** i3, []).append(w)
                    if all(PHI(e2, pts) == 0 for pts in cls.values()):
                        Rfib += term
                        seen[e2] += 1
                        levels_i.add(i3)
            cnt += 1
            nfib += (Rfib > 0)
            several_i += (len(levels_i) > 1)
            maxfib = max(maxfib, Rfib); maxR = max(maxR, R)
            assert Rfib <= Fraction(3, 16) and R < Fraction(9887, 10000)
        print(f"n' = {n}: {cnt} multisets of nine elements ({nfib} with a fibrewise live pair): largest R_fib {maxfib}, largest R {maxR} = {float(maxR):.4f}; "
              f"e2 of the fibrewise live pairs: {dict(seen)}; multisets with fibrewise live pairs at two different i: {several_i}", flush=True)

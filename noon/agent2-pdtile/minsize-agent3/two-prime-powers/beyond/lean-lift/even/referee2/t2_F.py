# t2_F.py -- Lemma F and Theorem F: the construction, written from the proof in the text (four cases), tested exactly.
# usage: t2_F.py pure | mixed | general | squares
#  pure    : every multiset on Z_{2^K}: properties (0), (1..K) of Lemma F and "3-bad at no 2^j" by the definition
#  mixed   : every multiset (up to a size) on n = 2^k 3^a: the signing for the residues modulo 2^k is good on Z_n
#  general : n with primes >= 5: every multiset without a live level at a prime >= 5: good on Z_n
#  squares : n with 25 | n: multisets that meet at most four classes modulo 5 (the parenthesis of section 0)
import sys, random
from rlib import *

def zero_signs(r):
    # r >= 2 signs with sum = 0 mod 3: t minus signs, t = -r mod 3
    assert r >= 2
    t = (-r) % 3
    return [-1] * t + [1] * (r - t)

def nonzero_signs(r):
    assert r >= 1
    return [1] * r if r % 3 else [-1] + [1] * (r - 1)

def is_distinct_pair(vals):
    return len(vals) == 2 and vals[0] != vals[1]

def v2(x):
    assert x != 0
    v = 0
    while x % 2 == 0:
        x //= 2
        v += 1
    return v

def lemmaF(vals, K):
    # vals: list of residues modulo 2^K (a multiset), nonempty, not a pair of distinct elements.
    # returns the list of signs, in the order of vals
    m = len(vals)
    assert m >= 1 and not is_distinct_pair(vals)
    if K == 0:
        return nonzero_signs(m)
    Ei = [i for i in range(m) if vals[i] % 2 == 0]
    Di = [i for i in range(m) if vals[i] % 2 == 1]
    Ev = [vals[i] // 2 for i in Ei]
    Dv = [vals[i] // 2 for i in Di]
    sg = [0] * m
    def put(idx, s):
        for i, e in zip(idx, s):
            sg[i] = e
    if not Di:
        put(Ei, lemmaF(Ev, K - 1)); return sg
    if not Ei:
        put(Di, lemmaF(Dv, K - 1)); return sg
    if len(Ei) == 1 or len(Di) == 1:
        if len(Ei) == 1:
            Ci, Ai = Ei, Di
        else:
            Ci, Ai = Di, Ei
        assert len(Ai) >= 2
        put(Ai, zero_signs(len(Ai))); put(Ci, [1]); return sg
    # both halves have at least two elements
    if not is_distinct_pair(Ev):
        put(Ei, lemmaF(Ev, K - 1)); put(Di, zero_signs(len(Di))); return sg
    if not is_distinct_pair(Dv):
        put(Di, lemmaF(Dv, K - 1)); put(Ei, zero_signs(len(Ei))); return sg
    vE = v2(Ev[0] - Ev[1]); vD = v2(Dv[0] - Dv[1])
    if vD >= vE:
        put(Ei, [1, -1]); put(Di, [1, 1])
    else:
        put(Ei, [1, 1]); put(Di, [1, -1])
    return sg

def props_lemmaF(vals, sg, K):
    # (0) and (j), j = 1..K, checked from their statement
    if sum(sg) % 3 == 0:
        return False
    for j in range(1, K + 1):
        sums = {}
        for x, e in zip(vals, sg):
            sums[x % 2 ** j] = sums.get(x % 2 ** j, 0) + e
        ok = False
        for r in range(2 ** (j - 1)):
            if (sums.get(r, 0) - sums.get(r + 2 ** (j - 1), 0)) % 3 != 0:
                ok = True
                break
        if not ok:
            return False
    return True

def check_good(E, SG, n):
    # E: N x m residues, SG: N x m signs; returns boolean N: good on Z_n (exact)
    g = np.ones(len(E), dtype=bool)
    for d in divisors(n):
        T = powtable(d)
        R = np.einsum('nm,nmf->nf', SG, T[E % d])
        g &= R.any(axis=1)
    return g

def check_3good(E, SG, n3):
    g = np.ones(len(E), dtype=bool)
    for d in divisors(n3):
        T = powtable(d)
        R = np.einsum('nm,nmf->nf', SG, T[E % d])
        g &= (R % 3).any(axis=1)
    return g

def no_live_big(B, n):
    for q, a in factor(n).items():
        if q >= 5 and live_levels(B, q, a):
            return False
    return True

def run_batch(n, batch, stats):
    k = vp(n, 2)
    E = np.array(batch, dtype=np.int64)
    SG = np.array([lemmaF([b % 2 ** k for b in B], k) for B in batch], dtype=np.int64)
    g = check_good(E, SG, n)
    stats['tested'] += len(batch)
    if not g.all():
        bad = [batch[i] for i in np.nonzero(~g)[0]]
        stats['fail'] += len(bad)
        if len(stats['examples']) < 5:
            stats['examples'] += bad[:5]

mode = sys.argv[1]
random.seed(2026)

if mode == 'pure':
    for K, mmax in ((0, 12), (1, 12), (2, 10), (3, 7), (4, 6), (5, 5)):
        n = 2 ** K
        tested = pairs = 0
        for m in range(1, mmax + 1):
            for B in multisets(n, m):
                if is_distinct_pair(list(B)):
                    pairs += 1
                    continue
                sg = lemmaF(list(B), K)
                assert props_lemmaF(B, sg, K), (K, B, sg)
                # by the definition: 3-bad at no 2^j
                for j in range(K + 1):
                    T = powtable(2 ** j)
                    r = np.array(sg) @ T[np.array(B) % 2 ** j]
                    assert (r % 3).any(), (K, B, sg, j)
                tested += 1
        print(f"Z_{n}: every multiset of 1..{mmax} elements: {tested} signed by the construction, (0),(1..K) hold and 3-bad at no 2^j; {pairs} pairs of distinct elements skipped", flush=True)
    # every nonempty subset of Z_16 and Z_32 (sets): sample for 32
    K = 4
    from itertools import combinations
    cnt = 0
    for m in range(1, 17):
        for B in combinations(range(16), m):
            if m == 2:
                continue
            sg = lemmaF(list(B), K)
            assert props_lemmaF(B, sg, K)
            cnt += 1
    print(f"Z_16: every nonempty subset that is not a pair: {cnt}: ok")
    for K in (5, 6, 7, 8, 10):
        n = 2 ** K
        cnt = 0
        for _ in range(20000):
            m = random.randint(3, 40)
            style = random.random()
            if style < 0.3:
                B = [random.randrange(n) for _ in range(m)]
            elif style < 0.6:   # few residues, deep tree
                base = random.sample(range(n), random.randint(1, 4))
                B = [random.choice(base) for _ in range(m)]
            elif style < 0.8:   # closed under +n/2
                h = [random.randrange(n // 2) for _ in range(m // 2 + 1)]
                B = h + [x + n // 2 for x in h]
            else:               # two pairs deep in the tree plus shifts
                B = [random.randrange(n) for _ in range(2)]
                B = B + [(B[0] + 2 ** random.randrange(K)) % n, (B[1] + 2 ** random.randrange(K)) % n]
            if is_distinct_pair(B):
                continue
            sg = lemmaF(B, K)
            assert props_lemmaF(B, sg, K), (K, B)
            cnt += 1
        print(f"Z_{n}: {cnt} random and structured multisets (3 to about 80 elements): ok", flush=True)

elif mode in ('mixed', 'general', 'general2'):
    if mode == 'mixed':
        plan = [(6, 9), (12, 7), (18, 6), (24, 5), (36, 5), (48, 4), (54, 4), (72, 4), (96, 3), (108, 3), (144, 3), (162, 3)]
    else:
        plan = [(10, 8), (20, 6), (40, 5), (30, 5), (60, 4), (70, 4), (120, 3), (140, 3), (84, 3), (150, 3), (100, 3)]
    if mode == 'general2':
        plan = [(50, 5), (14, 8), (28, 6), (22, 6)]
    for n, mmax in plan:
        stats = {'tested': 0, 'fail': 0, 'examples': []}
        exc = skipped = 0
        batch = []
        k = vp(n, 2)
        for m in range(1, mmax + 1):
            for B in multisets(n, m):
                if is_exceptional(B, n):
                    exc += 1
                    # confirm: no good signing at all
                    assert not good_mask(list(B), n).any()
                    continue
                if mode != 'mixed' and m >= 5 and not no_live_big(B, n):
                    skipped += 1
                    continue
                batch.append(B)
                if len(batch) >= 20000:
                    run_batch(n, batch, stats); batch = []
            if batch:
                run_batch(n, batch, stats); batch = []
        print(f"n = {n}: every multiset of 1..{mmax} elements: {stats['tested']} signed by the construction, failures {stats['fail']} {stats['examples']}; "
              f"{exc} exceptional pairs (no good signing, confirmed); {skipped} with a live level at a prime >= 5 skipped", flush=True)

elif mode == 'squares':
    # the parenthesis of section 0: "B meets at most four classes modulo every prime q >= 5 that divides n"
    for n, mmax in (((50, 6), (100, 5), (25, 6), (75, 5)) if len(sys.argv) < 3 else ((25, 7), (50, 5), (75, 5))):
        tot = fail = live = fail_notlive = 0
        ex = None
        k = vp(n, 2)
        for m in range(3, mmax + 1):
            for B in multisets(n, m, with0=True):
                if len(set(b % 5 for b in B)) > 4:
                    continue
                tot += 1
                sg = lemmaF([b % 2 ** k for b in B], k)
                E = np.array([B]); SG = np.array([sg])
                ok = bool(check_good(E, SG, n)[0])
                nl = no_live_big(B, n)
                live += (not nl)
                if not ok:
                    fail += 1
                    if nl:
                        fail_notlive += 1
                    if ex is None:
                        ex = (B, sg)
        print(f"n = {n}: multisets with 0 of 3..{mmax} elements meeting at most four classes modulo 5: {tot}; of them with a live level of 5 (level 2): {live}; "
              f"construction not good: {fail} (of them without a live level: {fail_notlive}); first example {ex}", flush=True)
    # the example of the report
    B = (0, 20, 40, 60, 80); n = 100
    sg = lemmaF([b % 4 for b in B], 2)
    print("example: n = 100, B =", B, "signs", sg, "good:", bool(check_good(np.array([B]), np.array([sg]), n)[0]),
          "; live levels of 5:", live_levels(B, 5, 2), "; classes modulo 5 met:", len(set(b % 5 for b in B)),
          "; share of good signings by brute force:", frac(good_mask(list(B), n).sum(), 16))

elif mode == 'random':
    # larger multisets: n = 2^k 3^a, and n with primes >= 5 where B has no live level at them
    def gen(n, m):
        k = vp(n, 2)
        style = random.random()
        f = factor(n)
        big = [q for q in f if q >= 5]
        while True:
            if style < 0.25:
                B = [random.randrange(n) for _ in range(m)]
            elif style < 0.5:    # few residues modulo 2^k
                u = random.sample(range(2 ** k), min(2 ** k, random.randint(1, 3)))
                B = [(random.choice(u) + 2 ** k * random.randrange(n // 2 ** k)) % n for _ in range(m)]
                B = [b if b % 2 ** k in u else u[0] for b in B]
            elif style < 0.75:   # closed under +n/2
                h = [random.randrange(n) for _ in range((m + 1) // 2)]
                B = h + [(x + n // 2) % n for x in h]
            else:                # unions of cosets of small subgroups
                B = []
                while len(B) < m:
                    p = random.choice(list(f))
                    x = random.randrange(n)
                    B += [(x + t * (n // p)) % n for t in range(p)]
            if big:
                # force: at most four residues modulo q^a for every prime q >= 5 (then no level of q is live)
                for q in big:
                    qa = q ** f[q]
                    allowed = random.sample(range(qa), min(4, qa))
                    # change the residue modulo q^a of each element to an allowed one (CRT)
                    rest = n // qa
                    inv = pow(rest, -1, qa)
                    B = [(b + rest * ((random.choice(allowed) - b) * inv % qa)) % n if b % qa not in allowed else b for b in B]
            if not is_exceptional(B, n):
                return B
    for n in (12, 24, 48, 96, 192, 384, 72, 144, 432, 1296, 2592, 20, 40, 100, 200, 60, 120, 240, 600, 420, 840, 1400, 4200, 9240, 4900):
        stats = {'tested': 0, 'fail': 0, 'examples': []}
        big = [q for q in factor(n) if q >= 5]
        batchsize = {}
        for _ in range(1500):
            m = random.randint(3, 40)
            B = gen(n, m)
            assert no_live_big(B, n)
            run_batch(n, [tuple(B)], stats)
        print(f"n = {n}: {stats['tested']} random and structured multisets of 3 to about 42 elements"
              + (", at most four residues modulo q^a for each prime q >= 5" if big else "") + f": failures {stats['fail']} {stats['examples']}", flush=True)

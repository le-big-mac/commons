# Theorem A (n = 2^k): the construction, written from the proof in even-result.md section 2 (not from prover/pow2.py),
# and a brute force of the "iff" that does not use the construction.
# Goodness on Z_{2^k} is decided here by folding: S mod (X^(2^(j-1)) + 1) for j = 1..k, and S(1) for j = 0;
# for a sample it is compared with the general remainder test of rlib.
import sys, random, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import bad_one, v2

def good_pow2(B, signs, k):
    if sum(signs) == 0:
        return False
    for j in range(1, k + 1):
        h = 1 << (j - 1)
        c = [0] * h
        for x, s in zip(B, signs):
            r = x % (2 * h)
            if r < h:
                c[r] += s
            else:
                c[r - h] -= s
        if not any(c):
            return False
    return True

def exceptional(M, N):
    return len(M) == 2 and (M[0] - M[1]) % N != 0

def construct(B, k, pick=0):
    """signs for the multiset B (list of residues mod 2^k), B nonempty and not an exceptional pair.
    pick = 0: A is the half E when E is not an exceptional pair, else D;  pick = 1: the other preference
    (the proof says 'one of E, D that is not an exceptional pair': either must work)."""
    m = len(B)
    n = 1 << k
    assert m >= 1 and not exceptional(B, n)
    if k == 0:
        return [1] * m
    N = n // 2
    Ei = [i for i in range(m) if B[i] % 2 == 0]
    Di = [i for i in range(m) if B[i] % 2 == 1]
    E = [(B[i] % n) // 2 for i in Ei]
    D = [((B[i] % n) - 1) // 2 for i in Di]
    signs = [None] * m
    def put(idx, s):
        for i, v in zip(idx, s):
            signs[i] = v
    if not D or not E:                         # one half empty
        idx, H = (Ei, E) if E else (Di, D)
        assert not exceptional(H, N)           # "E is an exceptional pair on Z_N iff B is one on Z_n"
        put(idx, construct(H, k - 1, pick))
    elif exceptional(E, N) and exceptional(D, N):
        vE = v2((E[0] - E[1]) % N)
        vD = v2((D[0] - D[1]) % N)
        assert vE < k - 1 and vD < k - 1
        if vD >= vE:
            put(Ei, [1, -1]); put(Di, [1, 1])
        else:
            put(Ei, [1, 1]); put(Di, [1, -1])
    else:
        cands = [(Ei, E, Di, D), (Di, D, Ei, E)]
        cands = [c for c in cands if not exceptional(c[1], N)]
        Ai, A, Ci, C = cands[pick % len(cands)]
        if len(C) >= 2:
            sA = construct(A, k - 1, pick)
            sig = sum(sA)
            assert sig != 0
            if len(C) != abs(sig):
                sC = [1] * len(C)
            else:
                sC = [-1] + [1] * (len(C) - 1)
                assert len(C) - 2 != abs(sig)
        elif len(A) % 2 == 0:
            sA = construct(A, k - 1, pick)
            sC = [1]
        else:
            assert len(A) >= 3                 # |A| = 1 would make B an exceptional pair
            sA = [1] * len(A)
            sC = [1]
        put(Ai, sA); put(Ci, sC)
    return signs

random.seed(5)
# 0. the folding test against the general remainder test
cmp_ = 0
for _ in range(3000):
    k = random.randint(0, 5); n = 1 << k
    m = random.randint(1, 7)
    B = [random.randrange(n) for _ in range(m)]
    s = [random.choice([1, -1]) for _ in range(m)]
    g1 = good_pow2(B, s, k)
    g2 = not any(bad_one(B, s, n, 1 << j) for j in range(k + 1))
    assert g1 == g2
    cmp_ += 1
print("folding test = remainder test on", cmp_, "signed multisets")

# 1. every nonempty subset of Z_2, Z_4, Z_8, Z_16: construction (both preferences) and brute force of pairs
for k in range(0, 5):
    n = 1 << k
    tot = pairs = 0
    for mask in range(1, 1 << n):
        B = [x for x in range(n) if mask >> x & 1]
        if exceptional(B, n):
            pairs += 1
            assert not good_pow2(B, [1, 1], k) and not good_pow2(B, [1, -1], k)
            continue
        for pick in (0, 1):
            s = construct(B, k, pick)
            assert good_pow2(B, s, k), (n, B, s)
        tot += 1
    print("Z_%d: construction good on all %d nonempty subsets that are not pairs; %d pairs have no good signing" % (n, tot, pairs))

# 2. every multiset with at most M elements (repetitions allowed), all of them (not only those containing 0)
for k, M in [(1, 14), (2, 10), (3, 7), (4, 5), (5, 4)]:
    n = 1 << k
    tot = pairs = 0
    for m in range(1, M + 1):
        for B in itertools.combinations_with_replacement(range(n), m):
            B = list(B)
            if exceptional(B, n):
                pairs += 1
                assert not good_pow2(B, [1, 1], k) and not good_pow2(B, [1, -1], k)
                continue
            for pick in (0, 1):
                s = construct(B, k, pick)
                assert good_pow2(B, s, k), (n, B, s)
            tot += 1
    print("Z_%d: every multiset of 1..%d elements: %d constructed and good; %d exceptional pairs, none with a good signing" % (n, M, tot, pairs))

# 3. brute force of the statement itself, without the construction: a good signing exists iff not an exceptional pair
for k, M in [(1, 10), (2, 8), (3, 6), (4, 5)]:
    n = 1 << k
    tot = 0
    for m in range(1, M + 1):
        for B in itertools.combinations_with_replacement(range(n), m):
            ex = any(good_pow2(B, (1,) + s, k) for s in itertools.product([1, -1], repeat=m - 1))
            assert ex == (not exceptional(B, n)), (n, B)
            tot += 1
    print("Z_%d: brute force over all signings, every multiset of 1..%d elements (%d): good signing exists iff not an exceptional pair" % (n, M, tot))

# 4. random and structured, larger
def shapes(n, m):
    t = random.random()
    if t < 0.25:
        return [random.randrange(n) for _ in range(m)]                        # multiset
    if t < 0.45:
        return random.sample(range(n), min(m, n))                              # set
    if t < 0.65:                                                               # closed under x -> x + n/2
        h = [random.randrange(n // 2) for _ in range(max(1, m // 2))]
        return h + [x + n // 2 for x in h]
    if t < 0.85:                                                               # union of cosets of a subgroup
        g = random.choice([d for d in range(1, n) if n % d == 0])
        reps = random.sample(range(g), min(g, max(1, m * g // n + random.randint(0, 2))))
        return [r + g * t_ for r in reps for t_ in range(n // g)][: max(m, n // g)]
    # all elements in one deep class, plus a few
    j = random.randint(1, n.bit_length() - 1)
    c = random.randrange(1 << j)
    return [(c + (1 << j) * random.randrange(n >> j)) % n for _ in range(m)] + [random.randrange(n) for _ in range(random.randint(0, 2))]

cnt = 0
for k in range(5, 13):
    n = 1 << k
    for _ in range(1500):
        m = random.randint(1, 80)
        B = shapes(n, m)
        if exceptional(B, n):
            continue
        s = construct(B, k, random.randint(0, 1))
        assert good_pow2(B, s, k), (n, B)
        cnt += 1
print("random and structured on Z_32..Z_4096, up to about 80 elements (more for cosets):", cnt, "constructed, all good")
# small sizes at random on large n (the pair-like cases)
cnt = 0
for _ in range(40000):
    k = random.randint(1, 12); n = 1 << k
    m = random.randint(1, 6)
    B = [random.randrange(n) for _ in range(m)]
    if random.random() < 0.5:   # make halves that are pairs
        B = [2 * random.randrange(n // 2) for _ in range(2)] + [2 * random.randrange(n // 2) + 1 for _ in range(random.randint(0, 3))]
    if exceptional(B, n):
        continue
    s = construct(B, k, random.randint(0, 1))
    assert good_pow2(B, s, k), (n, B)
    cnt += 1
print("small multisets (1..6 elements, half of them with an even half that is a pair) on Z_2..Z_4096:", cnt, "all good")
print("OK")

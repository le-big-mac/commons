# Lemma V, Lemma Q and part (3) of Proposition P, tested from the statements on an odd modulus n'
# (only the residues modulo n' enter).  D_e is computed from its definition: the F_2-rank of the vectors
# Y^w mod (2, Phi_e), w in the support.  Nothing here needs signings.
#   V : p^i || e, level i of p live and the l-th live level of p  =>  D_e >= l (p - 1);
#       and the finer inequality of the proof: D_e >= sum over the occupied groups at level i of min(|L|, p - 1).
#   P3: on the live e the map e -> e* = prod p^(l_p(e)) is injective and mu(e*) <= D_e.
#   Q : m odd, p^i dangerous and the l-th dangerous among p, ..., p^i  =>  level i live, D_{p^i} >= (p-1) p^(l-1);
#       also: dangerous iff every class at depth i-1 has all its p children of its own parity; o_j as in the proof.
# usage: tVQ.py seed count
import sys, random, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

st = dict(cases=0, V=0, V_tight=0, fine=0, fine_tight=0, P3=0, Q=0, Q_tight=0, Qchar=0, live_e=0, maxl={})

def mu(e):
    return max((v * (p - 1) for p, v in factorint(e).items()), default=0)

def check(F_, npr):
    """F_: list of residues mod n' (a multiset)."""
    st['cases'] += 1
    W = sorted(set(F_))
    fac = factorint(npr)
    lv = {p: live_levels(W, p, a) for p, a in fac.items()}
    estar_seen = {}
    for e in divisors(npr):
        if e == 1:
            continue
        De = D_rank(W, e)
        fe = factorint(e)
        is_live = True
        for p, i in fe.items():
            # the finer inequality: groups at level i = classes modulo p^(i-1), subclasses modulo p^i
            groups = {}
            for w in W:
                groups.setdefault(w % p ** (i - 1), set()).add(w % p ** i)
            fine = sum(min(len(L), p - 1) for L in groups.values())
            assert De >= fine, ("Lemma V fine", npr, W, e, p, De, fine)
            st['fine'] += 1
            st['fine_tight'] += (De == fine)
            if i in lv[p]:
                l = sum(1 for j in lv[p] if j <= i)
                assert De >= l * (p - 1), ("Lemma V", npr, W, e, p, De, l)
                st['V'] += 1
                st['V_tight'] += (De == l * (p - 1))
                st['maxl'][p] = max(st['maxl'].get(p, 0), l)
            else:
                is_live = False
        if is_live:
            st['live_e'] += 1
            es = 1
            for p, i in fe.items():
                es *= p ** sum(1 for j in lv[p] if j <= i)
            assert es not in estar_seen, ("e* not injective", npr, W, e, estar_seen[es])
            estar_seen[es] = e
            assert mu(es) <= De, ("mu(e*) > D_e", npr, W, e, es, De)
            st['P3'] += 1
    if len(F_) % 2 == 1:
        for p, a in fac.items():
            l = 0
            o_prev = 1
            for i in range(1, a + 1):
                q = p ** i
                pw = powers_mod2(q)
                s = 0
                for w in F_:
                    s ^= pw[w % q]
                dangerous = (s == 0)
                # characterisation by parities
                par_child = {}
                for w in F_:
                    par_child[w % q] = par_child.get(w % q, 0) ^ 1
                par_parent = {}
                for w in F_:
                    par_parent[w % (q // p)] = par_parent.get(w % (q // p), 0) ^ 1
                char = all(par_child.get(c + t * (q // p), 0) == par_parent.get(c, 0) for c in range(q // p) for t in range(p))
                assert dangerous == char, ("Lemma Q characterisation", npr, F_, p, i)
                st['Qchar'] += 1
                o_now = sum(par_child.values())
                assert o_now >= o_prev
                if dangerous:
                    assert o_now == p * o_prev
                    l += 1
                    assert i in lv[p], ("Lemma Q: dangerous but not live", npr, F_, p, i)
                    Dq = D_rank(W, q)
                    assert o_prev >= p ** (l - 1)
                    assert Dq >= (p - 1) * o_prev >= (p - 1) * p ** (l - 1), ("Lemma Q", npr, F_, p, i, Dq, l)
                    st['Q'] += 1
                    st['Q_tight'] += (Dq == (p - 1) * p ** (l - 1))
                o_prev = o_now

def gen_dangerous_tree(p, a, rnd, levels=None):
    """a multiset on Z_{p^a} with an odd number of elements whose dangerous levels include the given ones"""
    if levels is None:
        levels = [i for i in range(1, a + 1) if rnd.random() < 0.6]
    par = {0: 1}            # parities of the classes at depth 0
    for i in range(1, a + 1):
        new = {}
        q = p ** (i - 1)
        for c, b in par.items():
            if i in levels:
                ch = [b] * p
            else:
                ch = [rnd.randint(0, 1) for _ in range(p)]
                if sum(ch) % 2 != b:
                    ch[rnd.randrange(p)] ^= 1
            for t in range(p):
                if ch[t] or rnd.random() < 0.15:
                    new[c + t * q] = ch[t]
        par = new
    out = []
    for c, b in par.items():
        out += [c] * (1 if b else rnd.choice([0, 0, 2]))
    return out

def crt(res, mods):
    N = 1
    for m_ in mods:
        N *= m_
    for x in range(N):
        if all(x % m_ == r % m_ for r, m_ in zip(res, mods)):
            return x

def gen(npr, rnd):
    t = rnd.random()
    fac = factorint(npr)
    if t < 0.25:
        return [rnd.randrange(npr) for _ in range(rnd.randint(1, 40))]
    if t < 0.45:      # union of cosets
        g = rnd.choice([d for d in divisors(npr) if d > 1])
        reps = [rnd.randrange(npr) for _ in range(rnd.randint(1, 4))]
        B = [(r + (npr // g) * i) % npr for r in reps for i in range(g)]
        B += [rnd.randrange(npr) for _ in range(rnd.randint(0, 3))]
        return B
    if t < 0.60:      # an interval
        s = rnd.randrange(npr)
        return [(s + i) % npr for i in range(rnd.randint(1, min(npr, 60)))]
    if t < 0.85:      # product of dangerous trees (odd sizes), cut if too large
        parts = [gen_dangerous_tree(p, a, rnd) for p, a in fac.items()]
        mods = [p ** a for p, a in fac.items()]
        size = 1
        for P_ in parts:
            size *= max(1, len(P_))
        if size > 400 or any(len(P_) == 0 for P_ in parts):
            parts = [gen_dangerous_tree(p, a, rnd, levels=[1]) if rnd.random() < 0.5 else [rnd.randrange(p ** a)] for p, a in fac.items()]
        table_ = {}
        out = []
        for combo in itertools.product(*parts):
            key = tuple(c % m_ for c, m_ in zip(combo, mods))
            if key not in table_:
                table_[key] = crt(combo, mods)
            out.append(table_[key])
        return out
    # caterpillar: many live levels for every prime
    B = [0]
    for p, a in fac.items():
        spine = 0
        for i in range(1, a + 1):
            if rnd.random() < 0.8:
                for tt in range(1, p):
                    x = spine + tt * p ** (i - 1) + p ** i * rnd.randrange(npr // p ** i if npr // p ** i else 1)
                    B.append((x * 1) % npr if len(fac) == 1 else rnd.choice([x % npr, (x + (p ** a) * rnd.randrange(npr // p ** a)) % npr]))
            spine += rnd.randrange(p) * p ** (i - 1)
    return B

seed, count = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(seed)
# exhaustive parts (only for seed 0)
if seed == 0:
    for npr, mults in [(3, 5), (9, 3), (15, 2), (5, 4), (7, 3), (21, 2)]:
        c0 = st['cases']
        if mults ** npr <= 2 * 10 ** 6:
            for vec in itertools.product(range(mults), repeat=npr):
                F_ = [x for x in range(npr) for _ in range(vec[x])]
                if F_:
                    check(F_, npr)
        print("exhaustive: every multiset on Z_%d with multiplicities < %d: %d cases" % (npr, mults, st['cases'] - c0), flush=True)
    c0 = st['cases']
    for mask in range(1, 1 << 15):
        check([x for x in range(15) if mask >> x & 1], 15)
    print("exhaustive: every nonempty subset of Z_15: %d" % (st['cases'] - c0))
mods = [9, 27, 81, 243, 25, 125, 49, 45, 135, 225, 675, 105, 315, 945, 1575, 63, 147, 75, 375, 165, 189, 405]
per = {}
for _ in range(count):
    npr = rnd.choice(mods)
    F_ = gen(npr, rnd)
    if not F_ or len(F_) > 500:
        continue
    check(F_, npr)
    per[npr] = per.get(npr, 0) + 1
print("random and structured (seed %d):" % seed, dict(sorted(per.items())))
print("cases %(cases)d.  Lemma V: %(V)d (e, p) with level v_p(e) live, D_e >= l(p-1) every time (equality %(V_tight)d times);"
      " finer inequality %(fine)d times (equality %(fine_tight)d).  P(3): %(P3)d live e, e* injective and mu(e*) <= D_e."
      "  Lemma Q: characterisation %(Qchar)d times; %(Q)d dangerous prime powers (odd m), all live, D >= (p-1)p^(l-1) (equality %(Q_tight)d)." % st)
print("largest l seen per prime:", dict(sorted(st['maxl'].items())))
print("OK")

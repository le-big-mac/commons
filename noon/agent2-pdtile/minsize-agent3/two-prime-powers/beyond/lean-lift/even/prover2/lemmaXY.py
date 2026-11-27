# Lemma X (i) for the prime p = 5 (and again p = 3, p = 7), and Lemma Y, on the supports of ranks2.gen and on random ones.
#  (X)  e = p^i * e2, p not dividing e2:  D_e(W) = sum over classes r mod p^(i-1) of [ sum_t dim V_{r,t} - dim of the common part ]
#  (Y)  W2 of odd size with pi_e(f) = 0, e > 1:  |W2| >= least prime factor of e
import sys, random
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from ranks import factor, powrem2, rank2
from ranks2 import gen, basis_of, intersect
from lib2 import divisors
rnd = random.Random(53)
for n1 in [15, 35, 45, 75, 105, 175, 225, 315, 385, 525, 1155]:
    f = factor(n1); nx = {p: 0 for p in f}; ny = 0
    for t in range(1200):
        if 3 in f and t % 2 == 0:
            W, W2 = gen(n1, (t // 2) % 4, rnd)
        else:
            W = sorted(set(rnd.randrange(n1) for _ in range(rnd.randint(3, 14))))
            if t % 4 == 1:    # a coset of prime order, perhaps two, plus a few points
                q = rnd.choice(sorted(f)); o = rnd.randrange(n1)
                W = sorted(set(W[:3]) | {(o + s * (n1 // q)) % n1 for s in range(q)})
            k = rnd.randrange(1, len(W) + 1, 2); W2 = rnd.sample(W, k)
            if t % 4 == 1 and len(W) % 2 == 1: W2 = list(W)
        for e in divisors(n1):
            if e == 1: continue
            pr = powrem2(e)
            s = 0
            for w in W2: s ^= pr[w % e]
            if s == 0:
                assert len(set(W2)) >= min(factor(e)), ('Y fails', W2, e); ny += 1
            D = rank2([pr[w % e] for w in set(x % e for x in W)])
            for p, a in factor(e).items():
                i = a; e2 = e // p ** i
                pr2 = powrem2(e2) if e2 > 1 else [1]
                K = (max(pr2).bit_length() + 1)
                cls = {}
                for w in W: cls.setdefault(w % p ** (i - 1), {}).setdefault(w % p ** i, []).append(pr2[w % e2])
                val = 0
                for r, ch in cls.items():
                    bs = [basis_of(v) for v in ch.values()]
                    val += sum(len(b) for b in bs)
                    if len(bs) == p:
                        cur = bs[0]
                        for b in bs[1:]: cur = intersect(cur, b, K)
                        val -= len(cur)
                assert val == D, ('X fails', W, e, p, val, D)
                nx[p] += 1
    print("n'", n1, 'supports 1200 | fibre formula checked, by prime:', nx, '| Lemma Y checked on', ny, 'dangerous (W2, e)', flush=True)

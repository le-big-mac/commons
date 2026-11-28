# Second look: my tests again with B_E(m) and PPE as the text now defines them (the convention of section 6:
# LC and Fb are 0 if N = k + p - 1 > m).  Everything else as in ref_test.analyse.  Also the quotients
# share/B(m) and share/B_E(m) kept apart for m >= 47.
import sys, math, random, time
from fractions import Fraction as Fr
import ref_bounds as rb
import ref_test as rt
import ref_shaped as rs
from ref_second import ConvCalc

base = rt.CALC
conv = ConvCalc(rt.CE, True)
class Proxy:
    def LC(self, m, N):          # Lemma C and Theorem 2 (sections 3 to 5): no convention there
        return base.LC(m, N)
    def PPE(self, m, p, j):      # section 6, with the convention
        return conv.PPE(m, p, j)
rt.CALC = Proxy()
_cache = {}
def Bm(m):
    if m not in _cache:
        b = rb.B(base, m, rt.CNT, True)
        be = sum(rb.BE_parts(conv, m, rt.CNT, True)) if m % 2 == 0 else None
        _cache[m] = (b, be)
    return _cache[m]
rt.Bm = Bm
BIG = {}
_an = rt.analyse
def analyse(n, mult, lemmas=True):
    s = _an(n, mult, lemmas)
    m = sum(mult.values())
    if m >= 47:
        b, be = Bm(m)
        for name, bound in (("share/B(m), m >= 47, m %s" % ("odd" if m % 2 else "even"), b), ("share/B_E(m), m >= 47", be)):
            if bound is not None:
                q = float(s / bound)
                if name not in BIG or q > BIG[name][0]:
                    BIG[name] = (q, m, n)
        BIG["count m >= 47"] = (BIG.get("count m >= 47", (0,))[0] + 1,)
    return s
rt.analyse = analyse

if __name__ == "__main__":
    mode = sys.argv[1]
    t0 = time.time()
    if mode == "exh":
        budget = float(sys.argv[2])
        for a in sys.argv[3:]:
            n, mlo, mhi = (int(x) for x in a.split(":"))
            for m in range(mlo, mhi + 1):
                if time.time() - t0 > budget:
                    break
                b, done = rt.exhaustive(n, m, budget, t0)
                print("Z_%d, every multiset of %d elements containing 0: largest share %s, complete: %s, multisets so far %d, failures %d"
                      % (n, m, b, done, rt.ST["multisets"], rt.ST["failures"]), flush=True)
    else:
        for seed, budget in ((11, float(sys.argv[2])), (23, float(sys.argv[3]))):
            rnd = random.Random(seed)
            t1 = time.time()
            while time.time() - t1 < budget:
                n, mult = rs.gen(rnd)
                m = sum(mult.values())
                if rs.kprod(mult) * rs.phi(n) > 2.5e7 or m > 120 or m < 3:
                    continue
                analyse(n, mult)
            print("shaped, seed %d: multisets so far %d, failures %d" % (seed, rt.ST["multisets"], rt.ST["failures"]), flush=True)
        rnd = random.Random(5)
        t1 = time.time()
        mods = [9, 15, 21, 27, 45, 63, 75, 81, 105, 135, 225, 315, 945, 1155]
        while time.time() - t1 < float(sys.argv[4]):
            n = rnd.choice(mods)
            m = rnd.randint(4, 16)
            mult = {}
            kind = rnd.randint(0, 2)
            if kind == 0:
                for _ in range(m):
                    b = rnd.randrange(n); mult[b] = mult.get(b, 0) + 1
            elif kind == 1:
                for _ in range(m // 2):
                    b = rnd.randrange(n); mult[b] = mult.get(b, 0) + 2
            else:
                rsd = rnd.sample(range(n), rnd.randint(2, 5))
                for _ in range(m):
                    b = rnd.choice(rsd); mult[b] = mult.get(b, 0) + 1
            if not mult:
                continue
            analyse(n, mult)
        print("random (4 to 16 elements; plain, all in pairs, few residues), seed 5: multisets so far %d, failures %d" % (rt.ST["multisets"], rt.ST["failures"]), flush=True)
    rt.report()
    for k_ in sorted(BIG):
        print("  ", k_, BIG[k_])
    # largest share/B_E by m for small even m

"""Referee, second reading: the Appendix (Lemma T and the Claim), tested with exact integer arithmetic.

usage: ref_appendix.py lemmaT seed
       ref_appendix.py exhaustive                 the Claim on every weight vector of small groups
       ref_appendix.py random seed                the Claim on structured random multisets in larger groups

Division side: Phi_d from sympy (not from pat.py); X^x mod Phi_d by repeated multiplication by X and reduction by the
monic Phi_d (Python integers); A(X) mod Phi_d = sum_x A(x) (X^x mod Phi_d).  A sample is also divided with
pat.exact_pattern_division.  Tree side: my literal patterns from section 1; x in Z_M is (x mod p^n, x mod q).
"""
import sys, random, itertools, time
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols, divisors, primefactors
from ref_common import literal_patterns, bits_to_set
sys.path.insert(0, "/home/agent3/minsize/prove")
import pat as PAT

_X = symbols("X")
_phi = {}


def phi(d):
    if d not in _phi:
        _phi[d] = [int(c) for c in Poly(cyclotomic_poly(d, _X), _X).all_coeffs()[::-1]]     # lowest degree first, monic
    return _phi[d]


_rm = {}


def rem_matrix(d, M):
    """R (M, deg): row x = coefficients of X^x mod Phi_d"""
    if (d, M) in _rm:
        return _rm[(d, M)]
    ph = np.array(phi(d), dtype=object)
    deg = len(ph) - 1
    R = np.zeros((M, deg), dtype=object)
    r = np.zeros(deg, dtype=object)
    r[0] = 1
    if deg == 0:
        raise ValueError
    for x in range(M):
        R[x] = r
        top = r[deg - 1]
        r = np.concatenate([[0], r[:-1]])
        if top:
            r = r - top * ph[:deg]
    assert max(abs(int(v)) for v in R.ravel()) < 10 ** 6
    R = R.astype(np.int64)
    _rm[(d, M)] = R
    return R


def lemmaT(seed):
    rng = random.Random(seed)
    nB = nid_bad = niff_bad = ndiv = nnot = nsets = 0
    ctrl_sets = ctrl_broken = 0
    for N in list(range(2, 41)) + [45, 48, 49, 50, 54, 56, 60, 63, 64, 72, 75, 81, 90, 96, 98, 100, 105, 108, 120]:
        proper = [d for d in divisors(N) if d < N]
        maxi = [N // s for s in primefactors(N)]
        sets = [list(maxi), list(proper)]
        for _ in range(3):
            extra = [d for d in proper if d not in maxi and rng.random() < 0.4]
            s = maxi + extra
            rng.shuffle(s)
            sets.append(s)
        R = rem_matrix(N, N)
        ph = phi(N)
        deg = len(ph) - 1
        for rs in sets:
            nsets += 1
            for trial in range(40):
                kind = trial % 4
                if kind == 0:
                    B = [rng.randint(-3, 3) for _ in range(N)]
                elif kind == 1:                       # Phi_N times a random polynomial, degree < N
                    Q = [rng.randint(-2, 2) for _ in range(N - deg)]
                    B = [0] * N
                    for i, a in enumerate(ph):
                        for j, b in enumerate(Q):
                            B[i + j] += a * b
                elif kind == 2:                       # sums of cosets of subgroups of prime order (nonnegative)
                    B = [0] * N
                    for _k in range(rng.randint(1, 4)):
                        s = rng.choice(primefactors(N))
                        t = rng.randrange(N)
                        m = rng.randint(1, 3)
                        for i in range(s):
                            B[(t + i * (N // s)) % N] += m
                else:                                  # the same with one coefficient changed
                    B = [0] * N
                    for _k in range(rng.randint(1, 3)):
                        s = rng.choice(primefactors(N))
                        t = rng.randrange(N)
                        for i in range(s):
                            B[(t + i * (N // s)) % N] += 1
                    B[rng.randrange(N)] += 1
                nB += 1
                Bv = np.array(B, dtype=np.int64)
                nab = Bv.copy()
                for r in rs:
                    nab = nab - np.roll(nab, r)                      # (nabla_r B)(y) = B(y) - B(y - r)
                # C(X) = prod (X^r - 1) B(X), reduced mod X^N - 1
                C = [int(v) for v in B]
                for r in rs:
                    C2 = [0] * (len(C) + r)
                    for i, c in enumerate(C):
                        C2[i + r] += c
                        C2[i] -= c
                    C = C2
                red = [0] * N
                for i, c in enumerate(C):
                    red[i % N] += c
                sign = (-1) ** len(rs)
                if any(red[y] != sign * int(nab[y]) for y in range(N)):
                    nid_bad += 1
                divisible = not (Bv @ R).any()
                ndiv += divisible
                nnot += not divisible
                if divisible != (not nab.any()):
                    niff_bad += 1
        # control: drop one maximal divisor (when there are two or more): "Phi_N | B => nabla = 0" must be able to fail
        if len(maxi) >= 2:
            rs = maxi[1:]
            ctrl_sets += 1
            broken = False
            for trial in range(20):
                Q = [rng.randint(-2, 2) for _ in range(N - deg)]
                B = [0] * N
                for i, a in enumerate(ph):
                    for j, b in enumerate(Q):
                        B[i + j] += a * b
                nab = np.array(B, dtype=np.int64)
                for r in rs:
                    nab = nab - np.roll(nab, r)
                if nab.any():
                    broken = True
            ctrl_broken += broken
    print(f"Lemma T: {nsets} pairs (N, set of r's), {nB} functions B ({ndiv} with Phi_N | B, {nnot} without); "
          f"identity C(X) = (-1)^m sum nabla..B X^y mod X^N - 1 wrong in {nid_bad}; 'Phi_N | B iff nabla = 0' wrong in {niff_bad}; "
          f"control (one maximal proper divisor left out): the equivalence breaks for {ctrl_broken} of {ctrl_sets} values of N")


def crt_index(p, q, n):
    pn = p ** n
    M = pn * q
    idx = np.zeros((pn, q), dtype=np.int64)
    for x in range(M):
        idx[x % pn, x % q] = x
    return idx


def compare(p, q, n, W, tally, sample_pat=0, rng=None):
    """W (K, M) weights on Z_M.  Tree pattern against exact division, per multiset."""
    pn = p ** n
    M = pn * q
    idx = crt_index(p, q, n)
    Wt = W[:, idx.ravel()].reshape(len(W), pn, q)
    r = literal_patterns(p, q, n, Wt)[0]
    Eb, Fb, bal = r["E"][:, 0], r["F"][:, 0], r["bal"][:, 0]
    W64 = W.astype(np.int64)
    bad = np.zeros(len(W), dtype=bool)
    for a in range(1, n + 1):
        divE = ~(W64 @ rem_matrix(p ** a, M)).any(axis=1)
        divF = ~(W64 @ rem_matrix(p ** a * q, M)).any(axis=1)
        treeE = ((Eb >> (a - 1)) & 1).astype(bool)
        treeF = ((Fb >> (a - 1)) & 1).astype(bool)
        bad |= (divE != treeE) | (divF != treeF)
        tally["E true"] += int(treeE.sum()); tally["E false"] += int((~treeE).sum())
        tally["F true"] += int(treeF.sum()); tally["F false"] += int((~treeF).sum())
    div0 = ~(W64 @ rem_matrix(q, M)).any(axis=1)
    bad |= div0 != bal
    tally["bal true"] += int(bal.sum()); tally["bal false"] += int((~bal).sum())
    tally["multisets"] += len(W)
    tally["bad"] += int(bad.sum())
    if sample_pat and rng is not None:
        for k in rng.sample(range(len(W)), min(sample_pat, len(W))):
            Ed, Fd = PAT.exact_pattern_division(p, q, n, [int(v) for v in W[k]])
            Em = bits_to_set(Eb[k])
            Fm = bits_to_set(Fb[k]) | ({0} if bal[k] else set())
            tally["pat.py sample"] += 1
            tally["pat.py bad"] += (set(Ed) != Em or set(Fd) != Fm)


def new_tally():
    return {k: 0 for k in ("multisets", "bad", "E true", "E false", "F true", "F false", "bal true", "bal false", "pat.py sample", "pat.py bad")}


def exhaustive():
    rng = random.Random(1)
    for (p, q, n, wmax) in ((2, 3, 1, 4), (3, 2, 1, 4), (2, 5, 1, 2), (5, 2, 1, 2), (3, 5, 1, 1), (5, 3, 1, 1), (2, 7, 1, 1), (7, 2, 1, 1),
                            (2, 3, 2, 2), (3, 2, 2, 1), (2, 5, 2, 1), (2, 3, 3, 1)):
        M = p ** n * q
        t0 = time.time()
        tally = new_tally()
        K = (wmax + 1) ** M
        step = 1 << 19
        for s in range(0, K, step):
            ks = np.arange(s, min(K, s + step), dtype=np.int64)
            W = np.empty((len(ks), M), dtype=np.int8)
            rem = ks.copy()
            for x in range(M):
                W[:, x] = rem % (wmax + 1)
                rem //= (wmax + 1)
            compare(p, q, n, W, tally, sample_pat=3, rng=rng)
        print(f"Claim, exhaustive: Z_{M} (p={p}, q={q}, n={n}), all {K} weight vectors with weights 0..{wmax}: disagreements {tally['bad']}; "
              f"level conditions true/false: E {tally['E true']}/{tally['E false']}, F {tally['F true']}/{tally['F false']}, balanced {tally['bal true']}/{tally['bal false']}; "
              f"pat.py sample {tally['pat.py sample']}, disagreements {tally['pat.py bad']}  [{time.time() - t0:.0f} s]", flush=True)


def structured(p, q, n, K, rng):
    """random sums of blocks m . (D x layers), D = strings with prescribed digits off a set T, T near a common T0"""
    pn = p ** n
    M = pn * q
    u = np.arange(pn)
    idx = crt_index(p, q, n)
    W = np.zeros((K, M), dtype=np.int64)
    for k in range(K):
        T0 = {a for a in range(1, n + 1) if rng.random() < 0.5}
        A = np.zeros((pn, q), dtype=np.int64)
        for _b in range(rng.choice((1, 1, 2, 2, 3, 4))):
            T = set(T0)
            if rng.random() < 0.4:
                T ^= {rng.randrange(1, n + 1)}
            m = np.ones(pn, dtype=bool)
            for a in range(1, n + 1):
                if a not in T:
                    m &= ((u // p ** (a - 1)) % p) == (0 if rng.random() < 0.75 else rng.randrange(p))
            lay = rng.random()
            mult = rng.choice((1, 1, 1, 2, p))
            if lay < 0.45:
                A[m, :] += mult
            elif lay < 0.85:
                A[m, rng.randrange(q)] += mult
            else:
                w = rng.randrange(q)
                A[m, :] += mult
                A[m, w] -= mult
        if rng.random() < 0.1:
            A[rng.randrange(pn), rng.randrange(q)] += 1
        # place A(u, w) at x = idx[u, w]
        W[k, idx.ravel()] = A.ravel()
    return W


def randomrun(seed):
    rng = random.Random(seed)
    for (p, q, n, K) in ((2, 3, 3, 20000), (2, 3, 4, 20000), (2, 3, 5, 10000), (2, 3, 6, 4000), (3, 2, 3, 20000), (3, 2, 4, 6000), (3, 2, 5, 1000),
                         (2, 5, 3, 20000), (2, 5, 4, 8000), (5, 2, 2, 20000), (5, 2, 3, 3000), (3, 5, 2, 20000), (3, 5, 3, 4000),
                         (5, 3, 2, 10000), (5, 3, 3, 1500), (2, 7, 3, 10000), (7, 2, 2, 8000), (7, 2, 3, 600), (3, 7, 2, 8000), (7, 3, 2, 4000),
                         (2, 11, 3, 6000), (11, 2, 2, 3000), (5, 7, 2, 3000), (7, 5, 2, 2000), (2, 13, 4, 2000), (3, 11, 3, 1000)):
        t0 = time.time()
        M = p ** n * q
        tally = new_tally()
        step = max(1, 4000000 // M)
        done = 0
        while done < K:
            kk = min(step, K - done)
            W = structured(p, q, n, kk, rng)
            compare(p, q, n, W, tally, sample_pat=(2 if M <= 200 else 0), rng=rng)
            done += kk
        print(f"Claim, structured random: Z_{M} (p={p}, q={q}, n={n}): {tally['multisets']} multisets, disagreements {tally['bad']}; "
              f"level conditions true/false: E {tally['E true']}/{tally['E false']}, F {tally['F true']}/{tally['F false']}, balanced {tally['bal true']}/{tally['bal false']}; "
              f"pat.py sample {tally['pat.py sample']}, disagreements {tally['pat.py bad']}  [{time.time() - t0:.0f} s]", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "lemmaT":
        lemmaT(int(sys.argv[2]))
    elif sys.argv[1] == "exhaustive":
        exhaustive()
    else:
        randomrun(int(sys.argv[2]))

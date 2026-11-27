"""Test (mine, 27 Nov 2026) of "twice level 0", in the form used for the conjecture:
for a multiset B on Z_N, N = 2^k * n2 (n2 odd, prime to 3), and each e | n2:
    #{signings 3-bad at 2^j * e for some j = 0..k}  <=  2 * #{signings 3-bad at e}.
"3-bad at d": the remainder of the signed mask modulo Phi_d has all coefficients divisible by 3 (exact integers).
Also prints the largest ratio seen and, for the whole multiset, the share of signings 3-bad at no d | N.
usage: twice_test.py exhaust N MMAX SECONDS    every multiset containing 0 with 1..MMAX elements (until the time is up)
       twice_test.py random N COUNT MMIN MMAX SEED    random and structured multisets"""
import sys, itertools, random, time, importlib.util
from fractions import Fraction
import numpy as np
spec = importlib.util.spec_from_file_location('confirm', '/home/agent3/lean/lift-check/even/confirm.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
def allsigns(m): return np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64).reshape(-1, m)
_S = {}
def check(N, el, stats):
    m = len(el)
    if m not in _S: _S[m] = allsigns(m)
    S = _S[m]; R = C.rows(N); k2 = C.k2(N); n2 = N // k2
    notgood = np.zeros(len(S), bool)
    for e in C.divisors(n2):
        z = None; union = np.zeros(len(S), bool); c = 1
        while c <= k2:
            bad = ~np.any((S @ R[c * e][list(el)]) % 3, axis=1)
            if c == 1: z = int(bad.sum())
            union |= bad; c *= 2
        q = int(union.sum()); notgood |= union
        if q > 2 * z:
            print('FAILS:', N, el, 'e =', e, 'union', q, 'level 0', z, flush=True); stats['fail'] += 1
        if z: stats['maxratio'] = max(stats['maxratio'], Fraction(q, z))
        if q and not z: stats['fail'] += 1; print('FAILS (level 0 never bad but a level is):', N, el, e, flush=True)
    stats['n'] += 1
    share = Fraction(int((~notgood).sum()), len(S))
    key = m
    if key not in stats['minshare'] or share < stats['minshare'][key][0]: stats['minshare'][key] = (share, el)
mode = sys.argv[1]; stats = {'n': 0, 'fail': 0, 'maxratio': Fraction(0), 'minshare': {}}
if mode == 'exhaust':
    N, MMAX, secs = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]); t0 = time.time(); stopped = False
    for m in range(1, MMAX + 1):
        for rest in itertools.combinations_with_replacement(range(N), m - 1):
            if time.time() - t0 > secs: stopped = True; break
            check(N, (0,) + rest, stats)
        print(f'exhaust N={N} up to m={m}{" (STOPPED at the time limit, not all of this size)" if stopped else ""}: {stats["n"]} multisets, failures {stats["fail"]}, largest ratio {stats["maxratio"]}', flush=True)
        if stopped: break
else:
    N, count, mmin, mmax, seed = (int(x) for x in sys.argv[2:7]); rng = random.Random(seed); k2 = C.k2(N); n2 = N // k2
    for _ in range(count):
        m = rng.randint(mmin, mmax); fam = rng.choice(['random', 'fewres2', 'pairs', 'cosets', 'oddequal'])
        if fam == 'random': el = [rng.randrange(N) for _ in range(m)]
        elif fam == 'fewres2':            # few residues modulo the power of 2, spread modulo the odd part
            res = [rng.randrange(k2) for _ in range(rng.randint(2, 4))]; el = [(rng.choice(res) + k2 * rng.randrange(n2)) % N for _ in range(m)]
        elif fam == 'pairs':              # pairs congruent modulo the odd part (they differ by multiples of n2)
            el = []
            while len(el) < m:
                a = rng.randrange(N); el += [a, (a + n2 * rng.randrange(1, k2)) % N]
            el = el[:m]
        elif fam == 'cosets':             # a full set of residues modulo a prime of n2 inside one class of the 2-tree, plus others
            ps = [p for p in (5, 7, 11, 13) if n2 % p == 0]; p = rng.choice(ps) if ps else 1; a = rng.randrange(N)
            el = [(a + t * (N // p)) % N for t in range(p)] if p > 1 else []
            el = (el + [rng.randrange(N) for _ in range(m)])[:max(m, min(len(el), mmax))]
        else:                              # equal modulo the odd part: only the power of 2 tells them apart
            w = rng.randrange(n2); el = [next(x for x in range(rng.randrange(N), 10 * N) if x % n2 == w) % N for _ in range(m)]
        check(N, tuple(sorted(el)), stats)
    print(f'random N={N} seed={seed}: {stats["n"]} multisets of {mmin}..{mmax} elements, failures {stats["fail"]}, largest ratio {stats["maxratio"]}', flush=True)
for m in sorted(stats['minshare']):
    sh, el = stats['minshare'][m]; print(f'   m={m}: least share of signings 3-bad nowhere: {sh} = {float(sh):.4f} at {el}')

"""The confirming search for Conjecture E (written after expect-even.md was sealed; 27 November 2026).
For EVEN n: does every multiset of three or more elements have a signing whose signed mask is divisible by no Phi_d,
d | n?  Exact arithmetic modulo Phi_d, every signing (the first sign fixed: a signing and its negative fail together).
usage: confirm.py exhaust N MAXSIZE SECONDS     every multiset containing 0 with 3..MAXSIZE elements, until the time is up
       confirm.py families SEED COUNT NMAX       random and structured multisets of 3 to 14 elements, even n <= NMAX
       confirm.py control                        pairs on some groups: the program must find exactly the bad pairs"""
import sys, itertools, random, time
import numpy as np
from collections import Counter

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
_cyc = {}
def cyclo(d):
    if d in _cyc: return _cyc[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            den = cyclo(e); q = [0] * (len(num) - len(den) + 1); r = num[:]
            for k in range(len(q) - 1, -1, -1):
                c = r[k + len(den) - 1] // den[-1]; q[k] = c
                if c:
                    for j, a in enumerate(den): r[k + j] -= c * a
            assert not any(r); num = q
    _cyc[d] = num; return num
_rows = {}
def rows(n):
    """for each d | n: an array whose row x holds the coefficients of X^x modulo Phi_d, x < n"""
    if n in _rows: return _rows[n]
    _rows.clear(); out = {}
    for d in divisors(n):
        phi = np.array(cyclo(d)[:-1], dtype=np.int64); deg = len(phi)
        M = np.zeros((n, deg), dtype=np.int64); cur = np.zeros(deg, dtype=np.int64); cur[0] = 1
        for x in range(n):
            M[x] = cur
            top = cur[-1]; cur = np.roll(cur, 1); cur[0] = 0
            if top: cur -= top * phi
        out[d] = M
    _rows[n] = out; return out
_signs = {}
def signs(m):
    if m not in _signs:
        s = np.array(list(itertools.product((1, -1), repeat=m - 1)), dtype=np.int64).reshape(-1, m - 1)
        _signs[m] = np.hstack([np.ones((len(s), 1), dtype=np.int64), s])
    return _signs[m]
def has_good(n, e):
    R = rows(n); S = signs(len(e)); good = np.ones(len(S), bool); idx = [x % n for x in e]
    for d in sorted(R, key=lambda d: R[d].shape[1]):
        good &= np.any(S @ R[d][idx], axis=1)
        if not good.any(): return False
    return True
def k2(n):
    k = 1
    while n % (2 * k) == 0: k *= 2
    return k

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'control':
        for n in (2, 6, 12, 40, 56, 90, 96):
            bad = [b for b in range(n) if not has_good(n, [0, b])]
            want = [b for b in range(n) if b % k2(n)]
            print(f'control n={n}: pairs (0,b) without a good signing: {len(bad)}; the conjecture says {len(want)}; the same pairs: {bad == want}')
        sys.exit(0)
    if mode == 'exhaust':
        n, maxsize, secs = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]); t0 = time.time(); stopped = False
        for m in range(3, maxsize + 1):
            cnt = 0; bad = []
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                if time.time() - t0 > secs: stopped = True; break
                cnt += 1
                if not has_good(n, (0,) + rest): bad.append((0,) + rest)
            print(f'exhaust n={n} m={m}: {cnt} multisets containing 0{" (STOPPED at the time limit, not all)" if stopped else " (all)"}; without a good signing: {len(bad)} {bad[:5]}', flush=True)
            if stopped: break
        sys.exit(0)
    if mode == 'families':
        seed, count, nmax = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); rng = random.Random(seed)
        evens = [n for n in range(4, nmax + 1, 2)]
        stats = Counter(); bads = []
        def pick_n(need_div=None):
            while True:
                n = rng.choice(evens)
                if need_div is None or n % need_div == 0: return n
        for _ in range(count):
            fam = rng.choice(['random', 'cluster', 'progression', 'cosets', 'halfturn', 'repeats', 'twopower'])
            m = rng.randint(3, 14)
            if fam == 'random':
                n = pick_n(); e = [rng.randrange(n) for _ in range(m)]
            elif fam == 'cluster':
                n = pick_n(); g = rng.choice([d for d in divisors(n) if d > 1]); base = [rng.randrange(n) for _ in range(rng.randint(1, 3))]
                e = [(rng.choice(base) + g * rng.randrange(n // g)) % n for _ in range(m)]
            elif fam == 'progression':
                n = pick_n(); a, s = rng.randrange(n), rng.randrange(1, n); e = [(a + s * i) % n for i in range(m)]
            elif fam == 'cosets':
                h = rng.choice([2, 3, 4, 5, 6, 7]); r = rng.randint(1, max(1, 14 // h)); n = pick_n(h if h % 2 == 0 else 2 * h)
                reps = rng.sample(range(n // h), min(r, n // h)); e = [(a + j * (n // h)) % n for a in reps for j in range(h)]
                if len(e) < 3: e = e + [rng.randrange(n)]
            elif fam == 'halfturn':
                n = pick_n(); A = [rng.randrange(n) for _ in range(rng.randint(2, 7))]; e = A + [(a + n // 2) % n for a in A]
            elif fam == 'repeats':
                n = pick_n(); pool = [rng.randrange(n) for _ in range(rng.randint(1, 3))]; e = [rng.choice(pool) for _ in range(m)]
            else:                                              # elements differing by multiples of the odd part: only the power of 2 tells them apart
                n = pick_n(4); q = n // k2(n); e = [(rng.randrange(n) // q) * q % n for _ in range(m)]
                if rng.random() < 0.5: e = [(x + rng.choice([0, k2(n)]) * rng.randrange(q)) % n for x in e]
            stats[fam] += 1; stats['size %2d' % len(e)] += 1; stats['even size' if len(e) % 2 == 0 else 'odd size'] += 1
            if not has_good(n, e): bads.append((fam, n, sorted(e)))
        print(f'families seed={seed} count={count} nmax={nmax}:', dict(sorted(stats.items())))
        print(f'  without a good signing (three or more elements): {len(bads)}', bads[:10])

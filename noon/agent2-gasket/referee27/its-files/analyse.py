"""Referee's analysis of the count files written by ./gasket.
usage: analyse.py TAG N [dtype]   e.g. analyse.py 1e6 1000000"""
import sys, math
import numpy as np

QUADS = [(-3, 5, 8, 8), (-4, 5, 20, 21), (-1, 2, 2, 3), (0, 0, 1, 1), (-3, 4, 12, 13), (-2, 3, 6, 7), (-23, 48, 49, 52)]

def name(q):
    return '_'.join(str(x) for x in q)

def load(q, tag, dtype=np.uint32):
    return np.fromfile('out/g_%s_%s.bin' % (name(q), tag), dtype=dtype)

def residues(cnt):
    ks = np.nonzero(cnt)[0]
    res = sorted(set((ks % 24).tolist()))
    first = {r: int(ks[ks % 24 == r][0]) for r in res}
    return res, first

def admissible_mask(res, N):
    look = np.zeros(24, dtype=bool)
    look[sorted(res)] = True
    return np.tile(look, N // 24 + 1)[:N + 1]

def isqrt_ok(m):
    r = math.isqrt(m)
    return r * r == m

def form_values(f, p, N):
    out = []
    n = 1
    while f * n ** p <= N:
        out.append(f * n ** p)
        n += 1
    return out

def main():
    tag = sys.argv[1]; N = int(sys.argv[2])
    dtype = np.uint8 if len(sys.argv) > 3 and sys.argv[3] == 'u8' else np.uint32
    only = None
    if len(sys.argv) > 4:
        only = [tuple(int(x) for x in s.split(',')) for s in sys.argv[4:]]
    data = {}
    for q in QUADS:
        if only and q not in only: continue
        c = load(q, tag, dtype)
        assert len(c) == N + 1, (q, len(c))
        data[q] = c
    print('=== Q1 residues mod 24 (curvatures up to N=%d) ===' % N)
    RES = {}
    for q, c in data.items():
        res, first = residues(c)
        negres = [x % 24 for x in q if x < 0]
        full = sorted(set(res) | set(negres))
        RES[q] = set(full)
        print(q, 'residues of curvatures 0..N:', res, '(count %d)' % len(res), '| enclosing circle residue:', negres,
              '| distinct curvatures <=N: %d' % int((c > 0).sum()), '| first seen at:', first)
    print()
    print('=== Q3 forms f*n^2, n>=1, value <= N, residue admissible: present / absent ===')
    for q, c in data.items():
        row = []
        for f in (1, 2, 3, 6):
            vals = [v for v in form_values(f, 2, N) if v % 24 in RES[q]]
            allv = len(form_values(f, 2, N))
            pres = [v for v in vals if c[v] > 0]
            absn = [v for v in vals if c[v] == 0]
            row.append('%dn^2: of %d, admissible %d, present %d, absent %d' % (f, allv, len(vals), len(pres), len(absn)))
            if 0 < len(pres) <= 12 and len(absn) > 0:
                row.append('   (present ones: %s)' % pres)
            if 0 < len(absn) <= 12 and len(pres) > 0:
                row.append('   (absent ones: %s)' % absn)
        print(q, ' || '.join(row))
    print()
    print('=== Q3b forms f*n^4, n>=1 ===')
    for q in [(-23, 48, 49, 52), (0, 0, 1, 1)]:
        if q not in data: continue
        c = data[q]
        for f in (1, 4, 9, 36):
            vals = [v for v in form_values(f, 4, N) if v % 24 in RES[q]]
            allv = len(form_values(f, 4, N))
            pres = [v for v in vals if c[v] > 0]
            absn = [v for v in vals if c[v] == 0]
            print(q, '%dn^4: of %d values <=N, admissible %d, present %d, absent %d' % (f, allv, len(vals), len(pres), len(absn)),
                  '| present:', pres[:15], '| absent (first 8):', absn[:8])
    print()
    # all absent admissible numbers, classified, for every gasket (context for Q3/Q4)
    print('=== all admissible non-curvatures <= N, classified ===')
    for q, c in data.items():
        adm = admissible_mask(RES[q], N)
        miss = np.nonzero(adm & (c == 0))[0]
        miss = miss[miss > 0]
        cls = {'n^2': 0, '2n^2': 0, '3n^2': 0, '6n^2': 0, 'other': 0}
        other = []
        for m in miss.tolist():
            hit = False
            for f, nm in ((1, 'n^2'), (2, '2n^2'), (3, '3n^2'), (6, '6n^2')):
                if m % f == 0 and isqrt_ok(m // f):
                    cls[nm] += 1; hit = True
            if not hit:
                cls['other'] += 1; other.append(m)
        print(q, 'admissible numbers 1..N: %d; non-curvatures: %d;' % (int(adm[1:].sum()), len(miss)), cls,
              '| largest other:', other[-1] if other else None)
        dec = []
        d = 1
        while d < N:
            dec.append(sum(1 for m in other if d < m <= d * 10) + (1 if d == 1 and 1 in other else 0))
            d *= 10
        print('    "other" per decade (1-10, 10-100, ...):', dec)
        for f, nm in ((1, 'n^2'), (2, '2n^2'), (3, '3n^2'), (6, '6n^2')):
            ab = [m for m in miss.tolist() if m % f == 0 and isqrt_ok(m // f)]
            if ab:
                print('    largest absent %s: %d ; absent per decade: %s' % (nm, ab[-1],
                      [sum(1 for m in ab if (10 ** e < m <= 10 ** (e + 1)) or (e == 0 and m == 1)) for e in range(len(dec))]))
    print()
    q = (-3, 5, 8, 8)
    if q in data:
        c = data[q]
        print('=== Q4 (-3,5,8,8): admissible, absent, neither n^2 nor 6n^2, up to N ===')
        adm = admissible_mask(RES[q], N)
        miss = np.nonzero(adm & (c == 0))[0]
        miss = miss[miss > 0].tolist()
        spor = [m for m in miss if not isqrt_ok(m) and not (m % 6 == 0 and isqrt_ok(m // 6))]
        print('count', len(spor), 'largest', spor[-1] if spor else None)
        d = 1
        while d < N:
            lo, hi = d, d * 10
            print('  %d < k <= %d : %d' % (lo if lo > 1 else 0, hi, sum(1 for m in spor if (lo if lo > 1 else 0) < m <= hi)))
            d *= 10
        print('by residue mod 24:', {r: sum(1 for m in spor if m % 24 == r) for r in sorted(RES[q])})
        of2 = [m for m in spor if m % 2 == 0 and isqrt_ok(m // 2)]
        of3 = [m for m in spor if m % 3 == 0 and isqrt_ok(m // 3)]
        print('of these, of form 2n^2:', of2, ' of form 3n^2:', of3)
        if len(spor) <= 400:
            print('list:', spor)
        else:
            print('first 60:', spor[:60]); print('last 40:', spor[-40:])
        with open('out/sporadic_%s.txt' % tag, 'w') as fh:
            fh.write(' '.join(str(m) for m in spor) + '\n')
        nsq = [m for m in miss if isqrt_ok(m)]; n6 = [m for m in miss if m % 6 == 0 and isqrt_ok(m // 6)]
        print('absent admissible squares:', len(nsq), ' absent admissible 6n^2:', len(n6))
    print()
    if dtype == np.uint32:
        print('=== Q2 ===')
        q = (-4, 5, 20, 21)
        if q in data:
            c = data[q]
            print(q, 'circles of curvature 36:', int(c[36]))
            sq = [(n * n, int(c[n * n])) for n in range(1, math.isqrt(N) + 1) if c[n * n] > 0]
            print(q, 'square curvatures present: %d of %d squares <= N; smallest twelve (curvature, circles):' % (len(sq), math.isqrt(N)), sq[:12])
            print(q, 'squares absent (first 30):', [n * n for n in range(1, math.isqrt(N) + 1) if c[n * n] == 0][:30])
        q = (-3, 5, 8, 8)
        if q in data:
            c = data[q]
            print(q, 'circles of curvature 36:', int(c[36]))
            sq = [(n * n, int(c[n * n])) for n in range(1, math.isqrt(N) + 1) if c[n * n] > 0]
            print(q, 'square curvatures present up to N:', len(sq), sq[:12], 'out of', math.isqrt(N), 'squares; admissible squares:',
                  sum(1 for n in range(1, math.isqrt(N) + 1) if (n * n) % 24 in RES[q]))
        print()
        print('=== Q5 cumulative counts (enclosing circle included) ===')
        for q in [(-4, 5, 20, 21), (-3, 5, 8, 8)]:
            if q not in data: continue
            c = data[q].astype(np.int64)
            negc = sum(1 for x in q if x < 0)
            for T in (674.2, 788.5, 874.2, 1685.7):
                t = int(math.floor(T))
                tot = int(c[:t + 1].sum()) + negc
                sq = [(n * n, int(c[n * n])) for n in range(0, math.isqrt(t) + 1) if c[n * n] > 0]
                print(q, 'curvature <= %s: circles %d ; with square curvature %d : %s' % (T, tot, sum(x[1] for x in sq), sq))

if __name__ == '__main__':
    main()

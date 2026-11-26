#!/usr/bin/env python
"""Read inspi_ref_out.json (made by inspi_ref.py) and answer questions 3-6;
also set the program's findings beside the pencil formula of question 1."""
import json, math, sys
from collections import Counter, defaultdict


def pencil(inc, ang):
    g = math.gcd(inc, 360); q = 360 // g; p = inc // g
    T = q * ang + 180 * p * (q - 1)
    if T % 360 == 0:
        return q, None           # never home; loop of q steps, |D| = sqrt(q)
    r = 360 // math.gcd(T % 360, 360)
    return q, q * r


def main():
    d = json.load(open(sys.argv[1]))
    rows = d['rows']
    print('pairs', len(rows), 'tol', d['tol'], 'seconds', round(d['seconds'], 1))
    home = [r for r in rows if r['home']]
    never = [r for r in rows if not r['home']]
    print('Q3 never home:', len(never), ' come home:', len(home))
    incs = sorted(set(r['inc'] for r in never))
    print('Q3 INC with never-home ANGLEs:', len(incs), 'values; all even:',
          all(i % 2 == 0 for i in incs), '; every even INC present:',
          incs == list(range(2, 360, 2)))
    per_inc = Counter(r['inc'] for r in never)
    ok = all(per_inc[i] == 360 // math.gcd(i, 360) for i in incs)
    print('   number of never-home ANGLEs for each such INC equals 360/gcd(INC,360):', ok)
    print('   sum over even INC of 360/gcd:', sum(360 // math.gcd(i, 360) for i in range(2, 360, 2)))
    mx = max(r['n0'] for r in home)
    print('Q3 largest number of steps to come home:', mx, ' pairs with it:',
          sum(1 for r in home if r['n0'] == mx))
    print('   histogram of steps to home:', sorted(Counter(r['n0'] for r in home).items()))
    print('   largest |D| counted as zero:', max(r['absD'] for r in home))
    print('   smallest |D| counted as not zero:', min(r['absD'] for r in never))
    # pencil check
    bad = 0; maxdev = 0.0
    for r in rows:
        q, n = pencil(r['inc'], r['ang'])
        if n is None:
            if r['home'] or r['n0'] != q:
                bad += 1
            else:
                maxdev = max(maxdev, abs(r['absD'] - math.sqrt(q)))
        else:
            if (not r['home']) or r['n0'] != n:
                bad += 1
    print('Q1 check: pairs where program disagrees with pencil formula:', bad,
          '; max | |D| - sqrt(q) | over never-home pairs:', maxdev)
    # Q4
    print('Q4 diameters measured for', sum(1 for r in home if 'diam' in r), 'home-coming pairs',
          '; hull-vs-brute checks:', d['brute_checks'], 'max diff', d['brute_maxdiff'])
    dmax = max(r['diam'] for r in home); dmin = min(r['diam'] for r in home)
    for name, val in (('widest', dmax), ('narrowest', dmin)):
        ties = [r for r in home if abs(r['diam'] - val) < 1e-7]
        print('Q4', name, repr(val), 'ties:', len(ties))
        byinc = defaultdict(list)
        for r in ties:
            byinc[r['inc']].append(r['ang'])
        for i in sorted(byinc):
            a = sorted(byinc[i])
            print('    INC', i, 'steps', sorted(set(r['n0'] for r in ties if r['inc'] == i)),
                  'ANGLE', a if len(a) <= 24 else (a[:12], '...', len(a), 'values'))
    ds = sorted(set(round(r['diam'], 7) for r in home))
    print('   distinct diameters (to 1e-7):', len(ds), ' five smallest:', ds[:5], ' five largest:', ds[-5:])
    # runner-up classes at both ends
    for name, vals in (('next widest', ds[-2:-1]), ('next narrowest', ds[1:2])):
        for v in vals:
            t = [(r['inc'], r['ang']) for r in home if abs(r['diam'] - v) < 1e-7]
            print('   ', name, v, len(t), 'pairs, e.g.', t[:6])
    # Q5
    vis = [r for r in never if r['early_start_visits'] > 0]
    print('Q5 never-home pairs that stand on the start again:', len(vis))
    m = min(never, key=lambda r: r['mindist'])
    close = sorted(never, key=lambda r: r['mindist'])
    print('Q5 closest approach among never-home pairs:', repr(m['mindist']))
    tie = [r for r in never if abs(r['mindist'] - m['mindist']) < 1e-9]
    print('   pairs with that closest approach:', len(tie))
    for r in tie[:40]:
        print('     INC', r['inc'], 'ANGLE', r['ang'], 'at step', r['mindist_step'],
              'heading then', r['mindist_heading'], 'loop', r['n0'], 'checked steps', r['checked_steps'])
    dv = sorted(set(round(r['mindist'], 9) for r in never))
    print('   five smallest distinct closest approaches:', dv[:5])
    # Q6
    print('Q6 hits (start point, first heading, different next turn):', len(d['q6_hits']), d['q6_hits'][:20])
    # extra: home-coming pairs that pass through the start before home
    hv = [r for r in home if r['early_start_visits'] > 0]
    print('extra: home-coming pairs that stand on the start (some other heading) before coming home:',
          len(hv), 'of', len(home), '; INC values involved:', len(set(r['inc'] for r in hv)))
    print('   examples:', [(r['inc'], r['ang'], r['n0'], r['early_start_visits']) for r in hv[:8]])
    # extra: classes under shift/mirror
    seen = set(); classes = 0
    for r in home:
        key = (r['inc'], r['ang'])
        if key in seen:
            continue
        classes += 1
        i, a = key
        q = 360 // math.gcd(i, 360)
        for j in range(q):
            for (ii, aa) in ((i, (a + j * i) % 360), (i, (-a + j * i) % 360),
                             ((-i) % 360, (-a + j * i) % 360), ((-i) % 360, (a + j * i) % 360)):
                seen.add((ii, aa))
    print('extra: classes of home-coming pairs under shift, reversal and mirror:', classes)
    # check diameters constant on classes
    dd = {(r['inc'], r['ang']): r['diam'] for r in home}
    worst = 0.0
    for (i, a), v in dd.items():
        for (ii, aa) in ((i, (a + i) % 360), (i, (i - a) % 360), ((-i) % 360, (-a) % 360)):
            worst = max(worst, abs(dd[(ii, aa)] - v))
    print('   max difference of diameter between a pair and its shifted / reversed / mirrored partner:', worst)


if __name__ == '__main__':
    main()

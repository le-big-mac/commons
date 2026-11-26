"""Brute force: add up the turtle's steps.  Does NOT use any rule.

HAKMEM form: step k (k = 0, 1, 2, ...) is the unit vector at heading 2^k * theta,
theta = 2*pi*p/q.  The heading index 2^k * p mod q is followed until it repeats;
the steps of one full cycle are added up.  The path is bounded iff that cycle sum
is nought (otherwise the turtle drifts by the cycle sum each time round).

Output: brute.out
"""
import math, sys
import numpy as np

TOL = 1e-9


def cycle_sum(p, q):
    """Return (tail_len, cycle_len, |cycle sum|) for first heading 2*pi*p/q."""
    seen = {}
    seq = []
    a = p % q
    while a not in seen:
        seen[a] = len(seq)
        seq.append(a)
        a = (2 * a) % q
    tail = seen[a]
    cyc = np.array(seq[tail:], dtype=np.float64)
    ang = 2.0 * math.pi * cyc / q
    sx = math.fsum(np.cos(ang).tolist())
    sy = math.fsum(np.sin(ang).tolist())
    return tail, len(seq) - tail, math.hypot(sx, sy)


def walk_extent(p, q, nsteps):
    """Really walk nsteps and return the largest distance from the start."""
    a = p % q
    x = y = 0.0
    far = 0.0
    for _ in range(nsteps):
        t = 2.0 * math.pi * a / q
        x += math.cos(t)
        y += math.sin(t)
        far = max(far, math.hypot(x, y))
        a = (2 * a) % q
    return far


def gospel_extent(p, q, nsteps):
    """The book's program: LEFT ANGLE, FORWARD 1, ANGLE doubled.  Largest distance."""
    turn = p % q
    head = 0
    x = y = 0.0
    far = 0.0
    for _ in range(nsteps):
        head = (head + turn) % q
        t = 2.0 * math.pi * head / q
        x += math.cos(t)
        y += math.sin(t)
        far = max(far, math.hypot(x, y))
        turn = (2 * turn) % q
    return far


if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/brute.out', 'w')
    bounded = []
    small_nonzero = (9e9, None)
    big_zero = (0.0, None)
    res = {}
    for m in range(3, 3001, 2):
        tail, n, s = cycle_sum(1, m)
        res[m] = s
        if s < TOL:
            bounded.append(m)
            if s > big_zero[0]:
                big_zero = (s, m)
        else:
            if s < small_nonzero[0]:
                small_nonzero = (s, m)
    print('odd denominators 3..3000, numerator 1, tolerance', TOL, file=out)
    print('number bounded:', len(bounded), 'of', len(res), file=out)
    print('first thirty:', bounded[:30], file=out)
    print('all:', bounded, file=out)
    print('largest |sum| called nought: %.3e at m=%d' % big_zero, file=out)
    print('smallest |sum| called not nought: %.6f at m=%d' % small_nonzero, file=out)
    nz = sorted((s, m) for m, s in res.items() if s >= TOL)[:8]
    print('eight smallest nonzero sums:', [(round(s, 6), m) for s, m in nz], file=out)
    # other numerators, a sample: does boundedness depend on p?
    bad = 0
    tested = 0
    for m in range(3, 700, 2):
        for p in range(2, m):
            if math.gcd(p, m) == 1:
                tested += 1
                if (cycle_sum(p, m)[2] < TOL) != (res[m] < TOL):
                    bad += 1
    print('other numerators (odd m < 700, all p coprime): tested', tested, 'disagree with p=1:', bad, file=out)
    # even denominators: compare q = 2^a * m with m (p = 1 and p = 3 where coprime)
    bad = 0
    tested = 0
    for m in range(1, 400, 2):
        for a in range(1, 5):
            q = m << a
            for p in (1, 3, 5, 7):
                if math.gcd(p, q) == 1:
                    tested += 1
                    b = cycle_sum(p, q)[2] < TOL
                    want = (res[m] < TOL) if m > 1 else False
                    if b != want:
                        bad += 1
    print('even denominators 2^a*m (m<400 odd, a=1..4): tested', tested, 'disagree with odd part:', bad, file=out)
    # really walk: HAKMEM form and GOSPEL form, 20000 steps
    for q in (9, 18, 36, 45, 63, 171, 225, 441, 4, 8, 1, 3, 7, 1143, 2525, 9009, 9837):
        print('q=%5d  HAKMEM walk far=%10.3f   GOSPEL walk far=%10.3f   cycle (tail,len,|sum|)=%s'
              % (q, walk_extent(1, q, 20000), gospel_extent(1, q, 20000), cycle_sum(1, q)), file=out)
    out.close()
    print(open('/home/agent2/gospel/referee/brute.out').read()[:6000])

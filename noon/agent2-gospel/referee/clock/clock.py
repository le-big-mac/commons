"""Referee, blind: the clock of q hours.  Nothing of the coordinator's is imported.
For p/q in lowest terms, q = 2^s m (m odd): the marked hours are p*2^k mod q for k = s .. s+n-1 (one round).
'Falls into l-gons' (l prime, l | q): with every marked hour a, a + q/l is marked too.
'Closes': the unit steps at headings 2*pi*hour/q, added up over the round, come to nought (|sum| < 1e-9).
Output: clock.out"""
import math, random

def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: n //= d; f[d] = f.get(d, 0) + 1
        d += 1 if d == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def round_hours(p, q):
    s = 0; m = q
    while m % 2 == 0: m //= 2; s += 1
    a = p % q
    for _ in range(s): a = a * 2 % q
    hours = []; b = a
    while True:
        hours.append(b); b = b * 2 % q
        if b == a: break
    return s, hours

def study(p, q):
    s, H = round_hours(p, q)
    S = set(H)
    sx = math.fsum(math.cos(2 * math.pi * h / q) for h in H); sy = math.fsum(math.sin(2 * math.pi * h / q) for h in H)
    mag = math.hypot(sx, sy)
    f = factor(q)
    gons_twice = [l for l, e in f.items() if e >= 2 and all((a + q // l) % q in S for a in H)]
    gons_once = [l for l, e in f.items() if e == 1 and all((a + q // l) % q in S for a in H)]
    return s, len(H), mag, gons_twice, gons_once, f

if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/clock/clock.out', 'w')
    agree = dis = once = 0; closed = 0; least_open = 9e9; worst_closed = 0.0; two_l = []; ngons = {}
    for q in range(3, 6002, 2):
        s, n, mag, g2, g1, f = study(1, q)
        c = mag < 1e-9
        closed += c
        if c: worst_closed = max(worst_closed, mag)
        else: least_open = min(least_open, mag)
        if c == bool(g2): agree += 1
        else: dis += 1
        if g1: once += 1
        if len(g2) > 1: two_l.append((q, g2))
        if c:
            l = g2[0]; ngons[n // l] = ngons.get(n // l, 0) + 1
    print('odd q 3..6001, p = 1: closes %d; "closes" agrees with "falls into l-gons for a prime l that comes in at least twice" in %d, disagrees in %d'
          % (closed, agree, dis), file=out)
    print('   largest sum called nought %.1e, least not called nought %.4f; rounds falling into l-gons for an l that comes in once: %d' % (worst_closed, least_open, once), file=out)
    print('   rounds falling into polygons of two different primes: %d, e.g. %s' % (len(two_l), two_l[:6]), file=out)
    print('   number of l-gons in a closed round (smallest l): fewest %d; rounds made of exactly one polygon: %d; of two: %d'
          % (min(ngons), ngons.get(1, 0), ngons.get(2, 0)), file=out)
    rnd = random.Random(20261127); agree = dis = once = tested = evens = closedc = 0
    while tested < 600:
        q = rnd.randrange(3, 40000)
        if tested % 2 == 0: q = rnd.choice([9, 25, 27, 45, 49, 63, 81, 99, 117, 121, 125, 147, 171, 189, 225, 441, 513, 1323]) * rnd.choice([1, 2, 4, 8, 16, 3, 5, 7, 11, 6, 10, 12, 20, 28])
        p = rnd.randrange(2, q)
        if math.gcd(p, q) != 1: continue
        s, n, mag, g2, g1, f = study(p, q)
        if q % 2 == 0 and all(l == 2 for l in f): continue        # a power of 2: no round to speak of but the hour 0
        tested += 1; evens += (q % 2 == 0); c = mag < 1e-9; closedc += c
        if c == bool(g2): agree += 1
        else: dis += 1; print('   DISAGREE', p, q, mag, g2, file=out)
        if g1: once += 1; print('   ONCE', p, q, g1, file=out)
    print('600 fractions p/q with p not 1 (%d with even q; %d close): agree %d, disagree %d; l-gons for an l that comes in once: %d' % (evens, closedc, agree, dis, once), file=out)
    for (p, q) in ((1, 9), (1, 45), (1, 63), (1, 441), (5, 36), (1, 21), (1, 18), (7, 72), (1, 1194649 if False else 189)):
        s, n, mag, g2, g1, f = study(p, q); sH = sorted(round_hours(p, q)[1])
        print('%d/%d: tail %d, round %d, |sum| %.4f, l-gons for %s (once: %s); hours %s' % (p, q, s, n, mag, g2, g1, sH if n <= 14 else '...'), file=out)
    out.close()
    print(open('/home/agent2/gospel/referee/clock/clock.out').read())

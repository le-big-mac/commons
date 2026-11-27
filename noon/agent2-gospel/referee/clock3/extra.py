"""Referee: a few figures for the fixed sentences.  Output: extra.out"""
import math, sys
sys.path.insert(0, '/home/agent2/gospel/referee/clock3')
import check
def parts(q):
    s = 0; m = q
    while m % 2 == 0: m //= 2; s += 1
    return s, m
def first_repeat(p, q):
    seen = set(); t = p % q; k = 0
    while t not in seen: seen.add(t); t = t * 2 % q; k += 1
    return k
if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/clock3/extra.out', 'w')
    # the memo's rule, every bottom number to 130 and every first turn: where does it first break?
    breaks = []
    for q in range(2, 131):
        s, m = parts(q); f = check.factor(m); rep = any(e >= 2 for e in f.values())
        for p in range(1, q):
            if math.gcd(p, q) != 1: continue
            away = (m == 1) or check.walk_gain(p, q, s, check.order(m)) > 1e-9
            if rep == away: breaks.append((p, q, 'marches away though an odd prime comes in twice' if away else 'does not march away though no odd prime comes in twice'))
    print('memo rule, bottom numbers 2..130, every first turn: bottom numbers that break it:', sorted({b[1] for b in breaks}), '; kinds:', sorted({b[2] for b in breaks}), file=out)
    print('turns before a turn comes again, counted from the first step: 1/18 %d, 1/6 %d; rounds: %d and %d' % (first_repeat(1, 18), first_repeat(1, 6), check.order(9), check.order(3)), file=out)
    print('441: rounds of 1/441, 1/147 (a 3 out), 1/63 (a 7 out): %d, %d, %d' % (check.order(441), check.order(147), check.order(63)), file=out)
    print('27: rounds of 1/27 and 1/9: %d, %d; 225: 1/225, 1/75, 1/45: %d, %d, %d' % (check.order(27), check.order(9), check.order(225), check.order(75), check.order(45)), file=out)
    # open rounds whose hours all lie within less than half the clock
    half = other = 0; near = (9, None)
    for q in range(3, 2002, 2):
        n = check.order(q); H = []; t = 1
        for _ in range(n): H.append(t); t = t * 2 % q
        g = check.walk_gain(1, q, 0, n)
        if g < 1e-9: continue
        Hs = sorted(H); gaps = [Hs[i + 1] - Hs[i] for i in range(len(Hs) - 1)] + [Hs[0] + q - Hs[-1]]
        if max(gaps) > q / 2: half += 1
        else: other += 1
        d = abs((g * 1000) % 1 - 0.5) / 1000
        if d < near[0]: near = (d, (q, g))
    print('odd bottoms 3..2001, first turn 1, rounds that do not close: hours all within less than half the clock %d; not so %d' % (half, other), file=out)
    print('nearest of those distances to a rounding boundary of the third decimal: %.2e away, at 1/%d (%.9f)' % (near[0], near[1][0], near[1][1]), file=out)
    print('1/7: hours 1, 2, 4 span %d of 7 (half is 3.5); 1/9 hours 1,2,4,5,7,8: gaps 1,2,1,2,1,2' % (4 - 1), file=out)
    out.close(); print(open('/home/agent2/gospel/referee/clock3/extra.out').read())

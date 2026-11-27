"""Referee, second clock check: the made sentences' facts by my own orders and hours.  Output: check.out"""
import json, math
def order(m):
    if m == 1: return 1
    n, x = 1, 2 % m
    while x != 1: x = x * 2 % m; n += 1
    return n
def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: n //= d; f[d] = f.get(d, 0) + 1
        d += 1 if d == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def hours_of(p, q):
    s = 0; m = q
    while m % 2 == 0: m //= 2; s += 1
    a = p % q
    for _ in range(s): a = a * 2 % q
    H = []; b = a
    while True:
        H.append(b); b = b * 2 % q
        if b == a: break
    return s, m, H
if __name__ == '__main__':
    D = json.load(open('/home/agent2/gospel/referee/clock2/dump.json')); out = open('/home/agent2/gospel/referee/clock2/check.out', 'w')
    bad = []; c = dict(closed=0, open_rep=0, open_norep_poly=0, prime_or_none=0, straight=0, twoout=0, idle=0); facts = 0
    for d in D:
        p, q = d['p'], d['q']; s, m, H = hours_of(p, q); n = len(H); S = set(H); h0 = H[0]; f = factor(m)
        if m == 1: c['straight'] += 1; continue
        if (s, m, n, h0) != (d['tail'], d['m'], d['n'], d['first']): bad.append((p, q, 'tail, odd part, round or first hour'))
        sx = math.fsum(math.cos(2 * math.pi * h / q) for h in H); sy = math.fsum(math.sin(2 * math.pi * h / q) for h in H); closes = math.hypot(sx, sy) < 1e-9
        mine = []
        for l, e in sorted(f.items()):
            if e < 2: continue
            n1 = order(m // l); facts += 1
            if n not in (n1, l * n1): bad.append((p, q, 'neither l times as long nor no longer', l))
            mine.append(dict(l=l, e=e, n1=n1, long=(n == l * n1)))
            # "after n1 steps the turn stands again where it stood on a clock of q/l hours"
            if any((H[(k + n1) % n] - H[k]) % (q // l) for k in range(n)): bad.append((p, q, 'does not stand where it stood on the clock of q/l', l))
            poly = [(h0 + j * (q // l)) % q for j in range(l)]
            if n == l * n1:
                visit = [H[(i * n1) % n] for i in range(1, l)]
                if sorted(visit) != sorted(poly[1:]) or h0 in visit or H[(l * n1) % n] != h0: bad.append((p, q, 'the corners in turn', l))
                if not all(((a + q // l) % q) in S for a in H): bad.append((p, q, 'long but not every hour has its others', l))
            else:
                if H[n1 % n] != h0 or any(x in S for x in poly[1:]): bad.append((p, q, 'stands on h0 itself, others never reached', l))
        if [(x['l'], x['e'], x['n1'], x['long']) for x in mine] != [(x['l'], x['e'], x['n1'], x['long']) for x in d['take']]: bad.append((p, q, 'takeOut differs from mine'))
        if closes != any(x['long'] for x in mine) or closes != d['bounded']: bad.append((p, q, 'closes against "l times as long"'))
        if sorted(d['kinds']) != [x['l'] for x in mine if x['long']]: bad.append((p, q, 'polygons against long primes'))
        if closes: c['closed'] += 1; c['idle'] += any(not x['long'] for x in mine)
        elif mine: c['open_rep'] += 1; c['twoout'] += len(mine) > 1
        elif len(f) >= 2:
            c['open_norep_poly'] += 1; lone = min(f); poly = [(h0 + j * (q // lone)) % q for j in range(lone)]
            badc = [h for h in poly if h % lone == 0]
            if len(badc) != 1 or badc[0] in S or any(h % lone == 0 for h in H): bad.append((p, q, 'the one corner the prime divides'))
        else: c['prime_or_none'] += 1
    print('%d turtles; %d checks of "l times as long or no longer"; faults: %d %s' % (len(D), facts, len(bad), bad[:8]), file=out)
    print('cases:', c, file=out)
    out.close(); print(open('/home/agent2/gospel/referee/clock2/check.out').read())

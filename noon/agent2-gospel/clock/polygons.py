"""The clock picture, tried before it is drawn.  Noon (agent2), 27 November 2026.
On a clock with q hours mark the turtle's turns of one round (in units of 1/q of a whole turn: p, 2p, 4p, ... modulo q, after
the tail).  The steps of a round, laid tail to tail from the centre, are hands pointing at those hours (all turned back by the
same amount), so the round closes exactly when the marked hours balance about the centre.
Claim to try: the round closes exactly when, for some prime l that comes into q at least twice, the marked hours fall into
regular l-gons: with every marked hour a, the hours a + q/l, a + 2q/l, ... are marked too.
Tried against Python's own sums (table.json: every odd m from 3 to 3001 with p = 1; 306 fractions p/q, odd and even q).
usage: python -I polygons.py ../table.json > polygons.out"""
import sys, json
def factor(m):
    out = []; l = 2
    while l * l <= m:
        if m % l == 0:
            e = 0
            while m % l == 0: m //= l; e += 1
            out.append((l, e))
        l += 1 if l == 2 else 2
    if m > 1: out.append((m, 1))
    return out
def round_hours(p, q):                       # the turns of one round, as hours on a clock of q: after the tail, until the first comes again
    seen = {}; t = p % q; k = 0
    while t not in seen: seen[t] = k; t = t * 2 % q; k += 1
    tail = seen[t]; hours = [h for h, i in seen.items() if i >= tail]
    return tail, hours
def polygons(hours, q):                      # the primes l, coming into q at least twice, for which the hours fall into regular l-gons
    S = set(hours); out = []
    for l, e in factor(q):
        if e < 2 or l == 2: continue
        step = q // l
        if all((a + step) % q in S for a in S): out.append(l)
    return out
if __name__ == '__main__':
    table = json.load(open(sys.argv[1]))
    agree = 0; wrong = []; two = []; byl = {}
    for m_s, row in table['odd'].items():
        m = int(m_s); closes = bool(row[0]); tail, hours = round_hours(1, m); ls = polygons(hours, m)
        assert tail == 0 and len(hours) == row[1]
        if closes == bool(ls): agree += 1
        else: wrong.append(m)
        if len(ls) > 1: two.append((m, ls))
        for l in ls: byl[l] = byl.get(l, 0) + 1
    print('odd m from 3 to 3001, first turn 1/m: %d denominators; the round closes exactly when its hours fall into regular l-gons for a prime l that comes in twice or more: agree %d, disagree %d %s' % (len(table['odd']), agree, len(wrong), wrong[:5]))
    print('   closing rounds by the number of corners of their polygons:', sorted(byl.items()))
    print('   rounds that fall into polygons of two kinds at once: %d; the first few: %s' % (len(two), two[:6]))
    agree = 0; wrong = []; tails = 0; evens = 0
    for r in table['fracs']:
        tail, hours = round_hours(r['p'], r['q']); ls = polygons(hours, r['q'])
        assert tail == r['tail'] and len(hours) == r['round'], (r, tail, len(hours))
        if r['q'] % 2 == 0: evens += 1
        if tail: tails += 1
        if bool(ls) == bool(r['bounded']): agree += 1
        else: wrong.append((r['p'], r['q']))
    print('fractions p/q of the table (%d, of them %d with even q, %d with a tail): agree %d, disagree %d %s' % (len(table['fracs']), evens, tails, agree, len(wrong), wrong[:5]))
    # the corners must be a repeated prime's: with a prime that comes in once, the l-gon through an hour holds an hour the doubling cannot reach
    once = 0; reach = 0
    for m_s in table['odd']:
        m = int(m_s); tail, hours = round_hours(1, m); S = set(hours)
        for l, e in factor(m):
            if e == 1:
                once += 1
                if all((a + m // l) % m in S for a in S): reach += 1
    print('primes that come into m once (m odd, 3 to 3001): %d cases; rounds that fall into l-gons for such a prime: %d' % (once, reach))
    for q in (9, 45, 63, 7, 441, 21, 171):
        tail, hours = round_hours(1, q); print('   1/%d: hours %s; polygons for l in %s' % (q, sorted(hours) if len(hours) <= 14 else str(len(hours)) + ' hours', polygons(hours, q)))

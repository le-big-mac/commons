"""Referee: the recipe as now worded, done to the letter as a reader would do it, against the truth by adding up the round.

The recipe: lowest terms; the 2s out of the bottom number; split what is left into primes; no prime twice -> marches away;
otherwise cross one of a repeated prime out and count the steps before each turtle's turns repeat (by doubling, whole turns
left out, until a turn comes again); l times as many -> comes home; the same -> try any other repeated prime; none gives
more -> marches away; were there 2s -> for "comes home" read "circles one loop for ever".
Output: recipe.out"""
import math, itertools, json, re
import numpy as np


def count_repeat(p, b):
    """steps before the turns of p/b repeat: double, whole turns left out, until a turn comes again"""
    seen = set(); t = p % b; k = 0
    while t not in seen:
        seen.add(t); t = t * 2 % b; k += 1
    return k


def primes_of(n):
    f = []; d = 3
    while d * d <= n:
        while n % d == 0: f.append(d); n //= d
        d += 2
    if n > 1: f.append(n)
    return f


def recipe(P, Q):
    """every verdict the recipe can give, over every order of trying the repeated primes; and any count that is odd"""
    g = math.gcd(abs(P), Q); p, q = P // g, Q // g            # lowest terms
    b = q; twos = 0
    while b % 2 == 0: b //= 2; twos += 1                       # the 2s out
    f = primes_of(b); rep = sorted({l for l in f if f.count(l) >= 2})
    if not rep: return {'marches away'}, []
    verdicts = set(); odd = []
    n = count_repeat(p, b)
    for order in itertools.permutations(rep):
        v = 'marches away'
        for l in order:
            n1 = count_repeat(p, b // l)
            if n == l * n1: v = 'comes home'; break
            if n != n1: odd.append((P, Q, l, n, n1))
        if v == 'comes home' and twos: v = 'circles one loop for ever'
        verdicts.add(v)
    return verdicts, odd


def truth(P, Q):
    g = math.gcd(abs(P), Q); q = Q // g; p = (P // g) % q
    s = 0; m = q
    while m % 2 == 0: m //= 2; s += 1
    if m == 1: return 'marches away'
    t = p
    for _ in range(s): t = t * 2 % q
    H = []; a = t
    while True:
        H.append(a); a = a * 2 % q
        if a == t: break
    ang = np.array(H, dtype=np.float64) * (2 * math.pi / q)
    closes = math.hypot(math.fsum(np.cos(ang).tolist()), math.fsum(np.sin(ang).tolist())) < 1e-9
    return ('comes home' if s == 0 else 'circles one loop for ever') if closes else 'marches away'


if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/clock3b/recipe.out', 'w')
    cache = {}; n = wrong = split = oddc = 0; ex = []; kinds = {}
    def one(P, Q):
        global n, wrong, split, oddc
        g = math.gcd(abs(P), Q); key = ((P // g) % (Q // g), Q // g)
        if key not in cache: cache[key] = truth(P, Q)
        v, odd = recipe(P, Q); n += 1
        if len(v) != 1: split += 1; ex.append(('the order of trying changes the verdict', P, Q, sorted(v)))
        elif v != {cache[key]}: wrong += 1; ex.append(('verdict', P, Q, sorted(v), cache[key]))
        if odd: oddc += 1; ex.append(('a count neither l times nor the same', odd[0]))
        kinds[cache[key]] = kinds.get(cache[key], 0) + 1
    for Q in range(1, 521):
        for P in range(0, Q + 1): one(P, Q)                    # every first turn, lowest terms or not, 0 and a whole turn too
        for P in (-1, -2, -Q - 1, Q + 1, 2 * Q + 3, 7 * Q - 2): one(P, Q)
    extra = [11025, 99225, 17325, 53361, 3025, 1225, 1089, 5929, 7569, 14161, 1194649, 9 * 1093, 2 * 11025, 4 * 441, 8 * 225, 3 * 1093 * 1093]
    for Q in extra:
        for P in (1, 2, 5, 7, Q - 1, -1, 3, 21): one(P, Q)
    print('%d first turns tried (bottom numbers 1..520, every first turn from 0 to a whole turn, six more each beyond; %d larger bottoms): '
          'verdict other than the truth %d; verdict depending on the order of trying %d; a count neither l times nor the same %d'
          % (n, len(extra), wrong, split, oddc), file=out)
    print('truth among them:', kinds, file=out)
    for e in ex[:12]: print('  ', e, file=out)
    # against the page's own words, for the turtles I read off the page
    D = json.load(open('/home/agent2/gospel/referee/clock3b/page.json')); cmpn = dis = 0
    for r in D:
        if not r['valid']: continue
        say = r['say']
        pv = 'comes home' if 'it comes home after' in say else 'circles one loop for ever' if 'never gets away' in say else 'marches away'
        v, odd = recipe(r['p'], r['q']); cmpn += 1
        if v != {pv}: dis += 1; print('   PAGE', r['p'], r['q'], sorted(v), pv, file=out)
    print('against the page\'s own forecast: %d turtles, the recipe disagrees in %d' % (cmpn, dis), file=out)
    for P, Q in ((1, 1), (3, 8), (1, 18), (-1, 9), (3, 9), (0, 7), (1, 441), (5, 36)):
        print('  %d/%d: recipe %s; truth %s' % (P, Q, sorted(recipe(P, Q)[0]), truth(P, Q)), file=out)
    out.close(); print(open('/home/agent2/gospel/referee/clock3b/recipe.out').read())

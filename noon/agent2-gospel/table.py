"""A table for the page's tests, made in Python by walking and adding up, with nothing from core.js and nothing from the rule.
usage: python -I table.py table.json

odd:      for odd m from 3 to 3001 with numerator 1: is one round of the turns nought when added up (so the turtle is bounded)?
fracs:    made-up fractions p/q, q odd or even: the tail (steps before the turns repeat), the length of a round, whether the
          round adds up to nought, how far one round carries the turtle, and the first step at which the walked turtle is home
corners:  for a dozen turtles, where Python's walk stands after chosen steps (the turtle starts facing up the page, turns left, then steps)"""
import json, math, random, sys
from fractions import Fraction


def tail_round(p, q):
    """the turns are p 2^k / q of a turn; they repeat with period n after s steps: found by doubling, not by any formula"""
    seen = {}; x = p % q; k = 0
    while x not in seen: seen[x] = k; x = x * 2 % q; k += 1
    return seen[x], k - seen[x]

def places(p, q, n):
    turn = p % q; head = 0; x = y = 0.0; out = [(0.0, 0.0)]; home = 0
    for k in range(1, n + 1):
        head = (head + turn) % q; turn = turn * 2 % q
        x -= math.sin(2 * math.pi * head / q); y += math.cos(2 * math.pi * head / q); out.append((x, y))
        if not home and x * x + y * y < 1e-14 and head == 0 and turn == p % q: home = k
    return out, home

def one(p, q):
    fr = Fraction(p, q); p, q = fr.numerator % fr.denominator, fr.denominator
    s, n = tail_round(p, q); pts, home = places(p, q, s + 3 * n)
    dx, dy = pts[s + n][0] - pts[s][0], pts[s + n][1] - pts[s][1]; gain = math.hypot(dx, dy)
    return {'p': p, 'q': q, 'tail': s, 'round': n, 'bounded': gain < 1e-9, 'gain': gain, 'home': home}


if __name__ == '__main__':
    odd = {}
    for m in range(3, 3002, 2):
        r = one(1, m); odd[m] = [r['bounded'], r['round'], r['gain']]
    rng = random.Random(20261126)
    picks = [(1, 9), (1, 45), (1, 7), (1, 63), (1, 171), (1, 25), (1, 27), (1, 12), (2, 9), (1, 8), (3, 8), (1, 18), (1, 90), (5, 36), (1, 1), (0, 5), (4, 9), (7, 45), (1, 99), (1, 441), (1, 2525), (1, 9009),
             (1, 72), (1, 50), (11, 100), (1, 189), (1, 513), (2, 45), (44, 45), (-1, 9), (10, 90), (1, 6), (1, 36), (1, 1194649), (1, 19683), (1, 59049), (1, 1048576), (7, 2000000)]
    while len(picks) < 300:
        q = rng.choice([rng.randrange(2, 400), rng.randrange(2, 4000), 9 * rng.randrange(1, 300), 25 * rng.randrange(1, 100), 2 ** rng.randrange(1, 6) * (2 * rng.randrange(1, 300) + 1)])
        picks.append((rng.randrange(1, q), q))
    picks.append((1635, 1009681))                     # the nearest miss (added 26 November, after the others, so that none of them changes)
    picks += [(1739, 1094420), (12605, 1741011), (2195, 65537), (1008046, 1009681)]     # four more near misses: one after a tail, and the mirror image of the nearest
    fr = [dict(one(p, q), P=p, Q=q) for p, q in picks]
    cor = []
    for p, q in [(1, 9), (1, 45), (1, 7), (1, 63), (1, 171), (1, 25), (1, 27), (1, 12), (2, 9), (3, 8), (-1, 9), (1, 99), (1, 36), (1, 441), (1, 1194649), (1635, 1009681)]:
        s, n = tail_round(p % q, q); total = min(s + 2 * n, 400); pts, home = places(p, q, total)
        ks = sorted(set(k for k in (1, 2, 3, 5, total // 3, total // 2, total - 1, total) if 1 <= k <= total))
        cor.append({'P': p, 'Q': q, 'n': total, 'at': [[k, pts[k][0], pts[k][1]] for k in ks]})
    json.dump({'odd': odd, 'fracs': fr, 'corners': cor}, open(sys.argv[1], 'w'))
    print(f"odd m from 3 to 3001: {len(odd)}; bounded: {sum(1 for v in odd.values() if v[0])}; fractions: {len(fr)}, bounded {sum(1 for r in fr if r['bounded'])}, home at some step {sum(1 for r in fr if r['home'])}; least gain not called nought: {min(r['gain'] for r in fr if not r['bounded']):.4f}; largest called nought: {max([r['gain'] for r in fr if r['bounded']] + [0]):.1e}")

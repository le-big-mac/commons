"""A table for the page's tests, made in Python by walking, with nothing from core.js.
usage: python -I table.py table.json

whole:   for INC 1..359 and ANGLE 0..359, the first step at which the walked turtle is home (0: not in 720 steps)
corners: for a dozen turtles, where Python's walk stands after chosen steps (the turtle starts facing up the page)
decimal: made-up pairs with up to three decimals; the forecast by exact fractions (never, or the number of steps),
         and for the shorter ones the first step at which the walked turtle is home."""
import json, math, os, random, sys
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inspi import walk_all


def by_fractions(A, I):
    """A, I: whole thousandths of a degree.  Returns (q, None) for never, (q, steps) otherwise."""
    inc = Fraction(I % 360000, 360000)                      # INC as a part of a turn, in lowest terms
    q, p = inc.denominator, inc.numerator
    T = (Fraction(A, 360000) * q + Fraction(p * (q - 1), 2)) % 1
    return (q, None) if T == 0 else (q, q * T.denominator)


def walked(A, I, n):
    """the rule, step by step, turning in whole thousandths of a degree"""
    a0 = A % 360000; ang = a0; inc = I % 360000; head = 0; x = y = 0.0
    for k in range(1, n + 1):
        x += math.sin(2 * math.pi * head / 360000); y += math.cos(2 * math.pi * head / 360000)
        head = (head + ang) % 360000; ang = (ang + inc) % 360000
        if x * x + y * y < 1e-14 and head == 0 and ang == a0: return k, x, y
    return 0, x, y


def places(A, I, n):
    a0 = A % 360000; ang = a0; inc = I % 360000; head = 0; x = y = 0.0; out = [(0.0, 0.0)]
    for k in range(1, n + 1):
        x += math.sin(2 * math.pi * head / 360000); y += math.cos(2 * math.pi * head / 360000)
        head = (head + ang) % 360000; ang = (ang + inc) % 360000; out.append((x, y))
    return out


if __name__ == '__main__':
    first, reach, end = walk_all()
    cor = []
    for A, I, n in [(2000, 20000, 90), (10000, 20000, 234), (0, 7000, 720), (1000, 2000, 1080), (112000, 135000, 720), (30000, 180000, 6), (40000, 500, 1440),
                    (25000, 210000, 36), (2500, 20000, 144), (-2000, -20000, 90), (90000, 0, 4), (180000, 180000, 4)]:
        pts = places(A, I, n); ks = sorted(set(k for k in (1, 2, 3, 5, n // 3, n // 2, n - 1, n) if 1 <= k <= n))
        cor.append({'A': A, 'I': I, 'n': n, 'at': [[k, pts[k][0], pts[k][1]] for k in ks]})
    rng = random.Random(20261126); dec = []
    picks = [(2000, 20000), (10000, 20000), (0, 500), (500, 250), (125, 250), (1, 1), (0, 7000), (90000, 180000), (359999, 359999), (-2000, -20000), (0, 0), (72000, 0), (100, 0),
             (1234, 5678), (45000, 22500), (22500, 45000), (11250, 22500), (300, 7200), (0, 144000), (60000, 144000), (1500, 3000), (750, 1500)]
    while len(picks) < 400:
        kind = rng.random()
        if kind < 0.3: picks.append((rng.randrange(0, 360000), rng.randrange(1, 360000)))
        elif kind < 0.6: picks.append((rng.randrange(0, 3600) * 100, rng.randrange(1, 3600) * 100))
        elif kind < 0.8: picks.append((rng.randrange(0, 720) * 500, rng.randrange(1, 720) * 500))
        else: picks.append((rng.randrange(0, 1440) * 250, rng.choice([250, 500, 750, 1250, 2500, 7500, 12500, 22500, 37500, 112500])))
    for A, I in picks:
        q, steps = by_fractions(A, I); row = {'A': A, 'I': I, 'q': q, 'steps': steps}
        if steps is not None and steps <= 30000:
            row['home'] = walked(A, I, steps + 50)[0]
        if steps is None and q <= 6000:
            k, x, y = walked(A, I, 3 * q); row['after3'] = math.hypot(x, y); row['home'] = k
        dec.append(row)
    json.dump({'whole': [[int(v) for v in first[inc]] for inc in range(360)], 'decimal': dec, 'corners': cor}, open(sys.argv[1], 'w'))
    n_home = sum(1 for r in dec if r['steps'] is not None); n_walk = sum(1 for r in dec if 'home' in r)
    print(f"whole-degree pairs: {359 * 360}; never home: {int((first[1:] == 0).sum())}; decimal pairs: {len(dec)}, of which {n_home} come home by the fractions and {len(dec) - n_home} never; walked: {n_walk}")

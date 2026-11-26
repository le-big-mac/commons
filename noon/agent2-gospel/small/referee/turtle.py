# turtle.py -- walk the turtle itself (turn, step, double the turn), angles kept as whole numbers mod q,
# positions in mpmath (30 digits): how far does one round of n steps carry it?
import sys
from mpmath import mp, mpf, cos, sin, pi, sqrt, nstr
mp.dps = 30
def walk(p, q, steps):
    turn = p % q; head = 0; x = mpf(0); y = mpf(0); pos = [(x, y)]
    for _ in range(steps):
        head = (head + turn) % q
        t = 2 * pi * head / q
        x += cos(t); y += sin(t); pos.append((x, y))
        turn = 2 * turn % q
    return pos
def odd_part(q):
    e = 0
    while q % 2 == 0: q //= 2; e += 1
    return q, e
def order(m):
    if m == 1: return 1
    x = 2 % m; n = 1
    while x != 1: x = 2 * x % m; n += 1
    return n
if __name__ == '__main__':
    for p, q in [(1635, 1009681), (1739, 273605), (1739, 4 * 273605), (2923, 1915235), (1, 9), (1, 63), (5, 16), (3, 2 ** 20)]:
        m, e = odd_part(q); n = order(m)
        pos = walk(p, q, e + 3 * n)
        d = []
        for start in (0, e, e + n):
            (x0, y0), (x1, y1) = pos[start], pos[start + n]
            d.append(nstr(sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2), 15))
        print('p/q = %d/%d : odd part %d, %d factors of 2, round n = %d ; distance over n steps from step 0: %s ; from step e: %s ; from step e+n: %s' % (p, q, m, e, n, d[0], d[1], d[2]))

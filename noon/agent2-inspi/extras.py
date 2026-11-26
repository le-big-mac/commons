"""Two facts the page and the write-up want to state, tried before they are written.
usage: python -I extras.py > extras.out      (numpy)

1. Does a whole-degree turtle that never comes home ever stand on its starting point again (at any step, facing any way)?
   After n laps it is n B from its start and a lap is at most q steps long, so only the first q / sqrt(q) + 1 laps can matter.
2. When the turning in a lap is a whole number of turns, are the q steps of a lap a Zadoff-Chu sequence of length q and
   root p, as the encyclopedia's page defines one: x_u(n) = exp(-j pi u n (n + c_f + 2 s) / N), c_f = N mod 2, s a whole number?"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inspi import predicted, corners

if __name__ == '__main__':
    away = [(inc, A) for inc in range(1, 360) for A in range(360) if predicted(inc, A)[2] is None]
    back = []; nearest = (9e9, None); most = 0
    for inc, A in away:
        q = predicted(inc, A)[0]; laps = int(math.sqrt(q)) + 2; pts = corners(inc, A, q * laps)[1:]
        d = np.abs(pts); k = int(d.argmin()); most = max(most, q * laps)
        if d[k] < 1e-7: back.append((inc, A, k + 1))
        if d[k] < nearest[0]: nearest = (float(d[k]), (inc, A, k + 1))
    print(f"1. pairs that never come home: {len(away)}; of these, on their starting point again at some step of the first sqrt(q) + 2 laps (up to {most} steps): {len(back)}" + (f"; the first few: {back[:6]}" if back else ""))
    print(f"   the nearest any of them comes to its start after leaving it: {nearest[0]:.6f} steps (INC {nearest[1][0]}, ANGLE {nearest[1][1]}, at step {nearest[1][2]})")
    ok = bad = 0; ex = None
    for inc, A in away:
        g = math.gcd(inc, 360); q = 360 // g; p = inc // g
        k = np.arange(q); head = (k * A + inc * k * (k - 1) // 2) % 360            # heading before step k, whole degrees
        steps = np.exp(-2j * np.pi * head / 360)                                   # a right turn is clockwise
        cf = q % 2; found = False
        for s in range(q):
            zc = np.exp(-1j * np.pi * p * k * (k + cf + 2 * s) / q)
            if np.abs(zc - steps).max() < 1e-9: found = True; break
        ok += found; bad += not found
        if found and ex is None and q == 18: ex = (inc, A, p, q, s)
    print(f"2. the steps of one lap are a Zadoff-Chu sequence of length q and root p (some whole shift s) in {ok} of the {len(away)}; not in {bad}")
    if ex: print(f"   for instance INC {ex[0]}, ANGLE {ex[1]}: root {ex[2]}, length {ex[3]}, s = {ex[4]}")
    # the control: a pair that does come home must not pass
    cnt = 0; tried = 0
    for inc, A in ((20, 2), (7, 0), (180, 89), (135, 112), (40, 30), (120, 1)):
        g = math.gcd(inc, 360); q = 360 // g; p = inc // g; k = np.arange(q); head = (k * A + inc * k * (k - 1) // 2) % 360
        steps = np.exp(-2j * np.pi * head / 360); cf = q % 2; tried += 1
        cnt += any(np.abs(np.exp(-1j * np.pi * p * k * (k + cf + 2 * s) / q) - steps).max() < 1e-9 for s in range(q))
    print(f"   control: of {tried} pairs that do come home, the lap is such a sequence in {cnt}")

"""Facts the blind referee reported that I had not counted, recounted here with a program of my own before they are used.
usage: python -I extras2.py > extras2.out      (numpy)

1. Laps that end on the starting point (B = 0) though the turtle is not then home: which whole-degree pairs?
2. How many whole-degree turtles that come home stand on their starting point before they are home?
3. The turtle of Fergus Murray's page (its turns are whole multiples of the amount added): does it come home exactly
   when the lap is of even length?
4. Which first turns march away, for each even amount: the referee's rule (g the greatest common divisor of the amount
   and 360: a multiple of g when 8 divides the amount, g/2 more than a multiple of g otherwise)."""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inspi import predicted, corners

if __name__ == '__main__':
    closed_lap = []; before = 0; home_pairs = 0; rule_ok = rule_bad = 0; murray_ok = murray_bad = 0; earliest = {}
    for inc in range(1, 360):
        g = math.gcd(inc, 360); q = 360 // g
        for A in range(360):
            qq, T, n = predicted(inc, A)
            says_away = (A % g == 0) if inc % 8 == 0 else (inc % 2 == 0 and A % g == g // 2)
            if says_away == (n is None): rule_ok += 1
            else: rule_bad += 1
            if n is None:
                continue
            home_pairs += 1
            pts = corners(inc, A, n); d = np.abs(pts[1:n])            # the corners after steps 1 .. n-1
            if abs(pts[q]) < 1e-9: closed_lap.append((inc, A))
            if d.size and d.min() < 1e-9: before += 1
        for j in (0, 1, 2, 5):
            A = (j * inc) % 360; qq, T, n = predicted(inc, A)
            good = (n == 2 * q) if q % 2 == 0 else (n is None)
            murray_ok += good; murray_bad += not good
    print(f"1. whole-degree pairs whose lap ends on the starting point without the turtle being home: {len(closed_lap)}; all have ANGLE = INC: {all(a == i for i, a in closed_lap)}; all have a lap of even length: {all((360 // math.gcd(i, 360)) % 2 == 0 for i, a in closed_lap)}; amounts from 1 to 359 not divisible by 8: {sum(1 for i in range(1, 360) if i % 8)}")
    print(f"2. of the {home_pairs} whole-degree turtles that come home, {before} stand on their starting point at some step before they are home")
    print(f"3. first turn 0, 1, 2 or 5 times the amount added (four turtles for each of 359 amounts): home after twice the lap when the lap is even and never when it is odd, in {murray_ok}; otherwise in {murray_bad}")
    print(f"4. the referee's rule for which first turns march away agrees with the formula for {rule_ok} of the 129,240 pairs; disagrees for {rule_bad}")

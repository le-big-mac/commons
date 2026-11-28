"""Recount for the revision after the referee's report: eleven elements on Z_1155 = 3*5*7*11 with residues
(9, 1, 1) modulo 3, (7, 1, 1, 1, 1) modulo 5, (5, 1, ..., 1) modulo 7 and all different modulo 11; all signings, by
division by the cyclotomic polynomials (the function example of combine.py)."""
import combine
r3 = [0] * 9 + [1, 2]
r5 = [0] * 7 + [1, 2, 3, 4]
r7 = [0] * 5 + [1, 2, 3, 4, 5, 6]
r11 = list(range(11))
n = 1155
B = [next(x for x in range(n) if x % 3 == a and x % 5 == b and x % 7 == c and x % 11 == d) for a, b, c, d in zip(r3, r5, r7, r11)]
combine.example(n, B)

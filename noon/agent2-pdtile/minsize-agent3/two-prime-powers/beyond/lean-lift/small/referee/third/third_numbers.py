"""Third look: numbers quoted to outside readers, by command.
n'_36 and its number of digits; the orders of the nine test groups and their numbers of digits; n'_m | n'_36 for m <= 36."""
import math
def primes_upto(n): return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
def nprime(m):
    out = 1
    for p in primes_upto(m):
        if p >= 3: out *= p ** ((m - 1) // (p - 1))
    return out
n36 = nprime(36)
print("n'_36 =", n36, "; digits:", len(str(n36)), "; about %.3g" % n36)
print("n'_37 =", nprime(37), "; digits:", len(str(nprime(37))))
print("n'_m divides n'_36 for every m <= 36:", all(n36 % nprime(m) == 0 for m in range(1, 37)))
print("6587407633447265625 < n'_36:", 6587407633447265625 < n36, "; digits of 6587407633447265625:", len(str(6587407633447265625)))
groups = {'A': {3: 6, 5: 4, 7: 3, 11: 2, 13: 1}, 'B': {3: 4, 5: 3, 7: 2, 37: 1, 41: 1}, 'C': {3: 5, 5: 2, 37: 2, 101: 1},
          'D': {3: 3, 5: 2, 7: 1, 11: 1, 13: 1, 17: 1}, 'E': {3: 7, 5: 3, 7: 2, 11: 1, 13: 1}, 'G': {3: 6, 5: 11, 7: 6, 11: 2, 13: 1},
          'H': {3: 13, 5: 23, 7: 5}, 'I': {3: 9, 5: 12, 7: 7, 11: 3, 13: 2}, 'J': {3: 14, 5: 24, 7: 6, 43: 2, 47: 1}}
for g, f in groups.items():
    n = math.prod(p ** a for p, a in f.items())
    print(g, n, "digits", len(str(n)))

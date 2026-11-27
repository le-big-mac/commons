# third_look.py -- every difference between the third and the fourth version of the plain paragraphs (word by word),
# and the numbers of the new sentences.
import difflib, math, sys
from fractions import Fraction
sys.path.insert(0, "..")
from rlib import mu
a = open("/home/agent3/door/check-small/extract-every-3.md", encoding="utf-8").read().split()
b = open("/home/agent3/door/check-small/extract-every-4.md", encoding="utf-8").read().split()
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        n += 1
        print("%2d. OLD: %s\n    NEW: %s" % (n, " ".join(a[i1:i2]) or "-", " ".join(b[j1:j2]) or "-"))


def A(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


W = sum(Fraction(A(t) - A(t - 2), 2 ** t) for t in range(2, 1001, 2))
print("W = %.6f: fewer than 845 in 1,000: %s; more than 155 in 1,000 good: %s" % (float(W), W + Fraction(1, 10 ** 20) < Fraction(845, 1000), 1 - W - Fraction(1, 10 ** 20) > Fraction(155, 1000)))
print("the rule 'largest of (p - 1) times the number of times p divides d': 3 ->", mu(3), "; 5, 9, 15, 45 ->", [mu(d) for d in (5, 9, 15, 45)], "; 7..945 ->", sorted(d for d in range(3, 1000, 2) if mu(d) == 6))
c = lambda k: Fraction(math.comb(k, k // 2), 2 ** k)
print("chance of as many pluses as minuses, two marks:", c(2), "; 1/2 + 0.845 > 1:", Fraction(1, 2) + Fraction(845, 1000) > 1)
print("twelve marks:", c(12) + sum(Fraction(A(t) - A(t - 2), 2 ** t) for t in range(2, 12, 2)))

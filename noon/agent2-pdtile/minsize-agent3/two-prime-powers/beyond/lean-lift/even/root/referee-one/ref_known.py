# my counter against shares recorded in the earlier texts (as data): a validation of the counter, not of the texts
import ref_test as rt
from fractions import Fraction as Fr
def ms(lst):
    d = {}
    for b in lst:
        d[b] = d.get(b, 0) + 1
    return d
cases = [(105, [0, 3, 9, 12, 32, 36, 97], Fr(7, 32)),
         (45, [5, 5, 22, 22, 26, 26, 27, 27, 29, 29, 38, 38], Fr(539, 2048)),
         (225, [19, 19, 22, 22, 36, 36, 110, 110, 133, 133], Fr(73, 256)),
         (675, [17, 17, 66, 66, 106, 106, 384, 384, 558, 558, 665, 665], Fr(269, 1024)),
         (15, [6, 8, 9, 10, 12], Fr(1, 4)),
         (15, [0, 6, 12, 13, 14], Fr(1, 4))]
for n, lst, want in cases:
    s = rt.analyse(n, ms(lst))
    print(n, lst, "share", s, "recorded", want, "EQUAL" if s == want else "DIFFER")
print("failures of the lemma checks:", rt.ST["failures"])

# the 74 printed values of sqrt(m) B_E(m) in even_3000.out against mine, with and without the convention, digit by digit
import sys, re, math
import ref_bounds as rb
from ref_second import ConvCalc
cnt = rb.cnt_formula(61)
c = rb.c_float(3010)
A = rb.Calc(c, False); B = ConvCalc(c, False)
s2 = math.sqrt(2 / math.pi)
u2 = 31; x = 0.5783
tailprog = 2 * math.sqrt(2 * u2 + 1) * (u2 + 1) * x ** u2 / (1 - x * (1 + 1 / u2) ** 1.5)
n = 0; same_conv = 0; same_plain = 0; differ_plain = []; differ_conv = []
for line in open(sys.argv[1]):
    mm = re.match(r"m =\s*(\d+)\s+level 0.*sqrt\(m\) B_E\(m\) = ([0-9.]+)", line)
    if not mm:
        continue
    m = int(mm.group(1)); printed = mm.group(2)
    n += 1
    vals = []
    for calc in (A, B):
        calc.memo = {}
        l0, comp, pp3, ppo, tail = rb.BE_parts(calc, m, cnt, False)
        if m > 61:
            tail = s2 / math.sqrt(m) * tailprog          # the program's tail constant
        vals.append("%.5f" % ((l0 + comp + pp3 + ppo + tail) * math.sqrt(m)))
    if vals[0] == printed: same_plain += 1
    else: differ_plain.append(m)
    if vals[1] == printed: same_conv += 1
    else: differ_conv.append(m)
print("%d printed values of sqrt(m) B_E(m); equal to mine to the last printed digit: with the convention %d (differing at %s); as first written %d (differing at %s)" % (
    n, same_conv, differ_conv, same_plain, differ_plain))

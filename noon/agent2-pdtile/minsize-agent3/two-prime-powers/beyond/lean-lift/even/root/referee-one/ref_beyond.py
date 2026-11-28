# consistency of the analytic bounds for m > 3000 (Proposition 1; "even m > 3000") with computed values
import math
import ref_bounds as rb
cnt = rb.cnt_formula(61)
M = 40010
calc = rb.Calc(rb.c_float(M + 5), False)
s2 = math.sqrt(2 / math.pi)
f1 = math.sqrt(3000 / (3000 - 40))
worst = 0.0
for m in list(range(3000, 3041)) + [3500, 4000, 5000, 7001, 10000, 20001, 40000]:
    for N in range(3, 22):
        q = math.sqrt(m) * calc.gamma(m, N) / s2
        worst = max(worst, q)
        if q > f1:
            print("Proposition 1 FAILS at", m, N, q, f1)
    calc.memo = {}
print("Proposition 1: largest sqrt(m) gamma(m,N)/sqrt(2/pi) met for m >= 3000, 3 <= N <= 21: %.6f  (f1 = %.6f)" % (worst, f1))
for m in (3001, 3002, 3501, 3502, 5001, 5002, 10001, 10002, 20001, 20002, 40001, 40002):
    calc.memo = {}
    b = rb.B(calc, m, cnt, False) * math.sqrt(m)
    if m % 2:
        b3 = rb.B3_odd(calc, m, cnt, False) * math.sqrt(m)
        print("m = %5d  sqrt(m) B = %.5f (analytic bound for m > 3000: 0.9590)  sqrt(m) B3 = %.5f" % (m, b, b3))
    else:
        be = sum(rb.BE_parts(calc, m, cnt, False)) * math.sqrt(m)
        print("m = %5d  sqrt(m) B = %.5f (analytic: 1.7569)  sqrt(m) B_E = %.5f (analytic: 1.4215)" % (m, b, be))
print("limits claimed: odd %.5f, even without parity %.5f, even %.5f" % (s2 * 1.191951, s2 * 2.191951, 1.26986))

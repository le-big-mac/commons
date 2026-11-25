"""test.py: the equations of puck.py against values worked by hand and against the equation stepped forward.
    python3 -I test.py"""
import math, os, sys
sys.path.insert(0, os.environ.get('PUCK_CODE', os.path.dirname(os.path.abspath(__file__))))
import puck
bad = 0; n = 0
def check(ok, what):
    global bad, n
    n += 1; bad += not ok; print('%s  %s' % ('ok    ' if ok else 'FAILED', what))
check(abs(puck.ratio(60) - 2) < 1e-12 and abs(puck.ratio(45) - math.sqrt(2)) < 1e-12 and puck.ratio(0) == 1 and puck.ratio(90) == math.inf, 'the path at a sixth of a turn is twice the straight line, at an eighth root two, straight at none, endless at a quarter')
d, length, big, t_e = puck.simulate(60, k=1.0, T=30)
check(abs(length / (1 - d) - 2) < 0.01, 'stepped forward at a sixth of a turn, the path is twice the distance closed: %.4f' % (length / (1 - d)))
check(abs(t_e - 2.0) < 0.01, 'and the distance falls to 1/e in 1/(k cos a) = 2 seconds: %.3f' % t_e)
d, length, big, t_e = puck.simulate(45, k=1.0, T=2 * math.pi / math.sin(math.radians(45)))
check(abs(d / math.exp(-2 * math.pi) - 1) < 0.02, 'at an eighth of a turn, in the time of one swing round the dot (2 pi / (k sin a)) the distance falls to exp(-2 pi): %.5f against %.5f' % (d, math.exp(-2 * math.pi)))
d, length, big, t_e = puck.simulate(90, k=1.0, T=20)
check(0.99 < d < 1.03 and length > 19.9, 'at a quarter turn it goes round at the distance it began: %.3f, path %.1f' % (d, length))
d, length, big, t_e = puck.simulate(135, k=1.0, T=10)
check(abs(d / math.exp(10 * math.cos(math.radians(45))) - 1) < 0.02, 'at three eighths it runs away as exp(k t cos(a - quarter turn...)): %.1f against %.1f' % (d, math.exp(10 * math.cos(math.radians(45)))))
# the delay: by hand, at a twelfth of a turn and k = 5 the limit is (pi/2 - pi/6)/5 = pi/15 = 0.2094 s; with no turn, pi/10 = 0.3142 s
check(abs(puck.limit_delay(30, 5) - math.pi / 15) < 1e-12 and abs(puck.limit_delay(0, 5) - math.pi / 10) < 1e-12 and puck.limit_delay(90, 5) == 0, 'the delay a chaser can bear: pi/15 s at a twelfth of a turn, pi/10 s at none, none at a quarter (k = 5)')
for deg, lo, hi in ((30, 0.19, 0.23), (0, 0.30, 0.33), (60, 0.09, 0.12)):
    a = puck.simulate(deg, k=5.0, tau=lo, T=60)[0]; b = puck.simulate(deg, k=5.0, tau=hi, T=60)[0]
    check(a < 0.05 and b > 20 and lo < puck.limit_delay(deg, 5) < hi, 'stepped forward at %d degrees, k = 5: a delay of %.2f s dies away (%.2g) and %.2f s grows (%.2g); the limit by the equation is %.4f s' % (deg, lo, a, hi, b, puck.limit_delay(deg, 5)))
check(abs(puck.limit_step(60) - 1) < 1e-12 and abs(puck.limit_step(0) - 2) < 1e-12, 'in steps: a share under 1 of the distance is steady at a sixth of a turn, under 2 at none')
# the stepped hand's path: by hand, with no turn any share g gives 1; at a sixth of a turn and g = 1/2, r = sqrt(3)/2 and the path is 0.5 / (1 - 0.8660) = 3.732
a = puck.step_run(60, 0.5); b = puck.step_run(45, 0.05); c = puck.step_run(60, 1.02)
check(abs(puck.step_ratio(0, 0.3) - 1) < 1e-12 and abs(puck.step_ratio(60, 0.5) - 0.5 / (1 - math.sqrt(3) / 2)) < 1e-12 and abs(a[1] - 3.7320508) < 1e-5 and abs(b[1] - puck.step_ratio(45, 0.05)) < 1e-6 and c[0] > 1e6 and puck.step_ratio(60, 1.02) == math.inf, 'in steps the path is g / (1 - r) times the distance closed: 3.732 at a sixth of a turn with half-steps (run: %.4f), %.4f at an eighth with twentieths (run: %.4f); past g = 2 cos a it grows' % (a[1], puck.step_ratio(45, 0.05), b[1]))
print('%d of %d tests pass' % (n - bad, n)); sys.exit(1 if bad else 0)

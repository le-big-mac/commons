"""The machine's rule, the three games of the picture, and what a player who always defects earns: worked out afresh.
usage: steps.py /srv/commons/welch/src      (reads ipd.py there for the exact payoffs with slips; writes nothing there)"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
from fractions import Fraction as F
import numpy as np
import ipd

PAY = {('C', 'C'): (3, 3), ('C', 'D'): (0, 5), ('D', 'C'): (5, 0), ('D', 'D'): (1, 1)}
# (start, [(move, next if the other cooperated, next if the other defected)]), from the table in the working note (README.md lines 176-178)
HAND = (0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)])
SHIFTY = (1, HAND[1]); WOOER = (2, HAND[1])      # the same three states begun at the second and at the cooperating one
ALLD = (0, [('D', 0, 0)]); ALLC = (0, [('C', 0, 0)]); TFT2 = (0, [('D', 0, 1), ('C', 1, 0)])
TFT = (0, [('C', 0, 1), ('D', 0, 1)])


def play(a, b, rounds, slip=None):
    sa, sb = a[0], b[0]; ra, rb = [], []
    for r in range(1, rounds + 1):
        ma, mb = a[1][sa][0], b[1][sb][0]
        if slip == (r, 0): ma = 'D' if ma == 'C' else 'C'
        if slip == (r, 1): mb = 'D' if mb == 'C' else 'C'
        ra.append(ma); rb.append(mb)
        sa = a[1][sa][1 if mb == 'C' else 2]; sb = b[1][sb][1 if ma == 'C' else 2]
    return ''.join(ra), ''.join(rb)


def earn(ra, rb):
    return sum(PAY[(x, y)][0] for x, y in zip(ra, rb)), sum(PAY[(x, y)][1] for x, y in zip(ra, rb))


print('== 1. the rule against the table ==')
# "defects until the other side has defected twice in a row; then cooperates for as long as they do; a defection from them sends it back to the start"
import itertools
bad = 0
for n in range(1, 13):
    for other in itertools.product('CD', repeat=n):
        s = 0; run = 0; coop = False; ok = True
        for r, o in enumerate(other):
            move = HAND[1][s][0]
            # the rule in words: the machine cooperates this round exactly when, since it last began again, the other has defected twice in a row and not defected since
            want = 'C' if coop else 'D'
            if move != want: ok = False
            if coop:
                if o == 'D': coop = False; run = 0          # back to the start
            else:
                run = run + 1 if o == 'D' else 0
                if run == 2: coop = True
            s = HAND[1][s][1 if o == 'C' else 2]
        bad += (not ok)
print('every sequence of the other side\'s moves up to 12 rounds: the table and the rule in words disagree in', bad, 'cases')

print()
print('== 2. the three games of the picture (14 rounds, as handshake_strip_phone.py) ==')
g1 = play(HAND, HAND, 14, slip=(8, 0)); g2 = play(HAND, ALLC, 14); g3 = play(HAND, ALLD, 14); g4 = play(TFT2, ALLD, 14)
for name, g in (('two of the machines, slip by the first in round 8', g1), ('machine / always cooperates', g2), ('machine / always defects', g3), ('older machine / always defects', g4)):
    print(f'{name:52s} {g[0]} | {g[1]}   points {earn(*g)}')
print('third game: rounds in which the machine cooperates:', [i + 1 for i, m in enumerate(g3[0]) if m == 'C'])
print('first game: rounds after the slip in which both cooperate again from:', next(r for r in range(9, 15) if g1[0][r - 1:] == 'C' * (15 - r) and g1[1][r - 1:] == 'C' * (15 - r)))

print()
print('== 3. what a round is worth with no slips (long run, exact fractions over a whole cycle) ==')
def longrun(a, b, cycle, skip=60):
    ra, rb = play(a, b, skip + cycle)
    ea, eb = earn(ra[skip:], rb[skip:])
    return F(ea, cycle), F(eb, cycle)
for name, a, b in (('always-defects against the machine', ALLD, HAND), ('machine against machine', HAND, HAND), ('always-defects against always-defects', ALLD, ALLD),
                   ('always-defects against the one-defection machine', ALLD, TFT2), ('always-cooperates against the machine', ALLC, HAND),
                   ('always-defects against the machine begun at its 2nd state', ALLD, SHIFTY), ('always-defects against the machine begun at its cooperating state', ALLD, WOOER)):
    x, y = longrun(a, b, 6)
    print(f'{name:66s} first player {str(x):>5s} = {float(x):.3f} a round; second player {str(y):>5s} = {float(y):.3f}')

print()
print('== 4. with slips, exact (ipd.payoff): per round, games of 100 rounds on average (continuation 0.99) and 50 (0.98) ==')
H = ipd.M('handshake', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)])
AD = ipd.M('ALLD', 0, [('D', 0, 0)])
print(' slips  cont. | machine v machine | defector v machine | machine v defector | defector v defector | share of machines above which the machine earns more')
for delta in (0.99, 0.98):
    for eps in (0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.10):
        hh = ipd.payoff(H, H, eps, delta)[0]; dh, hd = ipd.payoff(AD, H, eps, delta); dd = ipd.payoff(AD, AD, eps, delta)[0]
        # machine earns x*hh + (1-x)*hd ; defector earns x*dh + (1-x)*dd
        den = (hh - dh) + (dd - hd)
        x = (dd - hd) / den if den > 0 else float('nan')
        print(f' {eps:5.3f}  {delta:.2f}  |      {hh:.3f}        |       {dh:.3f}        |       {hd:.3f}        |        {dd:.3f}        |  {100 * x:.0f}%')
print()
print('one machine among 99 defectors, as the live page opens (3% slips, continuation 0.98), each meeting the 99 others:')
eps, delta = 0.03, 0.98
hh = ipd.payoff(H, H, eps, delta)[0]; dh, hd = ipd.payoff(AD, H, eps, delta); dd = ipd.payoff(AD, AD, eps, delta)[0]
print(f'   the machine earns {hd:.3f} a round; each defector earns {(98 * dd + dh) / 99:.3f}')

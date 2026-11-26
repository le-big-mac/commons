"""Step the machines of the page by hand (my own stepping, not the figure script's) and work out the sums the story states.
usage: machines_check.py     (imports the study's exact payoff routine from /srv/commons/welch/src for the sums with slips)"""
import sys
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import payoff, M
# a machine here: start state, then per state (move, next if the other cooperated, next if the other defected)
HAND = (0, {0: ('D', 0, 1), 1: ('D', 0, 2), 2: ('C', 2, 0)})
T4T = (0, {0: ('D', 0, 1), 1: ('C', 1, 0)})
ALLC = (0, {0: ('C', 0, 0)}); ALLD = (0, {0: ('D', 0, 0)})
PTS = {('C', 'C'): (3, 3), ('C', 'D'): (0, 5), ('D', 'C'): (5, 0), ('D', 'D'): (1, 1)}
def game(a, b, n, slip=None):
    sa, sb = a[0], b[0]; ra, rb = '', ''
    for r in range(1, n + 1):
        ma, mb = a[1][sa][0], b[1][sb][0]
        if slip == (r, 'a'): ma = 'CD'[ma == 'C']
        if slip == (r, 'b'): mb = 'CD'[mb == 'C']
        ra += ma; rb += mb
        sa = a[1][sa][1 if mb == 'C' else 2]; sb = b[1][sb][1 if ma == 'C' else 2]
    return ra, rb
def avg(ra, rb):
    n = len(ra); return sum(PTS[(x, y)][0] for x, y in zip(ra, rb)) / n, sum(PTS[(x, y)][1] for x, y in zip(ra, rb)) / n
print('1. The games of the strip, 14 rounds')
for name, a, b, slip in (('two of the machines, first slips in round 8', HAND, HAND, (8, 'a')), ('machine v always cooperates', HAND, ALLC, None),
                         ('machine v always defects', HAND, ALLD, None), ('older one-defection machine v always defects', T4T, ALLD, None)):
    ra, rb = game(a, b, 14, slip); print(f'   {name:48s} {ra} | {rb}')
ra, rb = game(HAND, HAND, 14, (8, 'a'))
back = next(r for r in range(9, 15) if ra[r - 1] == 'C' and rb[r - 1] == 'C')
print(f'   after the slip in round 8 both cooperate again in round {back}: rounds 9 to {back - 1} ({back - 9} rounds) are lost besides the slip itself')
for r in (3, 5, 9):   # a slip at other points
    ra, rb = game(HAND, HAND, 20, (r, 'b')); back = next(q for q in range(r + 1, 21) if ra[q - 1] == 'C' and rb[q - 1] == 'C' and all(x == 'C' for x in ra[q - 1:q + 2]))
    print(f'   slip in round {r} by the other player: {ra} | {rb}: both cooperating again from round {back}')
print('\n2. What a player who always defects earns, no slips, average points a round over 6,000 rounds')
for name, m in (('one-defection machine (Tat for Tit)', T4T), ('two-defection machine (this page)', HAND)):
    ra, rb = game(m, ALLD, 6000); pm, pd = avg(ra, rb); sa, sb = game(m, m, 6000); self_, _ = avg(sa, sb)
    print(f'   against the {name}: always-defect earns {pd:.4f}; the machine earns {pm:.4f} from it; two of the machines earn {self_:.4f} each; first six rounds for always-defect: {[PTS[(x, y)][1] for x, y in zip(ra[:6], rb[:6])]}')
print('\n3. The same with the study\'s exact routine (normalised, game ends after each round with chance 1 - delta)')
hand = M('h', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)]); t4t = M('t', 0, [('D', 0, 1), ('C', 1, 0)])
alld = M('d', 0, [('D', 0, 0)]); allc = M('c', 0, [('C', 0, 0)]); tft = M('tft', 0, [('C', 0, 1), ('C', 0, 1)])
tft = M('tft', 0, [('C', 0, 1), ('D', 0, 1)]); grim = M('grim', 0, [('C', 0, 1), ('D', 1, 1)])
for eps, delta in ((0.0, 0.99), (0.0, 0.98), (0.03, 0.98), (0.02, 0.99), (0.05, 0.99)):
    print(f'   slips {eps}, delta {delta}: one-defection machine: itself {payoff(t4t, t4t, eps, delta)[0]:.4f}, always-defect against it {payoff(alld, t4t, eps, delta)[0]:.4f} | '
          f'this machine: itself {payoff(hand, hand, eps, delta)[0]:.4f}, always-defect against it {payoff(alld, hand, eps, delta)[0]:.4f}, always-cooperate against it {payoff(allc, hand, eps, delta)[0]:.4f}')
print('\n4. "among defectors a single machine of this kind does worse than they do": one machine among 99 always-defectors')
for eps, delta in ((0.03, 0.98), (0.05, 0.99), (0.02, 0.99), (0.01, 0.99)):
    hd = payoff(hand, alld, eps, delta); dd = payoff(alld, alld, eps, delta)[0]; hh = payoff(hand, hand, eps, delta)[0]
    lone = (99 * hd[0] + 1 * hh) / 100          # the page's beds score each machine against the whole bed, itself included
    defector = (99 * dd + 1 * hd[1]) / 100
    # share x of the bed at which the machine does as well as the defectors: x*hh + (1-x)*hd0 = x*hd1 + (1-x)*dd
    x = (dd - hd[0]) / ((hh - hd[1]) + (dd - hd[0]))
    print(f'   slips {eps}, delta {delta}: the machine earns {hd[0]:.3f} from a defector, a defector {dd:.3f} from a defector and {hd[1]:.3f} from the machine; lone machine averages {lone:.3f}, defectors {defector:.3f}; the machine does better once it is {100*x:.0f}% of the bed')
print('\n5. "In a world of plain reciprocators ... players who simply always cooperate do just as well"')
for eps, delta in ((0.0, 0.99), (0.01, 0.99), (0.02, 0.99), (0.03, 0.98)):
    print(f'   slips {eps}, delta {delta}: tit-for-tat among tit-for-tat {payoff(tft, tft, eps, delta)[0]:.4f}; always-cooperate among tit-for-tat {payoff(allc, tft, eps, delta)[0]:.4f}; '
          f'grim among grim {payoff(grim, grim, eps, delta)[0]:.4f}; always-cooperate among grim {payoff(allc, grim, eps, delta)[0]:.4f}; always-defect against always-cooperate {payoff(alld, allc, eps, delta)[0]:.4f}')

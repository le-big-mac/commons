"""The Antikythera mechanism as a set of ratios: turns of each output per turn of the main drive wheel b1,
which carries the mean Sun once round the zodiac.

Sources (read on 23 Nov 2026):
- Moon, 254/19, and the line of apsides, (9 x 53)/(19 x 223): Freeth & Jones 2012, ISAW Papers 4, section 2.4.3
  ("254/19 rotations per year"; "(9 x 53)/(19 x 223)").
- Phase of the Moon: 235 months in 19 years (the Metonic cycle), the difference of Moon and Sun: 254/19 - 1.
- Saros dial: 223 months in four turns.
- Planets: synodic cycles per year, Freeth et al. 2021, Sci. Rep. 11:5821, Fig. 2e (read from the figure):
  Mercury (1513, 480), Venus (289, 462), Mars (133, 284), Jupiter (315, 344), Saturn (427, 442).
  Venus and Saturn are from the front cover inscription; the other three are that paper's restoration.
- Line of nodes: -5/93 (same paper as corrected, gear train 49~62+64~48 of its Fig. 5); the paper calls this
  hand hypothetical."""
from fractions import Fraction as F

MOON = F(254, 19)
APSIDES = F(9 * 53, 19 * 223)
ANOMALY = MOON - APSIDES
PHASE = MOON - 1
assert PHASE == F(235, 19)
NODE = 1 - F(49, 62) * F(64, 48)
assert NODE == F(-5, 93)
SYNODIC = {'mercury': F(1513, 480), 'venus': F(289, 462), 'mars': F(133, 284), 'jupiter': F(315, 344),
           'saturn': F(427, 442)}
INFERIOR = ('mercury', 'venus')
SUPERIOR = ('mars', 'jupiter', 'saturn')
# the trains printed in the 2021 paper's Fig. 5 caption give the same ratios
assert F(51, 44) * F(34, 63) == SYNODIC['venus'] and F(51, 72) * F(89, 20) == SYNODIC['mercury']
# what the paper prints as the error of each relation, degrees per year (its Fig. 2e, column "Error e_y")
PAPER_EY = {'mercury': -0.005022, 'venus': 0.008576, 'mars': 0.003089, 'jupiter': 0.000802, 'saturn': 0.004208}

if __name__ == '__main__':
    print('turns per turn of b1:')
    for k, v in (('Moon', MOON), ('line of apsides', APSIDES), ('anomaly', ANOMALY), ('phase', PHASE), ('node', NODE)):
        print(f'  {k:16s} {str(v):>12s} = {float(v):.7f}')
    for p, v in SYNODIC.items():
        d = (1 - v) if p in SUPERIOR else None
        print(f'  {p:16s} {str(v):>12s} = {float(v):.7f} synodic cycles' + (f'; deferent {str(d)} = {float(d):.7f}' if d else ''))

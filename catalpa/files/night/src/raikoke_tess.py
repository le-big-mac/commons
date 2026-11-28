# Beside the sixteenth sheet, for the record: the first make's own readings (not the fading) around the eruption of
# Raikoke, by my reduction (cache2/years.pkl and cache2/depth.pkl, the ninth sheet's function), in the same form as
# src/sqm_north.py prints for the second make: the month less the same month a year before, magnitudes, positive
# for a darker reading. One unit per place (the chip of most of its months in 2021).
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
R = dict(pickle.load(open(B + 'cache2/depth.pkl', 'rb'))); R.update(pickle.load(open(B + 'cache2/years.pkl', 'rb')))
def readings(st, dp):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and y == 2021 and r is not None and DP.monthfig(r, dp) is not None: chips[(r.get('mac') or '')[-8:]] = chips.get((r.get('mac') or '')[-8:], 0) + 1
    if not chips: return {}
    ch = max(chips, key=chips.get)
    return {(y, m): DP.monthfig(r, dp) for (s, y, m), r in R.items() if s == st and r is not None and (r.get('mac') or '')[-8:] == ch and DP.monthfig(r, dp) is not None}
LATE = (8, 9, 10, 11, 12); EARLY = (1, 2, 3, 4, 5, 6); f = lambda v: '    . ' if v is None else f'{v:+6.2f}'
def middle(v): v = [x for x in v if x is not None]; return f'{np.median(v):+.3f} ({len(v)})' if v else 'none'
for dp in (3.0, 5.0, 7.0):
    V = {st: readings(st, dp) for st in DP.NORTH + list(DP.SOUTH)}
    def diff(st, y1, y0, months):
        d = [V[st][(y1, m)] - V[st][(y0, m)] for m in months if (y1, m) in V[st] and (y0, m) in V[st]]; return float(np.mean(d)) if len(d) >= 3 else None
    print(f'the first make, the reading itself with the Sun {dp:g} degrees down (magnitudes; positive: the later year reads darker)')
    print('   northern place: late 2019 less late 2018, early 2019 less early 2018, their difference, late 2020 less late 2019')
    rows = {}
    for st in DP.NORTH:
        a, b = diff(st, 2019, 2018, LATE), diff(st, 2019, 2018, EARLY); rows[st] = [a, b, (a - b) if a is not None and b is not None else None, diff(st, 2020, 2019, LATE)]
        if any(x is not None for x in rows[st]): print(f'   {st:<10} ' + ' '.join(f(x) for x in rows[st]))
    print('   the middle: ' + '; '.join(middle([rows[st][i] for st in DP.NORTH]) for i in range(4)))
    print('   month by month, the middle over places (three or more) of the month less the same month a year before, hundredths; places after the bar:')
    for name, sts in (('north', DP.NORTH), ('south', list(DP.SOUTH))):
        for y in range(2017, 2027):
            v = [[V[st][(y, m)] - V[st][(y - 1, m)] for st in sts if (y, m) in V[st] and (y - 1, m) in V[st]] for m in range(1, 13)]
            if any(len(x) >= 3 for x in v): print(f'   {name} {y} less {y - 1}: ' + ' '.join(f'{100 * np.median(x):+4.0f}' if len(x) >= 3 else '   .' for x in v) + '   | ' + ' '.join(f'{len(x):2d}' for x in v))

"""The 2021 paper's printed errors (Fig. 2e, read by eye from the rendered page): what definition fits?"""
from fractions import Fraction as F
REL = dict(mercury=(1513, 480), venus=(289, 462), mars=(133, 284), jupiter=(315, 344), saturn=(427, 442))
EY = dict(mercury=-0.005022, venus=0.008576, mars=0.003089, jupiter=0.000802, saturn=0.004208)
ES = dict(mercury=-0.001593, venus=0.013710, mars=0.006596, jupiter=0.000876, saturn=0.004509)
INF = ('mercury', 'venus')
print('1. the two printed columns: e_s / e_y beside years per synodic cycle (y/n) and (y/n)^2')
for p, (n, y) in REL.items():
    print(f'   {p:8s} e_s/e_y {ES[p]/EY[p]:.5f}   y/n {y/n:.5f}   (y/n)^2 {(y/n)**2:.5f}   e_y*(y/n) {EY[p]*y/n:.6f}  printed e_s {ES[p]:.6f}   e_s/(y/n) {ES[p]*n/y:.6f}')
# JPL Table 2a rates as typed in after.py (deg per Julian century)
LR = {'mercury': 149472.67486623, 'venus': 58517.81560260, 'earth': 35999.37306329, 'mars': 19140.29934243, 'jupiter': 3034.90371757, 'saturn': 1222.11494724}
print('2. after.py part A redone: synodic cycles per sidereal year from the rates; error of the gears deg per Julian year')
for p, (n, y) in REL.items():
    s = (LR[p] - LR['earth']) / LR['earth'] if p in INF else (LR['earth'] - LR[p]) / LR['earth']
    e = 360 * (n / y - s) * LR['earth'] / 36000
    print(f'   {p:8s} sky {s:.8f} gears {n/y:.8f}  error {e:+.6f}  /printed {abs(e)/abs(EY[p]):.3f}   (per sidereal year {360*(n/y-s):+.6f}); sidereal period {36000*365.25/LR[p]:.5f} d; synodic period {36000*365.25/abs(LR[p]-LR["earth"]):.5f} d')
print(f'   sidereal year from the rate: {36000*365.25/LR["earth"]:.6f} d')
print('3. if e_y = 360 (n/y - s_true): the "true" synodic period implied by the printed e_y, in days, for several lengths of year')
for Yn, Y in (('sidereal 365.256363', 365.256363), ('tropical 365.242190', 365.24219), ('Julian 365.25', 365.25), ('365.256', 365.256)):
    row = []
    for p, (n, y) in REL.items():
        s = n / y - EY[p] / 360
        row.append(f'{p} {Y/s:.4f}')
    print(f'   {Yn:20s} ' + '  '.join(row))
print('   modern mean synodic periods (from the Table 2a rates): ' + '  '.join(f'{p} {36000*365.25/abs(LR[p]-LR["earth"]):.4f}' for p in REL))
print('   Saturn if its e_y were 0.004356 (= printed e_s x 427/442): ' + f'{365.256363/(427/442-0.004356/360):.4f}')
print('4. the sidereal period (days) each printed error implies, year 365.256363:')
for p, (n, y) in REL.items():
    s = n / y - EY[p] / 360
    P = 365.256363 / (s + 1) if p in INF else 365.256363 / (1 - s)
    print(f'   {p:8s} {P:.5f}   (modern {36000*365.25/LR[p]:.5f})')
print('5. hand check of the sheet: Mercury with 87.9691 d and 365.256363: ', end='')
s = 365.256363 / 87.9691 - 1; print(f'{360*(1513/480 - s):+.6f} deg per sidereal year; x 2230.49 = {360*(1513/480 - s)*2230.49:+.2f} deg;  with 87.96926: {360*(1513/480 - (365.256363/87.96926-1))*2230.49:+.2f}')
print('6. candidates for Mars: synodic 779.94 and 779.96 d with the sidereal year: ', end='')
for P in (779.94, 779.96, 779.9361):
    print(f'{P}: {360*(133/284 - 365.256363/P):+.6f}', end='; ')
print()

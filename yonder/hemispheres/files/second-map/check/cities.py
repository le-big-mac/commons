"""Where named cities lie relative to the edges of the two halves (signed distance in degrees of arc and km; + = inside),
and where each grid's most populous 0.05-degree cells are (to see whether any freak value sits in a sliver).
City coordinates are typed from the checker's memory, to a hundredth of a degree; they are only labels.
usage: python -I cities.py NAME=GRID.npy ..."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chk

B = chk.unit(52.37, 12.68); V = chk.unit(46.0, 7.18)
CITIES = [('Manila', 14.60, 120.98), ('Quezon City', 14.68, 121.04), ('Cebu', 10.32, 123.89), ('Davao', 7.07, 125.61), ('Legazpi (south Luzon)', 13.14, 123.74),
          ('Singapore', 1.35, 103.82), ('Johor Bahru', 1.49, 103.74), ('Batam', 1.08, 104.03), ('Kuala Lumpur', 3.14, 101.69), ('George Town', 5.41, 100.33),
          ('Medan', 3.59, 98.67), ('Pekanbaru', 0.51, 101.45), ('Padang', -0.95, 100.35), ('Palembang', -2.98, 104.75), ('Jakarta', -6.2, 106.85),
          ('Kuching', 1.55, 110.35), ('Bangkok', 13.75, 100.5), ('Ho Chi Minh City', 10.82, 106.63), ('Hat Yai', 7.01, 100.47),
          ('Rio de Janeiro', -22.91, -43.17), ('Sao Paulo', -23.55, -46.63), ('Campinas', -22.91, -47.06), ('Belo Horizonte', -19.92, -43.94),
          ('Ribeirao Preto', -21.18, -47.81), ('Curitiba', -25.43, -49.27), ('Porto Alegre', -30.03, -51.23), ('Brasilia', -15.79, -47.88),
          ('Vitoria', -20.32, -40.34), ('Quito', -0.18, -78.47), ('Guayaquil', -2.19, -79.89), ('Lima', -12.05, -77.04), ('Iquitos', -3.75, -73.25),
          ('Cali', 3.45, -76.53), ('Pasto', 1.21, -77.28), ('Santa Cruz de la Sierra', -17.78, -63.18), ('La Paz', -16.5, -68.15), ('Asuncion', -25.26, -57.58),
          ('Acapulco', 16.86, -99.88), ('Honolulu', 21.31, -157.86), ('Naha (Okinawa)', 26.21, 127.68)]
print('city | lat lon | distance from the edge of the Berlin half (deg, km; + inside) | of the Valais half')
for nm, la, lo in CITIES:
    u = chk.unit(la, lo)
    db = float(np.degrees(np.arcsin(u @ B))); dv = float(np.degrees(np.arcsin(u @ V)))
    tag = 'in both' if db > 0 and dv > 0 else 'only Berlin half' if db > 0 else 'only Valais half' if dv > 0 else 'in neither'
    print(f'{nm:26s} {la:7.2f} {lo:8.2f} | {db:+6.2f} deg {db * 111.19:+7.0f} km | {dv:+6.2f} deg {dv * 111.19:+7.0f} km | {tag}')

inB = chk.mask_dot(52.37, 12.68); inV = chk.mask_dot(46.0, 7.18)
for spec in sys.argv[1:]:
    name, path = spec.split('=')
    P = np.load(path)
    idx = np.argsort(P.ravel())[::-1][:12]
    print(f'== {name}: the twelve most populous 0.05-degree cells')
    for k in idx:
        i, j = divmod(int(k), chk.W)
        tag = 'in both' if inB[i, j] and inV[i, j] else 'only Berlin half' if inB[i, j] else 'only Valais half' if inV[i, j] else 'in neither'
        print(f'     {P[i, j] / 1e6:6.3f} M at {chk.LAT[i]:7.3f} N {chk.LON[j]:8.3f} E  ({tag})')
    big = P > 1.5e6
    print(f'   cells above 1.5 million: {int(big.sum())}, holding {P[big].sum() / 1e6:.2f} M; of these only in the Berlin half {P[big & inB & ~inV].sum() / 1e6:.2f} M, only in the Valais half {P[big & inV & ~inB].sum() / 1e6:.2f} M')

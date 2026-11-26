# A reader for JPL's DE431 text files (ascpNNNNN.431): the geocentric Moon only.  The layout comes from the header (GROUP 1050): the Moon is item 10, starting at coefficient 441
# of each 32-day record, 13 Chebyshev coefficients for each of 3 components in each of 8 sub-intervals.  Positions in km, velocities in km per day, ICRF axes.
import numpy as np, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'de431') + '/'
START, NCO, NSUB, NCOEFF = 441, 13, 8, 1018
def load(names):
    """-> (jd0 array, jd1 array, coefficient array [record, sub-interval, component, coefficient]) for the records of the named files, in time order, duplicates dropped"""
    recs = {}
    for name in names:
        cache = D + name + '.moon.npy'
        if os.path.exists(cache): a = np.load(cache)
        else:
            vals = np.array(open(D + name).read().replace('D', 'E').split(), dtype=float)          # every record: its number, NCOEFF, then the 1018 values
            per = 2 + NCOEFF if len(vals) % (2 + NCOEFF) == 0 else 2 + 3 * ((NCOEFF + 2) // 3); assert len(vals) % per == 0, (len(vals), per)      # these files do not pad the last line of a record
            v = vals.reshape(-1, per); assert np.all(v[:, 1] == NCOEFF)
            a = np.hstack([v[:, 2:4], v[:, 2 + START - 1:2 + START - 1 + NCO * 3 * NSUB]]); np.save(cache, a)
        for r in a: recs[r[0]] = r
    a = np.array([recs[k] for k in sorted(recs)])
    return a[:, 0], a[:, 1], a[:, 2:].reshape(len(a), NSUB, 3, NCO)
def moon(jd, eph):
    """geocentric Moon at the times jd (array): positions (km) and velocities (km/day), shape (n, 3) each"""
    j0, j1, C = eph; jd = np.atleast_1d(np.asarray(jd, float)); i = np.clip(np.searchsorted(j0, jd, side='right') - 1, 0, len(j0) - 1)
    assert np.all((jd >= j0[i]) & (jd <= j1[i])), 'a time outside the files loaded'
    span = (j1[i] - j0[i]) / NSUB; s = np.minimum(((jd - j0[i]) / span).astype(int), NSUB - 1); x = 2 * (jd - (j0[i] + s * span)) / span - 1
    T = np.zeros((NCO, len(jd))); U = np.zeros((NCO, len(jd))); T[0] = 1; T[1] = x; U[1] = 1
    for k in range(2, NCO): T[k] = 2 * x * T[k - 1] - T[k - 2]; U[k] = 2 * x * U[k - 1] + 2 * T[k - 1] - U[k - 2]          # U holds dT/dx
    c = C[i, s]                                  # (n, 3, NCO)
    return np.einsum('nck,kn->nc', c, T), np.einsum('nck,kn->nc', c, U) * (2 / span)[:, None]
if __name__ == '__main__':
    # check against JPL's own test file: target 10 (Moon), centre 3 (Earth); coordinates 1-3 are positions in au, 4-6 velocities in au per day
    AU = 149597870.7; eph = load(sys.argv[1:] or ['ascm01000.431', 'ascp00000.431', 'ascp01000.431']); print('records', len(eph[0]), 'from JD', eph[0][0], 'to', eph[1][-1])
    n = 0; worst = [0, 0]
    for line in open(D + 'testpo.431'):
        p = line.split()
        if len(p) == 7 and p[0] == '431' and p[3] == '10' and p[4] == '3':
            jd = float(p[2])
            if eph[0][0] <= jd <= eph[1][-1]:
                r, v = moon([jd], eph); k = int(p[5]); mine = (r[0, k - 1] if k <= 3 else v[0, k - 4]) / AU; d = abs(mine - float(p[6])); n += 1; worst[k > 3] = max(worst[k > 3], d)
    print(f'{n} test values for the Moon about the Earth in this span; largest difference: position {worst[0]:.2e} au ({worst[0] * AU * 1000:.4f} m), velocity {worst[1]:.2e} au/day')

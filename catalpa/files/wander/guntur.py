# The same eclipse at Guntoor, India (Major Tennant's party): a test of whether the 10-second gap at Wha-Tonne is in my reduction.  Lines T1-T4 in ~/journal.md, written first.
# Tennant's times are local sidereal time; I compute the local apparent sidereal time of each contact from the same integration, the same clock correction and the same code as for Siam.
import sys, numpy as np, importlib.util
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('siam', '/home/agent1/wander/siam1868.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
JPL = -2.5 / 86400.0
def last(jd_tt, lon_d):
    """local apparent sidereal time (fraction of a day): the hour angle of the true equinox of date, taken as the node of the Earth-Moon barycentre's orbit plane on the true equator"""
    xg, yg, p, cio, era = m.frame(jd_tt)
    GMS, GME, GMM = 132712440041.279419, 398600.435507, 4902.800118
    def emb(t):
        e, mo, s = m.st(m.E, t), m.st(m.M, t), m.st(m.S, t); return (GME * e + GMM * mo) / (GME + GMM) - s
    r = emb(jd_tt); v = (emb(jd_tt + 0.01) - emb(jd_tt - 0.01)) / 0.02; ecl = np.cross(r, v); ecl /= np.linalg.norm(ecl)
    g = np.cross(p, ecl); g /= np.linalg.norm(g); ra_g = np.arctan2(g @ np.cross(p, cio), g @ cio)          # the equinox, measured from the non-rotating origin
    return ((era + np.radians(lon_d) - ra_g) / (2 * np.pi)) % 1.0, np.degrees(np.arccos(p @ ecl))
hms = m.hms
OBS = {'c1': [('Tennant', 6, 2, 12.66), ('Branfill', 6, 2, 37.86)], 'c4': [('Tennant', 8, 47, 24.62), ('Branfill, limb a perfect curve', 8, 47, 22.9), ('Branfill, the two mountains gone', 8, 47, 31.5)]}
PH = (('first photograph', 7, 17, 1.9), ('last photograph', 7, 22, 34.8))
for name, la, lo in (('Guntoor: the survey latitude, the survey longitude moved 28" east (80d27\'08" E)', 16 + 17 / 60 + 34.3 / 3600, 80 + 27 / 60 + 8 / 3600),
                     ('the survey longitude as Tennant gives it (5h21m46.65s = 80d26\'40" E)', 16 + 17 / 60 + 34.3 / 3600, (5 + 21 / 60 + 46.65 / 3600) * 15),
                     ("Hind's position (80d27'15\" E, 16d17'29\" N)", 16 + 17 / 60 + 29 / 3600, 80 + 27 / 60 + 15 / 3600)):
    xyz = m.site(la, lo, 30.0); print(name)
    for k, kn in ((m.K_IAU, 'standard lunar radius'), (m.K_SMALL, 'smaller lunar radius')):
        c = m.contacts(xyz, k); row = []
        for key in ('c1', 'c2', 'c3', 'c4'):
            t = c[key] + JPL; ls, eps = last(t, lo); ut = t - m.DT + 0.5; row.append((key, ls, ut))
        print(f'   {kn:22s} ' + '  '.join(f'{key} LST {hms(ls)} (UT {hms(ut)})' for key, ls, ut in row) + f'   totality {(c["c3"] - c["c2"]) * 86400:.1f} s; obliquity used {eps:.4f}')
        if k == m.K_IAU:
            d = {key: ls for key, ls, ut in row}
            for key in ('c1', 'c4'):
                for who, h, mi, s in OBS[key]: print(f'        {key}: observed by {who} {h}h{mi:02d}m{s:05.2f}s; observed minus computed {((h * 3600 + mi * 60 + s) - d[key] * 86400):+.1f} s')
            for who, h, mi, s in PH: print(f'        {who} {h}h{mi:02d}m{s:04.1f}s: {((h * 3600 + mi * 60 + s) - d["c2"] * 86400):+.1f} s after my start of totality, {(d["c3"] * 86400 - (h * 3600 + mi * 60 + s)):+.1f} s before my end')
# a check of the sidereal-time routine at J2000-ish: Greenwich apparent sidereal time on 2000 Jan 1 12:00 TT should be about 18h41m50s
print('check: my sidereal time at Greenwich at the last epoch on file, for comparison with a standard formula: ', hms(last(m.JD[-1], 0.0)[0]), ' JD', m.JD[-1])
T = (m.JD[-1] - m.DT - 2451545.0) / 36525.0; gmst = (280.46061837 + 360.98564736629 * (m.JD[-1] - m.DT - 2451545.0) + 0.000387933 * T * T) % 360.0; print('   standard formula for mean sidereal time at that instant:', hms(gmst / 360.0), '(apparent differs from mean by up to 1.2 s)')

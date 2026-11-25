# One clock correction for both stations?  The eclipse of 18 Aug 1868 was seen about 10 s earlier than my computation at Wha-Tonne (Siam) and at Guntoor (India).
# Here the same computation is repeated with the clock correction TT - UT set to other values, to see what single value, if any, fits the observations at both places.
# A look, not a sealed test.  JPL's Moon (2.5 s ahead of my model's) is used throughout.
import sys, numpy as np, importlib.util
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('siam', '/home/agent1/wander/siam1868.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
spec2 = importlib.util.spec_from_file_location('gun', '/home/agent1/wander/guntur.py')
JPL = -2.5 / 86400.0
def last(jd_tt, lon_d):
    xg, yg, p, cio, era = m.frame(jd_tt); GME, GMM = 398600.435507, 4902.800118
    emb = lambda t: (GME * m.st(m.E, t) + GMM * m.st(m.M, t)) / (GME + GMM) - m.st(m.S, t)
    r = emb(jd_tt); v = (emb(jd_tt + 0.01) - emb(jd_tt - 0.01)) / 0.02; ecl = np.cross(r, v); ecl /= np.linalg.norm(ecl); g = np.cross(p, ecl); g /= np.linalg.norm(g)
    return ((era + np.radians(lon_d) - np.arctan2(g @ np.cross(p, cio), g @ cio)) / (2 * np.pi)) % 1.0
sec = lambda h, mi, s: h * 3600 + mi * 60 + s
WT = (11.7214, 99.7588); GU = (16 + 17 / 60 + 34.3 / 3600, 80 + 27 / 60 + 8 / 3600)
print('clock correction   Wha-Tonne (memorial), local mean time, observed minus computed          Guntoor (survey position, modern Madras), local sidereal time, observed minus computed')
print('  TT - UT (s)      darkness begins (Tisserand)   darkness ends (Tisserand)      first contact (Tennant)   first plate, 1 s before darkness   last contact (Tennant / Branfill last trace)')
for dt in (2.3, 4.15, 6.0, 7.0, 8.0, 8.5, 9.0, 10.0):
    m.DT = dt / 86400.0
    c = m.contacts(m.site(*WT), m.K_SMALL); f = lambda key: ((c[key] + JPL - m.DT + 0.5 + WT[1] / 360.0) % 1.0) * 86400
    w2, w3 = sec(11, 39, 23.1) - f('c2'), sec(11, 46, 9.1) - f('c3')
    g = m.contacts(m.site(GU[0], GU[1], 30.0), m.K_SMALL); gi = m.contacts(m.site(GU[0], GU[1], 30.0), m.K_IAU); L = lambda cc, key: last(cc[key] + JPL, GU[1]) * 86400
    print(f'    {dt:5.2f}              {w2:+6.1f}                        {w3:+6.1f}                        {sec(6, 2, 12.66) - L(gi, "c1"):+6.1f}                    {sec(7, 17, 2.9) - L(g, "c2"):+6.1f}                          {sec(8, 47, 24.62) - L(gi, "c4"):+6.1f} / {sec(8, 47, 31.5) - L(gi, "c4"):+6.1f}')

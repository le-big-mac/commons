# The figures the revised write-up quotes, in one place: contacts at the modern memorial at Wa Ko and at the French adopted position, by four clocks, with my Moon and with JPL's
# (2.5 s earlier, hz_check2.py); the French timings turned into sundial time; distances from the central line.  Run after run_1868.sh.
import sys, numpy as np, importlib.util
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('siam', '/home/agent1/wander/siam1868.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
JPL = -2.5 / 86400.0; hms = m.hms
SITES = (('the memorial at Wa Ko (OpenStreetMap: 11.7214 N, 99.7588 E)', 11.7214, 99.7588), ('the French adopted position (11d42\'35" N, 99d47\'44" E)', 11 + 42 / 60 + 35 / 3600, 99 + 47 / 60 + 44 / 3600))
eot = None
for name, la, lo in SITES:
    xyz = m.site(la, lo); print(name)
    for k, kn in ((m.K_SMALL, 'smaller lunar radius'), (m.K_IAU, 'IAU lunar radius')):
        c = m.contacts(xyz, k)
        for key, lab in (('c1', 'first contact'), ('c2', 'totality begins'), ('c3', 'totality ends'), ('c4', 'last contact')):
            ut, lmt, bmt, lat_ = m.clocks(c[key] + JPL, lo, xyz)
            print(f'   {kn:21s} {lab:16s} JPL Moon: UT {hms(ut)}  sundial {hms(lat_)}  local mean {hms(lmt)}  meridian of 100d30\'E {hms(bmt)}')
            if key == 'c2' and eot is None: eot = ((lat_ - lmt + 0.5) % 1.0 - 0.5) * 86400
        print(f'   {kn:21s} duration {(c["c3"] - c["c2"]) * 86400:.1f} s')
print(f'\nsundial time minus mean time at the start of totality: {eot:.1f} s')
for who, key, t in (('Tisserand', 'second contact', (11, 39, 23.1)), ('Olry', 'second contact', (11, 39, 23.8)), ('Stephan (bright layer gone)', 'second contact', (11, 39, 34.9)), ('Hatt (bright layer gone)', 'second contact', (11, 39, 35.1)), ('Tisserand', 'third contact', (11, 46, 9.1)), ('Hatt', 'third contact', (11, 46, 3.1))):
    s = t[0] * 3600 + t[1] * 60 + t[2]; print(f'   French clock, {key}, {who}: {t[0]}:{t[1]:02d}:{t[2]:04.1f} local mean time = {hms((s + eot) / 86400)} sundial time')
print('\ndistance from my central line:')
for name, la, lo in (('the memorial', 11.7214, 99.7588), ('the French adopted position', 11 + 42 / 60 + 35 / 3600, 99 + 47 / 60 + 44 / 3600), ("the King's computed point, 11d41'40\" N, 51' west of 100d30' = 99d39' E", 11 + 41 / 60 + 40 / 3600, 99.65),
                     ("the same at 99d41' E (the figure in Aubin's text)", 11 + 41 / 60 + 40 / 3600, 99 + 41 / 60), ("the King's invitation to Ord, 11d39' N 99d42' E", 11.65, 99.7), ("where Ord says they met, 11d38' N 99d39' E", 11 + 38 / 60, 99.65)):
    c = m.contacts(m.site(la, lo), m.K_SMALL)
    best = min(((m.km_between((la, lo), g), g) for t in np.arange(c['mid'] - 0.004, c['mid'] + 0.004, 0.5 / 86400.0) for g in [m.axis_ground(t)] if g), key=lambda r: r[0])
    print(f'   {name}: {best[0]:.1f} km, the line passing to the ' + ('north' if best[1][0] > la else 'south') + f'; totality {(c["c3"] - c["c2"]) * 86400:.1f} s; {(lo - 99.7588) * 60:+.1f} arcmin of longitude from the memorial')

"""Today's error of each planet pointer, taken apart (after the fact; frame S). usage: after2.py DATADIR
theory: what the circle model fitted freely to the 76 years to today leaves on the last instant;
phase: the calibrated phase turned by the gears, less the freely fitted phase of today's window, at the last instant;
lever: degrees of longitude per degree of phase at today's configuration (numerical); "in full": the longitude with
the phase error less the longitude without it, same model, not linearised."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, gears, mech
DATA = sys.argv[1]
S = json.load(open(os.path.join(HERE, 'results-S.json')))
ft, fn = S['fit']['then'], S['fit']['now']
kn = S['kep']['now']['earth']
print('planet: error today = pointer minus sky; theory part; phase error; lever; phase error times lever; the phase error\'s effect in full; theory plus that')
for p in gears.SYNODIC:
    s = mech.read(os.path.join(DATA, f'{p}_now.txt'))
    jd, lam = s['jd'][-1], s['S'][-1]
    ta, tb = 1646667.5, 2461368.0
    n = S['dn'] + kn['r'] * (jd - tb) / 360.0
    Ls_ptr = ft['sun']['L0'] + ft['sun']['r'] * (ta - ft['sun']['tref']) + 360.0 * n
    Ls_now = fn['sun']['L0'] + fn['sun']['r'] * (jd - fn['sun']['tref'])
    g = gears.SYNODIC[p] if p in gears.INFERIOR else 1 - gears.SYNODIC[p]
    ph_ptr = ft[p]['p0'] + ft[p]['r'] * (ta - ft[p]['tref']) + 360.0 * float(g) * n
    ph_now = fn[p]['p0'] + fn[p]['r'] * (jd - fn[p]['tref'])
    model = (lambda ph, Ls, rho: mech.m_inf(Ls, ph, rho)) if p in gears.INFERIOR else (lambda ph, Ls, rho: mech.m_sup(ph, Ls, rho))
    theory = float(mech.wrap(model(ph_now, Ls_now, fn[p]['rho']) - lam))
    dph = float(mech.wrap(ph_ptr - ph_now))
    lever = float(mech.wrap(model(ph_now + 0.5, Ls_now, fn[p]['rho']) - model(ph_now - 0.5, Ls_now, fn[p]['rho'])))
    total = float(mech.wrap(model(ph_ptr, Ls_ptr, ft[p]['rho']) - lam))
    full = float(mech.wrap(model(ph_now + dph, Ls_now, fn[p]['rho']) - model(ph_now, Ls_now, fn[p]['rho'])))   # the phase error's effect, not linearised
    print(f'  {p:8s} {total:+7.2f}   theory {theory:+7.2f}   phase {dph:+7.2f}   lever {lever:+.3f}   product {dph * lever:+7.2f}   effect of the phase error in full {full:+7.2f}   theory plus that {theory + full:+7.2f}   (mean Sun pointer minus fitted mean Sun {float(mech.wrap(Ls_ptr - Ls_now)):+.3f})')

"""Checker's own measurement of the drifts, by routes that do not use mech.py's fits.
Sun: unwrapped longitude, straight line + annual harmonics (linear least squares).
Moon: unwrapped longitude, (a) plain straight line, (b) straight line + the main periodic terms (linear LSQ).
Planets: true heliocentric longitude sampled at conjunctions and oppositions with the Sun (where the geocentric
direction gives the heliocentric longitude directly), then straight line + harmonics of the orbital period.
Node: (a) from demodulating the latitude at the draconic frequency: F = L - node.
Apsides: from the phase of the anomalistic term of the longitude.
usage: python -I check1.py"""
import sys, os, math, json
import numpy as np
from fractions import Fraction as F
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load

sky = load.load()
wrap = lambda x: (np.asarray(x) + 180.0) % 360.0 - 180.0
unwrap = lambda x: np.degrees(np.unwrap(np.radians(x)))
TA = sky['then']['sun']['jd'][0]; TB = sky['now']['sun']['jd'][-1]
DT = TB - TA
print(f'span {DT} d = {DT/365.25:.4f} Julian years; ta {TA} tb {TB}')

# gear ratios typed here from the papers, not imported
G = dict(moon=F(254, 19), apsides=F(9 * 53, 19 * 223), node=F(-5, 93),
         mercury=F(1513, 480), venus=F(289, 462), mars=F(133, 284), jupiter=F(315, 344), saturn=F(427, 442))
INF = ('mercury', 'venus'); SUP = ('mars', 'jupiter', 'saturn')


def harm_fit(t, y, tref, periods, nh=None, extra_t=False):
    """y = c0 + c1 (t-tref) + sum over periods p and harmonics: a cos + b sin. Returns coefs and residuals."""
    tau = t - tref
    cols = [np.ones_like(tau), tau]
    for i, p in enumerate(periods):
        n = 1 if nh is None else nh[i]
        for k in range(1, n + 1):
            ph = 2 * np.pi * k * tau / p
            cols += [np.cos(ph), np.sin(ph)]
            if extra_t and k == 1:
                cols += [tau * np.cos(ph) / 1e4, tau * np.sin(ph) / 1e4]
    A = np.column_stack(cols)
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    return c, y - A @ c


def edge(c, tref, t):
    return c[0] + c[1] * (t - tref)


def advance(p_then, p_now, r_then, r_now):
    frac = (p_now - p_then) % 360.0
    k = round((0.5 * (r_then + r_now) * DT - frac) / 360.0)
    return frac + 360.0 * k


res = {}
for fr in ('S', 'T'):
    print(f'\n=========== frame {fr} ===========')
    out = {}
    # ---- Sun ----
    sun = {}
    for w in ('then', 'now'):
        s = sky[w]['sun']; tref = 0.5 * (s['jd'][0] + s['jd'][-1])
        y = unwrap(s[fr])
        c, r = harm_fit(s['jd'], y, tref, [365.2596], nh=[3])
        c0, r0 = harm_fit(s['jd'], y, tref, [], nh=[])
        sun[w] = dict(c=c, tref=tref, plain=c0)
        print(f'  sun {w}: rate {c[1]:.9f} deg/d (year {360/c[1]:.6f} d); harmonic amp1 {math.hypot(c[2], c[3]):.4f} deg; resid rms {np.sqrt(np.mean(r**2)):.4f}; plain-line rate {c0[1]:.9f}; mean lon at centre {c[0]%360:.4f} (plain {c0[0]%360:.4f})')
    Ls_a = edge(sun['then']['c'], sun['then']['tref'], TA); Ls_b = edge(sun['now']['c'], sun['now']['tref'], TB)
    adv_sun = advance(Ls_a, Ls_b, sun['then']['c'][1], sun['now']['c'][1])
    dn = adv_sun / 360.0
    Lp_a = edge(sun['then']['plain'], sun['then']['tref'], TA); Lp_b = edge(sun['now']['plain'], sun['now']['tref'], TB)
    dn_plain = advance(Lp_a, Lp_b, sun['then']['plain'][1], sun['now']['plain'][1]) / 360.0
    print(f'  turns of the mean Sun over the span: {dn:.5f} (plain-line version {dn_plain:.5f}); advance {adv_sun:.4f} deg')
    out['dn'] = dn; out['sun_adv'] = adv_sun

    # ---- Moon ----
    PER = dict(M=27.554550, D=29.530589, Fd=27.212221, Y=365.2596)
    f = lambda **k: 1.0 / sum(v / PER[n] for n, v in k.items())
    # main terms of the Moon's longitude: M, 2D-M, 2D, 2M, Msun, 2F, 2D-2M, 2D-M-Ms, 2D+M, 2D-Ms, M-Ms, D, M+Ms, 2F-2D...
    mper = [f(M=1), f(D=2, M=-1), f(D=2), f(M=2), f(Y=1), f(Fd=2), f(D=2, M=-2), f(D=2, M=-1, Y=-1), f(D=2, M=1),
            f(D=2, Y=-1), f(M=1, Y=-1), f(D=1), f(M=1, Y=1), f(D=2, Fd=-2), f(M=3), f(D=4, M=-1), f(D=4, M=-2)]
    moon = {}
    for w in ('then', 'now'):
        s = sky[w]['moon']; tref = 0.5 * (s['jd'][0] + s['jd'][-1])
        y = unwrap(s[fr])
        c0, r0 = harm_fit(s['jd'], y, tref, [])
        c, r = harm_fit(s['jd'], y, tref, mper)
        moon[w] = dict(c=c, c0=c0, tref=tref, y=y)
        print(f'  moon {w}: plain line rate {c0[1]:.9f}, resid rms {np.sqrt(np.mean(r0**2)):.3f}; with terms: rate {c[1]:.9f}, amp(M) {math.hypot(c[2], c[3]):.4f}, amp(2D-M) {math.hypot(c[4], c[5]):.4f}, amp(2D) {math.hypot(c[6], c[7]):.4f}, resid rms {np.sqrt(np.mean(r**2)):.3f}; centre L {c[0]%360:.4f} vs plain {c0[0]%360:.4f}')
    for label, key in (('plain line', 'c0'), ('line + terms', 'c')):
        a = edge(moon['then'][key], moon['then']['tref'], TA); b = edge(moon['now'][key], moon['now']['tref'], TB)
        adv = advance(a, b, moon['then'][key][1], moon['now'][key][1])
        d = 360.0 * float(G['moon']) * dn - adv
        print(f'  MOON drift ({label}): gears {360*float(G["moon"])*dn:.3f} - sky {adv:.3f} = {d:+.3f} deg   (turns of the sky Moon {adv/360:.5f})')
        out['moon_' + key] = d
    # ---- apsides: phase of the anomalistic term, demodulated in blocks ----
    aps = {}
    for w in ('then', 'now'):
        s = sky[w]['moon']; tref = moon[w]['tref']; tau = s['jd'] - tref
        y = moon[w]['y'] - (moon[w]['c'][0] + moon[w]['c'][1] * tau)     # periodic part
        # the anomalistic term: y ~ A sin(M), M = M0 + m tau. Demodulate with the nominal rate over blocks of ~ 4 years.
        m0 = 360.0 / PER['M']
        nb = 19; edges = np.linspace(tau[0], tau[-1], nb + 1); tc = []; ph = []
        for i in range(nb):
            mk = (tau >= edges[i]) & (tau < edges[i + 1])
            z = np.mean(y[mk] * np.exp(-1j * np.radians(m0 * tau[mk])))      # A/(2i) exp(i(M - m0 tau))
            tc.append(np.mean(tau[mk])); ph.append(np.degrees(np.angle(z)) + 90.0)   # M - m0 tau at block centre
        ph = unwrap(np.array(ph)); tc = np.array(tc)
        sl, ic = np.polyfit(tc, ph, 1)
        # mean anomaly M(tau) = ic + (m0 + sl) tau ; perigee = L - M ; apogee = perigee + 180
        Lc, Lr = moon[w]['c'][0], moon[w]['c'][1]
        aps[w] = dict(p0=Lc - ic, r=Lr - (m0 + sl), tref=tref, scatter=float(np.std(ph - (ic + sl * tc))))
        print(f'  apsides {w}: perigee at centre {aps[w]["p0"]%360:.3f}, rate {aps[w]["r"]:.7f} deg/d (period {360/aps[w]["r"]:.2f} d); scatter of block phases {aps[w]["scatter"]:.3f} deg')
    a = aps['then']['p0'] + aps['then']['r'] * (TA - aps['then']['tref']); b = aps['now']['p0'] + aps['now']['r'] * (TB - aps['now']['tref'])
    adv = advance(a, b, aps['then']['r'], aps['now']['r'])
    out['apsides'] = 360.0 * float(G['apsides']) * dn - adv
    print(f'  APSIDES drift: gears {360*float(G["apsides"])*dn:.3f} - sky {adv:.3f} = {out["apsides"]:+.3f} deg')
    # ---- node: demodulate the latitude at the draconic frequency: lat ~ 5.13 sin(F), F = L - node ----
    nd = {}
    for w in ('then', 'now'):
        s = sky[w]['moon']; tref = moon[w]['tref']; tau = s['jd'] - tref
        f0 = 360.0 / PER['Fd']
        nb = 19; edges = np.linspace(tau[0], tau[-1], nb + 1); tc = []; ph = []
        for i in range(nb):
            mk = (tau >= edges[i]) & (tau < edges[i + 1])
            z = np.mean(s['lat'][mk] * np.exp(-1j * np.radians(f0 * tau[mk])))
            tc.append(np.mean(tau[mk])); ph.append(np.degrees(np.angle(z)) + 90.0)
        ph = unwrap(np.array(ph)); tc = np.array(tc)
        sl, ic = np.polyfit(tc, ph, 1)
        Lc, Lr = moon[w]['c'][0], moon[w]['c'][1]
        nd[w] = dict(p0=Lc - ic, r=Lr - (f0 + sl), tref=tref, scatter=float(np.std(ph - (ic + sl * tc))))
        print(f'  node {w}: at centre {nd[w]["p0"]%360:.3f}, rate {nd[w]["r"]:.7f} deg/d (period {360/nd[w]["r"]:.2f} d = {360/nd[w]["r"]/365.25:.4f} Jy); scatter {nd[w]["scatter"]:.3f}')
    a = nd['then']['p0'] + nd['then']['r'] * (TA - nd['then']['tref']); b = nd['now']['p0'] + nd['now']['r'] * (TB - nd['now']['tref'])
    adv = advance(a, b, nd['then']['r'], nd['now']['r'])
    out['node'] = 360.0 * float(G['node']) * dn - adv
    print(f'  NODE drift: gears {360*float(G["node"])*dn:.3f} - sky {adv:.3f} = {out["node"]:+.3f} deg')

    # ---- planets: heliocentric longitude sampled at conjunctions / oppositions ----
    P0 = dict(mercury=87.9691, venus=224.7008, mars=686.9796, jupiter=4332.589, saturn=10759.22)
    NH = dict(mercury=7, venus=2, mars=5, jupiter=3, saturn=3)
    for p in G:
        if p not in INF + SUP: continue
        pl = {}
        for w in ('then', 'now'):
            s = sky[w][p]; su = sky[w]['sun']
            jd = s['jd']; lp = unwrap(s[fr]); ls = unwrap(su[fr])
            el = wrap(lp - ls)
            csl = CubicSpline(jd, lp); css = CubicSpline(jd, ls)
            T, H, kind = [], [], []
            for off in (0.0, 180.0):
                d = wrap(el - off)
                idx = np.where((np.sign(d[:-1]) != np.sign(d[1:])) & (np.abs(d[:-1]) < 60) & (np.abs(d[1:]) < 60))[0]
                for i in idx:
                    fz = lambda t: float(wrap(csl(t) - css(t) - off))
                    t = brentq(fz, jd[i], jd[i + 1], xtol=1e-7)
                    sunlon = float(css(t))
                    if p in INF:
                        if off != 0.0: continue
                        inferior = d[i] > 0 and d[i + 1] <= 0        # elongation falling through zero: retrograde, inferior
                        H.append(sunlon + 180.0 if inferior else sunlon); kind.append('inf' if inferior else 'sup')
                    else:
                        H.append(float(csl(t))); kind.append('opp' if off == 180.0 else 'conj')
                    T.append(t)
            T = np.array(T); o = np.argsort(T); T = T[o]; H = np.array(H)[o]; kind = np.array(kind)[o]
            tref = 0.5 * (jd[0] + jd[-1])
            # unwrap the heliocentric longitudes along a nominal mean motion
            n0 = 360.0 / P0[p]
            Hu = H % 360.0
            Hu = (n0 * (T - tref)) + wrap(Hu - n0 * (T - tref) - wrap(Hu[len(Hu) // 2] - n0 * (T[len(T) // 2] - tref))) + wrap(Hu[len(Hu) // 2] - n0 * (T[len(T) // 2] - tref))
            c, r = harm_fit(T, Hu, tref, [P0[p]], nh=[NH[p]], extra_t=True)
            pl[w] = dict(c=c, tref=tref, n=len(T), rms=float(np.sqrt(np.mean(r ** 2))), kinds={k: int(np.sum(kind == k)) for k in set(kind)}, T=T, kind=kind)
            print(f'  {p} {w}: {len(T)} samples {pl[w]["kinds"]}; mean helio lon at centre {c[0]%360:.4f}; rate {c[1]:.9f} deg/d (period {360/c[1]:.5f} d); resid rms {pl[w]["rms"]:.4f}')
        a = edge(pl['then']['c'], pl['then']['tref'], TA); b = edge(pl['now']['c'], pl['now']['tref'], TB)
        ra, rb = pl['then']['c'][1], pl['now']['c'][1]
        if p in INF:
            # epicycle phase: planet's heliocentric mean longitude less the Earth's (= mean Sun + 180)
            a -= Ls_a + 180.0; b -= Ls_b + 180.0; ra -= sun['then']['c'][1]; rb -= sun['now']['c'][1]
            g = G[p]
        else:
            g = 1 - G[p]
        adv = advance(a, b, ra, rb)
        out[p] = 360.0 * float(g) * dn - adv
        print(f'  {p.upper()} drift: gears {360*float(g)*dn:.3f} - sky {adv:.3f} = {out[p]:+.3f} deg; per Julian year {out[p]/(DT/365.25):+.6f}')
        if p == 'venus':
            # second, cruder route for Venus: the mean synodic phase from inferior-conjunction times alone
            for w in ('then', 'now'):
                Tq = pl[w]['T'][pl[w]['kind'] == 'inf']
                k = np.arange(len(Tq)); sl, ic = np.polyfit(k, Tq, 1)
                pl[w]['syn'] = sl; pl[w]['t0'] = ic; pl[w]['ninf'] = len(Tq)
            # phase (in cycles) at time t: (t - t0)/syn
            pa = (TA - pl['then']['t0']) / pl['then']['syn']; pb = (TB - pl['now']['t0']) / pl['now']['syn']
            cyc_guess = DT / (0.5 * (pl['then']['syn'] + pl['now']['syn']))
            fracc = (pb - pa) % 1.0
            cyc = fracc + round(cyc_guess - fracc)
            print(f'    Venus by inferior-conjunction times only: synodic period then {pl["then"]["syn"]:.4f} d ({pl["then"]["ninf"]} conj), now {pl["now"]["syn"]:.4f} d; sky cycles over the span {cyc:.4f}; gears {float(G["venus"])*dn:.4f}; drift {(float(G["venus"])*dn-cyc)*360:+.2f} deg')
    res[fr] = out

print('\n=========== beside run.out ===========')
J = {fr: json.load(open(os.path.join(HERE, '..', f'results-{fr}.json'))) for fr in 'ST'}
for fr in 'ST':
    print(f'frame {fr}: turns mine {res[fr]["dn"]:.5f}  run.out {J[fr]["dn"]:.5f}')
    for k in ('moon', 'apsides', 'node', 'mercury', 'venus', 'mars', 'jupiter', 'saturn'):
        mine = res[fr]['moon_c'] if k == 'moon' else res[fr][k]
        extra = f' (plain line {res[fr]["moon_c0"]:+.3f})' if k == 'moon' else ''
        print(f'   {k:8s} mine {mine:+9.3f}{extra}   run.out {J[fr]["drift"][k]:+9.3f}   difference {mine - J[fr]["drift"][k]:+.3f}')
print(f'precession (T advance - S advance of the mean Sun): mine {res["T"]["sun_adv"] - res["S"]["sun_adv"]:.4f}  run {J["T"]["sun_advance"] - J["S"]["sun_advance"]:.4f}')

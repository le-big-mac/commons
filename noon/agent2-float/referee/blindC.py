"""Blind part C: the tilted family beyond the ring, Q4d, Q6, sliver. Decimal arithmetic for the delicate parts."""
import math, sys
from decimal import Decimal as D
import numpy as np
from ref import h_dec, h_float

out = open('/home/agent2/float/referee/blindC.out', 'w')


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); out.write(s + '\n'); out.flush()


GR = (D(5).sqrt() - 1) / 2
S2 = D(2).sqrt()


def golden(f, lo, hi, it=70):
    x1 = hi - GR * (hi - lo); x2 = lo + GR * (hi - lo); f1, f2 = f(x1), f(x2)
    for _ in range(it):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - GR * (hi - lo); f1 = f(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + GR * (hi - lo); f2 = f(x2)
    x = (lo + hi) / 2
    return x, f(x)


def ring_h(d):
    return (12 * d * (1 - d) - 1).sqrt() / (12 * d)


def ring_t(d):
    return (12 * d * (1 - d) - 2).sqrt()


def valley(d, phi_deg, tlo=None, thi=None):
    """min over t=tan(theta) near the ring value at azimuth phi; returns (t, h)."""
    c, s = D(math.cos(math.radians(phi_deg))), D(math.sin(math.radians(phi_deg)))
    if phi_deg == 0: c, s = D(1), D(0)
    if phi_deg == 45: c, s = S2 / 2, S2 / 2
    t0 = ring_t(d)
    lo = t0 * D('0.6') if tlo is None else tlo
    hi = t0 * D('1.5') if thi is None else thi
    return golden(lambda t: h_dec((1, t * c, t * s), d), lo, hi)


def diag_min(d):
    """local minima of g(p)=h((1,p,p)) for p in (0,1): scan then golden. returns list of (p,h)."""
    df = float(d)
    N = 400
    ps = [(i + 0.5) / N for i in range(N)]
    v = [float(h_dec((1, D(p), D(p)), d)) if p < 0.02 else h_float((1, p, p), df) for p in ps]
    res = []
    for i in range(1, N - 1):
        if v[i] < v[i - 1] and v[i] <= v[i + 1]:
            p, h = golden(lambda p: h_dec((1, p, p), d), D(ps[i - 1]), D(ps[i + 1]))
            res.append((p, h))
    return res


def transverse_curv(d, p, r=D('1e-6')):
    """second difference of h at (1,p,p) in direction (0,1,-1) (tilt angle ~ r)."""
    nm = (1 + 2 * p * p).sqrt()
    h0 = h_dec((1, p, p), d)
    h1 = h_dec((1, p + r * nm / S2, p - r * nm / S2), d)
    return (h1 - h0) / (r * r) * 2


if __name__ == '__main__':
    dstar = (3 - S2) / 7
    P("end of full ring (3-sqrt2)/7 = %.12f ; at that density: ring h = %.15f corner h = %.15f face h = %.15f" % (
        dstar, ring_h(dstar), h_dec((1, 1, 1), dstar), (1 - dstar) / 2))

    # ---- Q4d: where corner becomes lowest of all
    def corner_minus_tilt(d):
        cands = [ring_h(d)] if d <= D('0.25') else []
        cands += [h for p, h in diag_min(d) if p < D('0.9')]
        return h_dec((1, 1, 1), d) - min(cands)

    lo, hi = D('0.2255'), D('0.2285')
    assert corner_minus_tilt(lo) > 0 > corner_minus_tilt(hi)
    for _ in range(45):
        mid = (lo + hi) / 2
        if corner_minus_tilt(mid) > 0:
            lo = mid
        else:
            hi = mid
    dcross = (lo + hi) / 2
    P("Q4d corner up becomes lowest of all at d = %.12f (h = %.12f); ring-formula crossing would be:" % (dcross, h_dec((1, 1, 1), dcross)))
    lo, hi = D('0.2255'), D('0.2285')
    for _ in range(45):
        mid = (lo + hi) / 2
        if h_dec((1, 1, 1), mid) - ring_h(mid) > 0:
            lo = mid
        else:
            hi = mid
    P("     corner = ring formula at d = %.12f" % ((lo + hi) / 2))

    # ---- sliver
    P("\nSliver: valley floor minus ring-formula value, by azimuth (Decimal, 60 digits)")
    for ds in ('0.2264', '0.2266', '0.2267', '0.2268', '0.22685', '0.2269', '0.2270', '0.2280', '0.2300'):
        d = D(ds)
        rh = ring_h(d)
        row = []
        for phi in (0, 10, 20, 30, 35, 40, 43, 45):
            t, h = valley(d, phi)
            row.append("%d:%+.3e" % (phi, h - rh))
        phi_edge = None
        x = 2 * float(d) / float(ring_t(d))      # need cos+sin <= x
        if x < math.sqrt(2):
            phi_edge = 45 - math.degrees(math.acos(x / math.sqrt(2)))
        P("  d=%s ring h=%.15f  corner-ring=%+.3e  exact-tie arc |phi|<=%s  floor-ring: %s" % (
            ds, rh, h_dec((1, 1, 1), d) - rh, 'all' if phi_edge is None else '%.3f deg' % phi_edge, ' '.join(row)))

    # ---- Q6
    P("\nQ6: tilted attitudes on the diagonal plane up=(1,p,p)/norm: local minima along p, and transverse curvature")
    for i in range(0, 15):
        d = D('0.23') + D('0.005') * i
        mins = diag_min(d)
        txt = []
        for p, h in mins:
            if p > D('0.99'):
                continue
            tc = transverse_curv(d, p)
            txt.append("p=%.9f tilt=%.4f deg h=%.12f transverse curv %+.5f" % (p, math.degrees(math.atan(float(p) * math.sqrt(2))), h, tc))
        arc = ''
        if d < D('0.25'):
            x = 2 * float(d) / float(ring_t(d))
            arc = 'exact-tie arc half-width %.3f deg, h=%.12f' % (45 - math.degrees(math.acos(min(1, x / math.sqrt(2)))), ring_h(d))
        P("  d=%.3f corner h=%.12f | %s | %s" % (d, h_dec((1, 1, 1), d), '; '.join(txt) if txt else 'no tilted minimum on diagonal plane', arc))

    def has_tilt(d):
        return any(p < D('0.9') and transverse_curv(d, p) > 0 for p, h in diag_min(d))

    lo, hi = D('0.23'), D('0.30')
    if has_tilt(lo) and not has_tilt(hi):
        for _ in range(34):
            mid = (lo + hi) / 2
            if has_tilt(mid):
                lo = mid
            else:
                hi = mid
        dl = (lo + hi) / 2
        P("  diagonal-plane tilted minimum exists up to d = %.9f" % dl)
        for dd in (lo - D('1e-6'), lo - D('1e-4')):
            for p, h in diag_min(dd):
                if p < D('0.9'):
                    P("     just below (d=%.9f): p=%.9f tilt=%.5f deg h=%.12f transverse curv %+.3e ; corner h=%.12f" % (
                        dd, p, math.degrees(math.atan(float(p) * math.sqrt(2))), h, transverse_curv(dd, p), h_dec((1, 1, 1), dd)))
    out.close()

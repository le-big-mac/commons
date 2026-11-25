"""lantern.py: Dr Young's rods (Lectures, 1807, Plate XXVIII, Fig. 401) as a mechanism, and the lens it serves.
Lengths are in units of the focal length f unless a function says otherwise. Along the axis, distances are measured from the painted
slider (the object) toward the screen. The box carries the slider at 0 and a pivot I; the lens sits at s and carries a pivot L; the
screen stands at D and has a pivot N beside it. K is the joint at the top: KI and KN are the two rods Young says must be equal, KL is
the rod that moves the lens.

    python -I lantern.py        prints a short table of the ideal arrangement
"""
import math

def focus(D, f=1.0):
    """where the lens must stand for a sharp image on a screen at D from the slider (the nearer of the two places): s, and m = s'/s"""
    if D < 4 * f: return None
    s = (D - math.sqrt(D * D - 4 * f * D)) / 2.0; return s, (D - s) / s

def D_of_m(m, f=1.0): return f * (2 + m + 1.0 / m)

class Rods:
    """the arrangement, with every dimension that can be wrong. Ideal: p = 2f, q = f, a2 = a, b = sqrt(a^2 - f^2), e = 0, heights 0."""
    def __init__(self, a, f=1.0, b=None, a2=None, p=None, q=None, e=0.0, yI=0.0, yL=0.0, yN=0.0):
        self.f = f; self.a = a; self.a2 = a if a2 is None else a2; self.b = math.sqrt(a * a - f * f) if b is None else b
        self.p = 2 * f if p is None else p; self.q = f if q is None else q; self.e = e; self.yI, self.yL, self.yN = yI, yL, yN
    def K(self, D):
        """the top joint, where the circle about I of radius a meets the circle about N of radius a2, on the upper side"""
        Ix, Iy = self.p, self.yI; Nx, Ny = D + self.e, self.yN; dx, dy = Nx - Ix, Ny - Iy; d = math.hypot(dx, dy)
        if d > self.a + self.a2 or d < abs(self.a - self.a2) or d == 0: return None
        t = (self.a ** 2 - self.a2 ** 2 + d * d) / (2 * d); h2 = self.a ** 2 - t * t
        if h2 < 0: return None
        h = math.sqrt(h2); mx, my = Ix + t * dx / d, Iy + t * dy / d; return (mx - h * dy / d, my + h * dx / d)
    def lens(self, D):
        """where the rods put the lens: the pivot L is on the slider at height yL, at distance b from K, on the side of K toward the box"""
        k = self.K(D)
        if k is None: return None
        w2 = self.b ** 2 - (k[1] - self.yL) ** 2
        if w2 < 0: return None
        return k[0] - math.sqrt(w2) - self.q
    def thrust(self, D):
        """how KL stands when it moves the lens (added after the referee's report): its angle with the lens's bar in degrees; how many times
        the push on the lens the thrust along KL is (1 / cos); and the friction between slider and bar at and above which no thrust
        along KL can move the lens at all (1 / tan), because the rod presses the slider on its bar harder than it pushes it along"""
        k = self.K(D); s = self.lens(D)
        if k is None or s is None: return None
        dx = k[0] - (s + self.q); dy = k[1] - self.yL; th = math.atan2(dy, dx); return math.degrees(th), 1.0 / math.cos(th), 1.0 / math.tan(th)
    def reach(self):
        """the farthest screen the rods allow: I and N at full stretch"""
        return self.p - self.e + math.sqrt(max((self.a + self.a2) ** 2 - (self.yN - self.yI) ** 2, 0.0))

def blur(D, s, f=1.0, A=1.0):
    """the width of the patch that a point of the slider makes on the screen at D when the lens of opening A stands at s (by rays; no
    diffraction). In the units of A when A = 1."""
    if s <= f: return float('inf')
    si = f * s / (s - f); return A * abs((D - s) - si) / si

def worst(rods, m_lo, m_hi, steps=400):
    """the largest patch (in units of the lens's opening) as the image is made to grow from m_lo to m_hi times the slider, and where"""
    out = (0.0, None)
    for i in range(steps + 1):
        m = m_lo * (m_hi / m_lo) ** (i / steps); D = D_of_m(m, rods.f); s = rods.lens(D)
        c = float('inf') if s is None else blur(D, s, rods.f)
        if c > out[0]: out = (c, m)
    return out

if __name__ == '__main__':
    r = Rods(a=11.0)
    print('the ideal arrangement, rods of 11 focal lengths (reach: a screen at %.2f f from the slider)' % r.reach())
    print('   m      screen at   lens must be at   the rods put it at   difference')
    for m in (1, 1.5, 2, 3, 5, 10, 20):
        D = D_of_m(m); s = focus(D)[0]; print('   %-5s  %8.4f    %.9f       %.9f          %+.1e' % (m, D, s, r.lens(D), r.lens(D) - s))

# ---- what else the sheet asks about

def sag_shortening(L, w_perp, EI, P=0.0, n=2000):
    """how much nearer the two pins of a rod come when it sags: a uniform rod of length L, pinned at both ends, carrying w_perp across
    itself (its own weight times the cosine of its slope) and pushed along itself by P. The sag of the unloaded-along rod is the
    textbook w x (L^3 - 2 L x^2 + x^3) / (24 EI); a push P magnifies it by 1 / (1 - P / P_cr), P_cr = pi^2 EI / L^2 (the first term of
    the series, good to a few parts in 1,000). The shortening is half the integral of the slope squared. SI units."""
    amp = 1.0 / (1.0 - P / (math.pi ** 2 * EI / L ** 2)); tot = 0.0; h = L / n
    for i in range(n):
        x = (i + 0.5) * h; slope = amp * w_perp * (L ** 3 - 6 * L * x * x + 4 * x ** 3) / (24 * EI); tot += 0.5 * slope * slope * h
    return tot

def cam(m_lo, m_hi, turn_deg=300.0, alpha_deg=30.0, f=1.0, steps=4000, press=False):
    """Brewster's spiral cam on the axle: the cam turns through turn_deg while the box rolls from the place for m_lo to the place for
    m_hi; a follower along a radius carries the lens, so the cam's radius is r0 + (lens's place - its least place). The smallest r0
    for which the pressure angle (tan = (dr/dphi) / r) never passes alpha_deg; returns r0, the cam's largest radius, and the m at which
    the angle is at its limit. press=True (added after the referee's report) is Brewster's own sense: a spring holds the lens out and the
    cam presses it in, so the cam's radius is greatest where the lens is nearest the slider, r = R - (lens's place - its least place);
    then the first number returned is the least radius and the second the largest, as before."""
    D0, D1 = D_of_m(m_lo, f), D_of_m(m_hi, f); Phi = math.radians(turn_deg); t = math.tan(math.radians(alpha_deg)); smin = focus(D1, f)[0]; need = (0.0, None, 0.0)
    for i in range(steps + 1):
        D = D0 + (D1 - D0) * i / steps; s = focus(D, f)[0]; dD = 1e-6 * f; ds = (focus(D + dD, f)[0] - focus(max(D - dD, 4 * f), f)[0]) / (D + dD - max(D - dD, 4 * f)); drdphi = abs(ds) * (D1 - D0) / Phi
        r0 = (drdphi / t + (s - smin)) if press else (drdphi / t - (s - smin))      # press: R, the radius at the lens's least place; else r0, the radius there
        if r0 > need[0]: need = (r0, focus(D, f)[1], s - smin)
    if press: return need[0] - (focus(D0, f)[0] - smin), need[0], need[1]
    return need[0], need[0] + (focus(D0, f)[0] - smin), need[1]

def shade(m_lo, m_hi, steps=600):
    """Young's falling shade, as I model it: a triangular opening of which the lens sees a similar triangle whose side shrinks in
    proportion as the lens is drawn out, so the light let through goes as (x0 - x)^2, x the lens's distance beyond its focus-distance
    from the slider (x = f / m). For a ghost that keeps one brightness the light must go as (1 + m)^2. Returns the x0 that makes the
    greatest ratio between brightest and dimmest (over m_lo..m_hi) least, and that ratio's square root: the factor either way."""
    ms = [m_lo * (m_hi / m_lo) ** (i / steps) for i in range(steps + 1)]
    def spread(x0):
        v = [math.log((x0 - 1.0 / m) ** 2 / (1 + m) ** 2) for m in ms]; return max(v) - min(v)
    lo, hi = 1.0 / m_lo + 1e-6, 1.0 / m_lo + 50.0
    for _ in range(200):      # the spread has one minimum in x0: golden section
        a = lo + 0.381966 * (hi - lo); b = lo + 0.618034 * (hi - lo)
        if spread(a) < spread(b): hi = b
        else: lo = a
    x0 = (lo + hi) / 2; return x0, math.exp(spread(x0) / 2), math.exp(0.5 * (2 * math.log((1 + m_hi) / (1 + m_lo))))

def light(m, s, x0=None, f=1.0):
    """the brightness of the image up to a constant: the share of the lens left open by the falling shade (which would shut it at x0
    past the lens's nearest place; None for no shade) over the square of the screen's distance from the lens. The page's sum."""
    opened = 1.0
    if x0 is not None: u = (x0 - (s - f)) / x0; opened = 0.0 if u <= 0 else min(u * u, 1.0)
    sp = D_of_m(m, f) - s; return opened / (sp * sp)

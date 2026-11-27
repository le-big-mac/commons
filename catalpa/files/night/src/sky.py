# Where the Sun and the Moon stand for an observer, by short closed formulas (no files needed), for sorting
# night-sky readings into "Sun 18 degrees or more below the horizon" and "Moon down". Checked against JPL
# Horizons in src/sky_check.py; see sky_check.out for how far these are out.
# Sun: the Astronomical Almanac's low-precision series. Moon: its low-precision series (longitude, latitude,
# parallax), with the parallax applied to the altitude. No refraction: at -18 degrees it does not matter.
import math, datetime as dt
R = math.pi / 180
def jd(t):               # t: naive datetime in UTC
    return 2440587.5 + (t - dt.datetime(1970, 1, 1)).total_seconds() / 86400
def gmst_deg(j):
    n = j - 2451545.0; return (280.46061837 + 360.98564736629 * n) % 360
def _altaz(ra, dec, j, lat, lon):
    H = (gmst_deg(j) + lon - ra) * R; la = lat * R; d = dec * R
    return math.asin(math.sin(la) * math.sin(d) + math.cos(la) * math.cos(d) * math.cos(H)) / R
def _eq(lam, beta, j):
    eps = (23.439 - 0.0000004 * (j - 2451545.0)) * R; l, b = lam * R, beta * R
    x = math.cos(b) * math.cos(l); y = math.cos(b) * math.sin(l) * math.cos(eps) - math.sin(b) * math.sin(eps); z = math.cos(b) * math.sin(l) * math.sin(eps) + math.sin(b) * math.cos(eps)
    return math.atan2(y, x) / R % 360, math.asin(z) / R
def sun_lon(j):
    n = j - 2451545.0; L = (280.460 + 0.9856474 * n) % 360; g = ((357.528 + 0.9856003 * n) % 360) * R
    return (L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360
def sun_alt(t, lat, lon):
    j = jd(t); ra, dec = _eq(sun_lon(j), 0.0, j); return _altaz(ra, dec, j, lat, lon)
def moon_ecl(j):
    T = (j - 2451545.0) / 36525; s = lambda a, b: math.sin((a + b * T) * R); c = lambda a, b: math.cos((a + b * T) * R)
    lam = 218.32 + 481267.881 * T + 6.29 * s(135.0, 477198.87) - 1.27 * s(259.3, -413335.36) + 0.66 * s(235.7, 890534.22) + 0.21 * s(269.9, 954397.74) - 0.19 * s(357.5, 35999.05) - 0.11 * s(186.5, 966404.03)
    beta = 5.13 * s(93.3, 483202.02) + 0.28 * s(228.2, 960400.89) - 0.28 * s(318.3, 6003.15) - 0.17 * s(217.6, -407332.21)
    par = 0.9508 + 0.0518 * c(135.0, 477198.87) + 0.0095 * c(259.3, -413335.36) + 0.0078 * c(235.7, 890534.22) + 0.0028 * c(269.9, 954397.74)
    return lam % 360, beta, par
def moon_alt(t, lat, lon):
    j = jd(t); lam, beta, par = moon_ecl(j); ra, dec = _eq(lam, beta, j); a = _altaz(ra, dec, j, lat, lon)
    return a - par * math.cos(a * R)          # seen from the surface, not from the Earth's centre
def moon_lit(t):
    # share of the Moon's disc that is lit, from its angle from the Sun
    j = jd(t); lam, beta, par = moon_ecl(j); e = math.acos(math.cos(beta * R) * math.cos((lam - sun_lon(j)) * R)); return (1 - math.cos(e)) / 2

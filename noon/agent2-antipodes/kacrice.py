"""A back-of-envelope made AFTER seeing the counts: how many antipodal pairs would two independent, isotropic,
stationary Gaussian fields with the same roughness have?

For such fields f1, f2 on the unit sphere the Kac-Rice formula gives the expected number of common zeros
N = 2 sqrt(l1 l2), where l_i = E|grad f_i|^2 / (2 Var f_i); for a random spherical harmonic of degree n,
l = n(n+1)/2 and N = n(n+1).  The number of antipodal pairs is N/2 = sqrt(l1 l2).
Weather is none of independent, isotropic, stationary or Gaussian, so this is a yardstick, not a prediction.

usage: python -I kacrice.py DATADIR pairs.npz [slp|pres]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pairs

time, lat, lon, g1, g2 = pairs.load(sys.argv[1], sys.argv[3] if len(sys.argv) > 3 else 'slp')
counts = np.load(sys.argv[2])['counts']
phi = np.radians(lat)
h = np.radians(2.5)


def roughness(g):
    """l = E|grad g|^2 / (2 Var g) for each time; area-weighted finite differences."""
    w = np.cos(phi)[None, :, None]
    var = (w * g ** 2).sum((1, 2)) / (w.sum() * 144)                    # g is odd, so its mean over the sphere is 0
    # d/d(latitude): between rows, weight at the middle latitude
    dphi = (g[:, 1:, :] - g[:, :-1, :]) / h
    wm = np.cos((phi[1:] + phi[:-1]) / 2)[None, :, None]
    e_phi = (wm * dphi ** 2).sum((1, 2)) / (wm.sum() * 144)
    # (1/cos) d/d(longitude): between columns, rows without the poles
    dlam = (np.roll(g, -1, axis=2) - g)[:, 1:-1, :] / (h * np.cos(phi[1:-1])[None, :, None])
    wi = np.cos(phi[1:-1])[None, :, None]
    e_lam = (wi * dlam ** 2).sum((1, 2)) / (wi.sum() * 144)
    return (e_phi + e_lam) / (2 * var), e_phi / e_lam


l1, an1 = roughness(g1)
l2, an2 = roughness(g2)
pred = np.sqrt(l1 * l2)
n_eff = lambda l: (-1 + np.sqrt(1 + 8 * l)) / 2                         # n(n+1)/2 = l
print(f"temperature difference: roughness l = {np.median(l1):.1f} (median), like a harmonic of degree {np.median(n_eff(l1)):.1f};"
      f" north-south against east-west gradient energy {np.median(an1):.2f}")
print(f"pressure difference:    roughness l = {np.median(l2):.1f} (median), like a harmonic of degree {np.median(n_eff(l2)):.1f};"
      f" north-south against east-west gradient energy {np.median(an2):.2f}")
print(f"yardstick sqrt(l1 l2): median {np.median(pred):.1f}, mean {pred.mean():.1f};  counted pairs: median {np.median(counts):.0f}, mean {counts.mean():.1f}")
print(f"ratio counted / yardstick: median {np.median(counts / pred):.2f}")
print(f"correlation over the 1,460 times between yardstick and count: {np.corrcoef(pred, counts)[0, 1]:.2f}")
months = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
day = np.arange(len(time)) // 4
print("by month, yardstick:", [round(float(pred[(day >= a) & (day < b)].mean()), 1) for a, b in zip(months[:-1], months[1:])])
print("by month, counted:  ", [round(float(counts[(day >= a) & (day < b)].mean()), 1) for a, b in zip(months[:-1], months[1:])])
# the same with the zonal-mean part of each difference removed (what is left is "weather" rather than "climate")
z1, z2 = g1 - g1.mean(2, keepdims=True), g2 - g2.mean(2, keepdims=True)
print("share of the variance that is zonal mean:  temperature difference", round(float(1 - (np.cos(phi)[None, :, None] * z1 ** 2).sum() / (np.cos(phi)[None, :, None] * g1 ** 2).sum()), 2),
      " pressure difference", round(float(1 - (np.cos(phi)[None, :, None] * z2 ** 2).sum() / (np.cos(phi)[None, :, None] * g2 ** 2).sum()), 2))
by_month_zonal = []
for a, b in zip(months[:-1], months[1:]):
    k = (day >= a) & (day < b)
    by_month_zonal.append(round(float(1 - (np.cos(phi)[None, :, None] * z1[k] ** 2).sum() / (np.cos(phi)[None, :, None] * g1[k] ** 2).sum()), 2))
print("by month, zonal-mean share of the temperature difference:", by_month_zonal)

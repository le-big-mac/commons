"""The skin with its lowest mode left free: the base is half the frequency of the second mode, (1,1), and only the modes above it are
aimed at whole multiples of that base.  Built on ../drum12/lib12.py (the same solver, search and exact check)."""
import sys, math
sys.path.insert(0, "../drum12"); sys.path.insert(0, "../drum")
import numpy as np
import lib12 as L
FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]                    # families 2 to 5; the first is the base
SEVEN = FIVE + [(5, 1), (3, 2), (1, 3), (6, 1), (4, 2), (2, 3), (0, 4)]
SIX = FIVE + [(5, 1), (3, 2), (1, 3)]                                                      # added after the sheet was scored: one step off my two sets
SETS = {"five": FIVE, "seven": SEVEN, "six": SIX}
class FreeSkin(L.Skin):
    """as lib12.Skin, with every target divided by the first mode's: the misses are frequency/(target x base) - 1, base = (1,1)/2"""
    def __init__(self, rings, modes, per=50):
        super().__init__(rings, modes, per); self.T = self.T / self.T[0]
def place(a, per=50):
    """the lowest mode's frequency over the base"""
    sk = FreeSkin(len(a), [(1, 1), (0, 1)], per); return float(sk.solve(np.asarray(a, float), grad=False)[0] + 1)
def exact(a, modes):
    """the overtone miss and the lowest mode's place by exact matching of Bessel functions across every ring edge"""
    r = L.exact_ratios(np.asarray(a, float), list(modes) + [(0, 1)]); T = np.array([L.target(m, n) for m, n in modes]); return float(np.abs(2 * r[1:-1] / T[1:] - 1).max()), float(2 * r[-1])
def disc_modes(s, k, modes):
    """one even disc (s times the skin inside radius k), exact: the overtone ratios to the base, and the lowest mode's place"""
    import drum
    w = drum.modes(float(s), float(k), list(modes) + [(0, 1)]); base = w[0] / 2; return [x / base for x in w[:-1]], w[-1] / base
def disc_miss(s, k, modes):
    r, pl = disc_modes(s, k, modes); return max(abs(x / L.target(m, n) - 1) for x, (m, n) in list(zip(r, modes))[1:]), pl

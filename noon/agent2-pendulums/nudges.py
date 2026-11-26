"""How far each strike is moved in the sound file: the random draws of piece.py replayed (same seed, same order).
   python -I nudges.py > nudges.out      (numpy)
Added 26 November 2026. The written list of notes is exactly steady; the sound is not quite."""
import sys; sys.dont_write_bytecode = True
import numpy as np
N = 16; T = 144.0; M = 36
rng = np.random.default_rng(7)
PITCH = [50, 52, 54, 57, 59, 62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86]
strikes = sorted((round(j * T / (M + k), 5), k, PITCH[k]) for k in range(N) for j in range(M + k + 1))
off = []
for t, k, m in strikes:
    rng.uniform(0.92, 1.04); off.append((t, k, rng.normal(0, 0.002)))
a = np.array([o for _, _, o in off]) * 1000
print('strikes', len(a), ' mean |nudge| %.2f ms, median |nudge| %.2f ms, largest %.2f ms, share over 4 ms %.3f' % (np.abs(a).mean(), np.median(np.abs(a)), np.abs(a).max(), (np.abs(a) > 4).mean()))
for t0 in (0.0, 144.0):
    c = np.array([o for t, _, o in off if t == t0]) * 1000
    print('chord at', t0, ': spread from first to last strike %.2f ms' % (c.max() - c.min()))

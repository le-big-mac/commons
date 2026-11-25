"""How the discord score of the web's sound depends on how mellow the pluck is.   usage: python tone_test.py   (writes test-*.wav here; run clash.py on them)"""
import sys, json
sys.path.insert(0, '/home/agent2/orbweb')
import numpy as np, orbweb as O
J = json.load(open('/home/agent2/orbweb/orb.json')); base = O.pluck
for name, width in (("a", 0.25), ("b", 0.40), ("c", 0.55)):
    def pluck(midi, dur, rng, bright=0.5, decay=0.996, width=width):
        f = 440 * 2 ** ((midi - 69) / 12); N = max(2, int(round(O.SR / f))); n = int(dur * O.SR) + N
        burst = rng.uniform(-1, 1, N); k = max(1, int(N * width * (1.3 - bright)))
        burst = np.convolve(np.r_[burst, burst, burst], np.hanning(k + 2)[1:-1] / max(1e-9, np.hanning(k + 2)[1:-1].sum()), mode='same')[N:2 * N]; burst -= burst.mean(); burst /= np.abs(burst).max()
        out = np.zeros(n); out[:N] = burst
        for i in range(N, n, N):
            seg = out[i - N:i]; nxt = 0.5 * decay * (seg + np.roll(seg, 1)); m = min(N, n - i); out[i:i + m] = nxt[:m]
        x = np.interp(np.arange(int(dur * O.SR)) * (f * (N + 0.5) / O.SR), np.arange(n), out)
        return x * np.minimum(np.arange(len(x)) / (0.002 * O.SR), 1) * np.minimum(1, (len(x) - np.arange(len(x))) / (0.05 * O.SR))
    O.pluck = pluck; O.sound(J, f'/home/agent2/orbweb/test-{name}.wav')

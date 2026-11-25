"""A second attempt at a number for "discordant": how much of the sound, over two-second windows, sits a semitone apart.
usage: python clash.py REF_A file.wav [REF_A file.wav ...]   (REF_A = 430 or 440: the tuning the file is in)
For each window: energy per pitch class c[0..11] (partials between 100 and 4000 Hz, within 35 cents of a pitch class);
semitone clash = sum_i c[i] c[i+1] / (sum c)^2 * 12; the same for the tritone and for the fifth, for comparison."""
import sys
import numpy as np
from scipy.signal import stft
from listen import load

for ref, path in zip(sys.argv[1::2], sys.argv[2::2]):
    sr, x = load(path)
    f, t, Z = stft(x, sr, nperseg=16384, noverlap=16384 - 4096)
    P = np.abs(Z) ** 2
    keep = (f > 100) & (f < 4000)
    pc = 12 * np.log2(f[keep] / float(ref))
    near = np.abs(pc - np.rint(pc)) < 0.35
    cls = (np.rint(pc).astype(int) % 12)[near]
    Pk = P[keep][near]
    C = np.zeros((12, P.shape[1]))
    np.add.at(C, cls, Pk)
    w = int(round(2.0 * sr / 4096))                                     # frames in two seconds
    Cw = np.stack([np.convolve(C[i], np.ones(w), mode='valid') for i in range(12)])
    tot = Cw.sum(0)
    ok = tot > 0.05 * np.median(tot)
    Cn = Cw[:, ok] / tot[ok]
    semi = 12 * (Cn * np.roll(Cn, -1, axis=0)).sum(0)
    trit = 12 * (Cn * np.roll(Cn, -6, axis=0)).sum(0)
    fifth = 12 * (Cn * np.roll(Cn, -7, axis=0)).sum(0)
    used = (Cn > 0.03).sum(0)
    print(f"{path.split('/')[-1]:26s} semitone clash {semi.mean():.3f} (90th pct {np.percentile(semi, 90):.3f}); tritone {trit.mean():.3f}; fifth {fifth.mean():.3f};"
          f" pitch classes sounding at once (median) {np.median(used):.0f}")

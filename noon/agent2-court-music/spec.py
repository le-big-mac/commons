"""Spectrogram of the whole piece and two close-ups.   usage: python spec.py court.wav events.json out.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import stft
from listen import load
sr, x = load(sys.argv[1])
ev = json.load(open(sys.argv[2]))
f, t, Z = stft(x, sr, nperseg=4096, noverlap=4096 - 512)
S = 20 * np.log10(np.abs(Z) + 1e-9)
S -= S.max()
keep = (f >= 50) & (f <= 8000)
fig, axes = plt.subplots(3, 1, figsize=(15, 13))
b = ev['beats']
for ax, (t0, t1, title) in zip(axes, ((0, ev['TOTAL'], 'whole piece'), (ev['T_NETORI'] - 2, b[32] + 1, 'the first two phrases'), (b[176] - 1, ev['TOTAL'], 'the last phrase and the ending'))):
    k = (t >= t0) & (t <= t1)
    ax.pcolormesh(t[k], f[keep], S[keep][:, k], cmap='magma', vmin=-80, vmax=-10, shading='auto', rasterized=True)
    ax.set_yscale('log'), ax.set_ylim(50, 8000), ax.set_yticks([100, 200, 430, 860, 1720, 3440, 6880]), ax.set_yticklabels(['100', '200', '430', '860', '1720', '3440', '6880'])
    ax.set_title(title, loc='left'), ax.set_ylabel('Hz')
    for bb in b[::16]:
        if t0 <= bb <= t1:
            ax.axvline(bb, color='white', lw=0.5, alpha=0.5)
axes[-1].set_xlabel('seconds')
fig.tight_layout()
fig.savefig(sys.argv[3], dpi=75)

"""The piece as a scrolling score with its sound.   usage: python video.py events.json breath-apportioned.mp3 out.mp4

One long strip is drawn (pitch against time above, the three drums below), 40 pixels to the second, and ffmpeg
slides a 1280 x 720 window along it under a fixed line: what is under the line is what is sounding."""
import sys, json, subprocess, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tuning import freq

ev = json.load(open(sys.argv[1]))
E, T0, T1, TOTAL, beats = ev['events'], ev['T_NETORI'], ev['T_END'], ev['TOTAL'], ev['beats']
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE, AQUA, SHO = "#2a78d6", "#eb6834", "#1baf7a", "#cfc9bd"
PPS, W, H, HEAD = 40, 1280, 720, 400                                    # pixels per second; window; where the line stands
DPI = 100
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID})
YT = ['E2', 'B2', 'E3', 'B3', 'E4', 'B4', 'E5', 'B5', 'E6', 'B6']
width = int(TOTAL * PPS) + W
a, b = -HEAD / PPS, (width - HEAD) / PPS                                # the strip's time range, with room before and after

sho = [e for e in E if e[0] == 'sho']
bars = []
for k, e in enumerate(sho):
    nxt = sho[k + 1][2] if k + 1 < len(sho) and sho[k + 1][2] > e[2] else None
    bars.append((e[2], nxt if nxt is not None else (40.5 if e[2] < T0 else T1 + 2.5), e[1], e[3]))

fig = plt.figure(figsize=(width / DPI, H / DPI), dpi=DPI)
ax = fig.add_axes([0, 0.27, 1, 0.62])
px = fig.add_axes([0, 0.06, 1, 0.17], sharex=ax)
ax.set_yscale('log'), ax.set_ylim(70, 2300), ax.set_xlim(a, b)
for axx in (ax, px):
    axx.set_xticks([]), axx.set_yticks([]), axx.minorticks_off()
    for sp in axx.spines.values():
        sp.set_visible(False)
for n in YT:
    ax.axhline(freq(n), color=GRID, lw=0.8, zorder=0)
for k, t in enumerate(beats[::4]):
    for axx in (ax, px):
        axx.axvline(t, color=GRID, lw=2.0 if k % 4 == 0 else 0.7, zorder=0)
names = {0: 'A: the flute alone, then the drums', 2: 'A again', 4: 'B', 6: 'B again', 8: 'C', 10: 'C again: the drums twice as fast'}
for p, name in names.items():
    ax.text(beats[16 * p] + 0.3, 1.03, name, fontsize=15, color=INK, va='bottom', fontweight='bold', transform=ax.get_xaxis_transform())
ax.text(0.3, 1.03, "prelude: one player at a time, no beat", fontsize=15, color=INK, va='bottom', fontweight='bold', transform=ax.get_xaxis_transform())
ax.text(T1 + 4.5, 1.03, "ending: the lute, then the koto, alone", fontsize=15, color=INK, va='bottom', fontweight='bold', transform=ax.get_xaxis_transform())
for t0, t1, name, notes in bars:
    for n in notes:
        f = freq(n)
        ax.fill_between([t0, t1], f * 0.98, f * 1.02, color=SHO, lw=0, zorder=1)
    ax.text(t0 + 0.15, freq(notes[-1]) * 1.07, name, fontsize=10, color=MUTED, va='bottom', zorder=2)
for e in E:
    if e[0] in ('hichiriki', 'ryuteki'):
        lf, am = np.array(e[3][0]), np.array(e[3][1])
        t = e[2] + np.arange(len(lf)) / 100.0
        ax.plot(t, np.where(am > 0.05, 2.0 ** lf, np.nan), color=BLUE if e[0] == 'hichiriki' else AQUA, lw=4.5, zorder=4 if e[0] == 'hichiriki' else 3, solid_capstyle='round')
    if e[0] == 'biwa':
        n = e[3]
        ax.plot(np.linspace(e[2] - 0.35, e[2], len(n)), [freq(x) for x in n], color=ORANGE, lw=1.6, marker='o', ms=7, zorder=5)
    if e[0] == 'koto':
        ax.plot([e[2]], [freq(e[3])], color=ORANGE, marker='D', ms=8, mfc='white', mew=2.2, ls='', zorder=5)
px.set_ylim(-0.6, 2.6)
for e in E:
    if e[0] == 'taiko':
        px.plot([e[2]], [0], marker='o', ms=22 if e[1] == 'strong' else 10, color=INK, ls='', zorder=3)
    if e[0] == 'kakko':
        px.plot([e[2], e[2]], [0.7, 0.7 + 0.65 * min(e[3], 1.0)], color=INK, lw=1.6, zorder=3)
    if e[0] == 'shoko' and e[3] > 0.9:
        px.plot([e[2]], [2], marker='|', ms=16, mew=2.4, color=INK, ls='', zorder=3)
fig.savefig('strip.png', dpi=DPI, facecolor='white')
plt.close(fig)

# the fixed panel on the left: what the rows are
fig = plt.figure(figsize=(1.9, H / DPI), dpi=DPI)
ax = fig.add_axes([0, 0.27, 1, 0.62])
px = fig.add_axes([0, 0.06, 1, 0.17])
ax.set_yscale('log'), ax.set_ylim(70, 2300), ax.set_xlim(0, 1)
px.set_ylim(-0.6, 2.6), px.set_xlim(0, 1)
for axx in (ax, px):
    axx.set_xticks([]), axx.set_yticks([]), axx.minorticks_off()
    for sp in axx.spines.values():
        sp.set_visible(False)
for n in YT:
    ax.text(0.93, freq(n), n, ha='right', va='center', fontsize=11, color=MUTED)
for y, col, name in ((freq('E6') * 1.25, AQUA, 'flute'), (freq('E5') * 0.8, BLUE, 'reed'), (freq('B5') * 1.12, MUTED, 'mouth organ'), (freq('E3') * 1.25, ORANGE, 'lute'), (freq('E4') * 1.3, ORANGE, 'koto')):
    ax.text(0.06, y, name, ha='left', va='center', fontsize=11.5, color=INK, fontweight='bold')
    ax.plot([0.06, 0.42], [y * 0.9, y * 0.9], color=col, lw=4, solid_capstyle='round')
for y, name in ((2, 'small gong'), (1, 'small drum'), (0, 'big drum')):
    px.text(0.93, y, name, ha='right', va='center', fontsize=11.5, color=INK)
fig.savefig('panel.png', dpi=DPI, facecolor='white')
plt.close(fig)

cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-loop', '1', '-framerate', '30', '-i', 'strip.png', '-loop', '1', '-framerate', '30', '-i', 'panel.png', '-i', sys.argv[2],
       '-filter_complex',
       f"[0:v]crop={W}:{H}:'min(t*{PPS},iw-{W})':0[s];[s][1:v]overlay=0:0[o];[o]drawbox=x={HEAD}:y=60:w=2:h={H - 100}:color=0x2b2622@0.9:t=fill[v]",
       '-map', '[v]', '-map', '2:a', '-t', f"{TOTAL:.2f}", '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', sys.argv[3]]
subprocess.run(cmd, check=True)
print("strip", width, "x", H, "pixels; video", sys.argv[3], os.path.getsize(sys.argv[3]), "bytes")

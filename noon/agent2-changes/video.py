"""The piece as a picture that follows the sound.   usage: python video.py changes.json changes.mp3 out.mp4
The 120 rows stand on the screen in three columns; the row being rung is lit, and the bell being struck is ringed."""
import sys, json, subprocess, io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
D = json.load(open(sys.argv[1])); rows = D['rows']; calls = D['calls']; strikes = D['strikes']
INK, MUTED, GRID, BLUE, ORANGE = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834"
W, H, FPS = 1280, 720, 15
X0 = [150, 550, 950]; DX = 40; Y0 = 112; DY = 14.2
pos = lambda c, k, place: (X0[c] + (place - 1) * DX, Y0 + k * DY)
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK})
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
for c in range(3):
    part = rows[c * 40:(c + 1) * 40] + [rows[(c + 1) * 40] if (c + 1) * 40 < 120 else [1, 2, 3, 4, 5]]
    for bell, col in ((1, ORANGE), (2, BLUE)):
        ax.plot([pos(c, k, r.index(bell) + 1)[0] for k, r in enumerate(part)], [pos(c, k, 1)[1] for k in range(len(part))], color=col, lw=2.2, zorder=1, solid_capstyle='round', solid_joinstyle='round')
    for k, r in enumerate(part):
        for place, b in enumerate(list(r) + [6], 1):
            x, y = pos(c, k, place)
            ax.text(x, y, str(b), ha='center', va='center', fontsize=9.5, family='DejaVu Sans Mono', color=MUTED if (k == 40 or b == 6) else INK, fontweight='bold' if b in (1, 2) and k < 40 else 'normal',
                    bbox=dict(facecolor='white', edgecolor='none', pad=0.8), zorder=3)
    for lead in range(4):
        y = Y0 + (lead * 10 + 9.5) * DY
        ax.plot([X0[c] - 24, X0[c] + 5 * DX + 24], [y, y], color=GRID, lw=1, zorder=0)
        if calls[c * 4 + lead] == 'B':
            ax.text(X0[c] + 5 * DX + 34, y, "bob", fontsize=9, color=INK, va='center', ha='left')
ax.text(60, 40, "All 120 orders of five bells, each rung once", fontsize=17, color=INK, va='center')
ax.text(60, 72, "orange: the treble's path     blue: bell 2's path     6: the tenor, last in every row", fontsize=10.5, color=MUTED, va='center')
buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig)
bg = Image.open(buf).convert('RGB'); assert bg.size == (W, H), bg.size
mono = ImageFont.truetype(font_manager.findfont('DejaVu Sans Mono:bold'), 15); sans = ImageFont.truetype(font_manager.findfont('DejaVu Sans'), 17)
first = {}
for t, k, place, b in strikes:
    first.setdefault(k, t)
ks = sorted(first); starts = np.array([first[k] for k in ks]); st = np.array([s[0] for s in strikes])
total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', sys.argv[2]], capture_output=True, text=True).stdout)
def where(k):                                         # which diagram row shows row k of the piece (four rounds, the 120, four rounds)
    if k < 4:
        return 0, 0, "rounds"
    if k >= 124:
        return 2, 40, "rounds: home"
    r = k - 4
    return r // 40, r % 40, f"row {r + 1} of 120"
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', sys.argv[2],
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', sys.argv[3]], stdin=subprocess.PIPE)
n = int(total * FPS)
for f in range(n):
    t = f / FPS
    im = bg.copy(); d = ImageDraw.Draw(im, 'RGBA')
    i = int(np.searchsorted(starts, t, side='right')) - 1
    if i >= 0 and t < starts[-1] + 6 * D['beat'] + 1.0:
        c, k, label = where(ks[i])
        x, y = pos(c, k, 1)
        d.rounded_rectangle([x - 22, y - 7.5, x + 5 * DX + 22, y + 7.5], radius=6, fill=(43, 38, 34, 26))
        j = int(np.searchsorted(st, t, side='right')) - 1
        if j >= 0 and t - st[j] < 0.22 and strikes[j][1] == ks[i]:
            _, _, place, b = strikes[j]
            sx, sy = pos(c, k, place)
            d.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=(43, 38, 34, 255))
            d.text((sx, sy), str(b), font=mono, fill=(255, 255, 255, 255), anchor='mm')
        d.text((W - 60, 40), label, font=sans, fill=(111, 103, 94, 255), anchor='rm')
    ff.stdin.write(im.tobytes())
ff.stdin.close(); ff.wait()
print(n, "frames,", round(total, 1), "seconds")

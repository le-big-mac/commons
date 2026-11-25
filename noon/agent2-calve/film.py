"""A short film: three blocks of ice let go in the sea.   usage: python film.py berg.mp4
Hydrostatic forces only, with friction added so that the blocks come to rest; the friction is invented."""
import sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import berg
K = 2; W, Hh, FPS = 1280 * K, 720 * K, 30;      # drawn at twice the size and reduced, so that edges are smooth
OW, OH = 1280, 720; SEC = 30; UNITS = 90.0                     # 90 units of time in 30 seconds: 3 units a second (27 s of an 800 m block's time)
SKY, SEA, SEA2, ICE, EDGE, INK, MUTED = (236, 240, 243), (86, 132, 168), (58, 98, 134), (247, 250, 252), (150, 170, 186), (43, 38, 34), (111, 103, 94)
font = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", s * K)
BLOCKS = [(0.90, 14.0, "nine tenths as wide as tall", "rocks, and stays upright"), (0.745, 3.0, "three quarters as wide", "leans, and stays leaning"), (0.50, 2.0, "half as wide", "rolls over")]
dt = 0.004; every = int(round((UNITS / (SEC * FPS)) / dt)); tracks = []
for e, th0, _, _ in BLOCKS:
    M = e; I = M * (e * e + 1) / 12; tracks.append(berg.run(e, th0, UNITS, dt=dt, cy=0.22 * M, cth=0.22 * I, every=every))
n = min(len(t) for t in tracks); S = 250.0 * K; Y0 = 330 * K                      # pixels per block height; the water line's row
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", sys.argv[1]], stdin=subprocess.PIPE)
for k in range(n):
    im = Image.new("RGB", (W, Hh), SKY); dr = ImageDraw.Draw(im)
    for i, (e, th0, name, what) in enumerate(BLOCKS):
        t, y, th, vy, om = tracks[i][k]; cx = (230 + i * 410) * K; P = [(cx + S * px, Y0 - S * py) for px, py in berg.corners(e, -th, y)]      # drawn tilting to the right
        dr.polygon(P, fill=ICE); dr.line(P + [P[0]], fill=EDGE, width=K)
    sea = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); ds = ImageDraw.Draw(sea); ds.rectangle([0, Y0, W, Hh], fill=SEA + (150,)); ds.line([0, Y0, W, Y0], fill=SEA2 + (255,), width=2 * K)
    im = Image.alpha_composite(im.convert("RGBA"), sea).convert("RGB"); dr = ImageDraw.Draw(im)
    for i, (e, th0, name, what) in enumerate(BLOCKS):
        cx = (230 + i * 410) * K; t, y, th, vy, om = tracks[i][k]
        dr.text((cx, 636 * K), name, font=font(19), fill=(255, 255, 255), anchor="mm"); dr.text((cx, 664 * K), what if t > 6 else f"let go at {th0:g} degrees", font=font(16), fill=(214, 226, 236), anchor="mm")
    dr.text((40 * K, 26 * K), "Calved: three blocks of ice, let go", font=font(26), fill=INK); tt = tracks[0][k][0] * 9.03
    dr.text((40 * K, 62 * K), f"If the blocks are 800 m tall, this is {int(tt // 60)} min {int(tt % 60):02d} s after they were let go. The friction that brings them to rest is invented, and it sets the pace.", font=font(15), fill=MUTED)
    ff.stdin.write(im.resize((OW, OH), Image.LANCZOS).tobytes())
ff.stdin.close(); ff.wait(); print(n, "frames")
for i, (e, th0, _, _) in enumerate(BLOCKS): print(f"   e = {e}: let go at {th0} degrees; tilt at the end {math.degrees(tracks[i][n - 1][2]):.1f} degrees; greatest {np.degrees(tracks[i][:n, 2]).max():.1f}")

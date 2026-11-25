"""A film of three lattices from the same kind of start.   usage: python -I film.py snap snaplist.txt hawk.mp4"""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
snapdir, gens = sys.argv[1], [0] + [int(x) for x in open(sys.argv[2]).read().split()]
W, H, FPS = 1280, 720, 30; BG, INK, MUTED = (250, 248, 244), (43, 38, 34), (111, 103, 94); DOVE, HAWK = np.array([223, 233, 245], np.uint8), np.array([43, 38, 34], np.uint8)
font = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", s)
PAN = [("0.15", "r = 0.15", "well mixed: 85% doves"), ("0.50", "r = 0.50", "well mixed: 50% doves"), ("0.66", "r = 0.66", "well mixed: 34% doves")]
data = [np.fromfile(f"{snapdir}/s-{r}.bin", dtype=np.uint8).reshape(-1, 200, 200) for r, _, _ in PAN]; n = min(len(d) for d in data); assert n == len(gens), (n, len(gens))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28", sys.argv[3]], stdin=subprocess.PIPE)
frames = 0
for k in range(n):
    im = Image.new("RGB", (W, H), BG); dr = ImageDraw.Draw(im)
    dr.text((30, 22), "Hawks and doves with neighbours", font=font(26), fill=INK)
    dr.text((30, 58), f"Light: doves. Dark: hawks. Each site copies, now and then, a neighbour who is doing better. r is what a dove gives up.   Generation {gens[k]:,}", font=font(15), fill=MUTED)
    for i, (r, name, mixed) in enumerate(PAN):
        a = data[i][k]; rgb = np.where(a[..., None] == 1, DOVE, HAWK); x0 = 30 + i * 415; im.paste(Image.fromarray(rgb).resize((400, 400), Image.NEAREST), (x0, 110))
        dr.text((x0, 524), name, font=font(19), fill=INK); dr.text((x0, 552), f"doves now {100 * a.mean():.1f}%;  {mixed}", font=font(15), fill=MUTED)
    dr.text((30, 600), f"Time speeds up as the film goes on: the first seconds show a generation every tenth of a second, the last second before it stops some {round((gens[n - 1] - gens[n - 31]) / 100) * 100:,}.", font=font(15), fill=MUTED)
    rep = 3 if k < 60 else 1
    if k == n - 1: rep = 75
    for _ in range(rep): ff.stdin.write(im.tobytes()); frames += 1
ff.stdin.close(); ff.wait(); print(frames, "frames;", frames / FPS, "seconds")

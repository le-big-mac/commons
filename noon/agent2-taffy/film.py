"""A film of two taffy pullers side by side: a figure of eight round two rods (stretches) and two swaps the same way round (does not).
usage: python film.py out.mp4 [frame.png frame_index]      (also writes film.json: the lengths after every move)"""
import sys, os, json, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
import taffy as TF
W, H, SS, FPS = 1280, 720, 2, 30
INK, MUTED, GRID, ORANGE, BG = (43, 38, 34), (111, 103, 94), (228, 223, 214), (235, 104, 52), (251, 250, 247)
FONT = matplotlib.get_data_path() + "/fonts/ttf/DejaVuSans.ttf"
F = {s: ImageFont.truetype(FONT, s * SS) for s in (14, 16, 20, 28)}
MOVES_TOTAL, PER_MOVE, EVERY, DT = 16, 40, 5, 0.005           # 16 moves, 40 frames a move, a frame every 5 steps
PANELS = [("Left pair a full turn, then right pair a full turn the other way", 3, TF.DEVICES['T2'][1]), ("Left pair a half turn, then right pair a half turn the same way", 3, TF.DEVICES['T3'][1])]
SC = 118
def states(moves, n):
    x = TF.refine(TF.circle()); t = 0.0; L0 = TF.length(x); yield t, x, TF.rods(moves, n, 0.0)[0], L0
    for step in range(1, MOVES_TOTAL * int(round(1 / DT)) + 1):
        p1, v1 = TF.rods(moves, n, t); p2, v2 = TF.rods(moves, n, t + DT / 2); p3, v3 = TF.rods(moves, n, min(t + DT, math.floor(t) + 1 - 1e-12))
        k1 = TF.velocity(x, p1, v1); k2 = TF.velocity(x + 0.5 * DT * k1, p2, v2); k3 = TF.velocity(x + 0.5 * DT * k2, p2, v2); k4 = TF.velocity(x + DT * k3, p3, v3)
        x = TF.refine(x + (DT / 6) * (k1 + 2 * k2 + 2 * k3 + k4)); t = round(t + DT, 10)
        if step % EVERY == 0: yield t, x, TF.rods(moves, n, min(t, MOVES_TOTAL - 1e-9))[0], L0
def draw(dr, ox, title, t, x, p, L0, n):
    X = lambda q: ((ox + SC * (q[..., 0] + 1.45)) * SS, (330 - SC * q[..., 1]) * SS)
    dr.text((ox * SS, 118 * SS), title, font=F[16], fill=INK, anchor="ls")
    px, py = X(x); pts = np.stack([px, py], 1)
    if len(pts) > 400000: pts = pts[::2]                    # below a third of a pixel apart: every second point is enough
    dr.line([tuple(q) for q in pts] + [tuple(pts[0])], fill=ORANGE + (255,), width=int(1.3 * SS), joint=None)
    for q in p:
        cx, cy = X(q); r = 0.07 * SC * SS; dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK + (255,), outline=BG + (255,), width=SS)
    dr.text((ox * SS, 560 * SS), f"length × {TF.length(x) / L0:,.0f}", font=F[28], fill=INK, anchor="ls")
    dr.text(((ox + 560) * SS, 560 * SS), f"move {min(int(t) + 1, MOVES_TOTAL)} of {MOVES_TOTAL}", font=F[16], fill=MUTED, anchor="rs")
if __name__ == "__main__":
    gens = [states(m, n) for _, n, m in PANELS]; frames = MOVES_TOTAL * PER_MOVE + 1; lengths = [[] for _ in PANELS]
    only = int(sys.argv[3]) if len(sys.argv) > 3 else None
    ff = None if only is not None else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                                         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', sys.argv[1]], stdin=subprocess.PIPE)
    for f in range(frames):
        st = [next(g) for g in gens]
        for j, (t, x, p, L0) in enumerate(st):
            if f % PER_MOVE == 0: lengths[j].append(TF.length(x) / L0)
        if only is not None and f != only: continue
        im = Image.new("RGB", (W * SS, H * SS), BG); dr = ImageDraw.Draw(im, "RGBA")
        dr.text((60 * SS, 50 * SS), "Two ways to pull taffy", font=F[28], fill=INK, anchor="ls")
        dr.text((60 * SS, 80 * SS), "The orange line is a loop of candy, carried by a model fluid that moves with the rods. Same number of moves on both sides.", font=F[16], fill=MUTED, anchor="ls")
        for j, (t, x, p, L0) in enumerate(st): draw(dr, 60 + 610 * j, PANELS[j][0], t, x, p, L0, PANELS[j][1])
        dr.text((60 * SS, 660 * SS), "Left: folded back on itself at every trip, as its braid demands. Right: the braid demands nothing; this fluid still stretches it, more slowly.", font=F[16], fill=INK, anchor="ls")
        out = im.resize((W, H), Image.LANCZOS)
        if only is not None: out.save(sys.argv[2]); break
        reps = 30 if f == 0 else 105 if f == frames - 1 else 1          # hold the first and the last picture
        for _ in range(reps): ff.stdin.write(out.tobytes())
    if ff: ff.stdin.close(); ff.wait(); json.dump(dict(moves=MOVES_TOTAL, lengths=lengths), open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'film.json'), 'w')); print(f"{frames} pictures; lengths after each move saved")

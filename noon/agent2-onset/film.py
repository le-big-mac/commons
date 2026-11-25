"""A film of the bell piece: each bell a dot going round, striking as it passes the top.
usage: python film.py step.json step.npz step.wav out.mp4 [frame.png seconds]"""
import sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
J = json.load(open(sys.argv[1])); PH = np.load(sys.argv[2])['phases']; WAV, OUT = sys.argv[3], sys.argv[4]
W, H, SS, FPS = 1280, 720, 2, 30
INK, MUTED, GRID, NEUTRAL, BLUE, ORANGE, BG = (43, 38, 34), (111, 103, 94), (228, 223, 214), (185, 177, 165), (42, 120, 214), (235, 104, 52), (251, 250, 247)
FONT = matplotlib.get_data_path() + "/fonts/ttf/DejaVuSans.ttf"
F = {s: ImageFont.truetype(FONT, s * SS) for s in (14, 16, 20, 28)}
N, LEAD, TEND = J['N'], J['lead'], J['tend']; T1, T2, T3, KMAX = J['t1'], J['t2'], J['t3'], J['kmax']
r = np.array(J['r']); tr = np.arange(len(r)) * J['r_dt']
strikes = [[] for _ in range(N)]
for t, i, m in J['strikes']: strikes[i].append(t)
strikes = [np.array(s) for s in strikes]
lo, hi = min(J['pitch']), max(J['pitch'])
def colour(m):                                       # one hue, dark for the low bells, light for the high ones
    k = (m - lo) / (hi - lo); a, b = (18, 62, 125), (150, 196, 245)
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
def coupling(t):
    return 0.0 if t < T1 or t >= T3 else KMAX * min(1.0, (t - T1) / (T2 - T1))
def caption(t):
    if t < T1: return "No coupling: each bell keeps its own time."
    if t < T1 + (T2 - T1) / KMAX: return "The bells begin to feel each other. Below the critical coupling nothing much happens."
    if t < T2: return "Past the critical coupling a common beat grows, the middle tempos first."
    if t < T3: return "Held at three times critical: one chord, rolled from the fastest bell (lowest) to the slowest."
    return "Let go: each bell returns to its own time."
CX, CY, RAD = 330, 385, 215
PX0, PX1 = 700, 1220
def chart(dr, y0, y1, ymax, title, series_t, series_y, now, col, dashed=None):
    X = lambda t: (PX0 + (PX1 - PX0) * t / TEND) * SS; Y = lambda v: (y1 - (y1 - y0) * v / ymax) * SS
    dr.text((PX0 * SS, (y0 - 12) * SS), title, font=F[16], fill=INK, anchor="ls")
    for v in range(int(ymax) + 1):
        dr.line([(PX0 * SS, Y(v)), (PX1 * SS, Y(v))], fill=GRID, width=SS); dr.text(((PX0 - 8) * SS, Y(v)), str(v), font=F[14], fill=MUTED, anchor="rm")
    if dashed is not None:
        for x in range(PX0, PX1, 12): dr.line([(x * SS, Y(dashed)), ((x + 6) * SS, Y(dashed))], fill=NEUTRAL, width=SS)
    k = series_t <= now
    pts = [(X(a), Y(b)) for a, b in zip(series_t[k], series_y[k])]
    if len(pts) > 1: dr.line(pts, fill=col, width=int(2 * SS), joint="curve")
    if pts: dr.ellipse([pts[-1][0] - 4 * SS, pts[-1][1] - 4 * SS, pts[-1][0] + 4 * SS, pts[-1][1] + 4 * SS], fill=col)
KT = np.linspace(0, TEND, 1200); KV = np.array([coupling(t) for t in KT])
def frame(tau):
    t = max(0.0, tau - LEAD); th = PH[min(len(PH) - 1, int(round(t * 30)))]
    im = Image.new("RGB", (W * SS, H * SS), BG); dr = ImageDraw.Draw(im, "RGBA")
    dr.text((60 * SS, 50 * SS), "Falling into step", font=F[28], fill=INK, anchor="ls")
    dr.text((60 * SS, 80 * SS), "Twenty-four bells, each a dot going round at its own tempo. A bell strikes when its dot passes the top.", font=F[16], fill=MUTED, anchor="ls")
    dr.ellipse([(CX - RAD) * SS, (CY - RAD) * SS, (CX + RAD) * SS, (CY + RAD) * SS], outline=GRID, width=int(1.5 * SS))
    dr.line([(CX * SS, (CY - RAD - 16) * SS), (CX * SS, (CY - RAD + 16) * SS)], fill=INK, width=int(1.5 * SS))
    z = np.exp(1j * th).mean()                         # the common beat: an arrow whose length is r
    ax, ay = CX + RAD * z.imag, CY - RAD * z.real
    dr.line([(CX * SS, CY * SS), (ax * SS, ay * SS)], fill=ORANGE + (255,), width=int(3 * SS)); dr.ellipse([(ax - 5) * SS, (ay - 5) * SS, (ax + 5) * SS, (ay + 5) * SS], fill=ORANGE + (255,))
    order = np.argsort([-(t - s[s <= t][-1]) if (s <= t).any() else -99 for s in strikes])    # draw the bells that have just struck last, on top
    for i in order:
        x, y = CX + RAD * math.sin(th[i]), CY - RAD * math.cos(th[i]); s = strikes[i]; since = t - s[s <= t][-1] if (s <= t).any() else 9
        c = colour(J['pitch'][i])
        if since < 0.6:
            g = 1 - since / 0.6; rr = 9 + 16 * g
            dr.ellipse([(x - rr) * SS, (y - rr) * SS, (x + rr) * SS, (y + rr) * SS], fill=c + (int(110 * g),))
        dr.ellipse([(x - 8) * SS, (y - 8) * SS, (x + 8) * SS, (y + 8) * SS], fill=c + (255,), outline=BG + (255,), width=SS)
    dr.text((60 * SS, (CY + RAD + 36) * SS), "Dark dots: the low bells, which are the faster ones.", font=F[14], fill=MUTED, anchor="ls")
    dr.text((60 * SS, (CY + RAD + 56) * SS), "Orange arrow: the common beat. Its length is r.", font=F[14], fill=MUTED, anchor="ls")
    chart(dr, 170, 300, 3, "coupling (1 = the critical value)", KT, KV, t, INK, dashed=1)
    chart(dr, 380, 510, 1, "how far in step: r, from 0 (no common beat) to 1 (all together)", tr, r, t, ORANGE)
    for v in (0, 60, 120, 180):
        dr.text(((PX0 + (PX1 - PX0) * v / TEND) * SS, 530 * SS), f"{v} s", font=F[14], fill=MUTED, anchor="ms")
    dr.text((60 * SS, 690 * SS), caption(t), font=F[20], fill=INK, anchor="ls")
    return im.resize((W, H), Image.LANCZOS)
if __name__ == "__main__":
    if len(sys.argv) > 5:
        frame(float(sys.argv[6])).save(sys.argv[5]); sys.exit()
    total = TEND + 5.5
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', WAV,
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait(); print(f"{total:.1f} seconds, {int(total * FPS)} frames")

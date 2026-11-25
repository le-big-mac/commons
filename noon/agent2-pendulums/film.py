"""A film of the pendulum wave: sixteen dots swinging, each sounding at the top of its swing.
usage: python film.py pendula.json pendula.wav out.mp4 [frame.png seconds]"""
import sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
J = json.load(open(sys.argv[1])); WAV, OUT = sys.argv[2], sys.argv[3]
W, H, SS, FPS = 1280, 720, 2, 30
INK, MUTED, GRID, NEUTRAL, ORANGE, BG = (43, 38, 34), (111, 103, 94), (228, 223, 214), (185, 177, 165), (235, 104, 52), (251, 250, 247)
FONT = matplotlib.get_data_path() + "/fonts/ttf/DejaVuSans.ttf"
F = {s: ImageFont.truetype(FONT, s * SS) for s in (14, 16, 20, 28)}
N, T, M, LEAD, TAIL = J['N'], J['T'], J['M'], J['lead'], J['tail']
def colour(k):                                        # one hue, dark for the low voices, light for the high ones
    a, b = (18, 62, 125), (150, 196, 245); x = k / (N - 1)
    return tuple(int(a[i] + (b[i] - a[i]) * x) for i in range(3))
MARKS = [(0, "all"), (1 / 4, "every 4th"), (1 / 3, "every 3rd"), (1 / 2, "every 2nd"), (2 / 3, "every 3rd"), (3 / 4, "every 4th"), (1, "all")]
def caption(t):
    for f, words in ((0, "All sixteen together."), (1 / 4, "A quarter of the way: every fourth voice together."), (1 / 3, "A third of the way: every third voice together."),
                     (1 / 2, "Half way: every second voice together. From here it runs backwards."), (2 / 3, "Two thirds: every third voice together."),
                     (3 / 4, "Three quarters: every fourth voice together."), (1, "All sixteen together again.")):
        if abs(t - f * T) < 2.2: return words
    return "Drifting: the fastest voice (highest, right) gains one turn on its neighbour in 144 seconds." if t < T / 2 else "Drifting back."
X0, X1, YC, AMP = 150, 1130, 330, 150
def frame(tau):
    t = min(max(tau - LEAD, 0.0), T)
    im = Image.new("RGB", (W * SS, H * SS), BG); dr = ImageDraw.Draw(im, "RGBA")
    dr.text((60 * SS, 50 * SS), "Sixteen pendulums", font=F[28], fill=INK, anchor="ls")
    dr.text((60 * SS, 80 * SS), f"Voice k makes {M} + k turns in {T:.0f} seconds and sounds each time it reaches the top. Nothing pulls them together.", font=F[16], fill=MUTED, anchor="ls")
    dr.line([(X0 - 40) * SS, (YC - AMP) * SS, (X1 + 40) * SS, (YC - AMP) * SS], fill=GRID, width=int(1.5 * SS))
    dr.text(((X1 + 48) * SS, (YC - AMP) * SS), "top", font=F[14], fill=MUTED, anchor="lm")
    for k in range(N):
        x = X0 + (X1 - X0) * k / (N - 1); turns = (M + k) * t / T; th = 2 * math.pi * turns; y = YC - AMP * math.cos(th)
        dr.line([x * SS, (YC - AMP) * SS, x * SS, (YC + AMP) * SS], fill=GRID, width=SS)
        since = 9 if tau < LEAD else tau - LEAD - T if tau >= LEAD + T else (turns - math.floor(turns + 1e-9)) * T / (M + k)      # after the last chord the glow fades
        c = colour(k)
        if since < 0.5:
            g = 1 - since / 0.5; rr = 13 + 20 * g
            dr.ellipse([(x - rr) * SS, (y - rr) * SS, (x + rr) * SS, (y + rr) * SS], fill=c + (int(120 * g),))
        dr.ellipse([(x - 12) * SS, (y - 12) * SS, (x + 12) * SS, (y + 12) * SS], fill=c + (255,), outline=BG + (255,), width=SS)
    dr.text((X0 * SS, (YC + AMP + 34) * SS), "low, slow", font=F[14], fill=MUTED, anchor="ms"); dr.text((X1 * SS, (YC + AMP + 34) * SS), "high, fast", font=F[14], fill=MUTED, anchor="ms")
    yb = 610; X = lambda f: (X0 + (X1 - X0) * f) * SS
    dr.line([X(0), yb * SS, X(1), yb * SS], fill=NEUTRAL, width=int(2 * SS))
    for f, lab in MARKS:
        dr.line([X(f), (yb - 6) * SS, X(f), (yb + 6) * SS], fill=INK, width=int(1.5 * SS)); dr.text((X(f), (yb + 26) * SS), lab, font=F[14], fill=MUTED, anchor="ms")
    dr.polygon([(X(t / T), (yb - 9) * SS), (X(t / T) - 8 * SS, (yb - 25) * SS), (X(t / T) + 8 * SS, (yb - 25) * SS)], fill=ORANGE + (255,))
    dr.text((60 * SS, 690 * SS), caption(t), font=F[20], fill=INK, anchor="ls")
    dr.text(((W - 60) * SS, 690 * SS), f"{t:5.1f} s", font=F[16], fill=MUTED, anchor="rs")
    return im.resize((W, H), Image.LANCZOS)
if __name__ == "__main__":
    if len(sys.argv) > 4:
        frame(float(sys.argv[5])).save(sys.argv[4]); sys.exit()
    total = LEAD + T + TAIL
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', WAV,
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait(); print(f"{total:.1f} seconds, {int(total * FPS)} frames")

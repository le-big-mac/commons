"""Orb web: a drawing of a web being spun, each thread plucked as it is laid.
usage: python orbweb.py build orb.json | python orbweb.py sound orb.json orb.wav | python orbweb.py film orb.json orb.wav orb.mp4 [frame.png seconds]
The order of work is the textbook one (first lines, frame, radii, a wide scaffold spiral outward, the sticky spiral inward while the scaffold is
taken up).  The shapes, the timing and the notes are invented."""
import sys, json, math, wave, subprocess
import numpy as np

# ------------------------------------------------------------------ geometry and timeline
H = np.array([0.0, 0.16])                                           # the hub, a little above the middle
FRAME = np.array([(-1.05, 0.98), (1.0, 1.02), (1.32, 0.15), (0.95, -0.95), (-0.2, -1.2), (-1.15, -0.8), (-1.3, 0.2)])
MOOR = {0: (-3.3, 0.936), 1: (3.3, 1.065), 2: (3.3, 0.0), 3: (1.9, -1.7), 4: (-0.27, -1.7), 5: (-2.4, -1.7), 6: (-3.3, 0.35)}      # 0 and 1 lie on the line of the top edge: the bridge is the top of the frame; all run off the picture
NR, AUX_TURNS, CAP_TURNS = 30, 5, 20
def ray(phi):
    d = np.array([math.cos(phi), math.sin(phi)]); best = None
    for a, b in zip(FRAME, np.roll(FRAME, -1, axis=0)):
        e = b - a; den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12: continue
        t = ((a[0] - H[0]) * e[1] - (a[1] - H[1]) * e[0]) / den; u = ((a[0] - H[0]) * d[1] - (a[1] - H[1]) * d[0]) / den
        if t > 0 and -1e-9 <= u <= 1 + 1e-9 and (best is None or t < best): best = t
    return best
def build():
    rng = np.random.default_rng(3)
    phi = np.radians(90 + 12 * np.arange(NR) + rng.uniform(-2.5, 2.5, NR)); phi[0] = math.radians(90); phi[15] = math.radians(270)
    R = np.array([ray(p) for p in phi]); P = lambda k, rho: (H + rho * R[k % NR] * np.array([math.cos(phi[k % NR]), math.sin(phi[k % NR])])).tolist()
    segs = []; notes = []; t = 1.0
    def add(kind, p, q, dur, **kw):
        nonlocal t
        segs.append(dict(kind=kind, p=list(map(float, p)), q=list(map(float, q)), t0=t, t1=t + dur, **kw)); t += dur
    # first lines: the bridge, with its moorings, and a line dropped through the hub
    notes.append((t, 'low', 0)); add('frame', MOOR[0], MOOR[1], 2.2)
    notes.append((t, 'low', 2)); add('radius', P(0, 1.0), P(15, 1.0), 1.8)
    t += 0.3
    # the frame and its moorings
    for i in (1, 2, 3, 4, 5, 6):
        notes.append((t, 'low', i)); add('frame', FRAME[i], FRAME[(i + 1) % 7], 0.55)
        if i not in (1,): add('frame', FRAME[i], MOOR[i], 0.3)
    t += 0.3
    # radii: each new one where the gap is widest, so the pull stays balanced
    done = [0, 15]; order = []
    while len(done) < NR:
        gap = lambda k: min(abs((phi[k] - phi[j] + math.pi) % (2 * math.pi) - math.pi) for j in done)
        k = max((k for k in range(NR) if k not in done), key=gap); done.append(k); order.append(k)
    for k in order:
        notes.append((t, 'radius', k)); add('radius', P(k, 0.0), P(k, 1.0), 0.36)
    t += 0.4
    steps = lambda turns: int(turns * NR)
    for s in range(steps(3)):                                       # a few tight loops at the hub
        a, b = 0.03 + 0.09 * s / steps(3), 0.03 + 0.09 * (s + 1) / steps(3); add('hub', P(s, a), P(s + 1, b), 0.02)
    t += 0.3
    aux = []
    for s in range(steps(AUX_TURNS)):                               # the scaffold spiral, outward
        a, b = 0.17 + 0.73 * s / steps(AUX_TURNS), 0.17 + 0.73 * (s + 1) / steps(AUX_TURNS)
        add('aux', P(s, a), P(s + 1, b), 6.0 / steps(AUX_TURNS)); segs[-1]['sector'] = s % NR; segs[-1]['rho'] = (a + b) / 2; aux.append(segs[-1])
    t += 0.5
    add('walk', P(steps(AUX_TURNS), 0.90), P(steps(AUX_TURNS), 0.945), 0.4)
    t_cap = t
    for s in range(steps(CAP_TURNS)):                               # the sticky spiral, inward, the other way round
        a, b = 0.945 - 0.645 * s / steps(CAP_TURNS), 0.945 - 0.645 * (s + 1) / steps(CAP_TURNS); k0 = steps(AUX_TURNS) - s
        add('capture', P(k0, a), P(k0 - 1, b), 24.0 / steps(CAP_TURNS)); segs[-1]['rho'] = (a + b) / 2
        sector = (k0 - 1) % NR
        for x in aux:                                               # the scaffold is taken up where she meets it
            if 'gone' not in x and x['sector'] == sector and x['rho'] >= b - 0.012: x['gone'] = t
        if s % 5 == 0: notes.append((t, 'capture', (a + b) / 2))
    for x in aux: x.setdefault('gone', t)
    t_done = t
    add('walk', P(steps(AUX_TURNS) - steps(CAP_TURNS), 0.30), H, 1.6)
    t_home = t; notes.append((t + 0.4, 'chord', 0))
    return dict(H=H.tolist(), phi=phi.tolist(), R=R.tolist(), segs=segs, notes=notes, t_cap=t_cap, t_done=t_done, t_home=t_home, t_dawn=t_home + 1.5, t_end=t_home + 9.5,
                frame_len=[float(np.linalg.norm(FRAME[(i + 1) % 7] - FRAME[i])) for i in range(7)])

# ------------------------------------------------------------------ sound: plucked strings
SR = 44100
PENTA = [0, 2, 4, 7, 9]
def scale(lo_midi, n): return [lo_midi + 12 * (i // 5) + PENTA[i % 5] for i in range(n)]
def pluck(midi, dur, rng, bright=0.5, decay=0.996):
    f = 440 * 2 ** ((midi - 69) / 12); N = max(2, int(round(SR / f))); n = int(dur * SR) + N
    burst = rng.uniform(-1, 1, N); k = max(1, int(N * 0.40 * (1.3 - bright)))            # a soft pluck: the burst is smoothed over a good part of the period,
    win = np.hanning(k + 2)[1:-1]                                                          # which takes most of the upper overtones out (see tone_test.py)
    burst = np.convolve(np.r_[burst, burst, burst], win / win.sum(), mode='same')[N:2 * N]; burst -= burst.mean(); burst /= np.abs(burst).max()
    out = np.zeros(n); out[:N] = burst
    for i in range(N, n, N):
        seg = out[i - N:i]; nxt = 0.5 * decay * (seg + np.roll(seg, 1)); m = min(N, n - i); out[i:i + m] = nxt[:m]
    x = np.interp(np.arange(int(dur * SR)) * (f * (N + 0.5) / SR), np.arange(n), out)  # the loop is N + 1/2 samples long (the averaging adds half a sample): resample to the true pitch
    return x * np.minimum(np.arange(len(x)) / (0.002 * SR), 1) * np.minimum(1, (len(x) - np.arange(len(x))) / (0.05 * SR))
def sound(J, path):
    from scipy.signal import fftconvolve, lfilter
    rng = np.random.default_rng(5); T = J['t_end'] + 1.0; L = np.zeros(int(T * SR)); Rr = L.copy()
    R = np.array(J['R']); rank = np.argsort(np.argsort(-R))                         # 0 = the longest radius
    rad_notes = scale(50, 11)                                                       # D3 ... D5
    cap_notes = scale(62, 11)                                                       # D4 ... D6
    def put(t, x, g, pan):
        i = int(t * SR); a = (pan + 1) * math.pi / 4; m = min(len(x), len(L) - i)
        L[i:i + m] += x[:m] * g * math.cos(a); Rr[i:i + m] += x[:m] * g * math.sin(a)
    for t, kind, v in J['notes']:
        if kind == 'low': put(t, pluck([38, 45, 47, 40, 38, 42, 45][v], 4.0, rng, bright=0.25, decay=0.998), 0.55, 0.0)          # D2 A2 B2 E2 D2 F#2 A2: all in the scale
        elif kind == 'radius': put(t, pluck(rad_notes[int(rank[v] * 11 / len(R))], 2.6, rng, bright=0.5), 0.42, 0.7 * math.cos(J['phi'][v]))
        elif kind == 'capture': put(t, pluck(cap_notes[min(10, int((0.945 - v) / 0.645 * 11))], 1.4, rng, bright=0.65, decay=0.994), 0.2, 0.5 * math.sin(7 * v))
        elif kind == 'chord':
            for j, m in enumerate((50, 57, 62, 66, 69, 74)): put(t + 0.22 * j, pluck(m, 6.0, rng, bright=0.4, decay=0.9985), 0.36, -0.5 + 0.2 * j)
    n = int(2.2 * SR); ir = rng.normal(size=(2, n)) * np.exp(-np.arange(n) / SR / 0.5); ir[:, :int(0.01 * SR)] = 0; ir = lfilter([0.12], [1, -0.88], ir, axis=1)
    for ch, c in ((L, 0), (Rr, 1)): ch += 0.28 * fftconvolve(ch, ir[c])[:len(ch)] / np.sqrt((ir[c] ** 2).sum())
    x = np.stack([L, Rr], 1); x = np.tanh(x / np.abs(x).max() * 1.5) / np.tanh(1.5) * 0.7; fo = np.linspace(1, 0, int(2.5 * SR)); x[-len(fo):] *= fo[:, None]
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
    print(f"{len(J['notes'])} plucked notes, {T:.1f} seconds")

# ------------------------------------------------------------------ film
def film(J, wav, out, still=None, still_t=None):
    from PIL import Image, ImageDraw, ImageFont
    import matplotlib, colorsys
    W, Hh, SS, FPS, SC = 1280, 720, 2, 30, 215
    INK, MUTED, THREAD, AUXC, BG = (43, 38, 34), (111, 103, 94), (92, 86, 80), (176, 168, 157), (251, 250, 247)
    FONT = matplotlib.get_data_path() + "/fonts/ttf/DejaVuSans.ttf"; F = {s: ImageFont.truetype(FONT, s * SS) for s in (15, 20, 28)}
    X = lambda p: ((W / 2 + 40 + SC * p[0]) * SS, (Hh / 2 + 28 - SC * p[1]) * SS)
    segs = J['segs']; T = J['t_end']; rng = np.random.default_rng(1)
    beads = []                                                      # the droplets on the sticky spiral: position, time laid, a hue and a phase for the morning
    for s in segs:
        if s['kind'] == 'capture':
            p, q = np.array(s['p']), np.array(s['q']); n = max(1, int(np.linalg.norm(q - p) * SC / 6))
            for j in range(n): beads.append(((p + (q - p) * (j + 0.5) / n).tolist(), s['t0'] + (s['t1'] - s['t0']) * (j + 0.5) / n, rng.random(), rng.random()))
    def caption(t):
        k = [s for s in segs if s['t0'] <= t]
        if t < 1.0 or not k: return "An orb web, from the first line."
        last = k[-1]; i = segs.index(last)
        if i == 0: return "A first line across."
        if i == 1: return "A line dropped through what will be the hub."
        if last['kind'] == 'frame': return "The frame, and the lines that moor it."
        if last['kind'] == 'radius': return "The radii, each laid where the gap is widest."
        if last['kind'] == 'hub': return "A few tight loops at the hub."
        if last['kind'] == 'aux': return "A wide scaffold spiral, from the hub outward."
        if t < J['t_done']: return "The sticky spiral, from the outside in. The scaffold is taken up as she meets it."
        if t < J['t_dawn']: return "Done. She goes to the hub to wait."
        return "Morning."
    base = Image.new("RGB", (W * SS, Hh * SS), BG); bd = ImageDraw.Draw(base, "RGBA"); drawn = set()
    def spider(dr, pos, ang, a=255):
        x, y = X(pos); u = np.array([math.cos(ang), -math.sin(ang)]); v = np.array([-u[1], u[0]])
        for j, (off, ln) in enumerate(((-0.9, 15), (-0.35, 17), (0.25, 17), (0.8, 15))):
            for side in (-1, 1):
                root = np.array([x, y]) + u * off * 5 * SS; knee = root + (v * side * 0.75 + u * (off * 0.5)) * ln * 0.55 * SS; tip = knee + (v * side * 0.55 + u * (off * 0.9)) * ln * 0.6 * SS
                dr.line([tuple(root), tuple(knee), tuple(tip)], fill=INK + (a,), width=int(1.3 * SS))
        for c, r in ((-5.5, 6.5), (3.5, 4.2)):
            cx, cy = np.array([x, y]) + u * c * SS; dr.ellipse([cx - r * SS, cy - r * SS, cx + r * SS, cy + r * SS], fill=INK + (a,))
    def frame(t):
        for i, s in enumerate(segs):                                # finished permanent threads go on the base once
            if i not in drawn and s['t1'] <= t and s['kind'] in ('frame', 'radius', 'hub', 'capture'):
                bd.line([X(s['p']), X(s['q'])], fill=THREAD + (255,), width=int((1.5 if s['kind'] == 'frame' else 1.1) * SS)); drawn.add(i)
        im = base.copy(); dr = ImageDraw.Draw(im, "RGBA"); pos, ang = None, math.pi / 2
        if t >= J['t_dawn']:                                        # morning light
            g = min(1.0, (t - J['t_dawn']) / 4.0); dr.rectangle([0, 0, W * SS, Hh * SS], fill=(255, 214, 150, int(46 * g)))
        for s in segs:
            if s['t0'] > t: break
            if s['kind'] == 'aux' and s['t1'] <= t and t < s['gone']: dr.line([X(s['p']), X(s['q'])], fill=AUXC + (255,), width=SS)
            if s['t0'] <= t < s['t1']:
                f = (t - s['t0']) / (s['t1'] - s['t0']); p, q = np.array(s['p']), np.array(s['q']); m = p + (q - p) * f
                if s['kind'] != 'walk': dr.line([X(p), X(m)], fill=(AUXC if s['kind'] == 'aux' else THREAD) + (255,), width=int(1.1 * SS))
                pos = m; ang = math.atan2(q[1] - p[1], q[0] - p[0])
        for (p, tb, hue, ph) in beads:
            if tb > t: continue
            x, y = X(p)
            if t < J['t_dawn']: dr.ellipse([x - 1.5 * SS, y - 1.5 * SS, x + 1.5 * SS, y + 1.5 * SS], fill=(150, 160, 172, 255))
            else:
                g = min(1.0, (t - J['t_dawn']) / 4.0); tw = 0.5 + 0.5 * math.sin(2 * math.pi * (0.3 * t + ph)); r = (1.5 + 1.0 * g * tw ** 3) * SS
                c = colorsys.hsv_to_rgb(0.11 if hue < 0.5 else 0.58, 0.38 * g * tw ** 3, 1.0); dr.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(255 * v) for v in c) + (255,), outline=(168, 176, 186, 255))
        if pos is None:
            last = [s for s in segs if s['t1'] <= t]; pos = np.array(last[-1]['q']) if last else np.array(MOOR[0]); ang = -math.pi / 2 if t >= J['t_home'] else math.pi / 2
        spider(dr, pos, ang)
        dr.text((60 * SS, 52 * SS), "Orb web", font=F[28], fill=INK, anchor="ls")
        dr.text((60 * SS, 80 * SS), "A drawing, not a spider: the order of work is the textbook one,", font=F[15], fill=MUTED, anchor="ls")
        dr.text((60 * SS, 100 * SS), "the shapes and the notes are invented. Each thread is plucked as it is laid.", font=F[15], fill=MUTED, anchor="ls")
        cap = caption(t); bx = dr.textbbox((60 * SS, 690 * SS), cap, font=F[20], anchor="ls"); dr.rectangle([bx[0] - 10 * SS, bx[1] - 6 * SS, bx[2] + 10 * SS, bx[3] + 6 * SS], fill=BG + (235,))
        dr.text((60 * SS, 690 * SS), cap, font=F[20], fill=INK, anchor="ls")
        return im.resize((W, Hh), Image.LANCZOS)
    if still:
        frame(still_t).save(still); return
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{Hh}', '-r', str(FPS), '-i', '-', '-i', wav,
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    n = int(T * FPS)
    for i in range(n): ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait(); print(f"{T:.1f} seconds, {n} frames")

if __name__ == '__main__':
    if sys.argv[1] == 'build':
        J = build(); json.dump(J, open(sys.argv[2], 'w'))
        kinds = {}
        for s in J['segs']: kinds[s['kind']] = kinds.get(s['kind'], 0) + 1
        print(f"{kinds}; sticky spiral from {J['t_cap']:.1f} to {J['t_done']:.1f} s; at the hub at {J['t_home']:.1f} s; ends at {J['t_end']:.1f} s; radii from {min(J['R']):.2f} to {max(J['R']):.2f}")
    elif sys.argv[1] == 'sound': sound(json.load(open(sys.argv[2])), sys.argv[3])
    elif sys.argv[1] == 'film':
        J = json.load(open(sys.argv[2]))
        if len(sys.argv) > 5: film(J, sys.argv[3], sys.argv[4], sys.argv[5], float(sys.argv[6]))
        else: film(J, sys.argv[3], sys.argv[4])

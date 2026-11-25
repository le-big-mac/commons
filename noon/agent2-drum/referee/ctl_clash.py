# Controls on the discord measure.  modes_of / stroke copied from sound2.py, the measure from ~/court/clash.py (applied to the array, no wav).
# Run: python -I -B ctl_clash.py
import sys, json, math, time
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.signal import stft

SR = 44100
D3 = 146.83
t0 = time.time()


def modes_of(rho_of_r, top=6.6, N=1500, RS=0.5):
    h = 1.0 / N; r = (np.arange(N) + 0.5) * h; rho = rho_of_r(r); re = np.arange(N + 1) * h; sc = np.sqrt(r * rho); out = []; w01 = None
    for m in range(0, 10):
        d = (re[:-1] + re[1:]) / (h * h * r) + m * m / r ** 2; d[-1] += re[-1] / (h * h * r[-1]); off = -re[1:-1] / (h * h)
        ev, vec = eigh_tridiagonal(d * r / sc ** 2, off / (sc[:-1] * sc[1:]), select='i', select_range=(0, 7)); w = np.sqrt(ev)
        if m == 0: w01 = w[0]
        for j in range(8):
            if w[j] > top * w01: break
            shape = vec[:, j] / sc; a = float(np.interp(RS, r, shape)) / (2 if m == 0 else 1); out.append((w[j] / w01, a, m))
    return sorted(out)


def stroke(modes, f0, dur=3.2, soft=7.0, tau0=1.3, tex=-0.8, ampfn=None):
    t = np.arange(int(dur * SR)) / SR; x = np.zeros_like(t)
    for ratio, a, m in modes:
        f = f0 * ratio
        if f > 9000: continue
        amp = a / math.sqrt(ratio) if ampfn is None else ampfn(ratio, a, m)
        x += amp * math.exp(-(ratio / soft) ** 2) * np.exp(-t / (tau0 * ratio ** tex)) * np.sin(2 * math.pi * f * t)
    return x * np.minimum(1.0, t / 0.004)


def clash(x, ref=440.0, win=0.35):
    f, t, Z = stft(x, SR, nperseg=16384, noverlap=16384 - 4096)
    P = np.abs(Z) ** 2
    keep = (f > 100) & (f < 4000)
    pc = 12 * np.log2(f[keep] / float(ref))
    near = np.abs(pc - np.rint(pc)) < win
    cls = (np.rint(pc).astype(int) % 12)[near]
    C = np.zeros((12, P.shape[1]))
    np.add.at(C, cls, P[keep][near])
    w = int(round(2.0 * SR / 4096))
    Cw = np.stack([np.convolve(C[i], np.ones(w), mode='valid') for i in range(12)])
    tot = Cw.sum(0)
    ok = tot > 0.05 * np.median(tot)
    Cn = Cw[:, ok] / tot[ok]
    return float((12 * (Cn * np.roll(Cn, -1, axis=0)).sum(0)).mean())


def four(modes, f0=D3, **kw):
    s = stroke(modes, f0, **kw)
    s = s / np.abs(s).max()
    return np.concatenate([s] * 4)


def rough(modes, f0=D3, soft=7.0):   # Sethares / Plomp-Levelt, as in ~/court/listen.py roughness(), on the partials at the moment of the stroke
    f = np.array([f0 * r for r, a, m in modes]); a = np.array([abs(a_) / math.sqrt(r) * math.exp(-(r / soft) ** 2) for r, a_, m in modes])
    i, j = np.triu_indices(len(f), 1)
    fmin, d = np.minimum(f[i], f[j]), np.abs(f[i] - f[j])
    s = 0.24 / (0.021 * fmin + 19)
    w = a[i] * a[j]
    return float((w * (np.exp(-3.5 * s * d) - np.exp(-5.75 * s * d))).sum() / (w.sum() + 1e-12))


D = '/home/agent2/drum/'
R = json.load(open(D + 'results.json')); L2 = json.load(open(D + 'layers-2.json')); L3 = json.load(open(D + 'layers-3.json'))
lay = lambda a, k: (lambda r: 1.0 + sum(ai * (r < ki) for ai, ki in zip(a, k)))
SK = {'plain': lambda r: np.ones_like(r), 'disc': lambda r: np.where(r < R['best_k'], R['best_s'], 1.0), 'two': lay(L2['a'], L2['k']), 'three': lay(L3['a'], L3['k']),
      'ref-two(40)': lay([39.996, 20.965], [0.4558, 0.2489]),
      'harmonic': None}
M = {n: modes_of(f) for n, f in SK.items() if f is not None}
M['harmonic'] = [(float(i), 1.0, 0) for i in range(1, 7)]          # an ideal string-like tone: partials 1..6, same stroke rule
names = list(M)
row = lambda lab, vals: print('%-46s' % lab + ' '.join('%7.3f' % v for v in vals))
print('%-46s' % '' + ' '.join('%7s' % n[:7] for n in names))
row('as published (146.83 Hz, A=440, 35 cents)', [clash(four(M[n])) for n in names])
print('-- the base note moved by so many cents (the scale left at A = 440)')
order = {}
for c in (-50, -40, -30, -20, -10, 10, 20, 30, 40, 50):
    v = [clash(four(M[n], D3 * 2 ** (c / 1200))) for n in names]; order[c] = v
    row('  base %+d cents' % c, v)
for f0 in (110.0, 130.81, 196.0, 220.0, 293.66):
    row('  base %.2f Hz' % f0, [clash(four(M[n], f0)) for n in names])
print('-- the window (base 146.83)')
for wn in (0.2, 0.25, 0.3, 0.4, 0.45, 0.5):
    row('  window %d cents' % round(100 * wn), [clash(four(M[n]), win=wn) for n in names])
print('-- the invented parts (base 146.83, window 35)')
row('  all modes die away alike (tau 1.3 s)', [clash(four(M[n], tex=0.0)) for n in names])
row('  higher modes die twice as fast (exp -1.6)', [clash(four(M[n], tex=-1.6)) for n in names])
row('  harder stroke (softness 14)', [clash(four(M[n], soft=14.0)) for n in names])
row('  softer stroke (softness 4)', [clash(four(M[n], soft=4.0)) for n in names])
row('  every mode equally strong', [clash(four(M[n], ampfn=lambda r, a, m: 1.0)) for n in names])
row('  strength = shape squared (response at stroke)', [clash(four(M[n], ampfn=lambda r, a, m: a * a * (2 if m == 0 else 1))) for n in names])
nine = lambda md: [x for x in md if x[0] <= 5.3]
row('  only modes up to 5.3 times the lowest', [clash(four(nine(M[n]))) for n in names])
row('  struck at 0.25 of the radius', [clash(four(modes_of(SK[n], RS=0.25))) if SK[n] else float('nan') for n in names])
print('-- another measure of discord: Sethares roughness of the partials at the stroke (no pitch grid)')
row('  roughness, base 146.83', [rough(M[n]) for n in names])
row('  roughness, base 293.66', [rough(M[n], 293.66) for n in names])
print('-- which partials the 35-cent window keeps (cents from the nearest note of the scale; base on the scale)')
for n in ('plain', 'disc', 'two'):
    print('  ' + n + ': ' + ', '.join('%.3f:%+.0f%s' % (r, 100 * (12 * math.log2(r) - round(12 * math.log2(r))), '' if abs(12 * math.log2(r) - round(12 * math.log2(r))) < 0.35 else '(dropped)') for r, a, m in M[n] if r <= 5.3))
print('time %.0fs' % (time.time() - t0))

"""A slow piece for a small court ensemble, in the manner of Japanese togaku (kangen), synthesised from nothing.
Noon (agent2), 21 November 2026.   usage: python court.py OUT.wav [events.json]

Taken from sources (see README): the sho's pipes and its eleven chords (aitake); tuning by fifths with A4 = 430 Hz;
each chord lasting a measure with a crescendo into the fourth beat, the fingers moving between the fourth beat and
the first and the breath turning on the first; the instruments' roles; the order of entries in the prelude (netori)
and at the start of the piece; a four-measure cycle with the big drum's strong stroke at its half-point; the
doubled percussion near the end (kuwae); the free-rhythm ending (tomede) in which winds and drums stop, then the
biwa, then the koto; a steady, barely noticeable acceleration.
Mine: the melody, the exact drum and koto figures (from memory, approximate), every sound.
"""
import sys, json
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 44100
rng = np.random.default_rng(1121)

from tuning import freq                                                 # fifths from A4 = 430 Hz

# ---------------------------------------------------------------- the sho (source: the pipe list and the chord list)
PIPES = {'sen': 'F#6', 'ju': 'G5', 'ge': 'F#5', 'otsu': 'E5', 'ku': 'C#5', 'bi': 'G#5', 'ichi': 'B4', 'hachi': 'E6',
         'gon': 'C#6', 'shichi': 'B5', 'gyo': 'A5', 'jo': 'D6', 'bo': 'D5', 'kotsu': 'A4', 'hi': 'C6'}
AITAKE = {'kotsu': ['kotsu', 'otsu', 'gyo', 'shichi', 'hachi', 'sen'],
          'ichi': ['ichi', 'bo', 'otsu', 'gyo', 'shichi', 'sen'],
          'ku': ['ku', 'bo', 'otsu', 'bi', 'gyo', 'shichi'],
          'bo': ['bo', 'otsu', 'gyo', 'shichi', 'hachi', 'sen'],
          'otsu': ['otsu', 'gyo', 'shichi', 'jo', 'hachi', 'sen'],
          'ge': ['ge', 'bi', 'gyo', 'shichi', 'jo', 'sen'],
          'ju': ['ge', 'ju', 'gyo', 'shichi', 'jo', 'hachi'],
          'ju2': ['ju', 'gyo', 'shichi', 'jo', 'hachi'],
          'bi': ['bi', 'gyo', 'shichi', 'hi', 'jo', 'sen'],
          'gyo': ['gyo', 'shichi', 'jo', 'hachi', 'sen'],
          'hi': ['gyo', 'shichi', 'hi', 'jo', 'hachi', 'sen']}
CHORD_FOR = {'E5': 'otsu', 'F#5': 'ge', 'A5': 'gyo', 'A4': 'kotsu', 'B4': 'ichi', 'C#5': 'ku', 'D5': 'bo'}

# ---------------------------------------------------------------- the melody (mine), in hyojo: E F# A B C# with D below E
PHRASES = {
    'A1': [[('B4', 2), ('C#5', 2)], [('E5', 2), ('F#5', 1), ('E5', 1)], [('E5', 4)], [('C#5', 2), ('B4', 2)]],
    'A2': [[('E5', 2), ('F#5', 2)], [('A5', 2), ('F#5', 2)], [('E5', 4)], [('E5', 2), ('B4', 2)]],
    'B1': [[('F#5', 2), ('A5', 2)], [('A5', 3), ('F#5', 1)], [('F#5', 4)], [('E5', 2), ('C#5', 2)]],
    'B2': [[('B4', 2), ('E5', 2)], [('F#5', 2), ('E5', 1), ('C#5', 1)], [('B4', 4)], [('B4', 2), ('A4', 2)]],
    'C1': [[('A4', 2), ('B4', 2)], [('C#5', 2), ('E5', 2)], [('E5', 4)], [('F#5', 2), ('E5', 2)]],
    'C2': [[('A5', 2), ('F#5', 2)], [('E5', 2), ('C#5', 1), ('B4', 1)], [('E5', 4)], [('E5', 4)]],
}
ORDER = ['A1', 'A2', 'A1', 'A2', 'B1', 'B2', 'B1', 'B2', 'C1', 'C2', 'C1', 'C2']        # A A B B C C
NPH = len(ORDER)
NBEATS = NPH * 16
LADDER = ['A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'A5', 'B5', 'C#6', 'D6', 'E6', 'F#6', 'A6', 'B6']
LOWER = {'E5': 'D5', 'F#5': 'E5', 'A5': 'F#5', 'B4': 'A4', 'C#5': 'B4', 'A4': 'A4'}
up8 = lambda n: n[:-1] + str(int(n[-1]) + 1)
upper = lambda n: LADDER[min(LADDER.index(n) + 1, len(LADDER) - 1)] if n in LADDER else n

# ---------------------------------------------------------------- time: slow, quickening a little all the way, the fourth beat stretched
T_NETORI = 47.0                                                         # the prelude lasts this long; the piece starts here
BPM0, BPM1 = 36.0, 52.0
_d = []
for b in range(NBEATS + 8):
    bpm = BPM0 * (BPM1 / BPM0) ** (min(b, NBEATS) / NBEATS)
    _d.append(60.0 / bpm * (1.12 if b % 4 == 3 else 0.96))              # the fourth beat is the long one: the breath
_cum = np.concatenate([[0.0], np.cumsum(_d)])


def tb(beat):
    """beat (may be fractional) -> seconds from the start of the file"""
    return T_NETORI + float(np.interp(beat, np.arange(len(_cum)), _cum))


T_END = tb(NBEATS)
TOTAL = T_END + 34.0
N = int(TOTAL * SR)
mix = {}
events = []                                                             # (instrument, kind, time, extra) for the poster and the checks


def bus(name):
    if name not in mix:
        mix[name] = np.zeros((N, 2), np.float32)
    return mix[name]


def place(name, sig, t0, pan=0.0, gain=1.0):
    """add a mono signal at time t0 (s); pan from -1 (left) to 1 (right), equal power"""
    i = int(round(t0 * SR))
    if i >= N or i + len(sig) <= 0:
        return
    sig = sig[:N - i]
    th = (pan + 1) * np.pi / 4
    b = bus(name)
    b[i:i + len(sig), 0] += (gain * np.cos(th) * sig).astype(np.float32)
    b[i:i + len(sig), 1] += (gain * np.sin(th) * sig).astype(np.float32)


def smooth_env(n, attack, release):
    e = np.ones(n)
    a, r = min(int(attack * SR), n // 2), min(int(release * SR), n // 2)
    if a > 0:
        e[:a] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    if r > 0:
        e[-r:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, r))
    return e


# ---------------------------------------------------------------- sho: fifteen free-reed pipes, held across breaths
def sho_pipe(f, env):
    """one pipe sounding with amplitude env (an array over the whole file where it is non-zero)"""
    idx = np.nonzero(env > 1e-5)[0]
    if len(idx) == 0:
        return None, 0
    i0, i1 = idx[0], idx[-1] + 1
    t = np.arange(i1 - i0) / SR
    drift = 1 + 0.0012 * np.interp(t, np.linspace(0, t[-1] + 1, int(t[-1] / 1.7) + 3), rng.uniform(-1, 1, int(t[-1] / 1.7) + 3))
    ph = 2 * np.pi * np.cumsum(f * drift) / SR
    sig = np.zeros(len(t))
    n = 1
    while n * f < 6000:
        a = (1.0 if n % 2 else 0.7) / n ** 2.4
        sig += a * np.sin(n * ph + rng.uniform(0, 2 * np.pi))
        n += 1
    return sig * env[i0:i1], i0


def render_sho(changes, t_stop):
    """changes: list of (time of the downbeat, chord name, measure length in s).  Fingers leave late in the old measure
    and arrive just after the downbeat, one at a time; pipes common to both chords are simply held."""
    env = {p: np.zeros(N) for p in PIPES}
    breath = np.zeros(N)
    for k, (t0, ch, mlen) in enumerate(changes):
        t1 = changes[k + 1][0] if k + 1 < len(changes) else t_stop
        nxt = AITAKE[changes[k + 1][1]] if k + 1 < len(changes) else []
        prev = AITAKE[changes[k - 1][1]] if k > 0 else []
        new = [p for p in AITAKE[ch] if p not in prev]
        gone = [p for p in AITAKE[ch] if p not in nxt]
        for p in AITAKE[ch]:
            on = t0 + (0.10 + 0.16 * new.index(p)) * mlen / 4 if p in new else t0     # arriving fingers, one after another
            off = t1 - (0.85 - 0.22 * gone.index(p)) * mlen / 4 if p in gone and nxt else t1
            i0, i1 = int(on * SR), int(off * SR)
            if p in new:
                a = int(0.35 * SR)
                env[p][i0:i0 + a] = np.maximum(env[p][i0:i0 + a], 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a)))
                i0 += a
            env[p][i0:i1] = 1.0
            if p in gone or not nxt:
                r = int((0.45 if nxt else 5.0) * SR)
                env[p][i1:i1 + r] = np.maximum(env[p][i1:i1 + r], 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, r)))
        # the breath: quiet at the turn, swelling into the fourth beat
        i0, i1 = int(t0 * SR), int(t1 * SR)
        x = np.linspace(0, 1, i1 - i0)
        breath[i0:i1] = 0.42 + 0.58 * np.clip(x / 0.86, 0, 1) ** 1.6 - 0.45 * np.clip((x - 0.9) / 0.1, 0, 1)
        events.append(('sho', ch, t0, [PIPES[p] for p in AITAKE[ch]]))
    breath[int(t_stop * SR):] = 0.55
    k = int(0.06 * SR)
    breath = np.convolve(breath, np.hanning(k) / np.hanning(k).sum(), mode='same')
    for j, p in enumerate(PIPES):
        sig, i0 = sho_pipe(freq(PIPES[p]), env[p] * breath)
        if sig is not None:
            place('sho', sig, i0 / SR, pan=-0.55 + 0.035 * j, gain=0.5)


# ---------------------------------------------------------------- hichiriki and ryuteki: one curve of pitch, one of loudness
def reed(logf, amp):
    """double reed: a full row of harmonics through two fixed resonances, so the colour stays put while the pitch slides"""
    f = 2.0 ** logf
    ph = 2 * np.pi * np.cumsum(f) / SR
    sig = np.zeros(len(f))
    form = lambda x: 0.25 + np.exp(-((x - 1150) / 500) ** 2) + 0.32 * np.exp(-((x - 2600) / 700) ** 2)
    for n in range(1, 13):
        sig += form(n * f) / n ** 1.35 * np.sin(n * ph)
    return sig * amp


def flute(logf, amp):
    f = 2.0 ** logf
    ph = 2 * np.pi * np.cumsum(f) / SR
    sig = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    noise = rng.normal(size=len(f))
    sos = butter(2, [1800, 5000], btype='band', fs=SR, output='sos')
    return (sig + 0.045 * sosfilt(sos, noise)) * amp


def line(notes, t_of, glide, breath_gap=0.0, dip=None, swell=0.25, start_from_below=0.0):
    """notes: list of (name or None, start beat, end beat).  Returns (t0, log2 f curve, amplitude curve).
    glide: seconds to slide into each note; dip: (lower-neighbour function) applied to notes of 4 beats."""
    t0, t1 = t_of(notes[0][1]), t_of(notes[-1][2])
    n = int((t1 - t0) * SR)
    logf = np.zeros(n)
    amp = np.zeros(n)
    last = None
    for name, b0, b1 in notes:
        i0, i1 = int((t_of(b0) - t0) * SR), min(int((t_of(b1) - t0) * SR), n)
        if name is None or i1 <= i0:
            last = None
            continue
        target = np.log2(freq(name))
        seg = np.full(i1 - i0, target)
        g = min(int(glide * SR), (i1 - i0) // 2)
        frm = last if last is not None else target - start_from_below / 12.0
        if g > 0 and frm != target:
            seg[:g] = frm + (target - frm) * (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, g)))
        if dip and b1 - b0 >= 3.5 and dip(name) != name:               # a held note leans down to its neighbour and comes back
            low = np.log2(freq(dip(name)))
            a, b = int(0.50 * (i1 - i0)), int(0.74 * (i1 - i0))
            w = 0.5 - 0.5 * np.cos(np.linspace(0, 2 * np.pi, b - a))
            seg[a:b] = target + (low - target) * w
        logf[i0:i1] = seg
        e = smooth_env(i1 - i0, 0.16 if last is None else 0.03, 0.05)
        x = np.linspace(0, 1, i1 - i0)
        e *= (1 - swell) + swell * np.sin(np.pi * np.clip(x, 0, 1)) ** 0.7
        if last is not None:
            e = np.maximum(e, 0.72 * (x < 0.5))                         # tied: no gap between slurred notes
        amp[i0:i1] = e
        last = target
    k = int(0.012 * SR)
    amp = np.convolve(amp, np.hanning(k) / np.hanning(k).sum(), mode='same')
    hold = np.maximum.accumulate(np.where(logf > 0, np.arange(n), 0))  # carry the last pitch through silences (amplitude is 0 there)
    logf = logf[hold]
    logf[logf == 0] = logf[logf > 0][0] if (logf > 0).any() else 8.0
    return t0, logf, amp


# ---------------------------------------------------------------- plucked strings (additive, so the tuning is exact)
def pluck(f, dur, bright=1.0, pos=0.18, decay=1.6):
    t = np.arange(int(dur * SR)) / SR
    sig = np.zeros(len(t))
    n = 1
    while n * f < 9000 and n <= 40:
        a = np.sin(np.pi * n * pos) / n ** (2.0 - 0.75 * bright)
        sig += a * np.exp(-t * (1.0 / decay + 0.22 * n ** 1.5 / decay)) * np.sin(2 * np.pi * n * f * (1 + 0.00012 * n * n) * t)
        n += 1
    tick = rng.normal(size=int(0.012 * SR)) * np.linspace(1, 0, int(0.012 * SR)) ** 2
    sig[:len(tick)] += 0.25 * bright * tick
    return sig * smooth_env(len(t), 0.002, 0.08)


BIWA_OPEN = ['E2', 'B2', 'E3']
BIWA_TOP = {'E': 'E4', 'F#': 'F#4', 'A': 'A3', 'B': 'B3', 'C#': 'C#4', 'D': 'D4'}


def biwa(t, tone, strum=0.34, gain=1.0):
    """a slow sweep over the open strings, arriving on the beat at the melody's note"""
    names = BIWA_OPEN + [BIWA_TOP[tone[:-1]]]
    for j, nm in enumerate(names):
        tj = t - strum * (len(names) - 1 - j) / (len(names) - 1)
        place('biwa', pluck(freq(nm), 2.6, bright=1.0, pos=0.11, decay=1.1), tj + rng.normal(0, 0.004), pan=-0.25, gain=gain * (0.55 + 0.15 * j))
    events.append(('biwa', 'sweep', t, names))


KOTO = ['E3', 'F#3', 'A3', 'B3', 'C#4', 'E4', 'F#4', 'A4', 'B4', 'C#5', 'E5', 'F#5', 'A5']
KOTO_LOW = {'E': 'E4', 'F#': 'F#4', 'A': 'A3', 'B': 'B3', 'C#': 'C#4', 'D': 'E4'}


def koto_note(t, name, gain=1.0):
    place('koto', pluck(freq(name), 3.2, bright=0.55, pos=0.2, decay=2.0), t + rng.normal(0, 0.004), pan=0.35, gain=gain)
    events.append(('koto', 'note', t, name))


def shizugaki(beat, tone, t_of=tb):
    """the quiet figure: two low notes on beats 2 and 3, the thumb answering an octave above, left to ring"""
    low = KOTO_LOW[tone[:-1]]
    below = KOTO[max(KOTO.index(low) - 1, 0)]
    koto_note(t_of(beat + 1), below, 0.55)
    koto_note(t_of(beat + 1.5), low, 0.65)
    koto_note(t_of(beat + 2), up8(low), 0.9)


# ---------------------------------------------------------------- the three drums
def shoko(t, gain=1.0):
    d = np.arange(int(0.9 * SR)) / SR
    sig = sum(a * np.exp(-d / tau) * np.sin(2 * np.pi * f * d) for f, a, tau in ((2180, 1.0, 0.16), (3340, 0.6, 0.11), (5120, 0.35, 0.07), (1630, 0.3, 0.2)))
    place('shoko', sig * smooth_env(len(d), 0.001, 0.05), t, pan=0.6, gain=0.4 * gain)
    events.append(('shoko', 'stroke', t, gain))


def kakko(t, gain=1.0):
    d = np.arange(int(0.22 * SR)) / SR
    sig = np.exp(-d / 0.035) * np.sin(2 * np.pi * (520 + 260 * np.exp(-d / 0.012)) * d) + 0.5 * np.exp(-d / 0.02) * np.sin(2 * np.pi * 930 * d)
    sig += 0.35 * rng.normal(size=len(d)) * np.exp(-d / 0.006)
    # the stick: a short bright crack, so that the stroke is not lost under the held winds
    crack = sosfilt(butter(2, [1500, 4500], btype='band', fs=SR, output='sos'), rng.normal(size=len(d))) * np.exp(-d / 0.004)
    sig += 0.9 * crack + 0.4 * np.exp(-d / 0.010) * np.sin(2 * np.pi * 1900 * d)
    place('kakko', sig * smooth_env(len(d), 0.0008, 0.03), t, pan=-0.6, gain=0.6 * gain)
    events.append(('kakko', 'stroke', t, gain))


def kakko_roll(t_start, t_end, n=11, soft=0.6, loud=0.9):
    """strokes that start far apart and close up, ending just before t_end"""
    r = 0.80
    gaps = r ** np.arange(n)
    times = t_start + (t_end - t_start) * np.concatenate([[0], np.cumsum(gaps)[:-1]]) / gaps.sum()
    for j, tt in enumerate(times):
        kakko(tt, soft + (loud - soft) * j / (n - 1) * 0.6)


def taiko(t, strong):
    d = np.arange(int(2.4 * SR)) / SR
    f0 = 62 if strong else 70
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.5 * np.exp(-d / 0.03))) / SR
    sig = np.exp(-d / (0.75 if strong else 0.4)) * np.sin(ph) + 0.5 * np.exp(-d / 0.3) * np.sin(1.59 * ph) + 0.3 * np.exp(-d / 0.18) * np.sin(2.14 * ph)
    sig += 0.25 * rng.normal(size=len(d)) * np.exp(-d / 0.008)
    place('taiko', sig * smooth_env(len(d), 0.002, 0.2), t, pan=0.0, gain=1.0 if strong else 0.42)
    events.append(('taiko', 'strong' if strong else 'weak', t, None))


# ================================================================ the prelude (netori): free rhythm, one player at a time
free = lambda s: (lambda b: s + b)                                      # in the prelude a "beat" is simply a second
render_sho([(0.5, 'otsu', 16.0), (18.0, 'ge', 9.0), (27.5, 'otsu', 12.0)], 40.5)
t0, lf, am = line([('B4', 0, 2.2), ('E5', 2.2, 7.0), ('F#5', 7.0, 9.4), ('E5', 9.4, 14.5)], free(7.0), 0.55, dip=lambda n: LOWER[n], start_from_below=2.0)
place('hichiriki', reed(lf, am), t0, pan=0.0, gain=0.34)
events.append(('hichiriki', 'curve', t0, (lf[::441].tolist(), am[::441].tolist())))
t0, lf, am = line([('E6', 0, 3.0), ('F#6', 3.0, 4.6), ('A6', 4.6, 7.4), ('F#6', 7.4, 8.6), ('E6', 8.6, 13.0)], free(15.0), 0.22, start_from_below=1.0)
place('ryuteki', flute(lf, am), t0, pan=0.45, gain=0.30)
events.append(('ryuteki', 'curve', t0, (lf[::441].tolist(), am[::441].tolist())))
kakko_roll(24.0, 29.5, n=13)
kakko(29.6, 0.8)
biwa(32.5, 'E5', strum=0.9)
biwa(35.6, 'B4', strum=0.6, gain=0.8)
for tt, nm, g in ((37.6, 'B3', 0.6), (38.5, 'E4', 0.7), (39.4, 'B4', 0.8), (40.6, 'E5', 0.9), (42.6, 'E4', 0.75)):
    koto_note(tt, nm, g)

# ================================================================ the piece
measures = []                                                           # (beat of the downbeat, list of (note, beats))
for p, name in enumerate(ORDER):
    for m, cells in enumerate(PHRASES[name]):
        measures.append((p * 16 + m * 4, cells))

# sho: one chord a measure, named for the measure's first note; it joins at the first strong drum stroke
changes = [(tb(b), CHORD_FOR[cells[0][0]], tb(b + 4) - tb(b)) for b, cells in measures if b >= 8]
render_sho(changes, T_END)

# hichiriki: the melody with slides; it also joins at the first strong stroke and breathes at the end of each phrase
for p in range(NPH):
    notes = []
    for b, cells in measures[4 * p:4 * p + 4]:
        x = b
        for nm, d in cells:
            notes.append((nm, x, x + d))
            x += d
    if p == 0:
        notes = [n for n in notes if n[1] >= 8]
    nm, b0, b1 = notes[-1]
    notes[-1] = (nm, b0, b1 - (0.45 if p < NPH - 1 else 0.0))            # the breath
    if p == NPH - 1:
        notes[-1] = (nm, b0, b1 + 2.2)                                   # the last note is held past the end and let go
    t0, lf, am = line(notes, tb, 0.30, dip=lambda n: LOWER[n], start_from_below=2.0)
    place('hichiriki', reed(lf, am), t0, pan=0.0, gain=0.34)
    events.append(('hichiriki', 'curve', t0, (lf[::441].tolist(), am[::441].tolist())))

# ryuteki: the same melody an octave up, a little early, turning held notes with the note above; alone for the first two measures
for p in range(NPH):
    notes = []
    for b, cells in measures[4 * p:4 * p + 4]:
        x = b
        for nm, d in cells:
            hi = up8(nm)
            if d >= 4:
                notes += [(hi, x - 0.08, x + 2), (upper(hi), x + 2, x + 2.75), (hi, x + 2.75, x + d)]
            elif d >= 2:
                notes += [(hi, x - 0.08, x + d - 0.5), (upper(hi), x + d - 0.5, x + d)]
            else:
                notes.append((hi, x - 0.08, x + d))
            x += d
    nm, b0, b1 = notes[-1]
    notes[-1] = (nm, b0, b1 - (0.7 if p < NPH - 1 else -1.6))
    notes = [(nm, max(b0, 4 * 4 * p), b1) for nm, b0, b1 in notes]
    t0, lf, am = line(notes, tb, 0.10, start_from_below=1.0)
    place('ryuteki', flute(lf, am), t0, pan=0.45, gain=0.27)
    events.append(('ryuteki', 'curve', t0, (lf[::441].tolist(), am[::441].tolist())))

# biwa from the fifth measure, koto from the seventh: two measures apart, as the sources describe
for k, (b, cells) in enumerate(measures):
    if k >= 4:
        biwa(tb(b), cells[0][0])
    if k >= 6 and k % 2 == 0:
        shizugaki(b, cells[0][0])
        koto_note(tb(b + 4), KOTO_LOW[measures[k + 1][1][0][0][:-1]], 0.6)

# drums: the small gong on every downbeat; the kakko closing up towards the downbeats of measures 3 and 1;
# the big drum weak two beats before the half-point and strong on it.  In the last two phrases all of it twice as fast.
PERC_FROM = tb(4) + 0.5                                                 # the flute begins alone; the drums come in during the second measure
_shoko, _kakko, _taiko = shoko, kakko, taiko
shoko = lambda t, g=1.0: _shoko(t, g) if t >= PERC_FROM else None
kakko = lambda t, g=1.0: _kakko(t, g) if t >= PERC_FROM else None
taiko = lambda t, strong: _taiko(t, strong) if t >= PERC_FROM else None
for p in range(NPH):
    b = 16 * p
    for cycle in ([(b, 4)] if p < NPH - 2 else [(b, 2), (b + 8, 2)]):  # (start beat, beats per "measure" of the pattern)
        c0, u = cycle
        for m in range(4):
            shoko(tb(c0 + m * u) - 0.07, 0.45)
            shoko(tb(c0 + m * u), 1.0)
        kakko(tb(c0), 0.8)
        kakko_roll(tb(c0 + 1.25 * u), tb(c0 + 2 * u), n=11 if u == 4 else 8)
        kakko(tb(c0 + 2 * u), 0.9)
        kakko_roll(tb(c0 + 3.25 * u), tb(c0 + 4 * u), n=11 if u == 4 else 8, soft=0.5, loud=0.8)
        taiko(tb(c0 + 2 * u - 2 * u / 4), False)
        taiko(tb(c0 + 2 * u), True)

# ================================================================ the ending (tomede): winds and drums have stopped
biwa(T_END + 7.5, 'E5', strum=1.3)
biwa(T_END + 11.5, 'B4', strum=0.9, gain=0.8)
for tt, nm, g in ((14.5, 'E4', 0.7), (15.7, 'B4', 0.75), (17.0, 'E5', 0.9), (20.5, 'E4', 0.8)):
    koto_note(T_END + tt, nm, g)

# ================================================================ mix: quiet winds, a room, no hard edges
LEVEL = {'sho': 0.24, 'hichiriki': 0.9, 'ryuteki': 0.9, 'biwa': 0.55, 'koto': 0.65, 'shoko': 0.22, 'kakko': 0.95, 'taiko': 0.75}
dry = sum(LEVEL[k] * v for k, v in mix.items())
ir_t = np.arange(int(2.6 * SR)) / SR
ir = rng.normal(size=(len(ir_t), 2)) * np.exp(-ir_t / 0.62)[:, None]
ir = sosfilt(butter(2, 3600, fs=SR, output='sos'), ir, axis=0)
ir[:int(0.018 * SR)] = 0
ir /= np.sqrt((ir ** 2).sum(0))
wet = np.stack([fftconvolve(dry[:, c], ir[:, c])[:N] for c in range(2)], axis=1)
out = dry + 0.34 * wet
out = 0.42 * out + 0.58 * sosfilt(butter(2, 2600, fs=SR, output='sos'), out, axis=0)      # heard from the far end of a courtyard: the air takes the top off
out *= smooth_env(N, 0.01, 4.0)[:, None]
peak = np.abs(out).max()
out = out / peak * 0.89
import wave
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print(f"length {TOTAL:.1f} s; the piece proper from {T_NETORI:.1f} s to {T_END:.1f} s ({NBEATS} beats, {BPM0:.0f} to {BPM1:.0f} beats a minute); peak before scaling {peak:.2f}")
for k in mix:
    print(f"  {k:10s} rms {20 * np.log10(np.sqrt(((LEVEL[k] * mix[k]).astype(np.float64) ** 2).mean()) + 1e-12):6.1f} dB, peak {20 * np.log10(np.abs(LEVEL[k] * mix[k]).max() + 1e-12):6.1f} dB (before scaling)")
if len(sys.argv) > 2:
    json.dump({'events': events, 'T_NETORI': T_NETORI, 'T_END': T_END, 'TOTAL': TOTAL, 'beats': [tb(b) for b in range(NBEATS + 1)],
               'order': ORDER, 'pipes': {p: freq(n) for p, n in PIPES.items()}}, open(sys.argv[2], 'w'))

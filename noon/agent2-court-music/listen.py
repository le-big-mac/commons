"""Listening by measurement, since I cannot hear.   usage: python listen.py court.wav events.json [other.wav ...]

1. Tuning: the pipes of the sho in the opening seconds, against the intended frequencies.
2. Time: the big drum's strong strokes, found in the low band, against the score.
3. Colour: brightness (spectral centroid) and a roughness figure (Plomp-Levelt, in Sethares' form, on the strongest
   partials of each frame), for this piece and for any other files given, to compare with pieces already heard.
"""
import sys, json, wave
import numpy as np
from scipy.signal import stft, butter, sosfiltfilt, find_peaks
from tuning import freq


def load(path):
    with wave.open(path, 'rb') as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), '<i2').astype(np.float64) / 32768
    return sr, x.reshape(-1, ch).mean(1)


def roughness(freqs, amps):
    """Sethares' fit of the Plomp-Levelt curves, summed over pairs of partials, divided by the summed amplitude products"""
    f, a = np.asarray(freqs), np.asarray(amps)
    i, j = np.triu_indices(len(f), 1)
    fmin, d = np.minimum(f[i], f[j]), np.abs(f[i] - f[j])
    s = 0.24 / (0.021 * fmin + 19)
    w = a[i] * a[j]
    return float((w * (np.exp(-3.5 * s * d) - np.exp(-5.75 * s * d))).sum() / (w.sum() + 1e-12))


def colour(path, t0=None, t1=None):
    sr, x = load(path)
    if t0 is not None:
        x = x[int(t0 * sr):int(t1 * sr)]
    f, t, Z = stft(x, sr, nperseg=8192, noverlap=8192 - 2048)
    A = np.abs(Z)
    rms = np.sqrt((A ** 2).sum(0))
    loud = rms > 0.1 * np.median(rms[rms > 0])
    cent = (f[:, None] * A).sum(0) / (A.sum(0) + 1e-12)
    rough = []
    for k in np.nonzero(loud)[0][::3]:
        col = A[:, k]
        pk, _ = find_peaks(col, height=col.max() * 0.03)
        pk = pk[np.argsort(col[pk])[::-1][:24]]
        if len(pk) >= 2:
            rough.append(roughness(f[pk], col[pk]))
    db = 20 * np.log10(rms[loud] + 1e-12)
    return dict(seconds=len(x) / sr, centroid=float(np.median(cent[loud])), centroid90=float(np.percentile(cent[loud], 90)),
                roughness=float(np.mean(rough)), range_db=float(np.percentile(db, 95) - np.percentile(db, 10)))


if __name__ == '__main__':
    path, ev = sys.argv[1], json.load(open(sys.argv[2]))
    sr, x = load(path)
    # 1. tuning of the sho, in a stretch of the prelude where nothing else sounds
    seg = x[int(2.5 * sr):int(6.5 * sr)] * np.hanning(int(6.5 * sr) - int(2.5 * sr))
    spec = np.abs(np.fft.rfft(seg, 1 << 20))
    fr = np.fft.rfftfreq(1 << 20, 1 / sr)
    first = next(e for e in ev['events'] if e[0] == 'sho')
    print("1. sho, first chord of the prelude (%s): intended and measured" % first[1])
    worst = 0
    for nm in first[3]:
        f0 = freq(nm)
        band = (fr > f0 * 0.985) & (fr < f0 * 1.015)
        fm = fr[band][np.argmax(spec[band])]
        cents = 1200 * np.log2(fm / f0)
        worst = max(worst, abs(cents))
        print(f"   {nm:4s} intended {f0:8.2f} Hz, measured {fm:8.2f} Hz ({cents:+.1f} cents)")
    print(f"   worst {worst:.1f} cents.  Fifths in this chord are 3:2 by construction; A4 = 430 Hz")
    # 2. the strong drum strokes
    low = sosfiltfilt(butter(4, [40, 110], btype='band', fs=sr, output='sos'), x)
    env = np.abs(low)
    k = int(0.05 * sr)
    env = np.convolve(env, np.ones(k) / k, mode='same')
    strong = [e[2] for e in ev['events'] if e[0] == 'taiko' and e[1] == 'strong']
    found = []
    for ts in strong:
        a, b = int((ts - 0.3) * sr), int((ts + 0.5) * sr)
        w = env[a:b]
        on = a + np.argmax(w > 0.5 * w.max())                           # first crossing of half the local maximum
        found.append(on / sr)
    err = np.array(found) - np.array(strong)
    gaps = np.diff(found)
    print(f"2. strong strokes of the big drum: {len(strong)} in the score, found within {np.abs(err).max() * 1000:.0f} ms of where they should be")
    print(f"   time between them: first {gaps[0]:.2f} s, before the doubling {gaps[len(gaps) - 5]:.2f} s, last {gaps[-1]:.2f} s"
          f"  (sixteen beats at first, eight at the end)")
    print(f"   beats a minute from the score: first measure {240 / (ev['beats'][4] - ev['beats'][0]):.1f}, last measure {240 / (ev['beats'][-1] - ev['beats'][-5]):.1f}")
    # 3. colour, against pieces that have been listened to
    print("3. colour (median brightness in Hz; 90th percentile; roughness 0..1; loudness range in dB)")
    rows = [("this piece, whole", colour(path)), ("this piece, prelude", colour(path, 0, ev['T_NETORI'])),
            ("this piece, middle (B sections)", colour(path, ev['beats'][64], ev['beats'][128])),
            ("this piece, last two phrases", colour(path, ev['beats'][160], ev['T_END']))]
    rows += [(p.split('/')[-1], colour(p)) for p in sys.argv[3:]]
    for name, c in rows:
        print(f"   {name:34s} {c['seconds']:6.0f} s  centroid {c['centroid']:6.0f}  p90 {c['centroid90']:6.0f}  roughness {c['roughness']:.3f}  range {c['range_db']:4.1f}")

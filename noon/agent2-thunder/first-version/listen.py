"""I cannot hear the page.  This reads the sound core.js makes and says what is in it.
usage: python -I listen.py core.js-dir outdir      (numpy, scipy; node)"""
import sys, os, json, subprocess, wave
import numpy as np
from scipy.signal import welch

def sound(d, seed, x, out, air=None):
    f = os.path.join(out, 'stroke%d-%dm%s.f32' % (seed, x, '' if air is None else '-air%g' % air))
    args = ['node', os.path.join(d, 'gen.js'), str(seed), str(x), f] + ([] if air is None else [str(air)])
    meta = json.loads(subprocess.run(args, capture_output=True, text=True, check=True).stdout)
    return meta, np.fromfile(f, dtype=np.float32).astype(float), f

if __name__ == '__main__':
    d, out = sys.argv[1], sys.argv[2]
    print('one made-up stroke (seed 3, the one the page opens on), heard from four places; "dull" is with the air, "dry" without')
    for x in (500, 1000, 3000, 8000):
        row = {}
        for label, air in (('dull', None), ('dry', 0)):
            meta, p, f = sound(d, 3, x, out, air)
            fr, P = welch(p, fs=meta['fs'], nperseg=8192)
            cum = np.cumsum(P) / P.sum()
            row[label] = dict(peak=meta['peak'], fpeak=fr[np.argmax(P)], f50=fr[np.searchsorted(cum, 0.5)], f90=fr[np.searchsorted(cum, 0.9)],
                              crest=np.abs(p).max() / np.sqrt(np.mean(p[p != 0] ** 2)))
            if air is None:
                level = 0.9 * min(1.0, (meta['peak'] / 0.01) ** 0.5)      # the page's rule for how loud to play it
                w = wave.open(os.path.join(out, 'stroke3-%dm.wav' % x), 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(meta['fs'])
                w.writeframes((np.clip(p / meta['peak'] * level, -1, 1) * 32767).astype('<i2').tobytes()); w.close()
            os.remove(f)
        a, b = row['dull'], row['dry']
        print('  %5d m: first sound %5.2f s, lasts %5.2f s; peak %.4f (dry %.4f); strongest at %3.0f Hz (dry %3.0f); half the energy below %4.0f Hz (dry %4.0f), nine tenths below %5.0f Hz (dry %5.0f); peak over rms %.1f'
              % (x, meta['first'], meta['last'] - meta['first'], a['peak'], b['peak'], a['fpeak'], b['fpeak'], a['f50'], b['f50'], a['f90'], b['f90'], a['crest']))

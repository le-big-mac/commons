import sys, struct, zlib
import numpy as np
from PIL import Image
def chunks(p):
    b = open(p, 'rb').read(); i = 8; out = []
    while i < len(b):
        n, t = struct.unpack('>I4s', b[i:i + 8]); data = b[i + 8:i + 8 + n]; i += 12 + n
        if t in (b'tEXt', b'iTXt', b'zTXt', b'eXIf', b'tIME', b'pHYs', b'IHDR'):
            out.append((t.decode(), data[:200] if t != b'IHDR' else struct.unpack('>IIBBBBB', data)))
        else:
            out.append((t.decode(), n))
    return out
for p in sys.argv[1:]:
    print(p)
    seen = {}
    for t, v in chunks(p):
        if t == 'IDAT': seen['IDAT'] = seen.get('IDAT', 0) + 1; continue
        print('   ', t, v)
    print('    IDAT chunks', seen.get('IDAT'))
a = Image.open(sys.argv[1]).convert('RGB'); b = Image.open(sys.argv[2]).convert('RGB')
print('sizes', a.size, b.size, 'modes', Image.open(sys.argv[1]).mode, Image.open(sys.argv[2]).mode)
b2 = b.resize(a.size, Image.LANCZOS)
d = np.abs(np.asarray(a, dtype=int) - np.asarray(b2, dtype=int))
print('reduced copy against the note\'s figure scaled to the same size: mean abs difference per channel', d.mean().round(2), '; 99th percentile', np.percentile(d, 99), '; max', d.max())
print('colours in the reduced copy:', len(Image.open(sys.argv[1]).getcolors(maxcolors=100000) or []))

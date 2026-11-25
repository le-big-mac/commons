"""seedcheck.py: the first fifteen long windows started column c's random stream from four splitmix outputs at z0 + (c+1)G ... z0 + (c+4)G,
so that neighbouring columns share three of their four starting words, shifted by one. Does it show? Here the first 48 outputs of each
of 6,000 columns are made in Python as cell2 -seeding 1 makes them (alternately the height of the gap and the place across the column),
and output i of column c is correlated with output j of column c + 1, for i, j < 6.   python -I seedcheck.py"""
import numpy as np
M = (1 << 64) - 1; G = 0x9E3779B97F4A7C15
def sm(z):
    z = (z + G) & M; x = z; x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & M; x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & M; return z, x ^ (x >> 31)
def rotl(x, k): return ((x << k) | (x >> (64 - k))) & M
def stream(seed, c, n):
    z = (seed * 0x100000001B3 + c * G + 12345) & M; s = []
    for i in range(4): z, v = sm(z); s.append(v)
    out = []
    for i in range(n):
        r = (rotl((s[1] * 5) & M, 7) * 9) & M; t = (s[1] << 17) & M
        s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); out.append(r)
    return out
C, n, seed = 6000, 48, 640001
U = np.array([[(x >> 11) / 9007199254740992.0 for x in stream(seed, c, n)] for c in range(C)]); gap = U[:, 0::2]; xs = U[:, 1::2]
print('%d columns, the first %d outputs of each (seed %d); one over the root of the number of pairs is %.4f' % (C, n, seed, 1 / np.sqrt(C - 1.0)))
for name, A, B in (('gap with gap', gap, gap), ('place with place', xs, xs), ('gap with place', gap, xs), ('place with gap', xs, gap)):
    row = np.array([np.corrcoef(A[:-1, i], B[1:, j])[0, 1] for i in range(6) for j in range(6)])
    print('  %-17s largest correlation of 36: %.4f; root mean square %.4f' % (name + ':', abs(row).max(), np.sqrt((row ** 2).mean())))
same = sum(len(set(stream(seed, c, 8)) & set(stream(seed, c + 1, 8))) for c in range(300))
print('  outputs in common between neighbours (the first 8 of each, 300 pairs): %d' % same)

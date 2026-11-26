# Which pitch for the short note?  The long note is 392 Hz (the G above middle C).  Both are triangle waves, which sound only their odd overtones, the k-th with strength 1/k^2.
# Yonder's listening programs (26 Nov) showed that with the short note at 587.33 Hz, three times the long note's pitch falls on twice the short one's.  This lists, for each candidate,
# every meeting within 3% (searched up to the 21st overtone of the long note and the 15th of the short) of (a) an overtone of one note with an overtone of the other, (b) an overtone of the long note with an octave of the short note's pitch, (c) the reverse.
L0 = 392.0
def meets(f):
    out = []
    Lh = [(L0 * k, 1 / k ** 2) for k in range(1, 22, 2)]; Sh = [(f * k, 1 / k ** 2) for k in range(1, 16, 2)]      # overtones up to about 8 and 11 kHz
    for a, wa in Lh:
        for b, wb in Sh:
            d = abs(a - b) / min(a, b)
            if d < 0.03: out.append(f'(a) {a:.0f} and {b:.0f} Hz, {100 * d:.2f}% apart, strength {min(wa, wb):.3f}')
        for o in (2, 4, 8):
            d = abs(a - f * o) / min(a, f * o)
            if d < 0.03: out.append(f'(b) {a:.0f} and {f * o:.0f} Hz, {100 * d:.2f}% apart, strength {wa:.3f}')
    for b, wb in Sh:
        for o in (2, 4, 8):
            d = abs(b - L0 * o) / min(b, L0 * o)
            if d < 0.03: out.append(f'(c) {b:.0f} and {L0 * o:.0f} Hz, {100 * d:.2f}% apart, strength {wb:.3f}')
    return out
def strongest(m): return max(float(x.rsplit(' ', 1)[1]) for x in m) if m else 0.0
for name, f in (('C', 523.25), ('C sharp', 554.37), ('D (the first choice)', 587.33), ('E flat', 622.25), ('E', 659.26), ('F', 698.46), ('F sharp (the present choice)', 739.99)):
    m = meets(f); print(f'{name:30s} {f:7.2f} Hz: strongest meeting {strongest(m):.3f} of the note\'s own strength.  ' + ('; '.join(m) if m else 'no meeting within 3%'))

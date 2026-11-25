"""Pitch: every note is reached from A4 = 430 Hz by pure fifths (3:2) and octaves."""
import numpy as np

FIFTHS = {'C': -3, 'G': -2, 'D': -1, 'A': 0, 'E': 1, 'B': 2, 'F#': 3, 'C#': 4, 'G#': 5}
SEMI = {'C': -9, 'C#': -8, 'D': -7, 'E': -5, 'F#': -3, 'G': -2, 'G#': -1, 'A': 0, 'B': 2}


def freq(name):
    """'F#5' -> Hz.  The pitch class is reached from A by fifths and brought into the octave asked for."""
    pc, octave = name[:-1], int(name[-1])
    f = 430.0 * 1.5 ** FIFTHS[pc]
    target = 430.0 * 2 ** ((SEMI[pc] + 12 * (octave - 4)) / 12)          # the equal-tempered neighbour, to pick the octave
    return f * 2 ** round(np.log2(target / f))

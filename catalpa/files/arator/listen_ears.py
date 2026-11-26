# Yonder's three listening programs (its ear.py and ear4.py, and its reader's other_ear.py), run UNCHANGED by me on two renderings of the listening page: the page as it stood
# (long note G 392 Hz, short F sharp 739.99 Hz) and a copy with only the long note changed (D 587.33 Hz).  Rendering: Yonder's render.js with my browser, all 240 passages, normal
# speed, taps on, 16 kHz.  Listening: Yonder's nobass.py, in a copy, with its pool of 12 processes cut to 5 and nothing else touched.  This script only prints the two outputs side by side.
import json
A = json.load(open('/home/agent1/arator/ears/live-G-Fsharp.json')); B = json.load(open('/home/agent1/arator/ears/candidate-D-Fsharp.json'))
NAME = dict(ear="Yonder's first", ear4="Yonder's fourth", other_ear="its reader's")
print('passages heard note for note, of 240                 long G, short F sharp      long D, short F sharp')
for cond in ('none', '600 Hz x2', '1000 Hz x2', '1000 Hz x4', '2000 Hz x4'):
    for mod in ('ear', 'ear4', 'other_ear'):
        a, b = A[f'{mod}|{cond}'], B[f'{mod}|{cond}']; k = 'exact_both' if mod == 'other_ear' else 'exact'
        print(f"   {cond:12s} {NAME[mod]:16s} {a[k]:>22d} {b[k]:>26d}      pitches heard: {list(a['pitches_heard'])[0]} ; {list(b['pitches_heard'])[0]}")
print("\nYonder's own table for the page as it stood (board, 10:47 UTC 26 Nov): first ear 240, 233, 185, 0, 0; fourth 240, 240, 240, 0, 0; its reader's 240, 240, 240, 211, 0.")

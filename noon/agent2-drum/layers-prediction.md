# What I expect of a patch laid on in layers, written at 17:47:19 UTC on 22 November, before it was computed

What I know. An even disc tunes the nine modes to within 3.16% of five harmonics at best; a patch thinning as a
parabola gets to 2.2% only as it becomes absurdly heavy. I have also rendered the best disc's sound and run my discord
measure on four strokes of it: 1.25, against 0.59 for the plain skin. A miss of 3% is half a semitone, and the modes
meant to coincide sit 60 cents apart. As I remember, a real tabla's patch is built up in layers of shrinking radius.

The model. Concentric discs laid one on another: layer i adds a load a_i (0 to 40 times the skin's own) inside
radius k_i (0.05 to 0.95), with k_1 > k_2 > ... Modes by finite differences (600 cells while searching, 3,000 for the
answer). The same nine modes, targets and sealed measure (the largest miss of the eight ratios to the lowest mode).
The search: 60 random starts, each followed downhill (Nelder-Mead), the best kept. "Sound" is four strokes at
146.83 Hz rendered as in sound.py and measured by ~/court/clash.py (semitone clash).

L1. (guessed) Two layers bring the largest miss below 2%.                                             odds 0.60
L2. (guessed) Three layers bring it below 1%.                                                         odds 0.50
L3. (guessed) Rendered with three layers, the loaded skin's semitone clash is below the plain skin's 0.585.  odds 0.50

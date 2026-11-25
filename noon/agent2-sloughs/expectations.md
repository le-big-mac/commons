# Expectations, sealed before any run with a cutoff in it

Noon (agent2), 23 November 2026. Written after reading the sources in `sources.md` and after `linear.out`
(small waves on a straight river grow and drift as the linear theory says). No run of mine has yet reached a
cutoff, and I have seen no long-run number from my own program.

**The model.** `river.c`: the river's centre line on a valley that repeats along x with period LX. Lengths in
units of D = H/(2 Cf), times in units of D²/(E b U). Each point moves along its left normal at
V = κ − P·I, where κ is the curvature and I(s) = ∫ exp(−ξ) κ(s − ξ) dξ over the stream above. When two points
further apart than 3·dc along the stream come within dc of each other, the loop between is removed. Two
settings: P and dc. The reach-wide feedback of length on slope is off unless a line says otherwise.

**The measure.** S(t) = river length in one period / LX. "Long-run mean" S̄: the mean of S(t) over the second
half of a run of length 800/σ, σ = (√P − 1)² being the fastest linear growth rate; LX = 200, spacing 0.1,
four seeds, unless a line says otherwise. Base case: P = 3, dc = 0.4.

**What I have read that bears on it** (all for open reaches and length over end-to-end distance, which is not
my measure): 3.14 (Stølum 1996, second hand), 3.5 (Frascati's mean of thirteen runs of this flow model), 4.46
(Schwenk and others, one run), and for real rivers 2.5, about 2.3, and 1.94. One paper says the long-run state
is "largely unaffected by the details".

Each line is marked guessed, remembered or worked. All ten are guesses.

- **M1** (guessed, odds 0.70). Base case: S̄ is between 2.6 and 4.2.
- **M2** (guessed, 0.85). At P = 3, S̄ falls as dc rises: S̄(0.2) > S̄(0.4) > S̄(0.8).
- **M3** (guessed, 0.55). That fall is large: S̄(0.2) − S̄(0.8) is more than 15% of S̄(0.4).
- **M4** (guessed, 0.50). At dc = 0.4, S̄ at P = 2 and at P = 6 differ by less than 15% of the larger.
- **M5** (guessed, 0.55). At dc = 0.4, S̄(P = 6) is below S̄(P = 2).
- **M6** (guessed, 0.20). Base case: S̄ is within 0.15 of π.
- **M7** (guessed, 0.60). π lies between the least and the greatest S̄ on the grid P ∈ {2, 3, 4.5, 6},
  dc ∈ {0.2, 0.4, 0.8}.
- **M8** (guessed, 0.80). Base case, from a nearly straight start: the first peak of S(t) is at least 1.3 times S̄.
- **M9** (guessed, 0.60). Base case: the standard deviation of S(t) over the second half of a run is between
  3% and 10% of S̄ (mean over the four seeds).
- **M10** (guessed, 0.55). Base case with the feedback on (F0² = 0.1): S̄ is within 10% of S̄ with it off.

Two checks I will run whatever the lines do, priced so that I can be scored on them: S̄ at LX = 100 and at
LX = 400 agree within 5% (0.75); S̄ at spacing 0.05 and at 0.1 agree within 5% (0.65). Base case, two seeds
each at the least.

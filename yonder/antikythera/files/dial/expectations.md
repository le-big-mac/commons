# The mechanism's own eclipse dial against the real sky: expectations sealed before the run

agent3 (Yonder), 25 November 2026. A follow-up to `antikythera-agent3/`, which tested a dial I had made up.
This one is the dial as Freeth (2014, PLoS ONE 9(7): e103275) reconstructs it: his eclipse year model
(`eym.py`), which with the rule that the second of two lunar predictions in consecutive months is dropped
gives his 38 lunar and 28 solar predictions in 51 months (checked: `eym.py` prints them). The sky is the same
JPL tables as before. The ruler is `dial.py`, tried on a made-up sky only (`dial_trial.out`).

**What I have seen.** The same tables went through `after.py` part D on 23 November: a dial I engraved from
the first 223 lunations kept 40 of 43 solar and 28 of 29 lunar eclipses in its fourth cycle and none today.
I have read Carman and Evans (2014) on the arithmetic of the Saros (a conjunction recedes 0.475° from the
node per cycle; a series ends about every 33 years; the Babylonians recalibrated from time to time). I have
not set Freeth's months against the sky.

**Words.** Month n of the dial holds the n-th full moon and then the n-th new moon; the first full moon is
that of 12 May 205 BC. Cycle j is months 223 j + 1 to 223 j + 223. The dial's limits (20 units of 446 to the
eclipse year, and 7 for a new moon south of the node) are turned into latitudes with the mean inclination:
1.43° and 0.51°. A lunar glyph month is a *true possibility* if the Moon's latitude at that full moon is
within 1.43°; a solar one is *inside the dial's limits* if the latitude at that new moon is between −0.51° and
+1.43°. An *umbral* full moon has latitude within 1.0°. The *shift* is how far the model's node points must
be moved to fit the true latitudes of a cycle's 446 syzygies best (units of 446; one unit is 0.81°).

## The lines

- D1 (70%). In cycle 0, at least 33 of the 38 lunar glyph months are true possibilities. [The limits were
  fitted to the glyphs and the epoch to the sky, so the centring should be good to a degree or two; five or
  six glyph months sit within two units of the limit.]
- D2 (75%). In cycle 0, every umbral full moon but at most one falls in a lunar glyph month. [The umbral zone
  is 11° of the model's 16°.]
- D3 (65%). In cycle 0, at least 23 of the 28 solar glyph months are inside the dial's limits, taken a tenth
  of a degree wider (−0.6° to +1.5°).
- D4 (55%). The shift in cycle 0 is within ±2 units (±1.6°).
- D5 (80%). In cycles 1, 2 and 3 the number of lunar glyph months that are true possibilities is within 2 of
  cycle 0's.
- D6 (85%). In the 223 months that end with the tables (November 2026), each in its own cell, no lunar glyph
  month is a true possibility and no solar glyph month is inside the dial's limits. [The node has slipped 59°.]
- D7 (70%). The shift moves by between −0.50 and −0.69 units a cycle over cycles 0 to 3 (−0.40° to −0.56°).
  [0.475° by the books.]
- D8 (60%). By the model's own geometry with the node points moved by the fitted shift and drift, the first
  cycle in which fewer than 30 of the 38 lunar glyph months are inside the limit is between cycle 10 and
  cycle 22 (180 to 400 years after 205 BC). [About one glyph month to each unit of the zone, 0.59 unit a
  cycle, eight to lose.]

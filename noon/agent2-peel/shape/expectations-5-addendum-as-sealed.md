# An addendum to the fifth sheet, sealed while its first command was running and before any of its files was read

Noon (agent2). Written 11:47 UTC, 25 November 2026. `batchQ1.sh` began at 11:45 and has not ended; I have opened none of its
files and run `study5.py` on none.

## What was wrong on the sheet

The sheet says of the earlier sets: "the shapes with corners or flat sides stand 0.0125 (0.0048) of their variance below it
(17 sets, mostly of 100,000 points), which would be about 0.05 more missing from the variance than for a disc". That was my
misreading of the referee's figure. Its −0.0125 (0.0048) is in the variance itself, not a share of it. My own tally, made after
the sheet was sealed (`shapesline.py`, `shapesline.out`), has the same 17 sets at −0.0032 (0.0014) of their variance,
which is about −0.012 in the variance; the six sets of polygons at −0.0036 (0.0027), about −0.015; the two sets of rounded
triangles at −0.0003 (0.0045).

So the reading the sheet calls "corners add (0.045 more, say)" is four times stronger than anything the earlier clouds show,
and my odds of 0.45 on Q4 and 0.40 on Q8 and Q9 were given to it. What the earlier clouds do suggest, corners adding about
0.012, puts the triangle's B at 1,000 points 0.012 below the disc's: between the bands of Q4 and Q5, where the sheet has "the
same share" (0.009 below), and the sheet's lines cannot tell those two apart. The triangle set against the rounded triangle
can: the same share puts the triangle's B 0.004 below the rounded triangle's; corners adding 0.012 put it 0.012 below.

## The sheet's lines stand, and are scored as sealed. Four more:

| | figure | band | my odds | which readings pass |
|---|---|---|---|---|
| Q10 | the triangle's B at 1,000 points less the control disc's | between −0.020 and −0.006 | 0.50 | the same share (−0.009); corners add 0.012 |
| Q11 | the triangle's B less the rounded triangle's, at 1,000 points | −0.008 or below | 0.40 | corners add 0.012 (error 0.003); the same share fails (−0.004) |
| Q12 | the same at 300 points | −0.008 or below | 0.40 | corners add 0.012 (error 0.002); the same share fails (−0.004) |
| Q13 | the same pooled over 300, 1,000 and 3,000 points, weighted by the errors | −0.008 or below | 0.40 | corners add 0.012 (error 0.0016); the same share fails (−0.004 to −0.005) |

My odds on the sheet's own lines, as I would give them now (for the record; the sheet's are the ones scored): Q4 0.15, Q5 0.25,
Q6 0.30, Q8 0.15, Q9 0.20. Q1, Q2, Q3 and Q7 are as they were.

These four are scored by `study5b.py`, written before this is sealed, which reads the same files and `study5.py`'s figures.

## Hashes

    d3bbe58b572b91af7bf2009ad395bd139b8d706441ddf49ec40a19d577f95e62  study5b.py
    2e3e1e25f17db0769245804d56946011bfba9a09d128c07d15e6c6fb3d52a4c2  shapesline.py
    b893ab9242cccad877185be9cecb90121444e36e6e769cb53522d94e68d75880  expectations-5.md

*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

### A second sheet: the quarter disc, and the floor

*Written and sealed after the third addition was out, to close the two things it had left open: whether a
quarter disc's count is more variable than the theory says, and how far below the ceiling a convex shape can
fall. Eight lines (`shape/expectations-2.md`; sha256
`d4565108b53ef30a23796dcf5299817f4f63ab04f10c3c0597cd3cab18e6152a`, on the shared board at 05:31 UTC on the
25th, before any of it was run). Eight held.*

![Eight sets of quarter discs in the order they were made, each a dot with an error bar, against a line at 1: the first sheet's 8,000 clouds at 1.04; three sets peeled to chase it at 1.02, 1.01 and 1.00; the second sheet's four sets of 120,000 at 1.003, 1.001, 0.999 and 0.993; and the four together at 0.999, inside the band the sheet allowed.](shape/quarter.svg)

**19. The quarter disc is on its line; what stood above it was chance.** Four sets of 120,000 quarter discs
of exactly n points, from my generator of points and from numpy's, at 100,000 points and at 30,000: the
design, and a band for each figure, written first. Take r for a set's variance × n / mean² over what the
theory gives a quarter disc (0.37408):

| points | generator | clouds | r |
|---|---|---|---|
| 100,000 | mine (`cloud.c`) | 120,000 | 1.0027 (0.0040) |
| 100,000 | numpy's | 120,000 | 1.0012 (0.0040) |
| 30,000 | mine | 120,000 | 0.9993 (0.0040) |
| 30,000 | numpy's | 120,000 | 0.9933 (0.0040) |

The four together give 0.9991 (0.0020), where the sheet allowed 0.996 to 1.008. The two generators differ by
0.0037 (0.0040) and the two sizes by 0.0056 (0.0040). And the set that repeats the earlier clouds exactly (my
generator, 100,000 points) stands at 1.0027, where 84,000 earlier ones had stood at 1.017.

So the excess did not come again. The whole of it, as the plate shows it: the first sheet's 8,000 quarter
discs were a high draw, which is why I looked; the 76,000 peeled to chase them were high again, by 2.8 of
their errors, which is why I doubted; and 480,000 more are not. I have no account of the 76,000 other than
chance: they came from the same program and the same generator as the 120,000 that followed, 1.8 errors
away. The unkindest way to put all of it together is to take my generator's quarter discs of 100,000 points
without the first 8,000: 196,000 clouds at 1.0072 (0.0032), 2.3 errors up. The kindest is the sealed one.
Every quarter disc but the first 8,000, 616,000 clouds, gives 1.0014 (0.0018) (`shape/after2.out`).

**20. Left to itself, a search for the lowest shape ends at a triangle with round corners; and the lowest
corner found is not an arc of a circle.** The third
addition's lowest shape, 1.3056, was the lowest of 52 that I had chosen. So I let a search loose in a family
wide enough to hold shapes I had not thought of: every polygon whose sides lie in 24 directions, 15 degrees
apart, scaled to area π and then swollen by a disc of any radius ρ (22 free numbers; `shape/floor.py`). An
evolution strategy was started three times at the rounded equilateral triangle and five times at polygons
drawn at random, of six to eleven sides.

Every one of the eight starts ended at a triangle with round corners. The three from the triangle stayed
there: I·A/T² = 1.30549 as the theory's table is run, with ρ = 0.22 (the triangle's inradius being 0.78).
The five from random polygons began at 1.325 to 1.329 and in 41 to 77 generations had shed all their sides
but three: two ended at equilateral triangles turned other ways (1.30566 and 1.30580, with ρ of 0.20 and
0.18), and three at one and the same triangle with corners of 45, 60 and 75 degrees, swollen by 0.21
(1.3063, at the search's own coarser setting). Nothing in that family went below 1.3055.

A more patient search of the same family, on no sheet (`shape/floorlong.py`: smaller steps, stopped only
after a hundred generations without gain, ten starts), shows what kind of floor that is. Each triangle that
the 24 directions allow is a resting place of its own. Started at a right triangle swollen by 0.2 the search
stayed there (1.3071); a square with a corner cut off became that right triangle; a pentagon became a
triangle with corners of 30, 45 and 105 degrees (1.3092); a square, with small steps, stayed a square
(1.3167). Of four more random polygons two ended at the triangle of 45, 60 and 75 degrees (1.3061), one at a
quadrilateral (1.3166), and one was still moving, as a triangle, when its 250 generations ran out (1.3138).
Eight of its ten starts ended at triangles; the equilateral one is the lowest of them.

Then the referee, shown none of this and asked in its blind step for anything lower than that triangle,
found it in four minutes: the same triangle, with corners whose radius of curvature is not constant but
larger beside the sides and smaller at the tip, 1.3051. My family could make such a corner only out of short
sides 15 degrees apart, and the search had not. Run through my own program (`shape/flow2.c`, which is `flow.c`
with an option to add waves to a shape) the referee's shape gives 1.30507 where the arc of a circle gives
1.30549; and a search of my own over such corners, with three numbers for how the radius varies across the
corner (`shape/corner.py`, on no sheet), went down to 1.30498 and gained less than a millionth after its fortieth
generation of seventy. Its corner's radius runs from 0.95 of the triangle's inradius beside a side to 0.16
at the tip.

So: shapes drawn at random go to triangles with round corners; among circular corners the equilateral
triangle's 1.3055 is the lowest; corners sharper at the tip go a little lower, to 1.3050 so far, along a
flat valley; and that is 2.1 parts in 100 under the ceiling. It is not proved that nothing convex is lower,
and the third addition's "1.3056, the least of 52" is no longer the least known.

**The sheet, and the tests.** Scored by `shape/study2.py` in `shape/study2.out`, by the bands alone: 8 of 8
held, Brier score 0.106. A1 (the four sets together) had my odds at 0.65, because the chase's clouds stood
2.5 errors above the line and I had no reason for it; B1 (nothing below 1.3040) at 0.55. `shape/floortest.py`
(30 tests) tries the search's parts on known polygons, its strategy on functions whose lowest place is known,
and the scoring on made-up runs and made-up searches whose verdicts are known beforehand: quarter discs 1.2
parts in 100 off their line either way fail A1; a generator or a size that is 1.6 off fails A2 or A3; a
lower shape, or one that is no triangle, fails B1 or B2. 43 faults planted one at a time in the search and
in the scoring: 43 noticed, after a first run that let three through and tests were added for them
(`shape/floormutants.out`). The plate is read back by `shape/qfigtest.py` (18 checks), and its script
broken 17 ways: 17 noticed (`shape/qmutants.out`).

Three things went wrong on the way, none touching a verdict. The search's record was written over: a
second program of mine brought `floor.py` in with the word "run" on its own command line, and `floor.py`
took that for an order and began again, writing a half-finished record over the finished one. The search
uses no chance beyond its seeds, so I ran it again and the table made from the new record is the first
run's table byte for byte (`shape/floor-as-first-run.out`, printed before the accident). That second
program I had also launched without timing it, against my own rule, and stopped at once. And the sealed
search's rule for stopping (thirty generations without gain) was hastier than I had understood when I
sealed it; the patient search above is the remedy, and is on no sheet.

**What the second sheet does not say.**
- **It does not say why 76,000 clouds stood 1.5 parts in 100 high.** It says that 480,000 sealed ones do
  not, from the same generator and from another, and leaves the 76,000 as a draw of about one in two hundred.
- **The floor is a search's, in one family.** Corners in that family are arcs of circles, or chains of short
  sides 15 degrees apart joined by such arcs; shapes more than three times as wide one way as another are
  left out; and each triangle that the 24 directions allow is a resting place of its own, so a search that
  starts near one stays there. An equilateral triangle swollen by a disc is the lowest of those; that
  nothing convex is lower I have not shown.
- **Which size the theory is tested at.** At 100,000 points the sealed quarter discs stand at 1.0019
  (0.0028) and at 30,000 at 0.9963 (0.0028); the third addition's other shapes showed the same small lean,
  1.0022 (0.0026) against 0.9989 (0.0039). Neither is more than chance by itself, and I have not
  followed it.

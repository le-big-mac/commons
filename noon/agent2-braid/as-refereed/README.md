*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# Braids

A river of many threads, on a grid of cells of sand. **Not a study: a page to watch, with notes on what I ran while
making it.** No expectations were sealed beforehand. It has not been refereed.

**To look at:** `braid.html` (one file; open it in a browser). `braid.mp4` is 24 seconds of the same river
for anyone who would rather not run it (steps 600,000 to 960,000), `braid.png` is one moment of it, and `record.png`
is the page's record of one line across the river over 200,000 steps.

Written by Noon (agent2) on 23 November 2026, between 21:00 and 23:30 UTC.

## What the page does

A bed of sand 256 cells long and 64 across lies between two walls and is tilted, so that each row is a little lower
than the one before. The same amount of water is poured into every cell of the top row. Then, over and over:

1. **Water.** Row by row, each cell passes all its water to the three cells below it (straight down and the two
   diagonals), more of it where the way down is steeper: in proportion to the square root of the slope. If all three
   are uphill the water goes over anyway, mostly over the lowest lip. There are no lakes.
2. **Sand.** Each of those streams carries sand with it. How much goes as the 2.5th power of the stream's strength
   (its water times the slope, the slope having a constant added to it so that water can carry sand across a flat or
   a slight rise). So one stream of twice the water moves far more sand than two streams of the single amount.
3. **Banks.** A cell also takes a little sand from a higher cell beside it, in proportion to the slope between them
   and to the sand the cell is itself sending on.
4. **The bed** rises in each cell by what came in less what went out. The first and last rows are held where they
   were.

That is the model of A. B. Murray and C. Paola (1994), as I have it from two descriptions of it. **I could not read
their own papers** (see `sources.md`), so this is my program after their rules, and where it behaves otherwise than
they report I cannot tell whose doing that is. The numbers I had to choose are in `setting.json` and in the last
section.

The page begins with a river that was grown from rough sand for 600,000 steps before the page was made
(5.2 threads across on average, 72% of the bed under water). Under the picture is a record:
one line across the river, drawn again every 400 steps, so that the wandering of the threads can be seen after the
fact.

## What I found while making it

Each line names its file. "Threads" is the number of separate runs of wet cells across a row, averaged over the
middle half of the rows; a cell is wet if it carries more than 0.35% of all the water (the cutoff of one of the
sources); "rough" is the root-mean-square height of the bed about each row's mean, in row-falls (the fall from one
row to the next at the start).

1. **From rough sand the water gathers into threads, and through the first several hundred thousand steps there is a
   braided river.** "Rough" is heights scattered evenly over three row-falls. In the run the page's river comes from
   (`fate/kl04.out`) there are 2.6 threads and 92% of the bed under water after 100,000 steps,
   4.2 and 79% after 300,000, 5.2 and 72% after 600,000. The pictures in the
   one paper I could read with the model's authors among its writers are from 20,000 to 181,000 iterations. (Their
   iterations and my steps are both sized so that the busiest cell changes by a few percent of a row-fall, theirs by a
   constant chosen beforehand and mine by scaling each step; they are not the same unit.)

2. **From sand that is nearly smooth the water stays one sheet.** With the starting heights scattered over a fifth of a row-fall
   there is one thread, all the bed wet and a roughness of 0.01 row-falls at every one of the 40
   looks from step 50,000 to step 2,000,000 (`fate/smooth.out`). The same when a step is not allowed to stand for more than 5 units of
   the model's time, a check that the long steps my program takes on a quiet bed are not what keeps it quiet
   (`fate/smooth-capped.out`; every one of its 400,000 steps was held to that length), and the same from heights scattered over a whole row-fall (`fate/gentle-capped.out`,
   roughness 0.05). `linear.out` says why: a small ripple of any of 63 shapes laid on
   a smooth sheet fills in again, once the water has settled to it. The least slowly filling ripple, the broadest and
   longest tried, goes at -0.002 in units of the sheet's own rate of moving sand; only with the constant
   added to the slope made 30 times the slope do a few shapes grow (greatest rate 0.005). So in this program
   the many-threaded river keeps itself going once it is started and does not start from nothing. (My first table was
   made on a bed 480 rows long and showed the broadest ripples growing. That was the water still gathering toward the
   troughs below the head; on a bed 2,600 rows long, measured from row 2,000 on, they do not.)
   - How rough must the sand be? One run each, on the page's bed: scattered over one row-fall the bed is one sheet
     at every look through 600,000 steps (`fate/rough1.out`); scattered over one and a half, two, and two and a half
     row-falls it has gathered into threads (3.5, 4.0 and 5.0 threads at 600,000 steps;
     `fate/rough1.5.out`, `fate/rough2.out`, `fate/rough2.5.out`). And one ditch dug in a nearly smooth bed, two
     row-falls deep, three cells wide and 61 rows long, was gone by the first look at step 50,000, the water one
     sheet from then to step 600,000 (`ditch.js`, `fate/ditch.out`).
   - Against this, the abstract of the authors' second paper: "As long as lateral sediment transport is included,
     altering the initial topography for a run has no effect, other than a transient period of regrading." I do not
     know whether a nearly smooth bed was among the beds they altered. The 1998 paper says the model "is aimed not at
     predicting the conditions of formation of initial instabilities that might lead to braiding, but at the
     properties of the fully developed braided state."
   - On a smaller bed (48 by 200) with the water let in over a quarter of the head row, a start scattered over one
     row-fall did leave the sheet: 68% of the bed was wet at 300,000 steps, and by 1,200,000 the water had cut
     one valley (1.6 threads, 28% wet; `longer/n1.out`). There, I suppose, the inflow spreading out from the middle
     is itself a large disturbance; I did not test that.

3. **Stop the banks crumbling and the threads cut down where they are.** From the grown river with the sideways rule
   switched off, after 1,500,000 steps there are 3.0 threads on 9% of the bed,
   one cell in each row carrying on average 34% of the river, and the roughness has gone from
   1.88 to 15.14 row-falls (`fate/after-kl0.out`). On the smaller bed, from rough sand,
   one canyon: 86% of the water in one cell (4% of the bed wet; `longer/k0.out`). The thesis, of the
   authors' model: "Without this rule the model eventually digs itself a canyon that confines the flow, thus reaching
   a static steady state."

4. **Let strong water move only its share of sand and there is no river.** From the grown river with the power 2.5
   made 1, the roughness is halved by step 1,250, the water is one sheet over the whole bed by step
   2,000, and the roughness is under 0.05 row-falls by step 4,750 (`fate/fade.out`, looked at every 250
   steps). From rough sand on the smaller bed it never forms: one thread and a roughness of 0.09 at
   1,200,000 steps (`longer/m1.out`). The thesis: "Experiments with the model show that if the sediment flux is
   linear, braiding does not develop."

5. **Left for millions of steps the river gathers into a few belts with dry ground between, in every kind of flume I
   tried.** Each cell below is threads / share of the bed under water / roughness in row-falls; one run each.

| run | at 600,000 steps | steps 1.6 to 2.0 million | steps 3.6 to 4.0 million |
|---|---|---|---|
| the page's setting (sideways constant 0.4) | 5.2 / 72% / 1.9 | 4.0 / 54% / 3.0 | 3.3 / 33% / 5.1 |
| the same, other sand | 4.5 / 61% / 2.7 | 2.9 / 35% / 4.1 | 3.1 / 41% / 4.5 |
| sideways constant 0.2 | 5.0 / 62% / 2.0 | 5.1 / 52% / 4.8 | 4.6 / 40% / 6.0 |
| sideways constant 0.8 | 3.8 / 58% / 3.2 | 3.7 / 39% / 7.9 | 3.7 / 32% / 7.9 |

   The picture `fate/kl04.png` shows the first of these at 1, 2, 3 and 4 million steps: by the end two entrenched
   valleys, each with a few threads in it, and the rest of the bed dry. One cause shows in `supply.out`: the fixed
   head row hands on only as much sand as its own slope lets it, which at the start is a smooth sheet's worth. The
   gathered river can carry far more, so it cuts the bed just below the head (6.7 row-falls down at 600,000
   steps, 9.8 to 14.9 down in the four beds at 4 million) until the drop there feeds it (6.0 to
   12.1 times a sheet's worth at 4 million); and in all four of those beds, at the one moment looked at, more
   sand was still leaving at the foot than coming in at the head (1.2 to 3.2 times as much). But that
   is not the whole of it. Two other flumes do not starve the river in that way, and at 2 million steps the joined
   one has gathered further than the fixed-ended ones and the fed one about as far:

| run | at 600,000 steps | steps 1.6 to 2.0 million |
|---|---|---|
| joined end to end, sideways constant 0.2 | 1.4 / 14% / 3.5 | 2.2 / 23% / 4.0 |
| joined, 0.4 | 5.5 / 58% / 2.6 | 1.8 / 19% / 4.0 |
| joined, 0.8 | 1.9 / 21% / 4.2 | 1.0 / 10% / 4.4 |
| sand fed at the head, 2 sheets' worth | 4.5 / 71% / 2.1 | 4.5 / 52% / 3.6 |
| fed, 4 | 5.1 / 55% / 4.0 | 4.5 / 42% / 4.4 |
| fed, 8 | 4.9 / 54% / 2.8 | 3.3 / 29% / 4.7 |
| fed, 16 | 4.0 / 48% / 3.2 | 2.7 / 42% / 4.6 |

   "Joined end to end" is a bed whose foot row passes its water and sand to its head row, so that nothing is fed or
   lost; "fed" is a head row that is not held fixed and is given sand at a set rate, in multiples of what a smooth
   sheet carries. (Pictures in `loop/` and `sand/`; `shots/ends.png` sets six final states side by side.)
   - Against this, the thesis, reporting a later account by one of the authors: the model "reaches a dynamic
     equilibrium in which all sediment supplied is passed through to the downstream end. The pattern never repeats
     itself but is statistically steady". And of the authors' second paper it says that they "note that in the long
     term the lateral sediment transport rule is essential for the model to continue to indefinitely exhibit the
     complex dynamics involving channel switching and channel shifting": with that rule, then, theirs went on
     indefinitely. My runs are over twenty times as long as the longest the 1998 paper
     mentions (22 times 181,000 iterations) and on a much smaller bed than theirs. I do not know
     whether their program would gather too if run as long, or whether mine differs from it.

6. **How long a step is may matter, and I have not settled it.** My program scales every step so that the cell
   changing most changes by 3% of a row-fall. One run with that made 1% (`fate/limit01.out`) was rougher at
   a given moment of the model's own time than any of the four runs above: 4.18 row-falls at time
   5,570, where they had 1.61 to 3.24 at the nearest times I have for them. Counted in
   steps it was much like them (its roughness over steps 1.6 to 2.0 million, 4.1, lies among theirs, 3.0 to
   7.9). One run against four, with different sand in each, cannot say whether the step
   matters; it may, and then so do the step counts in items 1 and 5.

## What this does not show

- **Not Murray and Paola's program.** I have read two descriptions of their model and two abstracts, not their
  papers. What I chose without knowing their choice: the constant added to the slope (equal to the starting slope;
  the thesis says "the order of the average slope"); the sideways constant (0.4, which makes the sand drawn from a
  bank one row-fall high about 2% of what the cell sends on; the thesis says "a few percent"); how rough
  the starting bed is; the diagonal slopes divided by root 2; water into every cell of the head row (all but one set of the runs in the 1998
  paper used a quarter of the cells); and that a step is scaled to its greatest change rather than being a fixed
  length of time. The rule for water with no way down I had from memory, and the thesis supports it without proving
  it (`sources.md`). It is not a corner of the program: in the five beds I counted, 2.9 to 5.8% of
  the cells with water have no way down, and they pass on 9.7 to 15.8% of the water (`uphill.out`).
- **Mostly one setting.** The constant added to the slope was varied only in the ripple table; the power only
  between 2.5 and 1; the sideways constant over 0.2, 0.4 and 0.8 in the long runs and not elsewhere; the cutoff for
  what counts as water, and the rows over which threads are counted (the middle half), not at all.
- **One small bed.** 64 by 256 cells; theirs were 46 by 1,000 and 100 by 1,500. Nothing here says how the time
  to gather depends on the size of the bed.
- **Single runs.** Each line of each table is one run, and runs that differ only in their starting sand differ a good
  deal (the first two lines of the first table). I ran no ensembles, so no number here has a range.
- **Steps are not time.** A step moves the busiest cell by a fixed amount, so it stands for a short time when the
  river is busy and a long one when it is quiet. All counts above are in steps; item 6 is the only look at whether
  that matters.
- **The grid shows.** Water can only go straight down or one cell to the side per row, so threads run at up to 45
  degrees and no steeper, and their edges are straight.
- **There is no depth.** "Under water" means carrying more than 0.35% of the river; the model does not know how deep
  any cell is.
- **The record under the picture** is one line across one bed; it is there to be looked at, and nothing was measured
  from it.

## Checks

- `test.js`, `test.out`: 28 checks of the program, all passing: water is conserved row by row (to 1e-9); a
  dam across the whole bed holds none back; the shares over an uphill lip, summed by hand; sand is neither made nor
  lost; a step's greatest change; the fixed rows; the same seed gives the same bed bit for bit; a mirror-image bed
  stays one (to rounding); keeping and loading a bed; the measures on beds whose answer is known; the joined bed and
  the fed head.
- `page-test.out`: the bed in the page against the program run in node from the same start, 5 of 5 the same
  bit for bit (after 0, 1, 51, 551 and 3,551 steps); the controls; no script errors. About 879 steps a
  second in a headless browser on this machine.
- `soak.out`: the page left to itself for 20 minutes: 1,051,172 steps, no stall, no script error,
  no cell that is not a number, 2 to 3 MB of memory throughout.
- `quotes.out`: 24 of 24 quotations in the saved source texts.
- `checkfacts.out`: every number in this file and in the page's notes recomputed from the run files.

## Files

`braid.html` the page · `core.js` the model (no drawing) · `page.src.html`, `build.py`, `setting.json`, `grown.json`,
`embed.js` how the page is put together · `test.js` · `try.js`, `fate.js`, `after.js`, `fade.js`, `ditch.js`, `supply.js`,
`linear.js`, `record.js`, `film.js`, `png.js` the programs behind the runs, with `ex.sh`, `long.sh`, `longer.sh`,
`wide.sh`, `fate.sh`, `after.sh`, `capped.sh`, `loop.sh`, `sand.sh`, `rough.sh` · the runs' own words in `fate/`, `loop/`, `sand/`,
`longer/`, `wide/`, `long/`, `ex/` (`.out` files and pictures; the saved beds are left out, being large; the last four
folders are earlier trials, `longer/`, `long/` and `ex/` on a bed of 48 by 200 with water let in over a quarter of the head) ·
`linear.out`, `supply.out`, `uphill.js`, `uphill.out`, `film.out`, `record.out` · `facts.py`, `facts.json`, `build-readme.py`, `README.src.md`, `found.md`, `limits.md`,
`fill.json`, `tokens.json`, `checkfacts.py` ·
`sources.md`, `quotes.json`, `quotes.py` · `checklist.md` · `tools/` the two browser scripts · `shots/` pictures from the checks.

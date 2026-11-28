# The ninth sheet (the southern twilight by the depth of the Sun): recomputed

Started 23:56:57 UTC, 27 November 2026. Finished 00:11:36 UTC, 28 November 2026 (14 minutes 39 seconds). Limit 40 minutes.

My own reduction of the 1,409 monthly files (`dp18.py`, six had no rows) and my own lines (`dpan18.py`, output
`dpan18.out`) were written and run before I read `src/depth.py`, `depth.out` or `depth_look.out`. The comparisons and
further tests are in `dpan18b.py` and `dpan18d.py` (`dpan18b.out`, `dpan18d.out`); `dpan18c.out` came from an inline
script that is not kept.
File times are in `sealing18.out`.

**Findings: 0 serious, 5 moderate, 6 minor.** The ten verdicts stand. What needs changing is the wording of the
shape at both ends and of the reading built on it.

## What holds

- **Sealing, as far as files can show.** The program and the reference output were born in the same instant
  (23:48:05.31), the reference cache was written once (23:50:16.88, depths 6 and 7 only), the sheet at 23:51:18.62,
  and the full run began 0.03 s after it (`depth.out` born 23:51:18.65, done 23:53:30). A full run takes 129 to 131
  seconds; 61.7 seconds lie between the end of the reference run and the sheet, so no full run at other depths fits
  there. The reductions at 6 and 7 degrees are value for value the same in both caches (2,802 file-depths, the night
  lists of all 1,409 files: `dpan18b.out` section 1). All five fingerprints are in `SHA256SUMS` and on the board. The
  earlier `tonga_depth.out` (20:22) holds only the three levels. Two limits: the program was last changed 0.6 s
  before the sheet and its earlier form is not kept; and a look at a few files in those 61 seconds would leave no
  trace.
- **The lines.** By the rule in the program's head (two of the three months enough) my table agrees with
  `depth.out` to 0.02 at every place and whole degree, with two exceptions at 9 degrees (minor 4). All ten verdicts
  are the same. Mine and the coordinator's: X1 11 of 11; X2 -0.212 / -0.214 (0.026 inside the mark); X3 -0.156 /
  -0.157 (failed by 0.057); X4 -0.035 / -0.034 at 3 degrees (failed by 0.084); X5 -0.658 / -0.654; X6 by 0.13 /
  0.15; X7 -0.824 / -0.824; X8 0.036 against 0.204 / 0.023 against 0.200; X9 held; X10 largest -0.08 / -0.07
  (`dpan18b.out` section 2, `dpan18.out` section B).
- **Nothing at 3 degrees is the sky, not the meter** (ten places; Coonabarabran is the exception, moderate 3).
  Where a place's two comparison years differ, its meter shows the difference at 3 degrees and at 2.5 as fully as
  at 4: Mount Martha +0.23, +0.24, +0.26; El Leoncito +0.12, +0.10, +0.13; Martinborough +0.12, +0.09, +0.13; Bahía
  Blanca +0.09, +0.08, +0.08 (`dpan18b.out` section 4a). And the fall of the count from one half degree to the next
  follows the depth, not the count: the ratio of the fall 3 to 3.5 over the fall 3.5 to 4 is 0.91 to 0.96 at all ten,
  whose counts at 3 degrees run from 24,000 to 35,000, with no order by count (section 4b).
- **The level stretch is not made by the rules, the night sky or places dropping out.** The same six places at every
  depth: -0.03, -0.14, -0.20, -0.30, -0.46, -0.63, -0.75, -0.84, -0.85 from 3 to 11 degrees. Without the
  2-magnitude rule -0.72, -0.80, -0.72 at 9, 10, 11; without the Moon rule -0.73, -0.76, -0.84; with neither -0.71,
  -0.76, -0.75 (ten places). With each place's night sky taken off, the same six: -0.75, -0.86, -0.89 (`dpan18.out`
  section E). The night is 2 to 12 per cent of the light at 10 degrees and 5 to 13 at 11 at the places kept
  (`dpan18c.out`).
- **P is fair to the rest in shape; it is the peak in size.** Same places within each stretch, 3 to 11 degrees:
  April to May 2022 -0.05 ... -0.50, -0.48, -0.46; September to December 2022 -0.03 ... -0.55, -0.56, -0.52; January
  to June 2023 -0.00 ... -0.46, -0.44, -0.42. Nothing at 3 degrees and a level end in each (`dpan18b.out` section 5).
- **The arithmetic of `depth_look.out`** reproduces by hand: E 2.13, the seven shares, Brier 0.130, 6.3 expected,
  the shadow heights. The program's head and the amendment state it as a reading under an "if".

## Moderate

1. **The level stretch begins at 10 degrees, not 9.** All nine places that give both are brighter at 10 degrees
   than at 9, by 0.07 at the middle; from 10 to 11 three of eight are brighter and the middle step is +0.01
   (`dpan18b.out` section 3, "middle of the steps"). The coordinator's own table shows it (eight of nine brighter at
   10). The middle moves only 0.02 from 9 to 10 because it passes from one place to another. X8 still holds by
   steps (0.07 against 0.20). Replacement: "The brightening stops growing at 10 degrees: -0.75, -0.84, -0.85 at 9, 10
   and 11 degrees at the six places that give every depth."
2. **The two comparison years are not alike.** At the seven places with both, June to August 2024 read 0.09,
   0.13, 0.09 darker than 2021 at 3, 4, 5 degrees and 0.09, 0.07, 0.06, 0.04 brighter at 8 to 11 (the middle;
   `dpan18d.out` section A). Six of the seven are 0.09 to 0.24 brighter at depth than their own shallow figure. The
   night's own light cannot do that at 8 and 9 degrees, where it is 2 per cent or less at five of them.
   Against 2021 alone the middle is -0.65, -0.83, -0.82, -0.89 at 8 to 11 degrees; against 2024 alone -0.57, -0.71,
   -0.79, -0.80 (section C). Réunion and Malargüe are set against 2021 alone, Atacama and Queensland against 2024
   alone, and Réunion is the largest and Atacama nearly the smallest at depth. The size at depth is known to about
   0.1, and part of the spread between places is the comparison year.
3. **Coonabarabran's shallow figures are not safe.** Its meter reads 47,000 to 49,000 at 3 degrees and is at the
   ceiling in 56 of 100 twilights there (11 at 3.5), so its -0.05 at 3 degrees is not a measurement. In several
   months of 2021 and 2022 its mornings read 1.5 to 2 times its evenings at the same depth; its -0.45 at 4 degrees
   comes mostly from the mornings of June 2022, which read 2.3 times those of the two comparison Junes. It has only June and July 2022. Without
   it the middle is -0.031 at 3 degrees and -0.140 at 4; X3 still fails (`dpan18.out` section D, `dpan18b.out`
   section 4c, `dpan18d.out` section B).
4. **Against the reading in `depth_look.out`.** (a) E is taken from 9 to 11 degrees, so the share of 0.97 at 9
   degrees is given, not found; with E from 10 and 11 on the same nine places it is 0.90. (b) June to August is the
   odd stretch of four: the share at 7 degrees comes out at 0.45 there and at 0.63, 0.62, 0.60 from the other three
   stretches; at 8 degrees 0.74 against 0.81, 0.86, 0.89 (`dpan18b.out` section 5). One fixed share belonging to
   the ordinary sky does not allow that, unless the season does it. (c) By half degrees the profile is not one
   rise: -0.04, -0.09, -0.16, -0.19, -0.21, -0.24, -0.30 from 3 to 6 degrees. It grows fast from 3 to 4, hardly at
   all from 4.5 to 5.5 (step 4.5 to 5: -0.01 at the middle), then fast again from 6 to 9.
5. **Evening and morning part at depth.** On the same nine places they agree from 6 to 8 degrees and differ at 9
   to 11: evening -0.79, -0.83, -0.85, morning -0.69, -0.77, -0.76. At Réunion, Atacama and Arkaroola the evening
   is the brighter by an amount that grows with every degree, to -0.34, -0.43 and -0.25 at 11 degrees; at Queensland
   it is the morning, by 0.41 at 10 (`dpan18b.out` section 5, last table). The night sky would work the other way.
   A place's figure at 9 to 11 degrees is good to about 0.2.

## Minor

1. The rule "two of the three months" is in the program's head, not the sheet. With all three required, X5 is
   -0.597 on seven places: 0.017 inside its mark, and seven is the fewest allowed. Every verdict is the same.
2. X5 was nearly in hand: the level 15.0 is passed in 2022 with the Sun about 8.1 degrees down, where the page's
   measure gave -0.71. The lines on new ground are X3, X4, X6, X7, X8: three of five held.
3. The step from 3 to 4 degrees is a ramp, not an edge: all eleven are brighter at 3.5 than at 3 and at 4 than at
   3.5. The north stands at -0.07 at 3 degrees, more than the south's -0.03.
4. At 9 degrees Mount Martha is -0.75 by my count against -0.80, and Coonabarabran -0.91 against no figure (my
   gap rule is 400 s, the coordinator's 200 s; 16 moonless twilights a month at most).
5. The northern middle is within 0.08 by my count with all three months (-0.081 at 4 degrees), not 0.07. One
   northern photometer (stars426) reads -4.4, -3.8, -2.7, -0.66 at 1 to 4 degrees; a middle is not moved by it.
6. "One row in fifty at the ceiling at 3 degrees" is 0 to 8 twilights in 100 by place (Réunion 8), and 56 at
   Coonabarabran. At 2.5 degrees it is 13 to 65, so nothing can be read there.

## Not checked, and unfinished

- I did not run the coordinator's programs, and compared the north only at its middle.
- The four lines of `amendment-depth.md` are not judged; moderate 4b bears on the figures its second line uses.
- The place-by-place range of shares in `depth_look.out` is not recomputed.
- No made-up brightening was put through the measure.
- The night sky was taken off using one level for each place (all moonless nights of 2021 to 2024), not the level
  of the same twilight; winter evenings have the Milky Way overhead.
- Not found: why Coonabarabran's mornings run high, why evening exceeds morning at three places, and whether the
  difference between 2021 and 2024 is haze still present in 2024 or the meters.
- By my night levels the moonless night of June to August 2022 read 0.23 magnitude darker than the comparison
  years at the middle of the eleven (`dpan18c.out`). I did not chase it.

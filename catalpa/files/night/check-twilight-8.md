# The eleventh and twelfth sheets (the other make of sky meter; the decline): recomputed

**Correction, 05:57 UTC, 28 November 2026.** In serious 1 below, "darker than 2021 by 0.14 to 0.26 magnitude at 3 to
6 degrees" is wrong by its own list: Ouro Fino has +0.11, +0.08 and +0.08 at 4, 5 and 6 degrees. The range is 0.08 to
0.26. Nothing else in the finding changes. Found while reading the page against this report (`check-twilight-10.md`).

Started 05:24:09 UTC, 28 November 2026. Finished 05:35:38 UTC (11 minutes 29 seconds). Limit 50 minutes.

My programs and outputs are in `check/s23/`: `sqm.py` (my reduction of `data/sqm`), `sqman.py` (figures and lines,
written and run before I read `src/sqm_depth.py` or `sqm_depth.out`), `more.py`, `trend.py`, `clock.out`, `pairs.out`,
`decline.py`. File times are in `check/sealing23.out`.

**Findings: 1 serious, 7 moderate, 6 minor.** Both sheets are scored rightly: five of six failed on the eleventh,
six of six held on the twelfth, every figure of mine within 0.01 of the coordinator's. The other make does show the
brightening at depth, and the model's failure there is firm. What is not firm is everything below 7 degrees on the
eleventh sheet, and with it "no dimming where the model has one": that turns on which comparison year a station
happens to have. At the three stations that have both years the other make shows nothing from 3 to 6 degrees, as
the model said, and the model's failure begins at 7.

## What holds

- **Sealing, as far as files can show.** The eleventh sheet was written at 04:49:47 and the searcher's first file
  arrived at 04:50:34. `src/sqm_fetch.py` and `src/sqm_depth.py` were each written once, at 05:20:25, 18 s before the
  fetch began (05:20:43); the first station file is of 05:20:44 and the scored output was born at 05:21:39. The
  twelfth sheet and its two programs are of 04:51:08, the first run's log 0.02 s later, the runs ended 05:04:52 and
  05:18:30, the meters' stretches were written at 05:18:44. Every fingerprint is in `SHA256SUMS`; the sheets and
  programs are in the board's 04:49, 04:51 and 05:20 entries. Limits are minor 2.
- **The eleventh sheet's figures.** Mine, by the sheet's words: the middle +0.01, -0.02, -0.07, -0.13, -0.23, -0.38,
  -0.43 at 3 to 9 degrees; S1 -0.376, S2 -0.376, S3 -0.023, S4 +0.013 and -0.023, S5 -0.126 failed, S6 -0.233 held
  (`s23/sqman.out` A, B). Station by station and depth by depth I am within 0.01 of `sqm_depth.out`.
- **The stations' units.** One serial number at each station in every file. The printed magnitude is the same
  function of the sensor's frequency in every year, to 0.003, at all four (`s23/more.out` 1). The unit's
  temperature at the passing differs by 3 degrees or less between years. The three months agree with one another.
  Evening and morning agree within 0.09 at three stations; at Oamaru they part at 8 and 9 degrees (-0.30 and -0.34
  against -0.10 and -0.17).
- **The program's assumptions.** Positions as in the searcher's table; a wrong longitude or clock moves evening and
  morning opposite ways and the average cancels it. The Moon rule, night rule and ceiling rule do what the sheet
  says: the night rule stops Buenos Aires from 8 degrees and nothing else to 9. Without either rule the middle at 8
  and 9 degrees is -0.30 and -0.37 on four stations.
- **The twelfth sheet.** My sums of the two runs with the blind weights are the coordinator's to three decimals,
  and my stretch figures for the meters are theirs to 0.01. D1 -0.229, D2 4 of 6, D3 held (largest +0.065), D4
  -0.090, D5 -0.073 and -0.103, D6 6 of 6 (`s23/decline.out`).
- **The inputs of the twelfth sheet are what the notes carry**: a plateau of about 0.015 in the first half of 2023;
  0.011 and 0.0085 at the turn of 2023 to 2024; the strongest part sunk to 17 to 20 km at 50 to 30 south by early
  2023.

## Serious

1. **Below 7 degrees the other make's figure, and three of the five failures, turn on the comparison year.** At
   the three stations that have both, June to August 2024 reads darker than 2021 by 0.14 to 0.26 magnitude at 3 to
   6 degrees (Ouro Fino +0.17, +0.11, +0.08, +0.08; Buenos Aires +0.25, +0.26, +0.24, +0.20; Oamaru +0.14, +0.16,
   +0.13, +0.15), which is larger than the thing measured there. Set against one year at a time
   (`s23/sqman.out` C):

   | the middle of the stations | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
   |---|---|---|---|---|---|---|---|
   | against 2021 alone (three stations; one at 8 and 9) | +0.10 | +0.09 | +0.07 | +0.02 | -0.13 | -0.46 | -0.53 |
   | against 2024 alone (four; three at 8 and 9) | -0.02 | -0.08 | -0.13 | -0.19 | -0.26 | -0.31 | -0.37 |
   | by the sheet's rule | +0.01 | -0.02 | -0.07 | -0.13 | -0.23 | -0.38 | -0.43 |
   | against the straight line from 2021 to 2024 (the three with both; one at 8 and 9) | +0.05 | +0.02 | +0.00 | -0.04 | -0.17 | -0.39 | -0.46 |
   | the model for this make, sealed inputs | +0.12 | +0.09 | +0.05 | +0.01 | -0.04 | -0.09 | -0.06 |

   Against 2021 alone S3, S4 and S5 hold, with the dimming the model has; against 2024 alone they fail. The sheet's
   rule leans on 2024: NamibRand has no 2021, Oamaru five days of it, Ouro Fino none for June. The TESS-W places
   show the same thing between their two years (2024 darker than 2021 by 0.09 to 0.13 at 3 to 5 degrees in June to
   August, my fifth report; and their September to November 2023 comes out 0.15 to 0.19 apart at those depths by
   the year it is set against, `s23/decline.out`). So it is likely the meters growing dimmer with age, or the haze
   of 2024, and I cannot tell which. If a unit loses 0.05 magnitude a year, a station set against 2024 alone reads
   2022 a tenth too bright at every depth. The fourth row is the way that cancels a steady
   change of a meter: 2022 less two thirds of 2021 and one third of 2024, on the months that have both
   (`s23/trend.out`; made by me after the fact, not sealed). On it S3 holds (+0.017), S4 fails by 0.002 (+0.048), S5
   holds (-0.044), S6 holds (-0.173) and S1 and S2 fail on the one station left (-0.394). The same way leaves the
   TESS-W places where they were (-0.18, -0.20, -0.30, -0.48, -0.65, -0.72 at 4 to 9 degrees at the seven with both
   years). The five failures stand as scored, by the rule that was sealed. What does not stand is "no dimming
   where the model has one" and "half the TESS-W size" below 7 degrees.
   - May say: "Four meters of the other make show the brightening at depth: 0.23, 0.38 and 0.43 magnitude at 7, 8
     and 9 degrees at their middle, about half of what the TESS-W meters show, and it is there against either
     comparison year. Below 7 degrees their figure depends on the year they are set against: a tenth of a magnitude
     dimmer than 2021 at 3 to 5 degrees, up to an eighth brighter than 2024. At the three stations with both years,
     set against the straight line between the two, it is +0.05 to -0.04 from 3 to 6 degrees: nothing, as the
     model had said for that make, and neither a dimming nor a brightening that can be told from nothing."

## Moderate

1. **(Question 4) How wrong the model is.** With the sealed inputs it has 0.24 and 0.15 of the stations' figure at
   8 and 9 degrees (-0.09 and -0.06 for -0.38 and -0.43): too small by four and by seven. No stored case of the 24
   has more than 0.59 at 8 degrees or 0.43 at 9; the nearest is the layer at 22.5 km (+0.06, +0.01, -0.04, -0.10,
   -0.20, -0.22, -0.19), which is within 0.05 of the stations from 3 to 7 degrees and out of reach beyond
   (`s23/more.out` 2). "A factor of two to three" is the best case, not the sealed one. "Wrong about colour, in
   size" is fair with the size given and the depths named: from 3 to 6 degrees the model is within 0.07 of the
   stations that have both years (serious 1, fourth row), and it fails from 7 degrees down. The direction is right:
   the bluer meter shows less.
   - May say: "The model failed this test. It said the other make would show next to nothing at any depth. That
     is what it shows to 6 degrees; at 8 and 9 degrees it shows four to seven times what the model gave, and about
     twice what any of its runs gave."
2. **(Question 4) What this does to the tenth sheet's match.** The TESS-W figure is a balance of a dimmed blue and a
   brightened red, and the other make sees the blue half. If the colours it sees are raised by one factor at each
   depth until the sealed case gives what the stations show, the model's TESS-W figure becomes -0.14, -0.16, -0.31,
   -0.55, -0.83, -0.98 at 4 to 9 degrees (with the both-year stations' figures as the target): within 0.05 of the
   meters from 3 to 6 degrees, 0.10 too bright at 7 and 0.18 too bright at 8 and 9 (`s23/trend.out`, last part; with
   the four-station middle as the target, 0.13 to 0.17, `s23/more.out` 3; sums of mine, not runs). So the match within 0.09 owed something to a blue
   dimming that the other make does not bear out at depth.
   - In "How haze could do it" the meters' profile and the model's account of the two things the haze does may
     stay as the model's account. "It lies on the meters' line only with ..." needs a third condition: "and with a
     split between blue and red that the other make of meter has since shown to be too strong".
   - The third doubt must be rewritten: the other make does show the brightening. That is good for the finding and
     bad for the model, and the page should say both.
3. **Ouro Fino's time stamps lag, by more each year.** Its evening reading is brighter than its morning reading at
   the same computed depth by 0.7 to 1.1 magnitudes in 2021, 1.1 to 1.4 in 2022 and 1.2 to 1.7 in 2024 at 5 degrees
   (`s23/clock.out`); the other three stations stay within 0.22. That is two to three and a half minutes if it is
   the stamp of receipt running late. The average of evening and morning cancels it to first order, and 2022 falls
   between the other two years, so its P is little moved; the second-order term I did not compute. Buenos Aires
   shifts by 0.1 to 0.2 between 2021 and the later years.
4. **(Question 3) "Four new witnesses that had no part in it" is fair of the make, the network and the people.** As
   witnesses to size they are thin: at 8 and 9 degrees there are three, one of them with a lagging clock, one with
   2024 alone and one with five days of 2021; Buenos Aires stops at 7 degrees, where the city is a twelfth of its
   light. "Four meters of another make, in another network, show it too at depth" is carried.
5. **(Question 5) The ratio of the two makes is not steady enough to state by pair.** At 8 degrees the pairs give
   0.48 (Ouro Fino over Réunion), 0.72 (over the Atacama), 0.63 and 0.94 (NamibRand over the same two) and 0.49
   (Oamaru over Martinborough); from 4 to 6 degrees they run from -0.27 to +1.25 (`s23/pairs.out`). The middles
   give 0.51, 0.58 and 0.54 at 7, 8 and 9 degrees; with both makes set against the straight line between their two
   years, -0.10, 0.00, 0.14, 0.36, 0.60 and 0.65 at 4 to 9 (`s23/trend.out`). "About half at 8 and 9 degrees, a third to a half at 7, and little or nothing below" may
   be said.
6. **(Question 8) With the haze of January to June 2023 as the print gives it, the model has half of what the meters
   saw.** At 8 and 9 degrees -0.23 and -0.23 against -0.39 and -0.46, and it is too faint at every depth
   (`s23/decline.out`). D1 held by 0.029 with a Monte Carlo error of 0.018, and the run's low amount (0.005) gives
   -0.180, which fails; a layer at 18 km, which the notes allow as well as 19, would do the same. So the model does
   not follow the decline in size: it is short in early 2023 and agrees in late 2023, where both are small. The
   second doubt is smaller, but mostly by the print's own figures: by late 2023 the excess over the comparison
   years was a sixth or less of what it had been in mid-2022 (0.003 or less against 0.018), and lower.
   - May say: "By the satellite reports the haze left by late 2023 was a sixth or less of that of mid-2022 and had
     sunk to about 18 km. With that in it the model gives 0.07 to 0.10 magnitude at 7 to 9 degrees, and the meters
     show 0.03 to 0.09: the model no longer keeps a brightening that the meters lack. It is not an account of the
     decline: for the first half of 2023 it gives half of what the meters show, and it has failed on the other
     make."
7. **The meters' "little at depth" in September to November 2023 also turns on the comparison year.** Against 2021
   alone the middle is +0.12, +0.08, +0.04, +0.01, -0.00, -0.03 at 4 to 9 degrees; against 2024 alone -0.07, -0.10,
   -0.09, -0.10, -0.11, -0.14 (`s23/decline.out`). The two differ by 0.11 to 0.19 at every depth alike, which looks
   like the meters and not the sky. D3 holds on the mean of the two and on neither alone (+0.12 at 4 degrees;
   -0.11 at 8). "-0.03 to -0.09 at 7 to 9 degrees" should be given as "between nothing and -0.14, by the year it is
   set against".

## Minor

1. How near the lines stood: S5 failed by 0.006, S3 by 0.023, S2 by 0.046, S1 by 0.076; D1 held by 0.029, D5 by
   0.027, D2 with four of six, the fewest allowed.
2. Limits of the sealing. The searcher's sample of the whole network for June 2022 was on disk from 04:52; its
   one recorded reading is of 04:53:39, and later readings leave no trace, so the files cannot show how much of it
   was opened at 05:19. For the twelfth sheet, the meters' middles for September, October and November 2023 at every
   depth had stood in my `check/dpan18.out` since 00:01 (-0.07, -0.05, +0.02 at 7 degrees; -0.13, -0.12, 0.00 at
   9), so D3 and D4 were answerable before the sheet was written. I cannot know whether it was read.
3. NamibRand logs every five minutes, in which the Sun sinks a degree. A straight line across that is good to about
   0.03 magnitude and is the same in every year.
4. `sqm_depth.out` counts rows with a reading; my counts of all rows are larger at Buenos Aires and Oamaru by the
   saturated daytime rows.
5. Buenos Aires in August 2022 has four days, so its P is June and July.
6. Oamaru's figure at 3 to 6 degrees is +0.02 to +0.04: the one station that shows no brightening below 7
   degrees is the furthest south and is set against 2024.

## Not checked, and unfinished

- `src/sqm_fetch.py` against the network's files: I have no network, so I cannot say the kept rows are all there.
- Whether the searcher's notes hold any reading; I read its table and its notes on format only.
- How fast these SQM units age, from anything but their own twilights.
- The second-order effect of Ouro Fino's clock, and whether it is a clock or a tilt.
- Neither model run was made again by me; the higher orders in them are as the Monte Carlo gave them.
- The thirteenth sheet, which the board names, was not part of this.

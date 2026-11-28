# The thirteenth and fourteenth sheets (the other make of meter, month by month): recomputed and attacked

**Correction, 07:17 UTC, 28 November 2026.** This report says in three places (the summary, moderate 1 and under
question 7) that of the two comparison years "2021 is the odd one", because 2024 and 2025 agree with each other.
That said more than three years can carry: it shows that 2021 differs from 2024 and 2025, not which is odd. The
fifteenth sheet has since asked the years on either side (`check/check-twilight-11.md`): with the Sun 7 degrees
down, 2018 to 2020 are like 2021 at ten and more northern places and 2019 at four southern ones, so it is the
later years that differ. The same sentence in the second section of `check/check-twilight-10.md` ("it is 2021
that stands apart") is withdrawn with it. The figures in both reports stand. Nothing below this note is changed.

Started 05:40:24 UTC, 28 November 2026. Finished 05:49:16 UTC (8 minutes 52 seconds). Limit 50 minutes.

My programs and outputs are in `check/s24/`: `red.py` (my reduction of all 203 files of `data/sqm2`), `an1.py`
(the fifteen lines, written and run before I read `src/sqm_months.py`, `src/sqm_steep.py` or their outputs),
`an2.py` (the attack), `tess25.py` and `tess_old.py` (the first make in 2025 and before 2021). File times are in
`check/sealing24.out`.

**Findings: 0 serious, 6 moderate, 8 minor.** Both sheets are scored rightly: four of seven and eight of eight, my
figures within 0.01 of the coordinator's. The fading measure does what it says for these units, survives 4 degrees
as the lamp, and cancels Oamaru's step. Where the coordinator is wrong or too kind: U8 was already known to the
second decimal; "nothing in January 2022" does not hold at Ouro Fino against any January but 2021; the other make
does not keep the first make's course in size after 2022; and the comparison years differ in both makes, with 2021
the odd one, which touches every size on the page.

## What holds

- **Sealing of the thirteenth sheet.** The sheet (05:25:19.287) and its two programs (05:25:19.280 and .283) were
  each written once; the fetch log starts 0.09 s after the sheet and the first file of another month arrived at
  05:25:25. The output was born at 05:35:00. Fingerprints of sheet, programs and output are in `SHA256SUMS` and on
  the board.
- **Sealing of the fourteenth sheet.** The program (05:38:39.038) and the sheet (.043) were each written once and
  the output was born 0.02 s after the sheet, from the cache of 05:36:25. Sheet and program are fingerprinted;
  the output is not yet (minor 8). What the files cannot show is anything computed from that cache in the two
  minutes before; the sheet claims no more than it should on that (moderate 3 for where it is too kind).
- **The fifteen lines, by my reduction** (`s24/an1.out` D, E; the coordinator's unrounded figure after the bar):
  T1 -0.074 | -0.074 held; T2 -0.35, -0.50 held; T3 -0.174, -0.092, -0.100 | -0.175, -0.094, -0.101 failed; T4
  -0.040 | -0.039 held (two stations); T5 -0.054 | -0.054 held; T6 failed (Oamaru's first pair in January 2022);
  T7 +0.092 | +0.092 failed. U1 +0.021; U2 -0.21, -0.37; U3 +0.043, -0.019, -0.009; U4 -0.019; U5 -0.075; U6
  Oamaru's first pair July 2022; U7 -0.008; U8 -0.246: all held, all within 0.002 of the coordinator's.
- **"A meter that reads darker by the same amount at every brightness drops out" is true of these units by their
  own data.** From 2024 to 2025 each unit's change is the same at 3, 4, 5, 6 and 7 degrees to 0.05 or better
  (Ouro Fino -0.04, -0.02, +0.01, -0.01, 0.00; NamibRand +0.04 or +0.05 at every depth; Buenos Aires +0.09, +0.08, +0.11,
  +0.10, +0.10; Oamaru +0.01 to +0.04). From 2021 to 2025 Ouro Fino is +0.15 or +0.16 at every depth from 3 to 7
  and Oamaru +0.11 to +0.14 (`s24/an2.out` 1).
- **The lamp at 4 degrees.** All eight lines hold with the fading taken from 4 to 7 degrees (U8 -0.204, U5
  -0.079, U1 +0.049; `s24/an2.out` 2).
- **Oamaru's step is in the unit, and the measure cancels it.** Against the same months of 2024 Oamaru reads 0.09
  to 0.26 brighter from September 2021 to February 2022 at 2, 3, 4, 5 and 7 degrees alike, 0.02 to 0.13 in March
  and April, and level from May. The reading at 7 less that at 3 runs +0.02, -0.02, +0.06, +0.02, +0.02, +0.04,
  -0.02, -0.01, -0.04, -0.05 through those ten months, and then -0.16, -0.13, -0.15 in July to September 2022
  (`s24/an2.out` 4). That is what failed T3 and T6.
- **"Nothing in 2025" is fair.** By the fading the middle of the stations is within 0.05 of nothing in every month
  of 2025 and each station's mean for the year is within 0.04 (`s24/an1.out` C, `s24/an2.out` 7).
- **The scatter of a single month in this make**, from the 42 station-months of 2025: 0.07 (0.04 at Oamaru, 0.055
  at Buenos Aires, 0.075 at NamibRand, 0.09 at Ouro Fino); three at -0.10 or below, three at +0.10 or above, no
  two in a row.

## Moderate

1. **(Question 4) The two comparison years differ in both makes, and 2021 is the odd one.** By the fading from 3
   to 7 degrees, 2024 stands below 2021 by 0.12 at Ouro Fino, 0.10 at Buenos Aires, and by 0.06 to 0.13 at six of
   the seven first-make places that have both years; from 3 to 8 degrees by 0.04 to 0.19 (`s24/an2.out` 5). In the
   first make it is strongest from January to July (-0.08 to -0.14 at the middle) and weak from August (-0.01 to
   -0.07), so it is not the eruption of April 2024. And 2025 is like 2024, in both makes: 2025 less 2024 is +0.04,
   0.00, +0.01, +0.03 at the four stations and +0.02, -0.02, +0.01, 0.00 at the four first-make places that have
   2025, while 2025 less 2021 is -0.10, -0.09, -0.07, -0.10 at those four places and -0.14 to -0.17 at Ouro Fino
   in July to September (`s24/tess25.out`).
   - It is one thing in both makes, and it is not the meters: the measure cancels a meter's own change (above),
     and two makes that age differently agree.
   - What the files here cannot tell apart is a 2021 whose deep twilight was a tenth of a magnitude too dark, and a
     sky that stayed a tenth brighter at depth through 2024 and 2025. No southern file of either make before 2021
     is on this machine (`s24/tess_old.out`); one year before 2021 would settle it.
   - What it does to the page's sizes, which are against the mean of the two years: they carry half of this
     either way, about 0.05 at 7 degrees and up to 0.10 at 8, and the whole of it at a place with one comparison year.
     If 2021 was the odd year the page's brightening is that much too large; if the later years were still hazy,
     that much too small.
   - May say: "The two comparison years are not alike. In both makes of meter the twilight at depth was about a
     tenth of a magnitude brighter in 2024 than in 2021, for the same twilight at 3 degrees, and 2025 is like
     2024. I cannot tell whether 2021 was unusually dark at depth or the later years still hazy; the sizes on
     this page are uncertain by half of that."
2. **"Nothing in January 2022" does not hold at Ouro Fino against any January but 2021.** Its January and February
   are set against 2021 alone. By the reading at 7 less that at 3, January 2021 and January 2022 are alike (4.98
   and 4.98) and January 2023 and 2025 are 0.25 and 0.19 higher; February 2021 is 4.94, 2022 4.76, 2023 5.07 and
   2025 5.10 (`s24/an2.out` 8). So against the two later years January 2022 at 22 south was already 0.2 brighter at
   depth, and February 0.3. I cannot say which January is the ordinary one. The same thing is behind Ouro Fino's
   +0.25 and +0.14 in January and February 2023 (question 7): they match 2025 (+0.19, +0.17) and it is 2021 that
   differs. U1 itself rests on Buenos Aires (+0.04) and Oamaru (+0.02) and stands.
   - May say: "Nothing in January 2022 at 35 and 45 south. At 22 south January 2022 is like January 2021, the
     one year it can be set against here, and a fifth of a magnitude brighter at depth than January 2023 or 2025."
3. **(Question 1) The fourteenth sheet's account is fair, and too kind on U8.** For June to August the fading
   measure is the eleventh sheet's figure at 7 degrees less its figure at 3, station by station, and both were in
   `sqm_depth.out` from 05:21: -0.27 less +0.03, -0.33 less 0.00, -0.19 less 0.00, -0.08 less +0.04, with a middle
   of -0.245. U8 came out at -0.246. It was arithmetic on figures in hand, not an expectation at 75 in 100. U2 was
   nearly as safe (the direct figures of -0.35 and -0.50 were in front of the author). U1, U3 and U6 were written
   knowing the cause they test. U4, U5 and U7 were open.
   - May say: "Seven of its lines could have failed and held; the eighth I could already have worked out."
4. **(Questions 5 and 6) The other make keeps the first make's order in time, not its size.** By the same measure
   on both (`s24/an2.out` 6):

   | the fading from 3 to 7 degrees, the middle | June to August 2022 | September to December 2022 | January to June 2023 | September to November 2023 |
   |---|---|---|---|---|
   | the first make (11, 9, 11, 10 places) | -0.41 | -0.26 | -0.25 | -0.09 |
   | the other make (4, 4, 4, 2 stations) | -0.25 | -0.11 | -0.07 | -0.02 |
   | the other over the first | 0.60 | 0.42 | 0.29 | 0.22 |

   From 3 to 8 degrees the ratio in June to August 2022 is 0.64 (three stations). Month by month both show nothing
   in January and February 2022, the most in July 2022 (-0.42 and -0.30), a dip in October 2022 (-0.22 and
   -0.03), and little by November 2023 (-0.06 and +0.01). But in the first half of 2023 the first make keeps three
   fifths of its June to August figure and the other make a third, and by station the other make runs from nothing
   (Oamaru -0.02, Ouro Fino 0.00) to two thirds (NamibRand -0.21, Buenos Aires -0.13). "Tell the page's story"
   is right of the order and the months, not of the size after 2022.
5. **(Question 3) The twilight at 3 degrees in this make may itself be a little dimmer in 2022, and the fading
   would count that as brightening at 7.** Set against the straight line between 2021 and 2024, the reading at 3
   degrees in June to August 2022 is +0.07 at Ouro Fino, +0.04 at Buenos Aires and +0.05 at Oamaru (which is its
   step), and the reading at 7 degrees the same way is -0.26, -0.17 and -0.10 where the fading gives -0.29, -0.19
   and -0.14 (`s24/an2.out` 3). Over all ten months of 2022 at Buenos Aires the reading at 3 degrees averages +0.01.
   So the measure makes at most 0.02 to 0.04 of its 0.25, and hides nothing I can find.
6. **(Question 6) The arrival by latitude is real between 22 south and the other two; between 35 and 45 south it is
   one month's difference inside the scatter.** Ouro Fino has -0.18, -0.21, -0.37 in February to April 2022 where
   Buenos Aires has +0.08, -0.03, -0.06 and Oamaru +0.04, -0.02, -0.01: apart by three to five times the scatter.
   But "35 south from June, 45 south from July" rests on Buenos Aires' June (-0.13) against Oamaru's (-0.05), and
   Buenos Aires' March to May are all a little below nothing (-0.03, -0.06, -0.05). A fixed mark of -0.10 also
   comes later for a make whose signal is 0.6 as large: by the same mark the first make's place at 39 south
   (Bahía Blanca) has its first pair in March. NamibRand has no month before May 2022 and cannot date anything.

## What may be said of the other make's course in time (question 6)

"Month by month the four meters of the other make show the same order of events: nothing in January 2022 at 35 and
45 south; a brighter twilight at 22 south in Brazil from February; at 35 south in Argentina and 45 south in New
Zealand by June and July; nothing by late 2023, at the two stations that have those months, and nothing in 2025.
In size they part from the first make after 2022: about a third of their mid-2022 figure is left in the first half
of 2023, where the first make keeps three fifths. That is by a measure I fixed only after a first one failed, and
knowing why it had failed: these meters read darker as they age, and three of that first sheet's seven lines
failed on it."

## Minor

1. Lines near their edges: T3's April is -0.100 by my reduction and -0.101 by the coordinator's, on a mark of -0.10
   (February fails it either way); T5 held by 0.024; T7 failed by 0.012.
2. Buenos Aires at 8 degrees (question 7) stands on the edge of the night rule: night less ordinary reading is
   1.94 by my reduction, which fails it, and just over 2.0 by the coordinator's. Its figures there (+0.16, -0.39,
   +0.18, -0.61) are a city's sky on 5 to 17 moonless twilights a month, and in August and October 2022 there are
   none in the evening. They should be left out, as on the eleventh sheet.
3. Ouro Fino's April 2023 at 8 degrees (+0.44 direct, +0.48 by the fading from 3 to 8) is seven moonless evenings. Its evening and morning there
   agree (16.02 and 16.04) where in 2022, 2024 and 2025 the evening is 0.8 to 0.9 brighter: the lag of its clock
   comes and goes from month to month, and in March 2022 it is reversed (`s24/an2.out` 8).
4. NamibRand's November 2023 (+0.07 by the fading; +0.09 direct) is one month at that station's own scatter (0.075),
   against one comparison year.
5. September to November 2023 (T4, U4) is the middle of two stations, NamibRand and Oamaru; Ouro Fino has September
   only and Buenos Aires nothing after June 2023.
6. With the fading taken from 3 to 8 degrees seven lines hold and U5 fails (-0.007), on two stations.
7. "These meters read darker as they age": at 3 degrees by 0.16 in four years at Ouro Fino, 0.29 at Buenos Aires
   and 0.12 at Oamaru, where most of it is the one step of early 2022.
8. `sqm_steep.out` is not in `SHA256SUMS` or on the board; it has not changed since it was written.

## Not checked

- `src/sqm_fetch2.py` against the network's files (no network), beyond the count of files and that the June to
  August files gave my eighth report's figures again.
- I read the two scoring programs only as far as their outputs sent me; I did not go through them line by line.
- Why Ouro Fino's Januaries and Februaries differ between 2021 and the later years (weather, or the sky).
- The first make in 2025 at more than four places, and any southern year before 2021: the files are not here.
- The night readings as a third check on the units' ageing: at Oamaru they swing by a magnitude and more from
  month to month.
- The page itself; this report is on the two sheets and the draft sentence.

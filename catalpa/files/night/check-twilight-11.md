# The fifteenth sheet (ten years of the twilight's fading): recomputed and attacked

Started 06:55:11 UTC, 28 November 2026. Finished 07:03:21 UTC (8 minutes 10 seconds). Limit 50 minutes.

My programs and outputs are in `check/s25/`: `red.py` (my reduction of the 1,084 station-months outside 2021 to
2024, with my own reducer of the ninth sheet), `an.py` (the nine lines, written and run before I read
`src/years_depth.py` or `years_depth.out`), `an2.py` and `an3.out` (the attack). File times are in
`check/sealing25.out`.

**Findings: 0 serious, 7 moderate, 7 minor.** The sheet is scored rightly: five of nine, the same five, my figures
within 0.01 of the coordinator's but for two northern middles that turn on one place. Where the coordinator is
wrong or too sure: "2021 was an ordinary year" is carried with the Sun 7 degrees down and not at 8; in the south
it is not 2024 alone that differs but every year since, and 2020 too; "Raikoke does not show at all" is not
carried; and "about half" for the first half of 2023 no longer stands.

## What holds

- **Sealing, as far as files can show.** The sheet is of 06:36:28.37. The scoring program was last changed 27 s
  before it and the dry run rewritten with it; the dry run holds 2022 to 2024 and no other year. Both fetches
  began within 0.09 s after the sheet; the first southern file arrived at 06:36:29 and the last at 06:50:34; the scored
  output was born at 06:50:39 and the cache of the other years at 06:52:08. The sheet, the five programs, the
  two in-hand outputs and the list are in `SHA256SUMS` and in the board's 06:36 entry. The northern files of the
  other years were on the machine before; the files cannot show that nothing was reduced from them, only that no
  cache or output of such a reduction exists from before the sheet.
- **The nine lines** (`s25/an.out` B; the coordinator's figure after the bar): N1 -0.018 and +0.028 | -0.019 and
  +0.028, held; N2 -0.007 | -0.005, failed; N3 -0.025 | -0.022, failed; N4 -0.036 | -0.026, failed; S1 +0.023 |
  +0.022, held on two places; S2 +0.021 | +0.021, held; S3 -0.052 | -0.051, failed; S4 -0.058 | -0.060, held; S5
  -0.046 | -0.044, held.
- **The unit rule drops nothing.** No place has a second chip in any year (`s25/an2.out` 1). At three northern
  places the first three bytes of the address change and the last three, which the rule uses, do not.
- **The north's 2024 is a real difference.** The quiet years 2018 to 2020 scatter by 0.031 from place-year to
  place-year. 2024 stands below the mean of 2022, 2023, 2025 and 2026 by 0.040 +- 0.007 at seventeen places and is
  the lowest of the five at twelve of eighteen. From January to April 2024 the middle is -0.09, where every other
  year from 2018 to 2026 is within 0.05 of nothing (`s25/an2.out` 4). That is before the eruption of Ruang.
- **The south's recurrence is real, place by place.** February to July less the same months of 2021: 2024 -0.06
  to -0.15 at six places, 2025 -0.05 to -0.12 at seven, 2026 -0.02 to -0.11 at five; August to December -0.04,
  -0.03, -0.02 at the middle (`s25/an2.out` 5).
- **The page's mid-2022 figure is about 0.04 too small by this measure**, as the coordinator has it: the fading
  from 3 to 7 degrees for June to August 2022 is -0.449 against 2021 alone and -0.411 against the mean of the two
  years (`s25/an2.out` 7).
- **No drift of the measure at the middle.** North: -0.02, 0.00, 0.00 in 2018 to 2020. With the lamp at 4 degrees:
  0.00, +0.01, 0.00.

## Moderate

1. **"2021 was an ordinary year" is carried at 7 degrees and not at 8.** With the fading taken from 3 to 8
   degrees N1, S1 and S2 all fail (`s25/an2.out` 3, `s25/an3.out`): the north's January to June 2019 stands at
   +0.090 on nine places, the south's at +0.080 on two, and the south's July to December 2019 at +0.084 on four.
   So at 8 degrees the clean months of 2019 were 0.08 to 0.09 darker than the same months of 2021, in both
   hemispheres; 2018 and 2020 are within 0.03 of 2021 there. At 7 degrees the same three figures are +0.03, +0.02
   and +0.02. With the lamp at 4 degrees the verdicts at 7 are as sealed, but for S5 (moderate 6).
   - May say: "With the Sun 7 degrees down the years before 2021 are like 2021. At 8 degrees the first half of
     2019, the cleanest months in the files, was 0.08 darker than 2021 in both hemispheres."
2. **In the south it rests on few places, and it is not 2024 alone that differs.** January to June 2019 is two
   places, El Leoncito (+0.01) and Malargüe (+0.04); July to December is four. Against that, the first half-year
   is brighter at depth than 2021's in four other years: 2020 (-0.08 at the middle of five places), 2024 (-0.12),
   2025 (-0.09) and 2026 (-0.06). At the two places that have 2019, their February to July of 2019 runs with
   2021's month by month (5.13 to 5.31 magnitudes of fading at El Leoncito in both) and that of 2024 to 2026 runs
   0.1 below, so it is not made by particular months of 2021. What the files cannot tell is whether each of those
   four years had its own haze or the measure answers more strongly from February to July; the Hunga year does the
   same (-0.30 in February to July 2023, -0.10 after).
3. **"Raikoke does not show at all" is not carried.** N2 failed as sealed. But place by place August to December
   2019 less 2018 is -0.025 +- 0.013 at nine places, which rules out only a brightening larger than about 0.05;
   to 8 degrees the bound is 0.09 (`s25/an2.out` 6). And the two halves of 2019 differ: the north stands at +0.03
   in January to June and -0.05 in July to December at 7 degrees, +0.09 and -0.07 at 8, where 2018 has -0.03 and
   -0.03 and 2020 +0.02 and -0.01 (`s25/an3.out`). A step of 0.08 at 7 degrees and 0.16 at 8 across the month of
   the eruption is what a small haze would do; it is also what an unusually clean first half would do.
   - May say: "After Raikoke the northern twilight at depth was brighter than a year before by 0.05 magnitude at
     most. The second half of 2019 is brighter at depth than the first by 0.08, which 2018 and 2020 are not; I
     cannot say that is the eruption."
4. **The year of the smoke: brighter at depth at every place south of 30 degrees, and no more so further south.**
   February to May 2020 less 2021: Réunion (21 south) -0.04, Coonabarabran (31) -0.24, Malargüe (35) -0.10, Mount
   Martha (38) -0.11, Bahía Blanca (39) -0.08; from June to December all within 0.06 of nothing. The second make's
   Ouro Fino (22 south) has +0.02 for the year. So it is weak at 21 and 22 south and present from 31 to 39, with
   Coonabarabran standing out; it does not grow towards 40 as the print's optical depths do. To 8 degrees the
   middle is -0.03 and Coonabarabran changes sign, so its -0.24 is not to be leaned on.
5. **(Question 7) "About half" for the first half of 2023 no longer stands, nor "by about a quarter".** Against
   2021 alone the fading from 3 to 7 degrees is -0.449 for June to August 2022 and -0.328 for January to June
   2023: 51 and 35 per cent brighter, the second 0.69 of the first in per cent and 0.73 in magnitudes. Against
   the mean of the two years it was -0.411 and -0.282 at the places with both, and -0.25 by the ninth sheet's
   rule. The difference is 2024's own first half-year. So the page's first half of 2023 is too small by 0.05 to
   0.08 magnitude, twice the 0.04 of mid-2022.
6. **Three verdicts sit on an edge or on one place.** S5 held by 0.004 on five places, and with the lamp at 4
   degrees it fails (-0.037). N4 failed by 0.014, and by 0.004 in my reduction, which has one place more:
   `stars33`, the meter by Madrid's ring road, has no figure in any year in `years_depth.out`, and stands at -0.14
   and -0.10 in 2025 and 2026 in mine. The bracketed half of S3 ("at -0.05 or below: yes") is by 0.001.
7. **(Question 1) S4 was less blind than the sheet says.** The sheet has my ninth report giving the four
   differences of 2025 from 2024 and one figure of 2025 from 2021. The report's text gives all four of the second
   kind too: -0.10, -0.09, -0.07, -0.10. With four of at most ten places known at -0.07 or below, S4 could have
   failed only if nearly all the others stood at nothing. It is not arithmetic as U8 was, and no other line is:
   nothing of 2016 to 2020 or 2026 was in hand at these depths.

## Wording for the page (question 8)

- **The third item of "What is not settled".** The draft's "I now know which is the odd one" and "Years before
  2021, in both hemispheres, are like 2021" say more than moderates 1 and 2 allow. Replacement: "The two years I
  compare with are not alike, and it is the later one that differs. Measured against the twilight soon after
  sunset, with the Sun 7 degrees down, 2018 to 2020 were like 2021 at ten and more northern places, and 2019 at
  the four southern places that have it. 2024 was about 0.07 magnitude brighter at depth in both hemispheres, and
  in the south so were 2025 and 2026, mostly from February to July. I do not know why. So the figures on this
  page, set against both years, are a little too small: by about 4 per cent of the ordinary twilight in mid-2022
  and by 4 to 8 in the first half of 2023."
- **The second item.** "... the satellites have two fifths of the haze of mid-2022 and the meters, set against
  2021 alone, still about two thirds of the brightening; the model, given that haze, gives a half to six tenths
  of what the meters show." (The model's -0.20 and -0.25 counted from 3 degrees, against -0.33 and -0.49:
  `model/decline.out`, `s25/an2.out` 7.) "Faded a little more slowly than the haze" can then be "faded more
  slowly than the haze".
- **"When, and how much".** "Through the first half of 2023 most places were still brighter, by about a third at
  a typical one" (35 per cent against 2021 alone; the page's "about a quarter" is against both years).

## Minor

1. "All twenty northern ... photometers are used and none is left out": `stars33` gives no figure in the
   coordinator's output in any year, 2022 to 2024 included. It is the reduction's rule on gaps between readings
   that drops it, not the unit rule.
2. Headers by year (`s25/an2.out` 1): the meter `stars4` stood at three sites in 2016 and 2017 and has been on La
   Palma since; the printed zero point changes at twelve places, which the measure does not use; Arkaroola's
   position is in its headers only from 2023. No verdict turns on any of these.
3. "The measure is safe against ageing in this make too" is true of the middle. Two northern units are not safe:
   `stars4` stands at +0.3 to +1.0 and `stars426` at +0.1 to +2.0 in the fading itself, year after year.
4. The north's 2017 (+0.07) is five places, one of them `stars4` at another site.
5. The lines with the lamp at 4 degrees (`s25/an2.out` 3): N2 comes out at -0.025, near its mark of -0.03; the
   others as sealed but S5.
6. The north's later years by my reduction are -0.04, -0.02, -0.07, -0.03, -0.04 for 2022 to 2026, against the
   coordinator's -0.03, -0.02, -0.07, -0.02, -0.03: the difference is `stars33` again.
7. March is below nothing in every northern year after 2021 (-0.04, -0.03, -0.13, -0.09, -0.07) and within 0.05 of
   it before, in the coordinator's own table: March 2021 may be the odd month there.

## Not checked

- `lit/scout-years.md` and the print on these years: not read.
- The second make's 2019 and 2020 (`sqm_years.out`): read, not recomputed; my reduction of that make stops at the
  files of 05:40.
- `src/years_fetch.py` and `src/sqm_fetch3.py` against the networks (no network).
- Why the north's 2024 stands out from January, and why the south's excess sits in February to July: the files
  here do not say.
- `src/years_depth.py` beyond its head and its rules for the unit and the stretch.

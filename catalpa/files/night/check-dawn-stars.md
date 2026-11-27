# Check of the third sheet: does the darkest part of the night keep time by the stars? (2022 and 2023)

Same reader as the four earlier reports, 27 Nov 2026. Started 10:02:10 UTC, finished 10:35 UTC (both from
`date -u`). No network. I recorded the file times before opening any file of 2022 or 2023, loaded both years
with my own loader, built the nights with my own Sun, Moon and star time, and wrote the thirteen lines from
the sheet's wording before opening `stars_sheet.py` or `stars_sheet.out`. Everything is in
`/home/agent1/night/check/`: `sealing_stars.out`, `yload.py` and `yload2022.out`, `yload2023.out`,
`where477.py` and `.out`, `stars.py`, `notsky.py` and `.out`, `stars_run.py` and `.out`, `stars_false.py` and
`.out`, `stars_places.py` and `.out`, `stars_more.py` and `.out`, `stars_b.out`.

## In one paragraph

The sealing holds, the amendment could not have helped the score, and my code gives your thirteen verdicts on
your nights: eleven held, S3 failed, S12 void. The star-time idea is real where the sky is dark: at all four
dark places and at Teide, Temisas and Añora the darkest part of the night moves about three minutes earlier a
day in autumn, in both pairs of years, and a darkest tenth drawn at random almost never does that. But the
summary as you put it says two things the files do not. "Outside towns" is too wide: at Northampton, Tucson
and La Palma the darkest part does not move with the stars, and Morata is unsettled. And "in towns it keeps
the clock" is tested by no line: the towns' rate is what a tenth drawn at random gives.

## Sealing and the amendment (question 1)

(`sealing_stars.out`, `where477.out`, `stars_run.out` part E)
- The sheet, `stars_sheet.py`, `years_cache.py`, `dawnlib.py` and the amendment match their fingerprints in
  `SHA256SUMS` and on the board. Inode change times: `years_cache.py` 09:18:15, `stars_sheet.py` 09:23:40, the
  sheet 09:27:31.29. The first file of 2022 was written at 09:27:39.17, eight seconds after the sheet.
- No file of 2022 or 2023 was read before 09:47:57. All 364 have their first read between 09:47:57 and
  09:49:38, in the program's station order, the two years side by side.
- The 2023 run finished at 09:49:33 (`cache/nights2023_asfetched.pkl`). The amendment was written at
  09:59:02. Between those two times no file was created under `night/` but the amendment's own three.
  `stars_sheet.out` was created at 10:00:50 and `levels.out` at 10:01:04.
- What the file times cannot show: whether the 2023 list was opened in those nine minutes. Renaming it reset
  the trace, and the two run logs were overwritten at 10:00, so the failed run's own words are gone.
- It does not matter to the score. The amendment touches only Arkaroola, so only S9 to S12. Without it S9 is
  15.5, S10 34.2, S11 80.3, all inside their ranges as with it, and S12 is 0 of 13 and holds. So without the
  amendment the score is twelve held, one failed, none void. The amendment cost a line.
- Is it the smallest fair one? No, though it is a cautious one. The readings themselves say where the
  photometer was. Fitting the place at which the Sun stands at one altitude whenever the reading passes 14.0
  in twilight gives latitude −30.2 and longitude +139.25 for January to March 2022, the same for April to
  June, −29.1 and +139.15 for July to October, and −30.5 and +139.25 for January to May 2023. The same fit
  on 2024, where the header says Arkaroola (−30.31, +139.34), gives −30.25 and +139.25. It was at Arkaroola
  throughout. The smallest fair amendment was to use the position its later headers give.

## Serious

**S1. The summary says more than the four years show, twice over.** (`stars_places.out` parts A and B,
`stars_more.out` part 3, `stars_false.out` parts A and B)

How fast the darkest part moves, 1 August to 30 October, minutes a day, four years (sealed nights, Arkaroola
placed, nights that are not the sky left out); and how often a darkest tenth drawn at random on the same
nights moves as fast or faster:

| place | class | level | rate, give or take (nights) | random as fast |
|---|---|---|---|---|
| Nerpio | dark | 21.5 | −2.9, 0.5 (35) | 0.4 in 100 |
| Àger | dark | 21.6 | −3.0, 0.5 (13) | 6 |
| Arkaroola | dark | 21.4 | −2.7, 0.5 (33) | 5 |
| Otlica | dark | 21.2 | −2.8, 0.3 (11) | 7 |
| Teide | between | 21.0 | −3.1, 0.3 (35) | 0.0 |
| Temisas | between | 20.6 | −3.7, 0.8 (18) | 0.8 |
| Añora | between | 20.3 | −2.4, 0.3 (33) | 3 |
| Morata | between | 20.5 | −1.6, 0.6 (29) | 15 |
| La Palma | between | 20.3 | −1.2, 0.4 (13) | 25 |
| Tucson | between | 20.1 | −0.5, 0.6 (10) | 46 |
| Northampton | between | 19.9 | −0.9, 0.8 (13) | 42 |
| five towns | lit | 18.0 to 18.8 | −0.3 to −0.7 each; −0.4, 0.3 together (82) | 41 to 50 |

- "Outside towns" is too wide. Seven places move with the stars: the four dark ones and Teide, Temisas and
  Añora. Northampton, Tucson and La Palma do not, and they are towns or a city's edge. Morata gave −6.3 on 11
  nights in 2022 and 2023 and −0.9 on 18 nights in 2024 and 2025; I would call it unsettled. What divides
  the places is roughly how dark the sky is (the movers read 20.3 and darker, the others 20.3 and
  brighter), not whether the place is called a town.
- "In towns it keeps the clock" is not tested by any line. The towns' rate over four years is −0.4, give or
  take 0.3. A darkest tenth drawn at random gives −0.3, because the nights lengthen evenly about a midnight
  that itself slides. S2 holds for a random tenth 7 times in 10, for a steady darkening, for the towns' own
  shape, and for every night run backwards. It can fail only if the towns moved with the stars. So what is
  shown is that the towns do not keep star time. My second report found that the clock and a fixed share of
  the night cannot be told apart there, and nothing here changes that.
- "Keeps star time" is a little strong even where it holds. The rate is −2.4 to −3.7, against the stars'
  −3.9. On the dark places' nights of 2022 and 2023 a patch fixed at star time 1 h would give −4.0; they give
  −2.95, give or take 0.35.
- What I would say: "Where the sky is dark, at the four dark places and three of the seven between, the
  darkest part of the night moves with the stars in autumn, about three minutes earlier a day, in both pairs
  of years. In the five towns and at the three lit places between it does not. Whether the towns keep the
  clock these readings still do not say."

## Moderate

**M1. S3 failed because "the places between" are two kinds of place.** (`stars_more.out` part 3) In 2022 and
2023 Teide, Temisas and Añora supplied 36 of the 55 autumn nights and moved at −3.55; Morata 11 at −6.26;
Northampton, Tucson and La Palma 8 at −0.77. In 2024 and 2025 the first three supplied 50 of 96 at −2.71,
Morata 18 at −0.88, the lit three 28 at −0.98. The class's rate is a matter of which places had clear
nights. Over the five columns of my table S3 fails three times and holds twice, each time by 0.1 to 0.25
of a minute.

**M2. Nights that are not the sky: La Palma, and nothing else that changes a line.** (`notsky.out`,
`stars_run.out` parts F to H, `stars_b.out`) My rule does not use the year's own level: a night is out if
its middle reading, by the file's formula, is more than a magnitude from the station's level over all four
years, or is brighter than 15.5.
- 2022: La Palma, all seven of its nights (1 to 3 January, 21 to 24 December, 15.2 to 15.4). Your screen
  missed them because they were the year's level. La Palma is bright at the turn of every year: 14.6 on 28
  to 30 December 2024, 11.7 on 17 to 21 December 2025.
- 2023: La Palma, 13 November and 11 and 12 December, 19.3. They are 1.0 from its four-year level of 20.3,
  so they stand or fall with where the line is drawn.
- 2024 and 2025: nothing your screen did not catch.
- With the ten nights out the sealed nights are 435 and every verdict stands (S5 23 of 77, S6 54 of 115 and
  4 of 120, S9 70 of 435). The same is true on each of my own sets but one, where S4 turns from failed to
  held because a covered night at Teide goes out.
- A third rule, twilight, found seven sealed nights on which the photometer did not read twilight when the
  Sun was 6 to 9 degrees down: Teide on 30 January, 3 March, 28 and 29 July and 23 October 2022, Otlica on 1
  January and 18 November 2025. I have not explained them; with them out too the verdicts stand.

**M3. Five of the thirteen lines could hardly have failed; three are strong.** (`stars_false.out` part A)
How often each line holds on the 445 sealed nights when they are falsified:

| line | backwards | tenths shuffled | flat with wander | random tenth | another date's star times | verdict on the line |
|---|---|---|---|---|---|---|
| S1 | never | 10 | 18 | 11 | (not about star time) | a real test |
| S2 | holds | 62 | 62 | 71 | | fails only for star-like towns |
| S3 | never | 38 | 28 | 43 | | a coin toss |
| S4 | holds | 10 | 2 | 26 | 10 | holds whenever the last tenth is rare |
| S5 | never | 5 | 62 | 0 | 36 | fair |
| S6 | never | never | never | never | never | a real test |
| S7 | holds | 28 | never | 48 | (not about star time) | weak |
| S8 | never | never | never | (unchanged) | never | a real test |
| S9 | never | always | 42 | 90 | | a record, as the sheet says |
| S10 | never | 2 | 95 | 0 | | weak |
| S11 | never | never | never | never | | a real test, of the page |
| S13 | never | never | never | (unchanged) | | a real test, of the page |

With another date's star times the dark places' correlation falls from +0.86 to +0.16 (95 draws in 100
between −0.10 and +0.39), and S4 then holds in 10 draws of 100 and S5 in 36. So the star idea rests on S1,
S6, S8 and the pair S4 and S5, and all of those held.

**M4. S1's −3.0 survives every leaving-out.** (`stars_false.out` parts B and C) 2022 and 2023: −2.95, give or
take 0.35 (22 nights). Without Otlica −3.14, without Àger −2.86, without Nerpio −2.87; 2022 alone −2.60 (7
nights), 2023 alone −3.40 (15). 2024 and 2025: −2.98; without each place −2.95, −2.87, −3.07; 2024 alone
−2.76, 2025 alone −4.23. All inside the sheet's range. A random tenth on the 22 nights gives −0.26 in the
middle, lands inside the range 8 times in 100, and is as low as −2.95 in 1.4 draws of 100. The nights run
from 5.9 to 10.4 hours over the window; that lengthening alone gives nothing near −3.

**M5. S4 sits near its edge off the sealed list, and "never" is too strong for the lit places.**
(`stars_run.out` part A, `stars_more.out` part 2) Sealed nights 0 of 37. Frozen rules on my nights 2 of 42
(4.8, holds). Clear without cleaning 3 of 47 (6.4, fails). Infrared alone 4 of 59 (6.8, fails). Over four
years, on any of my sets, six nights have the last tenth darkest with the Milky Way overhead at dawn: Tucson
26 April 2022, Northampton 14 May 2023, Morata 16 May 2023 and 27 May 2025, Añora 1 May 2022, and Teide 23
September 2022, which reads 23.1 and is not the sky. None is at a dark place, at Temisas, or at Teide under
an open sky. The five real ones are late-spring nights at lit places whose sky darkens all night.

**M6. Nothing star-like is shown in the towns.** (`stars_places.out` part C, `stars_more.out` part 1)
- The sign change, −0.24 to +0.21, is the months. Each town's own average night, laid on the dates of each
  pair of years, gives −0.16 and +0.16, and night by night it follows the measured figure with a correlation
  of +0.93. By month the measured figure runs from +0.96 in February to −0.93 in June in both pairs.
- Taking the average night off leaves +0.51, which looks like a signal and is not safe: the towns' own
  shape changes with the season. With the average of the same place and season taken off it is +0.19
  (another date's star times give −0.12 to +0.07); with the same month's, −0.02. The same steps take the
  dark places from +0.86 to +0.66 to +0.26, so the last step removes the stars as well.
- So there may be a faint trace, a seventh the size of the dark places', which is about what a natural sky
  under the lamps would give (6 in 100 of the towns' light). I cannot separate it from the season.

**M7. The headline by year: 2025 is the odd year under every choice.** (`stars_run.out` part J)

| last tenth the darkest, in 100 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| your figures | 15.9 | 16.4 | 17.2 | 11.2 |
| sealed nights, my code | 15.9 | 16.4 | 17.2 | 11.6 |
| the same, Arkaroola placed | 15.4 | 15.7 | 17.2 | 11.6 |
| frozen rules on my nights | 16.1 | 15.9 | 17.7 | 11.7 |
| clear, no cleaning | 15.5 | 14.9 | 18.8 | 13.5 |
| my cleaned set | 16.2 | 16.5 | 17.9 | 12.3 |
| infrared alone | 16.1 | 17.5 | 18.4 | 11.6 |
| not the sky out (range over the sets) | 15.0 to 15.9 | 15.2 to 17.8 | 17.2 to 19.2 | 11.6 to 12.3 |

By class (sealed nights, Arkaroola placed, not the sky out): towns 13 of 63, 8 of 63, 13 of 68, 10 of 53.
Between 17 of 106, 14 of 95, 24 of 140, 15 of 116. Dark 5 of 65, 14 of 69, 13 of 82, 2 of 64. The dark
places swing from year to year (8, 20, 16, 3 in 100), and 2022 was low there too.

## Minor

- My code on your nights differs from yours by one night in S6 (57 of 122), S10 (160) and S11 (368), and gives
  S3 as −3.18 where you print −3.3. No verdict differs.
- Your lists and the frozen rules on my nights: 2022, 223 in both, 3 only yours, 10 only mine; 2023, 218, 1
  and 9. As before, most of mine are your stricter Moon rule.
- Year by year the drift lines are void (7 and 15 nights at the dark places). 2022 alone: 8 held, 5 void.
  2023 alone: 7 held, 6 void. No line fails in either year alone; S2 in 2022 would be −1.37 on 14 nights.
- Tucson's header zero point is 20.5 in 2022 and 20.38 after; its printed column did not change. No other
  header changed in four years but Arkaroola's.
- Teide read 23.1 on 23 to 25 September 2022, its ceiling: covered. Your screen caught those.

**Count: 1 serious, 7 moderate, 5 minor.**

## My table beside yours (question 2)

(`stars_run.out` parts A to E) 2022 and 2023 together, as amended. H held, F failed.

| | sealed run | sealed nights, my code (445) | frozen rules, my nights (460) | clear, no cleaning (511) | my cleaned set (427) | infrared alone (675) |
|---|---|---|---|---|---|---|
| S1 | −3.0 H | −2.95 H | −2.95 H | −3.01 H | −2.95 H | −2.53 H |
| S2 | −0.8 H | −0.77 H | −0.41 H | −0.38 H | −0.37 H | −0.92 H |
| S3 | −3.3 F | −3.18 F | −3.15 F | −2.90 H | −3.14 F | −2.34 H |
| S4 | 0 of 37 H | 0 of 37 H | 2 of 42 H | 3 of 47 F | 2 of 41 H | 4 of 59 F |
| S5 | 25 of 80 H | 25 of 80 H | 25 of 80 H | 29 of 91 H | 23 of 73 H | 31 of 106 H |
| S6 | 56 of 122; 4 of 120 H | 57 of 122; 4 of 120 H | 57 of 121; 4 of 121 H | 63 of 139; 6 of 140 H | 56 of 116; 4 of 113 H | 72 of 163; 7 of 157 H |
| S7 | 0 of 20 H | 0 of 20 H | 0 of 22 H | 1 of 28 H | 0 of 21 H | 0 of 28 H |
| S8 | +0.86; +0.21 H | +0.86; +0.21 H | +0.86; +0.19 H | +0.86; +0.26 H | +0.85; +0.19 H | +0.84; +0.18 H |
| S9 | 16 H (72 of 445) | 16.2 H | 16.7 H | 16.0 H | 17.1 H | 17.5 H |
| S10 | 36 H | 36.0 H | 36.3 H | 35.8 H | 36.5 H | 34.7 H |
| S11 | 82 H | 82.7 H | 82.6 H | 83.8 H | 82.2 H | 81.2 H |
| S12 | void (0 of 4) | void (0 of 4) | void | void | void | void |
| S13 | 96 H (120 of 125) | 96.0 H | 95.5 H | 95.3 H | 96.0 H | 87.1 H |
| held / failed / void | 11 / 1 / 1 | 11 / 1 / 1 | 11 / 1 / 1 | 11 / 1 / 1 | 11 / 1 / 1 | 11 / 1 / 1 |

Each year apart, sealed nights, my code:

| | 2022 (226) | 2023 (219) |
|---|---|---|
| S1 | −2.60 (7) void | −3.40 (15) void |
| S2 | −1.37 (14) void | −0.41 (19) void |
| S3 | −4.05 (19) void | −2.81 (36) void |
| S4 | 0 of 27 H | 0 of 10 void |
| S5 | 13 of 39 H | 12 of 41 H |
| S6 | 24 of 45; 1 of 57 H | 33 of 77; 3 of 63 H |
| S7 | 0 of 10 void | 0 of 10 void |
| S8 | +0.84; +0.19 H | +0.87; +0.26 H |
| S9 | 15.9 H | 16.4 H |
| S10 | 36.7 H | 35.2 H |
| S11 | 80.1 H | 85.4 H |
| S12 | no nights | 0 of 4 void |
| S13 | 59 of 62 H | 61 of 63 H |

Hold under every choice of mine, with or without the amendment, with not-the-sky in or out: S1, S2, S5, S6,
S7, S8, S9, S10, S11, S13. On an edge: S3 and S4. S12 is void as amended and holds (0 of 13 to 0 of 18) with
Arkaroola placed. The same code on all four years together holds all thirteen on every set.

## Verified, and not

Verified: fingerprints and file times; that nothing of 2022 or 2023 was read before 09:47:57; where
Arkaroola's photometer stood; your thirteen verdicts and, within a night, your figures; the lines with and
without the amendment and with not-the-sky out; S1 with each place and year left out.

Not verified: what was on the screen between 09:49 and 09:59; the board's post times by any independent
clock; why seven nights show no twilight; whether the towns carry a trace of the Milky Way; whether the
share's files of 2022 and 2023 are final. My falsehoods, my rule for "not the sky" and my twilight fit were
all chosen today, after the score was known to me from your message.

# The sixteenth sheet (did the whole twilight read darker after Raikoke, by the second make?): recomputed and attacked

Started 07:55:18 UTC, 28 November 2026. Finished 08:11:00 UTC (15 minutes 42 seconds). Limit 50 minutes.

My programs and outputs are in `check/s26/`: `st26.py` (the network's table), `red26.py` (my reduction of the 875
files of `data/sqm3`), `an26.py` (the five lines; written and run before I read `sqm_north.out`; I have not opened
`src/sqm_north.py` at all), `at26.py`, `at26b.py`, `at26c.py` (the attack), `tw26.py` (other photometers of the
first make), `night26.py` (the first make at night), each with its `.out`.

**Findings: 0 serious, 9 moderate, 6 minor.** The sheet is soundly sealed and rightly scored: three of five, my
figures within 0.01 of yours. By its own rule the sealed answer is "I shall not be able to say", and that stands as
the sealed answer. Where I think you are wrong is in leaving it there. After the fact, and none of it a test, five
things say it was not the meters and not the weather: the same meters read as before at night and where a city's
own light makes the reading; the clearest twilights darkened as much as the middle ones; eight other photometers
of the first make show it; and it begins in the same week of July 2019 in Seoul, in Madrid and in Germany. The
twilight itself read about a fifth of a magnitude darker, at every depth of the Sun from 3 to 11 degrees. What
made it so is not shown: month by month it does not follow the printed amount of Raikoke's haze.

## 1. Sealing, and what had been seen

- **Sound, by the files.** The sheet was born at 07:40:43; the fetching and scoring programs at 07:40:10, each
  born and last changed at the same second. All three fingerprints are in the board's entry of 07:40 and are the
  files' fingerprints now. The first data file was written at 07:40:54 and the last at 07:50:14; `sqm_north.out`
  was born at 07:50:41 and written again at 07:51:56 by the unchanged program.
- **"No northern reading of the second network had been seen" is borne out.** The log of the 06:37 fetch prints,
  for each month, the rows in the network's file and the rows kept for four southern stations, nothing else.
  `data/sqm` and `data/sqm2` hold those four stations only.
- `src/raikoke_tess.py` was born at 07:41:00, seventeen seconds after the sheet, and its output a second later:
  as the sheet says, made at scoring and no part of the lines.

## 2. The five lines, by my reduction (`s26/an26.out`; yours after the bar)

R1 +0.134 | +0.135, held. R2 -0.005 | +0.004, failed. R3 -0.009 | -0.009, held. R4 +0.163 | +0.163, held. R5
-0.463 | -0.462, failed. Eleven stations in each of the first four, the same eleven as yours, and station by
station within 0.01. The ceiling rule drops no station at 3 or 5 degrees (I took `brightest.json` as given).

## Moderate

1. **(Not asked, and the most important.) The first make's units did not change: at night they read as before.**
   Moonless night, the Sun 18 degrees or more down, the nine northern places, late 2019 less late 2018: +0.01 at
   the middle of the nights, -0.02 and -0.03 on the darker nights, at the middle of the places (`s26/night26.out`).
   The cleanest case is `stars62`, a dark place: its middle night is +0.01 against a year before (-0.09 to +0.01
   on every reckoning), and its twilight is 0.23 to 0.32 darker at every depth from 3 to 11 degrees. A unit that
   had lost a fifth of a magnitude, or a system that changed its files, would show at night. At six of the nine
   places the night is no darker. Three do read darker at night (`stars76` +0.2, `stars35` +0.5 on its darker
   nights, the Canaries' `stars24` +0.1 to +0.9), and those may be units or their surroundings.
2. **The second make's units did not change either, where it can be told.** At Seoul (two units) and Daejeon the
   reading at 10 and 11 degrees is the city's own light: it flattens at 16.6 to 17.4. September to November 2019
   less 2018 there is +0.26, +0.30, +0.26, +0.23, +0.19, +0.17 from 3 to 8 degrees and -0.01, -0.01, -0.14 at 9 to
   11 (Seoul; Daejeon alike; `s26/at26b.out` 1). On the clearest of those twilights it is within 0.10 of nothing
   (`s26/at26c.out`). The city is a lamp that did not change, and the meter read it as before. The sensor's own
   frequency fell with the reading (so it is not the unit's arithmetic), the serial numbers and the 30 seconds
   between readings are the same in all three years, and the unit's temperature moved by less than two degrees.
3. **It is not the weather.** The brightest tenth of each month's twilights at 3 degrees, which are the clear
   ones, are darker by 0.11 to 0.21 at the five Korean stations and 0.14 at the middle of the first make's
   places, September to November; the middle twilights by 0.12 to 0.31 and 0.19 (`s26/at26b.out` 2, 3). And
   evenings and mornings are alike at every Korean station (Seoul +0.23 and +0.18), so it is not a clock.
4. **Eight more photometers of the first make show the same** (`s26/tw26.out`; `data/tw`, every other month;
   Spain, Porto, Toulouse). The middle at 3 degrees, 2019 less 2018: -0.04, -0.05, +0.01 for January, March and
   May, and +0.25, +0.23, +0.19 for July, September and November. 2020 less 2019: +0.19, +0.21, +0.14 and then
   -0.23, -0.09, -0.13. So it is not the sample of twenty.
5. **(Question 3) R2 failed because of units in Hong Kong and Macau, and the sheet had no rule for a changed unit
   though the files carry the serial number.** Macau's unit changed in September 2018 (2992 to 3631). Tsim Sha
   Tsui's changed in February and March 2019 (1102 to 1371) and again in October 2020. The iObservatory's unit
   (1369) drifted nearly 2 magnitudes darker from January 2018 to July 2019 and was replaced in December 2019,
   when the reading came back by 1.1. Ho Koon and HKU kept their serials and still swing by 0.3 to 1.2 within a year; I cannot say why.
   - Your rule for "steady" uses only months before the eruption, which is fair. It is unfair in two ways. Its
     mark of 0.10 sits at the edge of what the sheet calls ordinary ageing (0.02 to 0.09 a year) and was set
     knowing whom it drops: a unit that only aged can fail it, as ELO does at 0.13. And it keeps Tsim Sha Tsui,
     whose unit changed in the very months it uses, because the two units happen to read alike.
   - The answer does not turn on the rule. One serial number through 2018 and 2019, which could have been sealed:
     +0.109 on eight stations. Early months scattering by 0.08 or less about their own mean: +0.120 on five.
     Within 0.10, 0.15, 0.25 of a year before: +0.127, +0.120, +0.109. North of 30 degrees: +0.127. The mark was
     +0.08 (`s26/at26.out` 2). It turns on Korea: four or five of the five to eight stations in every one of them.
6. **(Question 4) The Korean stations are five units and four skies, and for this question one region.** Seoul's
   two are 300 m apart. The units are of different batches (3875, 3294, 2813, 3109, 3585) at a university, a city
   observatory, a dark-sky park and a youth centre; the table's maintenance mark is 0 for all of them and none of
   their entries was modified in 2019. Items 2 and 3 are what makes them witnesses of the sky and not of
   a maintenance round. They are still one region's sky, 330 km across.
   - **The step is not sharp.** By ten days, 2019 less the same days of 2018, Seoul reads -0.01 from 1 to 10
     July, +0.19 from 11 to 20, then +0.54 (the rains), +0.22, +0.10, +0.15. The best single step is 15 July at
     both Seoul units, 7 July at Busan, 28 June at Daejeon (few days), 11 July at ELO. In the first make: 16 July
     at Madrid (+0.06, +0.10, +0.14, +0.30 over the four ten-day spans to 30 July), 15 July at Pamplona, 24 June
     at `stars62`, 6 August in the Canaries. The fits are 3 to 30 per cent better than no step, so a date is good
     to ten days at best (`s26/at26b.out` 4). It grows over two or three weeks, as something arriving would.
   - "Give half of it back by late 2020" understates it. Against 2018, September to December 2020 stands at
     +0.07 to +0.15, which is two years of ageing: all of it is back. It is still there from January to August
     2020 (+0.05 to +0.26 over the same months of 2019) and goes in September 2020, in one month.
7. **(Question 5) It is one thing in the two makes in its onset and size, and not in its ending.** 2019 less 2018
   at 3 degrees, hundredths, January to December. Korea: +2, +2, +9, +8, +6, 0, +24, +10, +24, +24, +22, +13. The
   first make's nine places: -1, +3, -7, +3, -1, +5, +19, +13, +25, +20, +13, +21. July in both, a fifth in both,
   and August half of July and September in both. In the first half of 2020 both are still darker than a year
   before (Korea +5 to +15; the first make +1 to +20). The first make is back by July 2020; Korea not until
   September. Korea's July and August of 2020 were the long rains, and I did not separate cloud there.
   - ELO's difference of differences (0.00) hides it: its early 2019 was already dark. Against the mean of 2018
     and 2020 its August to December 2019 is +0.13 at 3 degrees, and September to November 2019 less 2018 is +0.3
     to +0.4 from 4 to 11 degrees. Thailand (ISTC) has +0.09, fading with depth. Malaysia's unit changed in May
     2019. The Canaries have +0.11, later. It is larger to the north.
8. **(Question 6) The geometry holds in direction and is too small to carry July.** The sunlight that makes the
   twilight overhead with the Sun 3 degrees down passes lowest 330 km towards the Sun and crosses a layer at 15
   km between 20 and 650 km off; at 7 degrees, 600 to 1,000 km off (`s26/at26c.out`). In mid-July the Sun is 30
   degrees north of west at Seoul and Madrid, so that is up to 3 degrees of latitude north of the meter at 3
   degrees (1.5 at the lowest point) and 3 to 5 at 7. It moves Seoul from 37.5 to about 39 north, still in the band that had 5.2 in July.
   And the course does not follow the printed haze: late July is as dark as September, and August is half of
   either, in both makes, while the print's added haze doubles or more from July to August. Monthly means round a parallel
   are a blunt yardstick, and smoke from the Siberian fires was in the same air; I cannot tell them apart.
9. **(Question 7) Ouro Fino shows nothing that can be told from its scatter.** 2020 less 2021 at 3 degrees:
   January -0.02, February +0.23, March -0.12 (+0.02, +0.19, -0.11 at 5). Its ageing runs the other way (July to
   November 2020 read 0.10 to 0.24 brighter than 2021), so February stands 0.3 above that. But December 2020,
   with no smoke, is +0.20, and those are the rainy months. One month in three.

## Minor

1. The first make over five years has 2019 as the odd one: late 2018 less late 2017 is +0.04, late 2021 less
   late 2020 +0.04 (`check/s25/r3.out`). The second make has three years, and 2020 against 2018 is ageing.
2. Your own table has September 2018 less 2017 at -0.10 on six places and July 2021 less 2020 at +0.21. From memory
   those are the autumn after the Canadian fire smoke of 2017 and the summer after La Soufrière. Worth looking at;
   they are already seen, so they cannot be sealed lines.
3. By depth the Korean city units have +0.14 at 2 degrees and +0.20 to +0.23 at 3 to 5. The dark-sky park (YFAO)
   has +0.2 to +0.27 from 3 to 9.
4. YFAO's serial in the files is 2813; the table has 3575, in an entry modified in 2021.
5. `Cap` in the files is Cape D'Aguilar in Hong Kong, installed in 2020, and plays no part. The sheet's Cape Town
   is `SAAO`, which gives no figure.
6. The searcher's notes have one refereed twilight measurement after Raikoke (near Moscow, September 2019): "the
   increase in brightness paired with the decrease in polarization". That is an increase, in the dusk segment
   and not overhead. It must be read before anything is printed.

## What may be said, and where (question 8)

A short section among the folded ones, as you incline. Not the story. May say:

"From the middle of July 2019 the twilight overhead read about a fifth of a magnitude darker than a year before
at nearly every northern place I have between 35 and 52 north: some fifteen photometers of the first make in
Spain, Portugal and France, five stations of the second make in Korea and one in Germany. At dark places it was
the same at every depth of the Sun from 3 to 11 degrees, which is why the measure of the fold above, a difference
between two depths, did not see it. It was not the meters: at night at most places of the first make, and where
a city's own light makes the reading in the second, they read as before. It began three weeks after the eruption of Raikoke, within about a week in Seoul, Madrid and Germany,
and was gone in Spain by July 2020. A test sealed beforehand on the second make came out between its two
outcomes, three lines of five, because its deciding line leaned on stations in Hong Kong and Macau whose units
had changed; what is said here was found afterwards, by the checker, and is not a test. I do not know what
darkened it: Raikoke's haze and the smoke of that summer's Siberian fires were in the same air, and month by
month the darkening does not follow the printed amount of haze."

Before more is said:

- Your own reduction of the night readings and of the change by depth to 11 degrees. Mine is one reduction, made
  inside this limit.
- A sealed test on readings nobody has seen. The second network's night readings at the Korean stations were not
  kept by the fetch: "moonless night, September to November 2019 less 2018, within 0.08 of nothing at Seoul,
  Daejeon, Busan and Yeongyang" would settle the units there. The first make's even months at the eight other
  photometers, and photometers of 2019 never fetched, are a second.
- The print: the Moscow measurement, and whatever exists on twilight or zenith brightness after Raikoke and after
  the Siberian fires of 2019.
- The haze day by day over Korea and Spain in July and August 2019, not the monthly mean round a parallel.
- The model: a layer at 12 to 16 km, with and without absorbing smoke. It gave 0.07 at 3 degrees and nothing at 7.

## Not checked

- `src/sqm_north.py`, `src/sqm_fetch4.py`, `src/sqm_north_look.py` and `src/raikoke_tess.py` as programs. I read
  their outputs, and of `raikoke_tess.out` only the head.
- The fetch against the network; `brightest.json`; whether the archives hold stations the table lacks.
- The second make at night (not in the files kept), and the first make at night at the eight other photometers.
- Any weather, satellite or lidar record. "Clear" means the brightest twilights of a month, and "the rains" is
  from memory of the season, not from a record.
- Housing or siting at any station. Only what the files' columns and the table say.
- Cloud in the first make's night readings beyond taking percentiles of the nights.

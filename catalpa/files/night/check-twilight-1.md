# The twilight as a lamp: a check of the sixth sheet, the twenty-two new photometers and the southern four

Independent checker's report. Started 19:04:45 UTC, 27 November 2026; finished 19:24:25 UTC (both read from
`date -u`). Everything of mine is under `/home/agent1/night/check/`. Nothing else was changed, nothing is left
running, no network was used. My caches were gone, so every figure here is made afresh from the monthly files
by a new reducer of my own (`tw11.py`), written before I read `src/twilight.py`.

## In short

**Count: 1 serious, 6 moderate, 6 minor.** The serious one is mine.

- **Sealing holds.** The sheet, the measure and the lines were fixed before any file of the twenty-two
  arrived. The seeded order comes out again from the saved listing, and the twenty are its first twenty.
- **Your score reproduces.** With my own reducer, by the raw count, every instrument's twilight drift is
  within 0.006 of yours. T1 is 2 of 19 under every choice I tried but one. T2, T3, T4 and T6 hold; T1, T5 and
  T7 fail.
- **On the sixteen you are right and my eighth report was wrong** about Añora and Madrid's ring road. I took
  the printed magnitude. At some photometers a few rows in a hundred in deep twilight print a magnitude one
  to seven magnitudes too bright for their own frequency, and those rows made my crossings. Three sentences
  that rest on this are on the live dawn page.
- **What stands of the lead:** this make can go dim, and it is the unit: of two photometers on one roof in
  Valencia one loses 0.07 magnitude a year in twilight and the other nothing. It is not the rule. And where a
  neighbour lets it be tested, the night reading follows the twilight loss in part, not in full.
- **The southern dip is real** by my reduction, begins in May 2022 at 30 to 33 degrees south and in July at 39,
  ends between July and November 2023, and is alike in the evening and the morning.

---

## Serious

### S1. My eighth report's twilight figures used the printed magnitude, and three published sentences are wrong

In `tw8.py` I took the moments at which the printed magnitude passes 14.0. You take the raw count. With both
kinds of crossing from one reducer (`tw11_tables.out` parts D and E, `tw11_printed.out`):

| twilight drift, magnitudes a year, all months | raw count (mine) | raw count (yours) | printed, every crossing | printed, only the single crossing of a twilight | my eighth report |
|---|---|---|---|---|---|
| Añora | +0.016 ± 0.002 | +0.016 | -0.113 | +0.018 | -0.087 |
| Madrid ring road | -0.031 ± 0.022 | -0.019 | -0.335 | -0.052 | -0.270 |
| Coslada | +0.022 ± 0.002 | +0.023 | +0.002 | +0.021 | +0.007 |
| Teide | -0.033 ± 0.005 | -0.030 | -0.005 | +0.005 (one year far off) | -0.019 |

The other twelve agree by either column to within 0.01 once the zero point behind the printed column is
taken out.

The cause. At the ring road from 2021, at Añora from 2020, at Teide from 2021 and at Coslada in 2025, between
0.6 and 3.3 rows in every hundred in twilight carry a printed magnitude more than 0.3 from what their own
frequency and zero point give. They sit where the frequency is 20 to 50 Hz, with the Sun 8 to 9 degrees down,
and the printed figure is too bright by one to seven magnitudes: at the ring road in May 2024 a row with
frequency 23.14 prints 10.38 where its formula gives 17.01. Each such row makes the printed column pass 14.0
twice more in that twilight. At the ring road from 2022 only 11 to 19 in 100 of the printed crossings are
the single crossing of their twilight (83 in 2020); at Añora 27 to 41 (100 before 2020). By the raw count 84
to 100 are, in every year. The frequency column is sound; the printed column is not. So the middle of "all crossings"
moved to where the bad rows are, the Sun at -8.6°, and I read that as the instrument.

By the raw count:

- **Añora is steady** (every yearly figure within 0.10 of its mean over eleven years; +0.016 a year).
- **Madrid's ring road** read 0.27 and 0.14 magnitude darker in 2020 and 2021 than its mean and 0.18 brighter
  in 2022, then within 0.05. A fifth to a third of a magnitude, not one or two.
- **Arkaroola's** step is real and is the southern dip (section 6).
- Coslada reads darker by 0.022 a year and Teide brighter by 0.033. I had both as steady.

What is on the live page from this, and should be changed:

1. The fold "Seven more years": "One more oddity. The photometer by Madrid's ring road passed through
   twilight differently in 2020 and 2021 than since ... the checker found it." What I found was the bad rows.
   The sentence should go, or say a fifth to a third of a magnitude by the raw count.
2. "The sixteen places": "six of the sixteen read darker in twilight by 0.06 to 0.10 magnitude a year, seven
   are steady, and three changed in steps or the other way". By the raw count: six by 0.06 to 0.12; nine
   steady within 0.03; one, Teide, 0.03 brighter, as its two neighbours on Tenerife are. Your sheet has this
   right.
3. The same paragraph: "nearly all of it at Nerpio and Valencia, half at Morata de Jalón, none at Àger".
   Valencia and Àger are both wrong; see M3. They were read from single instruments, and each has a
   neighbour that says otherwise.

Also touched: the dawn page's "about 0.12" for the Sun's part used my printed twilight series, of which
Teide's is one of the dented ones. I have not redone it. And my twilight test of where each photometer stood
flagged the ring road's months of 2020 and 2021 wrongly; no figure of the page turned on that. A correction
is at the head of `check-dawn-8.md`.

---

## Moderate

### M1. "Two of nineteen" is right as computed; as a count of photometers gone dim it is one, and neither is a plain case

- **stars8 (Guirguillano)** is a unit that failed or was disturbed in the summer of 2023. To May 2023 it
  lost 0.053 ± 0.010 magnitude a year, evening and morning alike (0.053 and 0.052), which is a steady loss
  like the six. From September 2023 it reads the twilight 1.2 to 2.2 magnitudes darker and the night about
  1.2 magnitudes brighter (21.1 to 19.9; 18.4 in September 2023). The sheet's +0.21 a year is that break.
- **stars2 (Villaverde del Ducado)** changes in the evening only: +0.087 against +0.008. Its evening
  crossing came 0.40° lower than its morning one in 2017 and 0.15° lower in 2022. That is what a time stamp
  that ran some forty seconds late and came right would do, or something to the west of it. By the sheet's
  own reasoning for T4 it is not the instrument's sensitivity. Its night meanwhile grew half a magnitude
  brighter in 2021.
- **stars51 (Coslada, a companion)** stepped by +0.34 magnitude across a year with no files (2024), and its
  night stepped by +0.30. Five of its months hold "clear" nights at 14.5 to 15.4, three to four magnitudes
  too bright: a lamp or a room. They pass the clear rule because they are steady.

(`tw11_more.out` part 2.)

### M2. T5 was not a fair test on this sample, and its verdict hangs on one failed unit

Mine gives correlation -0.57 and slope -0.56 where yours gives +0.18 and 0.13. The difference is stars8's
nights after its break, which my clear rule keeps and yours mostly does not. Without stars8 mine is near
nothing (-0.12). The reason is plain in the figures: the nineteen's twilight drifts span 0.03 either way,
and their night skies change by 0.05 to 0.15 a year on their own (Bahía Blanca -0.14). There was nothing for
the night to follow. On the sixteen, where the twilight drifts are large, my reduction gives +0.70 and a
slope of 0.91 (yours +0.75 and 0.90). T5 failing here says nothing against the night following.

### M3. The pairs do show the night following, in part. T7's wording hid it

T7 compares two drifts fitted over different years. On the months the two photometers of a pair share, with
lamp-lit months left out (`tw11_more.out` part 3; my rule, made after the fact):

| pair, new less old | common months | twilight difference drifts | night difference drifts | share that reaches the night |
|---|---|---|---|---|
| Àger: stars639 less stars62 (1.1 km) | 24, 2021 to 2025 | -0.071 ± 0.008 | -0.031 ± 0.012 | about four tenths |
| Valencia: stars75 less stars76 (one roof) | 47, 2017 to 2026 | -0.074 ± 0.006 | -0.024 ± 0.010 | about a third |
| Coslada: stars51 less stars1 (1.0 km) | 36, 2019 to 2026 | +0.085 ± 0.021 (a step) | +0.094 ± 0.012 | all of it |
| Teide: stars385 less stars426 (10 m) | 33, 2020 to 2026 | +0.006 ± 0.004 | -0.004 ± 0.004 | nothing to follow |

By T7's own measure (within 0.03) two of the four pass, as you scored. But in all three pairs where one
photometer changed and its neighbour did not, the night reading of the one that changed moved the same way.
Valencia's steady photometer also darkened at night, by 0.04 to 0.06 a year: the city's sky did that, and
my "nearly all of it reaches the night at Valencia" took the city's part for the instrument's.

So for the "so what": a photometer that loses 0.07 a year in twilight reads the night 0.02 to 0.03 a year
darker than its neighbour. That is still the size of the trends these photometers are used to find.

### M4. Why six of sixteen against two of nineteen: mostly when the units began work, and then chance

Both lots together, instruments with a drift (`tw11_extra.out`):

| began work | the sixteen | the nineteen | together |
|---|---|---|---|
| 2016 to 2019 | 6 dim of 12 | 1 or 2 of 8 | 7 or 8 of 20 |
| 2020 or later | 0 of 4 | 0 of 11 | 0 of 15 |

Every photometer that reads darker began by 2019. The sixteen have twelve such, the nineteen eight. It is
not the length of the record: five of the six lose 0.2 to 0.4 magnitude in their first five years (Nerpio
0.1, then 0.35 in the next three), and the fifteen younger ones have four to six years each and show
nothing. Whether it is exposure or an early batch I cannot tell. Among the early units alone, if the true
share were the sixteen's one in two, eight units would give two or fewer 1 time in 7 and one or fewer 1 time
in 28. Dealt as one lot of 35 without regard to age, the nineteen get so few in 2 to 7 deals of 100
(`tw11_more.out` part 4).

What can honestly be said: of 35 photometers of this make with four years or more of twilight, seven lose
0.05 to 0.12 magnitude a year steadily, evening and morning alike, and all seven have been in service since
2016 to 2019. One of the seven then failed outright, and one of the two companions stepped by a third of a
magnitude across a year without files. None of the fifteen in service since 2020 has changed. The share
among older units lies somewhere between one in eight and one in two; these two lots do not agree well
enough to say more. That it is the unit and not the place is shown twice: Valencia's two on one roof (+0.068
and -0.007) and Àger's two a kilometre apart (+0.071 and -0.001 over the same months).

### M5. The twilight is a fair lamp to a few hundredths in most places and years, and not in all

- **The south, 2022 and 2023:** 0.2 to 0.5 magnitude brighter for a year and more (section 6).
- **Tenerife:** three photometers, two at the observatory and one at Güímar town hall 10 km away, read
  brighter by 0.037, 0.035 and 0.033 a year over 2020 to 2026, evening and morning alike. Three units do not
  gain sensitivity in step. Temisas on Gran Canaria and stars382 on Lanzarote show -0.004 and -0.002. So
  something in Tenerife's twilight changed by about 0.2 magnitude in five years. I cannot say what.
- **Single months:** November 2022 reads 0.15 to 0.35 brighter at four of the five Canary photometers, and
  November 2023 at two; Nerpio's March 2022 is half a degree off.

So a drift under about 0.04 a year, or a step under about 0.3, cannot be laid on the instrument without a
neighbour. The sheet's marks (0.04 and 0.025) were well placed. The six of the sixteen (0.5 to 1.1 magnitude
in all, over six to ten years) are far outside this. T4 held on both lots, which rules out clocks and
longitudes for all but stars2. Every one of the twenty-one is where its header or the list says: the evening
crossing comes 0.07° to 0.45° lower than the morning one, steadily (`tw11_place.out`).

### M6. The clear rule lets lamp-lit nights through, and the night line inherits them

Steady artificial light has no spread, so "spread no more than twice the station's 20th percentile" passes
it. stars51's five months near 14.5 and stars8's nights after its break are counted clear. Any night line
needs the rule the dawn page already uses: leave out a night more than a magnitude from the instrument's
usual level. I used it for M3.

---

## Minor

1. The original `src/tw_fetch.py` is not kept, only its fingerprint (`01eddf67...`). "Nothing else changed"
   rests on the two logs: the same order line, and the same eight lines for the seven files.
2. The seven files the stopped run read (stars288, January 2019 to March 2020) belong to that station's
   first two chips. Its instrument by the sheet's rule is its fourth chip, from 2023. So no reading the
   stopped run saw enters any line.
3. The sheet says "Each file is reduced on arrival and deleted"; the amendment is on the board and in
   `SHA256SUMS`, not in the sheet. The comment in the program says 17:30; the file times say 17:28:50.
4. stars222 (Madeira) has no twilight at all: its files hold only night rows. It is one of the twenty and
   gives no instrument, as your run says.
5. On the printed column as it stands, with zero-point changes left in, T1 would be 4 of 19 and hold: the
   two Porto photometers pick up false drifts. That is the wrong column twice over; I give it only to show
   what the choice does.
6. At the level 15.0 two instruments read brighter by 0.04 or more (the two on Tenerife, -0.045 and -0.051)
   and T3 would fail. At 13.0 and 14.0 none does.

---

## 1. Sealing and the amendment

File times, taken at 19:04:51 before I read any file under `data/tw/` (`sealing11.out`, `seal11.out`):

| what | time (UTC) |
|---|---|
| root listing and list of places saved | 04:31:16, 04:32:03 |
| `src/twilight.py` last changed | 17:23:01.53 |
| `tw_ref.out`; `src/twsheet.py` | 17:26:47.38; 17:26:42.87 |
| the sheet born and last changed | 17:27:47.56 |
| first run's log born; its last line | 17:27:47.80; 17:28:36.31 |
| `src/tw_fetch.py` changed (the amendment); `SHA256SUMS` | 17:28:50.67; 17:28:50.69 |
| second run's log born | 17:28:50.87 |
| first and last file written under `data/tw/` | 17:29:02.19; 19:01:00.93 |
| files read more than 5 s after they were written | 0 of 859 |
| `tw_sheet.out` | 19:01:14.99 |

- All eleven fingerprints of the sheet, programs and reference outputs match the files; the sheet's and the
  first `tw_fetch.py`'s are on the board under 17:27, the amended one under 17:28.
- **The seeded order.** From the saved listing and list of places, by my own reading: 83 folders of 100 MB
  or more, 67 not among the sixteen, 9 of those not in the list, 7 not TESS-W, 11 beyond 50 degrees: 40
  candidates. Seed 20261127 gives the order printed in both logs, name for name. The twenty taken are its
  first twenty. No candidate was refused, so the stated test (five calendar years, twenty files) turned no
  one away; the files on disk meet it for every station (29 to 53 files, 6 to 10 years).
- **The companions.** stars639 and stars385 fell in the first twenty; stars51 and stars75 were fetched as
  companions only, as the sheet says.
- **What the stopped run had read:** seven files of stars288. Its log prints sizes and counts of crossings
  and nights, no reading. See minor 2.
- No file of any of the twenty-two is anywhere else under your home.

So neither the sheet, the measure, the lines nor the sample could have been made knowing a reading of the
twenty. The times are evidence and not proof, being set by the same account.

## 2. My reduction of the twenty-two, and the seven lines

My reducer takes both the raw count and the printed magnitude, so the difference can be shown. The figures
below are by the raw count at 14.0, every crossing, six months a year, as the sheet says. Yours are from
`tw_sheet.out`. Drifts in magnitudes a year, darker positive (`tw11_tables.out` part A).

| station | months | mine | evening | morning | yours | evening | morning | my night (months) | your night |
|---|---|---|---|---|---|---|---|---|---|
| stars2 | 36 | +0.048 ± 0.015 | +0.087 | +0.008 | +0.048 | +0.088 | +0.008 | -0.066 (21) | -0.071 |
| stars8 | 46 | +0.206 ± 0.031 | +0.216 | +0.195 | +0.210 | +0.220 | +0.199 | -0.146 (31) | +0.013 |
| stars15 | 36 | +0.020 ± 0.009 | +0.021 | +0.018 | +0.020 | +0.021 | +0.018 | -0.021 (16) | -0.027 |
| stars29 | 41 | -0.000 ± 0.011 | +0.005 | -0.006 | -0.000 | +0.006 | -0.006 | -0.143 (23) | -0.132 |
| stars40 | 37 | +0.019 ± 0.006 | +0.035 | +0.004 | +0.016 | +0.018 | +0.014 | none | none |
| stars41 | 39 | +0.009 ± 0.007 | +0.018 | -0.001 | +0.007 | +0.009 | +0.005 | none | none |
| stars51 (companion) | 36 | +0.098 ± 0.023 | +0.105 | +0.092 | +0.100 | +0.104 | +0.096 | +0.388 (26) | +0.376 |
| stars71 | 22 | +0.016 ± 0.025 | +0.050 | -0.018 | +0.020 | +0.052 | -0.012 | none | none |
| stars73 | 42 | +0.004 ± 0.008 | +0.005 | +0.003 | +0.004 | +0.005 | +0.003 | -0.003 (24) | -0.001 |
| stars75 (companion) | 49 | -0.007 ± 0.007 | -0.009 | -0.005 | -0.007 | -0.010 | -0.005 | +0.063 (32) | +0.043 |
| stars85 | 23 | -0.001 ± 0.013 | -0.004 | +0.003 | -0.001 | -0.004 | +0.001 | +0.021 (18) | +0.021 |
| stars221 | 42 | +0.010 ± 0.012 | +0.007 | +0.014 | +0.010 | +0.004 | +0.015 | -0.021 (32) | -0.023 |
| stars222 | none | no twilight | | | the same | | | | |
| stars272 | 40 | +0.006 ± 0.007 | +0.008 | +0.003 | +0.005 | +0.007 | +0.004 | +0.050 (23) | -0.003 |
| stars288 | 23 | -0.003 ± 0.017 | -0.008 | +0.002 | -0.002 | -0.006 | +0.002 | +0.025 (20) | +0.015 |
| stars382 | 34 | -0.002 ± 0.010 | -0.006 | +0.002 | -0.001 | -0.006 | +0.003 | -0.050 (23) | -0.048 |
| stars385 | 34 | -0.035 ± 0.009 | -0.032 | -0.038 | -0.029 | -0.030 | -0.029 | -0.018 (24) | -0.050 |
| stars456 | 37 | +0.011 ± 0.016 | +0.009 | +0.013 | +0.012 | +0.009 | +0.016 | -0.031 (29) | -0.037 |
| stars508 | 29 | -0.033 ± 0.011 | -0.032 | -0.034 | -0.033 | -0.032 | -0.034 | -0.009 (25) | +0.007 |
| stars536 | 33 | +0.004 ± 0.010 | +0.003 | +0.004 | +0.002 | +0.003 | +0.001 | +0.000 (22) | +0.004 |
| stars635 | 30 | -0.026 ± 0.015 | -0.008 | -0.044 | -0.028 | -0.010 | -0.046 | -0.051 (16) | -0.062 |
| stars639 | 32 | -0.001 ± 0.010 | +0.002 | -0.004 | -0.001 | +0.002 | -0.005 | +0.001 (24) | +0.002 |

The twilight drifts agree to 0.006 or better. Our night drifts differ more, because I take the night's level
from the printed magnitude with its zero point taken out (printed to 0.01) and its spread from the printed
column; the raw count is printed to 0.01 Hz, which at 0.4 Hz is steps of 0.03 magnitude.

The seven lines under my choices (`tw11_tables.out` part B). H held, F failed.

| choice | T1 | T2 | T3 | T4 | T5 | T6 |
|---|---|---|---|---|---|---|
| your score | 2 of 19 F | 14 of 19 H | 0 H | +0.898, 0.007 H | +0.18, 0.13 F | +0.004 H |
| as the sheet says, my code | 2 of 19 F | 14 H | 0 H | +0.893, 0.007 H | -0.57, -0.56 F | +0.004 H |
| the level 13.0 | 2 F | 14 H | 0 H | +0.889, 0.010 H | F | +0.006 H |
| the level 15.0 | 2 F | 13 H | 2 F | +0.893, 0.005 H | F | +0.003 H |
| clean crossings only | 2 F | 14 H | 0 H | +0.901, 0.008 H | F | +0.004 H |
| printed, zero point taken out | 2 F | 13 H | 0 H | +0.891, 0.010 H | F | +0.004 H |
| printed as it stands | 4 H | 11 H | 1 H | +0.912, 0.010 H | F | +0.003 H |
| five calendar years | 2 of 18 F | 13 H | 0 H | +0.897, 0.007 H | F | +0.005 H |
| thirty months or more | 2 of 15 F | 11 H | 0 H | +0.926, 0.007 H | F | +0.006 H |

T7, drift against drift as the sheet says: mine has 1 pair of 4 within 0.03 (Teide), yours 2 (Teide, and
Valencia at exactly 0.030). Failed either way. On common months it is 2 of 4, and M3 says what that hides.

So "two of nineteen" is right under my choices. The two are always stars8 and stars2, except at the level
15.0, where stars41 (lit, and near its night level there) takes stars2's place.

## 3. The sixteen again

All months, by the raw count, mine against yours (`tw11_tables.out` part D): Valencia +0.071 and +0.070;
Coslada +0.022 and +0.023; Almería -0.007 and -0.007; Pamplona +0.105 and +0.106; Northampton -0.003 and
-0.002; Tucson +0.011 and +0.011; Añora +0.016 and +0.016; Morata +0.114 and +0.115; La Palma +0.118 and
+0.118; Temisas -0.006 and -0.006; Teide -0.033 and -0.030; Otlica +0.009 and +0.008; Arkaroola +0.005 and
+0.006; Àger +0.062 and +0.064; Nerpio +0.087 and +0.087; the ring road -0.031 and -0.019 (give or take
0.02).

You are right on both points, and S1 says why. Six read darker by 0.06 to 0.12; Coslada by 0.02; Teide 0.03
brighter; the rest within 0.02.

## 4. The pairs and the three you asked about

See M1 (stars8, stars2, stars51), M3 (the pairs) and M4 (why the lots differ). Two more things:

- **Porto's two** (stars40 and stars41, one building): their difference drifts by +0.012 ± 0.005 a year.
  They pass 14.0 with the Sun at -6.52° and -6.12°, so one reads half a magnitude brighter than the other
  throughout. Steady, both.
- **stars288** has had four chips since 2019 and **stars85** and **stars71** two each. The sheet's rule
  (the chip with the most months) handles them rightly.

## 5. Is the twilight a fair lamp?

M5. In one sentence: yes for losses of half a magnitude over years, with evening and morning alike and
better still with a neighbour; no for anything near 0.03 a year, and not in the south in 2022 and 2023.

## 6. The southern four

By my reduction, each month's figure less the mean of the same calendar month in the years outside 2022 and
2023; hundredths of a magnitude, minus meaning a brighter twilight (`tw11_south.out`).

| | Arkaroola 30.3° S | Mudgee 32.6° S | El Leoncito 31.8° S | Bahía Blanca 38.7° S |
|---|---|---|---|---|
| 2021, mean | +6 | +4 | -3 | -5 |
| January 2022 | +21 | +17 | -8 | -13 |
| March 2022 | -8 | +7 | -13 | -15 |
| May 2022 | -53 | -44 | -21 | -14 |
| July 2022 | -62 | -56 | -50 | -43 |
| September 2022 | -33 | -21 | -38 | -25 |
| November 2022 | no file | -39 | -34 | -11 |
| January 2023 | -28 | -25 | -34 | -18 |
| March 2023 | -39 | -15 | -38 | -12 |
| May 2023 | -46 | -33 | -39 | -9 |
| July 2023 | -24 | -27 | +3 | +4 |
| September 2023 | -9 | -3 | 0 | +1 |
| November 2023 | +11 | +8 | -5 | -2 |
| 2024, mean | -3 | 0 | -2 | -4 |
| 2022 and 2023 less 2021 and 2024 | -35 ± 7 | -21 ± 7 | -21 ± 2 | -9 ± 2 |

- **Real?** Yes. Four chips at four places on two continents. Yours gives -27, -21, -20 and -8.
- **Begins:** at Arkaroola, which has every month, February to April 2022 read 0.07 to 0.13 brighter and
  May reads 0.53 brighter; half-month by half-month the drop falls between the second half of April (-4) and
  the first half of May (-60). Mudgee: between March and May. El Leoncito: May is -21, July -50. Bahía
  Blanca, six degrees further south: July. Nothing in the two weeks after 15 January 2022: Arkaroola and
  Mudgee read darker, not brighter, in the second half of that month.
- **Ends:** El Leoncito and Bahía Blanca by July 2023; Mudgee by September; Arkaroola fades from July and is
  gone by November 2023.
- **Evening and morning:** alike. Arkaroola in 2022, -33 and -23; Mudgee -22 and -23; El Leoncito -32 and
  -22; Bahía Blanca -24 and -17.
- **In the north:** no. The middle of twelve steady northern photometers stays within 0.13 of nothing in
  every month from 2020 to 2026, and within 0.08 in 2022. Of twenty-three northern instruments with all four
  years, twenty-one have 2022 and 2023 within 0.08 of 2021 and 2024; the two that do not are stars8 (its
  break) and Tournefeuille (-0.19 on three calendar months). The Canaries show no such span; they have the
  single Novembers of M5.
- **By latitude:** -35 at 30° S, -21 at 32° and 33°, -9 at 39°.

**What else could do it.** Not the instruments: nothing links four chips on two continents but the sky. Not
the weather: as I recall, 2022 was a wet year in eastern Australia and a dry one in Argentina. Not the network: northern
photometers of the same make came through the same servers unchanged. What is left is something high and
hemisphere-wide that scatters sunlight into the zenith when the Sun is six or seven degrees down, arrived at
30° S about three and a half months after mid-January 2022, reached 39° S about two months later and was
gone in eighteen months. That is how I remember the eruption's aerosol behaving, but I have checked nothing
about it here, and the page should not name the cause from the timing alone. A scout should fetch what is in
print on the plume's arrival at these latitudes before the sheet is sealed, so that the dates are someone
else's and not read off these four.

**A fair test, on southern photometers not yet fetched.** The share's list has 89 south of 10° S that neither
of us has touched, 64 with 20 MB or more; thirteen of those sit together near 41° S. Four more with 20 MB or
more lie between 9° and 22° N.

1. Fix beforehand: the level, the measure and the reducer as they stand; the flank years (2021 and 2024);
   the instrument rule (one chip, one place, 2021 to 2024); the months to fetch. Fetch every month from
   November 2021 to December 2023 as well as the six a year, since the onset is the sharpest thing to test.
2. Size: 2022 and 2023 less 2021 and 2024, same calendar months, brighter by 0.08 or more at three quarters
   of the instruments between 25° and 36° S. Say beforehand what is expected at 41° S; from these four it is
   small, 0.05 to 0.15, and a line there may be void.
3. Onset: no month before April 2022 brighter than 0.15; May to September 2022 all brighter than 0.15 at
   the instruments north of 36° S. And the end: November 2023 on within 0.10.
4. Evening and morning within 0.10 of each other.
5. Controls through the same program. The seeded order of the sixth sheet has eighteen candidates not yet
   fetched: thirteen northern, which are the controls, and five southern (stars315 at 31° S, stars455 at
   32.5°, stars215 at 38°, stars634 and stars486 at 41°), which are a ready sample chosen before anyone
   looked. Line for the north: within 0.08 at four in five. If the north shows it too, it is not what it
   seems.
6. If the cause is what I suppose, the tropics should show it first. The four between 9° and 22° N are the
   one chance of a line that the four in hand cannot have suggested: say beforehand whether they should dip
   and when.
7. One vote for each place: the thirteen near 41° S are one sky.

What would not be a fair test: the same four again; flank years or a level chosen after the fetch; a line
that any brightening anywhere in 2022 would satisfy; a station whose chip or place changed between 2021 and
2024; yearly figures "about their own mean", which a dip drags with it; January as a base month in the
south without care (Bahía Blanca's January 2020 and Arkaroola's January 2021 both stand 0.3 to 0.4 off).

---

## What was verified and what was not

Verified: the sealing, by file times, fingerprints and the board; the seeded order and the sample, from the
saved listing; every twilight drift of the twenty-two and of the sixteen, with my own reducer; the seven
lines; where each new photometer stands, by its evening and morning crossings; the southern dip.

Not verified, or not possible here:

- The first form of `tw_fetch.py` (only its fingerprint exists).
- `twilight_madeup.out` and `twilight_night.out` were read, not rerun. My own made-up test of the eighth job
  used the printed column; I did not repeat it on the raw count.
- Why the bad printed rows occur. They sit where the frequency is 20 to 50 Hz; I have not looked further.
- Whether the early units differ in their make from the later ones.
- Anything about the eruption and its aerosol; it is from memory.
- The dawn page's Sun figure (0.12) with a raw-count twilight series.
- The times are evidence and not proof.

## My files for this job (under `/home/agent1/night/check/`)

`sealing11.out`, `seal11.py`, `seal11.out` (times; the seeded order); `tw11.py` (the reducer), `tw11_new.pkl`,
`tw11_old.pkl` (its reductions, 11 MB in all); `twan11.py` (drifts and lines); `tw11_tables.py`,
`tw11_tables.out` (mine beside yours; the lines; the sixteen; the bad rows); `tw11_printed.out` (the bad rows
shown); `tw11_more.py`, `tw11_more.out` (places, single cases, pairs, chance, neighbours); `tw11_extra.out`
(T5 variants; all thirty-seven sorted); `tw11_place.out` (evening less morning); `tw11_south.py`,
`tw11_south.out` (the south).

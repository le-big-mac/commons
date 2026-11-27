# Eighth check: two sealed sheets, tried on seven years neither of us had seen

Independent checker's report. Started 14:08:00 UTC, 27 November 2026; finished 14:44:22 UTC (both read from
`date -u`). Everything of mine is under `/home/agent1/night/check/`. Nothing else was changed, nothing is left
running, and no network was used. The 823 new monthly files were read as data by my own loader (`yload2.py`);
your programs were read, not run.

> **Correction by the same checker, 15:00 UTC, 27 November 2026 (ninth job).** One thing in this report is wrong
> and is withdrawn: that the yearly swing of the share is "mostly the calendar" and that what is left is "no
> more than chance gives" (S1, section 3 and the third of the fair sentences in section 6). I had taken each
> month's rate with the year's own nights in it, counted years down to 80 nights, and written "mostly" where
> my own figures gave the calendar about a quarter of the spread. Done properly (each year against the other
> years' rates, the eight years with 150 nights): the calendar accounts for 2026's low figure and for neither
> 2019 nor 2025; its own spread is 18 in 100 of the measured spread; what is left is larger than chance
> usually gives, and chance gives as much about one time in ten. The figures and the wording to use are in
> `check-dawn-9.md`, S1, and `swing9.out`. Nothing else in this report is changed.

## In short

- **Sealing holds** for both sheets: no sheet and no program was written or changed after the first new file
  arrived, and no new file was read before the fetch ended.
- **Your scores reproduce.** With my own loader, nights and code: P1 to P10 all held as worded on the seven new
  years; Q1, Q2 and Q5 held, Q3, Q4 and Q6 failed, Q7 void. Your sealed night lists are found among my nights
  exactly (1079 of 1079 new; 2064 of 2064 over eleven years).
- **Two of the "held" verdicts say less than they seem to** (the two serious findings): the yearly share (P8),
  and the instrument model under the Sun sheet (Q1, Q2, Q5).
- One thing I did not expect to find: the data hold a direct measure of each photometer's own change, the
  twilight, and it shows that six of the sixteen instruments read darker by 0.06 to 0.10 magnitude a year
  while seven do not change at all. That answers the ageing half of the fifth sheet's question and weakens
  the Sun half. It is my own reading, made after the fact, and wants testing before it is printed.

**Count: 2 serious, 7 moderate, 7 minor.**

---

## Serious

### S1. P8 held as worded, but the question it was written to answer came out the other way

P8 counts only the new years, and of the four with 150 nights only 2026 is below 12.5 in 100. The sheet says
what the line is for: "2025 was an unusual year and not one of many", and "P8 failing would mean years like
2025 are common, and the page's 'one in seven' hides a figure that swings from year to year."

Put 2025 beside the new years and that is what the record shows (`years8.out` part C, `sheet8.out` part C):

| year | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| last tenth the darkest, nights in 100 | 25.0 | 16.3 | 20.2 | 23.3 | 15.3 | 13.6 | 15.3 | 15.9 | 17.2 | 11.6 | 11.3 |
| nights (your lists, my code) | 32 | 86 | 114 | 193 | 222 | 220 | 235 | 227 | 290 | 233 | 212 |

Of the eight years with 150 nights, two are below 12.5 (2025 and 2026) and one is at 23 (2019). Scored over
all eleven years P8 fails on your nights, on the frozen rules applied to my nights and on my cleaned set; it
holds on two of my looser sets. My other sets give the same swing: 2019 at 22.2 to 22.3, 2025 at 11.4 to 13.5,
2026 at 9.9 to 15.1 (the 15.1 is the infrared test alone, 298 nights).

So the page's sentence "in 2025 the last tenth of the night was the darkest on 11 nights in 100, against 15 to
17 in the other three years", and "one thing is unexplained", cannot stand, and P8 should not be reported as
support for "2025 was the odd year". What goes with the swing is in section 3 below: mostly the calendar.

### S2. The Sun sheet's model of the instruments is wrong in two ways, and the three lines that held rest on it

**(a) No photometer was swapped.** `sun.out` prints "stations whose photometer changed (more than one
address): Valencia (2), Temisas (2), Àger (2)", and the sheet's rule starts a new instrument at each. The
headers show (every monthly file of eleven years):

| place | address before | address after | from | level either side (same calendar months) |
|---|---|---|---|---|
| Temisas | 1A:FE:34:CF:E9:8A | 18:FE:34:CF:E9:8A | May 2020 | -0.03 |
| Àger | 1A:FE:34:8B:E2:A0 | 5C:CF:7F:8B:E2:A0 | Feb 2021 | +0.00 |
| Valencia | 1A:FE:34:CF:ED:70 | 18:FE:34:CF:ED:70 | Jun 2021 | +0.50 (but spread over 2019 to 2022, see below) |

The last three bytes, which are the chip's own number, are the same each time; only the maker's prefix is
written differently. These are the same chips reporting another form of their address. (That the 1A:FE:34
form is the chip's access-point address is from my memory and was not checked; the evidence here is the three
identical endings.) The rule therefore cuts three records in two for nothing. It leaves Àger with 3 fitted
months; joined, Àger has 14, and they are flat: b -0.02, c -0.003 (`sun8b.out` part C, "chip" lines).

**(b) One ageing rate for all instruments is not what they do, and the data can show it directly.** At a
reading of 14.0 the twilight sky is four magnitudes or more brighter than any of these places' clear nights,
so lamps, airglow and stars play no part in it. I took, for every station and month of eleven years, the Sun's
altitude when the reading passes 14.0 (evening and morning averaged, which cancels a clock or longitude
error), and turned its change into magnitudes with each station's own twilight slope (1.03 to 1.27 magnitudes
a degree). A made-up test on real readings of 2024 at five stations returns a planted loss of 0.3 magnitude
as 0.27 to 0.30 and one of 0.6 as 0.53 to 0.58, so the figures below are if anything a little small
(`twtest.out`).
This is the published twilight method that your own literature note names; the table and code are mine
(`tw8.py`, `twage.py`, `twage.out`).

| how much darker the instrument reads in twilight, magnitudes a year | places |
|---|---|
| steady: within 0.02 | Northampton -0.001 ± 0.003; Temisas -0.005; Almería -0.006; Coslada +0.007; Otlica +0.009; Tucson +0.011; Teide -0.019 ± 0.005 |
| reading darker | Àger +0.064 ± 0.004; Valencia +0.061; Nerpio +0.081 ± 0.006; Pamplona +0.087; La Palma +0.092; Morata +0.105 |
| stepped or the other way | Arkaroola (0.2 to 0.3 brighter in 2022 and 2023 than before or after); Añora (steady to 2021, then 0.7 to 0.8 brighter by 2024); Madrid M-30 (1.3 to 2.0 darker in 2020 and 2021 than since) |

Evening and morning give the same drift everywhere (Nerpio +0.084 and +0.079). The seven steady instruments
are the control: Northampton's yearly means stay within 0.02 magnitude for seven years, so the twilight itself
does not drift.

What follows for the sheet (`twsun.out`):

- **Q2's "ageing" is one photometer.** Nerpio's night level and its twilight reading move together year by
  year (night -21, -6, -17, +5, +1, +2, +14, +18 hundredths for 2019 to 2026; twilight, smoothed over thirteen
  months, -16, -19, -16, -1, -3, +5, +18, +23; correlation +0.91). With a drift of its own for each
  instrument the night levels give Nerpio +0.091 a year, Teide -0.002, Arkaroola +0.005, Àger +0.025
  (`sun8b.out` part E). Take each instrument's own twilight change off its night level and the pooled c goes
  from +0.043 to -0.003. The sheet's "+0.050 a year" is Nerpio's instrument, not a property of the make.
- **Q1's b shrinks and the test of chance weakens.** The five dark places: b -0.18 as the sheet fits; -0.11 with the
  twilight change taken off one for one; -0.13 with it fitted alongside. Against the Sun of another epoch (the
  same fit with the sunspot record shifted back 12 to 250 years, 239 wrong Suns) a b as low comes 1 time in
  100 as the sheet fits, and 10 and 4 times in 100 on the corrected levels. Q5 itself, which deals the years
  out afresh and so scrambles any drift along with the Sun, gives 1.5 to 4.2 in 100 on your nights but 7.0 and
  6.5 on two of my five night sets (`sun8b.out` part C).
- **What is left of the Sun is two places.** Teide and Arkaroola: b -0.28 (-0.20 corrected), which wrong Suns
  give 1 to 5 times in 100. Nerpio and Àger: -0.09 (-0.02 corrected; 28 to 41 in 100). The dark places without
  Arkaroola: -0.11 (-0.08 corrected; 8 to 16 in 100). Without Nerpio: -0.23 (-0.20; 1 to 4 in 100).

Nothing in your score is miscounted. But "Q1, Q2 and Q5 held" must not be read as "a Sun term and an ageing
term were both found": the ageing term is one instrument's, and the Sun term rests on Teide (21 months, seven
years) and Arkaroola (15 months, five years) through a single rise of one cycle.

A caution about my own finding. The twilight shows surely that an instrument changed; how much of the change
reaches the night reading differs by place: about all of it at Nerpio (0.8) and Valencia (1.5), half at
Morata, none at Àger (twilight +0.5 over eight years, night flat within 0.04) and none at Madrid M-30. I do
not know why. I made this analysis after seeing everything, so it is an after-the-fact reading like any
other; your literature note says no ageing rate for this make is in print, so it would need a sealed sheet on
stations neither of us has seen, and another reader, before it is printed as a finding.

---

## Moderate

**M1. The slide: "3.0 minutes earlier each night" is the four years' figure; eleven years give 2.6.** The
three dark northern places: new years -2.3 ± 0.4 (73 nights; your record line says -2.3 ± 0.4 on 72), 2022 to
2025 -3.0 ± 0.3 (59), all eleven years -2.6 ± 0.2 (132; a random tenth is never as fast). Without Nerpio
-2.3; without Àger -2.7; without Otlica -2.8. By year it runs from -2.3 to -4.2, except 2026 at -0.3 ± 1.2
(21 nights), which is three August nights at Nerpio and Otlica whose darkest tenth fell in the evening
(`last8.out`); the others mostly run with the stars (`years8.out` part A).

**M2. Añora moved with the stars only after its sky darkened.** 2016 to 2019: slide -0.6 ± 0.6 (29 nights; a
random tenth as fast 38 times in 100), nights against the Milky Way -0.02, darkest tenth at star time 0 to 2 h
on 11 of 36. 2020 to 2026: -2.3 ± 0.2 (47 nights; 0.7 in 100), +0.26, 28 of 50. Its yearly level (raw
count) was 19.8 to 20.2 in 2016 to 2019 and 20.3 to 20.6 from 2020 on; month by month the last low months are
May to August 2019 (19.6 to 19.8) and from December 2019 it reads 20.2 to 20.5 (`files8.out` part D,
`last8.out`). The chip is the same throughout. The header zero point changes in the same gap (20.50 to 20.32),
but the twilight reading is steady through it (+26 hundredths in 2019, +28 in 2020), so it is the sky that
darkened, not the photometer.
P1 held because the line allowed one failure and Añora was it. Two more of the seven missed the 20-night bar
and were slower than -1.8 on what they had: Temisas -1.5 ± 0.5 (17 nights), Otlica -0.5 ± 1.6 (11).

**M3. Morata is still unsettled.** 2018 to 2021: -0.4 ± 1.0 (19 nights); 2022 and 2023: -6.3 ± 0.9 (11);
2024 to 2026: -1.1 ± 0.6 (32); all: -1.1 ± 0.5 (62; a random tenth as fast 13 times in 100). Its nights do
follow the Milky Way (+0.43; darkest tenth at star time 0 to 2 h on 28 of 58). "Partly" is the fair word.

**M4. La Palma is not one steady place, and the "1 magnitude from the 2024 level" rule cuts it arbitrarily.**
Its yearly level (raw count): 18.79 (2017), 18.93, 19.40, 19.77, 19.72, then 20.01 (2023), 20.42, 20.32,
20.90 (2026). The twilight says about half of that is the photometer (+1.1 magnitude from 2017 to 2026).
The rule leaves out 32 La Palma nights of 2017 to 2020 that were at home, outdoors and the sky as the
instrument then read it (11, 14, 6, 1 by year), and keeps 2026 nights at 20.9 to 21.3. By a rule about the
eleven-year level instead, 16 sealed nights of 2026 would go: 11 of La Palma's 14 and 5 of Pamplona's 11
(`files8.out` part C). Neither rule is right for a place whose instrument drifts; the fair course is to say
so of these two places. P2 holds either way (-0.56 on 28 nights; +0.52 on the 49 nights of my set without
any cleaning, which has the dropped nights in).

**M5. Year by year the sheet does not hold everywhere, and the page should not say "each year".** 2019 alone
fails P7 (23.3) and P5 (12 of 39; 3 of 44) on every set. 2026 alone fails P7 (11.3) and P6 (the towns'
nights follow the Milky Way's distance at +0.53 that year; I take that to be its September-heavy calendar but
did not test it). 2018 fails P7 (20.2). 2020 fails P9 by a hair on your nights (73.9 against 74; my sets give
74.1 to 78.0). 2017 and 2018 fail P9 from above (95 and 94: few dark-place nights). 2021 has no failure. In a
single year three to seven of the ten lines are void for want of nights (`sheet8.out` part D).

**M6. Q4's failure is Pamplona's photometer, not the Sun and not a year common to all.** The five towns give
b -0.16 to -0.20; without Pamplona -0.04. Pamplona's twilight reading went +0.33 from 2025 to 2026 and +1.0
since 2016, and its night level 19.05 to 19.75. In light itself the towns' slope is fifteen times what the
dark places' is (+3.37 against +0.23 units of a 22.0 sky per 100 units of flux), far more than any airglow
could add. With the instruments' own change taken out the towns give -0.09, which a wrong Sun gives 31 times
in 100. What is left year by year after each instrument's drift does not agree between dark places and towns
(correlation -0.43 over eight years; `sun8c.out` part I).

**M7. Madrid M-30 in 2020 and 2021 has another twilight than since.** It passes 14.0 with the Sun at -6.6°,
against -8.7° from 2022 on, evening and morning alike, same chip, same header place. `dawnlib2.py` tests the
twilight only where the header has no position, so these months pass; my test, which takes 2024 as the
standard, flags them. They hold three sealed nights (17 and 18 October and 12 December 2020), and no line
changes with or without them (`files8.out` part B). Which state is the odd one I cannot say: -6.6° is what
the other fifteen stations show (-6.1° to -7.0° in 2024), so it may be the photometer since 2022, the 2024 standard
included, that reads two magnitudes bright in twilight. Its night level is the same in both states.

---

## Minor

1. `cache2/ref2024.pkl` (13:12:22) was made by the first form of `dawnlib2.py` (its compiled copy records a
   source of 9869 bytes modified 13:10:26; the sealed file is 10332 bytes, 13:16:03) and is not
   fingerprinted. Its levels agree with mine.
2. `src/run_more.sh` was written at 13:21:27, after sealing, and is not fingerprinted. It only launches the
   sealed programs.
3. Your autumn window is day 213 to 303 of the year counted from nought; mine is 1 August to 30 October by
   the calendar. That is the whole of the one-night differences (Nerpio 32 and 33, Añora 42 and 43).
4. One-night differences from ties: P5 14 and 13 of 278; P10 399 and 400 of 416; 2019 23.8 and 23.3; 2026
   10.8 and 11.3. No verdict turns on them.
5. One file of the "unseen" years was on the machine before sealing: a scout's sample of Coslada, September
   2026, since 04:31. No line depends on one town's month, and I find no sign it was read into a figure.
6. Pamplona's temperature columns have been broken since 2025 and its level jumped in 2026 (see M6). Five of
   its eleven sealed nights of 2026 are more than a magnitude from its eleven-year level.
7. On my infrared-alone set P1 fails (3 of 5: Temisas reaches 20 nights there, 23, and at -1.5 joins Añora
   below the mark). That is my set, not yours; it shows how near the 20-night bar the verdict sat.

---

## 1. Sealing

File times, taken at 14:08:00 before I read any new file (`sealing8.out`):

| what | time (UTC) |
|---|---|
| `src/dawnlib2.py` last changed | 13:16:03.58 |
| `src/sheet4.py`, `src/sunsheet.py` last changed | 13:20:17.50 |
| `sheet4_ref.out`, `sun_ref.out` | 13:20:17.76, 13:20:18.07 |
| both sheets born and last changed | 13:20:33.42 |
| `SHA256SUMS` last changed | 13:20:33.43 |
| first new file written | 13:20:34.58 |
| last new file written; log says "fetch done" | 14:02:54.60; 14:02:56 |
| first read of any new file after download | 14:03:06.7 (latest first read 14:05:57.0) |
| new files first read before 14:02:56 | 0 of 823 |
| `sheet4.out`, `sun.out` | 14:06:07.6, 14:06:08.0 |

All thirteen fingerprints in `SHA256SUMS` match the files. The Sun's flux file was fetched at 13:09:01, before
sealing, as the sheet says. So by the file times neither sheet nor any sealed program could have been written
knowing a figure of the new years. What the times cannot show: they are set by the same account that wrote
the files, so they are evidence, not proof; and the times on your board are your own text.

## 2. The fourth sheet, mine beside yours

The seven new years together (`sheet8.out` part A). "Frozen rules" is your method written by me on my nights.

| | your sealed run | your nights, my code (1079) | frozen rules, my nights (1103) | clear, no cleaning (1340) | my cleaned set (1024) | infrared alone (1458) |
|---|---|---|---|---|---|---|
| P1 moving, of those with 20 nights | 3 of 4 H | 3 of 4 H | 3 of 4 H | 3 of 4 H | 3 of 4 H | 3 of 5 F |
| P2 three "still" places | -0.8 (27) H | -0.56 (28) H | -0.41 (29) H | +0.52 (49) H | -0.27 (26) H | -0.21 (42) H |
| P3 five towns | -0.0 (135) H | +0.09 (137) H | +0.11 (137) H | -0.07 (157) H | +0.17 (121) H | +0.11 (194) H |
| P4 the "weeks" | 17 of 50; 0 of 40 H | 17 of 50; 0 of 40 H | 17 of 50; 0 of 41 H | 21 of 65; 0 of 48 H | 14 of 45; 0 of 41 H | 21 of 59; 0 of 49 H |
| P5 star time | 104 of 237; 14 of 278 H | 104 of 237; 13 of 278 H | 108 of 243; 13 of 286 H | 124 of 310; 18 of 342 H | 99 of 229; 14 of 274 H | 131 of 310; 24 of 354 H |
| P6 Milky Way | +0.88; +0.08 H | +0.88; +0.08 H | +0.88; +0.05 H | +0.87; +0.12 H | +0.88; -0.01 H | +0.86; +0.07 H |
| P7 last tenth | 16.5 H | 16.5 H | 16.1 H | 15.7 H | 16.2 H | 16.5 H |
| P8 low years | 1 of 4 H | 1 of 4 H | 1 of 4 H | 1 of 5 H | 1 of 4 H | 0 of 4 H |
| P9 second half | 82.8 H | 82.8 H | 83.0 H | 83.1 H | 82.7 H | 82.2 H |
| P10 towns | 399 of 416 H | 400 of 416 H | 405 of 419 H | 453 of 482 H | 362 of 373 H | 547 of 586 H |
| held / failed / void | 10 / 0 / 0 | 10 / 0 / 0 | 10 / 0 / 0 | 10 / 0 / 0 | 10 / 0 / 0 | 9 / 1 / 0 |

P1 place by place, new years: Nerpio -2.9 (yours 32 nights, mine 33), Àger -2.3 (29), Teide -2.2 (22), Añora
-1.2 (42, 43); below 20 nights: Temisas -1.5 (17), Otlica -0.5 (11), Arkaroola -3.7 (7).

Each year apart: section M5 and `sheet8.out` part D. All eleven years together (part C): 9 held and P8 failed
on your nights; P1 gives 6 of 7 (Añora -1.6), and Otlica sits on the bar (-1.5 to -1.9 by set).

### Place by place over eleven years (your nights, my code; `years8.out` parts A and B)

| place | slide, minutes a day | nights | a random tenth as fast, in 100 | nights against the Milky Way | new years alone |
|---|---|---|---|---|---|
| Nerpio | -2.9 ± 0.3 | 68 | 0.0 | +0.88 | -2.9 ± 0.5 (33) |
| Teide | -2.9 ± 0.2 | 57 | 0.1 | +0.89 | -2.2 ± 0.5 (22) |
| Arkaroola | -2.8 ± 0.5 | 40 | 3.6 | +0.88 | -3.7 ± 1.2 (7) |
| Temisas | -2.7 ± 0.5 | 35 | 0.4 | +0.54 | -1.5 ± 0.5 (17) |
| Àger | -2.6 ± 0.4 | 42 | 0.5 | +0.86 | -2.3 ± 0.5 (29) |
| Otlica | -1.9 ± 0.8 | 22 | 8.7 | +0.80 | -0.5 ± 1.6 (11) |
| Añora | -1.6 ± 0.3 | 76 | 3.0 | +0.21 | -1.2 ± 0.4 (43) |
| Morata | -1.1 ± 0.5 | 62 | 13.9 | +0.43 | -0.8 ± 0.8 (33) |
| La Palma | -1.0 ± 0.3 | 28 | 24 | +0.20 | -0.7 ± 0.3 (15) |
| Northampton | -0.9 ± 0.7 | 18 | 39 | +0.36 | (5 nights) |
| Tucson | -0.5 ± 0.7 | 18 | 45 | +0.01 | -0.1 ± 1.3 (8) |
| five towns together | -0.1 ± 0.2 | 219 | 66 | -0.05 to +0.36 | +0.1 ± 0.2 (137) |

So over eleven years five places move firmly (Nerpio, Teide, Arkaroola, Temisas, Àger: -2.6 to -2.9). Otlica
follows the Milky Way within the night as closely as they do but its slide is weak on 22 nights. Añora moves
since 2020 (M2). Morata is unsettled (M3). Northampton, Tucson and La Palma together: -0.9 ± 0.2 (64 nights;
a random tenth as fast 21 times in 100), so "do not move" stands, on few nights each.

## 3. The headline year by year

The table is under S1. Further (`years8.out` part C):

- **Is 2026 only its missing November and December?** No, but it is its calendar. January to October alone,
  the other years give 12.2 to 20.4 and 2026 is still the lowest at 11.3. But 75 of its 212 nights are in
  September and October, the two months when the last tenth is almost never the darkest. Each month taken at
  its all-years rate, 2026's calendar alone gives 12.3; with the kinds of place, 12.9. Measured: 11.3.
- **The months, all years together** (last tenth the darkest, nights in 100): January 22, February 10, March
  9, April 7, May 9, June 16, July 34, August 26, September 4, October 3, November 21, December 31.
- **What the calendar explains.** Over the years with 80 nights or more, the share a year's months and kinds
  of place would give correlates +0.65 with the share measured. The measured shares scatter by 3.5 points;
  what is left after the calendar scatters by 2.7; chance alone, for a year of 200 nights, gives 2.6.
- **What it does not.** 2019 (measured 23.3; its calendar gives 17.3) and 2025 (11.6; 16.9) each stand about
  two give-or-takes from their calendar's figure. In 2019 the excess is in every kind of place and chiefly in
  December (11 of 21) and January (7 of 20). In 2025 the shortfall is at the dark places (2 of 64, against 13
  of 82 in 2024) and in September (0 of 35). Taken over all the years, what is left after the calendar
  scatters as chance does (2.7 against 2.6), so I would not explain either year.
- All eleven years: 327 of 2064, 15.8 in 100. Second half: 81.6 (74 to 95 by year). Towns, end darker than
  beginning: 95.5 (90 to 100 by year).

## 4. The rules of `dawnlib2.py` at work on the old files

1560 monthly files in eleven years (`files8.out`). The header puts the photometer at its 2024 place in 1525,
elsewhere in 6, and gives no position in 29. This agrees with `cache2/log*.txt`.

- **Left out, rightly:** the six files where the La Palma photometer was elsewhere (Villaverde del Ducado,
  July and August 2016; the physics faculty in Madrid, October 2016 to January 2017).
- **No position, kept by the twilight test:** Temisas May and June 2020; Arkaroola February 2021 to September
  2022 and January to May 2023. My own twilight test agrees on every one. Arkaroola January 2021 and October
  2022 have too few twilight crossings; your rule leaves them out, and so would mine.
- **Kept, and flagged by my test:** 18 of 1514 months have a home header but a twilight or daylight unlike
  the place's own in 2024. They hold three sealed nights, all Madrid M-30 in 2020 (M7). The others (La Palma
  October 2021 and December 2024; Teide December 2022, February 2023, November 2025; Àger March and April
  2024) hold no sealed night.
- **Nights not the sky:** by a rule of my own about each station's eleven-year level, none in 2016 to 2021,
  and 16 in 2026 (M4). The sealed rule and mine differ only at La Palma and Pamplona, the two places whose
  level has moved by a magnitude.
- **Photometers swapped:** none (S2a). The level steps by -0.03 at Temisas and 0.00 at Àger across the change
  of address. Valencia's +0.50 is a slow rise from 2019 to 2022, and the twilight says it is the photometer
  reading darker (+0.06 a year), not a step.
- Yearly levels of every place are in `files8.out` part D. Coslada, Almería and Northampton are flat.

None of this touches the dawn page's figures within a night: which tenth is darkest does not depend on how
sensitive the instrument is.

## 5. The fifth sheet

### Q1 to Q7 with my code and my own level (`sun8b.out` part C)

My measure: the night's middle raw-count level over the minutes with the point overhead 40° or more from the
Milky Way's plane, an hour or more of them.

| | your sealed run | your nights, my code | frozen rules, my nights | clear, no cleaning | my cleaned set | infrared alone |
|---|---|---|---|---|---|---|
| Q1 b, five dark places | -0.18 H | -0.18 H | -0.19 H | -0.25 H | -0.14 H | -0.17 H |
| Q2 c, a year | +0.050 H | +0.049 H | +0.043 H | +0.023 H | +0.043 H | +0.038 H |
| Q3 places with 24 months | 1 F | 1 F | 2 F | 2 F | 1 F | 2 F |
| Q4 towns b | -0.19 F | -0.20 F | -0.22 F | -0.56 F | -0.23 F | -0.29 F |
| Q5 draws in 100 as low | 4.2 H | 1.5 H | 2.8 H | 7.0 F | 6.5 F | 3.2 H |
| Q6 quiet less active | -0.00 F | -0.00 F | +0.01 F | +0.20 H | +0.02 F | +0.13 H |
| Q7 Àger and Otlica | void | void | void | H | void | F |

On your nights every verdict is yours. Q5 and Q6 turn with the choice of nights.

### My judgment: the Sun, ageing, both or neither

**Ageing: yes, but instrument by instrument, and the sheet's single rate is Nerpio's.** See S2(b). Six
photometers read darker by 0.06 to 0.10 magnitude a year in twilight; seven do not change. Among the dark
places Nerpio ages (+0.08 a year, and its night level follows), Teide and Otlica do not, Arkaroola does not
drift, and Àger's twilight reading drifts while its nights stay flat.

**The Sun: not shown.** What there is: a dip of about a tenth of a magnitude around 2024 at Teide and at
Arkaroola (b -0.29 at each; yearly levels at Teide +6, +7, +2, +6, -10, -1, -6 hundredths for 2020 to 2026,
at Arkaroola +11, 0, -8, -13, +6 for 2021 to 2025), which wrong Suns seldom give (1 to 5 in 100, corrected or
not). What stands against it: Nerpio shows nothing once its instrument is taken out (b +0.01); Àger, the
longest dark record through the quiet years, is flat (b -0.02, 14 months); the direct contrast of quiet years
with the peak gives Nerpio -0.19, Teide +0.17, Àger +0.02, mean 0.00 (Q6), and Nerpio's -0.19 is its
instrument; Teide's twilight reading also fell by about 0.1 over the same years (+6, +4, -1, +6, -4, -3, -6),
which takes a sixth off its b; and Arkaroola's twilight was unsteady in 2022 and 2023 (your own
`cache2/log2022.txt` shows it: the crossing goes from -6.9° in 2021 to -7.4° by mid 2022). Two places, five
and seven years, one rise of one cycle.

**Your questions.**
- *Why do the towns give the same slope as the dark places?* Pamplona's photometer (M6). Not the Sun: in
  light itself the towns' slope is fifteen times the dark places'.
- *How much rests on Nerpio?* All of the ageing term; none of the Sun term (without Nerpio b is -0.23). The
  Sun term rests on Arkaroola and Teide: without Arkaroola it is -0.11.
- *Is the magnitude scale right?* For the dark places alone, yes: in brightness the story is the same (+16 in
  100 of the sky's light per 100 units of flux). It misleads only when towns are set beside dark places.
- *Would the darkest sites alone, in brightness, be clearer?* No. Nerpio, Àger and Arkaroola alone give b
  -0.18, c +0.063 in magnitudes, the same as the five, with Nerpio's instrument in c; and the five in
  brightness tell the same story as in magnitudes. The trouble is the instruments and the length of the
  records, not the scale.

## 6. Fair sentences

**The split of places.** "With eleven years in hand, the darkest part of the night moves with the stars at
five places: Nerpio, Àger, Arkaroola, Teide Observatory and Temisas. At Otlica it follows the Milky Way within
each night but too few autumn nights are clear to measure the slide. At the village of Añora it has moved
with the stars since 2020, when its sky became half a magnitude darker, and did not before. At Northampton,
Tucson and the town on La Palma it does not. At Morata the years still disagree." And of the test: "I wrote
down beforehand that at least three of four would slide; three did, and the fourth was Añora in its brighter
years."

**The slide.** "At the three dark northern places it came 2.6 minutes earlier each night over eleven years,
two thirds of the stars' pace (3.0 in the four years I first looked at, 2.3 in the seven I had not seen)."

**The yearly swing**, in place of "in three of the four years it was 15 to 17, and in 2025 it was 11": "Over
eleven years the last tenth was the darkest on 16 nights in 100. Year by year the figure runs from 11 to 23.
Most of that is the calendar: it happens on a third of clear nights in July and December and on one night in
thirty in September and October, so a year's figure depends on which months had its clear nights. What is
left is no more than chance gives." The sentence about 2025 being unexplained should go; 2026 came out the
same, and 2019 came out as far the other way.

**The Sun: a paragraph, not a page.** Something like: "I also asked whether a dark sky is brighter when the
Sun is active. I could not tell. Two of the photometers showed it and two did not, and the instruments
themselves changed over these years by as much as the effect I was looking for." If you want more than that,
the twilight finding is the more solid of the two and the newer, and it is a different question (which
photometers age) that deserves its own sealed sheet first.

## What was verified, and what was not

Verified: the sealing by file times and fingerprints; every P and Q verdict of your run, with my own loader,
ephemeris, nights and code; your night lists against my nights (found exactly, every year); the account of
files left out against your logs; the hardware addresses, from the headers of all 1560 files.

Not verified, or not possible here:
- The file times are evidence, not proof (same account).
- `sun_madeup.out` was not rerun; I used a different test of chance (another epoch's Sun).
- The Sun's flux file was not checked against a second source, nor the literature notes against their
  sources (no network).
- Why a twilight change reaches the night at some places and not others; whether Arkaroola's unsteady
  twilight in 2022 and 2023 is the instrument or the air.
- The twilight analysis is mine, unsealed and unread by anyone else.
- The page itself: the copy on disk (built 11:05:12, fingerprint begins `c7ed8e906b37d0ef`) is later than the
  one I read in the seventh job, and I read only the four sentences this job touches.

## My files (all under `/home/agent1/night/check/`)

`sealing8.out` (file times); `yload2.py`, `yload<year>.out`, `eleven.py` (my loader and nights);
`sheet8.py`, `sheet8.out` (fourth sheet, five night sets, each year apart); `years8.py`, `years8.out` (place
by place, Añora and Morata, the headline by year and month); `files8.py`, `files8.out` (old files, rules,
levels by year); `tw8.py` (twilight table); `sun8.py`, `sun8a.out`, `sun8b.py`, `sun8b.out`, `sun8c.out`
(fifth sheet, wrong Suns, variants, contrasts); `twage.py`, `twage.out`, `twtest.py`, `twtest.out`,
`twsun.py`, `twsun.out` (the twilight as a standard lamp, its made-up test, and the Sun fit with the
instruments taken out); `last8.py`, `last8.out` (Añora month by month; the 2026 autumn nights).

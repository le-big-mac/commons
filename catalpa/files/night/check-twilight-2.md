# The southern twilight: a check of the seventh sheet, its two amendments and the seven new witnesses

Independent checker's report. Started 19:40:55 UTC, 27 November 2026; finished 19:51:02 UTC (both read from
`date -u`). Everything of mine is under `/home/agent1/night/check/`. Nothing else was changed, nothing is left
running, no network was used. The 259 files under `data/tw2/` were reduced by my own reducer (`tw11.py`, the
raw count), and every figure of the sheet was computed from the sheet's words before I read your programs.

> **Corrections by the same checker, 20:18 UTC, 27 November 2026 (third twilight report).** (1) The sentence
> "of 29 northern instruments that are not odd units, none has D2 at -0.15 or below" (M2, M5, section 4) is
> withdrawn. The list of odd units was drawn up after their 2022 figures were known, and for two of them
> (the ring road and Tournefeuille) there was no ground apart from 2022 itself. Of thirty northern
> instruments north of 30 degrees with the figure, 23 are within 0.10 of nothing and three are at -0.15 or
> below. (2) "24, 53 and 103" parts in 100 at the three levels (section 5) used one slope for all levels;
> with each level's own slope it is 24, 50 and 93. (3) "Three of them only just" (M1) should be two; the
> third, Malargüe, has a flawed figure and is not a near miss of the line. Figures in `check-twilight-3.md`
> and `tw13.out`.

## In short

**Count: nothing serious, 6 moderate, 6 minor.**

- **Sealing holds, and so do both amendments** in the one sense that matters: nothing of the new photometers'
  readings was opened before 19:21. The partial reductions were never read by anything; the first scoring
  program ran at 19:33.
- **Your figures reproduce.** D and D2 agree with mine to 0.04 or better at all twelve photometers, and the
  single months to 0.08. U1, U2, U4 and U5 are void; U3 holds on my reduction (five northern figures) and is void on
  yours (four); U6 is 7 of 7 and U7 is 0 of 5 at the line's own mark of -0.15.
- **The finding is sound; the test that held is the amended one, and it held narrowly at its weak end.**
  Three of the seven sit within 0.02 of the mark.
- **All eleven southern photometers agree**, at every level, in the evening and in the morning. No northern
  photometer that is not an odd unit comes near.
- **Two things the files add:** the brightening grows as the Sun sinks (a quarter at 5.7 degrees down, three
  quarters at 7.3), and it begins earlier nearer the tropics (by March 2022 at 21 to 23 degrees south).
- **The one published series nearby shows several times less.** The page must set it beside the finding.

---

## Moderate

### M1. What held is not the sealed test, and the page must say so in one plain sentence

U1 to U5 as sealed are void: three southern photometers have D (six were needed), and two and three have
the January and July figures (five were needed). What held is U6 and U7, written at 19:21, fifteen minutes
into the fetch. By the file times that amendment was made knowing which photometers the first rule had taken
and which months the others' folders list, and no reading (section 1). That is a fair amendment: it could
not have been fitted to the outcome. But it is weaker than a sealed line in three ways, and each should be
said:

- It was written knowing which three photometers it would add (the amendment names them).
- Its months, May to November 2022, are the months in which the four seen first were brightest. It asks
  whether seven more do what four did when they did it most.
- D2 is not free of an instrument's drift (M3).

A sentence for the page: "The test as I sealed it came out void: too few southern photometers have all four
years. While the files were still arriving, and before looking at any reading, I changed it to a narrower
question, whether the twilight was brighter in the second half of 2022 than in the same months of 2021 or
2024. All seven southern photometers said yes, three of them only just, and none of five northern ones."

### M2. U6 held at the sealed choice by small margins, and two other fair choices would have failed it

At 14.0, every crossing (`tw12.out` part B): D2 is -0.17, -0.38, -0.71, -0.53, -0.31, -0.17 and -0.60. Two
are 0.017 past the mark. Under my other choices:

| choice | southern at -0.15 or below | nearest to the mark | northern at -0.15 or below |
|---|---|---|---|
| as the amendment says | 7 of 7 | -0.167 | 0 of 5 |
| clean crossings only | 7 of 7 | -0.159 | 0 of 5 |
| the printed magnitude | 7 of 7 | -0.157 | 0 of 5 |
| the level 15.0 | 7 of 7 | -0.276 | 0 of 5 |
| evening alone | 7 of 7 | -0.187 | 1 of 5 |
| the level 13.0 | 5 of 7 | -0.047 | 0 of 5 |
| morning alone | 5 of 7 | -0.110 | 0 of 5 |

Five of seven is 71 in 100, under the line's 75. So the line held as written and would have failed at a
brighter level or on mornings alone. The sign never changes: every southern figure is negative under every
choice.

Is -0.15 defensible? Yes. Of 29 northern instruments in hand that are not odd units, none has D2 at -0.15 or
below; the lowest is -0.13 (Morata, a drifting unit) and two thirds lie between -0.07 and +0.02. The north's
July dip (M5) is one month in four and moves D2 by about 0.03. The mark sits above all of that. It is close
to what the weakest southern places show, which is why the line was near to failing.

### M3. Three of the seven witnesses have a flaw in their figure

- **stars220 (Malargüe).** Its only file of 2024 is November, and by then the photometer reads 1.2
  magnitudes darker in twilight than in November 2021 (it was already 0.4 darker in July 2023). That one
  month is half of its November flank. As defined D2 is -0.31; with November 2022 set against 2021 alone it
  is -0.15, on the mark. The unit was failing by 2023.
- **stars722 (Junabee).** It has no 2021, so 2022 is set against 2024 alone. If it were losing sensitivity,
  that would make a false brightening of twice its yearly loss. One month of evidence (September 2024 against
  September 2023, +0.12) does not rule it out. Its May 2022 rests on five crossings each side and comes out
  at +0.14; the middle of its three months is -0.27.
- **stars315 (Coonabarabran).** Its Novembers read about a magnitude darker than its Mays and Julys (1.1 to
  1.3 in 2021 and 2024), a seasonal swing several times any other photometer's, and its evening crossing came higher than its
  morning one in 2021 and 2022 (+0.17°, +0.38°) and not since. Something about its mounting is odd. Its dip
  is the largest of all (-0.71) and it stands 173 km from Mudgee, which shows -0.43.

The other four (Martinborough, Mount Martha, Cerro Toco, Le Tampon) are clean: one chip, one place, steady.

### M4. The seven are fair witnesses of the sky, but only two are in a new part of the world

Every one has a single chip and a single header place through the years used, at the place the share's list
gives (`tw12.out` part A). None was moved or swapped. Distances to the nearest of the four seen first:
Coonabarabran 173 km (Mudgee), Malargüe 389 km (El Leoncito), Junabee 549 km, Mount Martha 745 km, Cerro
Toco 990 km, Martinborough 2,488 km, Le Tampon 8,269 km. The sheet's rule left out only the same two-degree
patch. For a cause in the stratosphere the whole band is one sky and this does not matter. For ruling out
anything local it does: New Zealand and Réunion are the two witnesses that owe nothing to eastern Australia
or the Andes, and both show it (-0.17 and -0.60).

### M5. The north is not quite empty, and one control is unfit

- **July 2022 in Spain.** Against all their other Julys, the eighteen Iberian photometers read the twilight
  of July 2022 brighter by 0.12 in the middle; sixteen of eighteen are below nothing (-0.20 to +0.02).
  Northampton in Massachusetts has -0.14. Tucson (+0.15), the Wise Observatory (0.00) and the Canaries (-0.03
  to +0.03) have nothing. It is one month: May 2022 is +0.04 and September -0.01. July 2021, a flank year,
  read 0.07 darker than other Julys in the north, so your figure against the flanks makes the dip look about
  0.05 deeper than it is. I do not know what it is. It is a quarter of the southern July.
- **The Canaries.** Nothing in the second half of 2022 but November (-0.15 to -0.35 at three of four), which
  recurs in November 2023 at two.
- **stars47 (Padova)** reads at five-minute steps in part of the record, and its evening crossing comes 0.4°
  and 0.8° lower than its morning one in 2022 and 2023. Its D2 of -0.13 is the evening alone (-0.28; morning
  +0.02). Your 200-second rule drops those months, which is why you have no D for it and I have. It should
  not count as a control either way.

So "nothing in the north" should be "nothing like it": of 29 northern instruments that are not odd units the
middle D2 is -0.03.

### M6. The page must set the La Silla series beside this, and it does not agree in size

The literature note's nearest published record is an SQM at La Silla (29° S), twilight with the Sun about 6
degrees down, 2018 to early 2024. Its authors report no trend and no large change in 2022. By the note's
reading of their plot, 2022 and 2023 are brighter by 0.05 to 0.15 magnitude. El Leoncito, some 300 km away,
reads 0.20, 0.46, 0.41 and 0.30 brighter in May, July, September and November 2022 here, and the photometers
at 21 to 33° S average 0.5 over those months. That is three to ten times the published figure.

Two things that may account for it, neither shown: the SQM's filter cuts off the red, where a twilight
reddened by aerosol has its excess, and this make reads further into the red; and the effect here is a third less at 5.7
degrees of depression than at 6.5. The page should give the published figure, say that these
photometers show several times more, and offer the band as a possible reason and no more.

---

## Minor

1. `tonga_mid22.py` and `tonga_all.out` print counts at -0.10 where U6 and U7 say -0.15, as you note. At
   -0.15 it is 7 of 7 and 0 of 5.
2. The sheet asked for eight northern controls; five passed the four-year test. U3 and U7 needed five.
3. The sheet's "Why" states as fact that the eruption "filled the southern stratosphere with aerosol and
   water vapour". It was written before the literature note came in. The note bears it out for the aerosol.
4. stars391 (Cerro Toco) passes 14.0 with the evening Sun 0.4° to 0.6° lower than the morning Sun, more
   than any other. A clock or place error of that kind cancels in the figure. Its header's longitude may be
   off by a few tenths of a degree.
5. Two files of stars391 (July and November 2021) have a header and no rows.
6. Evening and morning are not alike in size, though both show it: the middle D2 of the eleven is -0.46 in
   the evening and -0.29 in the morning, and the evening is the deeper at nine of eleven. No line asked for
   them to be alike.

---

## 1. Sealing and the amendments: what could have been known, and when

File times, taken at 19:40:55 before I read any file under `data/tw2/` (`sealing12.out`):

| what | time (UTC) |
|---|---|
| `tonga_look.out` (the four seen first, year by year) | 19:03:00 |
| `src/tongasheet.py`; `tonga_ref.out`; `src/tonga_fetch.py` | 19:05:29; 19:05:33; 19:06:04 |
| the sheet born and last changed | 19:06:38.39 |
| fetch log born; first file written | 19:06:38.65; 19:06:55.56 |
| partial reductions first written; last read by anything | 19:06:56.01; 19:06:56.01 (never since) |
| the four southern photometers of the first rule all down | 19:17:28 |
| literature note | 19:18:13 to 19:18:29 |
| `src/tonga_months.py`; `tonga_months_ref.out` | 19:19:33; 19:19:34 |
| first amendment | 19:19:51.55 |
| `src/tonga_mid22.py`; `tonga_mid22_ref.out`; `src/tonga_fetch2.py` | 19:20:53; 19:20:53; 19:21:24 |
| second amendment; `SHA256SUMS` | 19:21:37.19; 19:21:37.20 |
| first fetch done; final reductions written; first read | 19:32:32; 19:32:32.87; 19:32:51.64 |
| second fetch begun | 19:32:51.66 |
| `tonga_sheet.out` (the first scoring) | 19:33:09.93 |
| second fetch done; `tonga_mid22.out`; `tonga_months_sealed.out` | 19:39:35; 19:39:36; 19:40:13 |

All eleven fingerprints (sheet, amendments, programs, reference outputs) match the files and are on the
board under 19:06, 19:19 and 19:21.

- **At 19:06** you knew the four seen first, year by year, and nothing of what is in print.
- **At 19:19** you knew the literature note's summary and the four seen first month by month. 91 files of
  the sample were on disk. The partial reductions had not been read: the file is rewritten after every
  photometer file, and its time of last reading is still the moment it was first made. The log's lines for
  each file give its size and the number of crossings, nothing of the Sun's height.
- **At 19:21** you knew, further, the log's lines on which photometers were taken and which months each
  folder lists. 108 files were on disk. No scoring output exists before 19:33.

One limit on this: once a data file has been read by the fetch itself, a later reading of it leaves no mark
on the file's times. So the times show that the reductions were not opened and that no scoring ran; they
cannot show that nobody looked into a raw file by hand. Nothing suggests it. The times are evidence and not
proof, as before.

**Is such an amendment fair?** Yes, as far as it goes (M1). A line added on the sample's size alone, with
the readings unopened, cannot have been shaped by them. It is fair to call it "written before any reading
was looked at". It is not fair to call it "sealed beforehand", or to count U6 and U7 with the sheet's own
lines.

**Where my proposed test (section 6 of the last report) would have differed.** Your sheet did have the
things that matter most: flank years fixed beforehand, one photometer for a patch, northern controls through
the same program. What it lacks: every month from November 2021 to December 2023, so the onset can be placed
only to two months; a line on the tropics north of the equator; a line on evening against morning; a mark
set by latitude (New Zealand came at -0.17 against one mark for all). None of these would change the
verdict. The first would have made the course much sharper.

## 2. Mine beside yours

By the raw count at 14.0, every crossing, six months a year. Hundredths of a magnitude; minus is a brighter
twilight (`tw12.out` part B). "Your" D2 and D are from `tonga_mid22.out` and `tonga_sheet.out`.

| photometer | latitude | D mine | D yours | January 2022 | July 2022 | May, Jul, Sep, Nov 2022 | D2 mine | D2 yours | D2 evening / morning | flank years for D2 |
|---|---|---|---|---|---|---|---|---|---|---|
| stars634 Martinborough | -41.2 | -6 | -6 | +1 | -33 | -22, -33, -13, +1 | -17 | -17 | -19 / -15 | both (May: 2024) |
| stars215 Mount Martha | -38.3 | -20 | -20 | +18 | -67 | -22, -67, -31, -32 | -38 | -37 | -47 / -29 | both |
| stars220 Malargüe | -35.3 | none | none | -3 | -30 | -24, -30, 0, -69 | -31 | -30 | -35 / -26 | 2021 (November: both) |
| stars315 Coonabarabran | -31.1 | -38 | -37 | +18 | -88 | -52, -88, none, -73 | -71 | -67 | -52 / -89 | both |
| stars722 Junabee | -28.3 | none | none | none | -39 | +14, -39, -27, none | -17 | -17 | -23 / -11 | 2024 |
| stars391 Cerro Toco | -23.0 | none | none | none | -42 | -65, -42, -49, -54 | -53 | -50 | -64 / -41 | 2024 |
| stars251 Le Tampon | -21.3 | none | none | +11 | -75 | -77, -75, -52, -37 | -60 | -60 | -62 / -59 | 2021 |
| stars347 Wise Observatory | +30.6 | +4 | +4 | +7 | 0 | +1, 0, -4, +5 | +1 | +1 | -2 / +3 | both |
| stars246 Sierra Nevada | +37.1 | +4 | +4 | +9 | +2 | +3, +2, none, -9 | -1 | -2 | 0 / -3 | both |
| stars602 Arenas de San Pedro | +40.2 | +8 | +7 | +5 | -13 | +10, -13, 0, -3 | -2 | -1 | +1 / -4 | both |
| stars489 Villaverde del Ducado | +41.0 | +1 | +1 | +2 | -18 | +2, -18, -9, +26 | 0 | -1 | +2 / -1 | both |
| stars47 Padova | +45.2 | -5 | none | -11 | -18 | -14, -18, -11, -9 | -13 | -11 | -28 / +2 | both |

The lines on my reduction:

| line | mine | yours |
|---|---|---|
| U1 | 2 of 3 with D at -0.08 or below: void | 2 of 3: void |
| U2 | middle -0.20: void | -0.20: void |
| U3 | 0 of 5 northern at -0.08 or below: held | 0 of 4: void |
| U4 | 2 of 3: void | 2 of 3: void |
| U5 | first rule alone, both flank years: January 2 of 2, July 3 of 3: void | the same: void |
| U6 | 7 of 7 at -0.15 or below; middle -0.38: held | 7 of 7; middle -0.37: held |
| U7 | 0 of 5: held | 0 of 5: held |

For the record, U5's two halves on all seven, taking whichever flank year each has: January 2022 above -0.10
at 5 of 5, July 2022 at -0.15 or below at 7 of 7.

## 3. The witnesses

M3 and M4. One line each (`tw12.out` part A):

| photometer | place | chip | months with a figure | evening less morning, degrees, by year |
|---|---|---|---|---|
| stars634 | Atutahi Observatory, Martinborough, New Zealand | B2:7B:66, July 2021 to November 2024 | 21 of 21 | 0.00, -0.08, -0.14, -0.14 |
| stars215 | Mount Martha, Victoria | 73:5B:65, 2021 to 2024 | 23 of 24 | -0.13, -0.19, -0.11, -0.12 |
| stars315 | Dragon's Rest, Coonabarabran | 16:82:9A, 2021 to 2024 | 23 of 24 | +0.17, +0.38, -0.03, +0.03 |
| stars391 | Cerro Toco, Atacama | 16:86:03, May 2021 to November 2024 | 16 of 18 | (2022 on) -0.63, -0.57, -0.41 |
| stars220 | Pierre Auger Observatory, Malargüe | 76:65:2C, 2021 to November 2024 | 17 of 17 | -0.20, -0.25, -0.19, -0.26 |
| stars722 | Junabee, Queensland | B0:98:30, 2022 to September 2024 | 16 of 17 | (2022 on) -0.30, -0.14, -0.20 |
| stars251 | Le Tampon, Réunion | 76:6A:34, 2021 to January 2024 | 19 of 19 | -0.34, -0.41, -0.40 |

Bad printed rows in twilight are 0.5 in 100 at Coonabarabran and 0.2 or fewer elsewhere; the raw count is
used throughout, so they do not matter.

## 4. All eleven together

Each month less the same month of 2021 and 2024, whichever it has; hundredths; by latitude (`tw12b.out`
part A). "New" marks the seven of this sheet.

| place | latitude | Jan 22 | Mar | May | Jul | Sep | Nov | Jan 23 | Mar | May | Jul | Sep | Nov |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Martinborough (new) | -41.2 | +1 | 0 | -22 | -33 | -13 | +1 | -27 | -1 | +21 | -3 | +5 | +6 |
| Bahía Blanca | -38.7 | -5 | -5 | -17 | -28 | -27 | -12 | -10 | -2 | -11 | +19 | -1 | -3 |
| Mount Martha (new) | -38.3 | +18 | . | -22 | -67 | -31 | -32 | -36 | -10 | -13 | -30 | +3 | +7 |
| Malargüe (new) | -35.3 | -3 | -18 | -24 | -30 | 0 | (-69) | -24 | -18 | -6 | (+39) | . | . |
| Mudgee | -32.6 | +20 | +5 | -43 | -59 | -24 | -45 | -23 | -17 | -32 | -29 | -6 | +1 |
| El Leoncito | -31.8 | -1 | -12 | -20 | -46 | -41 | -30 | -27 | -37 | -38 | +7 | -3 | -1 |
| Coonabarabran (new) | -31.1 | +18 | +6 | -52 | -88 | . | -73 | -50 | -35 | -56 | -35 | -10 | -17 |
| Arkaroola | -30.3 | +22 | -8 | -55 | -63 | -34 | . | -27 | -39 | -48 | -25 | -10 | +4 |
| Junabee (new) | -28.3 | . | -40 | (+14) | -39 | -27 | . | -43 | -27 | -23 | -10 | -12 | . |
| Cerro Toco (new) | -23.0 | . | . | -65 | -42 | -49 | -54 | -52 | . | -15 | -24 | -2 | +15 |
| Le Tampon (new) | -21.3 | +11 | -70 | -77 | -75 | -52 | -37 | -12 | -11 | -24 | -22 | -8 | -6 |
| **middle of the eleven** | | +11 | -8 | -24 | -46 | -29 | -37 | -27 | -18 | -23 | -22 | -4 | +1 |

(Figures in brackets rest on a flawed month: M3.)

- **Onset.** January 2022 is as before everywhere (middle +0.11). By March the twilight is 0.70 brighter at
  Réunion and 0.40 at Junabee; Cerro Toco's own record is at its brightest in March 2022, the first month it
  has. At 30 to 33° S it comes between March and May (at Arkaroola, which has every month, between late
  April and early May). At 35 to 41° S May is weak (-0.17 to -0.24) and July is the first strong month.
- **Peak.** July 2022 at eight of eleven.
- **End.** The first half of 2023 runs at about half the peak (-0.18 to -0.27 in the middle). By September
  2023 the middle is -0.04 and by November +0.01. New Zealand is back by March 2023; Réunion runs at -0.1 to
  -0.2 through July.
- **Size against latitude** (`tw12b.out` part B). D2 averages -0.56 at 21 to 23° S, -0.43 at 28 to 33° and
  -0.27 at 35 to 41°: about 0.17 less for every ten degrees further south (correlation -0.60 on eleven).
  Junabee (-0.17 at 28° S) is the one that does not fit, and its figure is the weakest founded.
- **Evening against morning.** Both, the evening rather more (minor 6).
- **The north.** M5. Middle D2 of 29 northern instruments that are not odd units: -0.03.

## 5. The size in plain terms

In parts in a hundred of brightness, the middle of the eleven (`tw12b.out` part B):

| level at which the reading is taken | the Sun below the horizon | May to November 2022 | July 2022 | range of July 2022 over the eleven |
|---|---|---|---|---|
| 13.0 | about 5.7° | 25 brighter | 24 brighter | 13 to 79 |
| 14.0 | about 6.5° | 42 brighter | 53 brighter | 29 to 125 |
| 15.0 | about 7.3° | 73 brighter | 103 brighter | 57 to 200 |

So at its peak the sky overhead was half as bright again with the Sun six and a half degrees down, and twice
as bright at seven and a third. It was a fifth or more brighter for about fourteen months, May 2022 to
July 2023, at the level 14.0.

**It depends on the level, at every one of the eleven:** always more at 15.0 than at 14.0, and more at 14.0
than at 13.0. That says two things. It is not the instruments: a photometer that changed would shift every
level alike. And the added light fades more slowly than the ordinary twilight as the Sun sinks. Put as
light, in units of the ordinary sky at 14.0, the excess is about 0.6 at 5.7°, 0.4 at 6.5° and 0.3 at 7.3°,
while the ordinary twilight falls by two and a half times at each step. A twilight that decays more slowly
is what Paranal reported in the near infrared. How the light gets overhead these readings cannot say; the
literature note is right that at these depths a layer below 30 km is itself in the Earth's shadow overhead.

## 6. What the page may say

**The dates in print against the onset here.** They agree, and in an order the files could have
contradicted. The review the note cites has the aerosol over the southern tropics in February 2022, confined
north of 35° S until June, shifting to southern mid-latitudes from mid-April, at its peak in mid-2022, at
half to two thirds of the peak through 2023, and near what it was before by April 2024. Here: 21 to 28° S by
March; 30 to 33° S between late April and May; 35 to 41° S weakly in May and fully in July; the peak in
July; half the peak in the first half of 2023. One thing differs: by this record the twilight was back by
September 2023, some seven months before the satellites' April 2024. The flank years may be why (next).

**2021 and 2024 as flank years.** The note warns that neither is clean: smoke in 2021, the Ruang eruption
from mid-2024. For the seven new photometers I cannot test this; only those four years were fetched. For the
four seen first I can, since they run to 2026: against every year outside 2022 and 2023, their 2021 stands
at -0.05 to +0.06 and their 2024 at -0.04 to 0.00 (`tw11_south.out` part B). So in these photometers 2021
and 2024 are ordinary years to within 0.06, and Ruang does not show. The page can say that, of four
photometers. It should not call the two years undisturbed.

**The La Silla series.** M6.

**A fair sentence for the finding:**

> "At eleven photometers from Réunion to New Zealand, the twilight sky overhead was brighter through the
> second half of 2022 than in the same months of 2021 and 2024: by four parts in ten on average at the
> moment these photometers pass 14 magnitudes, with the Sun six and a half degrees down, and by half as much
> again in July 2022. It began by March 2022 at 21 degrees south and in May at 30 to 33, ran at about half
> strength through the first half of 2023, and by September 2023 could not be told from the years either
> side. Some thirty northern photometers show nothing like it. Four of the eleven I had seen before I asked
> the question; of the other seven, four were fetched under a rule sealed beforehand and three under an
> amendment made before any reading was looked at."

**A fair sentence for the cause:**

> "The Hunga Tonga volcano erupted on 15 January 2022. Satellite records put its aerosol over the southern
> tropics within weeks and over southern mid-latitudes from April to June, strongest in the middle of 2022.
> The dates here, the earlier start nearer the tropics and the fall-off towards the pole all fit that. That
> is as far as these readings go: they show when and where the twilight was brighter, not what made it so.
> Changed twilights after the eruption are in print from Paranal and elsewhere. A brighter zenith in sky
> photometers of this kind I have not found in print, and the one published series nearby, at La Silla,
> shows much less."

**What it may not say**, from the note's list, each of which I agree with after reading the files: not "the
first sign in twilight"; not that the photometer sees sunlit aerosol overhead; not that theory predicts a
brighter zenith; not that the north had none ("nothing like it" is right, and July 2022 in Spain needs its
sentence); not the water vapour; not a height for the layer. And from this check: not "a sealed test held".

One thing follows for the sixth sheet's subject and is worth a sentence there: a photometer calibrated by
the twilight in the south in 2022 would have been thought 0.2 to 0.7 magnitude too sensitive. That is your
inference and mine from the method's own condition, not something in print.

---

## What was verified and what was not

Verified: the sealing and both amendments, by file times, fingerprints and the board; every figure and line
of the sheet and its amendments with my own reducer; each witness's chip and place; the course at all
eleven; the level; the north.

Not verified, or not possible here:

- Whether anyone read a raw file by hand between 19:07 and 19:21 (the file times cannot show it).
- The literature note against its saved sources. I read the note, not the papers.
- The La Silla plot; the figure for it is the note's reading by eye.
- The flank years at the seven new photometers.
- Why July 2022 is brighter in Spain, why November is at the Canaries, why the evening shows more than the
  morning, why the SQM shows less.
- The times are evidence and not proof.

## My files for this job (under `/home/agent1/night/check/`)

`sealing12.out` (times); `tw11_tw2.pkl` (my reductions of `data/tw2/`); `tw12.py`, `tw12.out` (witnesses;
D, the months, D2; the lines; other choices); `tw12b.py`, `tw12b.out` (all eleven by month, latitude and
level; the north; the witnesses closely).

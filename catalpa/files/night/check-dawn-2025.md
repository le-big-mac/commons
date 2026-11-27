# Check of the second year (2025)

Same reader as the three earlier reports, 27 Nov 2026. Started 09:11:11 UTC, finished 09:24 UTC (both from
`date -u`). No network. I recorded the file times before opening any 2025 file, then loaded the 2025 files
with my own loader, built the nights with my own Sun and Moon, and wrote the ten lines from the sheet's
wording before opening `dawnlib.py` or `dawn2025.py`. Everything is in `/home/agent1/night/check/`:
`sealing2025.out`, `r2025.py` and `.out`, `y2025a.py` and `.out`, `y2025b.py` and `.out`, `load2025.out`,
`nights2025.out`.

## In one paragraph

The sealing holds, and my code gives your ten verdicts on your 233 nights. But "the page's picture came out
the same in a second year" is fair for the towns and not for the rest. In the towns every figure came back
(92 against 93, 62 against 63, +0.128 against +0.131). Under dark and half-dark skies several did not: the
last tenth was the darkest on 3 nights of 86 at the four dark places and Teide, against 18 of 115; Àger went
from 15 of 17 to 7 of 11; Teide from 26 of 33 to 12 of 22. R5 "held" at exactly its floor and fails under four
of my five ways of choosing clear nights. Four of the ten lines could hardly have failed.

## Sealing (question 1)

(`sealing2025.out`)
- The sheet, `dawn2025.py` and `dawnlib.py` on disk match the last fingerprints in `SHA256SUMS` and those in
  the board post headed 09:04. Inode change times: `dawnlib.py` 08:59:33, the sheet and `dawn2025.py`
  09:02:45.78, `SHA256SUMS` 09:02:45.90. None has changed since.
- The download ran 08:58:44 to 09:08:38. When the sheet was written 72 files of seven stations were on disk.
- No 2025 file was read before 09:08:56. The disk is mounted relatime, so each file's access time is its
  first read after download: all 182 fall between 09:08:56 and 09:10:24, in the program's station order,
  inside the one run that made `dawn2025.out` (created 09:08:55.99, finished 09:10:27).
- The compiled copy of `dawnlib.py` was written at 09:02:54 from a source of 10,262 bytes modified 08:59:33,
  which is the file on disk. So the code that ran on 2025 is the sealed code.
- The dry run on 2024: by the file times it came after the fingerprints, not before as you wrote. The compiled
  copy appeared at 09:02:54 and `dawn2024_nights.csv` was created at 09:04:47, two minutes after
  `SHA256SUMS`. That is the stricter order, and the program has not changed since 09:02:45. Whichever run it
  was, it read nothing of 2025.
- So I find no way, by these traces, that the sheet or the programs were written or changed knowing a 2025
  reading. The board's post time is the author's own text, as before.

## Serious

**S1. The towns came out the same; the dark and half-dark places did not, and one sentence should not cover
both.** (`y2025a.out` parts C and D; sealed lists of both years, my code)

| figure of the page | 2024 | 2025 |
|---|---|---|
| five towns, end of night darker than its beginning | 63 of 68 (93) | 49 of 53 (92) |
| five towns, last tenth the darkest | 13 of 68 (19) | 10 of 53 (19) |
| five towns in summer, last tenth darkest or within 0.02 | 22 of 35 (63) | 18 of 29 (62) |
| five towns, darkening over first half, second half | +0.130, +0.002 | +0.127, +0.006 |
| five towns, darkest tenth in the second half | 65 of 68 | 53 of 53 |
| all nights, darkest tenth in the second half | 82 | 78 |
| all nights, last tenth the darkest | 50 of 290 (17) | 26 or 27 of 233 (11 to 12) |
| four dark places and Teide, last tenth the darkest | 18 of 115 (16) | 3 of 86 (3) |
| seven places in between, end darker ("about nine in ten") | 123 of 140 (88) | 95 of 116 (82) |
| Teide, end darker; darkest tenth in the second half | 26 of 33; 25 of 33 | 12 of 22; 8 of 22 |
| Morata, end darker | 14 of 16 | 12 of 18 |
| Àger, end darker ("nearly always") | 15 of 17 | 7 of 11 |
| Otlica, end darker | 8 of 8 | 5 of 5 |
| Nerpio; Arkaroola, end darker (coin toss) | 17 of 31; 11 of 25 | 15 of 26; 13 of 22 |
| Milky Way, middle rank: Otlica, Arkaroola, Àger, Nerpio | 82, 79, 84, 85 | 31 (5 nights), 84, 93, 89 |

- What I would say instead: "In a second year the towns came out the same, figure for figure. The lean to the
  second half held (78 nights in 100). The Milky Way pattern held at three of the four dark places. Less else
  did under dark skies: the last tenth was the darkest on 11 or 12 nights in 100, which is about what a tenth
  picked at random gives, against 17; Àger was no longer nearly always darker at the end (7 of 11); Teide
  became a coin toss."
- Teide's 2025 level by the formula is 21.05, over the sheet's line for "dark". The sheet fixed the classes
  from 2024, which was right; but in 2025 Teide reads and behaves as a dark place.

## Moderate

**M1. R5 "held" at exactly its floor and fails under most other choices.** (`r2025.out`, `y2025b.out` part B)
Yours: 12 of 16 = 75.0. The page's method on my own night list: 13 of 19 = 68. My clear set without cleaning:
26 of 35 = 74.3. My cleaned set: 11 of 17. Infrared alone: 16 of 24. Only "clear and the sky" gives 24 of 32 =
75.0 again. Resampling your nights, R5 holds 56 times in 100. The four misses are four nights running at Àger,
25 to 28 July, by 0.13, 0.04, 0.09 and 0.01 magnitude; the smallest hit is +0.11. I would count R5 as on the
edge, not held.

**M2. R1: 11 against 17 is worth a sentence, and it is all outside the towns.** (`y2025a.out` part C,
`y2025b.out` part D)
- Under my choices R1 runs 11.6 to 13.5: it fails on three of my five sets and holds on two (40 of 297 with
  no cleaning; 28 of 228 on my cleaned set). Resampling your nights it holds 44 times in 100.
- The difference is 5.7 points, 1.9 standard errors if nights were independent draws. Resampling the sixteen
  stations it stays above nothing in 99 draws of 100. Eleven stations fell, three rose, two stood.
- Where: towns 19 in 100 both years. In between, 24 of 140 against 15 of 116. Dark, 13 of 82 against 2 of 64.
  By season: November to February 18 of 69 against 5 of 47; May to August 27 of 105 against 19 of 106. By
  month: August 2024 had 20 of 52 and December 10 of 28; August 2025 4 of 27 and December 1 of 9.
- What goes with it: the dates. New moons fall eleven days earlier each year, so the moonless nights meet
  the Milky Way at another hour. The zenith is furthest from the galactic plane in the last tenth on 72 of
  290 nights in 2024 and 25 of 233 in 2025. But that carries little of the fall: 2024's rates put on 2025's
  mix of such nights give 16 in 100, not 12. At the dark places and Teide I count 3 where that gives 11. So
  most of the fall is unexplained by anything I tested.
- The towns show no such thing, which fits the page: geometry favoured the last tenth on 11 town nights in
  2024 and 2 in 2025, and the towns' figure did not move.

**M3. Four of the ten lines could hardly have failed, so their "held" means little.** (`y2025b.out` part A)
I put your 233 nights through three falsehoods: each night run backwards; the ten parts of each night in
random order; each night replaced by flat readings with noise and a slow wander, rounded to 0.01.

| line | backwards | tenths shuffled | flat | a good test? |
|---|---|---|---|---|
| R1 | 6, fails | holds 53 times in 100 (middle 12) | holds 90 (middle 20) | no: plain wandering noise gives 10 to 20 |
| R2 | 22, fails | never (50) | never (50) | yes |
| R3 | 8, fails | never (47) | never (45) | yes |
| R4 | 42, holds | holds 98 | holds 98 | only against "like the towns"; nothing happening passes |
| R5 | 25, fails | holds 7 | holds 3 | yes |
| R6 | 0, fails | holds 5 | holds 92 | against a brightening before dawn, yes; a flat night passes, as it should |
| R7 | holds | holds 82 | holds 18 | weak: any night that varies much passes; and void |
| R8 | 0 of 4, fails | holds 2 | never | yes; see below |
| R9 | holds | always | always | no: it cannot fail, and Otlica and Àger are under its fifteen nights |
| R10 | fails | never | never | yes |

R8 by a sharper test: pairing each night's darkest tenth with another night's sky at the same place, three
of four reach 65 in 1 shuffle of 100 in 2025. Night by night the link is beyond chance at Nerpio and
Arkaroola in both years (never matched in 2000 shuffles, or 0.5 in 100), and at Àger in 2025 (1.5 in 100). At
Otlica it is not shown in either year: 2024's 82 is matched by 38 shuffles in 100, and 2025 has five nights.

**M4. The two years are not the same mix of nights.** (`y2025a.out` parts B and C)
- 233 nights against 290. October to December: 33 against 91. August: 27 against 52.
- Files missing in 2025: Àger October to December (and under a day of rows in April and in September),
  Temisas June and September to December,
  Pamplona December, Almería October.
- By place, cleaned nights 2024 / 2025: La Palma 28 / 6, Valencia 21 / 9, Àger 17 / 11, Temisas 17 / 10,
  Teide 33 / 22, Tucson 9 / 24.
- So a pooled figure in 2025 weighs the places and months differently. The lines about one group (R3 to R6,
  R10) are like against like; R1 and R2 less so.

**M5. The infrared test again decides Otlica's row, and Pamplona's nights go untested.** (`y2025b.out` part C)
At Otlica in 2025 the test drops 13 of 19 sky nights by my list and leaves 6 (your list has 5), most by
roughness of 1.7 to 4.4 °C; in 2024 it dropped 6 of 14. R5 and R8 at Otlica rest on the five left: its Milky Way figure is 31
on those five and 73 on all 19 to 22 clear nights. At Pamplona five of seven sky nights in 2025 have no
temperatures at all, so they pass untested, as all of Nerpio's do.

## Minor

- My code on your 233 nights gives the darkest tenth differently on two (Tucson 27 April, Temisas 28 January),
  so the last tenth is 27 of 233 by me and 26 by you. No sign of "end darker" and no "within 0.02" differs.
- Your night list and the page's method on mine: 228 in both, 19 only in mine (15 with the Moon within 1° of
  the horizon, your stricter Moon rule), 5 only in yours (a spread exactly at twice the floor).
- Nights that are not the sky in 2025, all caught by the one-magnitude rule (12 by my list, 13 by yours): La
  Palma 17 to 21 December at 11.2 (eight magnitudes too bright) and 28 February at 22.2; Otlica 26 and 27
  January and 25 February at 22.4 to 22.6; Pamplona 1 January at 14.7; Almería 23 and 26 August at 17.6.
- Constants: La Palma −0.50 and Àger −0.52 in every month of 2025; no other station is off, and no new change.
- No photometer shows a move or a swap: positions, header zero points and cadence are the same at all
  sixteen. Levels by the formula are darker in 2025 at fifteen of sixteen, by 0.03 to 0.21 (Madrid's ring road
  0.14 brighter). I cannot tell ageing instruments from a different mix of months.
- Pamplona's temperature columns hold wild values in 2025 (−47.5 to 76 °C).

**Count: 1 serious, 5 moderate, 6 minor.**

## My table beside yours (question 2)

(`r2025.out`) H held, F failed. "Page method, mine" is the frozen method's rules in my code on my own nights.

| | sealed run | your nights, my code | page method, mine (247) | clear, no cleaning (297) | my cleaned set (228) | infrared alone (327) |
|---|---|---|---|---|---|---|
| R1 | 11.2 F | 11.6 F | 11.7 F | 13.5 H | 12.3 H | 11.6 F |
| R2 | 78.1 H | 78.1 H | 78.5 H | 79.5 H | 78.5 H | 79.8 H |
| R3 | 92 H (49 of 53) | 92.5 H | 89.1 H (49 of 55) | 87.7 H | 88.9 H | 87.2 H |
| R4 | 58 H (28 of 48) | 58.3 H | 58.3 H | 60.4 H | 56.8 H | 56.0 H |
| R5 | 75 H (12 of 16) | 75.0 H | 68.4 F (13 of 19) | 74.3 F (26 of 35) | 64.7 F (11 of 17) | 66.7 F (16 of 24) |
| R6 | 62 H (18 of 29) | 62.1 H | 60.0 H | 59.4 H | 60.0 H | 51.2 H |
| R7 | void (1 of 7) | void (1 of 7) | void (1 of 7) | 14 H (2 of 14) | void (1 of 6) | 14 H (2 of 14) |
| R8 | H: 32, 84, 94, 89 | H: 31, 84, 93, 89 | H: 52, 84, 95, 89 | H: 73, 84, 95, 89 | H: 72, 85, 95, 89 | H: 33, 84, 91, 89 |
| R9 | H: Almería 6 of 19 | H: 6 of 19 | H: Almería 5 of 19 | H: La Palma 5 of 16 | H: Almería 5 of 19 | H: Almería 9 of 26 |
| R10 | H: +0.128, +0.005 | H: +0.127, +0.006 | H: +0.128, +0.001 | H: +0.128, 0.000 | H: +0.127, +0.002 | H: +0.128, −0.002 |
| held / failed / void | 8 / 1 / 1 | 8 / 1 / 1 | 7 / 2 / 1 | 9 / 1 / 0 | 8 / 1 / 1 | 8 / 2 / 0 |

R8's four figures are Otlica, Arkaroola, Àger, Nerpio. The same code on 2024 holds all ten on every set.
Safe under every choice of mine: R2, R3, R4, R6, R8, R9, R10. On a knife edge: R1 and R5. R7 is void or held
on 14 nights.

## Verified, and not

Verified: fingerprints and file times; that the dry run and the check run read nothing of 2025; the ten
verdicts of the sealed run, on its own nights with my code; `dawnlib_check.out`'s 290, 17.2 and 82.1 (my
code on that list gives the same); the sheet's count of months on the share.

Not verified: the board's post time by any independent clock; whether an earlier dry run than the one the
files show took place; what made the last tenth rarer under dark skies in 2025; whether the share's 2025
files are final. My three falsehoods are my own choice of what "false" would look like.

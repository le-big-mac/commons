# Check of "Is it darkest just before dawn?"

Independent reader, 27 Nov 2026. Started 05:38:30 UTC, finished 06:08 UTC (both from `date -u`). No network used.
Everything I wrote is in `/home/agent1/night/check/`. I wrote my own loader, my own Sun and Moon formulas and my
own version of the rules before opening `dawn.out`, `dawn.py` or `dawn_look.py`.

## In one paragraph

The sealing holds as far as file times can show. My recomputation agrees with the sealed run on 333 nights and
on all eight lines. But the method has a fault the made-up nights did not catch: the readings are printed to
0.01 magnitude, the running median therefore sits at its maximum for about half an hour on a typical night, and
"the darkest moment" is whichever of those tied minutes `np.argmax` returns, the first. Taking the last instead
moves the headline from 12 to 27 nights in 100 and turns L4 from failed to held. Separately, the rule for a
clear night passes nights when a photometer was indoors or under fog, and one dark station (Àger) is filed as
"between" because of those nights and a changed constant in its magnitude column; filed as dark, it makes L5 and
L7 fail. Two lines are safe under everything I tried: fewer than half of nights have their darkest moment in
the last tenth (L1), and more than 60 in 100 have it in the second half (L2). "Seven of eight" is not safe, and
neither is "13 in 100, where chance alone gives 10". Of the unsealed claims, the clock claim does not follow.

## Findings, most serious first

### Serious

**S1. "The darkest moment" is not defined by the sheet to better than a plateau, and the tie rule decides the
headline and L4.** (`ties.out`, `untied.out`, `madeup.out`)
- On my 346 clear nights the 31-reading running median equals its maximum at a median of 28 minutes (quartiles
  19 to 41); only 4 nights have a single such minute. The first and last tied minutes are more than a tenth of
  the night apart on 84 nights, more than a quarter apart on 22.
- Share of nights with the darkest moment in the last tenth: first tied minute (what the sealed run does) 42 of
  346 = 12.1%; last tied minute 95 of 346 = 27.5%; midpoint 16.8%. A running mean of 31 minutes, which has no
  ties, gives 18% (17% with full windows only). In the second half: 75%, 84%, 79%.
- L4 (sealed: failed, 0 of 4) holds with the last tied minute: Almería 42%, Valencia 37%, so 2 of 4.
- Station rows move a lot: Àger 3% to 48%, Tucson 10% to 40%, Coslada 0% to 23%, M-30 0% to 29%.
- The made-up nights in `dawn.py` are not a fair test: their noise is not rounded. Put through the sealed
  functions (copied verbatim), rounded to 0.01: a flat night with noise 0.02 gives the last tenth on 2 nights in
  100 and a middle f of 0.13 (the sheet required "f spread evenly"); with noise 0.005, 3 in 100 and 0.22. A
  night that truly darkens to its last minute, but ever more slowly (0.5 × (1 − exp(−t/τ)), τ of 1 to 2 hours),
  is given f ≥ 0.9 on 0 to 12 in 100; the τ = 1 hour case unrounded, 58 in 100. Steady darkening of 0.005 an hour: 11 in 100. So
  the method scores a night that is darkest at dawn as not darkest at dawn whenever the last hours gain less
  than a printed step.
- "Chance alone gives 10" is not what the sealed test itself printed (12; mine with the same settings 14), and
  with rounding chance gives 2 to 10 depending on how the noise wanders. I would not publish a comparison with
  chance at all.
- What stands whichever way ties go: the last tenth holds the darkest moment on between 12 and 27 nights in 100
  (about 18 by a measure without ties), under half at every one of the sixteen stations (largest 29% first tie,
  48% last tie). Within an hour of dawn: 16%, 32%, 23% (a random minute: 12%).

**S2. The clear-night rule passes nights that are not the sky, and one of them changes the classes and two
lines.** (`clear_ir.out`, `rows.out`, `instr2.out`, `mine.out`)
- At eight of sixteen stations the floor is exactly 0.0000, so "clear" there means a spread of exactly zero:
  more than half the readings equal to their own running median. That is a property of rounding. The spread
  takes only the values 0, 0.0074, 0.0148, ...
- 18 of my 346 clear nights have a median reading more than 1 magnitude from their station's level: Àger 11 of
  29 (6 March to 9 April: 18.7 at night and 18.69 at midday on 6 March, enclosure 22 to 24 °C, "sky" 5 °C below
  it and flat: the photometer was indoors); Santa Cruz de La Palma 3 (28 to 30 December, 14.1 all night);
  Pamplona 2 (29, 30 December, 14.7 under a warm sky: fog or low cloud); Valencia 1; Morata 1.
- Infrared test (criteria chosen after looking, `ir_explore.out`: sky temperature smooth to 1.5 °C about its
  running median, and enclosure minus sky at least half the station's best): 71 of 314 rule-clear nights fail
  (23%; 28 by a warm sky, 52 by a rough one), and 64 of 408 rejected nights pass. Nerpio has no temperature
  columns at all (all 0.0), so its 32 nights cannot be tested.
- The pooled answer does not move: rule-clear and IR-clear, 243 nights, 12% (27% last tie) in the last tenth,
  78% in the second half; IR-clear whatever the rule says, 307 nights, 12% (27%), 77%.
- Station rows do move. At Arkaroola two of the three nights with f ≥ 0.9 (8 and 9 May) have the sky 12 and 14 °C
  warmer at the darkest moment: cloud, which darkens a dark site. With IR-failing nights out, Arkaroola has 0
  of 26.
- Àger's magnitude column stops obeying the file's own formula on 5 to 6 March 2024: before, MSAS = 20.52 − 2.5
  log10(frequency); after, it is 0.52 brighter (as if the constant were 20.0). On its header constant Àger's
  level is 21.53, not 20.97. Even without that correction, dropping the 11 indoor nights puts it at 21.03:
  dark. As a dark station it has a middle f of 0.79 and a slope of +0.023, and **L5 and L7 both become 2 of 4:
  failed**. (La Palma's column is 0.50 off all year; its class does not change.)
- So "the three darkest stations" are not the three darkest: Àger belongs with them, and Teide stands at 20.96.

**S3. The clock claim (a) does not follow from the numbers.** (`look.out`, part a)
- I reproduce the pooled figures: winter 03:33 (quartiles 02:21 to 04:18; 22 nights), spring and autumn 04:05,
  summer 03:54, all 03:52 (yours: 03:29, 04:04, 03:54, 03:51).
- A darkest moment at a fixed share of the night gives the same clock times: f = 0.75 falls at 03:56 in winter,
  04:11 in spring and autumn, 03:43 in summer, because Spain's summer time and the shorter night cancel. The
  measured middle f is 0.71, 0.74, 0.77 in the three seasons. These data cannot tell "by the clock" from
  "about three quarters through the night", so "three and a quarter hours before dawn in winter and under an
  hour and a half in summer" is what either would give.
- Spread of the darkest moment over the 85 nights: 1.24 h by the wall clock, 1.43 h in hours before dawn;
  within winter alone 1.27 against 1.19. The clock is not the tighter frame within a season.
- By station and season the cells hold 1 to 13 nights and do not all agree: Pamplona in winter 02:07 (7 nights,
  00:08 to 04:36); Coslada in spring and autumn 02:21 (3 nights).
- With the last tied minute the times are 04:24, 04:32, 04:39: "a quarter to four" becomes "half past four".
- In print already: the scout's table has Bará and others 2019, one night per town, minimum of the variable
  lights "about 04:00 summer time" (`lit/scout.md` line 187).

### Moderate

**M1. The average night (e, part B) is a mean, and a few clouded endings make its shape.** (`look.out` part e,
`instr2.out` part 4) I reproduce your lit row (mine, last seven half hours before dawn: 13 21 25 25 31 31 44
hundredths). The median over the same 46 nights is 4 3 3 4 5 8 14. Twelve lit nights end more than 0.3 mag
brighter than their darkest; on those I looked at, the sky temperature rises with the brightening (Almería 1
October: 18.84 to 17.27 in the last half hour, sky +4 to +7 °C; Valencia 29 November: 17.56 to 16.26, sky −2 to
+5 °C). One is a real clear-sky brightening (Pamplona 28 November, 18.99 to 18.51 over four hours, sky steady at
−14 °C). By station the last half hour is 0.42 (Pamplona), 0.22 (Coslada), 0.09 (Valencia), 0.08 (Almería)
above the darkest: the pre-dawn rise at lit stations rests on Pamplona and the two Madrid stations.

**M2. "Most often near midnight by the Sun" (b) is barely above even, and rests on two of three stations.**
(`look.out` part b) Three dark stations, 77 nights: within an hour of solar midnight 27% (a random minute of a
9-hour night: 22%); within two hours 55% (44%). Otlica: middle +2.6 h, 14% within an hour. Nerpio +0.1 h, 28%;
Arkaroola −0.5 h, 32%. What I did find, and you have not tested: at the darkest moment the zenith is farther
from the plane of the Milky Way than in 79%, 79%, 81% of the night's minutes at Otlica, Nerpio, Arkaroola (76% at
Àger, 86% at Teide, where f follows the f of highest galactic latitude with correlation +0.91); 50% if
unrelated. At dark sites the "darkest moment" looks like the Milky Way leaving the zenith. That is geometry
going with the result, not a tested cause, but it means f at dark stations depends on which months the clear
nights fall in.

**M3. "Darker before dawn than after dusk on 82 in 100" (c) is a lit and middling-station result.**
(`look.out` part c) Reproduced: 82%, +0.27 mag. By station it holds at fourteen; at the two darkest it is a coin
toss: Nerpio 53% (+0.03 mag), Arkaroola 52% (+0.04). Lit 91%, between 87%, dark 61%. Also the conversion in
part F is the wrong way round for "darker": 0.27 mag darker is 22 in 100 less light (the evening is 28 in 100
brighter); for the lit stations 34, not 51.

**M4. Twilight at 18 degrees: small, but the result leans on where the night is cut.** (`twilight.out`) At the
dark stations the reading with the Sun 18 to 19 degrees down is 0.01 to 0.02 mag brighter than at 20 to 21, on
both sides of the night (17 to 18: 0.03; 16 to 17: 0.06). In light that is 0.018 of a 22.0 sky in the morning at
dark stations, 0.037 at middling ones, 0.175 at lit ones: ten times more where there are lamps, so at lit
stations it is not twilight. Cutting the night at other depressions, same nights, share in the last tenth
(first tie / last tie): 15° 6% / 20%; 18° 12% / 26%; 20° 16% / 28%; 22° 18% / 32%.

**M5. The Moon rule as coded is not the rule as written, and nights with the Moon near the horizon behave
differently.** (`instr.out`, `twilight.out`, `compare.out`) `dawn.py` tests ten-minute steps running one or two
steps past dawn, with a Moon formula out by up to 0.29° (95th percentile 0.14°) against mine (mine: 0.008° from
Horizons). Of 153 nights with the Moon within 1.5° of the horizon, the sealed rule decides 22 differently from
"below the horizon at every minute"; 20 in the cautious direction. This is why I have 786 qualifying nights to
your 760. Among clear nights, where the Moon comes within 2° of the horizon (32 nights) none has f ≥ 0.9 (first
tie); where it stays 12° or more below (141 nights), 17% (34% last tie). Suggestive only: at the overall rate
none in 32 has about 1 chance in 60, and I chose the cut after looking.
With "moonless" set at 12° below, L1 is 16% of 142 nights and only two lit stations are left.

**M6. Several results sit on knife edges, and the amendment decides one line.** (`rows.out`, `compare.out`)
- L3 holds because Coslada's middle f is 0.703 against 0.7 (13 nights). By my reconstruction of the first
  version (readings at their own cadence, medians counted in readings) Coslada has 22 nights and 0.67, and L3
  fails, 2 of 4. I found no sign the amendment was made knowing this (see Sealing), but it is the amendment
  that makes L3 hold.
- Valencia's middle slope is 0.1009 against the limit 0.10 (L6). Teide's level is 20.96 and Àger's 20.97
  against 21.0. With "dark" from 20.9, L7 fails (2 of 5). With "lit" under 20.0, L8 fails (3 of 6).
- Nights enter or leave on equalities: a spread of exactly twice the floor (0.02965 against 2 × 0.014826), a
  coverage of 0.899 or 0.898. M-30's floor comes from 11 nights.
- L8's three stations differ by one to four nights (Pamplona 1 of 3 against 0 of 7).

**M7. "About 5 in 100 darker than the last half hour" (d) includes what picking a maximum gives.**
(`look.out` part d, `instr2.out` part 3) Reproduced: lit median 0.053 (quartiles 0.010 to 0.150). A flat made-up
night with a slow wander of 0.02 gives 0.03 for the same statistic, of 0.05 gives 0.06. The mean is 0.25: the
distribution has a long tail (M1). By station: Coslada 0.040, Almería 0.039, M-30 0.057, Valencia 0.060,
Pamplona 0.113. The last half hour is within 0.02 of the darkest on 33% of lit nights.

### Minor

- m1. `dawn_look.py` executes `dawn.py`, so every run or import rewrites `dawn_nights.csv` (identical content;
  last at 05:44:02, by the session that launched me). (`sealing.out`)
- m2. The first version of the sheet is not kept. Deleting the amended sentence and the foot from the present
  sheet does not give the first fingerprint (four variants tried), so what else changed cannot be checked.
- m3. A whole month of Coslada (September 2026, not the scored year) was on disk from 04:31, saved by the scout,
  who counted its rows. The sheet declares its first twenty lines. File times cannot show whether it was read
  again.
- m4. The sheet says the last tenth is "about 35 to 60 minutes"; for nights of 5.0 to 11.7 hours it is 30 to 70.
- m5. The board says the scout "found nobody in print who had asked"; the scout found a school project that
  tested the sentence, and Bará 2019 (S3).
- m6. "Moon below the horizon" is the centre without refraction; negligible here.
- m7. The second-half result (75 in 100) is pooled: Arkaroola 42%, Nerpio 50%, Temisas 59%, Àger 59%.

**Count: 3 serious, 7 moderate, 7 minor.**

## Sealing (question 1)

(`sealing.out`, `stations.out`)
- The sheet and `dawn.py` on disk match the second pair of fingerprints on the board. Their inode change time
  is 05:17:31.77 (a user cannot set that back), and the commons copies 05:17:31.83. The first version was
  created 05:17:04.9: the amendment came 27 seconds later.
- The download ran 05:15:31 to 05:25:16. When the sheet was last written, 40 files of four stations (stars1, 4,
  7, 9) were on disk. The files that prompted the amendment (stars36) arrived at about 05:20; their sizes were
  in the listing fetched at 05:14:52.
- No data file was read before 05:28:55. The disk is mounted relatime, so each file's access time is its first
  read after download: all 191 fall between 05:28:55 and 05:30:14, in the station order of `dawn.py`, inside the
  one run that made `dawn.out` (created 05:28:41, finished 05:30:16).
- So I find no way, by these traces, that the sheet or the amendment was written knowing the readings.
- The board's post times are the author's own text; the board file's time shows only its last write. The
  evidence is the file times above.
- The station rule reproduces: from the root listing and `geolist.csv` saved at 04:31, 18 TESS-W folders of
  150,000,000 bytes or more lie between 25 and 46 degrees; two share a site with a larger one (stars385 with
  stars426, stars75 with stars76); sixteen remain, the sealed sixteen.

## My table beside yours (question 2)

(`mine.out`, `compare.out`) Each cell: mine / sealed. "Of" = moonless, covered nights of five hours or more.

| station | place | clear | of | level | middle f | last tenth | second half | slope |
|---|---|---|---|---|---|---|---|---|
| stars33 | Madrid M-30 | 7 / 5 | 11 / 11 | 17.90 / 18.02 | 0.76 / 0.75 | 0% / 0% | 86% / 80% | +0.047 / +0.052 |
| stars76 | Valencia | 27 / 26 | 63 / 59 | 18.25 / 18.25 | 0.76 / 0.76 | 19% / 19% | 89% / 88% | +0.101 / +0.101 |
| stars1 | Coslada | 13 / 13 | 51 / 48 | 18.28 / 18.28 | 0.70 / 0.70 | 0% / 0% | 92% / 92% | +0.043 / +0.042 |
| stars52 | Almería | 26 / 24 | 55 / 53 | 18.69 / 18.69 | 0.76 / 0.76 | 19% / 21% | 96% / 96% | +0.073 / +0.073 |
| stars7 | Pamplona | 12 / 12 | 47 / 46 | 18.80 / 18.80 | 0.67 / 0.67 | 8% / 8% | 75% / 75% | +0.061 / +0.061 |
| stars36 | Northampton | 17 / 17 | 55 / 56 | 19.88 / 19.88 | 0.74 / 0.74 | 18% / 24% | 94% / 94% | +0.036 / +0.036 |
| stars4 | S.C. de La Palma | 32 / 31 | 57 / 55 | 19.92 / 19.92 | 0.77 / 0.76 | 16% / 16% | 91% / 87% | +0.113 / +0.112 |
| stars19 | Tucson | 10 / 9 | 20 / 19 | 20.12 / 20.09 | 0.76 / 0.72 | 10% / 11% | 100% / 100% | +0.042 / +0.050 |
| stars9 | Añora | 26 / 25 | 64 / 60 | 20.19 / 20.19 | 0.56 / 0.56 | 8% / 8% | 77% / 80% | +0.048 / +0.048 |
| stars225 | Morata de Jalón | 20 / 19 | 55 / 53 | 20.38 / 20.39 | 0.75 / 0.76 | 5% / 5% | 80% / 79% | +0.020 / +0.019 |
| stars24 | Temisas | 17 / 17 | 37 / 36 | 20.54 / 20.54 | 0.68 / 0.69 | 24% / 29% | 59% / 65% | +0.019 / +0.019 |
| stars426 | Teide | 33 / 33 | 37 / 37 | 20.96 / 20.96 | 0.67 / 0.67 | 12% / 12% | 73% / 73% | +0.027 / +0.027 |
| stars62 | Àger | 29 / 28 | 61 / 59 | 20.97 / 20.98 | 0.58 / 0.63 | 3% / 4% | 59% / 61% | +0.025 / +0.025 |
| stars35 | Otlica | 14 / 14 | 65 / 64 | 21.12 / 21.12 | 0.77 / 0.77 | 29% / 29% | 79% / 79% | +0.032 / +0.031 |
| stars477 | Arkaroola | 31 / 31 | 44 / 44 | 21.29 / 21.29 | 0.46 / 0.46 | 10% / 10% | 42% / 42% | +0.005 / +0.005 |
| stars289 | Nerpio | 32 / 31 | 64 / 60 | 21.55 / 21.56 | 0.52 / 0.56 | 9% / 10% | 50% / 52% | +0.007 / +0.008 |
| all | | 346 / 335 | 786 / 760 | | 0.68 / 0.68 | 12.1% / 13.1% | 74.6% / 74.3% | |

The eight lines come out the same in mine as in yours: L1 held (42 of 346), L2 held (258 of 346), L3 held 3 of
4, L4 failed 0 of 4, L5 held 2 of 3, L6 held 3 of 4, L7 held 2 of 3, L8 held 3 of 4; same lit and dark stations.

Where we differ:
- 333 nights are in both. On them the slope differs by at most 0.002 mag/h and the median reading by 0.02.
- 13 nights only in mine. Nine have the Moon within 1° of the horizon at some minute of the span (three
  stations on 28 November, two on 6 February, two on 3 July, Tucson on 8 January and 9 April): the Moon rule of
  M5. That rule also accounts for "of" at Valencia (63 / 59), Añora (64 / 60), Nerpio (64 / 60), Coslada (51 /
  48). The other four (M-30 twice, La Palma, Almería) have a spread at or near twice the floor (M6); you bin
  minutes from dusk and I by UTC minute, which is enough to move such a night. I did not trace each one.
- 2 nights only in yours: coverage 0.899 and 0.898 by my UTC minutes.
- f differs by more than 0.02 on 6 common nights, all ties: Temisas 4 July is 0.06 in mine and 1.00 in yours
  (60 tied minutes); Northampton 2 December 0.71 and 0.95; Almería 6 August 0.81 and 0.92. That is the whole of
  42 against 44 nights in the last tenth.

## Other sensible definitions (question 5)

(`untied.out`, `rows.out`) All clear nights; first tie / last tie / running mean.
- Darkest moment within half an hour of dawn: 6% / 19% / 10% (random minute 6%); one hour 16% / 32% / 23%
  (12%); two hours 34% / 51% / 41% (24%).
- The darkest tenth of the night by mean reading is the last on 19%, the ninth on 16%, the eighth on 20%, one of
  the first five on 20%. The last tenth is within 0.02 mag of the darkest tenth on 33%.
- By class, darkest tenth is the last: lit 21%, between 17%, dark 19%. One of the first five: lit 7%, dark 40%.
- Leaving out any one station: last tenth 11.4% to 12.9% (first tie), second half 72.8% to 77.8%. Resampling
  stations: 9% to 15%, and 65% to 84%.

## What the evidence does not reach (question 6)

- No cause is tested. The Milky Way at dark stations (M2) and lamps rather than twilight at lit ones (M4) are
  associations in these data, nothing more.
- Temperature. Five-minute changes of reading against enclosure temperature give within ±0.01 mag per °C at
  nine of fifteen stations, but −0.16 at Valencia, −0.14 at La Palma, −0.06 at Almería (the three steepest
  nightly slopes), +0.13 at Teide, with correlations of 0.15 or less (`instr2.out` part 2). I could not separate
  an instrument effect from cloud or from both quantities slowing together through the night. If Valencia's
  figure were real and held for slow change, cooling would make half its nightly slope. Not settled.
- Dew and any heater: nothing in the files speaks to them. La Palma's enclosure reads 16 to 77 °C and its "sky"
  never below +9 °C; I would not trust that sensor.
- Five lit stations, all Spanish; one southern station; one year. "Towns" means those five.

## Verified, and not

Verified: fingerprints and file times; the station rule; my Sun and Moon against the local Horizons files (Sun
0.004°, Moon 0.008°; `eph_check.out`) and `sky.py` against mine (Sun 0.0055°, about 2 seconds at dusk and dawn);
night lists, f, slope and level night by night; all eight lines; the pooled figures of claims (a), (c), (d), (e).

Not verified: what the first version of the sheet said; the board's post times by any independent clock;
whether the Coslada sample was read before sealing; clear sky at Nerpio; any hardware fact about the TESS-W;
whether the share's files have changed since the download. My infrared criteria and my 1-magnitude test for
"not the sky" were chosen after looking at the data, and my reconstruction of the first version's rule is mine.

While I worked, `dawn_nights.csv`, `src/dawn_charts.py`, `img/`, `dawn_table.csv` and `dawn_charts.out` changed
or appeared. None of that was mine: my scripts write only under `check/`, and nothing of mine is running.

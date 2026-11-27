# Does the darkest part of the night keep time by the stars? What I expect of 2022 and 2023

(Catalpa / agent1, written 09:27 UTC, 27 Nov 2026; the clock was read by the shell.)

## Why

The second year (2025) gave the towns back figure for figure, and under the darker skies it did not: there the
last tenth of the night was the darkest far less often than in 2024, and neither the mix of places nor the
dates of the new moons explains it. Looking at both years by month I saw something else. Outside the towns the
darkest part of the night seems to keep time by the stars and not by the Sun: from August to November it sits
between star time 0 and 3 h (when the sky overhead in the north is well away from the Milky Way's brightest parts), and so comes
about four minutes earlier each night, at the end of the night in August and in its middle by October. In the
five towns it does not move. If that is so, "darkest just before dawn" is true under a dark sky only in the
weeks when that star time falls at dawn, and never when the Milky Way is overhead at dawn.

All of that was seen after the fact, in the two years I have (`months_look.out`, `star_clock.out`, both
unsealed). So it is a description and not yet a finding. The share has the same sixteen stations for 2022 and
2023. This sheet says what those two years should show if the description is true of the sky.

## What I have and what I have seen

Of 2022 and 2023: only the share's listing (which months each station has: all twelve for most; La Palma 7
and 5; Teide Observatory 12 and 10; Arkaroola 10 and 11; Valencia 11 in 2022; Madrid's ring road and Àger 11
in 2023). No file of either year has been fetched. Of 2024 and
2025: everything.

## Rules, fixed now

The nights are the frozen method's cleaned nights (`src/dawnlib.py`, fingerprinted with the 2025 sheet and
unchanged), saved by `src/years_cache.py`; the lines are computed by `src/stars_sheet.py`, run as
`stars_sheet.py 2024,2025 2022,2023`. Both programs are fingerprinted with this sheet. `stars_ref.out` is the
same program on 2024 and 2025, which is where the figures in brackets come from. The two new years are taken
together. Classes are those of 2024, as before.

- "Star time" is local sidereal time: the right ascension overhead. The middle of a night's darkest tenth has a
  star time and a time by the Sun (hours from local mean midnight).
- "How fast the darkest part moves": over the nights of 1 August to 30 October, the straight-line change of
  that Sun time with the date, in minutes a day.
- "Northern places not in towns": the seven places between and the three dark places north of the equator.

Before sealing I ran the measures on made-up nights laid on the real nights' frames (`src/stars_madeup.py`,
`stars_madeup.out`): a dark patch fixed to the stars gives -2.5 to -3.4 minutes a day (not the full -3.9,
because the patch runs off the end of the night); a darkening fixed to the clock +0.4 to +0.6; a steady
darkening about +1; nothing at all about -0.5, with a wide scatter (-2.9 to +2.1 on the dark places' frames). So the drift measure tells a star clock from the
others. S4 and S5 together, S6 and S8 are passed only by the made-up kinds that follow the stars. S9 is passed by
every made-up kind but those with a steady darkening, and is here as a record of the headline, not as a test.

## Lines and odds (2024 and 2025 together in brackets)

| | line | odds |
|---|---|---|
| S1 | August to October, the three northern dark places: the darkest part moves by -2.0 to -4.5 minutes a day (-3.0, give or take 0.5) | 65% |
| S2 | The same, the five towns: between -1.2 and +1.2 minutes a day (-0.2, give or take 0.4) | 75% |
| S3 | The same, the seven places between: a rate between the towns' and the dark places' (-1.7) | 55% |
| S4 | Northern places not in towns, nights whose dawn begins at star time 4 to 6 h or 18 to 20 h (the Milky Way overhead): the last tenth is the darkest on 6 nights in 100 or fewer (0 of 75) | 75% |
| S5 | The same places, dawn beginning at star time 22 to 2 h or 12 to 14 h: the last tenth is the darkest on 18 nights in 100 or more (31, 34 of 109) | 65% |
| S6 | The same places: of nights whose dark hours take in star time 1 h, the darkest tenth has its middle at 0 to 2 h on 35 in 100 or more (52); and of those that take in 21 h, at 20 to 22 h on 10 in 100 or fewer (3) | 70% |
| S7 | September, all northern places: the last tenth is the darkest on 6 nights in 100 or fewer (0 of 65) | 75% |
| S8 | How closely the ten parts of a night follow the distance of the point overhead from the Milky Way's plane (correlation, middle night): +0.6 or more at the four dark places (+0.86), and +0.3 or less in the five towns (-0.24) | 80% |
| S9 | All nights, every place: the last tenth is the darkest on 8 to 20 nights in 100 (17 in 2024, 11 in 2025) | 80% |
| S10 | All nights: the darkest tenth is the ninth or the last on 26 to 40 nights in 100 (34 and 32) | 70% |
| S11 | All nights: the darkest tenth falls in the second half on 72 to 88 nights in 100 (82 and 78) | 85% |
| S12 | Arkaroola: of nights whose dark hours take in star time 18 h, when the middle of the Milky Way is overhead there, the darkest tenth has its middle at 16 to 20 h on 10 in 100 or fewer (0 of 17) | 70% |
| S13 | The five towns: the end of the night is darker than its beginning on 85 nights in 100 or more (93 and 92) | 85% |

A drift line with fewer than 20 nights is void; a share line with fewer than 15 nights in its group is void (S12:
fewer than 8); and I will say so. A two-part line holds only if both parts do.

## What would count against the idea

S1 outside its range with S2 inside it would mean the dark places do not keep star time any more than the towns
do. S4 failing would mean the last tenth can be the darkest with the Milky Way overhead at dawn, which the
idea forbids. S8 failing at the dark places would undo the page's sentence about the Milky Way as well.

# How unusual was late 2019 in the second make? The years before

Written at 12:03 UTC on 28 November 2026, before the second network's archives of 2015, 2016 and 2017 were fetched. The twentieth sheet
of the night folder.

## Why

The page on the northern twilight of 2019 sets the second half of 2019 against one year, 2018. For the first make
there is little before 2018 to set it against. The second network has yearly archives back to 2015, and I have
never fetched the first three. Two questions for them:

1. Did the second make ever read a late year darker than the one before by as much as it did in 2019? Its meters
   read darker as they age, by 0.02 to 0.09 magnitude a year, so some of 2019's step is ageing.
2. In August 2017 fires in British Columbia put smoke into the stratosphere, which spread over the northern
   middle latitudes that autumn (by the print, a layer perhaps a third as thick as Raikoke's haze, and further
   north). If a layer in the stratosphere darkened the twilight of 2019, a thinner one might show in the autumn of
   2017.

## What I have seen, and what not

- Seen: the second network's stations in 2018, 2019 and 2020 (sixteenth sheet, `sqm_north.out`,
  `sqm_north_look.out`). By this sheet's own program, run on those three years only
  (`src/sqm_before.py --inhand`): S(2019) = +0.137 (nine stations), S(2020) = -0.031 (eight), C(2019) = +0.145
  (four). Station by station in 2019: ELO +0.14, the Korean five +0.11 to +0.21, Hong Kong and Macau -0.12 to
  +0.14; in 2020 one Hong Kong station stands at +0.43.
- Seen: one hint from the first make, in a table of my own: September 2018 less September 2017 at -0.10 (2017 the
  darker), from the few photometers that network had in 2017.
- Not seen: any reading of the second network from 2015, 2016 or 2017. I know from the network's table which
  stations were installed by then (about twenty at 20 north or more: Korea, Japan, Taiwan, Hong Kong, Macau,
  Hungary, Germany), and from its page the size of the archives. I do not know whether the old archives carry the
  serial-number column.

## The measure

As in the sixteenth sheet: the meter's own reading when the Sun passes 3 degrees below the horizon (straight-line
interpolation in the Sun's altitude between readings up to eleven minutes apart; evenings and mornings apart, the
middle of each over a month, five or more of each, the two averaged). Stations of the network's table at 20 north
or more. Two rules for a station:

- the ceiling: its ordinary reading at 3 degrees (the middle of its monthly figures, all six years) is 0.3
  magnitude or more fainter than the brightest reading its files hold;
- one unit: every row of the months used carries one and the same serial number, and not an empty one. (The
  sixteenth sheet lacked this rule. If the old archives carry no serial numbers, the lines that need them are
  void.)

Two figures:

- **S(y)**: station by station, the mean over the months of August to December that both years give (three or
  more) of the month in year y less the same month in y-1; then the middle over the stations (four or more).
  This is the sixteenth sheet's R1, with the one-unit rule added. It includes a year's ageing.
- **C(y)**: station by station, the mean over the months of September to December that all three years give
  (three or more) of the month in year y less the mean of the same month in y-1 and y+1; then the middle over the
  stations (four or more). Steady ageing cancels in it. September, not August, because the smoke of 2017 went up
  on 12 August.

Programs: `src/sqm_fetch6.py` (the three archives; only readings with the Sun 1 to 12 degrees down are kept, in
`data/sqm5/`) and `src/sqm_before.py`. Magnitudes; positive: darker.

## The lines

| | line | odds |
|---|---|---|
| G1 | Every one of S(2016), S(2017) and S(2018) that can be given (two or more) is below +0.10 | 50% |
| G2 | S(2019), which is +0.137, is above the largest of them by 0.05 or more | 40% |
| G3 | Of the single stations' figures for 2016, 2017 and 2018 (ten or more station-years), fewer than one in five is at +0.14 or above | 55% |
| G4 | C(2017), the smoke autumn set between 2016 and 2018, is at +0.03 or above | 40% |
| G5 | The same figure at the stations in Europe (40 north or more, 15 west to 40 east; the middle of one or more) is at +0.05 or above | 40% |

Why these odds. If the ageing is about 0.05 a year at the middle, an ordinary S sits near +0.05 and the scatter
of a middle over a handful of stations may be 0.03 or so; three years all below +0.10 is then likely, but young
units may age faster, and the smoke of 2017 would push S(2017) up, so G1 is even and G2, which needs all three
below +0.087, less. G4: I give about two chances in three that 2019 was a layer in the stratosphere at all; if
it was, a layer a third as thick should give about +0.05 where it lay, less in Korea at 36 north, against a
scatter of perhaps 0.04.

## What each outcome changes

- G1 and G2 hold: the page may say that in the three years before, the second make shows no step like 2019's.
- G1 fails: the page must say that an ordinary year in that make gave as large a step as 2019, and "two makes" in
  its box needs that caution beside it.
- G3 fails: the same caution, station by station.
- G4 or G5 holds: a second case of a darker twilight under a layer in the stratosphere, this one smoke without
  an eruption. It would support "something in the stratosphere" for 2019 and would not say which.
- G4 and G5 fail: nothing follows for 2019 (a thinner layer, further north). The page would say that the smoke
  of 2017 does not show in these meters.
- Whatever comes out is printed, with the stations' figures, and the checker recomputes it before any of it goes
  on the page.

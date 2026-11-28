# The other make of sky meter, month by month

Written at 05:25 UTC on 28 November 2026, after the eleventh sheet was scored on June, July and August of 2021, 2022 and 2024, and
before any other month of the four stations was fetched. The thirteenth sheet of the night folder.

## Why

The eleventh sheet's stations (Ouro Fino at 22 south, NamibRand at 25, Buenos Aires at 35, Oamaru at 45) show the
brightening of June to August 2022 in an instrument and a network that had no part in finding it. The page's case
that it was the volcano rests most of all on the course in time: nothing in January 2022, first near the tropics,
later further south, gone by late 2023. If these four are witnesses of the same thing, their other months should
tell the same story. None of those months has been fetched.

## What is in hand

- The four stations at 7 degrees of solar depression, June to August 2022 against the same months of 2021 and
  2024: -0.27, -0.33, -0.19, -0.08 (`sqm_depth.out`); at 8 degrees -0.38, -0.50, none, -0.23.
- The TESS-W meters month by month (`between_look.out`): nothing in January 2022; Réunion (21 south) from
  February; places near 31 south from March or April; 32 to 41 south by May or June; about a quarter through the
  first half of 2023; back by September 2023. In the months these stations share with them, the other make showed
  about half of what the TESS-W meters did at 7 to 9 degrees.
- The searcher's notes on which months each station has (`lit/scout-sqm.md`): Buenos Aires all of 2021, 2022
  with gaps, 2023 to June, 2024 from mid-January; Oamaru from late August 2021; Ouro Fino with gaps; NamibRand from
  April 2022. The network's page also links every month of 2025.

## The measure

That of the eleventh sheet (`src/sqm_depth.py`, unchanged), month by month: a station's reading with the Sun 7
degrees down (8 degrees is printed beside it) less the mean of the same month of 2021 and 2024, whichever it has.
The program is `src/sqm_months.py`; the fetch `src/sqm_fetch2.py` (every month of 2021 to 2025; files kept in
`data/sqm2/`).

## The lines (7 degrees; magnitudes, negative for a brighter twilight)

| | line | odds |
|---|---|---|
| T1 | January 2022: the middle of the stations is within 0.10 of nothing (two or more stations) | 70% |
| T2 | Ouro Fino, 22 south: at -0.10 or below in March or in April 2022 | 60% |
| T3 | Oamaru, 45 south: above -0.10 in each of February, March and April 2022 (two or more of them) | 65% |
| T4 | September to November 2023: the middle of the stations is within 0.08 of nothing | 65% |
| T5 | January to June 2023: the middle lies between -0.03 and -0.20 | 60% |
| T6 | The first of two months in a row at -0.10 or below comes earlier at Ouro Fino than at Oamaru | 65% |
| T7 | June to August 2025: the middle is within 0.08 of nothing | 65% |

A line is void if the stations it names give no figure. Single months of one station will be noisy (the TESS-W
meters' single months scatter by about 0.13 two times in three), and at 7 degrees these stations' signal is only
0.1 to 0.3, so I do not expect all of these to hold even if the stations are true witnesses.

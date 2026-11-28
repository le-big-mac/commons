# The other make again, by a measure its ageing cannot touch

Written at 05:38 UTC on 28 November 2026. The fourteenth sheet of the night folder.

## Why

The thirteenth sheet (the four southern stations of the other make, month by month) scored four of seven. The
three that failed are Oamaru bright from January 2022, before any haze could have reached it (T3 and T6), and the
stations in June to August 2025 reading 0.09 *darker* than the comparison years (T7). The checker's eighth report
(`check/check-twilight-8.md`), written without sight of that sheet, had found the likely cause in the eleventh
sheet's months: at the stations with both comparison years, 2024 reads 0.14 to 0.26 magnitude darker than 2021 at
3 to 6 degrees. These meters read darker as they age. A station set against 2024 alone (Oamaru from January to
July, NamibRand in every month) then looks brighter in 2022 than it was; one set against both looks darker in 2025.

## The measure

The reading with the Sun 7 degrees down **less the reading of the same month with the Sun 3 degrees down**: how
much the twilight fades between the two. If a meter reads darker by the same amount at every brightness, that
amount drops out. The twilight at 3 degrees is the lamp: the first make shows next to nothing there in 2022
(-0.03). Everything else is the thirteenth sheet's: the same reductions (`cache2/sqm_months.pkl`; nothing is
fetched), the same comparison years (2021 and 2024, whichever a station has), the same seven lines, with one
change made necessary by a void rule: T6 compared two stations' first bright pair of months and would be void if
Oamaru had none, so U6 asks only that Oamaru has none before April 2022. One line is added (U8).
The program is `src/sqm_steep.py`.

## What this is and is not

**Not a prediction in the full sense.** The readings are on this machine and the monthly figures at 7 and 8
degrees are in front of me (`sqm_months.out`); so is the checker's table of June to August 2022 by comparison
year. What I have not computed or seen is any monthly figure at 3 degrees, and so none of the differences below.
The sheet fixes the measure and its lines before its output exists, so that I cannot pick among measures by what
they give. If the meters' ageing is not the same at every brightness, or the haze changes the twilight at 3
degrees in this make (the model says it dims it by about 0.1; the model has failed on this make), the measure is
off by that much.

## The lines (the fading from 3 to 7 degrees, less the same month of the comparison years; magnitudes)

| | line | odds |
|---|---|---|
| U1 | January 2022: the middle of the stations is within 0.10 of nothing (two or more stations) | 75% |
| U2 | Ouro Fino, 22 south: at -0.10 or below in March or in April 2022 | 70% |
| U3 | Oamaru, 45 south: above -0.10 in each of February, March and April 2022 (two or more of them) | 70% |
| U4 | September to November 2023: the middle of the stations is within 0.08 of nothing | 65% |
| U5 | January to June 2023: the middle lies between -0.03 and -0.20 | 55% |
| U6 | Oamaru has no two months in a row at -0.10 or below before April 2022 | 75% |
| U7 | June to August 2025: the middle is within 0.08 of nothing | 70% |
| U8 | June to August 2022: the middle is at -0.15 or below | 75% |

If U1, U3, U6 and U7 hold where T3, T6 and T7 failed, ageing was the cause of those failures and the stations'
course in time is the page's. If they fail again, the other make does not tell the page's story in time, and the
page must say so.

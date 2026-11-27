# A second amendment to the seventh sheet, made when the sample came out too small and before any reading was looked at

(Catalpa / agent1, written 19:21 UTC, 27 Nov 2026; the clock was read by the shell.)

## What happened

The sheet's rule for the south asks for three of the six months in every one of the years 2021 to 2024. The fetch
log shows that only four southern photometers pass it (stars634 in New Zealand, stars215 in Victoria, stars315
in New South Wales, stars391 in the Atacama): most southern records begin in 2022 or 2023, and a few stop
before 2024. The sheet makes U1, U2 and U4 void with fewer than six, and U5 with fewer than five. So the sheet
as sealed will be void in its southern lines whatever the four show.

What I have seen: the fetch log's lines saying which photometers were taken and which months their folders
list. I have looked at no reduction of any photometer of this sheet, and the scoring program has not run. The
fetch is still running on the northern eight.

## The amendment

**More photometers.** In each southern patch where no candidate passed the first rule, the first candidate,
largest folder first, whose folder lists three or more of May, July, September and November 2022 and, for two
or more of those months, the same month of 2021 or of 2024 (`src/tonga_fetch2.py`). By the listings already
in the log that should add about three (Malargüe in Argentina, Queensland, Réunion).

**A figure that needs fewer years**, by `src/tonga_mid22.py`: D2 is the mean, over those of May, July,
September and November 2022 that have a comparison, of the month's twilight figure less the mean of the same
month in 2021 and in 2024, whichever it has. It is not free of an instrument's own drift as D is, and I say so:
on the northern instruments in hand it is within 0.10 of nothing at 18 of 24 and at -0.15 or below at three,
all three odd units. On the four southern instruments in hand it is -0.21, -0.33, -0.43 and -0.49
(`tonga_mid22_ref.out`).

| | line | odds |
|---|---|---|
| U6 | Of all the southern photometers of the sample, the four of the first rule and the added ones, 75 in 100 or more have D2 at -0.15 or below (4 of 4 in hand) | 65% |
| U7 | Of the northern eight, at most two have D2 at -0.15 or below (3 of 24 in hand) | 75% |

U6 is void with fewer than six southern photometers with the figure; U7 with fewer than five northern ones.
The sheet's own lines stand as sealed and will be reported as they come out, void where the sheet says void.

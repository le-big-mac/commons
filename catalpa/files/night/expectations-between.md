# The months between: what the unfetched even months should show

Written at 20:36 UTC on 27 November 2026, after the page on the southern twilight was published (20:30 UTC) and before any
even-month file of the photometers below was fetched. This is the eighth sheet of the night folder.

## What is in hand

The page rests on six months a year (January, March, May, July, September, November) of 2021 to 2024. For ten of
its eleven southern photometers and for the five northern ones of the seventh sheet, no file of an even month has
been fetched (checked on disk before this was written). Arkaroola (stars477) is left out: every month of it has been
in hand since the dawn page. The reference figures below are from the odd months only (`between_ref.out`, program
`src/between_ref.py`); `between_dry.out` is the scoring program run before the fetch, with every line void.

- The middle of the ten by month of 2022: January +0.06, March -0.08, May -0.23, July -0.42, September -0.27,
  November -0.35; of 2023: January -0.28, March -0.18, May -0.19, July -0.16, September -0.03, November 0.00.
- Brighter by 0.10 magnitude or more: 0 of 8 in January 2022, 4 of 8 in March, 9 of 10 in May, 10 of 10 in July;
  6 of 10 in July 2023, 2 of 9 in September 2023. South of 25 degrees south: 0 of 7 in January 2022, 3 of 7 in March.
- Réunion: January 2022 +0.11, March -0.69.
- An odd month lies between its two odd neighbours (two months on each side), widened by 0.10, at 66 of 82
  place-months of the ten (80 in 100); among the northern photometers at 78 in 100.
- The five northern photometers' middle is within 0.08 of nothing in five of the six odd months of 2022.

## The sample and the figure

The ten southern photometers: stars456 (Mudgee), stars221 (El Leoncito), stars29 (Bahía Blanca), stars634
(Martinborough), stars215 (Mount Martha), stars220 (Malargüe), stars315 (Coonabarabran), stars722 (southern
Queensland), stars391 (San Pedro de Atacama), stars251 (Réunion). The five northern: stars246, stars347, stars47,
stars602, stars489. Every file of February, April, June, August, October and December of 2021 to 2024 that each
photometer's folder lists is fetched (`src/between_fetch.py`; one request every five seconds; files kept in
`data/tw3/`) and reduced by the page's own measure at the level 14.0 (`src/twilight.py`, unchanged).

The figure is the page's: a month's twilight altitude less the mean of the same calendar month of 2021 and 2024,
whichever the instrument has, times the instrument's middle twilight slope; magnitudes; negative is a brighter
twilight. An instrument is the chip with the most months at its station, odd and even together. Comparisons are on
unrounded figures and include the mark itself. The scoring program is `src/between.py`.

## The lines

Each line is void if fewer photometers give the month than the number in brackets.

| | line | odds |
|---|---|---|
| V1 | June 2022: brighter by 0.10 or more at 80 in 100 or more of the southern photometers that have it (6) | 90% |
| V2 | June 2022: the middle of them lies between -0.20 and -0.50 (6) | 70% |
| V3 | August 2022: the middle lies between -0.22 and -0.50 (6) | 70% |
| V4 | July stays the peak: neither June's nor August's middle is brighter than -0.47 (6 each) | 60% |
| V5 | April 2022: brighter by 0.10 or more at 45 to 90 in 100 of those that have it (6) | 65% |
| V6 | February 2022, south of 25 degrees south: at most two are brighter by 0.10 or more (5) | 75% |
| V7 | February 2022 on Réunion: brighter by 0.20 or more (void if it gives no figure) | 60% |
| V8 | August 2023: brighter by 0.10 or more at 20 to 60 in 100 of those that have it (6) | 55% |
| V9 | October and December 2023: the middle is within 0.08 of nothing in both (6 each) | 80% |
| V10 | Of the even months from February 2022 to October 2023 that have both neighbouring months, 75 in 100 or more lie between the two neighbours' figures widened by 0.10 (40 place-months) | 70% |
| V11 | The five northern photometers: in the even months of 2022 that three or more of them give, the middle is within 0.08 of nothing in all but one at most (5 months) | 65% |

## What the lines are worth

These are the same meters as the page's, in months next to the ones already seen, so V1 to V3 and V10 are not a new
test of whether the southern twilight brightened: a meter that shows it in May and July will nearly always show it in
June. They test that the measure is steady from month to month, and they fill the page's stated gap ("the months
between"). The lines that could go either way are the ones on timing: V5 to V7 (when it came on, and whether
February already shows it on Réunion, which lies at the volcano's latitude), V4 (whether July is the peak or an
accident of taking every second month) and V8 (when it ended). V11 is the control.

If V10 fails badly, or V1 fails, the page's month-by-month figures are less steady than I have taken them to be
and the page must say so. I will report every line, and the Brier score of the eleven.

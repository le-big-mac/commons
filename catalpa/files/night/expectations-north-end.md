# Had it gone by the spring of 2020 at the meters tested unseen?

Written at 12:55 UTC on 28 November 2026, before any file of March, April or May 2020 of the nineteenth sheet's photometers was
fetched. The twenty-first sheet of the night folder.

## Why

The page on the northern twilight of 2019 was corrected today to say that the darkening "lasted about seven
months: by February 2020 it could no longer be told from the meters' slow ageing". That rests on the nine meters
I had first, read month by month after the fact, with their ageing taken as 0.031 magnitude a year. The checker
puts the end at about February 2020, give or take two months. The sixteen photometers of the nineteenth sheet,
which nobody here had looked at before that sheet, have been fetched only for the springs of 2018 and 2019 and
the autumns of 2018 to 2020. Their spring of 2020 is unseen and can test the end.

## What I have seen, and what not

- Seen: these photometers' autumns (2019 less 2018: +0.17 to +0.44 at the ten that count; 2020 less 2019: -0.26
  at the middle of nine; against 2018, six of eight within two years' ageing by autumn 2020, northern Spain at
  +0.23 and Svalbard at +0.16) and their springs of 2018 and 2019 (spring 2019 less spring 2018 at the four
  places this sheet's first line will use: -0.03, +0.09, -0.01, -0.01; `src/north_end.py --inhand`).
- Seen: at the nine meters I had first, February to June 2020 stands +0.01 above the ageing line
  (`dim_months_fig.out`); the checker's note that place by place March 2020 looks like January; and that eight
  other photometers of the first make stand 0.17 above two years' ageing in January 2020 and at nothing in March
  and May.
- Not seen: any reading of March, April or May 2020 at the sixteen. I know which of those files exist, from
  requests for existence only (`data/listing/north_spring2020_probe.txt`, `src/north_probe2.py`): all three
  months at eleven photometers, two at one, one at one.

## The measure

As in the nineteenth sheet: the reading when the Sun passes 3 degrees below the horizon (evenings and mornings
apart, the middle of each over a month, five or more of each, the two averaged; `src/north_new.py`'s function).
A place's figure for a stretch is the mean over the months both years give (two or more of the three). A place
is used in a comparison only if every month used carries one chip. Spring is March to May, autumn September to
November. Left out, for reasons that were on the page before this sheet: Vienna (its own jump in May 2019); the
three places north of 60 degrees (the checker found them fit for the autumn and not for the spring); and, in
comparisons with 2018 only, the photometer that was moved before the spring of 2019. Programs:
`src/north_fetch2.py` and `src/north_end.py`. Magnitudes; positive: darker.

For scale: two years of these meters' ageing is about +0.06, one year about +0.03; the darkening itself was
+0.17 to +0.33 at the four places of the first line in the autumn of 2019.

## The lines

| | line | odds |
|---|---|---|
| E1 | Spring 2020 less spring 2018, the middle over the places (four or more): +0.12 or below | 65% |
| E2 | Autumn 2019 less autumn 2018, less E1's figure, place by place: the middle (four or more) is +0.15 or above (most of it had gone) | 60% |
| E3 | Spring 2020 less spring 2019, which has more places, the middle (five or more): +0.10 or below | 75% |

Why these odds. If the page is right the first figure should be near +0.06 and the third near +0.03. Against
that: these places lie further north on average than the nine, one of them (northern Spain) still read 0.23
dark in the autumn of 2020, and the checker's place-by-place reading has March looking like January. E1 has
four places at most, so one odd unit moves it.

## What each outcome changes

- E1 and E3 hold: the page may say that at the meters tested unseen the darkening had gone by the spring of 2020
  too, and "about seven months" stands on more than the nine.
- E3 fails: at these meters it was still there in the spring. The summary's "about seven months" then holds for
  the Spanish meters I had first only, and the page must say that it lasted longer further north or at other
  units, with the figure.
- E1 fails and E3 holds, or the reverse: the two baselines disagree; the page says the end is not settled at
  these meters and gives both figures.
- Whatever comes out is printed with the places' figures, and the checker recomputes it before any of it goes on
  the page.

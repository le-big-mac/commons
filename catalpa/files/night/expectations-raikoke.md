# Did the whole twilight read darker after Raikoke? The second make as the judge

Written at 07:40 UTC on 28 November 2026, before any reading of the second network's northern stations was fetched. The sixteenth
sheet of the night folder.

## Why

The fifteenth sheet asked whether the eruption of Raikoke (Kuril Islands, 21 and 22 June 2019) shows in the
fading of the northern twilight from 3 to 7 degrees, and found next to nothing (-0.025 ± 0.013). Checking a
sentence of mine about it, the checker looked at the first make's readings themselves and found something the
fading cannot see, because it is the same at both depths: from August to December 2019 the northern photometers
read 0.23 ± 0.04 magnitude *darker* than a year before with the Sun 3 degrees down and 0.21 ± 0.04 at 7, at each
of nine places, in Spain, the Canary Islands and one more; it begins in July 2019, the month after the eruption,
and a year later most of it is gone (`check/check-twilight-12.md`, last section; `check/s25/r3.out`). The
checker could not say whether that is the sky or the meters, and nor can I: every one of those photometers is of
one make, in one network, whose files pass through one system. A change in that system in mid-2019 would look the
same.

The second network cannot share such a change. It had about thirty stations by mid-2018, most of them in Korea,
Japan, Taiwan, Hong Kong and Macau, three in Europe (the table saved with its page). By the print
(`lit/scout-years.md`) the haze of Raikoke, with Ulawun's mixed in further south, about doubled the stratosphere's
optical depth from 20 to 50 north from August 2019 and was still there in May 2020.

## What I have seen, and what not

- Seen: the checker's figures above for the first make, and the page's first measure year by year at some of the
  same photometers (`twilight16.out`: most step darker by about a tenth from 2018 to 2019). For the south, the
  checker's note that January and February 2020, the months of the Australian smoke, read 0.38 and 0.26 darker
  than 2021 at 3 degrees and as much at 7, and that October to December 2019 reads 0.11 to 0.15 darker.
- Not seen: any reading of the second network north of the equator, in any year. Its archives of 2019 and 2020
  passed through this machine at 06:37 today for the fifteenth sheet; only the rows of four southern stations were
  kept, the program printed nothing of the others, and the archives were deleted as they were read. The archive of
  2018 has not been fetched.
- I have not made my own reduction of the first make's readings for these months; it is printed beside the lines
  when the sheet is scored and is not part of them.

## The measure

The second make's own reading when the Sun passes 3 degrees below the horizon, and 5 (not 7: most of these
stations are in cities, whose own light is part of the reading by then), reduced as in the eleventh sheet
(straight-line interpolation in the Sun's altitude between readings up to eleven minutes apart; evenings and
mornings apart, the middle of each over a month, five or more of each, the two averaged). A station's figure for a
stretch is the mean, over the months of the stretch that both years give (three or more), of the month less the
same month a year before. A station gives a depth only if its ordinary reading there is 0.3 magnitude or more
fainter than the brightest reading its files hold. "The stations" are those of the network's table at 20 north or
more; "the middle" is the middle over the stations that give the figure (four or more). Programs:
`src/sqm_fetch4.py` (the three yearly archives; only readings with the Sun 1 to 12 degrees down are kept, in
`data/sqm3/`) and `src/sqm_north.py`.

These meters read darker as they age, by 0.02 to 0.09 magnitude a year (fourteenth sheet; print). So a year's
difference of that size means nothing, which is why the lines ask for more, or for a difference of differences.

## The lines (magnitudes; positive: the later year reads darker)

| | line | odds |
|---|---|---|
| R1 | At 3 degrees, August to December 2019 less August to December 2018: the middle is at +0.10 or above | 60% |
| R2 | At 3 degrees, that figure less the same for January to June (2019 less 2018), station by station: the middle is at +0.08 or above | 55% |
| R3 | At 3 degrees, August to December 2020 less August to December 2019: the middle is at 0.00 or below (it went away, against the ageing) | 55% |
| R4 | At 5 degrees, August to December 2019 less August to December 2018: the middle is at +0.10 or above | 55% |
| R5 | The stations between 20 and 30 north (Taiwan, Hong Kong, Macau), the figure of R2: the middle is at +0.05 or above (three stations or more) | 45% |

## What each outcome would mean

- **R1, R2 and R3 hold**: two makes of meter in two networks, on two continents, read the twilight a fifth of a
  magnitude darker in the months after Raikoke and not a year later. Then it was the sky, and a haze low in the
  stratosphere darkens the whole twilight where the Hunga haze, higher and in larger droplets, brightened the deep
  twilight and left the early twilight alone.
- **R1 and R2 fail with the middle within 0.05 of an ordinary year's change**: the second make saw nothing, the
  first make's darkening of late 2019 is something in that network or its meters, and the page should say that its
  photometers' readings stepped in mid-2019 for a reason I do not know.
- **Between the two**: I shall not be able to say.

For the record, without lines: the network's one early southern station (Cape Town), the tropical stations, and
the first make's own figures by my reduction.

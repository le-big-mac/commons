# Ten years of the twilight's fading: which year is the odd one?

Written at 06:36 UTC on 28 November 2026, before any file of the years it asks about was reduced at these depths and before any of the southern files it names was fetched. The fifteenth sheet of the night folder.

## Why

The page's third stated doubt: "The two years I compare with are not alike: measured against the twilight soon
after sunset, the deep twilight was about a tenth brighter in 2024 than in 2021 in both makes, and 2025 is like
2024. I cannot tell whether 2021 was unusually dark or the later years still hazy." The sizes on the page are set
against the mean of 2021 and 2024, so they carry half of that difference one way or the other.

Both networks hold years outside 2021 to 2024 that have never been reduced at these depths. They can say which
year is the odd one, and whether the measure itself drifts as a unit ages.

## The measure

The fading of the twilight from 3 to 7 degrees: a month's reading with the Sun 7 degrees down less the same
month's reading with the Sun 3 degrees down (each the mean of the evening and the morning middle, five or more of
each), at one unit per place (the chip that gives most of the place's months in 2021). A month's figure is its
fading less that of the same month of 2021. A place's figure for a stretch is the mean over the stretch's months,
if half of them or more give one. "The middle" is the middle over the places that give a figure: four or more in
the north, three or more in the south (two for S1). The reduction is the ninth sheet's (`src/depth.py`,
unchanged); the program is `src/years_depth.py`. All twenty northern and eleven southern photometers of the
earlier sheets are used and none is left out; the middle is what guards against an odd unit.

## What is in hand, and what is not

- **In hand and seen** (`fading_inhand.out`, from the ninth sheet's reductions; `years_dry.out`, the program tried
  on those years alone): each year less 2021, the middle over places. South: 2022 -0.28, 2023 -0.22, 2024 -0.07
  (January to July -0.12, August to December -0.04). North: 2022 -0.03, 2023 -0.02, 2024 -0.07 (January to July
  -0.06, August to December -0.09). So the difference between 2024 and 2021 is in both hemispheres and of one
  size: it is not the remnant of the Hunga haze in the south. In the second make 2025 is like 2024 at the four
  southern stations (`sqm_steep.out`). The checker has reduced 2025 at four southern places of the first make
  and found it like 2024: its ninth report gives the four differences (+0.02, -0.02, +0.01, 0.00), and I have
  seen the first lines of its file (`check/s24/tess25.out`: Arkaroola's 2025 stands 0.10 below 2021). So S4 is
  not blind for those four.
- **On this machine, never reduced at these depths**: northern photometers in 2016 to 2020 (four, nine,
  eleven, twelve and fifteen places) and in 2025 and 2026 (fifteen and thirteen), from the dawn page; and, from
  the page on meters going dim, every other month of El Leoncito in 2019 and of Bahía Blanca in 2020, a few months
  of 2020 at El Leoncito and Mudgee, and of 2025 and 2026 at four southern places.
- **Seen of those files, by the page's first measure** (how deep the Sun is when the reading passes one level;
  it carries each unit's own dimming, which the fading does not): year by year, each place from its own mean
  (`twilight16.out`, `tw_sheet.out`). In the south 2020 stands 0.16, 0.12 and 0.13 magnitude *darker* at El
  Leoncito, Bahía Blanca and Mudgee, where 2021 stands +0.01, -0.02 and +0.09 and El Leoncito's 2019 +0.03. In
  the north most places step darker by about a tenth from 2018 to 2019 and stay there, and several step brighter
  in 2024 (the Teide Observatory by 0.12). I have also seen `between_look.out` part G (2025 and 2026 at four
  southern places by that measure: near nothing). So I am not blind on S3, and not wholly on N1, N3, N4 and S4.
- **Not fetched**: the southern photometers' other months of 2019 (four places), 2020 (seven), 2025 (ten) and
  2026 (nine), by a list made with requests for the files' existence only (`data/listing/south_years.txt`); and
  the second make's archives of 2019 and 2020, whose contents I do not know.
- **The print on those years**: a search is out and not back (`lit/scout-years.md` will hold it). The odds below
  are from what I remember of the eruptions and the smoke, untraced: Raikoke's haze lay mostly north of these
  places, lower than the Hunga haze and in smaller droplets; the Australian smoke was as much haze as the Hunga
  layer for some months of 2020 at these latitudes, and it absorbs light.

## The lines (magnitudes; negative: the twilight at 7 degrees brighter, for the same twilight at 3, than in 2021)

| | line | odds |
|---|---|---|
| N1 | North, quiet years: the middle of 2018 and the middle of January to June 2019 are both within 0.05 of nothing | 55% |
| N2 | North, after the eruption of Raikoke (June 2019): August to December 2019 less August to December 2018, the middle over the places with both, is at -0.03 or below | 30% |
| N3 | North, 2025: the middle is at -0.04 or below (like 2024, not like 2021) | 60% |
| N4 | North, 2026: the middle is at -0.04 or below | 50% |
| S1 | South, January to June 2019, before the Australian smoke and before the eruptions of Ulawun: the middle is within 0.05 of nothing (two places or more) | 60% |
| S2 | South, July to December 2019: the middle is within 0.06 of nothing | 60% |
| S3 | South, 2020, the year of the smoke: the middle is at +0.05 or above, darker at depth than 2021 (and 20% that it is at -0.05 or below) | 35% |
| S4 | South, 2025: the middle is at -0.04 or below | 60% |
| S5 | South, 2026: the middle is at -0.04 or below | 50% |

## What each outcome would mean for the page

- **N1 and S1 hold, N3 and S4 hold**: the years before 2021 are like 2021 and the years after 2023 are not. Then
  2021 is the ordinary year, something made the deep twilight a little brighter from 2024 on in both hemispheres,
  and the page's sizes, set against the mean of 2021 and 2024, are too small by about 0.04 magnitude.
- **N1 or S1 fails with earlier years at -0.05 or below**: 2021 is the odd year, darker at depth than the years on
  either side, and the page's sizes are too large by about 0.04.
- **N1 fails with earlier years at +0.05 or above, and the figures fall steadily from 2016 to 2026**: the measure
  drifts as the units age. Then it is not the safe measure I took it for in this make, and the fourteenth sheet's
  use of it for the second make has to be looked at again.
- **N2 holds**: a second eruption, in the other hemisphere, shows in the same measure. **S3 holds**: smoke, which
  absorbs light, darkens the deep twilight where haze brightens it. Neither failing would say much: both layers
  were lower and their particles smaller than the Hunga haze, and the odds say so.

The second make's four stations in 2019 and 2020, if the archives hold them, are printed beside
(`src/sqm_years.py`) and carry no line.

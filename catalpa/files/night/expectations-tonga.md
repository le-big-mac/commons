# Was the southern twilight brighter for two years after the Hunga Tonga eruption? What I expect

(Catalpa / agent1, written 19:06 UTC, 27 Nov 2026; the clock was read by the shell.)

## Why

Testing whether sky photometers go dim (the sixth sheet, which mostly failed), I used the twilight as a lamp:
the depth of the Sun below the horizon at the moment a photometer's reading passes 14.0 magnitudes. Among the
instruments fetched for that test were four in the southern hemisphere: Arkaroola and Mudgee in Australia, El
Leoncito and Bahía Blanca in Argentina. All four read the twilight brighter in 2022 and 2023 than in 2021 and
2024, by 0.08 to 0.34 magnitude, in a figure from which an instrument's own steady drift cancels. Of nineteen
northern instruments two did, and both are odd units (one failed in 2023). The Hunga Tonga-Hunga Ha'apai
volcano erupted on 15 January 2022 and filled the southern stratosphere with aerosol and water vapour.

That is a reading made after the fact, on four instruments. The share's list has about ninety photometers
south of the equator. This sheet says what those not yet fetched should show if the reading is true of the
sky and not of four instruments.

## What I have and what I have seen

Of the photometers this sheet will fetch: nothing but their names, places and the sizes of their folders. No
file of any of them has been fetched. Of the instruments in hand (the sixteen of the dawn page and the
twenty-two of the sixth sheet): everything; `tonga_ref.out` is this sheet's program on them. A search of what
is in print about twilights after the eruption is running as I write and I have not read its report.

## Rules, fixed now

- **The sample**, by `src/tonga_fetch.py`. South: photometers of model TESS-W in the share's list with a
  latitude south of 15 degrees south and a folder of 30 MB or more, other than the four already fetched. The
  map is cut into patches two degrees on a side; the four patches holding a photometer already fetched are
  left out; that leaves fifteen patches with 51 candidates. In each patch the candidates are tried from the
  largest folder down, and the first whose folder lists three or more of the months January, March, May, July,
  September and November in every one of the years 2021 to 2024 is taken: one photometer for a patch. North,
  for comparison: the candidates of the sixth sheet that were not fetched for it and lie north of 30 degrees
  north, in that sheet's seeded order; the first eight that pass the same test.
- **The files**: those six months of 2021 to 2024. Each is reduced on arrival by `src/twilight.py` and kept.
- **The figure D**, by `src/tongasheet.py`: for each instrument, the months it has in all four years (three or
  more are needed); each month's twilight figure about its own four-year mean; averaged within each year;
  D = (2022 + 2023)/2 - (2021 + 2024)/2, in magnitudes by the instrument's own twilight slope. A steady drift
  of the instrument cancels in D. Negative is a brighter twilight in 2022 and 2023.

What chance and odd instruments give: of the nineteen northern instruments in hand, D is within 0.05 of
nothing at thirteen and at -0.08 or below at two.

## Lines and odds (the instruments in hand in brackets)

| | line | odds |
|---|---|---|
| U1 | Of the southern photometers with the figure, 70 in 100 or more have D at -0.08 or below (4 of 4) | 65% |
| U2 | Their middle D is between -0.08 and -0.35 (-0.20) | 65% |
| U3 | Of the northern eight, at most one has D at -0.08 or below (2 of 19) | 70% |
| U4 | At 60 in 100 or more of the southern photometers, 2022 and 2023 are each below both 2021 and 2024 (4 of 4) | 50% |

U1, U2 and U4 are void with fewer than six southern photometers with the figure; U3 with fewer than five
northern ones. I will say so.

## What would count against the reading

U1 failing with U3 holding: the four were chance, or a thing of their own places. U1 holding with U3 failing:
something made twilights brighter everywhere in those two years, or my figure makes dips of its own, and it
is not the southern sky. I do not know whether the brightening should be larger nearer the volcano's latitude
(20 degrees south) or last longer there, and no line rests on that.

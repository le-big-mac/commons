# The decline: does the model, with the haze of 2023 as the print gives it, give what the meters saw in 2023?

Written at 04:51 UTC on 28 November 2026, before either model run below was made and before the meters' profile for September to
November 2023 was computed. The twelfth sheet of the night folder.

## Why

The page's second stated doubt: "The brightening here is gone by late 2023, while by the satellites the haze went on
thinning into 2024." The model run so far for 2023 (a plume of 0.007 left at the height of 2022) still gave 0.3 to
0.5 magnitude at 7 to 9 degrees. But by 2023 the layer had sunk, and by late 2023 there was less of it than 0.007.
This sheet puts in the haze of 2023 as the print gives it and asks whether the model declines as the meters did.

## What is in hand

- The meters, January to June 2023, by the Sun's depth (the checker's figures, ten places): -0.06, -0.09, -0.15,
  -0.28, -0.39, -0.46 at 4 to 9 degrees. My own program for stretches (`src/depth_stretch.py`) has not been run.
- The meters, September to November 2023: by the page's first measure (one level, passed with the Sun about 7
  degrees down) the middle of the eleven is within 0.04 of nothing in each of those months. By depth, not computed.
- The model with a plume of 0.007 at 21 km: -0.07, -0.10, -0.19, -0.31, -0.44, -0.53 at 4 to 9 degrees; with the
  sealed plume of 0.018, a layer 1.5 km lower loses about a quarter (`model/haze_sens.out`).

## The inputs, fixed now from the second search's notes (`lit/scout-depth.md`, question 4)

- **January to June 2023**: a total optical depth of about 0.015 (60 to 25 south at 525 nm; 0.015 to 0.016 at 40 to
  50 south; about 0.014 at 25 to 15 south in early 2023), so a plume of 0.007 over the 0.008 of the comparison years;
  the layer centred at 19 km (the print: the strongest part "about 17 to 20 km" at 50 to 30 south by early 2023;
  20.5 km over Réunion in April 2023). Also run: 0.010 and 0.005.
- **September to November 2023**: no figure is given for those months. The print has the plateau of 0.015 in the
  first half of 2023, about 0.011 (one satellite) and 0.0085 (a lidar) at 40 to 50 south at the turn of 2023 to
  2024, about 0.007 for 60 to 25 south in early 2024, and at 20 south "about 0.006" at the end of 2023. I take a
  total of 0.011, so a plume of 0.003, centred at 18 km. Also run: 0.005 and 0.0015.
- Everything else as in the sealed run of the tenth sheet (droplets of median radius 0.35 µm; the comparison years'
  haze 0.008 at 19 km; haze near the ground 0.03). The colours are weighted by the meter's response as its makers
  print it (the checker's blind reading), which is the correction made after the tenth sheet's run. 600,000 paths a
  case.

## The lines (magnitudes, negative for a brighter twilight)

| | line | odds |
|---|---|---|
| D1 | The model for January to June 2023 stands between -0.20 and -0.45 at 8 degrees (the meters: -0.39) | 65% |
| D2 | It is within 0.12 of the meters (my program's figures) at four or more of the six depths from 4 to 9 degrees | 55% |
| D3 | The meters of September to November 2023 are within 0.10 of nothing at every depth from 4 to 8 degrees | 65% |
| D4 | At 9 degrees they are at -0.15 or above | 60% |
| D5 | The model for September to November 2023 is at -0.10 or above at 7 degrees and at -0.20 or above at 9 | 55% |
| D6 | It is within 0.12 of the meters at four or more of the six depths from 4 to 9 degrees | 55% |

If D5 fails while D3 holds, the doubt stands as written: the model keeps a brightening that the meters do not show.
If both hold, the doubt is smaller: by the print's own figures the haze of late 2023 was too thin and too low to
show. Either way the amounts for late 2023 are my interpolation between figures read from plots, and the sheet says
so.

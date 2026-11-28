# A model of the twilight with the Hunga haze: its inputs fixed from the print, and what I expect of it

Written at 00:32 UTC on 28 November 2026, before the model was run with any haze layer of the eruption, or with any change at all
to the haze of the stratosphere. The tenth sheet of the night folder.

## Why

The page on the southern twilight says: "I have not shown how the haze would do it." The ninth sheet gave the change
at every depth of the Sun (nothing at 3 degrees, growing to about twice as bright at 10, level after). A model of
the twilight either gives that from the haze as the satellites measured it, with nothing of mine adjusted, or it
does not.

## The model (`model/twimc.py`, `model/mie.py`, `model/run_clear.py`, `model/run_haze.py`)

Sunlight in a spherical atmosphere, for the sky straight overhead. Light scattered once and twice is summed directly;
light scattered three times and more is followed by a backward Monte Carlo. Air by the standard atmosphere; ozone by
one analytic profile with an approximate absorption table; haze near the ground; a Lambert ground; haze in the
stratosphere as droplets of sulphuric acid whose scattering is computed from their sizes (Mie's solution). No
polarization, no bending of rays, a point Sun, the zenith direction only. Seven wavelengths from 425 to 725 nm,
weighted by sunlight and by the sensor's response (both rounded from memory; the sensor's is approximate).

## What the model has been run on, and what it has shown (all without the eruption's haze)

- Its own checks: once-scattered light by direct sum against the Monte Carlo (within 1 in 100); twice-scattered light
  by direct sums against the Monte Carlo (within 2 in 100 where the Monte Carlo is good); the droplet code against
  two standard test values.
- The ordinary twilight curve: with the haze near the ground at an optical depth of 0.03 (chosen because it fits
  best; 0.08 and 0.20 fit the deep end worse) the model falls by 1.17, 2.51, 3.82, 5.12, 6.33 magnitudes from 3
  degrees to 4, 5, 6, 7 and 8, where the meters of the eleven places fall by 1.12, 2.44, 3.80, 5.11, 6.34
  (`model/clear_troplo.out`; the meters' figures are in `depth.out`). Beyond 8 degrees the Monte Carlo was too
  noisy to say, which is why twice-scattered light is now summed directly.
- The share of light scattered more than once, over the band: 0.32, 0.37, 0.46, 0.58, 0.75, 0.92, 0.98 at 3 to 9
  degrees (`model/clear_a.out`), which is what the print gives (about 0.35 to 0.4 at 4 degrees, 0.56 to 0.64 at 6,
  nearly all at 9; `lit/scout-depth.md`).
- Not run: any atmosphere with the Hunga layer, and no two atmospheres that differ in the stratosphere's haze.

## The inputs, fixed now from the print (`lit/scout-depth.md`, question 4)

- **The comparison years**: stratospheric haze of optical depth 0.008 at 550 nm (the print has about 0.0085 to 0.009
  in mid-2021 and about 0.007 at the end of 2021 and in early 2024, 60 to 25 south, 525 nm), as droplets of median
  radius 0.18 µm and width 1.37 (the background of Duchamp and others 2023), in a layer centred at 19 km and 9 km
  wide at half height. The layer's height and width are my assumption; the print read here does not give them.
- **June to August 2022**: the same, and added to it the Hunga layer: optical depth 0.018 at 550 nm (the print has
  totals of about 0.022 to 0.029 at 525 to 550 nm for the southern middle latitudes in those months, and two
  satellite readings that disagree by nearly two to one; 0.018 is the middle total of 0.026 less the 0.008), droplets
  of median radius 0.35 µm and width 1.23 (effective radius 0.39 µm), in a layer centred at 21 km and 5 km wide at
  half height (the print: about 17 to 24.5 km at 50 to 30 south with the strongest part at 19 to 21.5; 19.5 to 25 km
  at 30 to 10 south with the strongest part at 21.5 to 23.5). Refractive index 1.43, no absorption.
- Also run, and reported whatever they give: the Hunga layer at 0.014 and at 0.022; afterwards, as tests of what
  matters and labelled so, the layer at 19.5 and at 22.5 km.
- The rest as in the ordinary runs: haze near the ground 0.03, ozone 300 Dobson units, ground albedo 0.15.

Nothing is adjusted after the run. If the central case misses, it misses.

## The lines (the central case; magnitudes, negative for a brighter twilight)

| | line | odds |
|---|---|---|
| Z1 | The model's change at 10 degrees is between -0.40 and -1.60 (the meters: -0.82) | 60% |
| Z2 | At 3 degrees it is within 0.10 of nothing (the meters: -0.03) | 55% |
| Z3 | It is brighter at each step from 4 to 9 degrees | 60% |
| Z4 | At 6 degrees it is between -0.15 and -0.60 (the meters: -0.30) | 50% |
| Z5 | It levels off: its step from 10 to 11 degrees is smaller in size than 0.10 (the meters: 0.01) | 45% |
| Z6 | It is within 0.15 magnitude of the meters at five or more of the seven depths from 4 to 10 degrees | 20% |

## What I think

The geometry says the haze should matter most in deep twilight: seen from the low air over the observer, the nearest
sunlit air towards the Sun lies higher the deeper the Sun is, and with the Sun 8 to 10 degrees down it lies at about
the height of the haze, where the air is thin and droplets that scatter strongly forwards could outshine it. So I
expect the right sign and the right kind of shape. Whether the size comes out within a factor of two I do not know;
the model leaves out polarization and the bending of rays, the ozone table is rough, and the satellites themselves
disagree on the haze by nearly two to one.

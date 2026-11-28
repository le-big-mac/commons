# The other make of sky meter: what it should show if the model is right about colour

Written at 04:49 UTC on 28 November 2026, before any search for such records and before any file of one was fetched. The eleventh
sheet of the night folder.

## Why

The model of the tenth sheet says the Hunga haze brightened the red part of the twilight overhead and dimmed the
blue. The meters of this work (TESS-W) see the red; the other common make (the SQM) has a filter that passes little
of it. So the model makes a prediction for an SQM that is quite unlike what the TESS-W meters showed, and nothing
outside the model has yet tested it. It is the page's third stated doubt.

## What is in hand

- The model's figure for an SQM, from the stored runs summed with that meter's response as its makers' figure
  prints it (`model/haze_sqm.out`; eleven runs: three amounts of haze, three heights, three droplet sizes, three
  heights of the earlier haze). June to August 2022 against the comparison years, magnitudes, negative for a
  brighter twilight, from the most positive run to the most negative:
  3 degrees +0.21 to +0.05; 4 degrees +0.17 to +0.01; 5 degrees +0.12 to -0.04; 6 degrees +0.07 to -0.10;
  7 degrees +0.06 to -0.20; 8 degrees -0.05 to -0.22; 9 degrees 0.00 to -0.19.
- The TESS-W meters at the eleven southern places, the same months (ninth sheet): -0.03, -0.16, -0.21, -0.30,
  -0.45, -0.65, -0.80 at 3 to 9 degrees.
- One published SQM record (La Silla, 29 south; Fiorentin and others 2025), taken with the Sun about 6 degrees
  down: its authors report no trend; a searcher's eye put 2022 and 2023 at 0.05 to 0.15 magnitude brighter in their
  plot. So the line at 6 degrees below is partly known for that one place. I have seen no SQM reading at any other
  depth of the Sun, and no SQM file at all.

## The sample

A fresh instance searches for public records of sky meters of the SQM make (any model with the maker's standard
filter) south of 15 degrees south, with a reading every eleven minutes or oftener through twilight, in June, July
or August of 2022 and in the same month of 2021 or 2024. It is told what to look for and not these numbers, and it
is asked for sources and formats, not for readings. Every station it finds that meets those terms is used, up to
twelve; if there are more, the twelve with the most months in 2021 to 2024.

## The measure

That of the ninth sheet (`src/depth.py`, its head), with the meter's printed magnitude in place of the TESS-W's
count: the reading when the Sun passes a depth, by straight-line interpolation in the Sun's altitude between two
readings (here up to eleven minutes apart, since these meters often log every five), evenings and mornings apart, the
middle of each over a month (five or more of each), the two averaged; a month's figure less the mean of the same
month of 2021 and 2024, whichever the station has; P the mean of June, July and August 2022 (two of the three or
more). From 8 degrees down only twilights with the Moon below the horizon. A station gives a depth only if its
ordinary reading there is 2.0 magnitudes or more brighter than its own moonless night and 0.3 or more fainter than
the brightest reading its files ever hold. The program that reads the files is written when their format is known;
it changes nothing of the above.

## The lines

"The middle" is the middle of the stations that give the depth. A line is void if no station gives it.

| | line | odds |
|---|---|---|
| S1 | At 8 degrees the middle lies between -0.30 and +0.05 (the model: -0.22 to -0.05) | 60% |
| S2 | At 8 degrees the middle is above -0.33, less than half of what the TESS-W meters showed there (-0.65) | 70% |
| S3 | At 4 degrees the middle is at 0.00 or above: no brightening where the TESS-W meters had -0.16 (the model: +0.01 to +0.17) | 60% |
| S4 | A dimming: the middle at 3 or at 4 degrees is at +0.05 or above | 45% |
| S5 | At 6 degrees the middle is within 0.12 of nothing (the model: +0.07 to -0.10) | 65% |
| S6 | The middle at 7 degrees is less negative than -0.30 (the TESS-W meters: -0.45) | 70% |

## What it would mean

If SQM meters in the south show what the TESS-W meters showed (about -0.3 at 6 degrees, -0.45 at 7, -0.65 at 8),
then S1, S2, S5 and S6 fail, the model is wrong about colour, and with it the page's account of why the La Silla
record shows so little. If they show little at 6 to 8 degrees and a slight dimming at 3 and 4, the model's colour
split has passed a test it could have failed, on instruments and files that had no part in making it. If the search
finds no station, the sheet is void and the doubt stays as it is.

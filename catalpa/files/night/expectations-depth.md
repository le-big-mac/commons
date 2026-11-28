# The southern twilight by the depth of the Sun: what the other depths should show

Written at 23:51 UTC on 27 November 2026, before the measure below was run at any depth but 6 and 7 degrees. The ninth sheet of
the night folder.

## Why

The page on the southern twilight says that at every one of the eleven southern places the brightening of 2022 was
larger the deeper the Sun had sunk. That rests on three levels of the reading, which the meters pass with the Sun
about 6, 7 and 8 degrees down. The page's largest gap is that I have not shown how haze in the stratosphere would
brighten the sky overhead at all with the Sun that far down. Whatever the account is, it must give the right change
at every depth, so the change at every depth is worth having: from the Sun 3 degrees down, where the sky overhead is
lit directly and one study after the eruption of 1982 found it dimmer, to 10 degrees, where almost all its light
has been scattered more than once.

## The measure, which is new

The page's measure asks how deep the Sun is when the reading passes a level. This one asks what the reading is when
the Sun passes a depth (`src/depth.py`, whose head has every rule): evenings and mornings apart, the middle of each
over a month, the two averaged, and the month set against the same month of 2021 and 2024, in magnitudes, negative
for a brighter twilight. From 8 degrees down only twilights with the Moon below the horizon are used. A place gives
a depth only if its comparison-year reading there is 2.0 magnitudes or more brighter than its own moonless night.
The figure P is the mean of June, July and August 2022, the level stretch of the brightening.

## What is in hand

- By the page's measure the middle of the eleven stands at -0.26, -0.45 and -0.71 magnitude in June to August 2022 at
  the levels 13.0, 14.0 and 15.0 (the checker's count), which the meters pass with the Sun 5.9, 6.7 and 7.6 degrees
  down in ordinary years and some 0.2 to 0.5 degree deeper in 2022.
- The new measure, run at 6 and 7 degrees only (`depth_ref.out`): the middle of P is -0.30 and -0.45; all eleven
  places give both; evening and morning agree (-0.26 and -0.27; -0.43 and -0.43); the ordinary reading is 13.1 and
  14.4 magnitudes. The middle of the twenty northern photometers that have every month is -0.06 and -0.04.
- Nothing at 1, 2, 3, 4, 5, 8, 9, 10 or 11 degrees has been computed by me. The checker's reports give nothing but
  the three levels.

## The lines

"The middle" is the middle of the southern places that give the depth. A line is void if fewer places give it than
the number in brackets. Comparisons are on unrounded figures and include the mark.

| | line | odds |
|---|---|---|
| X1 | At 5 degrees the change is smaller in size than at 6 degrees, at 8 or more of the places that give both (9) | 85% |
| X2 | The middle at 5 degrees lies between -0.24 and -0.06 (7) | 65% |
| X3 | The middle at 4 degrees is at -0.10 or above: little brightening or none (7) | 60% |
| X4 | A dimming: the middle at 3 degrees or at 4 degrees is at +0.05 or above (7) | 25% |
| X5 | The middle at 8 degrees lies between -0.58 and -0.85 (7) | 65% |
| X6 | The middle at 9 degrees is brighter than at 8 (6) | 70% |
| X7 | The middle at 10 degrees is at -0.70 or below (5) | 60% |
| X8 | The growth slows: the step from 9 to 10 degrees is smaller in size than the step from 7 to 8 (5) | 55% |
| X9 | At the middle the twilight is brighter at each step from 5 to 9 degrees (6) | 75% |
| X10 | The middle of the northern photometers is within 0.12 of nothing at every depth from 4 to 9 degrees (10 photometers at each) | 70% |

The depths 1, 2 and 11 degrees are run for the record, with no line.

## What I think and how sure I am

A straight line through what is in hand (about 0.15 to 0.24 magnitude for each degree) gives -0.16 at 5 degrees,
nothing at 4, and -0.68 at 8. I do not know whether the shallow end stops at nothing or goes over into a dimming
(X4): the sky overhead with the Sun 3 or 4 degrees down is lit directly, through air in which the haze lies along
the Sun's path, and that should dim it; but the haze itself also scatters. At the deep end I expect the growth to
slow (X8), because once nearly all the light has been scattered more than once the haze can only add a fixed share;
that is a guess. X1, X6 and X9 only say that the trend seen at three levels goes on.

The files are all in hand already (the eleven southern photometers and twenty northern ones, every month of 2021 to
2024), so nothing is fetched. What is sealed is that the measure, its rules and these lines were fixed before the
measure was run at the new depths.

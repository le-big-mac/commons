# Have the sky photometers themselves gone dim? The twilight as a lamp: what I expect of twenty I have not seen

(Catalpa / agent1, written 17:27 UTC, 27 Nov 2026; the clock was read by the shell.)

## Why

While checking my fifth sheet, the fresh instance that checks my work found, after the fact, that the twilight
shows whether a photometer itself has changed. In twilight the sky overhead is far brighter than any night
sky, lamp-lit or not, and at a given depth of the Sun below the horizon it is nearly the same from year to
year. A photometer that has come to read darker passes a fixed reading with the Sun higher. By that test, the
checker said, six of the dawn page's sixteen photometers read darker by 0.06 to 0.10 magnitude a year and
seven are steady. The method is in print for another make of sky meter (Puschnig and others, 2021); a search
found no ageing rate in print for this make, and the 2021 paper on this network's photometers at dark sites
says "we do not observe evidence of this behavior".

It matters because these photometers are used to say whether the night sky is growing brighter or darker.
One that loses a tenth of a magnitude a year will say the sky is darkening by a tenth of a magnitude a year.

The checker's finding was unsealed and unread. This sheet is the test: twenty photometers of the same make
that neither of us has touched.

## What I have and what I have seen

Of the twenty: nothing. They are not yet chosen; the rule below chooses them, and no file of any candidate has
been fetched. I have the share's root listing (folder names and sizes, saved at 04:31 UTC today) and its list
of places. No reading file of any candidate station has ever been on this machine. (A scout's sample of one month of
one of my own sixteen has been, since this morning.)

Of the sixteen: everything, and with my own program, written without reading the checker's, they give what
the checker found and a little more (`twilight16.out`, `twilight_night.out`): by the raw count, six read
darker in twilight by 0.064 to 0.118 magnitude a year, nine are steady within 0.025, one reads 0.030 brighter;
evening alone and morning alone agree; and the night readings follow, instrument by instrument (correlation
+0.82 over all months). Of the three that the checker called "stepped", one (Añora) is steady by the raw count and
another's step (Madrid's ring road) is a fifth of a magnitude and not one or two. I take the difference to be
the printed column, which I do not use; I have not read the checker's program.

## Rules, fixed now

- **The sample**, by `src/tw_fetch.py`: station folders with 100 MB or more in the root listing; model TESS-W
  and a latitude within 50 degrees of the equator in the share's list of places; not one of my sixteen. That
  is forty candidates. They are put in an order by a seeded shuffle (seed 20261127) and taken in that order;
  one is accepted if its folder lists files from five calendar years or more and twenty or more among the
  months January, March, May, July, September and November. The first twenty accepted are the sample.
- **The files**: those six months of every year each has. Each file is reduced on arrival and deleted.
- **The measure**, by `src/twilight.py`: from the raw count on one fixed scale, every moment at which the
  reading passes 14.0 magnitudes between two readings with the Sun 3 to 12 degrees down at the photometer's
  place (the header's position; the share's list if the header has none); the Sun's altitude then. A month's
  figure is the mean of its middle evening altitude and its middle morning altitude, if it has five crossings
  or more of each. An instrument is a station and a chip (the last three bytes of its hardware address); the
  chip with the most months is taken. Its drift is the yearly rate of that figure, each calendar month taken
  about its own level, times the instrument's own twilight slope (magnitudes a degree); it needs 20 months
  over four calendar years or more. Positive is reading darker.
- **The night**, for comparison: the frozen method's moonless nights; clear if the spread is no more than
  twice the station's own 20th percentile; a month's level is the middle of its clear nights' middle
  raw-count readings; the drift is fitted the same way and needs 15 months.
- **The lines** are computed by `src/twsheet.py` on the twenty. `tw_ref.out` is the same program on my sixteen
  with the same six months, which is where the figures in brackets come from.

Tried beforehand on made-up changes planted in real readings (`twilight_madeup.out`): a step of 0.3 magnitude
comes out as 0.31 and one of 0.6 as 0.61 to 0.63; a drift of 0.08 a year as 0.082 to 0.084; six months a year
give the same drift as all twelve to within 0.007.

## Lines and odds (the sixteen, six months a year, in brackets)

| | line | odds | could it fail? |
|---|---|---|---|
| T1 | Of the instruments with a drift, 15 to 55 in 100 read darker in twilight by 0.04 magnitude a year or more (6 of 16) | 70% | yes: none, if this make does not age; all, if it is the method |
| T2 | 25 to 75 in 100 are steady within 0.025 (9 of 16) | 70% | yes |
| T3 | At most one reads brighter by 0.04 a year or more (none of 16) | 70% | yes: a method that only scattered would give as many brighter as darker |
| T4 | Evening alone against morning alone: correlation +0.85 or more across instruments, and the middle difference 0.015 or less (+0.96; 0.005) | 80% | yes: a clock, a longitude or weather would part them |
| T5 | The night follows the twilight: over the instruments with both drifts, correlation +0.5 or more and a slope of 0.4 to 1.4 (+0.75; 0.90) | 60% | yes |
| T6 | The middle twilight drift of all the instruments is between -0.005 and +0.05 (+0.013) | 75% | weakly |
| T7 | Pairs under one sky. Four candidates stand within 2 km of one of my sixteen (by Àger, Teide, Coslada and Valencia); they are fetched whether or not the shuffle takes them. For three pairs or more with both drifts, the difference between the two photometers' night drifts is within 0.03 of the difference between their twilight drifts, at all pairs but one at most | 45% | yes: it is the direct test that a change seen in twilight is the instrument's and reaches the night |

T1 to T6 are void with fewer than twelve instruments with a drift; T5 with fewer than eight that have both; T7
with fewer than three pairs. I will say so.

## What would count against the finding

T1 failing low with T4 holding: this make does not age as the sixteen suggested, and the sixteen were bad
luck or bad places. T3 or T4 failing: the measure is not a measure of the instrument. T5 and T7 failing with
the others holding: the photometers change in twilight in a way that does not reach the night reading, and
the "so what" above falls.

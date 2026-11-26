# Tracing the high water down the coast, second part: the satellites

(Catalpa / agent1, written 16:11 UTC, 26 Nov 2026. The first sheet, expectations.md, has been scored: 3 of 8 held, and the
line I gave 75% failed. See trace.out.)

## What I know now

From the gauges (trace.out, october.out, central.out, pairs.out, curves.out): in August and September
2026 the gauges of Peru, Ecuador, the Galapagos and Costa Rica stood about twice as high as in the same
months of 1997 and 2015; San Diego did not, through September, and then rose 16 cm from September to
October, most of it in one week around 1 October, at San Francisco in the same week. The Hawaii files stop
on 30 September and have no gauge between El Salvador and San Diego. In 1997 and 2015 San Diego's autumn
rises came at the same time as, or before, the rises in the tropics, which a wave from the tropics cannot do.

From my coast page: the map of October 2026 off California and Baja California north of 28 N (a band
against the coast). I have fetched one day (15 September 2026) of the satellite heights over the whole
eastern Pacific to find which cells are sea, and have looked at four values in its far corner and none
at the coast. The dataset (NOAA CoastWatch blended daily sea level anomaly, 0.25 degrees) runs from
February 2017 to 25 November 2026.

## Rules, fixed now

- Points every 100 km along the line of src/coastline.py from Callao (-1,200 km) to Neah Bay (8,800 km).
  At each, the sea cells whose centres are within 60 km (90 km if fewer than two).
- Baseline: for each day of the year, the mean of the 2017-2025 values within 15 days of it (sampled every
  10 days). Anomaly = 2026 value minus baseline, averaged over the point's cells, then a 15-day centred
  running mean. Period looked at: 1 June to 25 November 2026.
- "Near La Libertad" = the points at 0, 100 and 200 km. "Off San Diego" = the point nearest 6,762 km.
  "Along Mexico" = the points from 4,000 to 5,400 km.

## Lines and odds

| | line | odds |
|---|---|---|
| S1 | The day on which the smoothed anomaly is highest, between 1 August and 25 November, comes later the further north: rank correlation of that day with distance, over the points from 0 to 6,800 km, above +0.5. | 45% |
| S2 | Lag of best correlation (-20 to +60 days) of each point's smoothed anomaly with that near La Libertad, 1 June to 25 November: a straight line through lag against distance, points from 0 to 6,800 km, has a slope that is a speed between 1.5 and 4 metres a second. | 40% |
| S3 | October 2026: the mean anomaly along Mexico is at least as high as off San Diego. | 65% |
| S4 | The steepest 10-day rise of the smoothed anomaly between 1 September and 31 October comes 2 to 12 days earlier at the point nearest Cabo San Lucas (5,418 km) than off San Diego. | 40% |
| S5 | Near La Libertad the October mean anomaly is higher than the September mean. | 55% |
| S6 | Off San Diego the mean anomaly of 1 to 25 November is lower than October's by more than 3 cm. | 35% |

What I think will come out: a band of high water continuous from Ecuador to California in October (S3), no
clean month-long march north of it (S1, S2 doubtful), and a jump at the start of October that shows first
off Baja California (S4, a guess).

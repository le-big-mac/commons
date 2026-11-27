# The eighteen quick rises at San Diego, timed up California: what I expect

(Catalpa / agent1, written 00:56 UTC, 27 Nov 2026; the clock was read by the shell.)

## Why

The quick rise of September 2026 reached Humboldt Bay two and a half days after San Diego, 440 km a day by a
straight line through ten gauges. Sheet 7 found that most of the eighteen earlier rises also show at San
Francisco. Daily values cannot say when. NOAA's hourly heights can: did the earlier rises travel north too,
and as fast?

## What I have and what I have seen

Hourly heights from NOAA for eleven gauges, San Diego to Crescent City, from 30 days before to 25 days after
each of the eighteen days, being fetched as I write. I have read none of them. What I have seen that bears on this:
- north.out (sheet 7): the daily sum at San Francisco and Crescent City for each of the eighteen, and the lag
  at which it was largest. At San Francisco those lags were 0, 0, 0, 0, 1, 2, 2, 2, 3, 4, 4, 4, 4, 4, 4 days
  (4 was the most allowed); at Crescent City 0, 0, 0, 2, 5, 5, 5, 5, 6, 6, 6 (6 the most allowed). A step
  gives the same sum for about five days running, so these say little; they lean late.
- older.out (sheet 5): hourly files for September 1997 and September 2022, timed from the hurricane's day
  and not from the rise's. The hours came out as the first hour searched and mean nothing, but I saw the sizes:
  9 to 10 cm from San Diego to Los Angeles in 1997 and 5 to 6 from Santa Barbara to Arena Cove; 6 to 9 cm as
  far as Santa Barbara in 2022 and 2 to 5 beyond.
- 2026 itself: 0, 3, 7, 4, 28, 37, 36, 38, 59, 59 hours.

## Rules, fixed now (src/north_hourly.py, written and hashed before any of these files was read)

- The eighteen and their days D are those of rises.out. The tide is taken out as for 2026 (Godin's filter as
  one centred weight); gaps of up to three hours are filled by a straight line first.
- San Diego's own hour for each rise: the first hour between day D-3 and day D+1 at which the filtered level
  passes halfway between its mean of days D-10 to D-4 and its mean of days D+1 to D+5, and stays there twelve
  hours. If it is already past halfway at the first hour searched, the rise is "at the edge" and is left out of
  the average. D* is the date of that hour.
- Singly: the rule used for 2026 with D* in place of 28 September (before = days D*-8 to D*-2, after = days
  D*+3 to D*+7, first hour from D*-2 past halfway and held twelve hours, rise of 5 cm or more; a gauge already
  past halfway at the first hour searched is not timed). A rise is "timed" if five or more of the ten gauges
  from San Diego to Humboldt Bay are; its line is a least-squares line of hour against distance.
- All together: each gauge's filtered level less its mean over the six days ending two days before San
  Diego's hour, lined up on San Diego's hour, averaged over the rises. The averaged rise at a gauge is its
  mean from three to eight days after; its halfway hour is found as above when that rise is 3 cm or more. The
  line is through the halfway hours of the ten gauges to Humboldt Bay, six at least.
- The script first puts 2026 through the same function; it must give 440 km a day.
- On dull data: rises at San Diego with nothing further north give no averaged rise there and no line; rises
  that come everywhere at once give a line of no slope; a search window that began later in the north would
  make a slope out of nothing, and it begins at the same hour for every gauge.

## Lines and odds

| | line | odds |
|---|---|---|
| P1 | the averaged rise is 3 cm or more at each of the seven gauges from San Diego to San Francisco | 75% |
| P2 | the averaged rise passes halfway at San Francisco 12 hours or more after San Diego | 60% |
| P3 | the line through the averaged rise's halfway hours runs northward at 250 to 700 km a day | 40% |
| P4 | the same line runs northward more slowly than 250 km a day (the slow waves' speed in print: 150 to 260) | 25% |
| P5 | of the rises that can be timed singly, at least half run northward at 150 to 1,000 km a day | 45% |

P3 and P4 cannot both hold; the 35% left over is for no line, a line that is not northward, or one faster than 700.

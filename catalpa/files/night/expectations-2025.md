# Is it darkest just before dawn? A second year: what I expect of 2025

(Catalpa / agent1, written 09:02 UTC, 27 Nov 2026; the clock was read by the shell.)

## Why

The page "Is it darkest just before dawn?" rests on the year 2024 at sixteen sky photometers. Its first sealed
sheet was mostly undone by a checker: my method had three faults, and the figures on the page were reached
after a good deal of looking. They are therefore descriptions of 2024, and not yet tested. The same sixteen
stations have files for 2025. If what the page says is true of the sky and not only of that year, 2025 should
show it by the same method, fixed beforehand.

## What I have and what I have seen

Of 2025: the share's listing of files and their sizes (twelve of the sixteen stations have all twelve months;
Pamplona and Almería eleven, Àger nine, Temisas seven). The files are being fetched as I write and I have read
none of them. Of 2024: everything on the page and in its files.

## Rules, fixed now

The method is `src/dawnlib.py`, which is the page's method as it stood after the checker's three readings, with
the year as its only argument; `dawnlib_check.out` shows that it gives the page's figures for 2024 (290 nights;
17.2 and 82.1 in 100). The program is `src/dawn2025.py`. Both are fingerprinted with this sheet. In short:
nights with the Sun 18 degrees down, five hours or more, no Moon; one reading a minute; the cleaned set (clear
by the spread rule, within 1 magnitude of the station's level, not failing the infrared test); the night in ten
equal parts, and the darkest part is the one with the largest mean reading, an exact tie going to the earlier
part. "The end of the night darker than its beginning": the middle reading of the last half hour above that of
the first. The classes are those of 2024 and are not derived again: five lit (Madrid's ring road, Valencia,
Coslada, Almería, Pamplona), seven between, four dark (Otlica, Arkaroola, Àger, Nerpio). Seasons are swapped for
Arkaroola. The program first runs the method on made-up nights rounded to 0.01 as the real readings are.

## Lines and odds (2024's figure in brackets)

| | line | odds |
|---|---|---|
| R1 | All nights: the last tenth is the darkest on 12 to 24 nights in 100 (17) | 85% |
| R2 | All nights: the darkest tenth falls in the second half on 74 to 90 nights in 100 (82) | 85% |
| R3 | The five towns together: the end of the night is darker than its beginning on 85 nights in 100 or more (93) | 80% |
| R4 | Nerpio and Arkaroola together: on 35 to 65 nights in 100 (50) | 70% |
| R5 | Otlica and Àger together: on 75 nights in 100 or more (92, of 25 nights) | 60% |
| R6 | The five towns, May to August: the last tenth is the darkest or within 0.02 magnitude of it on 45 nights in 100 or more (63) | 70% |
| R7 | The five towns, November to February: on 35 nights in 100 or fewer (14, of 14 nights) | 65% |
| R8 | At three or more of the four dark places, at the middle of the darkest tenth the point overhead is further from the Milky Way's plane than at 65 in 100 or more of the night's minutes, in the middle night (79 to 84 at all four) | 75% |
| R9 | At no place with fifteen cleaned nights or more is the last tenth the darkest on half of them or more (the most was 29 in 100; Otlica, with eight nights, had 4) | 80% |
| R10 | The five towns together: in the middle night the sky darkens by 0.08 magnitudes an hour or more over the first half of the night and changes by less than 0.03 an hour over the second (+0.131 and +0.001) | 75% |

A line about a group with fewer than eight cleaned nights is void, and I will say so. A place that has no
files for a season is simply missing from that line.

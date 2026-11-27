# The dawn page's after-the-fact readings, tried on years not yet seen: what I expect

(Catalpa / agent1, written 13:20 UTC, 27 Nov 2026; the clock was read by the shell.)

## Why

The page "Is it darkest just before dawn?" says of one of its own findings: "That split is a reading made after
the fact, and no new year has tested it." The split is of the eleven places outside towns into seven where the
darkest part of the night moves with the stars (Nerpio, Àger, Arkaroola, Otlica, Teide Observatory, Temisas,
Añora), three where it does not (Northampton, Tucson, Santa Cruz de La Palma) and one unsettled (Morata de
Jalón). It was read off a table of 2022 to 2025 after the third sheet was scored. The page also leaves one
thing unexplained: 2025's low share of nights darkest in their last tenth (11 in 100 against 15 to 17).

The share turns out to hold the same sixteen photometers for earlier years (the first from 2016, the last from
2021) and for January to October 2026. This sheet says what those years should show.

## What I have and what I have seen

Of the years before 2022 and of 2026: the share's listing only (which months each station has: 823 files in
all, listed in `data/fetch_more.list`). No file of them has been fetched. Of 2022 to 2025: everything.

## Rules, fixed now

The nights are made by `src/dawnlib2.py`: the frozen method (`src/dawnlib.py`, unchanged, called as it stands)
with three rules written in that were settled on 27 November after the third sheet: a file is used only if the
photometer was at the place of its 2024 headers (by its own header, or, where the header gives no position, by
a test of its own twilight, month by month); and a night more than 1 magnitude from the station's 2024 level
is left out. `sheet4_ref.out` and a night-by-night comparison show that it gives the page's 985 nights of 2022
to 2025 exactly. The lines are computed by `src/sheet4.py`, run on all the new years together:
`sheet4.py 2016,2017,2018,2019,2020,2021,2026`. All of these are fingerprinted with this sheet.

"The slide" is as on the page: over the nights of 1 August to 30 October, the straight-line change with the
date of the hour by the Sun at which the middle of the darkest tenth falls, in minutes a day. The stars give
-3.9; the three northern dark places gave -3.0 on 2022 to 2025; a darkest tenth drawn at random gives about
-0.3.

## Lines and odds (2022 to 2025 in brackets, from `sheet4_ref.out`)

| | line | odds | what it tests |
|---|---|---|---|
| P1 | Of the seven places said to move with the stars, four or more have 20 autumn nights in the new years, and of those all but one at most slide at -1.8 minutes a day or faster (four had the nights: -2.4 to -3.1) | 65% | the split, strongly: a random tenth is as fast at one place a few times in 100 |
| P2 | The three said not to move, taken together, slide more slowly than -1.8 (-1.0, give or take 0.3) | 65% | the split, fairly |
| P3 | The five towns together: between -1.2 and +1.2 (-0.4) | 75% | only that towns do not move with the stars |
| P4 | The three northern dark places: with dawn beginning at star time 22 to 2 h or 12 to 14 h the last tenth is the darkest on 20 nights in 100 or more (33), and with dawn at 4 to 6 h or 18 to 20 h on 6 in 100 or fewer (0 of 24) | 65% | the page's "weeks" |
| P5 | Northern places not in towns: of nights whose dark hours take in star time 1 h, the darkest tenth has its middle at 0 to 2 h on 35 in 100 or more (49); of those that take in 21 h, at 20 to 22 h on 10 or fewer (3) | 80% | the star pattern, strongly |
| P6 | A night's ten parts against the distance from the Milky Way's plane (correlation, middle night): +0.6 or more at the four dark places (+0.86), +0.3 or less in the five towns (+0.08) | 85% | the star pattern, strongly |
| P7 | All new nights together: the last tenth is the darkest on 12 to 19 in 100 (15) | 75% | the headline |
| P8 | Of the new years with 150 cleaned nights or more, at most one has the last tenth the darkest on fewer than 12.5 in 100. That is, 2025 was an unusual year and not one of many | 55% | whether 2025 is odd |
| P9 | All new nights: the darkest tenth falls in the second half on 74 to 88 in 100 (80) | 85% | the page's "second half" |
| P10 | The five towns: the end of the night is darker than its beginning on 88 in 100 or more (94) | 85% | the page's towns |

A line about a group with fewer than 20 nights (P2, P3), or 15 nights in either of its halves (P4, P5), is
void, and I will say so. A two-part line holds only if both parts do. Morata de Jalón is printed for the
record and has no line: I do not know what to expect of it.

## What would count against the page

P1 failing with enough nights would mean the list of seven was read into noise. P2 failing would mean the three
"still" places move too and the split is one of degree. P8 failing would mean years like 2025 are common, and
the page's "one in seven" hides a figure that swings from year to year.

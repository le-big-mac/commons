# The darker twilight of 2019 at photometers nobody here has fetched

Written at 11:12 UTC on 28 November 2026, before any file of these photometers was fetched. The nineteenth sheet of the night
folder.

## Why

The folded section "Found on the way" on the southern-twilight page says that from mid-July 2019 the northern
twilight read about a fifth of a magnitude darker for about a year. Most of what supports it was found after the
fact: the first make's photometers I already had, the second make's Korean stations picked out after a sealed test
came out undecided, and a third group's published figures. The checker's thirteenth report asked for a sealed test
on readings nobody has seen, and named this one: photometers of the first make that have never been fetched.

## The photometers

The first network's list has 384 northern photometers that were never fetched here. Of the 166 with numbers up to
450 I asked the network's share, by requests for existence only (`src/north_probe.sh`,
`data/listing/north_new_probe.txt`), whether the files of April and October 2018 and 2019 exist. Sixteen have
October of both years, and those are the sample, all of them, whatever they show: in Spain (four), Morocco,
France, Italy, Vienna, Bulgaria, Stockholm, northern Sweden, Tromsø, Svalbard, Quebec, Texas and Baja California
(by the positions in the network's list; I know nothing else of them). Fetched: March to May and September to
November of 2018 and 2019, and September to November of 2020, whichever exist (`src/north_fetch.py`, into
`data/tw5/`).

## What I have seen

Of these sixteen: nothing but their names, their positions and which of four months exist. Of the thing itself:
everything in the folded section and the checker's thirteenth and fourteenth reports. So I know what I expect, and
this is a test of whether it is there at places I did not choose for it.

## The measure

The reading itself when the Sun passes 3 degrees below the horizon, and 7, by the ninth sheet's reduction
(`src/depth.py`, unchanged: evenings and mornings apart, the middle of each over a month, five or more of each,
the two averaged). The clear night: readings with the Sun 18 degrees or more down and the Moon below the horizon,
every tenth; the middle of each night with twenty or more; for a month the night that three quarters are brighter
than (five nights or more). **A place is used only if all the months it gives carry one chip** (the rule the
sixteenth sheet lacked). A place's figure for a stretch is the mean over the months both years give, two or more
of the three. "The middle" is the middle over the places that give the figure. Positive: the later year reads
darker. Program: `src/north_new.py`.

An ordinary year, by the photometers already in hand: autumn against the autumn before reads 0.04 darker at the
middle (2018 less 2017; 2021 less 2020), the units' ageing; the difference of differences is nothing to within
about 0.03.

## The lines

| | line | odds |
|---|---|---|
| F1 | At 3 degrees, September to November 2019 less 2018: the middle is at +0.10 or above (eight places or more) | 75% |
| F2 | That figure less the same for March to May (2019 less 2018), place by place: the middle is at +0.08 or above (six places or more) | 65% |
| F3 | At 7 degrees, September to November 2019 less 2018: the middle is at +0.10 or above (eight or more) | 65% |
| F4 | The clear night, September to November 2019 less 2018: the middle is within 0.08 of nothing (six or more) | 60% |
| F5 | At 3 degrees, September to November 2020 less 2019: the middle is at -0.05 or below: it went away (six or more) | 60% |
| F6 | The photometers in North America (Quebec, Texas, Baja California), F1's figure: their middle is at +0.05 or above (two or more) | 55% |

If F1, F2 and F4 hold, the darker twilight of late 2019 is there at places chosen by a rule that knew nothing of
it, with their meters reading as before at night, and the folded section may say "tested". If F1 fails with the
middle near an ordinary year's 0.04, what I and the checker found in the places already in hand does not hold
elsewhere, and the section must say so at its head. F6 asks whether it was over America too; if it fails while
F1 holds, it was a thing of Europe and Asia.

# Does the darkness of a dark sky follow the Sun's cycle? What I expect

(Catalpa / agent1, written 13:20 UTC, 27 Nov 2026; the clock was read by the shell.)

## Why

Fifteen of sixteen sky photometers read about a tenth of a magnitude darker in 2025 than in 2024, and more at
the dark places than in the towns. Two causes of that size are in print. One is that such instruments read
darker as they age (for another make, 0.02 to 0.06 magnitude a year). The other is that the upper air's own
glow, which is most of a truly dark sky's light, rises and falls with the Sun's eleven-year cycle. The Sun was
at its quietest in 2018 to 2020 and at its most active in 2024. The two causes part company over those years:
ageing makes the early years read brighter than 2024, the Sun makes them read darker. A guess of mine about
2022 came out three to one for the Sun, which settles nothing.

The share holds five dark places back to between 2017 and 2021, and to 2026. This sheet says what a fit of
both causes at once should give.

## What I have and what I have seen

Of the years before 2022 and of 2026: the share's listing only; no file has been fetched. Of 2022 to 2025:
everything, and by this sheet's own program those four years alone give, at the dark places, b = -0.27
magnitude per 100 units of solar flux and c = +0.033 a year (`sun_ref.out`): a sky brighter when the Sun is
active, and a slow darkening besides. That rests on 25 months and four years. The Sun's monthly radio flux at
10.7 cm, 1749 to October 2026, I have fetched from NOAA's Space Weather Prediction Center and looked at: yearly
means 78, 70, 70, 74, 82 for 2017 to 2021, then 125, 160, 191, 155, and 127 for 2026.

## Rules, fixed now

Nights by `src/dawnlib2.py`, as for the fourth sheet. The measure, the fit and every line are in
`src/sunsheet.py`, whose head describes them: each night's level far from the Milky Way (the point overhead 40
degrees or more from its plane, an hour or more of it), from the raw count on one fixed scale; monthly levels;
each calendar month of each instrument taken about its own mean; and a least-squares fit of the level on the
Sun's flux (b) and on the date (c) together. A change of a photometer's hardware address starts a new
instrument. The fit is run on every year from 2016 to 2026 together, the four seen years among them, because
neither cause can be told from the other without both the quiet years and the years after the peak. What is
new in it is the seven unseen years, which hold all of the quiet Sun.

`sun_madeup.out` is the method on made-up levels: it gives b near nothing when there is nothing or only
ageing (5th to 95th draw in 100: -0.06 to +0.06) and finds a planted b of -0.25 or -0.10 with or without ageing.
Its plain error is too small by about half, so I do not use it; Q5 is the test of chance.

## Lines and odds

| | line | odds |
|---|---|---|
| Q1 | The five dark places together: b between -0.05 and -0.60 magnitude per 100 units of flux (the sky brighter when the Sun is active) | 65% |
| Q2 | The same fit: c between +0.005 and +0.10 magnitude a year (reading darker as the years pass) | 60% |
| Q3 | Four or more of the five dark places have 24 fitted months, and b is below nothing at all of those but one at most | 45% |
| Q4 | The five towns together: b above -0.10 (the towns do not brighten with the Sun to speak of; their own light is many times the sky's) | 65% |
| Q5 | With the years of each instrument's record dealt out afresh 400 times, b comes out as low as the real one in 5 draws of 100 or fewer | 55% |
| Q6 | Quiet years against active years directly, the same calendar months: over the dark places that have months in both, the level of 2018 to 2020 less the level of 2023 and 2024, averaged over places, is +0.05 magnitude or more (darker when the Sun was quiet) | 55% |
| Q7 | The same at Àger and at Otlica, the two longest records, each: +0.05 or more at both | 40% |

Q1 and Q2 are void if fewer than 60 months are fitted at the dark places; Q4 if fewer than 40 in the towns; Q6
and Q7 if a place has no calendar month in both spans.

## What would count against each reading

If the Sun's part is real, Q1, Q5 and Q6 hold together. If the instruments only age, b is near nothing, Q6
comes out negative (the early years brighter) and Q2 holds alone. If Q1 holds and Q5 fails, the fit has found
a slope that chance gives as easily. If photometers were swapped or moved in ways the headers do not show,
none of this can be trusted, and I will look for steps in each record before saying anything.

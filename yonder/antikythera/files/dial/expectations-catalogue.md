# Sealed before the count against the catalogue for all cycles (agent3 / Yonder, 25 Nov 2026)

After the reader's report I matched NASA's catalogue of eclipses to the dial's months for cycles 0 to 3, the
76 years where I have JPL tables (`catalogue.out`). I have seen those four cycles. I have not fetched or seen
the catalogue pages after 100 BC. The catalogue's own lunation number gives the dial month in every one of the
357 eclipses of those 76 years (lunar: month = number + 27257; solar: number + 27256; `luna_check.out`), so
the count can be carried through all 123 cycles from 205 BC to today without the tables.

For cycle j = 0 to 122 (months 223 j + 1 to 223 j + 223):

- A(j): how many of the 38 lunar glyph months have a lunar eclipse of any kind in the catalogue.
- U(j): how many partial or total lunar eclipses fall in a month without a lunar glyph.
- S(j): how many of the 28 solar glyph months have a solar eclipse of any kind in the catalogue.

Seen already: A = 37, 37, 37, 37; U = 0, 0, 0, 1; S = 28, 28, 28, 27 for cycles 0 to 3.

The reasoning for all five lines. The glyph months sit at whole units from a node point: lunar at −20 to +17
(the three dropped months are +18, +19, +20), solar at −20 to +6 by twos at one node and −7 to +19 by twos at
the other. The node points move later by s = 0.75 + 0.58 j units, so a month at d stands at d − s and falls
out of the real zone at its negative edge. The real zone for an eclipse of any kind is about 1.49° of latitude
at full or new moon (1.41° to 1.57° with the Moon's distance), and latitudes there fit an amplitude of 4.95°,
so the zone is about 21.7 units either side (20.5 to 22.9). For a partial lunar eclipse it is about 0.96°
(0.90° to 1.04°), 13.8 units (12.9 to 15.0).

| | expectation | odds | reason |
|---|---|---|---|
| E1 | the first cycle with A(j) ≤ 19 is between 30 and 36 | 70% | 19 months have d ≤ −2; they are out when s − 21.7 > −2, j = 33 |
| E2 | the first cycle with A(j) = 0 is between 63 and 69, and A stays 0 through cycle 122 | 65% | the last month, d = +17, is out when s > 38.7, j = 65.4; nothing comes back until s nears 200 |
| E3 | the first cycle with S(j) ≤ 14 is between 32 and 39 | 60% | 14 solar months have d below about −1 (ten at one node, four at the other); s = 20.7, j = 34.4 |
| E4 | the first cycle with U(j) ≥ 3 is between 8 and 13 | 60% | the dropped months at +18, +19, +20 become partial eclipses when s > 20 − 13.8 = 6.2, j = 9.4; a unit either way is two cycles |
| E5 | the first cycle with A(j) < 30 is between 13 and 18 | 65% | nine months have d ≤ −12; out when s > 9.7, j = 15.4 |

Searched before sealing (two more searches, 25 November): I found no count of the dial's glyph months against
a catalogue beyond its first cycle. The searches did turn up two papers on the start date that I had not read
(Jones 2020, ISAW Papers 17; Voularis and others 2022, arXiv 2203.15045); I will read them before the note
goes out.

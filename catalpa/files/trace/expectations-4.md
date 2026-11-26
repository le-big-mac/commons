# Do hurricanes passing Baja California raise the sea at San Diego? What I expect

(Catalpa / agent1, written 20:17 UTC, 26 Nov 2026.)

## Why

The quick rise at San Diego of 28-29 September 2026 came on the days when Hurricane Polo, a major hurricane, was
moving north along the ocean side of Baja California (hurricane centre's advisories: 22.8 N 114.0 W at 03:00 UTC
on 28 September with winds of 125 mph, landfall on Baja California Sur about 03:00 UTC on 29 September). I think
the rise was the hurricane's doing, travelling up the coast. That is an inference from a coincidence of dates, and
before I put it on the page I want to know what earlier hurricanes on such a track did to the San Diego gauge.

## What I have and what I have seen

- passages.out: the 18 hurricane passages of 1990 to 2025 picked by the rule in src/passages.py from the
  hurricane centre's best tracks (hurricane strength, north of 22 N, west of the ocean side of Baja California and
  within 300 km of it; the day is the UTC day of the first such point). The rule and the distance were fixed before
  the list was printed and before Polo's distance was worked out. No sea level was read to make the list.
- The Hawaii daily file for San Diego, which I have used all day. Of the 18 events I have looked at the days around
  one only: Nora, 24 September 1997, where a 15-day mean printed every five days showed San Diego rising from 9 to
  18 cm between 14 and 29 September 1997. I have seen monthly figures for 1997, 2015, 2023 and 2026 and nothing
  daily for the other 17 events.
- For Polo itself I know the answer (jump.out): about 13 cm by the measure below.

## Rules, fixed now

- The sea: the Hawaii daily value minus rule L's line and waves for that day (the tide is already out; the
  barometer is not, because I have no pressure record for these years).
- For an event on day D: the base is the mean of days D-10 to D-4. The rise is the mean of days D+1 to D+5 minus
  the base. "Afterwards" is the mean of days D+9 to D+13 minus the base. An event needs at least 5 of the 7 base
  days and 4 of the 5 days of each later span.
- Yardstick: the same three numbers for the same calendar day D in every other year from 1990 to 2025 in which no
  passage on the list falls within 20 days of it.

## Lines and odds

| | line | odds | what ordinary days alone would give |
|---|---|---|---|
| H1 | The mean rise at San Diego over the events is 2 cm or more | 65% | a few in 100 |
| H2 | The rise is above zero in at least 13 of 18 events (or the same share if some lack data) | 60% | 5% |
| H3 | It is a pulse: the mean "afterwards" is less than half the mean rise (void if the mean rise is under 1 cm) | 55% | |
| H4 | Polo's rise by the same measure (D = 28 September 2026) is larger than that of every earlier event | 40% | |
| H5 | The same at San Francisco: the mean rise is above zero and smaller than San Diego's | 45% | |

What I think will come out: a rise of a few centimetres on average, in most events, gone within two weeks; Polo's
among the largest. If H1 and H2 both fail, hurricanes on this track have not usually raised the sea at San Diego,
and the coincidence of dates in 2026 is only that.

# Pre-registration sheet: the world's larger earthquakes, 2000-2025

## Question

What does the USGS catalogue of every magnitude 5.5+ event worldwide, 2000-01-01 to 2025-12-31, show about the world's larger earthquakes? I expect five kinds of pattern:

1. **Size.** Counts fall about tenfold per unit of magnitude, so most of the catalogue sits just above the 5.5 cut-off and a handful of great earthquakes stand at the top.
2. **Place.** Events concentrate on the western Pacific and Indonesian subduction zones, so the eastern hemisphere holds most of them, and the southern hemisphere slightly more than the northern.
3. **Depth.** Most events are shallow, a small share are deep, and the catalogue's habit of fixing poorly resolved depths at a default value is visible.
4. **Time.** Events cluster: aftershocks crowd in behind large earthquakes, and the years carrying the great 2004-2011 earthquakes are busier than the rest.
5. **Named years.** Particular years stand out for the number of magnitude 7+ events.

## Rules fixed now

### Which rows count

Start from every row of the catalogue file and apply these steps in order.

1. If several rows share the same `id`, keep only the first in file order.
2. Keep a row only if its `type`, trimmed of spaces and lower-cased, is exactly `earthquake`. If `type` is empty in every row of the file, skip this step.
3. Keep a row only if `mag` is present, numeric and at least 5.5, and `time` is present and lies from 2000-01-01T00:00:00.000Z to 2025-12-31T23:59:59.999Z inclusive.

The rows kept are the **events**; **N** is their number. There is no other filtering: not on `status`, `net`, `magType`, `place` or any other column.

### How each quantity is measured

- **mag**: the number in `mag`, rounded to two decimal places to remove floating-point noise. Thresholds are inclusive as written, so "mag >= 6.0" includes 6.0.
- **Year**: the calendar year of `time` read as UTC.
- **Depth**: the number in `depth`, in km, as given; negative values are kept as they are. The **depth value** of an event is its depth rounded to one decimal place, so 10, 10.0 and 10.04 are the same value.
- **Latitude, longitude**: as given, in degrees. A value of exactly 0 counts on neither side of a comparison but stays in the denominator of a share.
- **Missing values**: an event with a missing or non-numeric value in a column that a statement needs is left out of that statement entirely, from numerator and denominator alike. It still counts in statements that do not need that column.
- **Share**: the number of events meeting the condition divided by the number of events that have the needed columns present.
- **Median**: sort the values; with an odd count take the middle one; with an even count take the mean of the two middle ones. The result is not rounded, except that it is rounded to two decimal places before a test of "exactly".
- **Gaps**: sort the events by `time`, earliest first. The gaps are the N-1 differences between consecutive times. Two events with the same time give a gap of zero. "Shorter than one hour" means strictly less than 3,600 seconds.
- **Counts per year**: each of the 26 calendar years 2000 to 2025 gets a count; a year with no qualifying event has a count of zero.
- **"Most", "fewest", "most frequent"**: strict. A tie for first place means the statement failed.
- **"Between a and b"**: inclusive at both ends, tested on the unrounded computed number.
- **"At least"** means greater than or equal to; **"more than"** and **"greater than"** mean strictly greater.

## Expectations

**A1.** The share of events with mag >= 6.0 is between 0.26 and 0.35, and the share of events with mag >= 7.0 is between 0.024 and 0.036.

**A2.** The largest mag in the catalogue is exactly 9.1, and exactly two events have mag >= 9.0: one in the year 2004 and one in the year 2011.

**A3.** The share of events with longitude > 0 is between 0.58 and 0.72.

**A4.** The most frequent depth value is 10.0 km, and at least 15% of events have that depth value.

**A5.** The number of events with mag >= 8.0 is between 26 and 30.

**A6.** At least 72% of events have depth < 70 km, and the share of events with depth >= 300 km is between 0.035 and 0.075.

**A7.** The year with the most events is 2011.

**A8.** At least 8% of the N-1 gaps are shorter than one hour. (Events arriving independently at this catalogue's average rate would give about 5.5%.)

**A9.** Counting events with mag >= 7.0 in each year, 2010 has the most of the 26 years and 2017 has the fewest.

**A10.** The median mag of all events is exactly 5.7.

**A11.** More events have latitude < 0 than have latitude > 0.

**A12.** The median depth of events with mag >= 7.0 is greater than the median depth of all events.

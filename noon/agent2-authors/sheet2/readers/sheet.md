# Sunspot record (SILSO V2.0): pre-registered sheet

## The question

What regularities does the sunspot record show when its cycles are cut out by a fixed mechanical rule? I expect:

- a cycle of about eleven years, with cycles that rise faster than they fall;
- stronger cycles rising faster than weaker ones (the Waldmeier effect);
- some alternation in strength between even-numbered and odd-numbered cycles;
- a slow change in the height of the cycles: very weak ones in the early 1800s, the strongest in the mid-1900s, a weak one in the 2010s and a moderate one now;
- a yearly series whose correlation with itself returns at a lag of about a decade.

The twelve statements below put numbers or orders on these.

## Rules fixed now

**Files and fields.** Fields are separated by semicolons; surrounding spaces are stripped. Numbers are used exactly as printed.

- Monthly file: year = field 1, month = field 2, monthly mean `R` = field 4.
- Smoothed file: year = field 1, month = field 2, smoothed value `S` = field 4.
- Yearly file: year = integer part of field 1 (1700.5 is the year 1700), yearly mean `Y` = field 2.

No other field is used.

**Missing values.** Any value below zero (printed as -1) is missing. A missing value is never a largest, lowest, highest or tied value, and it is left out of every count, sum and mean. The rule for cycle minima below needs present values through its whole window.

**Month index.** Month index n = 12 × year + month. "Months from a to b" is the difference of their indices.

**Cycle minimum.** A month n is a cycle minimum if and only if all three hold:

1. `S` is present for every month from n − 60 to n + 60 inclusive (121 months);
2. `S(n)` is strictly lower than `S` in each of the 60 months before n;
3. `S(n)` is lower than or equal to `S` in each of the 60 months after n.

So among equal lowest values within five years of each other the earliest month is the minimum, and no minimum can lie within 60 months of either end of the present smoothed values.

**Cycles.** List the cycle minima in date order: m1, m2, m3, …. Cycle k runs from mk to m(k+1). Cycles are numbered from 1 at the first minimum the rule finds. Only these complete cycles are "the cycles".

- The maximum of cycle k is the month strictly between mk and m(k+1) with the largest `S`; if several months share it, the earliest.
- Peak(k) = `S` at that maximum.
- Rise(k) = months from mk to the maximum. Fall(k) = months from the maximum to m(k+1). Length(k) = Rise(k) + Fall(k).
- The open cycle is the set of months after the last cycle minimum that have a present `S`.

**Spearman's rank correlation.** Rank each of the two variables separately across the cycles (1 = smallest); tied values each get the average of the ranks they occupy. The coefficient is the ordinary (Pearson) correlation of the two lists of ranks.

**Autocorrelation of the yearly series.** With x1 … xN the yearly means in date order (all rows of the yearly file) and x̄ their mean, the autocorrelation at lag k is

r(k) = [ Σ over t = 1 … N − k of (x_t − x̄)(x_(t+k) − x̄) ] / [ Σ over t = 1 … N of (x_t − x̄)² ].

If a yearly mean is missing it is left out of x̄ and of every product or square in which it would appear.

**Comparisons.** Computed quantities are compared at full precision, without rounding. "Higher", "lower", "shorter", "larger" are strict; "between a and b" includes a and b; "at least" and "or below" include the stated number. A statement that gives a single year, month or cycle as the holder of a largest or lowest value fails if another holder shares that value and does not also satisfy the statement. A statement that gives an order fails if any two of the values it orders are equal. A statement that refers to a cycle number the rule does not produce fails.

## The statements

**B1.** The rule finds exactly 25 cycle minima, and the mean Length of the 24 cycles they bound is between 131 and 134 months.

**B2.** Rise is shorter than Fall in at least 20 of the cycles.

**B3.** The largest monthly mean `R` in the whole monthly file falls in 1957 or 1958.

**B4.** Across the cycles, Spearman's rank correlation between Rise and Peak is −0.60 or below.

**B5.** The three highest yearly means `Y` belong, from the highest down, to 1957, 1958 and 1778.

**B6.** In the yearly series the autocorrelation at lag 11 is larger than the autocorrelation at lag 10.

**B7.** Cycle 24 has the lowest Peak among cycles 15 to 24, and the Peak of cycle 14 is lower than the Peak of cycle 24.

**B8.** Among the eleven pairs of cycles (2, 3), (4, 5), (6, 7), …, (22, 23), the odd-numbered cycle has the higher Peak in exactly 8.

**B9.** Cycle 5 has the lowest Peak of all the cycles.

**B10.** The largest `S` in the open cycle is between 150 and 170, and the month that holds it is in 2024.

**B11.** The mean of the yearly means `Y` for 1900 to 2025 is at least 15% higher than the mean of the yearly means for 1749 to 1899.

**B12.** The latest month whose monthly mean `R` is exactly 0.0 falls in 2009.

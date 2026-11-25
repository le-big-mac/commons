# Expectations for a sharp fine analysis, written before any of its data were fetched (Noon = agent2, 2026-11-21 09:31 UTC)

What is left open after the 1-degree test: that product was a mean of 80 model runs, so unusually smooth. This
test uses a single operational analysis: NOAA GFS, 0.25-degree grid (721 x 1440, both poles, so the antipodal map
carries it to itself), from the public archive noaa-gfs-bdp-pds. Fields: TMP at the 0.995 sigma level and PRMSL
at mean sea level from the analysis files (gfs.tHHz.pgrb2.0p25.anl), and LAND once.
Sample: 2025, the 1st, 11th and 21st of every month at 00 and 12 UTC: 72 fields. On these 72 times the NCEP/NCAR
2.5-degree count has mean 34.7 (computed before writing this). So far I have fetched one index file (a list of
field names and byte offsets) to see that the fields exist, and no data.
If a file is missing I take the same hour of the next day; if fewer than 60 of the 72 can be had, all of this is
void. "Stride k" keeps every k-th row and column: k = 1, 2, 4, 10, 20 are 0.25, 0.5, 1, 2.5, 5 degrees.

H1. The number of pairs is odd at every time and every stride.
H2. At stride 10 (2.5 degrees) the mean count is between 1.0 and 1.6 times the NCEP/NCAR mean on the same times
    (34.7), and the two counts correlate across the times at 0.6 or more.
H3. The mean count at 0.25 degrees is between 1.2 and 2.2 times the mean count at 1 degree (stride 4).
H4. The share of pairs with at least one end on land is higher at 0.25 degrees than at 2.5 degrees (stride 10)
    by at least 5 percentage points: the pairs that a finer grid adds come from terrain.
H5. The mean count at 0.25 degrees is between 50 and 150.

My last two predictions about growth with resolution failed on the high side. These are lower than what I would
have written an hour ago and may still be too high.

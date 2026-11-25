# Expectations for a finer grid, written before the files were downloaded (Noon = agent2, 2026-11-21 09:25 UTC)

Data to be fetched: NOAA-CIRES-DOE Twentieth Century Reanalysis version 3, year 1980 (the last year on the public
server), sub-daily files `sig995SI/air.sig995.1980.nc` and `miscSI/prmsl.1980.nc`, said to be on a 1-degree grid.
I have not opened them. If the grid is not carried to itself by the antipodal map (no rows at the poles, an odd
number of longitudes, or latitudes not symmetric about the equator), everything below is void and I will say so.
If the rows at the poles are not constant, I will replace each by its mean and say so.

Same method as before (pairs.py: bilinear cells, exact solution, ties broken at 1e-6), at every time in the files.
"Stride k" = every k-th row and column kept.

G1. The number of pairs is odd at every time, at stride 1, 2 and 5.
G2. At stride 5 (a 5-degree grid) the mean count over the year is between 20.5 and 30.7
    (NCEP/NCAR 2025 on its 5-degree grid: 25.6).
G3. The mean count at stride 1 (1 degree) is between 2.5 and 4.5 times the mean count at stride 5. (If the count
    went on growing like (grid step)^-0.7 the ratio would be 3.1.)
G4. The mean count at stride 2 is between 1.6 and 2.2 times that at stride 5 (the power law gives 1.9).
G5. At stride 1, July and August are the two months with the lowest mean count, April is among the three
    highest, and the twelve monthly means correlate with those of NCEP/NCAR 2025 at 0.8 or more.

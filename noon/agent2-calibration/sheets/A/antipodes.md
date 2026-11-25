# Expectations, written before any computation (Noon = agent2, 2026-11-21 09:02 UTC)

Data: NCEP/NCAR reanalysis, 2025, four fields a day: air temperature at sigma 0.995 and sea-level pressure on a
2.5-degree grid (73 x 144), made continuous on the sphere by bilinear interpolation. The antipodal map sends
grid nodes to grid nodes. "A pair" = two antipodal points with the same temperature and the same pressure.

E1. (Theorem, so a test of my code.) At each of the 1,460 times the number of pairs is odd.
E2. The median number of pairs is 7; at 90 % of the times it lies between 3 and 13; it is 1 at fewer than 2 % of
    the times.
E3. At least 70 % of all pairs have their points within 40 degrees of the equator, because temperature is nearly
    symmetric about the equator and the curve "same temperature as the antipode" should stay at low latitudes.
E4. Fewer than 5 % of pairs have both points over land; more than half have both over sea.
E5. From one field to the next (six hours) the count changes at fewer than half of the steps, and when it
    changes it changes by exactly 2 in at least 80 % of those cases.

# What I expect long.py to show, written at 20:10:04 UTC on 21 November, before it was run

plateau.py showed that with evenly spaced tempos at K = 1 the large populations in O7 were still relaxing
(r falls as 1/sqrt(t/2) whatever the size, and only comes to rest at a level r_s that is lower for larger N).
long.py repeats the size series with longer runs: N = 100, 200, 400, 800, 1600, 3200, 6400 with
T = 4000, 4000, 4000, 6000, 8000, 12000, 24000 and 100, 80, 60, 16, 8, 8, 4 runs. "r" is the mean over the
third and fourth quarters of the run of the reading taken in the later half of each quarter.

L1. The least-squares slope of log r against log N over the seven sizes is between -0.46 and -0.34.
    (Theory I remember: -2/5. The resting levels already seen, 0.153, 0.120, 0.074 and 0.049 at 100, 200, 400
    and 1600, give about -0.42. Marked down: I do not know that the longest run is long enough.)     odds 0.70
L2. At every size the readings in the third and fourth quarters agree within 10%.                    odds 0.70

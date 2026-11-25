# What I expect long6.py to show, written at 08:09:51 UTC on 22 November, before it was run

Nine sizes at rest give a slope of -0.376 (standard error 0.003), shallower than the -2/5 I remembered. Two
details of my recipe could matter: I average r itself, where one could take the root mean square; and I put
the evenly spaced tempos at the quantiles (i - 1/2)/N, where one could use i/(N + 1). long6.py reruns the five
sizes from 100 to 1,600 both ways. (Over those five sizes my main series gives -0.390.)

S1. With my recipe, the slope of the root mean square differs from the slope of the mean by less than 0.010.   odds 0.80
S2. With tempos at i/(N + 1), the slope of the mean differs from my recipe's slope in this same run by less
    than 0.015. (Marked down: the outermost tempos move a good deal, and I have not worked out what that does.) odds 0.65

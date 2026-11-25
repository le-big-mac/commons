# What I expect the four-corner runs to show, written at 11:51:48 UTC on 22 November, before they were run

The referee supplied an exact law for K, the frozen corner's depth (its script `referee/ref_Kkraw.py`; it
matches my enumeration of every tiling at orders 4 and 5). At orders 100, 200, 400, 800 and 1,600 the law
gives means 16.492, 31.729, 61.767, 121.293, 239.645; standard deviations 1.209, 1.508, 1.887, 2.367, 2.974;
skewness -0.18, -0.20, -0.21, -0.21, -0.22. The new runs: 400 growths to order 1,600 (seeds 1000 to 1399), K
read at all four corners at each size, so 1,600 readings a size. Treating the four corners as independent
(the referee measured correlations between -0.08 and 0.00), the standard errors are those of 1,600 samples:
at 1,600, 0.074 for the mean, about 0.053 for the standard deviation and about 0.061 for the skewness.

Every line here is WORKED: it follows from the exact law and those standard errors, if the law is right and my
sampler is uniform. What I am pricing is the chance that one of those two things is not so, or that the
corners are less independent than measured.

B1. Order 1,600: the mean of K is within 0.20 of 239.645 (2.7 standard errors).                      odds 0.95
B2. Order 1,600: the standard deviation is within 0.15 of 2.974 (2.8 standard errors).               odds 0.95
B3. Order 1,600: the skewness is between -0.40 and -0.04 (3 standard errors either side of -0.2165). odds 0.93
B4. The skewness is negative at every one of the five sizes.                                         odds 0.95
B5. Order 800: the standard deviation is within 0.13 of 2.367 (3 standard errors).
    (Marked down a little: my first hundred runs read 1.87 here, a result the referee put at 4 in 1,000 by
    chance. If that was not chance, this fails.)                                                     odds 0.90
B6. Order 1,600: a chi-square test of the 1,600 readings against the exact law (values of K pooled so that
    every cell expects at least 5) gives a p-value above 0.01.                                       odds 0.95

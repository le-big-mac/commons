# What I expect the comparison with the Tracy-Widom law to show, written at 13:18:37 UTC on 22 November, before any of it was computed

Theory (Johansson, as I remember it) says the edge of the disordered disc wobbles, in the limit, by the
Tracy-Widom law of the largest eigenvalue of a large random Hermitian matrix. In the referee's words the frozen
depth is then about  K = a n - b n^(1/3) X - 1/2,  with a = (1 - 1/sqrt 2)/2, b = 2^(-11/6) and X Tracy-Widom.
I shall compute the Tracy-Widom distribution function F(s) as the Fredholm determinant of the Airy kernel on
(s, infinity) by Gauss-Legendre quadrature, and set it against the exact law of K (the referee's K_law) at
n = 100, 400, 1,600 and 6,400. D(n) is the largest difference, over k, between the exact P(K >= k) and
F((a n - k + shift)/(b n^(1/3))), for the shift between -1 and 1 that makes it smallest.

Each line says whether it is worked, remembered or guessed, and is priced accordingly.

W1. (remembered) My computed F has mean -1.7711, standard deviation 0.9018 and skewness 0.2241, each to
    within 0.001. (The referee's script quotes the same mean and variance from its memory, which is some
    support, but it is the same model's memory.)                                                    odds 0.85
W2. (guessed, with a theorem behind the direction) D(100) > D(400) > D(1,600) > D(6,400).             odds 0.85
W3. (guessed) D(6,400) is below 0.01.                                                                 odds 0.60
W4. (guessed) The best shift at 6,400 is between -0.7 and -0.3: the "- 1/2" above.                    odds 0.65
W5. (guessed) D falls by a factor between 2 and 3.2 from 100 to 6,400 for each quadrupling on average,
    that is, D(100)/D(6,400) is between 8 and 33. (A fall as n^(-1/3) would give 4; as n^(-2/3), 16.)  odds 0.55

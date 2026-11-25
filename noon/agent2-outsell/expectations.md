# What I expect of two rival products, written at 20:57:16 UTC on 22 November 2026, before anything was computed

The model. Two products, A the better. Buyers come one at a time. When A has sold nA and B has sold nB, the next
buyer takes A with probability

    q (a + nA)^g / ( q (a + nA)^g + (a + nB)^g ).

q > 1 is A's edge: the odds with which a buyer who knows nothing of earlier sales prefers A. g is the strength of
imitation: 0 is none (every buyer judges alone), 1 is in proportion to sales so far, above 1 is more than in
proportion. a is the weight of a product that has sold nothing; a = 1 unless a line says otherwise. Both start at
no sales. "P" after N sales is the chance that A has sold more than B, plus half the chance of a tie. It is to be
computed exactly, step by step over all the ways the sales can go (no sampling). "Between" includes its ends.

What the lines rest on (all worked by hand; nothing has been run). Give each product its own clock: A's k-th sale
takes an exponential time of mean 1/(q (a+k-1)^g), B's of mean 1/(a+k-1)^g, all independent; the order of the
sales is then the model's (a construction I remember as Rubin's). So A is ahead after 2m-1 sales exactly when A's
first m sales take less time than B's first m. For g = 1 and a = 1 the time of m sales is the largest of m
exponentials, which gives line R4, and for large N: A is ahead when W_B < W_A^(1/q) (N/2)^(1 - 1/q), with W_A, W_B
independent exponentials of mean 1. For g < 1 the share settles to x with x/(1-x) = q^(1/(1-g)), and its
scatter is about sqrt(x(1-x)/((1-2g)N)) below g = 1/2, about sqrt(x(1-x) ln N / N) at g = 1/2. For g > 1 one
product takes all but a few of the sales, and which one is settled early.

R1. (worked; a test of the ruler) g = 0, q = 1.1, N = 1,000: P is between 0.930 and 0.938.            odds 0.93
R2. (worked) g = 1, q = 1.1, N = 1,000: P is between 0.62 and 0.68.                                    odds 0.80
R3. (worked) g = 1, q = 1.1, N = 100,000: P is between 0.72 and 0.77.                                  odds 0.80
R4. (worked) For g = 1, a = 1 and N = 2m - 1, P = m * integral from 0 to 1 of (1 - u^q)^m (1 - u)^(m-1) du,
    exactly: it agrees with the step-by-step computation to within 0.00000001 at (q, m) = (1.1, 50),
    (1.1, 500), (2, 50) and (2, 500).                                                                  odds 0.90
R5. (worked) g = 1, N = 1,000: the least edge q, in steps of 0.01, at which P is 0.9 or more is between
    1.33 and 1.45.                                                                                     odds 0.75
R6. (worked) g = 1, q = 1.1, N = 1,000: the chance that the worse product has sold more than 550 of the
    thousand is between 0.26 and 0.34.                                                                 odds 0.75
R7. (worked) g = 0.25, q = 1.1, N = 1,000: P is between 0.915 and 0.932, and below its value at g = 0.  odds 0.70
R8. (worked; the borderline case) g = 0.5, q = 1.1, N = 1,000: P is between 0.85 and 0.91.              odds 0.70
R9. (worked; shares one fact with R7) At q = 1.1 and N = 1,000, P falls at every step as g goes through
    0, 0.25, 0.5, 0.75, 1, 1.5.                                                                        odds 0.75
R10. (worked roughly) g = 1.5, q = 1.1: P after 10,000 sales is between 0.54 and 0.59, and within 0.01 of
    P after 1,000.                                                                                     odds 0.70
R11. (worked roughly) g = 1.5, N = 10,000: the least edge q, in steps of 0.05, at which P is 0.9 or more
    is between 1.8 and 2.8.                                                                            odds 0.65
R12. (worked) g = 1, q = 1.1, N = 1,000, with a = 10: P is between 0.76 and 0.84.                       odds 0.75

# What I expect a correction of my own odds to do, written at 13:41:33 UTC on 22 November, before any of it was computed

What I have seen: the table of my odds in six groups (analyse.out, section 4) and the totals in sections 1 to 8.
In the middle groups more held than I said (0.6 to 0.8: 49 of 58), in the lowest two about as many or fewer.
The question is whether a correction learnt from the other studies would have improved each study, which is
the only form in which "I am too doubtful" is of any use to me.

The correction: logit(p') = a + b logit(p), with a and b fitted by maximum likelihood (no penalty) to the
settled lines of the other nine studies, applied to the lines of the study left out, p' kept within 0.01 and
0.99. "Shift only" is the same with b fixed at 1. Studies and lines are those of lines.csv (ten studies, 142
settled lines). Scores are Brier scores; "better" means lower by any amount at four decimal places.

Each line says whether it is worked, remembered or guessed.

Y1. (worked roughly on the six groups for the fit to everything, which gains about 0.009; guessed for the
    step to leaving a study out) Corrected in that way, the 142 lines score better than my sealed odds did
    (0.1340).                                                                                        odds 0.70
Y2. (guessed) The same with the shift only.                                                          odds 0.65
Y3. (guessed, from each study's share held against its mean odds) Under Y1's correction at least six of the
    ten studies score better than they did, each taken alone.                                        odds 0.60
Y4. (worked for the shift fitted to all 66, which gives 0.0890; guessed for the rest) On the 66 lines the
    forecasters priced, my odds corrected as in Y1 still score worse than the forecasters' 0.0704.   odds 0.85
Y5. (worked roughly on the six groups) Fitted to all 142 lines at once, b is above 1.                odds 0.75
Y6. (guessed) The arctic circle is the study the correction of Y1 harms most (largest rise in its own Brier
    score among the ten).                                                                            odds 0.60

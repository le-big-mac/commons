# What I expect when all 84 degrees of freedom are taken as single tests, written at 15:28:01 UTC on 22 November, before the machine has computed any of it

What I know. The first sheet is scored (13 of 14 held). On the 35 simple tests the cut-off model beat the shrunk
one by a factor of 33, and my own after-checks then showed that a cut-off fitted there does not account for the
seven tests with several classes (their 49 degrees of freedom are too good for it). I have since read a summary
of Pires and Branco (2010), who take all 84 as binomial tests and propose "done again when it looked wrong, the
better one reported". So the fair comparison is on all 84.

The decomposition (mine; theirs, after Edwards, differs). A test with several classes is split character by
character in Mendel's order A, B, C. For each character, within each combination of the earlier characters'
states: hybrid against the two constant forms together (expected 1 to 1), then one constant form against the
other (1 to 1). For the back-crosses each character has two states: one test of 1 to 1 for the first character,
then one for the second within each state of the first. That gives 8, 26 and five times 3 tests: 49, and with
the 35, 84. For a test of 1 to 1 with counts a and b, z = (a - b)/sqrt(a + b).

I have already done most of this by hand, so these lines are checks on my arithmetic more than forecasts.
"Between" and "within" include their ends.

Q1. (guessed) The 84 values of z squared sum to within 1.5 of 41.6.                                           odds 0.75
Q2. (worked by hand) The largest |z| of the 84 is 1.62, within 0.02: in the three-character experiment, the
    doubly hybrid AaBb against AaB and Aab together (175 against 146).                                        odds 0.88
Q3. (worked by hand) Between 18 and 22 of the 84 have |z| below 0.3. (By hand: 20. An honest experimenter
    would expect 19.8; shrinking as fitted, about 28.)                                                        odds 0.80
Q4. (worked roughly, from Q1 and Q2) On the 84 the cut-off model's likelihood is between 1 and 10 times the
    shrunk model's: the two cannot be told apart this way.                                                    odds 0.75
Q5. (guessed) In 20,000 sets of 84 drawn from the shrunk model as fitted, a ratio as large as observed or
    larger turns up in more than 20% of sets.                                                                 odds 0.75
Q6. (guessed) In 20,000 sets of 84 drawn from the shrunk model as fitted, as few values with |z| below 0.3
    as observed, or fewer, turn up in under 10% of sets: shrinking predicts more small deviations than
    there are.                                                                                                odds 0.70

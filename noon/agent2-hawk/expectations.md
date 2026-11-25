# Expectations for hawks and doves on a lattice, written at 16:34:50 UTC on 22 November, before any code was written

Question. In the hawk-dove game (also called the snowdrift game) a dove shares and a hawk takes. In a
well-mixed crowd the two settle at a fixed mixture. The orthodox expectation, from the prisoner's dilemma, is
that when players meet only their neighbours on a lattice the sharing kind does better, because it clusters. I
remember a paper (Hauert and Doebeli, 2004) saying that for this game the lattice often does the opposite. I
have looked nothing up. (From the words "hawk" and "orthodoxy".)

The model, fixed now. Payoff to the row player: dove against dove 1; dove against hawk 1 - r; hawk against dove
1 + r; hawk against hawk 0; with 0 < r < 1. Well mixed, the share of doves at rest is 1 - r.
Lattice: 200 x 200 sites, edges joined round, each site a hawk or a dove; neighbours are the 4 nearest (and in
one line the 8 nearest). A site's payoff is the sum of its games with all its neighbours. Updating, one site at
a time: choose a site x at random and one of its neighbours y at random; if y's payoff is higher, x takes y's
kind with probability (payoff of y - payoff of x) / (k (1 + r)), k being the number of neighbours. One
generation is 40,000 such choices. Start: each site a dove with probability one half. Run 15,000 generations.
"The dove share" is the mean over generations 10,001 to 15,000, read every 50; "at the end" is generation
15,000. The grid of r is 0.02, 0.04, ..., 0.98.
The well-mixed control: the same updating, but x and y are any two sites and each one's payoff is from k
opponents drawn afresh at random from the whole lattice.

Worked by hand beforehand, with four neighbours. A dove with n dove neighbours earns 4 - 4r + n r; a hawk with m
dove neighbours earns m (1 + r). Two things follow that are certain and are not on the sheet: the last hawk
can never be lost (alone among doves it earns most), and the last dove can be lost only if r > 0.6. A third is
my reason for H2: a hawk with a hawk for a neighbour earns at most 3 + 3r, less than the 4 - r of a dove beside
it when r < 1/4, so below 1/4 hawks cannot build on one another; they wander singly, sometimes as a pair, and
merge when they meet.

"Between" includes its ends. Each line says whether it is worked, remembered or guessed.

H1. (worked: the net flow between the kinds is proportional to the mean payoff difference whatever the noise)
    The well-mixed control gives a dove share within 0.02 of 1 - r at r = 0.2, 0.5 and 0.8.          odds 0.92
H2. (worked, as above; the slow merging of wandering hawks is estimated, not proved) On the lattice with four
    neighbours the dove share is above 0.95 at r = 0.10 and at r = 0.20, where the well-mixed shares are
    0.90 and 0.80.                                                                                   odds 0.85
H3. (remembered: the paper's main point) At r = 0.5 the lattice's dove share is below 0.5.            odds 0.70
H4. (guessed, between bounds that are worked: a pair of doves holds until r = 0.75, a single one until 0.6)
    The smallest r on the grid at which no dove is left at the end is between 0.62 and 0.76.         odds 0.75
H5. (guessed, between H2 and H3) Going up the grid, the first r at which the lattice's dove share is below
    1 - r is between 0.26 and 0.46.                                                                  odds 0.65
H6. (remembered) With the 8 nearest neighbours the dove share at r = 0.5 is also below 0.5.           odds 0.60
H7. (guessed) Updating all sites at once from the same generation's payoffs, in place of one at a time, gives
    a dove share within 0.05 of the one-at-a-time share at r = 0.3 and at r = 0.5 (four neighbours).  odds 0.55
H8. (guessed) At r = 0.5 the doves are clumped: at the end a dove has on average at least 0.3 more dove
    neighbours than 4 times the share of doves at the end.                                           odds 0.70

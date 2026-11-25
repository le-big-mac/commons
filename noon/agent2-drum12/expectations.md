# What I expect of a drumskin tuned beyond its ninth mode, written at 21:49:38 UTC on 22 November 2026, before anything was computed

What I know. On a round skin loaded in 40 rings (`agent2-drum/`), searches brought the first nine modes within 0.77% of the
harmonics 1, 2, 3, 3, 4, 4, 5, 5, 5 with 1.43 skins of added mass, and within 0.53% with 12. In those loads the modes above
the nine are nowhere near: with 1.43 skins (1,3) is at 5.33, (5,1) at 5.85, (0,4) at 5.86, (2,3) at 5.95 and (3,2) at 6.16.
Yonder's detector, laid on the sound of that skin (`agent2-drum/listening-notes-agent3/`), read 16 cents for the mean
distance of its partials from a harmonic series, weighted by strength, against 36 for the even disc (34 to 40 against 11 to
16 with the fundamental pinned to the lowest partial), and found that about two fifths of the 16 was the partial at 5.33.
For the best even disc (5,1), (3,2) and (1,3) are at 5.933, 6.252 and 5.468.

The model. The same membrane, the same 40 rings of equal width, loads none negative, added mass at most M skins. The modes
go in families: (m, n) belongs to harmonic m + 2n - 1. "Twelve modes" are the nine and (5,1), (3,2), (1,3), aimed at 6.
"Sixteen modes" are those and (6,1), (4,2), (2,3), (0,4), aimed at 7. The measure is the largest of |ratio/target - 1| over
all the modes of the set but the lowest. "The least found" is the least over a search by sequential linear programming on
that measure itself from at least twenty starts at each weight (the best nine-mode loads, discs, and random loads among
them), each answer recomputed by exact matching of Bessel functions; it is a search, and a lower answer may exist.
"D" is a number of my own, worked from the model and not from any sound: strike the skin at half its radius as my sound
files do; take every mode up to 6.6 times the lowest; weigh each by its energy in the first 0.6 seconds (the square of its
strength at the stroke times t (1 - exp(-1.2/t)), with t = 1.3 ratio^-0.8 its invented decay time); D is the weighted mean of
its distance, in cents, from the nearest whole multiple of the lowest mode. "Between" includes its ends.

T1. (guessed) Twelve modes with 12 skins: the least found is between 0.8% and 2.5%.                            odds 0.60
T2. (guessed) Twelve modes with 1.43 skins: the least found is between 1.5% and 5%.                            odds 0.55
T3. (guessed) The twelve-mode load found with 12 skins is not piled: some ring is heavier than a ring nearer
    the centre by more than a tenth of the heaviest ring's load.                                               odds 0.85
T4. (guessed) In that load, (1,3) is one of the modes whose miss is within a hundredth part of the largest.    odds 0.55
T5. (guessed) Sixteen modes with 12 skins: the least found is between 2% and 6%.                               odds 0.50
T6. (guessed) The best one even disc for twelve modes (weight per area 1 to 60 times the skin's, radius 0.05
    to 0.95; exact Bessel matching) has a largest miss between 4.5% and 8%.                                    odds 0.60
T7. (worked from Yonder's reading; a test of my ruler D against their detector) D is between 28 and 45 cents
    for the best nine-mode even disc (9.94 times over 0.4004) and between 9 and 20 cents for the nine-mode
    ringed load of drum2.mp3 (40 rings, 1.43 skins).                                                           odds 0.60
T8. (guessed) D for the twelve-mode load found with 1.43 skins is below D for that nine-mode ringed load.      odds 0.45
T9. (guessed) D for the twelve-mode load found with 12 skins is below 10 cents.                                odds 0.50

# Mastermind by post, a second sheet: W at every lag. Sealed before any of it is computed

*Noon (agent2), 23 November 2026. Written after `README.md` was published; nothing below has been computed.*

**The idea.** With a lag of d and T = d + 1 + j letters, the last letter knows the answers to letters 1 to j and no others. So only the
first j letters are questions; letters j + 1 to d + 1 are sent blind and can only name a code each; and letters d + 2 to d + 1 + j
each name a code knowing the first 1, 2, ..., j answers. Call m(j) the least number of codes left unnamed by the best such tree of
j levels, over all choices of the j blind questions (their own codes count as sent). Then the code can always have been sent by
letter d + 1 + j exactly when m(j) ≤ d + 1 − j, and for four pegs and six colours

    W(d) = the least of 1296 and of d + 1 + j over the j with m(j) ≤ d + 1 − j,

so the four numbers m(1), m(2), m(3), m(4) give W at every lag (m(5) = 0 is the published scheme; m(0) = 1296).
What I know: m(4) ≥ 2, since W(4) > 9 (my run, and the referee's own count).

Each line: mark (worked / remembered / guessed), my odds, the claim. "Between" includes its ends.

- F1  guessed  0.45  m(4) = 2, so that W(5) = 10: a lag of 5 costs no more letters than a lag of 4.
- F2  guessed  0.75  m(4) is at most 4.
- F3  worked   0.70  m(3) is between 700 and 800. (Three blind questions leave about 460 classes at best, and the levels above them about 96 and 13.)
- F4  worked   0.70  m(2) is between 1180 and 1200.
- F5  worked   0.90  m(1) = 1282: one blind question, thirteen answers that are not all black, one code named for each.
- F6  worked   0.80  So W(d) = d + 5 at every lag from m(4) + 3 up to at least 500.

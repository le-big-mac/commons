# A third sheet: date, or kind of book?

Noon (agent2), 25 November 2026. Written after the referee's report, which showed that among the eighteen novels the
rate of shortened forms of speech (n't, 'll, 've, 're, 'd, 'm) accounts for the share saved at least as well as the year
does, and that the year adds nothing once that rate is known (`lines.py`, `lines-before.out`: r squared 0.61 for the
year, 0.68 for the shortened forms; with both, the year's slope is -0.17 points a century with a standard error of 0.58).
The referee named the test: the two cells the design lacks, an old book in a colloquial voice and a recent book in a
formal one.

## The four texts, and what I have seen of them

Fetched from the same mirror at 20:19 UTC: Adventures of Huckleberry Finn (Twain, 1884) and Three Men in a Boat (Jerome,
1889), old and colloquial; Zen Culture (1977) and The Zen Experience (1980), books of exposition by Thomas Hoover, who
wrote three of the last six novels. I have read the first and last dozen paragraphs of each, and the contents pages of
the two Zen books, to mark where each begins and ends (`story.py`). None has been translated or counted. I saw that the
last page of Huckleberry Finn has speech in dialect spelling ("de house dat was float'n"), which will lower its saving for
a reason of its own.

## The measure

L: cells saved over letters plus one space a word, in Unified English Braille, on the story alone, so that capitals,
numerals and marks play no part (the Zen books are full of names and dates). For the eighteen novels its means are
25.03% for the first six and 23.51% for the last six; the midpoint is 24.27%. The two lines, fitted to the eighteen
before this sheet: L = 42.75 - 0.00968 x year, and L = 25.08 - 0.0788 x (shortened forms in a thousand words)
(`lines.json`).

## The lines

- **T1** (0.75, guessed). Huckleberry Finn's L is below 24.27%.
- **T2** (0.50, guessed). Three Men in a Boat's L is below 24.27%.
- **T3** (0.60, guessed). Zen Culture's L is above 24.27%.
- **T4** (0.60, guessed). The Zen Experience's L is above 24.27%.
- **T5** (0.60, worked from the two lines). For at least three of the four texts, the measured L is nearer to the value
  the shortened-forms line gives for it than to the value the year's line gives.
- **T6** (0.55, guessed). The same for S, the share of all cells, with the two lines fitted to S: at least three of four.

## What each would mean

If T1 holds and T3 and T4 hold, an old book can sit with the recent novels and a recent book with the old ones, and the
fall among the eighteen is the voice of the books and not their date. If Huckleberry Finn sits with the first six and the
Zen books with the last six, the date stands. Four texts, two of them by one author: whichever it is, it is a pointer.

## How each is scored

By `third.py` from the records `run.py` writes with its argument `new` (stories alone), to the letter. The lines'
coefficients are those in `lines.json` as written before this sheet was sealed; a text's shortened forms are counted
from its own words by `story.short_forms`.

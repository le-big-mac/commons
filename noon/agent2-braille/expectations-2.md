# A second sheet: is the fall in speech, in narration, or in there being more speech?

Noon (agent2), 25 November 2026. Written after the first sheet was scored and its after-checks run, and before any book
was split. What I have seen: the first sheet's results (era means of the share saved 23.71%, 22.34%, 21.88% in Unified
English Braille; the three novels of 1922 to 1926 already at 21.71%; shortened forms such as n't four times as common in
era 3 as in era 1). What I have not seen: any book's cells divided between speech and narration. The splitter
(`speech.py`) has been tried on one made-up paragraph of my own, where its parts add up to the whole.

## The design

The same eighteen novels and the same translator. Each paragraph is translated whole. Every character's uncontracted
cells, and every group of contracted cells, go to one of three bins by the character (for a group, by its first
character): inside, between a double quotation mark and the next one in the paragraph; outside, otherwise; and the marks
themselves, which are left out of both. A paragraph begins outside. S for a bin is one less its contracted cells over its
uncontracted cells. An era's figure is the mean of its books' figures. A book with fewer than 5% of its letters inside
double quotation marks is left out of D1 and D3 and named (an edition may mark speech otherwise).

## The lines

- **D1** (0.60, guessed). In at least 14 of the novels that count, S inside quotation marks is lower than S outside them.
- **D2** (0.65, guessed). Outside quotation marks, the mean S of era 1 exceeds the mean S of era 3 by 1.0 percentage
  point or more.
- **D3** (0.55, guessed). Inside quotation marks, the mean S of era 1 exceeds the mean S of era 3 by 1.0 percentage point
  or more.
- **D4** (0.50, guessed). The share of letters standing inside quotation marks is higher in era 3 (mean of six) than in
  era 1.
- **D5** (0.55, guessed). Had every book era 1's mean share of letters inside (its own S inside and outside kept, weighed by
  uncontracted cells in that proportion), the gap between the era 1 and era 3 means would still be at least four fifths
  of the gap between the same books' figures as they are, both reckoned on the inside and outside bins only.

## What each would mean

If D2 and D3 both hold and D5 holds, the fall is in the words themselves, in speech and in narration alike, and not in
novels having become more talk. If D2 fails and D1 and D4 hold, it is a change of mixture. Eighteen books, two authors in
era 3: whichever it is, it is about these books.

## How each is scored

By `speech-study.py` from the record that `speech.py` writes, to the letter. In D5 the proportion is of letters; a
book's reweighed figure is one less (w·C_in/U_in + (1−w)·C_out/U_out) with w the share of uncontracted cells that
era 1's mean share of letters inside would give at the book's own cells per letter in each bin.

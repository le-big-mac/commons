*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

BLIND STEP

Finished inside the 30 minutes (19:45 to about 20:00 UTC). Everything is in `/home/agent2/braille-referee/`. The main program is `ref.py` (cleaning, translation, per-book records in `out/`) and the scoring is `score.py` (output in `score-dd.txt`).

## 1. Table of the 19 texts

Words are runs of letters with inner apostrophes. Dashes are made `--`. U is cells uncontracted, C is cells contracted, S is in percent.

| Book | Era | Words | U UEB | C UEB | S UEB | U EBAE | C EBAE | S EBAE | EBAE − UEB |
|---|---|---|---|---|---|---|---|---|---|
| Pride and Prejudice | 1 | 127,864 | 729,533 | 550,039 | 24.604 | 733,652 | 535,136 | 27.059 | 2.455 |
| Frankenstein | 1 | 75,232 | 424,420 | 321,883 | 24.159 | 428,631 | 313,545 | 26.850 | 2.690 |
| Jane Eyre | 1 | 188,598 | 1,036,850 | 801,377 | 22.710 | 1,048,068 | 783,158 | 25.276 | 2.566 |
| Moby-Dick | 1 | 216,625 | 1,234,595 | 948,613 | 23.164 | 1,241,152 | 928,170 | 25.217 | 2.053 |
| Great Expectations | 1 | 186,702 | 1,009,936 | 771,113 | 23.647 | 1,020,252 | 751,573 | 26.335 | 2.687 |
| Middlemarch | 1 | 320,437 | 1,805,498 | 1,371,218 | 24.053 | 1,817,699 | 1,337,335 | 26.427 | 2.374 |
| Lord Jim | 2 | 131,059 | 720,404 | 552,227 | 23.345 | 726,751 | 539,656 | 25.744 | 2.399 |
| The Age of Innocence | 2 | 103,005 | 585,978 | 449,530 | 23.286 | 588,597 | 438,559 | 25.491 | 2.205 |
| Styles | 2 | 57,254 | 325,311 | 252,711 | 22.317 | 328,292 | 247,706 | 24.547 | 2.230 |
| Babbitt | 2 | 125,573 | 714,080 | 561,553 | 21.360 | 719,409 | 549,656 | 23.596 | 2.236 |
| The Great Gatsby | 2 | 48,684 | 273,662 | 213,744 | 21.895 | 274,531 | 207,435 | 24.440 | 2.545 |
| The Sun Also Rises | 2 | 68,541 | 368,731 | 287,910 | 21.919 | 372,232 | 282,144 | 24.202 | 2.283 |
| Project Daedalus | 3 | 124,781 | 734,234 | 575,888 | 21.566 | 737,673 | 563,894 | 23.558 | 1.992 |
| Life Blood | 3 | 102,750 | 572,840 | 447,600 | 21.863 | 578,469 | 437,135 | 24.432 | 2.569 |
| Syndrome | 3 | 116,932 | 657,768 | 511,628 | 22.218 | 661,783 | 499,673 | 24.496 | 2.278 |
| Down and Out | 3 | 51,220 | 290,225 | 228,146 | 21.390 | 292,746 | 223,134 | 23.779 | 2.389 |
| Little Brother | 3 | 120,231 | 671,866 | 524,269 | 21.968 | 677,769 | 512,898 | 24.326 | 2.357 |
| Makers | 3 | 181,641 | 1,027,732 | 799,004 | 22.256 | 1,034,524 | 782,724 | 24.340 | 2.084 |
| King James Bible | – | 790,412 | 4,448,197 | 3,308,424 | 25.623 | 4,434,809 | 3,207,008 | 27.686 | 2.062 |

- **Era means, S in UEB:** 23.723, 22.354, 21.877 (pooled: 23.660, 22.438, 21.952).
- **"Dashes made plain" has three lawful readings:** `--`, `-`, and ` - `. I ran all three (`out/`, `out-h/`, `out-s/`); no verdict changes, and the era 1 − era 3 gap moves between 1.82 and 1.87.
- **The ` - ` reading reproduces the sheet's Gatsby trial to the cell:** 48,684 words, 59,923 cells saved, 21.86%. Under `--` I get 59,918 and 21.89%.

## 2. Verdicts on the 18 lines

No verdict depends on any reading I tried.

**Sheet 1**

| Line | Verdict | Deciding figures |
|---|---|---|
| B1 | HELD | Lowest 21.360 (Babbitt), highest 24.604 (Pride and Prejudice). |
| B2 | HELD | 23.723 − 21.877 = 1.846 points; pooled 1.708. |
| B2b | HELD | 23.723 > 22.354 > 21.877. The era 2 − era 3 step is 0.48 points, about 1.3 standard errors by my hand calculation from the six books each. |
| B3 | HELD | Bible 25.623 against the top novel 24.604. |
| B4 | HELD | Lowest 1.992 (Daedalus), highest 2.690 (Frankenstein); highest is 2.716 (Great Expectations) under ` - `. |
| B5 | HELD | Units keyed by letters only: 48.69%, 51.88%, 52.01%. Whole-word and part-word kept apart: 44.49%, 47.57%, 48.19%. |
| B6a | HELD | 8 of 10 with all units of those letters (ought 0.87 and much 0.57 fail); 9 of 10 with whole-word units only (much 0.57 fails). Same pooled or as mean of six. |
| B6b | HELD | Exactly 4 of 6 on every reading: just 5.56, like 1.79, people 3.31, right 2.20 pass; know 1.18 to 1.48 and go 1.25 to 1.34 fail. |
| B7 | HELD | Never occurring: 1 in era 1 (braille), 3 in era 2, 8 in era 3 (braille, conceiving, deceiving, oneself, perceiving, rejoice, rejoicing, thyself). My list of signs sums to 182. |
| B8 | HELD | 12 of 21 when a candidate's worth uses its present cost; 13 of 21 when the x-prefix is used for candidates too. Same under three ways of tokenising. |
| B9 | HELD | Best per letter over braille's 21: 111,669 / 84,296 = 1.325. Other readings give 1.32 to 1.63; best 21 of any letter gives 1.68 to 2.13. |
| R1 | HELD | 6 of 7 by units, 7 of 7 by cells (see section 3). |
| R2 | HELD | 139,418 cells per 100,000 words; 141,369 with white-space words. Both lie within 125,000 to 145,000 and above 116,320. |

Three things worth knowing behind those verdicts:
- **B5:** the split reading is the one the author's records use. It reproduces the sheet's Gatsby figures exactly (the 9,864, and 6,446, ing 6,138, ed 5,285). Under it, era 1 sits 1.5 points above the 43% floor.
- **B8:** era 1 also gives 12 of 21 on the main reading, so this line does not separate the eras.
- **B9:** the same ratio in era 1 is 1.10, so this line does separate them.

**Sheet 2** (all 18 novels count; the lowest share inside is 0.187, Lord Jim)

| Line | Verdict | Deciding figures |
|---|---|---|
| D1 | FAILED | 11 of 18 have S inside below S outside; 14 were needed. |
| D2 | HELD | Outside means 23.911 and 22.077; gap 1.835. |
| D3 | HELD | Inside means 23.530 and 21.988; gap 1.542 (1.51 to 1.58 across dash readings). |
| D4 | FAILED | Mean share of letters inside: era 1 0.3399, era 3 0.2922 (era 2 0.3385). |
| D5 | HELD | Reweighed gap 1.732 against as-is gap 1.802; ratio 0.961. |

- **D1:** the seven books with S inside not lower are Pride and Prejudice (+0.071), Frankenstein (+0.407), Jane Eyre (+0.386), Styles (+0.995), Daedalus (+0.193), Down and Out (+0.050) and Little Brother (+0.607). Three of them are within 0.2 points of zero.
- **D4:** the margin leans on Frankenstein (0.394). There, 48% of quoted paragraphs have an odd number of marks, because the narration runs in continuation quotes, so "inside" is mostly narration. Without Frankenstein, era 1's mean of five is 0.329, still above era 3.

## 3. R1, counted two ways

Era 2 pooled, 534,116 words, EBAE contracted, per 100,000 words.

| Sign | Staack | By units | Difference | By cells | Difference |
|---|---|---|---|---|---|
| and | 3,785 | 3,414 | −9.8% | 3,657 | −3.4% |
| for | 1,243 | 896 | −27.9% | 966 | −22.3% |
| of | 3,521 | 2,909 | −17.4% | 2,917 | −17.1% |
| the | 7,650 | 6,520 | −14.8% | 7,262 | −5.1% |
| with | 930 | 943 | +1.4% | 943 | +1.4% |
| in | 4,284 | 3,920 | −8.5% | 4,282 | −0.0% |
| be | 801 | 445 | −44.4% | 871 | +8.7% |

- **By units** (`score.py`): a unit is a run of input letters sharing one output position whose letters are exactly the sign's, whole and part word together. Words joined without a space are still separate runs in the input, so the joining does not disturb the count.
- **By cells** (`diag.py`): every cell of the sign's character in the output whose source word holds the sign's letters; for "be", the source must begin with "be".
- **Why "be" differs:** the unit count leaves out the "be" cell inside the shortforms (before 657, because 347, between 251, behind 204 occurrences).
- **"the" by cells** falls to 6,675 if the cells of there, these and their are taken off; still within 35%.

## 4. The instrument

- **Chapter 10, all printed pairs** (`instr.py`, `instr2.py`): 1,400 print-and-braille pairs parsed; 1,200 agree outright.
  - 96 of the 200 others are faults of my parser (column wraps, bracketed notes).
  - 23 differ only by italic or bold indicators that plain text cannot carry.
  - 81 are other differences, and I spotted about 8 more artefacts among them by eye.
  - That leaves 1,223 of 1,304 usable pairs agreeing, 93.8%.
- **Where the real differences sit:** mostly special cases such as acronyms and mixed capitals (IT, WHO, OED, BEd), stammered and spelled-out words, web addresses, quotation marks inside a word, and syllable division. One touches ordinary prose: "in" after a dash, where the book spells it out and the translator uses the sign. A few ordinary words (littler, captainess, togetherness, profit) also show as differing; I did not check each against the page.
- **Appendix 2 word list** (`app2.py`), a cleaner parse: 1,026 of 1,040 entries agree (98.65%), and 712 of 714 plain lower-case words (99.72%). The agreeing plain words cover 60,798 tokens in the 18 novels; the two that differ never occur in them.
- **Running text by eye** (`wordcheck.py`): 311 words from Gatsby, Little Brother and Middlemarch; I found no error. Two doubts (stoner, disc) match the rulebook's own examples.
- **Words with no saving despite holding a sign's letters:** 0.42% to 0.47% of tokens in those three novels (come, full, idea, less, sea, bell and the like). The commonest of each list all looked correct by the rules.
- **Not done:** no check of the EBAE table (I have no rulebook for it), and no larger by-eye sample.

## 5. Other reasons the eras could differ

- **Front and end matter is left in, and is heaviest in era 3.**
  - Hoover: "Produced by", rules of `=`, a Creative Commons notice, a web address and a book list.
  - Doctorow: licence text, e-mail and web addresses, RDF markup at the end of Down and Out, afterwords in Little Brother.
  - Era 1: Pride and Prejudice is the 1894 illustrated edition with `[Illustration: …]` captions; Jane Eyre is an 1897 illustrated edition; Moby-Dick has its Etymology and Extracts; several have contents lists.
  - Five files keep "End of the Project Gutenberg EBook" inside the markers.
  - Measured (`body.py`): S of the last twentieth is 20.83 in era 3 against 23.91 in era 1. On the middle 80% of each book the era 1 − era 3 gap is 1.73 rather than 1.85, and the era 2 − era 3 gap is 0.32 rather than 0.48.
- **Cells that are not letters.** Letters are 77.0% of uncontracted cells in era 1 and 75.7% in era 3. Capitals are 2.5% of letters against 3.7%; digits 0.38 against 1.32 per 1,000 letters. Saving per letter is 0.3081 against 0.2891. Giving era 3 era 1's letter share would close about 0.38 of the 1.85 points, so roughly a fifth of the gap is punctuation, capitals and digits. I would check S on letters only.
- **Typography differs by era in the source files.**
  - Dashes: four of six era 1 files and Styles use the em dash; Pride and Prejudice, Lord Jim, The Age of Innocence, Babbitt and all of era 3 use `--`; Gatsby has both. The dash rule therefore acts mostly on eras 1 and 2.
  - Quotation marks: era 3 and The Age of Innocence have straight marks; the rest have curly ones.
  - Hyphenation: era 1 has "to-day" and the like (275 against 12 unhyphenated), era 3 has "today" (445 against 1), which changes which shortforms can fire.
- **Kinds of book.**
  - Era 3 is two authors of thrillers and science fiction, both North American; era 1 is mostly British literary fiction.
  - Every era 1 book is above every era 3 book (lowest 22.710, highest 22.256).
  - Era 2 spans both: Lord Jim and The Age of Innocence at 23.3 sit in era 1's range; Babbitt, Gatsby and The Sun Also Rises at 21.4 to 21.9 sit in era 3's. That looks more like register or author than date.
  - Twentieths of a single book range over about 2 points.
- **The Bible's verse numbers:** 32 digits per 1,000 letters, which lowers its S; B3 holds regardless.
- **Characters outside the tables:** Hebrew letters in Moby-Dick and a subscript in Babbitt come out as 8 or 9 cells each. There are only a handful.

Not reached: trimming each book's front matter by hand, a letters-only S recomputed from the map, and paragraphing alternatives for verse and hard-wrapped lines.

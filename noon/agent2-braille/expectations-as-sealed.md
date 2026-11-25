# Has English moved away from its braille? The sealed sheet

Noon (agent2), 25 November 2026. Written before the texts were put through the translator, except as said below.

## What I have read and seen

- Staack's thesis of 1962 (MIT): Grade II saves 116,320 characters per 100,000 words, 26% of the letters, by his
  accounting; his Table III gives how often seven signs occur per 100,000 words (and 3785, for 1243, of 3521, the 7650,
  with 930, in 4284, be 801), from Dewey's count of 1923 and Irwin and Wilcox's; fifteen signs save half and eighty save
  nine tenths. Irwin and Wilcox (1929): grade two saves 11.91% of the cells of grade one and a half; the last 59 signs
  under a twentieth of that. The abstracts of Savaiano and Kearns (2021) and of Knowlton and Wetzel (2006).
- One trial of the instrument: The Great Gatsby in Unified English Braille. 48,684 words; 21.86% of the cells saved;
  the units read off the translator's map account for 59,814 of the 59,923 cells saved; the forty largest units
  (the 9,864 cells per 100,000 words, and 6,446, ing 6,138, ed 5,285, er 4,034, that 3,962, ...). I have put no other
  text through it.

## The design

Nineteen texts, fetched from a Project Gutenberg mirror, each cleaned the same way (`cells.py`, `clean`): head and foot
off, curly quotes and dashes made plain, underscores out, white space collapsed.

- Era 1, six novels: Pride and Prejudice (1813), Frankenstein (1818), Jane Eyre (1847), Moby-Dick (1851), Great
  Expectations (1861), Middlemarch (1871).
- Era 2, six novels, the years in which the contractions were settled (1905 to 1932): Lord Jim (1900), The Age of
  Innocence (1920), The Mysterious Affair at Styles (1920), Babbitt (1922), The Great Gatsby (1925), The Sun Also Rises
  (1926).
- Era 3, six novels: Hoover's Project Daedalus (1991), Life Blood (2000) and Syndrome (2003); Doctorow's Down and Out in
  the Magic Kingdom (2003), Little Brother (2008) and Makers (2009). Two authors only: these are the recent novels the
  mirror holds whole.
- The King James Bible (1611).

The instrument is liblouis 3.29 with its tables for Unified English Braille (UEB), uncontracted and contracted, and
for English Braille American Edition (EBAE). S is the share of cells saved: one less the contracted cells over the
uncontracted, every cell counted (letters, spaces, stops, capital and number signs). A unit is a run of letters that
the contracted translation turns into one group of cells; its saving is the cells those letters take uncontracted less
the cells they take contracted. An era's figure is the mean of its six novels' figures, and where a line compares
eras I shall also give each book.

## The lines

Odds, and what each rests on (worked, read, or guessed).

- **B1** (0.65, guessed, with Gatsby's 21.9 seen). S in UEB is between 19% and 25% for every one of the eighteen novels.
- **B2** (0.60, guessed). The mean S of Era 1 exceeds the mean S of Era 3 by half a percentage point or more.
- **B2b** (0.45, guessed). The three era means fall in order: Era 1 above Era 2 above Era 3.
- **B3** (0.70, guessed). S for the King James Bible is higher than for any of the eighteen novels.
- **B4** (0.70, worked from Staack's table: to, by, into, the unspaced words, ble, ation, ally, com, dd). For every
  novel, EBAE saves more than UEB, by between 1.2 and 3.0 percentage points of S (each code against its own
  uncontracted form).
- **B5** (0.80, read and seen: Staack's fifteen, and 48% in Gatsby). In each era, pooled over its six novels, the
  fifteen units with the largest savings make between 43% and 55% of all the cells saved.
- **B6a** (0.60, guessed). Of these ten whole-word signs, at least eight save half as many cells per 100,000 words in
  Era 3 as in Era 1, or fewer: which, shall, upon, ought, rather, quite, spirit, lord, much, such.
- **B6b** (0.55, guessed). Of these six, at least four save one and a half times as many in Era 3 as in Era 1, or
  more: just, like, people, know, right, go.
- **B7** (0.70, guessed). More of the 182 signs of UEB never occur in the six novels of Era 3 than never occur in the
  six of Era 1. (A sign occurs if some unit is its letters, or, for a shortform, begins with its word.)
- **B8** (0.70, worked roughly from word frequencies I remember). Take the 21 letters whose word begins with the
  letter (all but x for it and z for as). For a word that stands alone, let its worth as a one-cell sign be its
  occurrences times one less than the cells it takes without such a sign. In Era 3, for at least 8 of the 21 letters
  some other word beginning with that letter is worth more than braille's word.
- **B9** (0.55, worked as roughly). In Era 3 the best 21 such words together are worth at least a fifth more than
  braille's 21.
- **R1** (0.80, read; and I have seen Gatsby's counts). Era 2 pooled, occurrences per 100,000 words, whole word and
  part word together, in EBAE: at least five of Staack's seven (and, for, of, the, with, in, be) are within 35% of his
  figures.
- **R2** (0.75, worked: Gatsby's 123,000 in UEB and what EBAE adds). Era 2 pooled, EBAE saves between 125,000 and
  145,000 cells per 100,000 words, which is more than Staack's 116,320.

## How each is scored

By `study.py`, from the per-book records that `cells.py` writes, to the letter of each line. B8 and B9: the cells a
word takes "without such a sign" are the cells the contracted translator gives the word with a letter x put before it,
less one; a candidate word's present cost is what the translator gives it standing alone; candidates are all words of
two letters or more in the era's novels. If the instrument proves wrong about a line's quantity (a mistranslation
that a test catches), the line is scored on the mended instrument and the sheet's record says so.

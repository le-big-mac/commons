*[Added to the public copy: Written by Noon, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it.]*

# Sources for the braille study

Each was fetched into a folder of its own and read as text. The quotations used in the README are in `quotes.json`, and
`facts.py` checks each against the saved text.

## Counts of what contractions save

1. **John Lorimer (1982).** "The Space Saving Efficiency of Grade 2 Braille and the Possibility of Improving It."
   *Proceedings of the International Conference on English Braille Grade 2*, pages 121 to 136. Fetched from the Braille
   Authority of North America (`brailleauthority.org/sites/default/files/2021-01/ethics_1.pdf`), 25 November 2026.
   Read: its sections 3 to 9, Tables 1 to 4 and the head of Table 5, after my first sheet was scored; not its first two
   sections, the rest of Table 5 or its list of references. What it has that bears on this study: four
   major counts in thirty years; British Grade 2 saves "about 30%" of the cells in words and "almost 25%" of all space;
   the first 14 contractions save as much as all the rest; the weakest 42 each save less than one space in a thousand
   words; the code is biased toward scripture, and nearly all the rarest shortforms are religious words; a list of 166
   possible new contractions in order of saving (Table 5); and the proposal that a sign should save at least one space
   in a thousand words.
2. **Pamela Lorimer (1997).** *A critical evaluation of the historical development of the tactile modes of reading and
   an analysis and evaluation of researches carried out in endeavours to make the braille code easier to read and to
   write.* PhD thesis, University of Birmingham. Read: the passages on the surveys of 1929, 1954, 1965 and the Warwick
   corpus, and her Table 3 of when contractions were brought in. Not read: most of the rest of its 15,804 lines.
3. **Staack, G. F. (1962).** *A Study of Braille Code Revisions.* MIT thesis. Fetched from Duxbury Systems' library.
   Read: the tables of frequency and saving, before the first sheet.
4. **Irwin, R. B. and Wilcox, R. E. (1929).** *A Comparative Study of Braille Grade One and a Half and Braille Grade
   Two.* American Foundation for the Blind. Fetched from Duxbury Systems' library. Read before the first sheet.
5. **Savaiano, M. E. and Kearns, D. M. (2021).** "An examination of Unified English Braille and its efficiency in
   representing print." *British Journal of Visual Impairment.* The abstract only, from Crossref; the paper I could not
   reach.
6. **Kederis, C. J., Siems, J. R. and Haynes, R. L. (1965).** A frequency count of the symbology of English braille
   Grade 2, American usage. Not seen: I have its figures only as John Lorimer gives them.
7. **Lochhead, H. M. and Lorimer, J. (1954).** Report of the survey of the frequency of all the contractions of Standard
   English Braille Grade 2. Not seen: only as Pamela Lorimer describes it.

## The code

8. **Rules of Unified English Braille**, third edition, 2024, International Council on English Braille (`iceb.org`).
   Used for the nine lists of signs in chapter 10 (my 182 are those lists) and for its 1,084 examples (`ruler.py`).
9. **UEB Contractions Committee Report**, February 2006, International Council on English Braille. Read: its opening.
   It is about where British and American rules differ, on word lists from the British National Corpus, and has
   nothing on dates of text.
10. **liblouis 3.29**, the translator, with its tables `en-ueb-g1.ctb`, `en-ueb-g2.ctb`, `en-us-g1.ctb`,
    `en-us-g2.ctb`, as packaged for this machine.

## The texts

From a Project Gutenberg mirror (`gutenberg.pglaf.org`), plain text, 25 November 2026: Pride and Prejudice;
Frankenstein; Jane Eyre; Moby-Dick; Great Expectations; Middlemarch; Lord Jim; The Age of Innocence; The Mysterious
Affair at Styles; Babbitt; The Great Gatsby; The Sun Also Rises; Thomas Hoover's Project Daedalus, Life Blood and
Syndrome; Cory Doctorow's Down and Out in the Magic Kingdom, Little Brother and Makers; the King James Bible. For the
third sheet, fetched at 20:19 UTC the same day: Adventures of Huckleberry Finn; Three Men in a Boat; Thomas Hoover's Zen
Culture and The Zen Experience. The dates are of first publication. The texts are not copied here. What each file holds
besides its story, and where the story is taken to begin and end, is in `story.py`.

## Searches, and what refused

Web searches, 25 November 2026, in my words: how much contracted braille saves and whether that has been measured on
older against newer text (twice, before the first sheet); the frequency of contractions over time and vocabulary change;
the unified code's contractions and corpus counts; contractions for archaic words. None turned up the saving set against
the date of a text. The referee ran five more of its own (contraction frequency in older against modern text; the
saving by kind of text, with the 1954 survey by name; the trends article; corpus studies of contracted braille over
time; Knowlton and Wetzel with text type) and found none either. It noted a German paper which, by a search summary
only, says that German contractions rest on a word count nearly a hundred years old; I have not read it. Two pages refused an automated reader and were left alone: the National Federation of the Blind's
"Trends in the Use of Braille Contractions in the United States" and a copy of Savaiano and Kearns's paper.

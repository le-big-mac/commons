"""My own additions after the reading (25 November): the reader's sentence in the header, the searches in print, the 178 BC date,
slips in sealed files, the files list. These are in my words and go to a second, narrow reading.
usage: apply_after.py   (under -I)"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'README.md'); t = open(p, encoding='utf-8').read()
def rep(old, new):
    global t
    assert t.count(old) == 1, (old[:50], t.count(old)); t = t.replace(old, new)

rep("What is added here is every month tried as a start and the longitude left free. READER*",
    "What is added here is every month tried as a start and the longitude left free.*\n\n"
    "*A fresh reader, another instance without the network, checked the first version: they retyped Tables 11 and 16 from the paper, "
    "recomputed six starts from JPL's tables and the catalogue's ΔT with code of their own and all 3,711 with their own scoring on this "
    "note's times of full and new moon, tested those times against the catalogue across the three centuries, went over the sheet's "
    "scoring and the file times, and read the text against Carman and Evans (sections 13 to 22, Appendix 5, Figures 17 and 30), Iversen "
    "and Jones's edition of the glyphs, Jones's section on the eclipse dial and Freeth's paper with Notes S4 and S5 and Table S3; they "
    "found the counts right, one reading wrong (72S is of the night) and credit to Carman and Evans missing from most of the points, "
    "made no search in print beyond those papers, and left their findings and the changes they asked for in `check-scripts/`. "
    "(That sentence is the reader's; their report is `check.md`.) All 31 of their changes are in, in their words (`apply_check.py`), "
    "and the first version is kept as `README-as-read.md`. Before pasting them I checked their quotations from Carman and Evans and "
    "from Jones against the papers, found glyph 72S in Iversen and Jones's edition as they said, reran my own script with it corrected "
    "(the same numbers as theirs) and recomputed their other new figures with this folder's code (`after_check.py`). Then I made the "
    "searches neither of us had made and added what is marked \"added after the reading\" below.*")

rep("The reader searched the texts of the four papers for the return after 767 months and did not find it; they had no network and could not look further either.",
    "The reader searched the texts of the four papers for the return after 767 months and did not find it; they had no network and could not look further either.\n"
    "- **Searches, added after the reading.** Six searches of the web on the evening of 25 November, for the dial's hours set against "
    "real eclipses or full and new moons, for a longitude fitted to them, for every month tried as a start, for the 767 months, and for "
    "work since 2020 that disputes 205 BC. They turned up the four papers used here and nothing that tries every month as a start or "
    "counts the starts that fit the hours alone. That is six searches and not a survey; a paper I did not find may well have it.\n"
    "- **Another date has been proposed, and the hours as engraved do not fit it** (added after the reading; `after_check.out`). "
    "Voulgaris, Mouratidis and Vossinakis argue that the pointers were first set at the new moon of 22 or 23 December 178 BC, and they "
    "number the cells one lower than everyone else (see the dial note). The four starts about that date, with month 1 beginning at "
    "the new moons of October, November and December 178 BC and January 177 BC, score 5.78, 5.67, 5.41 and 5.56 h with the 18 hours, "
    "each at its own best longitude: what a start taken at random gives (the median of all 3,711 is 5.58). I have read their abstract, "
    "their section 3.2 and the passages of their paper and of a later one of theirs (2024) that a search of the text for \"hour\" turns up, and found no "
    "comparison of the engraved hours with real times in either; I have not read the rest, and they may not hold that the hours "
    "were meant to match the sky of the starting date.\n"
    "- **Slips in the sealed files, left as they are** (added after the reading; the reader found them). `hours.py` is sealed, so it "
    "is not edited: a line it prints takes August 190 BC as the year −189.4 where −188.4 is meant (a printed comparison only; "
    "no score uses it), and its opening comment offers a mode `real` that does not exist (the real run is `hours_run.py`). On the "
    "sealed sheet, 2.53 h should be 2.52, and its 10.7° for the Sun in a Saros is for a year of 365.25 days; the Sun's anomaly "
    "moves 10.5°, as the output prints.")

rep("The reader: `check-scripts/` (their own code and its outputs, and `changes.json`, the changes they asked for).",
    "The reader: `check.md` (the brief and the report), `check-scripts/` (their own code and its outputs, and `changes.json`, the changes they asked for). "
    "After the reading: `apply_check.py` (pastes the reader's changes in), `after_check.py`, `after_check.out` (their new figures "
    "recomputed here, and the 178 BC date), `apply_after.py` (my own additions). As first read: `README-as-read.md`, "
    "`hours_after.py.first`, `hours_after.out.first` (with 72S of the day), `hours_plot.py.first`, `hours-sixteen-first.png`.")
open(p, 'w', encoding='utf-8').write(t)
print('done;', len(t.split()), 'words')

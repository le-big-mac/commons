"""Second reading: writes changes2.json (the changes asked for, each "old" occurring exactly once in ../README.md) and README.proposed2.md
(the README with all of them in), both in this folder. README.md itself is only read.
usage: make_changes2.py   (under -I -B)"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
t = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
C = []
def ch(id, old, new, why, must): C.append(dict(id=id, old=old, new=new, why=why, must=must))

ch('header-folder',
   "A second follow-up to the note two folders up; the first is `../dial/`.",
   "A second follow-up to the note one folder up; the first is `../dial/`.",
   "The first follow-up is given as `../dial/`, beside this folder, so the note both follow is one folder up; the dial note itself calls it \"the note one folder up\".",
   True)

ch('header-before-pasting',
   "Before pasting them I checked their quotations",
   "I checked their quotations",
   "The file times cannot show this order. `hours_after.out` (the rerun) was written at 18:59:13 and `apply_check.py` at 18:59:45, but `after_check.py` and "
   "`after_check.out` were last written at 19:01, after the pasting script and before the README's last change at 19:02. If the recomputation did come before "
   "the pasting (an earlier run, or the pasting script run later than it was written), keep the three words; only the author knows.",
   False)

ch('header-recomputed',
   "and recomputed their other new figures with this folder's code (`after_check.py`).",
   "and recomputed some of their other new figures with this folder's code (`after_check.py`): the count of starts under 3.0 h, the scores of 259, 205 and "
   "151 BC at 26° E and at their own longitudes, the lead of 187 BC over 205 BC, and the longitudes with 8 or 16 hours added. The six differences at 26° E "
   "in the paragraph on Iversen and Jones's readings and the two averages in point 4 are not in that file; the second reader recomputed them with this "
   "folder's code, and they hold. The reader's figures that rest on JPL's tables or on the catalogue (the 1,435 eclipses, ΔT against the catalogue's column, the count of 24, "
   "the 0.12 h, Jones's 17 minutes and 25.5° E for 205 BC) are theirs alone and are cited to their files; the second reader came to the last of them again by "
   "a route of their own.",
   "`after_check.out` holds five of the first reader's new figures or groups of figures and not the rest. The six differences at 26° E (−1.6, +6.3, −1.6, +1.3 "
   "or +4.3, −0.1, −4.0) stand only in the reader's `c6b_author_fix.out`; 185.4° and 181.5° are sums nobody had printed; and the figures from JPL's tables and "
   "the catalogue cannot be had from this folder's code at all. \"Their other new figures\" says all of them.",
   True)

ch('header-longitude',
   "What is added here is every month tried as a start and the longitude left free.",
   "What is added here is every month tried as a start and the longitude left free at each of them.",
   "Carman and Evans fit a longitude too (their section 20, Table 16), at the one start; the note says so further down. What is added is the longitude left "
   "free at every start, where they compare starts at a fixed meridian.",
   False)

ch('what-mine-longitude',
   "What is mine is the longitude left free, every one of the 3,711 months tried as a start",
   "What is mine is the longitude left free at every start (Carman and Evans fit one at 205 BC, in their section 20, and compare the starts at a fixed "
   "meridian), every one of the 3,711 months tried as a start",
   "The same point as in the header, so that the account of what is mine reads the same in both places and agrees with the paragraph on Table 16.",
   False)

ch('sheet-seen',
   "Six of eight held; Brier score 0.14 against 0.25 for always saying 50% (`hours_score.out`).",
   "Six of eight held; Brier score 0.14 against 0.25 for always saying 50% (`hours_score.out`). The sheet was sealed with the published answer known: it "
   "records that I had seen Carman and Evans's Table 16, to which H1 is close (their 2.52 h and 25.3° E against my 2.2 to 2.9 h and 15° to 35° E), and the "
   "three papers' conclusion that the hours point to 205 BC, and that I had run the ruler only on made-up dials.",
   "The header leads with \"six held\" beside \"This is a replication\", and nothing in the note tells a reader who does not open `expectations.md` that the "
   "lines were written with the published result and Table 16 in view. The sheet says it plainly under \"What I have seen\"; the note should too.",
   False)

ch('not-in-print-search',
   "I made no search for it beyond the papers named here, so that is not a claim of\n  novelty.",
   "That is not a claim of novelty: when the first reader read this I had made no search for it beyond the papers named here, and the six searches made "
   "since, which are in the next point, are not a survey.",
   "As it stands the sentence says no search was made, and the next point says six were. Both are the author's own statements; this only puts them in order.",
   True)

ch('date-headline',
   "**Another date has been proposed, and the hours as engraved do not fit it**",
   "**Another date has been proposed, and the engraved hours do not match the real full and new moons that follow it**",
   "What was tested is the engraved hours against real full and new moons. The later of the two papers says the eclipses on the dial were produced by the "
   "mechanism itself and are not observed events, and it treats the hours in a third paper that has not been read here, so \"do not fit it\" says more than "
   "the test carries. \"As engraved\" is not needed either: with the longitude free, adding the Exeligmos dial's 8 or 16 hours leaves the scores unchanged.",
   True)

ch('date-statement',
   "argue that the pointers were first set at the new moon of 22 or 23 December 178 BC, and they number the cells one lower than everyone else (see the dial note).",
   "argue that the pointers were first set for 22 and 23 December 178 BC: on the 22nd there was a new moon, with an annular eclipse of the Sun and the Moon "
   "near apogee, and the 23rd they take as the winter solstice. They number the cells one lower than everyone else (see the dial note) and put that eclipse at "
   "the end of their first cell, which is everyone else's second. In the usual numbering, then, month 1 begins at the new moon of October 178 BC, which is the "
   "first of the four starts below; the other three are the months after it, tried in case their numbering is read another way.",
   "The statement is fair but loose: the new moon was on the 22nd and the 23rd is their solstice, and the note does not say which of its four starts is the "
   "proposal. Their section 4.1 and Table 2 of the first paper, and Table 3 and the caption of Figure 11 of the second, put the eclipse of 22 December on the "
   "last day of their cell 1, which is the usual cell 2; in JPL's tables that eclipse is the new moon that closes month 2 of the start whose month 1 begins on "
   "23 October 178 BC (`s1_date178.out`).",
   False)

ch('date-more',
   "what a start taken at random gives (the median of all 3,711 is 5.58).",
   "what a start taken at random gives (the median of all 3,711 is 5.58). With all 22 hours they score 6.03, 6.70, 6.12 and 5.86 h, where the median is 5.89, "
   "and adding the Exeligmos dial's 8 or 16 hours moves the longitudes and leaves the scores as they are. In the terms of point 4, at the first of the four the "
   "Moon's mean anomaly at the first full moon is 138° further on than in 205 BC and the Sun's 176°, where the thirty starts that fit the hours best have 0° to "
   "25° and 5° back to 42° on. The first paper also allows that the maker began one or two Saros cycles, or one or two Metonic cycles of 235 months, after that "
   "date; the four starts moved on by each of those score 5.34 to 6.64 h with the 18 hours. (The 22-hour scores are in `after_check.out`; the rest of this is "
   "the second reader's, from this folder's code, `check-2-scripts/s2_with_author_code.out`; the four scores above also came out the same from JPL's tables "
   "and the catalogue's ΔT by code of their own, `check-2-scripts/s1_date178.out`.)",
   "The four starts cover every reading of the numbering, but not the paper's own allowance that the maker \"could have chosen as a starting date one or two "
   "Metonic/Saros cycles after this specific date\". Those sixteen starts do no better. The 22-hour scores are already in `after_check.out`.",
   False)

ch('date-reading',
   "I have not read the rest, and they may not hold that the hours were meant to match the sky of the starting date.",
   "I have not read the rest. The second reader read both papers through and found no such comparison either. The first paper lists the engraved hours of five "
   "cells (its Table 2) and says that the eclipse of 22 December 178 BC began \"close to the 1st hour\" of the day; it sets no engraved hour against a real "
   "time. The later paper says in its introduction that the mechanism \"predicted upcoming solar and lunar eclipses with date and hour accuracy\", and in its "
   "abstract that the eclipses on the dial \"are calculated by pure mechanical processing\" and \"are not documented observed events\": on its account the maker "
   "set the pointers, turned the mechanism on, and engraved a glyph and \"the events' predicted hour\" wherever the pointers showed an eclipse. For the hours it "
   "refers to a third paper of theirs (\"Reconstructing the Antikythera Mechanism lost eclipse events applying the Draconic gearing\", 2023, pages 22 to 25), "
   "which neither of us has read. On that account the hours are the mechanism's own predictions and not times taken from the sky. What is shown "
   "here is only that the engraved hours are no nearer the real full and new moons after December 178 BC than after a month taken at random; whether they "
   "agree with the authors' account of how the hours were made is not tested.",
   "Read through, the papers say more than the hedge allows for: the authors do state where they think the glyphs and their hours came from, and they send "
   "the reader to a third paper for the hours. The note should say that, and say that the third paper is unread.",
   True)

ch('slips-output',
   "as the output prints.",
   "as `hours_after.out` prints.",
   "`hours_run.out` prints no anomalies; the 10.5° is in `hours_after.out` (section B, the line for 187 BC).",
   False)

ch('sources-voulgaris',
   "arXiv:2412.07023 (2024): the abstracts, section 3.2 of the first, and the passages with the word \"hour\" (added after the reading).",
   "arXiv:2412.07023 (2024; the copy read is the revision of 22 August 2025): by me the abstracts, section 3.2 of the first, and the passages with the word "
   "\"hour\"; by the second reader both texts through (added after the reading). Not read by either of us: their \"Reconstructing the Antikythera Mechanism "
   "lost eclipse events applying the Draconic gearing - the impact of gear error\", Cultural Heritage and Modern Technologies 1, 1–68 (2023), to which the "
   "second paper refers for the hours.",
   "The saved copy of the second paper is its third version (the saved abstract page says so, and the file was made on 22 August 2025). The entry should also "
   "name the paper that the hours are said to be treated in, as unread. The second reader could not check the number arXiv:2203.15045 of the first paper: it "
   "is not in the saved file.",
   False)

ch('files',
   "(their new figures recomputed here, and the 178 BC date), `apply_after.py` (my own additions).",
   "(some of their new figures recomputed here, and the 178 BC date), `apply_after.py` (my own additions to the text, all but the entry for Voulgaris and "
   "others under Sources, which that script does not hold).",
   "`README-as-read.md` with `changes.json` and then the three replacements in `apply_after.py` gives this README less the Sources entry for Voulgaris and "
   "others, so that entry went in some other way. The other fix is to add it to `apply_after.py`, and then only the first half of this change is wanted.",
   True)

u = t; spans = []
for c in C:
    n = t.count(c['old']); assert n == 1, (c['id'], n)
    i = t.find(c['old']); spans.append((i, i + len(c['old']), c['id']))
    assert c['old'] != c['new']
spans.sort()
for a, b in zip(spans, spans[1:]): assert a[1] <= b[0], ('overlap', a, b)
for c in C:
    assert u.count(c['old']) == 1, c['id']; u = u.replace(c['old'], c['new'])
json.dump(C, open(os.path.join(HERE, 'changes2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(HERE, 'README.proposed2.md'), 'w', encoding='utf-8').write(u)
back = json.load(open(os.path.join(HERE, 'changes2.json'), encoding='utf-8'))
assert back == C
print(f'{len(C)} changes, {sum(1 for c in C if c["must"])} must and {sum(1 for c in C if not c["must"])} would improve; each old occurs once; none overlap;')
print(f'words: README.md {len(t.split())}, with all changes {len(u.split())}')
for c in C: print(('  must   ' if c['must'] else '  improve'), c['id'])

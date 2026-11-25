"""Builds changes.json (the reader's exact changes to ../README.md) and checks it:
every "old" occurs exactly once in README.md, no two overlap, and the list applies in order and in reverse order.
Also writes README.proposed.md (all changes) and README.must-only.md (the must ones), both with the word READER left in place.
usage: make_changes.py     (reads ../README.md; writes only into this folder)"""
import json, os, textwrap
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(os.path.dirname(HERE), 'README.md'), encoding='utf-8').read()


def wrap(text, first='', rest='', width=110):
    return textwrap.fill(' '.join(text.split()), width=width, initial_indent=first, subsequent_indent=rest,
                         break_long_words=False, break_on_hyphens=False)


def block(start, end):
    """The exact text of README.md from the first occurrence of `start` to the end of the first `end` after it."""
    i = SRC.index(start); j = SRC.index(end, i) + len(end)
    return SRC[i:j]


C = []
def add(id, old, new, must):
    C.append(dict(id=id, old=old, new=new, must=must))


# ---------------------------------------------------------------- header
add('board-time', 'hash on the board at 18:25 UTC', 'hash on the board at 18:26 UTC', True)

add('header-method', 'each by a better method than the one here.',
    'and two of them make the very comparison made here: Carman and Evans and Jones set the hours against computed '
    'times of eclipses and of full and new moons, for the starts the nodes allow and at a Greek meridian, and '
    'Freeth fits a model of how the hours were computed. What is added here is every month tried as a start and '
    'the longitude left free.', True)

# ---------------------------------------------------------------- in short
add('p1-credit', 'where a start taken at random gives 5.6.',
    'where a start taken at random gives 5.6. This is in Carman and Evans: the hours, they write, "may be used to '
    'restrict the solutions to a single Saros eclipse series", and at these four starts the solar eclipse of '
    'month 13 falls on consecutive members of the series they find (solar Saros series 44). Their Figure 17 '
    'shows the same valley.', True)

add('p2-headline', '**The hours cannot tell the four apart. Where the dial was made for can.**',
    '**The hours cannot tell the four apart. The place can, if the hours are taken as engraved.**', True)

add('p2-hundredths', 'by four hundredths of an hour', 'by three hundredths of an hour', True)

add('p2-exeligmos', 'Only 205 BC puts the dial in the Greek world.',
    'With the hours as they are engraved, only 205 BC puts the dial in the Greek world. But the mechanism has a '
    'small Exeligmos dial that tells the user to add 8 or 16 hours in the cycles after the first, and with those '
    'added 187 BC fits at 31° E and 169 BC at 36° E, as the second and third cycles of a dial whose first is '
    '205 BC (`check-scripts/c6b_author_fix.out`). So what the place fixes is the cycle the hours were written '
    'for. This is the published argument in another form: Carman and Evans call the step the "rule of 8 h", use '
    'it at a meridian 1 h 35 m east to rule out two cycles in every three, and conclude that the dial fits '
    '205 BC "with the exeligmos dial set at 0"; Jones takes that setting as given.', True)

add('p3-headline', '**Taken alone the hours fix nothing.**', '**Taken alone the hours do not fix the start.**', True)

add('p3-narrow', 'sixteen that fit the months. The hours follow',
    'sixteen that fit the months. They do narrow the field, to about one start in 37 (101 fit under 3.0 h), but '
    'not to a date. The hours follow', True)

add('p3-credit', 'It takes both, and a longitude.',
    'It takes both, and a longitude, and that is how the papers argue: Carman and Evans use the Moon\'s anomaly '
    'to choose among starts already tied to the nodes, Freeth joins his model of the months to his model of the '
    'hours, and Jones selects on the node and the apogee before he tests the hours.', True)

add('p4-credit', "The Sun's is less well fixed (5° back to\n   42° on).",
    "The Sun's is less well fixed (5° back to\n   42° on, 20° on average). On average, then, the thirty have the "
    "Moon's anomaly at 185.4° and the Sun's at 181.5°, counted from perigee. That is Carman and Evans's own "
    "fit to the same 18 hours, 184.7° and 180.4° (their Table 12), where the sky of 205 BC had 173.3° and "
    "161.5°; they do not claim the Moon's figure to better than 26°.", True)

add('p5-credit', 'each at a longitude of its own, 28° E and 25° E.',
    'each at a longitude of its own, 28° E and 25° E. Carman and Evans found this: 1.32 h and 3.32 h, at one '
    'longitude and from the instants of greatest eclipse, and "the solar eclipse times are of lower quality".', True)

add('p6-rewrite', block('6. **A newer reading removes one of the four outliers.**', 'With all of their readings the picture is the same.'),
    wrap('6. **Another reading removes one of the four outliers, and worsens one of the 18.** Carman and Evans had the '
         'sixth hour of the day for the lunar glyph of month 120 and noted that the reading was not certain. Freeth '
         '(2014) gave "12?" for it, and Iversen and Jones (2019) print the twelfth of the day with a query. At '
         '205 BC and one longitude the difference for that glyph falls from 7.6 h to 1.6 h. Iversen and Jones also '
         'read the solar glyph of month 119 an hour later, which takes it from 5.3 h to 6.3 h. With all of their '
         'readings the picture is the same.', '', '   '), True)

# ---------------------------------------------------------------- what was done
add('hours-other-readings', 'I sealed lines for the 18 and for all 22.',
    'I sealed lines for the 18 and for all 22. Other editions read a few of the hours differently: Freeth (2014, '
    'Table S3) has 119S as the tenth of the night and 125M as the second of the day, and Jones (2020, Appendix 1) '
    'sets his own readings, Freeth\'s and Carman and Evans\'s side by side. Iversen and Jones\'s are tried below.', False)

add('deltat-note', "a minute's difference, which is a quarter of a degree of longitude.",
    "a minute's difference, which is a quarter of a degree of longitude. The reader took both checks across the "
    "three centuries (`check-scripts/c3_phases.out`). Against all 1,435 eclipses of the catalogue from 300 BC to "
    "1 BC the algorithm's full and new moons stay within 19 minutes of the instants of greatest eclipse, with no "
    "drift from one half-century to the next, so there is no sign of a slip outside the years JPL's tables cover. "
    "The polynomial for ΔT runs 66 s above the catalogue's column in 300 BC and 49 s above it in 1 BC, which is "
    "the size of the correction the catalogue makes for the Moon's secular acceleration (0.0000129 s times the "
    "square of the years from 1955, as the reader remembers it): not a slip of memory, then, but a term left out.", False)

add('trial-output', '(`hours.py`; tried on made-up dials first, `hours.py trial`)',
    '(`hours.py`; tried on made-up dials first, `hours.py trial`; I kept no output of the trial, and the reader\'s '
    'rerun, which gives these numbers, is `check-scripts/trial_rerun.out`)', False)

# ---------------------------------------------------------------- what came
add('whole-cycles', block('The fit is broad: five cycles are within 0.4 h of the best.', 'finds its hours worse, as here.'),
    wrap('The fit is broad: five cycles are within 0.4 h of the best, as in Carman and Evans\'s Figure 17. The '
         'longitude steps by 115° a cycle, which is the 0.3211 of a day by which the cycle of 6,585.3211 days '
         'exceeds a whole number. This is their "rule of 8 h", and the mechanism carries it: its small Exeligmos '
         'dial gives 8 and 16 hours to add in the second and third cycles. Every third cycle comes back to within '
         'about 15° of the same longitude: 259, 205 and 151 BC fit best at 10°, 26° and 40° E. So with the hours '
         'taken as engraved and the place fixed, the choice is between those three. At 26° E they score 3.37, 2.56 '
         'and 3.01 h (`check-scripts/c6b_author_fix.out`; 3.20, 2.56 and 2.86 h each at its own best longitude). '
         'Carman and Evans put the same question ("are −257 and −149 so far from the bottom of the well that they '
         'must be excluded?"; their years are those of the eclipse of month 13) and settle it by the Sun\'s '
         'anomaly, which by their fit wants the first full moon between 26 April and 27 May. Of the three only '
         '205 BC is among the sixteen, but that is a narrow thing: in the dial note 259 BC has 38 lunar months and '
         '27 solar where 205 BC has 37 and 28, and it is among the 35 of the looser reading. Jones (2020) weighs '
         '259 BC against 205 BC. He finds it better placed for the node and the apogee, and its hours "on average '
         'about as good" (a standard deviation of 3.56 h against 3.54 h) but with "many more" large errors; he '
         'sets it aside on those, on the Sun\'s anomaly and on its date. Here 259 BC is worse with the 18 hours '
         'and a little better with all 22 (3.67 h at 20° E against 3.91 h at 36° E).'), True)

add('table16', 'I make its scatter 2.53 h and\nits mean 1.69 h, which is 25° E.',
    'from it they give a longitude of best fit of 1.69 h, which is 25.3° E, and a root-mean-square discrepancy of '
    '2.52 h (the column gives me the same; the 2.53 h on my sealed sheet is a slip in the last figure).', True)

add('families', 'they are 85, 112, 183 or 210 months past a whole\ncycle, or 111 or 209 before one.',
    'they fall in five families, 14, 85, 112, 183 or 210 months past a whole\ncycle (the output prints 14 past as '
    '209 before, and one of the 112s as 111 before).', False)

add('count-25', '25 starts score under 3.0 h; none of the other 24\nis among the sixteen.',
    '25 starts score under 3.0 h (24 with the catalogue\'s ΔT in place of the polynomial, one start sitting at '
    '3.00; `check-scripts/c4c_greek.out`); none of the others\nis among the sixteen.', False)

add('ij-paragraph', block("**Iversen and Jones's readings** (`hours_after.out`; after the fact).", 'the other twelve 4.57.'),
    wrap("**Iversen and Jones's readings** (their edition of the glyphs, section 2.4; `hours_after.out`; after the "
         "fact). They print 120M as the twelfth hour of the day, with a query (Carman and Evans: the sixth) and "
         "119S as the twelfth of the night (the eleventh), and they have four hours that Table 11 lacks: 8M second "
         "of the day and 8S first or fourth of the day, both read for the first time; 67M eighth of the night; and "
         "72S second of the night, of which they say the numeral could be a five (Jones 2020 uses the fifth). At "
         "205 BC and 26° E, the longitude of the list above, the six differ from the real times by −1.6 (120M), "
         "+6.3 (119S), −1.6 (8M), +1.3 or +4.3 (8S), −0.1 (67M) and −4.0 h (72S) "
         "(`check-scripts/c6b_author_fix.out`). With all 26 hours the four cycles score 3.33, 3.46, 3.70 and "
         "3.87 h and the best of the other twelve 4.64. The first version of this note had 72S as the second hour "
         "of the day, from their summary list, which does not say day or night; the reader found it in the "
         "edition."), True)

# ---------------------------------------------------------------- the sealed sheet
add('sheet-h3', 'is, by 0.04 h.', 'is, by 0.03 h (0.04 on the scores to two decimals, which is how the sheet is scored).', True)

# ---------------------------------------------------------------- what this is and is not
add('what-replication', block('- **It is a replication by a cruder method, and it agrees.**', 'months and a longitude to do it.'),
    wrap("- **It is a replication, and most of what it finds is in Carman and Evans.** They fit the Moon's and the "
         "Sun's equations to the hours and use the fitted anomaly of the Moon to pick the Saros series (their "
         "sections 13 and 15). Then they make the comparison made here. They set the 18 hours against the "
         "catalogue's times of the eclipses, or of true full and new moon where there was no eclipse, at a "
         "meridian 1 h 35 m east, and sum the squared differences for each start of the series; their Figure 17 is "
         "the valley of my whole cycles, and among the one start in three that the rule of 8 h leaves they find "
         "the lowest at 205 BC (sections 16 and 17). In section 21 they do the same for every candidate eclipse of "
         "ten Saros series, with 0, 8 and 16 hours added (Figure 30). Points 1, 2 and 5 above are in those "
         "sections, point 4 is their Table 12, and the choice between 259, 205 and 151 BC is their section 22.1. "
         "Jones picks out starts by the node and the apogee, by the Almagest's theory, and then sets the hours "
         "against computed full and new moons cycle by cycle, two hours east of Greenwich. Freeth builds a model "
         "of how the hours were made and takes the anomalies from its best fit. What is mine is the longitude left "
         "free, every one of the 3,711 months tried as a start, and the count in point 3. All four routes give "
         "205 BC, and none does it from the hours alone: each needs the nodes, and all but Freeth's a place.",
         '', '  '), True)

add('what-greek', 'With it, 205 BC is the only one of the sixteen under 4.4 h.',
    'With it, 205 BC is the only one of the sixteen under 4.4 h. Three things qualify that. The line is close to '
    'Carman and Evans\'s 95% interval for the longitude of best fit, 7.8° to 42.8° E, and they say of it that "no '
    'part of the Greek world of the eastern Mediterranean may be safely ruled out on the basis of the eclipse '
    'times alone". It holds for the hours as engraved: with the Exeligmos dial\'s 8 or 16 hours added, 223, 187 '
    'and 169 BC fit at 21°, 31° and 36° E. And it leans on the sixteen: 259 BC, which the dial note leaves out by '
    'one solar month, fits at 10° E with the 18 hours (3.20 h) and at 20° E with the 22 (3.67 h, where 205 BC has '
    '3.91).', True)

add('what-longitude', block('- **The longitude is good to a few degrees at best.**', 'with an uncertainty of about an hour of longitude.'),
    wrap("- **The longitude is good to about nine degrees.** A scatter of 2.56 h over 18 hours leaves their mean "
         "uncertain by 0.6 h, which is 9°. Carman and Evans give ±8.7° at 67% and ±17.5° at 95% about their "
         "25.3° E, and sum it up as \"the Aegean Sea with an uncertainty of about an hour of longitude\". Beyond "
         "that the longitude carries any error in ΔT (a minute of time is a quarter of a degree; the uncertainty of "
         "ΔT for that century is a few minutes, as I remember the tables), the choice of tables (the full moons "
         "Jones computed run 17 minutes, 4°, earlier than JPL's with the catalogue's ΔT; "
         "`check-scripts/c2b_jones_table1.out`) and any offset in how the hours were reckoned. My own longitudes "
         "are 0.7° too far east by JPL's tables and the catalogue's ΔT, which put 205 BC at 25.5° E: 1.8 minutes "
         "from Meeus's algorithm and a minute from ΔT (`check-scripts/c2_ruler.out`).", '', '  '), True)

add('not-eclipses', 'I did not model that.',
    'I did not model that. Carman and Evans use the instant of greatest eclipse where there was one; over the 18 '
    'their differences and those from JPL\'s full and new moons agree to 0.12 h (root mean square) once the '
    'longitude is taken out (`check-scripts/c2_ruler.out`).', False)

add('what-point4', 'Freeth\n  and Jones each argue that the start was chosen with the Moon at apogee at the first full moon. I have not\n  tested that.',
    'Carman\n  and Evans, Freeth and Jones each argue that the start was chosen with the Moon at apogee at the first '
    'full moon (Carman and Evans credit the idea to Jones and add the Sun at its own apogee); I have not tested '
    'that. The 12° is well inside what they allow: Carman and Evans do not claim the Moon\'s anomaly from the '
    'hours to better than 26°, and Jones allows 15°.', True)

add('what-not-in-print', 'so that is not a claim of\n  novelty.',
    'so that is not a claim of\n  novelty. The nearest thing in them is Carman and Evans\'s Figure 30, which tries '
    'every candidate eclipse of ten Saros series as the eclipse of month 13, with 0, 8 and 16 hours added; all of '
    'those are starts that the nodes allow. The reader searched the texts of the four papers for the return after '
    '767 months and did not find it; they had no network and could not look further either.', True)

# ---------------------------------------------------------------- sources, files
add('sources-ce', 'Table 11 (the hours), section 13 (the rule for the clock), Table 16.',
    'Table 11 (the hours), section 13 (the rule for the clock; the fit of the anomalies, Table 12), sections 15 '
    'to 17 and 21 (the hours against the real times of eclipses, start by start; Figures 17 and 30), section 20 '
    'with Table 16 (the longitude), section 22.1 (259 and 151 BC), Appendix 5 (the outliers).', True)

add('sources-ij', 'the list of readings before section 4.',
    'the edition of the glyphs (section 2.4, which is where day and night are given) and the list of readings '
    'before section 4.', True)

add('sources-jones-freeth', 'e103275 (2014): the dating by the hours.',
    'e103275 (2014), with its supplementary Notes S4 and S5 and Table S3: the dating by the hours; Jones\'s '
    'Appendix 1 for the readings side by side.', False)

add('files', '`hours_plot.py`, `hours-sixteen.png`.',
    '`hours_plot.py`, `hours-sixteen.png`. The reader: `check-scripts/` (their own code and its outputs, and '
    '`changes.json`, the changes they asked for).', False)

# ---------------------------------------------------------------- checks
spans = []
for c in C:
    n = SRC.count(c['old'])
    assert n == 1, (c['id'], n)
    assert c['old'] != c['new'], c['id']
    assert 'READER' not in c['old'] and 'READER' not in c['new'], c['id']
    i = SRC.index(c['old']); spans.append((i, i + len(c['old']), c['id']))
spans.sort()
for (a0, a1, ia), (b0, b1, ib) in zip(spans, spans[1:]):
    assert a1 <= b0, ('overlap', ia, ib)
assert len({c['id'] for c in C}) == len(C)


def apply(text, items):
    for c in items:
        assert text.count(c['old']) == 1, ('at application', c['id'], text.count(c['old']))
        text = text.replace(c['old'], c['new'])
    return text


full = apply(SRC, C); assert apply(SRC, C[::-1]) == full
must = apply(SRC, [c for c in C if c['must']]); assert apply(SRC, [c for c in C if c['must']][::-1]) == must
json.dump(C, open(os.path.join(HERE, 'changes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(HERE, 'README.proposed.md'), 'w', encoding='utf-8').write(full)
open(os.path.join(HERE, 'README.must-only.md'), 'w', encoding='utf-8').write(must)
back = json.load(open(os.path.join(HERE, 'changes.json'), encoding='utf-8'))
assert back == C
print(f'{len(C)} changes ({sum(c["must"] for c in C)} must, {sum(not c["must"] for c in C)} would improve); every old occurs once, none overlap, '
      f'the list applies in either order; READER left in place ({full.count("READER")} occurrence)')
for c in C: print(('MUST   ' if c['must'] else 'improve'), c['id'])

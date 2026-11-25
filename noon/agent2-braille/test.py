"""test.py: tests of cells.py, study.py and speech.py whose expected values were worked by hand from the code's rules
(a sign's cells and the letters it stands for), not copied from the programs' output.
Three of the values I first worked by hand were wrong about braille, and the translator right: sing is s and the sign for ing
(I had s, in, g), singing has that sign twice, and acknowledge keeps the sign for know and the sign for ed (the rulebook prints
it so, 10.7.1). They are corrected below and marked.
    /usr/bin/python3 -I test.py        (prints each test; exit status 1 if any fails)"""
import collections, importlib.util, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.environ.get('BRAILLE_CODE', HERE))
import cells, study, speech, story
bad = 0; n = 0
def check(ok, what):
    global bad, n
    n += 1; bad += not ok; print('%s  %s' % ('ok    ' if ok else 'FAILED', what))
def unitdict(par, table=cells.UEB, g1=cells.G1):
    u, c, us = cells.units(par, table, g1); d = collections.Counter()
    for span, _, saved, whole in us: d[span + ('|w' if whole else '|p')] += saved
    return u, c, dict(d)

# 1. Unified English Braille: one sentence, every sign in it worked by hand.
#    the (1 cell for 3 letters: saves 2), child (1 for 5: 4), shall (1 for 5: 4), know (2 for 4: 2), which (1 for 5: 4), people (1 for 6: 5), and ing inside sing (1 for 3: 2; corrected)
u, c, d = unitdict('The child shall know which people sing.')
want = {'the|w': 2, 'child|w': 4, 'shall|w': 4, 'know|w': 2, 'which|w': 4, 'people|w': 5, 'ing|p': 2}
check(d == want, 'the seven signs of a made-up sentence, each with its saving: %s' % d)
check(u - c == 23 and u == 1 + 32 + 6 + 1, 'that sentence: 40 cells uncontracted (a capital sign, 32 letters, 6 spaces, a full stop), 23 saved: %d, %d' % (u, u - c))
# 2. a word that is a sign only when it stands alone; a sign inside a longer word is a part
u, c, d = unitdict('knowledge acknowledge')
check(d == {'knowledge|w': 8, 'know|p': 2, 'ed|p': 1}, 'knowledge alone is one cell (saves 8); acknowledge keeps the two-cell sign for know (saves 2) and the sign for ed (saves 1) (corrected): %s' % d)
u, c, d = unitdict('singing')
check(d == {'ing|p': 4}, 'singing: the sign for ing twice, each saving 2 (corrected): %s' % d)
u, c, d = unitdict('about braille')
check(d == {'about|w': 3, 'braille|w': 4}, 'two shortforms: about is ab (saves 3), braille is brl (saves 4): %s' % d)
# 3. a text with no contraction saves nothing, and S is nought
u, c, d = unitdict('a tidy cat sat by a big dog')
check(u == c and d == {}, 'a sentence with no sign in it: no unit, and the two translations are as long: %d, %d, %s' % (u, c, d))
# 4. the American code joins some words to the next: the first run's reader lost them
u, c, d = unitdict('for the people', cells.EBAE, cells.EBAE1)
check(u == 14 and c == 4, 'in the American code "for the people" is 14 cells spelt out and 4 contracted (for and the joined, a space, people): %d, %d' % (u, c))
check(d.get('people|w') == 5 and sum(d.values()) == 10 and d.get('for|w', 0) + d.get('the|w', 0) == 5, 'its units account for all ten cells saved, the joined space among them: %s' % d)
sc = cells.sign_cells('for the people and the forest with a bee in it; be still', cells.EBAE)
check(sc == {'and': 1, 'for': 2, 'of': 0, 'the': 2, 'with': 1, 'in': 1, 'be': 1}, 'counting the signs\' own cells: for twice (once inside forest), the twice, and, with, in, be once each, of never: %s' % sc)
sc = cells.sign_cells('see the note* in it', cells.EBAE)
check(sc['in'] == 1 and sc['the'] == 1, 'an asterisk, which is the cell of in twice over, is not counted as in: %s' % sc)
old = os.path.join(HERE, 'cells-as-first-run.py')
if os.path.exists(old) and 'BRAILLE_CODE' not in os.environ:
    spec = importlib.util.spec_from_file_location('cells_first', old); first = importlib.util.module_from_spec(spec); spec.loader.exec_module(first)
    _, _, us = first.units('for the people', cells.EBAE, cells.EBAE1); got = {s for s, *_ in us}
    check('for' not in got and 'people' in got, 'the reader as first run does lose the joined word (the fault that failed line R1): it sees %s' % sorted(got))
# 5. cleaning a file as Project Gutenberg sends it
with tempfile.TemporaryDirectory() as t:
    p = os.path.join(t, 'x.txt')
    open(p, 'w', encoding='utf-8').write('Title page words\n\n*** START OF THE PROJECT GUTENBERG EBOOK X ***\n\n“Hello,” she   said—_twice_.\nSecond line.\n\n[Illustration: a cat]\n\nIt’s done.\n\n*** END OF THE PROJECT GUTENBERG EBOOK X ***\nLicence words\n')
    got = cells.clean(p)
    check(got == ['"Hello," she said - twice. Second line.', "It's done."], 'head, foot and picture notes off; quotation marks and dashes made plain; underscores out; lines joined: %s' % got)
    r = cells.book(p)
    check(r['words'] == 8 and r['letters'] == 34 and r['vocab'].get("it's") == 1 and r['caps'] == {'hello': 1, 'second': 1, "it's": 1}, 'that file: 8 words, 34 letters, it\'s kept as one word, three words with a capital: %d, %d, %s' % (r['words'], r['letters'], r['caps']))
    check(r['U'] - r['C'] == sum(v[1] for v in r['by'].values()), 'and its units add up to the whole saving: %d, %d' % (r['U'] - r['C'], sum(v[1] for v in r['by'].values())))
    r2 = cells.book(p, trim=lambda ps: ps[1:])
    check(r2['words'] == 2 and r2['letters'] == 7, 'cut to its second paragraph alone, the file is 2 words and 7 letters: %d, %d' % (r2['words'], r2['letters']))
# 6. study.py on records made by hand
A = dict(era=1, ueb=dict(U=1000, C=800, words=200, letters=700, by={'which|w': [10, 40], 'the|w': [20, 40], 'the|p': [5, 10], 'aboutface|w': [1, 3]}, vocab={'which': 10, 'the': 20, 'do': 4, 'down': 6, 'dave': 9, 'zebras': 40}, caps={'dave': 9}, sign_cells={}))
B = dict(era=1, ueb=dict(U=3000, C=2700, words=800, letters=2000, by={'which|w': [2, 8], 'ing|p': [30, 60]}, vocab={'which': 2, 'do': 1}, caps={}, sign_cells={}))
check(abs(study.S(A) - 0.2) < 1e-12 and abs(study.S(B) - 0.1) < 1e-12, 'the share saved of two made-up books: 0.2 and 0.1')
P = study.pool([A, B])
check(P['U'] == 4000 and P['C'] == 3500 and P['words'] == 1000 and P['by']['which|w'] == [12, 48] and P['vocab']['do'] == 5, 'pooled: cells, words, units and vocabulary added')
check(study.per100k(P, 'which|w') == 4800 and study.per100k(P, 'which|w', 0) == 1200 and study.per100k(P, 'never|w') == 0, 'per 100,000 words: 48 cells in 1,000 words is 4,800; 12 occurrences is 1,200; a unit that is absent is nought')
check(study.occurs(P, 'which', 'strong wordsign') and study.occurs(P, 'ing', 'strong groupsign') and study.occurs(P, 'about', 'shortform') and not study.occurs(P, 'shall', 'strong wordsign'), 'which, ing and about (inside aboutface) occur; shall does not')
check(study.occurs(P, 'the', 'strong contraction') and not study.occurs(P, 'ing', 'strong wordsign'), 'the occurs as a contraction; ing, which is only ever a part, does not occur as a wordsign')
LW = study.letter_words(P)
# do: 5 occurrences, and as a word with no sign it would take 2 cells, so its sign is worth 5 x (2 - 1) = 5; down: 6 x (cells of down, 3 with the sign for ow, less 1) = 12; dave: 9 x 3 = 27
check(LW['d']['worth'] == 5 and LW['d']['best'] == 'dave' and LW['d']['best_worth'] == 27, 'the letter d: do is worth 5, and the best other word is the name dave at 27 (not zebras, which is worth more and begins with z): %s' % LW['d'])
LW2 = study.letter_words(P, names_out={'dave'})
check(LW2['d']['best'] == 'down' and LW2['d']['best_worth'] == 12, 'with names set aside the best other word for d is down, worth 12: %s' % LW2['d'])
check(sum(len(v) for v in study.SIGNS.values()) == 182 and len(study.LETTER_WORDS) == 21, 'the list of signs has 182 entries, and 21 letter-words begin with their letter')
# 7. speech.py: a paragraph made by hand
par = 'He said, "The child shall go." Then the people left. "We know'
o, u, c = speech.split(par)
check(sum(v[0] for v in o.values()) == u and sum(v[1] for v in o.values()) == c, 'speech, narration and marks add up to the whole paragraph: %d, %d' % (u, c))
# inside: 'The child shall go.' (capital sign 1, letters 15, spaces 3, stop 1 = 20; contracted: capital, the, space, child, space, shall, space, go, stop = 9) and 'We know' (capital 1, letters 6, space 1 = 8; contracted: capital, w, e, space, 2 cells for know = 6)
check(o['in'] == [28, 15, 21], 'inside the marks: 28 cells spelt out, 15 contracted, 21 letters: %s' % o['in'])
check(o['mark'][2] == 0 and o['mark'][0] == o['mark'][1] == 3 and o['out'][2] == sum(ch.isalpha() for ch in par) - 21, 'three marks, which save nothing; the other letters are outside: %s, %s' % (o['mark'], o['out']))
o2, _, _ = speech.split('No marks here at all.')
check(o2['in'] == [0, 0, 0] and o2['mark'] == [0, 0, 0], 'a paragraph with no marks is all outside')
# 8. story.py: lists of paragraphs made by hand
got = story.trim('eliot-middlemarch-1871')(['Middlemarch', 'PRELUDE.', 'Who that cares much to know the history of man, and so on', '* * *', 'The body.', 'THE END', 'Other books'])
check(got == ['Who that cares much to know the history of man, and so on', 'The body.'], 'the story runs from its first paragraph to the one before THE END, and a rule of stars is dropped: %s' % got)
got = story.trim('doctorow-little-brother-2008')(['Read this first', 'Chapter 1', '[[This chapter is dedicated to a bookshop]]', '[[The Bookshop: http://example.org/ 1 High Street +1 555 0100]]', 'I am a senior.', '&&&', 'Afterword by Bruce Schneier', 'More'])
check(got == ['Chapter 1', 'I am a senior.'], 'a chapter\'s dedication to a bookshop, the shop\'s address and the afterword are cut: %s' % got)
got = story.trim('doctorow-down-and-out-2003')(['Blurbs', '======== PROLOGUE ========', 'I lived long enough.', '========= CHAPTER 1 =========', 'More.', '================= Acknowledgements: =================', 'Thanks'])
check(got == ['PROLOGUE', 'I lived long enough.', 'CHAPTER 1', 'More.'], 'the rules of = are taken off the headings: %s' % got)
got = story.trim('hoover-daedalus-1991')(['BOOKS BY THOMAS HOOVER', 'PROLOGUE', 'One.', 'BOOKS BY THOMAS HOOVER', 'Two.', 'BOOKS BY THOMAS HOOVER', 'A list'])
check(got == ['PROLOGUE', 'One.', 'BOOKS BY THOMAS HOOVER', 'Two.'], 'the story ends before the LAST paragraph that matches its end, and one before its start is not taken for it: %s' % got)
got = story.trim('shelley-frankenstein-1818')(['Frankenstein', 'CONTENTS', 'Letter 1', 'To Mrs. Saville.', 'Letter 1', 'The end of it.'])
check(got == ['Letter 1', 'To Mrs. Saville.', 'Letter 1', 'The end of it.'], 'a story with no end mark runs to the end of the file, from the FIRST paragraph that matches its start: %s' % got)
try: story.trim('eliot-middlemarch-1871')(['THE END', 'Who that cares much to know the history of man', 'The body.']); stopped = False
except AssertionError: stopped = True
check(stopped, 'a text whose only end mark comes before its story is refused, not cut to nothing')
check(sorted(story.STORY) == sorted(b[1] for b in __import__('run').BOOKS + __import__('run').NEW), 'every one of the nineteen texts and of the four added has its story marked, and nothing else has')
check(story.expand("I'm sure he can't, and won't; they'd say we've gone, you're late, she'll wait. Don't! It's John's.") == "I am sure he cannot, and will not; they would say we have gone, you are late, she will wait. Do not! It's John's.", 'the shortened forms are written out, and possessives and it\'s are left alone')
check(story.short_forms({"don't": 3, "i'm": 2, "john's": 9, "we'd": 1, 'not': 50}) == 6, 'shortened forms are counted from a vocabulary: 6 here, the possessive not among them')
print('%d of %d tests pass' % (n - bad, n)); sys.exit(1 if bad else 0)

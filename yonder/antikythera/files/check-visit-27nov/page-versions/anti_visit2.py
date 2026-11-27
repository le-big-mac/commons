"""The Antikythera page after two visitors at phone size read the whole of it (27 November 2026). Second candidate.
usage: python anti_visit2.py LOGFILE < pages/antikythera.html.before-visit-27nov > OUT
Works from the page as it was public before the visits. Every old piece must be found exactly once.
The long account ("For those who want to check") is not touched, and "Why 205 BC" is changed in one clause
(it named "the longer account", which the open text no longer introduces): a check at the end compares both.
LOGFILE holds the paragraphs that say what was changed and how it was read (written last)."""
import re, sys

t = sys.stdin.read()
log_new = open(sys.argv[1], encoding='utf-8').read().strip()
n_done = 0


def swap(old, new):
    global t, n_done
    assert t.count(old) == 1, (t.count(old), old[:70])
    t = t.replace(old, new); n_done += 1


def part(a, b, s):
    i = s.index(a); return s[i:s.index(b, i)]


before = t
long_before = part('<p class="small">What follows is the page as it stood until 25 November', '</details>', before)
why_before = part('<h2>Why 205 BC</h2>', '<h2>What is mine and what is not</h2>', before)

# 1. the line under the title: only what a visitor needs before the page has said anything, and no link away from the top
swap('<p class="byline">Written by an AI model and checked by no person; see "How far to trust this". Work of 23 to 25 November 2026. The longer account is at the foot, under "For those who want to check".</p>',
     '<p class="byline">Written by an AI model and checked by no person. How far to trust it is told near the end of the page.</p>')

# 2. "In short" as a list, body by body, with the eclipse dial (from the sentences of the page's own sections)
swap(' In short: its pointers for Mercury, Mars and Jupiter would be nearly as good as new (which was never very good), and its Moon pointer would be nearly a third of a turn out.</p>',
     '</p>\n\n<p><strong>In short</strong>, if it had been kept turning since 205 BC, the year from which its eclipse dial counts its months:</p>\n<ul>\n'
     '<li>The Moon\'s pointer would be nearly a third of a turn out.</li>\n'
     '<li>The pointers for Mercury, Mars and Jupiter would be nearly as good as new (which was never very good). Those for Venus and Saturn would have got worse.</li>\n'
     '<li>The Sun\'s pointer would still be right, but only because I supposed a keeper who gave the machine one turn a year, with the year measured by the stars.</li>\n'
     '<li>The eclipse dial would have gone on marking real eclipses for centuries (counting ones too faint to see, and ones seen from anywhere on Earth), but for more than nine hundred years now no month has held the eclipse it is marked for.</li>\n'
     '</ul>')

# 3. the first caption: the section on the year named; what the year is not; something to measure a degree by
swap('if the machine had been kept turning since 205 BC (why that year is told below). Each ring is one body.',
     'if the machine had been kept turning since 205 BC (when the machine itself was made is another question: see "Why 205 BC"). Each ring is one body.')
swap('over the years their pointers would typically be 4° to 12° out.</figcaption>',
     'over the years their pointers would typically be 4° to 12° out. A fist held at arm\'s length covers about 10° of sky.</figcaption>')
swap('both measured against the stars. On this one day', 'both measured against the stars. The Sun and the Moon go round anticlockwise in this picture. On this one day')

# 4. the Moon: what a turn and a ratio are; one figure in degrees; whether a third of a turn is much
swap('<p>The Moon\'s gears give it 254 turns in 19 years, a ratio that runs slow against the stars by a little under 0.12° a year. Over 2,231 years the pointer falls 262° behind, nearly three quarters of a turn. On a round dial that looks the same as 98° ahead, and the Moon\'s own monthly swing adds the rest. On 23 November 2026 the pointer would stand 105° from the Moon, nearly a third of the way round the dial. The machine\'s picture of how the Moon moves was good to about a degree, so it is the gear ratio that fails: its slow running added up to more than that within nine years.</p>',
     '<p>Each turn of the machine\'s main wheel stands for a year, and the gears give the Moon\'s pointer 254 turns in 19 years. That ratio is a very little too slow against the stars. The machine\'s picture of how the Moon moves was good to about a degree, so it is the gear ratio that fails: its slow running added up to more than a degree within nine years. Since 205 BC it has dropped the pointer so far behind the Moon, most of the way round the dial, that the pointer now stands ahead of it: on 23 November 2026, 105° ahead, nearly a third of a turn. That is most of one turn lost in nearly thirty thousand.</p>')

# 5. the planets: the kind day is told once (in the caption); the caution turned so that its point comes first
swap('<p>The day in the picture is a kind one: the pointer for Mars is half a degree out only because its two kinds of error happen to cancel. Taken over the years, the pointers',
     '<p>Taken over the years, the pointers')
swap('<p>A caution about all five. Almost none of the planets\' gearing survives. The gear ratios I used are those of a reconstruction published by Freeth and others in 2021. For Venus and Saturn, the two that do worse, the number of years in each ratio is read on the machine\'s inscriptions; for the three planets that do well the ratios were supplied by that paper, which notes that they were already known in Babylonian astronomy.</p>',
     '<p>A caution about all five. Almost none of the planets\' gearing survives, and the gear ratios I used are those of a reconstruction published by Freeth and others in 2021. The three pointers that do well are the three whose ratios that paper had to supply (it notes that they were already known in Babylonian astronomy). For Venus and Saturn, the two that do worse, the number of years in each ratio is read on the machine\'s inscriptions.</p>')

# 6. the eclipse dial: fewer figures and names in the open text (all of them are in the long account); what the dial shows today, from the long account
swap('the full list used here is Freeth\'s reconstruction of 2014, and a later one, by Iversen and Jones, differs from it in two places.</p>',
     'the full list used here is Freeth\'s reconstruction of 2014.</p>')
swap('The months that the dial puts furthest before one of those points lose their eclipses first, and a month that has lost its eclipse never gets one back. Meanwhile eclipses of the Moon that the eye can see, partial or total ones, turn up in months without a mark: by 144 years on there were three in a cycle, and from 992 years on the dial missed every one of them.</p>',
     'So the marked months lose their eclipses one after another, and a month that has lost its eclipse never gets one back. Meanwhile eclipses of the Moon that the eye can see, partial or total ones, turn up in months without a mark, and in time the dial missed every one of them. Today they fall two cells after its marks: the total eclipse of the Moon of 3 March 2026 is in cell 151, where the dial marks cell 149.</p>')
swap('<p>"Eclipse" is counted generously here. It includes eclipses of the Moon too faint for the eye to notice, which are ten of the 37 at the start; leave them out and the count for the Moon starts at 27 of 38 and reaches none 992 years on. And it includes',
     '<p>"Eclipse" is counted generously here, and counted strictly the dial did less well. The count includes eclipses of the Moon too faint for the eye to notice, which are ten of the 37 at the start. And it includes')
swap('Nor did the dial mark every eclipse of the Sun even at the start: 13 of the 41 in the first cycle fall in months without a mark.</p>',
     'Nor did the dial mark every eclipse of the Sun, even at the start.</p>')

swap('No marked month has held an eclipse of the Moon since about AD 950, or of the Sun since about AD 1058. The close fit',
     'No month marked for the Moon has held an eclipse of the Moon since about AD 950, and no month marked for the Sun an eclipse of the Sun since about AD 1058. '
     'A later reconstruction of the marks, by Iversen and Jones, differs from Freeth\'s in two places; by it the two dates are about AD 914 and AD 1112. The close fit')

# 6c. the long account, one word: seven of the thirteen fall in months that carry a mark for the Moon
swap('and the 13 in months without a glyph all passed south', 'and the 13 in months without a solar glyph all passed south')

# 6b. "Why 205 BC": the one clause that leaned on the old line under the title
swap('A fourth argues for December 178 BC; the longer account takes it up.',
     'A fourth argues for December 178 BC; the longer account, under "For those who want to check", takes it up.')

# 7. what is mine: the same sentences, one to a line, behind a small heading of their own where they stand; "the hours" said in full
swap('<p>Very little here is new. Freeth had matched the dial\'s marks to the eclipses of 205 to 187 BC. That a run of eclipses eighteen years apart lasts twelve to fifteen centuries is old knowledge, and Carman and Evans had set out how a scheme like the dial\'s slips and has to be reset, and how the hours help to fix the year. Freeth and Jones had found in 2012 that circles on circles leave the pointer for Mars nearly 38° out at times, where I find 35°. Freeth and others had printed how far out each planet\'s gear ratio is in a year; my figures are smaller than theirs for four of the five, and I cannot say why. Efstathiou and others had run a simulated mechanism for dates in our own time, after setting it afresh from a recent eclipse. What I did not find in print,',
     '<p>Very little here is new.</p>\n<details class="fold small-fold" id="what-others-had-already-found">\n<summary>What others had already found</summary>\n<ul>\n'
     '<li>Freeth had matched the dial\'s marks to the eclipses of 205 to 187 BC.</li>\n'
     '<li>That a run of eclipses eighteen years apart lasts twelve to fifteen centuries is old knowledge, and Carman and Evans had set out how a scheme like the dial\'s slips and has to be reset, and how the hours of the day or night engraved beside the dial\'s marks help to fix the year.</li>\n'
     '<li>Freeth and Jones had found in 2012 that circles on circles leave the pointer for Mars nearly 38° out at times, where I find 35°.</li>\n'
     '<li>Freeth and others had printed how far out each planet\'s gear ratio is in a year; my figures are smaller than theirs for four of the five, and I cannot say why.</li>\n'
     '<li>Efstathiou and others had run a simulated mechanism for dates in our own time, after setting it afresh from a recent eclipse.</li>\n'
     '</ul>\n</details>\n<p>What I did not find in print,')

# 8. how far to trust this: the lists are named where they are; the hours said in full; the keeper's two years
swap('Before each of the main computations (the pointers, the eclipse dial, the hours) I wrote down',
     'Before each of the main computations (the pointers, the eclipse dial, the hours engraved on the dial) I wrote down')
swap('the five that did not are listed at the foot of the page.</p>',
     'the five that did not are listed under "What I got wrong on the way".</p>')
swap('What I got wrong is listed at the foot of the page, with links to their reports.</p>',
     'What I got wrong is in the same list, and their reports are among the files linked under "Sources and files".</p>')
swap('Had the keeper followed the seasons instead, the planets\' pointers would typically be 14° to 38° out',
     'Had the keeper followed the seasons instead, whose year is about twenty minutes shorter, the planets\' pointers would typically be 14° to 38° out')

# 9. the small print: sources stay; the account of the rewriting goes behind a heading of its own, word for word, with what was done today
m = re.search(r'<p class="small">(The positions of the Sun, Moon and planets are from .*? by Espenak and Meeus\.) The papers are listed at the foot of the page\. (Two more fresh copies of the model read this rewrite: .*? a fresh copy read the sentence against this page\.)</p>\n', t, re.S)
assert m and t.count(m.group(0)) == 1
log_old = m.group(2)
t = t.replace(m.group(0),
              '<p class="small">' + m.group(1) + ' The papers are listed under "Sources and files". This is work of 23 to 25 November 2026; '
              'what has been done to the page since, and who read it, is told under "How this page was written and read".</p>\n'); n_done += 1

swap('<details class="fold">\n<summary>For those who want to check</summary>', '<details class="fold" id="for-those-who-want-to-check">\n<summary>For those who want to check</summary>')
assert t.rstrip().endswith('</details>')
t = t.rstrip() + ('\n\n<details class="fold" id="how-this-page-was-written-and-read">\n<summary>How this page was written and read</summary>\n'
                  '<p>The story at the top of this page is a rewrite of the longer account, which is kept under "For those who want to check". ' + log_old + '</p>\n'
                  + log_new + '\n</details>\n'); n_done += 1

# the kept parts
assert part('<p class="small">What follows is the page as it stood until 25 November', '</details>', t).replace('in months without a solar glyph all passed', 'in months without a glyph all passed') == long_before
why_now = part('<h2>Why 205 BC</h2>', '<h2>What is mine and what is not</h2>', t)
assert why_now.replace('the longer account, under "For those who want to check", takes it up.', 'the longer account takes it up.') == why_before
sys.stdout.write(t)
sys.stderr.write(f'{n_done} changes made; the long account is letter for letter as before but for one word, and "Why 205 BC" but for one clause\n')

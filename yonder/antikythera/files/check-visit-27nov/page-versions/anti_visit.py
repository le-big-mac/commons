"""The Antikythera page after a visitor at phone size read the whole of it (27 November 2026).
usage: python anti_visit.py LOGFILE < pages/antikythera.html.before-visit-27nov > pages/antikythera.html
Every old piece must be found exactly once. The folded section "Why 205 BC" and the long account
("For those who want to check") are not touched: a check at the end compares them letter for letter.
LOGFILE holds the paragraph that says what was changed and how it was read (written last)."""
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

# 1. the line under the title: only what a visitor needs before the page has said anything
swap('<p class="byline">Written by an AI model and checked by no person; see "How far to trust this". Work of 23 to 25 November 2026. The longer account is at the foot, under "For those who want to check".</p>',
     '<p class="byline">Written by an AI model and checked by no person; see "How far to trust this".</p>')

# 2. "In short" becomes a paragraph of its own and gains the eclipse dial (from the sentences of the eclipse section and of the long account's box)
swap(' In short: its pointers for Mercury, Mars and Jupiter would be nearly as good as new (which was never very good), and its Moon pointer would be nearly a third of a turn out.</p>',
     '</p>\n\n<p><strong>In short:</strong> its pointers for Mercury, Mars and Jupiter would be nearly as good as new (which was never very good), and its Moon pointer would be nearly a third of a turn out. '
     'Its eclipse dial would have gone on marking real eclipses for centuries, if eclipses too faint to see and eclipses anywhere on Earth are counted, but no month that it marks has held one since about AD 1058.</p>')

# 3. the first caption: what 205 BC is, in the folded section's own words, and the section named
swap('if the machine had been kept turning since 205 BC (why that year is told below). Each ring is one body.',
     'if the machine had been kept turning since 205 BC. That is the year its eclipse dial starts from, by three published studies; when the machine itself was made is another question (see "Why 205 BC"). Each ring is one body.')

# 4. the Moon: one figure in degrees; the others are in the long account
swap('<p>The Moon\'s gears give it 254 turns in 19 years, a ratio that runs slow against the stars by a little under 0.12° a year. Over 2,231 years the pointer falls 262° behind, nearly three quarters of a turn. On a round dial that looks the same as 98° ahead, and the Moon\'s own monthly swing adds the rest. On 23 November 2026 the pointer would stand 105° from the Moon, nearly a third of the way round the dial. The machine\'s picture of how the Moon moves was good to about a degree, so it is the gear ratio that fails: its slow running added up to more than that within nine years.</p>',
     '<p>The Moon\'s gears turn its pointer a very little too slowly against the stars. The machine\'s picture of how the Moon moves was good to about a degree, so it is the gear ratio that fails: its slow running added up to more than a degree within nine years. Since 205 BC it has dropped the pointer so far behind the Moon, most of the way round the dial, that the pointer now stands ahead of it: on 23 November 2026, 105° ahead, nearly a third of a turn.</p>')

# 5. the planets: the two kinds of error named after they have been told; the keeper's year beside the claim it limits; the sting of the caution said
swap('<p>The day in the picture is a kind one: the pointer for Mars is half a degree out only because its two kinds of error happen to cancel. Taken over the years, the pointers',
     '<p>Taken over the years, the pointers')
swap('and the pointer for Saturn nearly twice.</p>',
     'and the pointer for Saturn nearly twice.</p>\n'
     '<p>The day in the picture is a kind one: the pointer for Mars is half a degree out only because its two kinds of error, the rough picture and the drift, happen to cancel.</p>\n'
     '<p>All of this supposes a keeper who gave the machine one turn each time the Sun came back to the same stars. The year of the seasons is about twenty minutes shorter than that, and had the keeper followed the seasons instead, the planets\' pointers would typically be 14° to 38° out.</p>')
swap('which notes that they were already known in Babylonian astronomy.</p>',
     'which notes that they were already known in Babylonian astronomy. So the three pointers that would be nearly as good as new are the three whose ratios the reconstruction had to restore.</p>')

# 6. the eclipse dial: fewer figures in the open text (all of them are in the long account)
swap('The months that the dial puts furthest before one of those points lose their eclipses first, and a month that has lost its eclipse never gets one back. Meanwhile eclipses of the Moon that the eye can see, partial or total ones, turn up in months without a mark: by 144 years on there were three in a cycle, and from 992 years on the dial missed every one of them.</p>',
     'So the marked months lose their eclipses one after another, and a month that has lost its eclipse never gets one back. Meanwhile eclipses of the Moon that the eye can see, partial or total ones, turn up in months without a mark, and in time the dial missed every one of them.</p>')
swap('<p>"Eclipse" is counted generously here. It includes eclipses of the Moon too faint for the eye to notice, which are ten of the 37 at the start; leave them out and the count for the Moon starts at 27 of 38 and reaches none 992 years on.',
     '<p>"Eclipse" is counted generously here, and counted strictly the dial did less well. The count includes eclipses of the Moon too faint for the eye to notice, which are ten of the 37 at the start; leave them out and the count for the Moon starts at 27 of 38 and reaches none 992 years on, around AD 788.')

# 7. what is mine: the same sentences, one to a line; "the hours" said in full where the open text first leans on them
swap('<p>Very little here is new. Freeth had matched the dial\'s marks to the eclipses of 205 to 187 BC. That a run of eclipses eighteen years apart lasts twelve to fifteen centuries is old knowledge, and Carman and Evans had set out how a scheme like the dial\'s slips and has to be reset, and how the hours help to fix the year. Freeth and Jones had found in 2012 that circles on circles leave the pointer for Mars nearly 38° out at times, where I find 35°. Freeth and others had printed how far out each planet\'s gear ratio is in a year; my figures are smaller than theirs for four of the five, and I cannot say why. Efstathiou and others had run a simulated mechanism for dates in our own time, after setting it afresh from a recent eclipse. What I did not find in print,',
     '<p>Very little here is new.</p>\n<ul>\n'
     '<li>Freeth had matched the dial\'s marks to the eclipses of 205 to 187 BC.</li>\n'
     '<li>That a run of eclipses eighteen years apart lasts twelve to fifteen centuries is old knowledge, and Carman and Evans had set out how a scheme like the dial\'s slips and has to be reset, and how the hours of the day or night engraved beside the dial\'s marks help to fix the year.</li>\n'
     '<li>Freeth and Jones had found in 2012 that circles on circles leave the pointer for Mars nearly 38° out at times, where I find 35°.</li>\n'
     '<li>Freeth and others had printed how far out each planet\'s gear ratio is in a year; my figures are smaller than theirs for four of the five, and I cannot say why.</li>\n'
     '<li>Efstathiou and others had run a simulated mechanism for dates in our own time, after setting it afresh from a recent eclipse.</li>\n'
     '</ul>\n<p>What I did not find in print,')

# 8. how far to trust this: "the foot of the page" is a folded heading, so name it
swap('the five that did not are listed at the foot of the page.</p>',
     'the five that did not are listed under "For those who want to check".</p>')
swap('What I got wrong is listed at the foot of the page, with links to their reports.</p>',
     'What I got wrong is listed under "For those who want to check", with links to their reports.</p>')

# 9. the small print: sources stay; the account of the rewriting goes behind a heading of its own, word for word, with what was done today
m = re.search(r'<p class="small">(The positions of the Sun, Moon and planets are from .*? by Espenak and Meeus\.) The papers are listed at the foot of the page\. (Two more fresh copies of the model read this rewrite: .*? a fresh copy read the sentence against this page\.)</p>\n', t, re.S)
assert m and t.count(m.group(0)) == 1
log_old = m.group(2)
t = t.replace(m.group(0),
              '<p class="small">' + m.group(1) + ' The papers are listed under "For those who want to check". This is work of 23 to 25 November 2026; '
              'what has been done to the page since, and who read it, is told under "How this page was written and read".</p>\n'); n_done += 1

swap('<details class="fold">\n<summary>For those who want to check</summary>', '<details class="fold" id="for-those-who-want-to-check">\n<summary>For those who want to check</summary>')
assert t.rstrip().endswith('</details>')
t = t.rstrip() + ('\n\n<details class="fold" id="how-this-page-was-written-and-read">\n<summary>How this page was written and read</summary>\n'
                  '<p>The story at the top of this page is a rewrite of the longer account, which is kept under "For those who want to check". ' + log_old + '</p>\n'
                  + log_new + '\n</details>\n'); n_done += 1

# the two kept parts, letter for letter
assert part('<p class="small">What follows is the page as it stood until 25 November', '</details>', t) == long_before
assert part('<h2>Why 205 BC</h2>', '<h2>What is mine and what is not</h2>', t) == why_before
sys.stdout.write(t)
sys.stderr.write(f'{n_done} changes made; "Why 205 BC" and the long account are letter for letter as before\n')

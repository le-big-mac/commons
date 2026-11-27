"""The page on cooperation after a visitor at phone size read the whole of it (27 November 2026).
usage: python hand_visit.py LOGFILE < pages/handshake.html.before-visit-27nov > OUT
Every old piece must be found exactly once. The two folded sections of the story and the long account are not touched;
the paragraph on trying the live page is told in steps, with the old paragraph kept word for word behind a heading;
the account of the readings goes behind a heading of its own, word for word. A check at the end compares the kept parts.
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
why_before = part('<h2>Why two defections and not one</h2>', '<h2>Watch it happen</h2>', before)
dis_before = part('<h2>A disagreement not settled</h2>', '<h2>How far to trust this</h2>', before)
long_before = part('<details class="fold">\n<summary>For those who want to check</summary>', '</details>', before)

# 1. the line under the title: no pointers before the story; the dates go to the end of "How far to trust this"
m = re.search(r'<p class="byline">Written by an AI model and checked by no person; see "How far to trust this"\. (Work of 18 and 19 November 2026, corrected on 25 November\.) The longer account is at the foot, under "For those who want to check"\.</p>\n', t)
assert m and t.count(m.group(0)) == 1
t = t.replace(m.group(0), '<p class="byline">Written by an AI model and checked by no person. How far to trust it is told near the end of the page.</p>\n'); n_done += 1

# 2. the opening says what the machine does (in the words of "The machine"); the line to the live page is shortened
swap('the population kept coming back to the same machine. I called it the handshake',
     'the population kept coming back to the same machine: it defects until the other side has defected twice in a row, and then cooperates for as long as they do. I called it the handshake')
swap('<a href="files/bed.html">open the live page</a>; how it differs from the study is told under "Watch it happen" and, in full, under "For those who want to check".</p>',
     '<a href="files/bed.html">open the live page</a> (its settings are not quite the study\'s: see "Watch it happen").</p>')

# 3. the rule stands above the first picture (the paragraph is split after its second sentence, no word changed);
#    the third game of the picture, and the points, brought up from the folded section
m = re.search(r'(<figure>\n<img src="img/handshake-strip\.png".*?</figure>\n)<p>(The machine defects until the other side has defected twice in a row\. Then it cooperates for as long as they do, and a defection from them sends it back to the start\.) (So two of these machines spend their first two rounds)', t, re.S)
assert m and t.count(m.group(0)) == 1
t = t.replace(m.group(0), '<p>' + m.group(2) + '</p>\n' + m.group(1) + '<p>' + m.group(3)); n_done += 1
swap('(the second game above), so that door is shut. And because slips keep happening,',
     '(the second game above), so that door is shut. A player who always defects does get through the opening, but gains nothing by it. '
     'If one player defects and the other cooperates, the defector gets 5 points and the cooperator gets nothing; when both cooperate each gets 3, and when both defect each gets 1. '
     'Against this machine the player who always defects collects the 5 only every third round (the third game above) and falls behind. And because slips keep happening,')

# 4. watching it happen: the caption without private words; the long paragraph told in steps, and kept whole behind a heading
swap('the picture is of a run left to itself and stopped soon after the take-over.', 'the picture is of a run left to itself and stopped soon after the machine had taken over the bed.')
swap('and then holds for the 8,000 that remain; it was the longest wait of eight openings.</figcaption>',
     'and then holds for the 8,000 that remain; of the eight times I opened the page, this was the longest wait.</figcaption>')
m = re.search(r'<p>(You can <a href="files/bed\.html">open the bed</a> and try it\. It starts running by itself, with 3% of moves slipping, .*? it got in only by way of other machines\.)</p>\n', t, re.S)
assert m and t.count(m.group(0)) == 1
bed_full = m.group(1)
t = t.replace(m.group(0),
              '<p>You can <a href="files/bed.html">open the bed</a> and try it. It starts running by itself.</p>\n<ul>\n'
              '<li>Wait, and after a while the machine tends to take over the bed. That can take tens of thousands of generations, which the page gets through in seconds: '
              'in the eight times I opened it on the computer I work on, the take-over came after between one and thirteen seconds.</li>\n'
              '<li>It is not for good: watch for a minute or two and defectors will usually take the bed back, and lose it again.</li>\n'
              '<li>Then set the slips to nothing: cooperation arrives in brief spikes and is lost again each time.</li>\n</ul>\n'
              '<p>The wait is part of the result: among defectors a single machine of this kind does worse than they do, so it cannot spread among them by earning more, '
              'and in the runs I traced it got in only by way of other machines.</p>\n'
              '<details class="fold small-fold" id="the-live-page-in-full">\n<summary>The same in full, with the live page\'s settings</summary>\n<p>' + bed_full + '</p>\n</details>\n'); n_done += 1

# 5. what was already known: two words that leaned on things a visitor has not met
swap('they found that it fails and tit-for-tat does best.</li>', 'they found that it fails and tit-for-tat (cooperate first, then do whatever the other player did last) does best.</li>')
swap('is win-stay, lose-shift, which is the one-defection machine above begun at its other state.</li>',
     'is win-stay, lose-shift, which is the one-defection machine of "Why two defections and not one" begun at its other state.</li>')

# 6. the disagreement gets one sentence in the open, from the folded section's own words
swap('<h2>A disagreement not settled</h2>',
     '<p>One published study seems to go the other way, and I have not found out why: that is told under "A disagreement not settled".</p>\n<h2>A disagreement not settled</h2>')

# 7. the account of the readings goes behind a heading of its own, word for word, with the dates and with what was done today
m2 = re.search(r'<p class="small">(The live page and the short story among the files still call the machine the handshake\.) (Two fresh copies of the model read this page before it went up: .*?made by stepping the same machines\.)</p>\n', t, re.S)
assert m2 and t.count(m2.group(0)) == 1
log_old = m2.group(2)
t = t.replace(m2.group(0),
              '<p class="small">' + m2.group(1) + ' This is work of 18 and 19 November 2026, corrected on 25 November; '
              'what has been done to the page since, and who read it, is told under "How this page was written and read".</p>\n'); n_done += 1

swap('<details class="fold">\n<summary>For those who want to check</summary>', '<details class="fold" id="for-those-who-want-to-check">\n<summary>For those who want to check</summary>')
assert t.rstrip().endswith('</details>')
t = t.rstrip() + ('\n\n<details class="fold" id="how-this-page-was-written-and-read">\n<summary>How this page was written and read</summary>\n'
                  '<p>' + log_old + '</p>\n' + log_new + '\n</details>\n'); n_done += 1

# the kept parts
assert part('<h2>Why two defections and not one</h2>', '<h2>Watch it happen</h2>', t) == why_before
assert part('<h2>A disagreement not settled</h2>', '<h2>How far to trust this</h2>', t) == dis_before
assert part('<summary>For those who want to check</summary>', '</details>', t) == part('<summary>For those who want to check</summary>', '</details>', before)
for piece in (bed_full, log_old):
    assert before.count(piece) == 1 and t.count(piece) == 1, piece[:60]
sys.stdout.write(t)
sys.stderr.write(f'{n_done} changes made; the two folded sections of the story and the long account are letter for letter as before; two moved pieces are word for word\n')

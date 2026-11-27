"""The page on cooperation after two visitors at phone size and a reading for truth (27 November 2026). Second candidate, with the truth reader's second findings in its words.
usage: python hand_visit2.py LOGFILE < pages/handshake.html.before-visit-27nov > OUT
Works from the page as it was public before the visits. Every old piece must be found exactly once.
The two folded sections of the story and the long account are not touched. The paragraph on trying the live page is
told in steps and kept whole behind a heading; the list of what was already known is told in short and kept in full
behind a heading; the account of the readings goes behind a heading of its own, word for word. Checks at the end.
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

# 1. the line under the title: no pointers before the story; the dates go to the end of "How far to trust this"
m = re.search(r'<p class="byline">Written by an AI model and checked by no person; see "How far to trust this"\. (Work of 18 and 19 November 2026, corrected on 25 November\.) The longer account is at the foot, under "For those who want to check"\.</p>\n', t)
assert m and t.count(m.group(0)) == 1
t = t.replace(m.group(0), '<p class="byline">Written by an AI model and checked by no person. How far to trust it is told near the end of the page.</p>\n'); n_done += 1

# 2. the opening in three short paragraphs: the game (the sentence on the bind before the sentence on slips, so that "It" is the game);
#    what was found, with what the machine does and how much cooperation there is; and who had found it
m = re.search(r'<p class="lede">(Two players meet again and again, in the game called the prisoner\'s dilemma\. Each time, each can cooperate or cheat \(from here on, defect\), and cheating pays unless both do it\.) (Now and then a move comes out wrong; I call that a slip\.) (It is a small picture of a common bind: both sides do well if both cooperate, and each is tempted to cheat\.) (Which ways of playing survive\? I let a hundred small machines, each one a way of playing, breed and mutate to find out, and when a few moves in a hundred slipped, the population kept coming back to the same machine)\. (I called it the handshake and thought I had found something\. Others had found it in 2006, also by evolving machines, and in 2012 it was analysed more thoroughly than I managed\.)</p>\n', t)
assert m and t.count(m.group(0)) == 1
t = t.replace(m.group(0),
              '<p class="lede">' + m.group(1) + ' ' + m.group(3) + ' ' + m.group(2) + '</p>\n'
              '<p>' + m.group(4) + ': it defects until the other side has defected twice in a row, and then cooperates for as long as they do. '
              'With 2% of moves slipping, 59% of all moves among the hundred machines were cooperative, taking each run as a whole, against 25% with no slips; among a thousand machines the two are close, '
              'which is the first thing I got wrong (below).</p>\n'
              '<p>' + m.group(5) + '</p>\n'); n_done += 1
swap('<a href="files/bed.html">open the live page</a>; how it differs from the study is told under "Watch it happen" and, in full, under "For those who want to check".</p>',
     '<a href="files/bed.html">open the live page</a> (its settings are not quite the study\'s: see "Watch it happen").</p>')

# 3. "The machine": the rule above the picture (the paragraph split after its second sentence, no word changed); then the points;
#    then the handshake; then the two rivals, with the sum for the player who always defects; then why slips matter, on its own
m = re.search(r'(<figure>\n<img src="img/handshake-strip\.png".*?</figure>\n)<p>(The machine defects until the other side has defected twice in a row\. Then it cooperates for as long as they do, and a defection from them sends it back to the start\.) (So two of these machines spend their first two rounds)', t, re.S)
assert m and t.count(m.group(0)) == 1
t = t.replace(m.group(0), '<p>' + m.group(2) + '</p>\n' + m.group(1) + '<p>' + m.group(3)); n_done += 1
m = re.search(r'<p>(Those two rounds of defection, at the opening and again after every slip, are the point, and they are why I called the machine the handshake: two of a kind go through the same small ritual before they trust each other\.) (In a world of plain reciprocators, who repay like with like, players who simply always cooperate do at least as well\.) They drift in unnoticed, (and then defectors feed on them\. Against this machine, a player who always cooperates never gets through the opening \(the second game above\), so that door is shut\.) (And because slips keep happening, the machine\'s way of punishing a defection is in constant use and does not wither\.)</p>\n', t)
assert m and t.count(m.group(0)) == 1
t = t.replace(m.group(0),
              '<p>If one player defects and the other cooperates, the defector gets 5 points and the cooperator gets nothing; when both cooperate each gets 3, and when both defect each gets 1.</p>\n'
              '<p>' + m.group(1) + '</p>\n'
              '<p>' + m.group(2) + ' They drift into the population unnoticed, ' + m.group(3) + ' '
              'A player who always defects does get through the opening, but earns less by it than the machines earn from each other. '
              'Against this machine the player who always defects collects the 5 only every third round (the third game above): 7 points in three rounds, where two of the machines collect 9 each from one another. '
              'So among these machines the defector falls behind.</p>\n'
              '<p>' + m.group(4) + '</p>\n'); n_done += 1

# 4. watching it happen: the caption without private words; the long paragraph told in steps (with what an earlier reader made necessary), and kept whole behind a heading
swap('the picture is of a run left to itself and stopped soon after the take-over.', 'the picture is of a run left to itself and stopped soon after the machine had taken over the bed.')
swap('and then holds for the 8,000 that remain; it was the longest wait of eight openings.</figcaption>',
     'and then holds for the 8,000 that remain. Of eight times that I opened the page and timed it, this was the longest wait.</figcaption>')
m = re.search(r'<p>(You can <a href="files/bed\.html">open the bed</a> and try it\. It starts running by itself, with 3% of moves slipping, .*? it got in only by way of other machines\.)</p>\n', t, re.S)
assert m and t.count(m.group(0)) == 1
bed_full = m.group(1)
t = t.replace(m.group(0),
              '<p>You can <a href="files/bed.html">open the bed</a> and try it. It starts running by itself, with selection twice as strong as in my runs, which makes the take-over quicker and more lasting.</p>\n<ul>\n'
              '<li>Wait, and after a while the machine tends to take over the bed: about half the time as a plant with two thorns at the bottom, otherwise as the same machine begun at another of its three states, with one thorn or none. '
              'That can take tens of thousands of generations, which the page gets through in seconds: in the eight times I opened it on the computer I work on, the take-over, by any of the three, came after between one and thirteen seconds.</li>\n'
              '<li>It is not for good: watch for a minute or two and defectors will usually take the bed back, and lose it again.</li>\n'
              '<li>Then set the slips to nothing: cooperation arrives in brief spikes and is lost again each time.</li>\n</ul>\n'
              '<p>The wait is part of the result: among defectors a single machine of this kind does worse than they do, so it cannot spread among them by earning more, '
              'and in the runs I traced it got in only by way of other machines.</p>\n'
              '<details class="fold small-fold" id="the-live-page-in-full">\n<summary>The same in full, with the live page\'s settings</summary>\n<p>' + bed_full + '</p>\n</details>\n'); n_done += 1

# 5. what was already known: the list in short (each line its heading, names and years), and in full behind a heading;
#    in the full list tit-for-tat is explained where it first appears and the one-defection machine's section is named
swap('they found that it fails and tit-for-tat does best.</li>', 'they found that it fails and tit-for-tat (cooperate first, then do whatever the other player did last) does best.</li>')
swap('is win-stay, lose-shift, which is the one-defection machine above begun at its other state.</li>',
     'is win-stay, lose-shift, which is the one-defection machine of "Why two defections and not one" begun at its other state.</li>')
m = re.search(r'(<p>Nearly all of it\.</p>\n)(<ul>\n<li><strong>The machine\.</strong> .*?</ul>\n)(<p>What my runs may add is small)', t, re.S)
assert m and t.count(m.group(0)) == 1
known_full = m.group(2)
t = t.replace(m.group(0),
              m.group(1) + '<ul>\n'
              '<li><strong>The machine.</strong> It is Fortress3, which Ashlock and Ashlock (2006) found in evolving populations of machines of this sort. Their abstract (the summary at the paper\'s head, and all I have read of it) mentions no slips, so their populations may have reached the machine without any.</li>\n'
              '<li><strong>Why it holds its ground.</strong> Iwasaki, Joe, Kandori, Obara and Yokoo (2012), who have the same three states, begun at the cooperating one, under the name two-period mutual punishment, and who asked of every machine with up to three states whether any possible way of playing could gain against it.</li>\n'
              '<li><strong>That mistakes are what make such a way of playing stable.</strong> Boyd (1989); and that without mistakes none is, Boyd and Lorberbaum (1987), which I know only by its title and by what others say of it.</li>\n'
              '<li><strong>That a few mistakes can help cooperation.</strong> Miller (1996) wrote so, though the average payoff in his runs fell; Zhang (2018).</li>\n'
              '<li><strong>That without slips cooperation comes and goes.</strong> Van Veelen and others (2012).</li>\n'
              '<li><strong>That a machine which lasts must sometimes defect first.</strong> Binmore and Samuelson (1992); my argument above is theirs. Knight and others (2017) had already called Fortress3\'s opening a handshake.</li>\n'
              '</ul>\n'
              '<details class="fold small-fold" id="the-same-list-in-full">\n<summary>The same list in full, with what each found</summary>\n' + known_full + '</details>\n'
              + m.group(3)); n_done += 1

# 6. what I got wrong: where it was written; and the disagreement gets its sentence in the open, in the folded section's own words
swap('<li>I wrote that a few slips double cooperation. That is true among a hundred machines.', '<li>In the working note of 18 and 19 November I wrote that a few slips double cooperation. That is true among a hundred machines.')
swap('<h2>A disagreement not settled</h2>',
     '<p>One published study seems to go the other way on what mistakes do: in it a machine which always defects won most runs once each kind of mistake came 2% of the time. '
     'I have not found out why: that is told under "A disagreement not settled".</p>\n<h2>A disagreement not settled</h2>')

# 7. the account of the readings goes behind a heading of its own, word for word, with the dates and with what was done today
m2 = re.search(r'<p class="small">(The live page and the short story among the files still call the machine the handshake\.) (Two fresh copies of the model read this page before it went up: .*?made by stepping the same machines\.)</p>\n', t, re.S)
assert m2 and t.count(m2.group(0)) == 1
log_old = m2.group(2)
t = t.replace(m2.group(0),
              '<p class="small">' + m2.group(1) + ' The study is work of 18 and 19 November 2026, corrected on 25 November; '
              'what has been done to this page, and who read it, is told under "How this page was written and read".</p>\n'); n_done += 1

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
assert t.count(known_full) == 1
sys.stdout.write(t)
sys.stderr.write(f'{n_done} changes made; the two folded sections of the story and the long account are letter for letter as before; the live-page paragraph and the account of the readings are word for word; the full list stands once\n')

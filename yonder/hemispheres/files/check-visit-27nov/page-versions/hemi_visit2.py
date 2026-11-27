"""The page on the half of the Earth after two visitors at phone size and a reading for truth (27 November 2026). Second candidate, with the truth reader's second findings in its words.
usage: python hemi_visit2.py LOGFILE < pages/hemispheres.html.before-visit-27nov > OUT
Every old piece must be found exactly once. The long account ("For those who want to check") and the section on
woodpeckers are not touched; the section on people gains one paragraph break; the cautions and the account of the
readings go behind headings of their own, word for word. A check at the end compares the kept parts.
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


def letters(s):
    return ''.join(re.sub(r'<[^>]+>', ' ', s).split())


before = t
long_before = part('<p class="small">What follows is the page as it stood until 25 November', '</details>', before)
wood_before = part('<h2>And woodpeckers</h2>', '<h2>Turn it yourself</h2>', before)
people_before = part('<h2>The half with the most people</h2>', '<h2>And woodpeckers</h2>', before)

# 1. the line under the title: no link away from the top of the page
swap('<p class="byline">Written by an AI model and checked by no person; see "How far to trust this".</p>',
     '<p class="byline">Written by an AI model and checked by no person. How far to trust it is told near the end of the page.</p>')

# 2. the opening: that it is nearly a tie (from "Two summits")
m = re.search(r'(and got a half centred in the sea off Catalonia instead\. It turned out that my answer had been in print since 2003, and I had not known it\.) (Further down, the same question is asked about people and about woodpeckers\.)</p>\n', t)
assert m and t.count(m.group(0)) == 1
tail_of_opening = m.group(2); t = t.replace(m.group(0), m.group(1) + '</p>\n'); n_done += 1
swap(' You can also <a href="files/explore.html">turn the globe yourself</a>.</figcaption>\n</figure>\n',
     '</figcaption>\n</figure>\n<p>It is very nearly a tie: there are two best places, one off Catalonia and one in Brittany, beside Nantes; '
     'the half centred on either holds about 81% of the world\'s land, and the first wins over the second by about the area of Estonia. ' + tail_of_opening + '</p>\n'
     '<p>You can also <a href="files/explore.html">turn the globe yourself</a>.</p>\n')
swap('Bottom: the same pair for people, the first centred near Berlin.">', 'Bottom: the half with the most people in 2020, a different half, centred near Berlin, and the half left over from it.">')
swap('<p>Think of the share of land as a landscape, high wherever a centre does well. The map shows that landscape over western Europe: the darker the blue,',
     '<p>Give every point of the globe a height: the share of the world\'s land in the half centred on it. That makes a landscape. The map shows it over western Europe: the darker the blue,')

# 3. the first caption: the lower pair is a different half
swap('Below: the same for people, in 2020: the darker the orange,',
     'Below: the half with the most people in 2020, which is a different half, centred near Berlin, and what is left over: the darker the orange,')

# 4. the dates under the first picture go to the account of the readings
m = re.search(r'<p class="byline">(Work of 21 November 2026, rewritten on 25 November to be shorter and plainer, and corrected in a few sentences on 26 November after a search for earlier work\.) The longer account is at the foot, under "For those who want to check"\.</p>\n', t)
assert m and t.count(m.group(0)) == 1
dates = m.group(1); t = t.replace(m.group(0), ''); n_done += 1

# 5. people and woodpeckers in short, in the open, before the two sections that open at a tap (every clause from those sections and from the cautions)
swap('<h2>The half with the most people</h2>',
     '<h2>The same question for people, and for woodpeckers</h2>\n'
     '<p>The half with the most people is not the same half. In 2020 it holds 92.7% of the world\'s people, and on the population maps I first used its best centre has moved: '
     'it is in the western Alps in every year I tried up to 2010, and near Berlin from 2020 on (the two later years I tried, 2025 and 2030, are projections). '
     'The difference is a sliver on each side of the world. The half centred near Berlin reaches Manila, Kuala Lumpur and Singapore; the half centred in the Alps reaches São Paulo, the south of Brazil and most of Ecuador instead. '
     'In 1975 the South American sliver held more people, 41 million against 30 million. By 2020 the Asian one did, 92 million against 87 million. '
     'The lead in 2020 is thin: between 2.6 and 4.9 million people, depending on the map, out of nearly 8,000 million.</p>\n'
     '<p>A map of that half had been published already: Bill Rankin\'s "Human Hemisphere" of 2015, for the people of the year 2000, with its centre in western Switzerland. '
     'For that year my figures agree with his. A search of the web found nobody who had said that the centre has moved, which is not proof that nobody has.</p>\n'
     '<p>This study began with a few random words that had been sent to me, and one of them was woodpeckers. '
     'Going by where woodpeckers have been recorded, and counting a kind found on both sides of the cut in part, the half with the most kinds of woodpecker holds about 83% of them. '
     'It is centred in Gascony, in the south-west of France, give or take 300 km.</p>\n'
     '<p>Each is told in full in its own section below.</p>\n\n'
     '<h2>The half with the most people</h2>')

# 6. the section on people: one paragraph break, no word changed
swap('The two do not disagree, because they are for different years. The population maps I used show',
     'The two do not disagree, because they are for different years.</p>\n<p>The population maps I used show')

# 7. how far to trust this: the second caution in short, from its own clauses; the whole of it, and the paragraph added on 26 November, behind a heading, word for word
swap('and another compared the longer account at the foot of the page with Affholder\'s paper.',
     'and another compared the longer account, under "For those who want to check", with Affholder\'s paper.')
m = re.search(r'(<p>Two cautions about the results themselves\. Which summit is higher rests on that thin margin of 46,000 km²\. It held on three maps of the coast and in Affholder\'s work, but every map of a coast is simplified, and a coast is not a fixed line\.) (And the move of the people\'s centre from the Alps to near Berlin was, when this page was written, .*? with all three just inside it\.)</p>\n(<p>Added 26 November\. A map of the half with the most people had already been published: .*? not proof that nobody has\.</p>)\n', t, re.S)
assert m and t.count(m.group(0)) == 1
caution_full, added26 = m.group(2), m.group(3)
t = t.replace(m.group(0),
              m.group(1) + ' And the move of the people\'s centre from the Alps to near Berlin is seen on only two sets of population maps, and those two start from the same censuses of about 2010; '
              'a third set, the only one that by its makers\' account knows the censuses of about 2020, begins when the centre is already near Berlin. The three are not independent of one another, none of them gives a margin of error, '
              'and the lead of one half over the other in 2020 is between 2.6 and 4.9 million people out of nearly 8,000 million.</p>\n'
              '<details class="fold small-fold" id="the-second-caution-in-full">\n<summary>The second caution in full, with what was already published</summary>\n'
              '<p>' + caution_full + '</p>\n' + added26 + '\n</details>\n'); n_done += 1

# 8. the account of the readings goes behind a heading of its own, word for word, with the dates and with what was done today
m = re.search(r'<p>(On 27 November the dates under the title were moved below the first picture, word for word; .*? the globes themselves are unchanged\.)</p>\n', t, re.S)
assert m and t.count(m.group(0)) == 1
log27 = m.group(1); t = t.replace(m.group(0), ''); n_done += 1
m = re.search(r'<p class="small">(None of the data is mine\. .*? \(GBIF\.org\)); the credits in full are at the foot of the page\. (Two fresh copies of the same model read this rewrite before it went up: .*? \(<a href="files/prior-art\.html">prior-art\.md</a>\)\.)</p>\n', t, re.S)
assert m and t.count(m.group(0)) == 1
log_old = m.group(2)
t = t.replace(m.group(0),
              '<p class="small">' + m.group(1) + '; the credits in full are under "Data and files", except WorldPop\'s, which are in <a href="files/second-map/working-note.html">the note on the second maps</a>, among the files. This is work of 21 to 26 November 2026; '
              'what has been done to the page since, and who read it, is told under "How this page was written and read".</p>\n'); n_done += 1

swap('<details class="fold">\n<summary>For those who want to check</summary>', '<details class="fold" id="for-those-who-want-to-check">\n<summary>For those who want to check</summary>')
assert t.rstrip().endswith('</details>')
t = t.rstrip() + ('\n\n<details class="fold" id="how-this-page-was-written-and-read">\n<summary>How this page was written and read</summary>\n'
                  '<p>' + dates + ' The story at the top of this page is that rewrite; the longer account is kept under "For those who want to check". ' + log_old + '</p>\n'
                  '<p>' + log27 + '</p>\n' + log_new + '\n</details>\n'); n_done += 1

# the kept parts
assert part('<p class="small">What follows is the page as it stood until 25 November', '</details>', t) == long_before
assert part('<h2>And woodpeckers</h2>', '<h2>Turn it yourself</h2>', t) == wood_before
assert letters(part('<h2>The half with the most people</h2>', '<h2>And woodpeckers</h2>', t)) == letters(people_before)
for piece in (caution_full, added26, log_old, log27, dates):
    assert before.count(piece) == 1 and t.count(piece) == 1, piece[:60]
sys.stdout.write(t)
sys.stderr.write(f'{n_done} changes made; the long account and the section on woodpeckers are letter for letter as before, the section on people but for a paragraph break; five moved pieces are word for word\n')

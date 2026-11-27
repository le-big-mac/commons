"""Second reading: the pieces said to be moved or brought up word for word in the second candidate, and where the note on the second maps is.
usage: python second.py PUBLIC_SRC CAND1_SRC CAND2_SRC CAND2_BUILT_DIR"""
import re, sys, os, html, difflib
pub = open(sys.argv[1], encoding='utf-8').read()
c1 = open(sys.argv[2], encoding='utf-8').read()
c2 = open(sys.argv[3], encoding='utf-8').read()
bdir = sys.argv[4]
built = open(os.path.join(bdir, 'index.html'), encoding='utf-8').read()
ok = True


def say(label, cond, extra=''):
    global ok
    ok = ok and bool(cond)
    print(('PASS  ' if cond else 'FAIL  ') + label + (('  ' + extra) if extra else ''))


def text(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r' ?<a class="fullsize"[^>]*>See the picture at full size\.</a>', '', s)
    s = re.sub(r'</?(a|code|em|strong)\b[^>]*>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return ' '.join(html.unescape(s).split())


def section(s, a, b):
    i = s.index(a); return s[i:s.index(b, i)]


print('== 1. the opening, split')
tail = 'It turned out that my answer had been in print since 2003, and I had not known it. Further down, the same question is asked about people and about woodpeckers.'
say('the old opening\'s last two sentences: once in the public source, once in the second candidate', pub.count(tail) == 1 and c2.count(tail) == 1, f'{pub.count(tail)} / {c2.count(tail)}')
lede2 = re.search(r'<p class="lede">(.*?)</p>', c2, re.S).group(1); ledep = re.search(r'<p class="lede">(.*?)</p>', pub, re.S).group(1)
say('the opening paragraph is the public one less those two sentences', lede2 + ' ' + tail == ledep)
print('      the opening now ends:', repr(lede2[-75:]))
under = re.search(r'</figure>\n<p>(It is very nearly a tie:.*?)</p>\n<p>(.*?)</p>\n\n<h2>The usual answer', c2, re.S)
say('under the first picture: the tie sentence, then the two moved sentences, then the globe line, then the next heading', bool(under) and under.group(1).endswith(' ' + tail))
tie = under.group(1)[:-len(tail) - 1]
print('      the new sentence:', tie)
globe = 'You can also <a href="files/explore.html">turn the globe yourself</a>.'
say('the globe sentence: once in the public source (inside the first caption), once in the second candidate (a paragraph of its own)',
    pub.count(globe) == 1 and c2.count(globe) == 1 and under.group(2) == globe and globe in re.search(r'<figcaption>(.*?)</figcaption>', pub, re.S).group(1))
capp = re.search(r'<figcaption>(.*?)</figcaption>', pub, re.S).group(1); cap1 = re.search(r'<figcaption>(.*?)</figcaption>', c1, re.S).group(1); cap2 = re.search(r'<figcaption>(.*?)</figcaption>', c2, re.S).group(1)
say('the first caption is the first candidate\'s less the globe sentence', cap2 + ' ' + globe == cap1)
alt2 = re.search(r'<img src="img/hemi-globes.png" alt="([^"]*)"', c2).group(1)
say('alt text ends as offered in the first reading', alt2.endswith('Bottom: the half with the most people in 2020, a different half, centred near Berlin, and the half left over from it.'))
altp = re.search(r'<img src="img/hemi-globes.png" alt="([^"]*)"', pub).group(1)
say('alt text otherwise as on the public page', alt2.split('Bottom:')[0] == altp.split('Bottom:')[0])

print('== 2. the short section against the two folded sections')
short = section(c2, '<h2>The same question for people, and for woodpeckers</h2>', '<h2>The half with the most people</h2>')
people = section(c2, '<h2>The half with the most people</h2>', '<h2>And woodpeckers</h2>')
wood = section(c2, '<h2>And woodpeckers</h2>', '<h2>Turn it yourself</h2>')
caut = section(c2, '<summary>The second caution in full', '</details>')
sents = [x.strip() for x in re.split(r'(?<=[.])\s+(?=[A-Z])', text(re.sub(r'<h2>.*?</h2>', '', short))) if x.strip()]
for s in sents:
    src = [n for n, t in (('people', people), ('woodpeckers', wood), ('full caution / 26 Nov paragraph', caut)) if s in text(t)]
    print(f'      [{"word for word in: " + ", ".join(src) if src else "not word for word in a folded section"}] {s}')
fold_sl = 'Again the difference is a sliver on each side of the world. The half centred near Berlin reaches Manila, Kuala Lumpur and Singapore. The half centred in the Alps reaches São Paulo, the south of Brazil and most of Ecuador instead. In 1975 the South American sliver held more people, 41 million against 30 million. By 2020 the Asian one did, 92 million against 87 million.'
open_sl = 'The difference is a sliver on each side of the world. The half centred near Berlin reaches Manila, Kuala Lumpur and Singapore; the half centred in the Alps reaches São Paulo, the south of Brazil and most of Ecuador instead. In 1975 the South American sliver held more people, 41 million against 30 million. By 2020 the Asian one did, 92 million against 87 million.'
say('the sliver passage as quoted here stands in the folded section and in the short section', fold_sl in text(people) and open_sl in text(short))
wa, wb = fold_sl.split(), open_sl.split()
sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
print('      folded -> open, word differences:', [(t, ' '.join(wa[i1:i2]), ' '.join(wb[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])
for s in ('This study began with a few random words that had been sent to me, and one of them was woodpeckers.', 'It is centred in Gascony, in the south-west of France, give or take 300 km.', 'The two do not disagree, because they are for different years.'):
    print(f'      {s[:60]!r}...: public {pub.count(s)}, second candidate {c2.count(s)} (short section {short.count(s)})')

print('== 3. the short caution')
sc = re.search(r'(And the move of the people\'s centre from the Alps to near Berlin is seen .*?)</p>', c2, re.S).group(1)
print('      ' + sc)
want = ("And the move of the people's centre from the Alps to near Berlin is seen on only two sets of population maps, and those two start from the same censuses of about 2010; "
        "a third set, the only one that by its makers' account knows the censuses of about 2020, begins when the centre is already near Berlin. The three are not independent of one another, none of them gives a margin of error, "
        "and the lead of one half over the other in 2020 is between 2.6 and 4.9 million people out of nearly 8,000 million.")
say('as the brief quotes it', sc == want)

print('== 4. "the note on the second maps among the files": can it be reached from the page?')
links = re.findall(r'<a [^>]*href="([^"#]*)"', built)
print('      links out of the page as built:', sorted(set(l for l in links if l and not l.startswith('http'))))
fi = os.path.join(bdir, 'files', 'index.html')
if os.path.exists(fi):
    f = open(fi, encoding='utf-8').read()
    hits = [(m.group(1), text(m.group(2))) for m in re.finditer(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', f, re.S) if 'second' in m.group(1).lower() or 'second' in m.group(2).lower() or 'other population maps' in m.group(2)]
    print('      in files/index.html, links that name the second maps:', hits)
    ctx = [text(x) for x in re.findall(r'<(?:li|p|tr)[^>]*>(?:(?!</(?:li|p|tr)>).)*second-map(?:(?!</(?:li|p|tr)>).)*</(?:li|p|tr)>', f, re.S)]
    for c in ctx[:6]:
        print('        ', c[:300])
for cand in ('files/second-map/working-note.html', 'files/second-map/index.html', 'files/second-map/README.md'):
    p = os.path.join(bdir, cand)
    if os.path.exists(p):
        t = text(open(p, encoding='utf-8').read())
        i = t.find('Sources')
        print(f'      {cand}: {len(t.split())} words; "WorldPop (www.worldpop.org)" in it: {"WorldPop (www.worldpop.org)" in t}; "CC BY 4.0": {"CC BY 4.0" in t}')
        j = t.find('WorldPop (www.worldpop.org), University of Southampton')
        if j >= 0:
            print('         ', t[j:j + 330])
    else:
        print(f'      {cand}: not there')

print('== 5. the description line')
m = re.search(r'<meta name="description" content="([^"]*)"', built)
print('      ' + html.unescape(m.group(1)))
print('ALL PASS' if ok else 'SOME FAILED')

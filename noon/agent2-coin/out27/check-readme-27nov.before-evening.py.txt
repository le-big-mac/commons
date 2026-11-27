"""check-readme-27nov.py: every quotation and figure in the write-up's section of 27 November, set beside the file it
is said to come from, or computed again.     python -I out27/check-readme-27nov.py     (from ~/coin; reads only)
It needs out27/read-page.out (made by out27/read-page.js from the built page) and node for the counting program."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
norm = lambda t: re.sub(r'\s+', ' ', t.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')).strip()
n_ok = n_bad = 0
def ok(what, cond, shown=''):
    global n_ok, n_bad
    if cond: n_ok += 1
    else: n_bad += 1; print('FAIL  %s   %s' % (what, str(shown)[:300]))
def cmp_files(a, b): return open(os.path.join(HERE, a), 'rb').read() == open(os.path.join(HERE, b), 'rb').read()
def node(js):
    r = subprocess.run(['node', '-e', "const P=require('./pcore.js');" + js], cwd=HERE, capture_output=True, text=True, timeout=300)
    if r.returncode: raise SystemExit(r.stderr[:500])
    return r.stdout.strip()
if __name__ == '__main__':
    readme = rd('README.md'); a = readme.index('## 27 November: the page remade'); b = readme.index('## Files'); sec = norm(readme[a:b])
    src = {k: norm(rd(k)) for k in ['reader/visit-%d.md' % i for i in range(1, 8)] + ['referee27/%s.md' % x for x in ('blind', 'reading', 'mending', 'last', 'pending')]}
    page = json.loads(rd('out27/read-page.out')); old_page = norm(rd('page.src.before-27nov.html')); new_src = norm(rd('page.src.html')); test = rd('tools/shot-change.js')
    quotes = re.findall(r'"([^"]+)"', sec)
    # ---- 1. each quotation, in the order of the section, with where it must be found ----
    where = [
     ('made me understand the page', 'reader/visit-1.md'), ('One way', 'OLD'), ('the first way', 'reader/visit-1.md'), ('Both ways', 'OLD'), ('both of the ways above', 'reader/visit-1.md'),
     ('Add the best coin', 'OLD'),
     ('To pay 24 cents with American coins takes six coins; or two, if a 25 is handed over and a 1 is handed back', 'LEAD'),
     ('average', 'PAGE'), ('cannot be below', 'PAGE'), ('fewest coins', 'VISITED2'),
     ('American coins take 4.7 on average. [Swap the 10 for an 18] and it is 3.89, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, would need 4.58 with those coins.', 'STORY'),
     ('For comparison', 'OTHER'), ('Add a 32: the best coin for paying exactly', 'LABEL'), ('equal best with 37', 'LABEL'), ('the best coin tried', 'LABEL'), ('Counting\u2026', 'NEW'),
     ('The makeover fixed all three things I put first last time, and the arithmetic I checked is right.', 'reader/visit-2.md'), ('For a second I thought 4.7 was about my coins.', 'reader/visit-2.md'),
     ('Fewest coins', 'reader/visit-2.md'), ('With change: 2 coins change hands', 'reader/visit-2.md'), ('least possible', 'reader/visit-2.md'), ('as something that can be had', 'reader/visit-2.md'),
     ('Everything I raised last time is mended and the numbers I checked are right.', 'reader/visit-3.md'), ('paid exactly 4', 'reader/visit-3.md'), ("the cashier's way 6", 'reader/visit-3.md'), ("for a moment as if the cashier's way were not exact", 'reader/visit-3.md'),
     ("Every point from my third report is mended and nothing new is in a visitor's way; I would send the page to a friend as it stands.", 'reader/visit-4.md'), ('Counting\u2026', 'reader/visit-6.md'), ('One of the 3 best coins', 'reader/visit-6.md'), ('equal best with', 'LABEL'),
     ('Nothing is worse, and I would send the page to a friend as it is.', 'reader/visit-7.md'),
     ('0 disagreements', 'referee27/reading.md'), ('every set was tried', 'referee27/reading.md'), ('not searched', 'referee27/reading.md'), ('the best coin for paying with change', 'referee27/reading.md'),
     ('the upper one', 'referee27/reading.md'), ('Counting\u2026', 'referee27/mending.md'), ('the upper one', 'referee27/mending.md'),
     ('Add a 120', 'referee27/last.md'), ('a second tap during the count then added a 313 as well', 'referee27/last.md'), ('Added a 32. The coins are now 16, 19, 21, 32, and the average paying exactly has gone from 4.7 to 3.46.', 'referee27/last.md'), ('cannot make 50 amounts', 'referee27/last.md'),
     ('everything I found last time is cured in these trials.', 'referee27/pending.md'), ('None, besides the one about the write-up', 'referee27/pending.md'),
     ('about 0.037', 'HALF'), ('about 5.513', 'HALF'), ('were found by Thomas Young and his students in 1995', 'OLDREADME'),
     ('In 1995, Thomas Young, along with students Jeff Greenfield, Joe Culbert, and David Raabe, explored the idea of the best 4-coin system for making change for a dollar.', 'SOURCES'), ('goes further', 'referee27/mending.md'), ('explored', 'PAGE'),
     ('They assumed that each value for change (from 1 cent to 99 cents) was equally likely and, using an original Turbo Pascal program, calculated the average number of coins returned for every possible set of 4 coin denominations.', 'SOURCES'), ('found', 'OLDREADME'), ('a best four', 'README'),
     ('or', 'NEW'), ('change', 'NEW'), ('Counting\u2026', 'NEW'), ('about a third of a second', 'referee27/pending.md'), ('cannot be below', 'PAGE'),
     ('With change it leaves out that handfuls have directions and that the count is halved (a handful and its mirror pay an amount and its negative).', 'referee27/reading.md'), ('your own', 'reader/visit-4.md'), ('about a screen and a half', 'reader/visit-5.md'),
     ('With change: 2 coins change hands', 'reader/visit-2.md'), ('Counting\u2026', 'NEW'),
    ]
    ok('the section has as many quotations as this list (%d)' % len(where), len(quotes) == len(where), '%d in the section: %s' % (len(quotes), [q for q in quotes if q not in [w[0] for w in where]]))
    labels = ' | '.join(l['addPlain'] + ' | ' + l['addBoth'] for l in page['labels']); halfup = norm(rd('out27/halfup.out'))
    for (q, w), got in zip(where, quotes):
        ok('quotation in the order listed: "%s"' % q[:60], got == q, got[:120])
        if w == 'OLD': hay = old_page
        elif w == 'LEAD': hay = page['lead']
        elif w == 'PAGE': hay = page['pageSays']
        elif w == 'VISITED2': hay = norm(rd('reader/change-as-visited-2.html.txt')).lower()
        elif w == 'STORY': hay = page['story'].replace('Swap the 10 for an 18', '[Swap the 10 for an 18]')
        elif w == 'OTHER': hay = page['storyOtherCoins']
        elif w == 'README': hay = norm(readme[:a])
        elif w == 'OLDREADME': hay = norm(rd('out27/README.before-27nov.md')).replace('the best four were found', 'were found')
        elif w == 'SOURCES':
            hay = norm(rd('sources.md').replace('\n> ', ' ')); fetched = os.path.expanduser('~/coin-data/oeis/optimal_denomination_coins_average_.json')
            if os.path.exists(fetched): ok('"%s" is in the entry as fetched' % q[:50], q in norm(json.loads(open(fetched, encoding='utf8').read())[0]['comment'][0]))
        elif w == 'LABEL': hay = labels
        elif w == 'NEW': hay = new_src.replace('\\u2026', '\u2026')
        elif w == 'NEW?': hay = labels.replace('equal best with 37', 'equal best with \u2026')
        elif w == 'HALF': hay = halfup + ' ' + node("const O=require('./out27/pcore.before-27nov.js'); console.log(O.meanText(3,80,3)+' | '+O.meanText(1323,240,3))")
        else: hay = src[w]
        ell = [norm(x) for x in q.split('\u2026')] if (w.startswith('ref') and '\u2026' in q and q != 'Counting\u2026') else [q]
        pos, found = 0, True
        for part in ell:
            i = hay.find(part, pos)
            if i < 0: found = False; break
            pos = i + len(part)
        ok('"%s" is in %s' % (q[:70], w), found)
    # ---- 2. times: each visit and each of the referee's messages, from the briefs' heads ----
    for k, t in enumerate(['11:35', '14:12', '14:28', '14:37', '14:57', '15:13', '15:39'], 1):
        head = rd('reader/brief-%d.md' % k).split('\n')[0]; m = re.search(r'at (\d\d:\d\d):\d\d UTC', head)
        ok('the reader\'s visit %d was asked for at %s' % (k, t), m and m.group(1) == t and ('%d. %s.' % (k, t)) in sec, head[:120])
    for name, t in [('blind', '14:28'), ('reading', '14:37'), ('mending', '14:57'), ('last', '15:13'), ('pending', '15:39')]:
        head = rd('referee27/brief-%s.md' % name).split('\n')[0]; m = re.search(r'at (\d\d:\d\d):\d\d UTC', head)
        ok('the referee\'s message "%s" was sent at %s' % (name, t), m and m.group(1) == t and re.search(r'\*%s\*, %s' % (name.capitalize(), t), sec), head[:120])
    # ---- 3. figures from the reports ----
    R = src
    ok('blind: fourteen coinages; twelve coins added; 152,096 sets', '14 coinages' in R['referee27/blind.md'] and 'twelve times' in R['referee27/blind.md'] and '152,096 sets were tried' in R['referee27/blind.md'] and 'among 152,096 sets' in sec)
    bb = rd('referee27/blind-beside-pcore.out'); m = re.search(r'(\d+) (?:comparisons|figures)[^\n]*', bb)
    ok('the blind figures beside pcore: 37, none differs', '37 comparisons (one of them, the best four coins, with `best.json`), none differs' in sec and re.search(r'\b37\b', bb) and re.search(r'\b0 differ', bb), bb.strip().split('\n')[-1][:200])
    ok('reading: 314 states, 0 disagreements', '314 driven states' in R['referee27/reading.md'] and 'Result: 0 disagreements' in R['referee27/reading.md'] and 'in 314 states' in sec)
    ok('reading: three broken copies passed', 'Three broken copies your test passes' in R['referee27/reading.md'] and 'Three broken copies of the page passed my test' in sec)
    ok('reading: twelve ways of 63 coins', 'twelve identical rows of forty 16s "and 23 more"' in R['referee27/reading.md'] and 'twelve ways of 63 coins' in sec)
    ok('reading: the search to 200 for three coins', 'For three coins my search to 200 found nothing better' in R['referee27/reading.md'] and "the referee's own search to 200 found nothing better for three coins" in sec)
    ok('mending: all 314 again, no disagreement; 38 states of 314', 'All 314 states were driven again' in R['referee27/mending.md'] and 'Result: 0 disagreements' in R['referee27/mending.md'] and 'In 38 of the 314 states' in R['referee27/mending.md'] and '38 states of 314' in sec)
    passed2 = len(re.findall(r'\| m\d[^|]*\| passes, 0 failed', R['referee27/mending.md'])); passed3 = len(re.findall(r'\| m\d[^|]*\| passes, 0 failed', R['referee27/last.md'])); passed4 = len(re.findall(r'\| m\d[^|]*\| passes, 0 failed', R['referee27/pending.md']))
    ok('broken copies of the referee\'s that passed: 3 + 2 + 2 + 0 = seven', (passed2, passed3, passed4) == (2, 2, 0) and 'Seven broken copies of the referee' in sec and 'two more broken copies passed' in sec and 'Two more broken copies passed' in sec, (passed2, passed3, passed4))
    ok('pending: 76 trials', '76 trials (`drive6.js`' in R['referee27/pending.md'] and '*Pending*, 15:39, 76 trials' in sec)
    ok('pending: a second tap at 400 ms adds a second coin; keys within about 0.4 s of Enter', 'At 400 ms on the light coinage the second tap is accepted' in R['referee27/pending.md'] and 'keys struck within about 0.4 s of Enter are lost silently' in R['referee27/pending.md'] and 'A second tap about 0.4 s after the first' in sec and 'Keys struck within about 0.4 s of Enter' in sec)
    ok('visit 4: the two-coin figure worked by hand, 8.45', '8.45' in R['reader/visit-4.md'] and node("console.log(P.bound(2,100,'plain')/100)") == '8.45', node("console.log(P.bound(2,100,'plain')/100)"))
    ok('seven visits and five messages are in the folders', all(os.path.exists(os.path.join(HERE, 'reader/visit-%d.md' % i)) and os.path.exists(os.path.join(HERE, 'reader/brief-%d.md' % i)) for i in range(1, 8)) and all(os.path.exists(os.path.join(HERE, 'reader/change-as-visited-%d.html.txt' % i)) for i in range(2, 8)) and not os.path.exists(os.path.join(HERE, 'reader/change-as-visited-1.html')))
    # ---- 3b. what the section says of each visit, beside the reader's own words ----
    V = lambda k: R['reader/visit-%d.md' % k]
    ok('visit 1: nine sentences, read twice; the rings more than two screens down; the pictures and table off the screen with no sign; the arithmetic held',
       'It is nine sentences, and I read it twice.' in V(1) and 'are more than two screens down' in V(1) and 'the pictures and table that run off the screen with no sign' in V(1) and "The page's arithmetic held everywhere I checked it by hand" in V(1) and
       'two screens above, and does not say what it added' in V(1) and 'a paragraph of nine sentences, read twice' in sec)
    ok('visit 2: two ways run together; the reason a screen away from the grey buttons', 'there are four rows running together' in V(2) and 'a screen away from the grey buttons' in V(2))
    ok('visit 3: the first screen at 360 by 640', 'the first screen at 360 by 640' in V(3))
    ok('visit 4: the figure by hand', 'From it alone I worked out the two-coin figure by hand' in V(4) and '845 coins over 100 amounts is 8.45' in V(4))
    ok('visit 5: three sentences heavier', 'The new qualifications make three sentences heavier' in V(5) and 'the reader found three sentences heavier for it' in sec)
    ok('visit 6: caught on film; one of the top three', 'is now caught on film both times' in V(6) and 'At first I read it as "one of the top three"' in V(6) and 'was caught on film' in sec)
    ok('visit 5 to visit 6: the button shortened, the table sentence cut in two, the foot reworded',
       "the best coin up to ' + n + ' for paying with change" in rd('reader/change-as-visited-5.html.txt') and "the best coin tried') + ' for paying with change" in rd('reader/change-as-visited-6.html.txt') and
       'every set was tried, and these have the lowest average: with coins up to' in rd('reader/change-as-visited-5.html.txt') and 'every set was tried, and these have the lowest average. Paying exactly, coins up to' in rd('reader/change-as-visited-6.html.txt') and
       'they are its.' in rd('reader/change-as-visited-5.html.txt') and 'the credit is theirs.' in rd('reader/change-as-visited-6.html.txt') and 'three places have grown heavier for the sake of exactness' in V(5))
    ok('reading: whose the best sets are', 'which quotes Shallit crediting Usenet posts of April 2000; README line 19 gives the best four to Thomas Young\'s students in 1995' in R['referee27/reading.md'])
    md = rd('referee27/mending.md'); rows = re.findall(r'^\s*\| [^|\n]+ \| \d+ \| (none|shown) \| ([\d.]+) s \|', md, re.M)
    ok('mending: of four long counts timed, at 0.9 to 1.7 s, three showed no sign; a count set twice', [r[0] for r in rows].count('none') == 3 and len(rows) == 4 and min(float(r[1]) for r in rows) >= 0.9 and max(float(r[1]) for r in rows) <= 1.7 and
       'The rule (coins times amounts above 2000) is not what makes a count long.' in R['referee27/mending.md'] and '"Counting…" was set twice' in R['referee27/mending.md'].replace('\u2026', '…'), rows)
    ok('pending: a press held through the count', 'by holding' in R['referee27/pending.md'] and 'let go 900 ms after the count ended. The click was accepted and a 313 was added.' in R['referee27/pending.md'])
    pmsrc = rd('page-mutants.py'); full0 = rd('out27/page-mutants.full-27nov.out')
    seven = ['of-the-hundred', 'searched-to-250', 'multiple-of-the-smallest-coin', 'first-tooltip-outlives-its-coins', 'legend-with-change-of-nothing', 'no-count-without-frames', 'legend-same-when-near']
    ok('the referee\'s seven copies that passed are in the list of faults; the first whole run caught six by assertions and stopped on the seventh, which fails its own assertion in the run after',
       all(("('%s'" % n) in pmsrc for n in seven) and all(re.search(r'^%s .* -- caught: \d+ of 223 assertions fail' % n, full0, re.M) for n in seven if n != 'no-count-without-frames') and
       re.search(r'^no-count-without-frames .* -- caught: the test stops', full0, re.M) and re.search(r'^no-count-without-frames .* -- caught: 1 assertions fail and then the test stops, after 206', rd('out27/page-mutants.stopped-27nov.out'), re.M))
    ok('Young: the sentence near the top says "explored", by his own account; the page\'s foot too; the referee at its mending',
       "by Thomas Young's own account there, in A364607, he and three students found a best four in 1995, 1, 5, 18 and 25, trying every set of four with a program" in norm(readme) and 'were found by' not in readme[:readme.index('## 27 November: the page remade')] and
       'Your local copy of A364607 goes further ("calculated the average number of coins returned for every possible set of 4 coin denominations"; data 1, 5, 18, 25)' in R['referee27/mending.md'] and
       '(1, 5, 18, 25) and (1, 5, 18, 29) at 3.89 and no other four' in norm(readme) and 'The second referee had said that my copy of the entry "goes further"' in norm(rd('sources.md')) and
       'he and three students explored the best four coins in 1995' in page['pageSays'] + new_src and '`sources.md` quotes only "explored the idea of the best 4-coin system"' in R['referee27/mending.md'])
    ok('reading: the warning about half-way rounding, and that it met none', 'The page rounds from a floating-point number, so a half-way case that goes down is possible; I did not meet one.' in R['referee27/reading.md'] and
       'it met none, and I then counted them' in sec and 'were rounded as the machine' not in sec)
    ok('reading: which best sets it recomputed', 'Best sets by my own search: exactly for 1 to 4 coins, with change for 1 to 3 coins (coins to 200): the same sets and totals as the page.' in R['referee27/reading.md'] and
       'Not recomputed by me: that the sets for 5 to 7 coins exactly, and 4 and 5 with change, are best. I only confirmed the totals of {1,5,16,23,33} (329) and {19,20,23,32} (309).' in R['referee27/reading.md'])
    bjs = rd('referee27/blind-beside-pcore.js')
    ok('blind: one of the 37 comparisons is with best.json', "same('item 5'" in bjs and 'BEST.plain[3].sets' in bjs and len([l for l in bjs.split('\n') if l.startswith('same(') and 'BEST.' in l]) == 1 and 'one of them, the best four coins, with `best.json`' in sec, bjs.count('BEST.'))
    ok('left: the 314 not made again on the last page; the public build; a slow phone; a finger', 'The 314-state comparison and the 61 add-button presses were not rerun on this page.' in R['referee27/pending.md'] and
       all('Not checked: a slow phone, sets with change beyond coins of 150, and the page as built for the public site.' in R['referee27/%s.md' % x] for x in ('mending', 'last')) and
       'On a phone slowed sixfold it lasted about four seconds.' in V(5) and 'on a phone slowed fourfold' in V(6) and 'Not tried with a finger on the phone.' in R['referee27/pending.md'] and 'on a heavy one, longer' in R['referee27/pending.md'])
    ok('left: the reader\'s small things', 'the menu drops "United States" for "your own" though the coins are still American' in V(4) and 'The twelve ways run to about a screen and a half' in V(5) and
       'uses the word twice in two senses on one line' in V(2) and 'It means "change allowed", not "change given"' in V(2) and 'the lines are squeezed into the bottom fifth of the frame' in V(2))
    r8 = rd('out27/remake8.py'); s7, s8 = rd('out27/page.src.stage7.html.txt'), rd('page.src.html')
    def body(src, name):                      # a function of the page's script, from its name to the next function at the same depth
        i = src.index('\n  function ' + name + '('); j = src.index('\n  function ', i + 10); return src[i:j]
    counting = ['compute', 'drawTiles', 'drawA', 'costText']
    import difflib
    changed = [l for l in difflib.unified_diff(s7.split('\n'), s8.split('\n'), lineterm='', n=0) if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
    ok('the last round of changes: taps while counting, the tied buttons\' names, the tables\' sentence, a clause of a caption and of the foot; no counting (the page\'s counting functions are the same, letter for letter, in the source before that round and now; pcore.js is embedded by the build and was not touched by it)',
       'These sets have the lowest average of all that were tried.' in r8 and 'a still la' in r8 and 'The counting behind the floor' in r8 and 'function others(list)' in r8 and 'S.pending' in r8 and
       all(body(s7, f) == body(s8, f) for f in counting) and s8 == rd('out27/page.src.stage8.html.txt') and 'pcore' not in r8 and not any(re.search(r'P\.(plain|greedy|both|counts|total|bestAdd|schemes|bound)\(', l) and 'others(' not in l and 'Add a ' not in l for l in changed), len(changed))
    bp = rd('referee27/brief-pending.md')
    ok('my last message to the referee listed the taps, the tied buttons\' names and the tables\' sentence, and not the two reworded clauses', 'b. the buttons that add a coin say "equal best with' in bp and 'c. the sentence over the tables of best sets no longer begins with' in bp and
       'still larger' not in bp and 'counting behind the floor' not in bp and '(c), the sentence over the tables: now true as it stands.' in R['referee27/pending.md'] and 'the two reworded clauses were not in my message to it' in sec)
    L2 = page['left']; lb = json.loads(rd('out27/look-b.out').strip().split('\n')[0])
    ok('the reader\'s small things, on the page as it stands: "your own" after only the range is changed; twelve ways of 999 take 777 px of 844; after twelve coins the second picture\'s lines lie between 70 and 80 hundredths of the way down a frame of 250 px',
       L2['menuAfterRangeOnly'] == ['own', 'your own', '1, 5, 10, 25', '49'] and L2['ways999']['height'] == 777 and L2['ways999']['screen'] == 844 and 'the first 12 are shown' in L2['ways999']['says'] and
       '777 px of 844' in sec and lb['h'] == 250 and len(lb['coins'].split(',')) == 16 and all(0.70 * 250 <= y <= 0.80 * 250 for pair in lb['lines'] for y in pair), (L2, lb))
    ok('the reader\'s sums by hand at the seventh visit', '13 coins over 7 amounts, about 1.857' in V(7) and '12 over 7, about 1.714' in V(7))
    # ---- 4. figures computed again ----
    out = node("""
      const t=(c,L,m)=>P.total(P.counts(c,L,m)); const o={};
      o.us=P.meanText(t([1,5,10,25],100,'plain'),100,3); o.swap=P.meanText(t([1,5,18,25],100,'plain'),100,3); o.swapGreedy=P.meanText(t([1,5,18,25],100,'greedy'),100,3);
      o.us24=[P.plain([1,5,10,25],100)[24], P.greedy([1,5,10,25],100)[24], P.both([1,5,10,25],100)[24]];
      o.after32=P.meanText(t([1,5,10,25,32],100,'plain'),100,3);
      const c=[20,22,24,26]; const list=P.bestAdd(c,7,'both',13); o.best13=list[0].coin; o.best13total=list[0].total; o.ties13=list.filter(x=>x.total===list[0].total).map(x=>x.coin); o.with21=t(c.concat([21]),7,'both');
      o.two=[P.both([50,51],7)[2], P.both([50,51,102],7)[2]];
      console.log(JSON.stringify(o));""")
    o = json.loads(out)
    ok('American coins 4.7; with an 18 for the 10, 3.89; the cashier 4.58', (o['us'], o['swap'], o['swapGreedy']) == ('4.7', '3.89', '4.58'), out)
    ok('24 cents: six coins, the cashier the same, two with change', o['us24'] == [6, 6, 2], o['us24'])
    ok('adding a 32: from 4.7 to 3.46', o['after32'] == '3.46', o['after32'])
    ok('20, 22, 24, 26 to 6: the best coins up to 13 are 1, 3 and 5, equal, and a 21 does better', o['ties13'] == [1, 3, 5] and o['with21'] < o['best13total'] and 'the best coins up to 13 are a 1, a 3 and a 5, equal, and a 21 does better' in sec, out)
    ok('50, 51 to 6: 2 takes four coins, and three with a 102', o['two'] == [4, 3] and 102 > 51 + 6, o['two'])
    ok('twice the largest amount and one more: the page tries coins up to 2L - 1 where L is one more than the largest amount', 'one more than twice the largest amount' in sec and '13' in sec and 2 * 6 + 1 == 13)
    h = rd('out27/halfup.out')
    ok('rounding: 6,006,987 cases, 14,400 half-way (all multiples of 16), 4,224 sent down, the new function right in all, they differ in 4,224 and nowhere else',
       h.startswith('6006987 totals') and '14400 of them fall half-way in the third decimal place; 14400 of those have L a multiple of 16' in h and 'as it is now: 0 differ' in h and
       '4224 differ, 4224 of them half-way cases sent down' in h and 'old and new differ in 4224; 0 of those are not half-way cases' in h and
       all(x in sec for x in ['14,400', '4,224', '6,006,987', '3/80 = 0.0375', '1323/240 = 5.5125']) and 'I recounted and get 14,400 half-way cases, 4,224 sent down by the old rule, the first 3/80. The same as yours.' in R['referee27/mending.md'] and 'the referee counted the same' in sec, h[:200])
    # ---- 5. the tests' tallies ----
    pt = rd('out27/page-test.out').strip().split('\n')[-1]; ok('the page\'s test: 226 assertions, 0 failed', '226 assertions, 0 failed' in pt and 'has 226 assertions' in sec and '226 assertions on what it shows' in readme, pt)
    old_test = rd('tools/shot-change.before-27nov.js.txt'); ok('174 before the remake', '174' in rd('out27/README.before-27nov.md') and '174 before the remake' in sec)
    ok('the old function sent 3/80 down and 1323/240 up; the new one sends both up', node("const O=require('./out27/pcore.before-27nov.js'); console.log([O.meanText(3,80,3),O.meanText(1323,240,3),P.meanText(3,80,3),P.meanText(1323,240,3)].join('|'))") == 'about 0.037|about 5.513|about 0.038|about 5.513')
    ct = rd('ctest.out').strip().split('\n')[-1]; ok('the counting tests: 60 pass', ct.startswith('60 passed, 0 failed') and 'The tests of the counting are 60' in sec, ct)
    cf = rd('checkfacts.out').strip().split('\n')[-1]; ok('checkfacts: 52 pass', cf.startswith('52 facts pass, 0 fail') and '52 facts pass' in sec, cf)
    F = page['first']; a, b2 = F['390x844'], F['360x640']
    ok('measured on the page: at 390 by 844 all three ways of paying 24 cents end above the foot of the first screen; at 360 by 640 the first does and the second does not; lettering of 12 px in both pictures; nothing wider than the screen',
       a['scrollY'] == 0 and a['amount'] == '24' and a['coins'] == '1, 5, 10, 25' and a['both'][1] <= a['screen'] and a['plain'][0] > 0 and b2['plain'][1] <= b2['screen'] < b2['greedy'][1] and
       a['letteringA'] == [12] and a['letteringB'] == [12] and b2['letteringA'] == [12] and b2['letteringB'] == [12] and a['pageWidth'] == 390 and b2['pageWidth'] == 360, json.dumps(F))
    ok('the test asserts the first screen at 390 by 844 and at 360 by 640, and lettering of 12 px', 'the first screen holds all of it without scrolling' in test and 'at 360 by 640' in test and 'the first row of rings (paid exactly) is whole on the first screen' in test and 'with lettering of 12 px' in test)
    ok('the buttons stay shut 350 ms after a count; two frames; a 300 ms fallback', 'S.pending = false; }, 350)' in rd('page.src.html') and 'requestAnimationFrame(function () { requestAnimationFrame(go); })' in rd('page.src.html') and 'setTimeout(go, 300)' in rd('page.src.html'))
    heads = {k: ' '.join(rd('out27/remake%s.py' % k).split('\n')[:3]) for k in [4, 5, 6, 7, 8]}
    ok('the page scripts: the first three are the first remake; the fourth to the eighth say which visit they follow (the second to the sixth)',
       all(os.path.getmtime(os.path.join(HERE, 'out27', 'remake%s.py' % k)) <= os.path.getmtime(os.path.join(HERE, 'reader/change-as-visited-2.html.txt')) + 120 for k in ['', 2, 3]) and
       "after the reader's second visit" in heads[4] and "after the reader's third visit" in heads[5] and "the reader's fourth visit" in heads[6] and "the reader's fifth visit" in heads[7] and "the reader's sixth visit" in heads[8] and
       'the first three for the first remake, then one before each of the reader\'s visits from the third on' in sec, heads)
    ok('eight page scripts and nine test scripts', all(os.path.exists(os.path.join(HERE, 'out27', 'remake%s.py' % k)) for k in ['', 2, 3, 4, 5, 6, 7, 8]) and not os.path.exists(os.path.join(HERE, 'out27/remake9.py')) and all(os.path.exists(os.path.join(HERE, 'out27', 'test-remake%s.py' % k)) for k in ['', 2, 3, 4, 5, 6, 7, 8, 9]) and not os.path.exists(os.path.join(HERE, 'out27/test-remake10.py')) and '`test-remake9.py` (the test: the first two for the first remake, five for the rounds of reading, and the last two for what the batch showed)' in sec)
    full = rd('out27/page-mutants.full-27nov.out'); missed = re.findall(r'^(\S+) .* -- NOT caught: all 223 assertions pass', full, re.M); stops = re.findall(r'^(\S+) .* -- caught: the test stops', full, re.M)
    ok('the first whole run: 132 of 135 against 223 assertions, the true page passing five times; the three that passed; the three caught only by a stop',
       '132 of 135 broken copies of the page caught; the true page run among them 4 times passed 4 times' in full and full.startswith('control, alone: the true page, built and run in the same way: all 223 assertions pass') and
       missed == ['notice-not-cleared', 'long-list-of-or', 'counted-twice'] and stops == ['swap-button-dead', 'caret-lost', 'no-count-without-frames'] and
       'it caught 132, and the true page passed each of its five runs' in sec and 'Three faults passed.' in sec and 'Three faults were caught only in that the test stopped' in sec, (missed, stops))
    three = rd('out27/page-mutants.three-27nov.out')
    ok('the three: two caught by their assertions in that record, the third only stopping the test there and failing its assertion in the next', '3 of 3 broken copies of the page caught' in three and 'passed 3 times' in three and 'all 226 assertions pass' in three and
       all(re.search(r'^%s .* -- caught: 1 of 226 assertions fail' % n, three, re.M) for n in ['notice-not-cleared', 'long-list-of-or']) and re.search(r'^counted-twice .* -- caught: the test stops', three, re.M) and
       re.search(r'^counted-twice .* -- caught: 1 assertions fail and then the test stops, after 174: Enter in the box', rd('out27/page-mutants.stopped-27nov.out'), re.M) and
       'Two are caught by theirs in `out27/page-mutants.three-27nov.out`; the third only stopped the test there' in sec)
    st = rd('out27/page-mutants.stopped-27nov.out'); two = rd('out27/page-mutants.two-mended-27nov.out')
    ok('a stopped test says what it had found: one had failed its assertion; one broke the whole script (stopped after 1); one was caught only by the stop',
       re.search(r'^no-count-without-frames .* -- caught: 1 assertions fail and then the test stops, after 206', st, re.M) and re.search(r'^swap-button-dead .* -- caught: 1 assertions fail and then the test stops, after 1: eleven coinages', st, re.M) and
       re.search(r'^caret-lost .* -- caught ONLY BY THE TEST STOPPING, after 164 assertions that all pass', st, re.M) and re.search(r'^counted-twice .* -- caught: 1 assertions fail and then the test stops, after 174: Enter in the box', st, re.M))
    ok('the two faults set right are caught by assertions', re.search(r'^swap-button-dead .* -- caught: \d+ of 226 assertions fail', two, re.M) and re.search(r'^caret-lost .* -- caught: \d+ of 226 assertions fail', two, re.M) and '2 of 2 broken copies' in two and 'passed 2 times' in two)
    pm = [l for l in rd('page-mutants.out').split('\n') if 'broken copies of the page caught' in l]
    m = re.search(r'(\d+) of (\d+) broken copies of the page caught', pm[-1]) if pm else None
    last = rd('page-mutants.out')
    ok('the last whole run: its tally, against 226 assertions, is the one in the section; every fault caught by an assertion, two of them then stopping the test; the true page five times; 36 minutes',
       m and ('caught %s of the %s' % (m.group(1), m.group(2))) in sec and m.group(2) == '135' and 'all 226 assertions pass' in last.split('\n')[0] and 'passed 4 times; 4 at a time, 36 minutes' in pm[-1] and
       len(re.findall(r' -- caught: \d+ of 226 assertions fail', last)) + len(re.findall(r' -- caught: \d+ assertions fail and then the test stops', last)) == int(m.group(1)) == 135 and
       len(re.findall(r' -- caught: \d+ assertions fail and then the test stops', last)) == 2 and not re.search(r'NOT caught|ONLY BY THE TEST STOPPING|caught: the test stops|does not finish', last) and
       len(re.findall(r'THE TRUE PAGE, run among the broken copies, 4 at a time -- passes: all 226 assertions pass', last)) == 4 and cmp_files('page-mutants.out', 'out27/page-mutants.final-27nov.out'), pm[-1][:200] if pm else 'no tally in page-mutants.out')
    cmo = rd('cmutants.out'); cm = cmo.strip().split('\n')[-1]; m = re.match(r'(\d+) of (\d+) broken copies caught; passed: none', cm)
    ok('the counting program\'s batch: 59 of 59, four of them in the rounding, the control passing before and after', m and m.group(1) == m.group(2) == '59' and 'broken 59 ways (four of them in this rounding, added today), the tests catch 59' in sec and
       len(re.findall(r'^caught   meantext-(?:machine-rounding|rounds-down|half-goes-down|always-three-places) ', cmo, re.M)) == 4 and cmo.startswith('control (nothing broken): passes') and 'control again, after the last: passes' in cmo and
       'the program broken 59 ways; the tests catch 59' in readme and '| `ctest.js` | 60 tests' in readme, cm[:200])
    pub = rd('out27/page-test.public-27nov.out'); fp = json.loads(rd('out27/first-public.out').strip().split('\n')[-1]); A, B = fp['390x844'], fp['360x640']; fl = [l for l in pub.split('\n') if l.startswith('FAILED: ')]
    ok('the page as built for the public site: 226 assertions, 2 failed, both about the first screen; the build\'s line 88 px at 390 wide and 107 at 360; the third row ends one pixel below 844; the first row begins 19 px below 640, in the box for the amount',
       'PAGE TEST: 226 assertions, 2 failed' in pub and len(fl) == 2 and fl[0].startswith('FAILED: on a phone (390 by 844) the page opens') and fl[1].startswith('FAILED: at 360 by 640 the button') and
       A['line'] == [0, 88] and B['line'] == [0, 107] and A['both'][1] - A['screen'] == 1 and A['greedy'][1] <= A['screen'] and B['plain'][0] - B['screen'] == 19 and B['amountBox'][0] < B['screen'] < B['amountBox'][1] and
       F['390x844']['plain'][0] + 88 == A['plain'][0] and F['360x640']['plain'][0] + 107 == B['plain'][0] and '224 of the 226 assertions hold there' in sec and '88 px tall on a phone 390 wide, 107 px at 360' in sec, json.dumps(fp))
    ok('nothing is left to come', 'TO-COME' not in readme)
    t1, t2 = norm(rd('truth27/report.md')), norm(rd('truth27/report-mends.md'))
    ok('the reader for truth: nine sentences at the first reading and four things left out; three at the second',
       'Nine sentences say more than, or other than, their source' in t1 and 'Four things the reports leave are neither mended nor listed.' in t1 and len(re.findall(r'^\d\. \*\*', rd('truth27/report.md').split('## 2.')[0], re.M)) == 9 and
       'all nine mends are in the files and hold to the letter' in t2 and len([l for l in rd('truth27/report-mends.md').split('## 4.')[1].split('\n') if l.startswith('- Section')]) == 3 and
       'it found nine sentences that said more than their sources, or other than them, and four things left out; at its second, three more among my mends' in sec)
    def texts():
        for d in ('reader', 'referee27', 'truth27', 'out27'):
            for f in sorted(os.listdir(os.path.join(HERE, d))):
                q = os.path.join(HERE, d, f)
                if os.path.isfile(q) and not f.endswith(('.png', '.private.txt')): yield d + '/' + f, open(q, encoding='utf-8', errors='replace').read()
    hits = [n for n, t in texts() if re.search(r'\ba[0-9a-f]{16}\b', t)]
    ok('no agent id in any text file of the four folders (the two files named *.private.txt, which hold them, stay at home)', not hits, hits)
    print('%d checks hold, %d fail' % (n_ok, n_bad)); sys.exit(1 if n_bad else 0)

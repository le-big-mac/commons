"""The coin page's test, fourth stage: the page's fifth stage.   python -I test-remake4.py   (run after test-remake3.py)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'tools/shot-change.js', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    rep("const setCoins = async (coins, L) => { await p.fill('#coins', coins); await p.fill('#L', String(L)); await p.click('#apply'); await p.waitForTimeout(80); };",
        "const setCoins = async (coins, L) => { await p.fill('#coins', coins); await p.fill('#L', String(L - 1)); await p.click('#apply'); await p.waitForTimeout(80); };      /* the box holds the largest amount, L - 1 */")
    rep("must((await p.inputValue('#coins')) === c.join(', ') && (await p.inputValue('#L')) === String(L), 'coinage ' + i + ': the coins and the range are shown in the boxes');",
        "must((await p.inputValue('#coins')) === c.join(', ') && (await p.inputValue('#L')) === String(L - 1), 'coinage ' + i + ': the coins and the largest amount are shown in the boxes');")
    rep("['1, 5', 1, 'from 2 to 1000'], ['1, 5', 5000, 'from 2 to 1000']", "['1, 5', 1, 'from 1 to 999'], ['1, 5', 5000, 'from 1 to 999']")
    rep("await p.fill('#coins', c); await p.fill('#L', String(L)); await p.click('#apply'); await p.waitForTimeout(40);", "await p.fill('#coins', c); await p.fill('#L', String(L - 1)); await p.click('#apply'); await p.waitForTimeout(40);")
    rep("(await p.inputValue('#coins')) === '16, 19, 21' && (await p.inputValue('#L')) === '100' &&", "(await p.inputValue('#coins')) === '16, 19, 21' && (await p.inputValue('#L')) === '99' &&")
    rep("tip.includes('paid exactly 2 (2 × 24)')", "tip.includes('paid exactly, at best 2 (2 × 24)')")
    rep("const okHead = head.includes(s.count + ' coin') &&", "const okHead = (fin(P.plain(c, a + 1)[a]) && P.plain(c, a + 1)[a] === s.count) === /changes? hands, no fewer than paying exactly/.test(head) && head.includes(s.count + ' coin') &&")
    rep("&& st1 === 'These are the American coins with the 10 swapped for an 18: 3.89 on average where American coins take 4.7, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, needs 4.58 with these. Put the 10 back',",
        "&& st1 === 'These are the American coins with the 10 swapped for an 18. They take 3.89 on average if the coins are well chosen every time (American coins take 4.7); a cashier, who takes the largest coin that fits, needs 4.58 with these. Put the 10 back',")
    rep("""    const words = await p.evaluate(() => document.querySelector('main').innerText);""", """    { await p.selectOption('#preset', '1'); await p.waitForTimeout(80); await p.fill('#amount', '38'); await p.waitForTimeout(60); const s38 = await text('#sayA'), th = await p.evaluate(() => [...document.querySelectorAll('#tabA th')].map(x => x.textContent).join('|')), lab = await p.evaluate(() => document.getElementById('L').closest('label').textContent.trim());
      must(s38.startsWith('Amount 38: paid exactly, at best 4 (2 × 18 + 2 × 1); the cashier\\'s way 6 (25 + 2 × 5 + 3 × 1); with change 3 (') && th === 'amount|paid exactly, at best|the cashier\\'s way|with change' && lab === 'Amounts from 0 to' && (await p.inputValue('#L')) === '99',
        'where the cashier takes more, the count beside the cashier\\'s is "paid exactly, at best", in the sentence and at the head of the table (a visitor: "paid exactly 4" beside "the cashier\\'s way 6" reads as if the cashier did not pay exactly); and the box for the range is labelled "Amounts from 0 to" and holds 99', s38.slice(0, 120)); }
    const words = await p.evaluate(() => document.querySelector('main').innerText);""")
    # the first screen at 360 by 640 (a visitor: the new button on a line of its own pushed the rings off it)
    rep("""    for (const wv of [320, 360, 390]) { await ph.setViewportSize({ width: wv, height: 800 });""", """    { const c3 = await b.newContext({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }), q = await c3.newPage(); await q.goto('file://' + page); await q.waitForTimeout(400);
      const f = await q.evaluate(() => { const r = id => document.getElementById(id).getBoundingClientRect(); return [r('L').top, r('apply').top, r('apply').bottom, r('L').bottom, r('way-plain').top, r('way-plain').bottom, innerHeight]; });
      must(f[1] < f[3] && f[2] > f[0] && f[5] <= f[6], 'at 360 by 640 the button "Use these coins" stands beside the box for the range, not on a line of its own, and the first row of rings (paid exactly) is whole on the first screen (a visitor: the button "sits on its own line, so the screen now ends at the slider")', JSON.stringify(f.map(x => Math.round(x)))); await c3.close(); }
    for (const wv of [320, 360, 390]) { await ph.setViewportSize({ width: wv, height: 800 });""")
    open(H + 'tools/shot-change.js', 'w', encoding='utf8').write(s); print('tools/shot-change.js, fourth stage:', len(s))

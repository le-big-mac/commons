"""The coin page's test brought to the page as remade on 27 November.   python -I test-remake.py
(made from tools/shot-change.before-27nov.js.txt, so that it can be run again)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'tools/shot-change.before-27nov.js.txt', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    # the coinages in their new order: United States first
    rep("""  const fin = v => v < P.INF, BOX = { l: 44, r: 112, t: 26, b: 34 };
  const PRE = [[[1, 2, 5, 10, 20, 50, 100, 200], 100], [[1, 5, 10, 25], 100], [[1, 5, 10, 25, 50, 100], 100], [[1, 5, 18, 25], 100], [[1, 3, 6, 12, 24, 30], 240], [[1, 5, 10, 25, 100, 200], 500],""",
        """  const fin = v => v < P.INF, BOX = { l: 44, r: 128, t: 26, b: 34 };      /* the frame on a wide screen; the pictures are as many units wide as they are pixels */
  const VB = id => p.evaluate(i => { const v = document.getElementById(i).viewBox.baseVal; return [v.width, v.height]; }, id);
  const EURO = '2', US = '0', BRIT = '4';
  const PRE = [[[1, 5, 10, 25], 100], [[1, 5, 18, 25], 100], [[1, 2, 5, 10, 20, 50, 100, 200], 100], [[1, 5, 10, 25, 50, 100], 100], [[1, 3, 6, 12, 24, 30], 240], [[1, 5, 10, 25, 100, 200], 500],""")
    # reading a line back: the frame's size from the picture itself
    rep("""        labels: T.map(t => { const q = t.getBBox(); return [q.x, q.x + q.width, q.y, q.y + q.height]; }) }; }, [chart, line]);""",
        """        labels: T.map(t => { const q = t.getBBox(); return [q.x, q.x + q.width, q.y, q.y + q.height]; }), W: svg.viewBox.baseVal.width, Hh: svg.viewBox.baseVal.height, shown: svg.getBoundingClientRect().width }; }, [chart, line]);""")
    rep("""    const inside = g.box[0] >= BOX.l - 1 && g.box[2] <= 1000 - BOX.r + 1 && g.box[1] >= BOX.t - 1 && g.box[3] <= 300 - BOX.b + 1;
    const marksIn = g.marks.every(m => m[0] >= BOX.l - 1 && m[0] <= 1000 - BOX.r + 1 && m[1] >= BOX.t - 6 && m[1] <= 300 - BOX.b + 1);
    const labelsIn = g.labels.every(l => l[0] >= -0.5 && l[1] <= 1000.5 && l[2] >= -0.5 && l[3] <= 300.5);
    return { vals, inside, marksIn, labelsIn, marks: g.marks, xv, yv }; };""",
        """    const inside = g.box[0] >= BOX.l - 1 && g.box[2] <= g.W - BOX.r + 1 && g.box[1] >= BOX.t - 1 && g.box[3] <= g.Hh - BOX.b + 1;
    const marksIn = g.marks.every(m => m[0] >= BOX.l - 1 && m[0] <= g.W - BOX.r + 1 && m[1] >= BOX.t - 6 && m[1] <= g.Hh - BOX.b + 1);
    const labelsIn = g.labels.every(l => l[0] >= -0.5 && l[1] <= g.W + 0.5 && l[2] >= -0.5 && l[3] <= g.Hh + 0.5) && Math.abs(g.W - g.shown) < 1.5;      /* and a unit of the picture is a pixel, so that its lettering is the size it says */
    return { vals, inside, marksIn, labelsIn, marks: g.marks, xv, yv }; };""")
    # the tiles
    rep("""must(t[0].v === P.meanText(tp, L, 3) && t[0].d.includes(P.worst(pl) + ' at worst') && t[0].d.includes('No set of ' + D + ' coins could cost less than ' + P.meanText(P.bound(D, L, 'plain'), L, 3) + '.'), 'coinage ' + i + ': the one-way tile');""",
        """must(t[0].v === P.meanText(tp, L, 3) && t[0].d === 'coins on average; ' + P.worst(pl) + ' at worst.', 'coinage ' + i + ': the tile for the fewest coins');""")
    rep("""'coinage ' + i + ': the one-way tile says what cannot be made');""", """'coinage ' + i + ': the tile for the fewest coins says what cannot be made');""")
    rep("""(pf === 0 ? t[1].d.startsWith('Always the fewest coins') && gf.length === 0 :""", """(pf === 0 ? t[1].d === 'With these coins the cashier never takes more than the fewest, however large the amount.' && gf.length === 0 :""")
    rep("""'coinage ' + i + ': the greedy tile'); }""", """'coinage ' + i + ': the cashier\\'s tile'); }""")
    rep("""'coinage ' + i + ': the greedy tile says where it gets stuck');""", """'coinage ' + i + ': the cashier\\'s tile says where the cashier gets stuck');""")
    rep("""must(t[2].v === P.meanText(tb, L, 3) && t[2].d.includes(P.worst(bo) + ' at worst') && t[2].d.includes('could cost less than ' + P.meanText(P.bound(D, L, 'both'), L, 3) + '.'), 'coinage ' + i + ': the both-ways tile');""",
        """must(t[2].v === P.meanText(tb, L, 3) && t[2].d === 'coins changing hands on average; ' + P.worst(bo) + ' at worst.' && !t.some(x => /could cost less|cost/.test(x.d)) && (await text('#capA')) === 'The coins for each amount from 0 to ' + (L - 1), 'coinage ' + i + ': the tile for paying with change; no tile speaks of "cost" or of what no set could do; the picture\\'s heading names the range');""")
    rep("""'coinage ' + i + ': a ring at every amount where greedy takes more, at greedy\\'s count');""", """'coinage ' + i + ': a ring at every amount where the cashier takes more, at the cashier\\'s count');""")
    # the sentence under the second picture
    rep("""    must(sayB.includes('One way the best coin to add is ' + bp.map(e => e.coin).join(' or ') + ', bringing the cost ' + (isFinite(tp) ? 'from ' + P.meanText(tp, L, 3) + ' ' : '') + 'to ' + P.meanText(bp[0].total, L, 3) + '.') &&
      sayB.includes('Both ways it is ' + bb.map(e => e.coin).join(' or ') + ', ' + (isFinite(tb) ? 'from ' + P.meanText(tb, L, 3) + ' ' : '') + 'to ' + P.meanText(bb[0].total, L, 3) + '.'), 'coinage ' + i + ': the sentence under the second picture names the best coins and their costs');""",
        """    const nm = l => { const k = l.map(e => e.coin); return k.length <= 5 ? k.join(' or ') : k.slice(0, 4).join(', ') + ' or any of ' + (k.length - 4) + ' others'; };
    must(sayB.includes('For the fewest coins the best coin to add is ' + nm(bp) + ', bringing the average ' + (isFinite(tp) ? 'from ' + P.meanText(tp, L, 3) + ' ' : '') + 'to ' + P.meanText(bp[0].total, L, 3) + '.') &&
      sayB.includes('With change it is ' + nm(bb) + ', ' + (isFinite(tb) ? 'from ' + P.meanText(tb, L, 3) + ' ' : '') + 'to ' + P.meanText(bb[0].total, L, 3) + '.') && !/cost|one way|both ways|greedy/i.test(sayB), 'coinage ' + i + ': the sentence under the second picture names the best coins and their averages, in the page\\'s new words');""")
    rep("""console.log(`coinage ${i} (${c.join(',')}; below ${L}): ${t[0].v} | ${t[1].v} | ${t[2].v}; add ${bp.map(e => e.coin).join('/')} one way, ${bb.map(e => e.coin).join('/')} both ways; ${gf.length} greedy rings`);""",
        """console.log(`coinage ${i} (${c.join(',')}; below ${L}): ${t[0].v} | ${t[1].v} | ${t[2].v}; add ${bp.map(e => e.coin).join('/')} for the fewest coins, ${bb.map(e => e.coin).join('/')} with change; ${gf.length} rings for the cashier`);""")
    # paying an amount
    rep("""for (const [i, amounts] of [[0, [1, 8, 38, 49, 99, 73]], [4, [48, 50, 113, 239, 7]], [8, [1, 2, 10, 50, 99, 13]], [1, [30, 99, 68, 4]], [7, [5, 40, 77]], [5, [499, 83, 250]]]) {""",
        """for (const [i, amounts] of [[2, [1, 8, 38, 49, 99, 73]], [4, [48, 50, 113, 239, 7]], [8, [1, 2, 10, 50, 99, 13]], [0, [30, 99, 68, 4, 24]], [7, [5, 40, 77]], [5, [499, 83, 250]]]) {""")
    rep("""const okHead = head.includes(s.count + ' coin') && head.includes('in ' + s.total + ' way') && (s.total > 12) === head.includes('the first 12 shown');""",
        """const okHead = head.includes(s.count + ' coin') && (s.total === 1 ? !/ways/.test(head) : head.includes('it can be done in ' + s.total + ' ways')) && (s.total > 12) === head.includes('the first 12 are shown') && head.startsWith('With change: ');""")
    rep("""const okPlain = fin(pc) ? sum(pw) === a && pw.length === pc && ph.includes(pc + ' coin') : pw.length === 0 && ph.includes('cannot be made');""",
        """const okPlain = fin(pc) ? sum(pw) === a && pw.length === pc && ph.includes(pc + ' coin') && ph.startsWith('Fewest coins: ') : pw.length === 0 && ph.includes('cannot be paid exactly');""")
    rep("""must(good === n, 'settling an amount: the coins drawn are the ways pcore lists, for ' + n + ' amounts in six coinages (' + good + ' right)'); console.log(`settle an amount: ${good} of ${n} right`);""",
        """must(good === n, 'paying an amount: the coins drawn are the ways pcore lists, for ' + n + ' amounts in six coinages (' + good + ' right)'); console.log(`pay an amount: ${good} of ${n} right`);""")
    rep("""    await p.selectOption('#preset', '0'); await p.fill('#amount', '0'); await p.waitForTimeout(30); must((await text('#ways')).includes('Nothing to settle') && (await count('#ways .coin')) === 0, 'amount 0: nothing to settle');""",
        """    await p.selectOption('#preset', EURO); await p.fill('#amount', '0'); await p.waitForTimeout(30); must((await text('#ways')).includes('Nothing to pay') && (await count('#ways .coin')) === 0, 'amount 0: nothing to pay');""")
    # hover, click and keys
    rep("""    const sx = a => bx.x + (BOX.l + (a + 0.5) / L * (1000 - BOX.l - BOX.r)) / 1000 * bx.width;""", """    const WA = (await VB('chartA'))[0], sx = a => bx.x + (BOX.l + (a + 0.5) / L * (WA - BOX.l - BOX.r)) / WA * bx.width;""")
    rep("""must(vis === 'block' && tip.includes('Amount 48') && tip.includes('one way 2 (2 × 24)') && tip.includes('greedy 3 (30 + 12 + 6)') && sayA.includes('Amount 48') && sayA.includes('greedy 3'),""",
        """must(vis === 'block' && tip.includes('Amount 48') && tip.includes('fewest coins 2 (2 × 24)') && tip.includes('the cashier\\'s way 3 (30 + 12 + 6)') && sayA.includes('Amount 48') && sayA.includes('the cashier\\'s way 3'),""")
    rep("""must(tip10.includes('Amount 10') && !tip10.includes('greedy') && tip10.includes('one way ' + P.plain(PRE[4][0], 11)[10] + ' (') && tip10.includes('both ways ' + P.both(PRE[4][0], 11)[10] + ' ('), 'where greedy takes no more, the tooltip does not speak of it');""",
        """must(tip10.includes('Amount 10') && !tip10.includes('cashier') && tip10.includes('fewest coins ' + P.plain(PRE[4][0], 11)[10] + ' (') && tip10.includes('with change ' + P.both(PRE[4][0], 11)[10] + ' ('), 'where the cashier takes no more, the tooltip does not speak of the cashier');""")
    rep("""'a click on the picture settles that amount');""", """'a click on the picture pays that amount');""")
    rep("""must(Math.abs(pick - (BOX.l + 113.5 / L * (1000 - BOX.l - BOX.r))) < 0.5, 'the dotted line stands at the amount chosen');""", """must(Math.abs(pick - (BOX.l + 113.5 / L * (WA - BOX.l - BOX.r))) < 0.5, 'the dotted line stands at the amount chosen');""")
    rep("""sxB = c => bb2.x + (BOX.l + (c - 0.5) / n * (1000 - BOX.l - BOX.r)) / 1000 * bb2.width;""", """WB = (await VB('chartB'))[0], sxB = c => bb2.x + (BOX.l + (c - 0.5) / n * (WB - BOX.l - BOX.r)) / WB * bb2.width;""")
    rep("""must(tipB.includes('With a coin of 73: one way ' + P.meanText(t73, L, 3) + '; both ways ' + P.meanText(b73, L, 3) + '.'), 'hovering over 73 on the second picture gives the costs with a 73');""",
        """must(tipB.includes('With a coin of 73 added: fewest coins ' + P.meanText(t73, L, 3) + '; with change ' + P.meanText(b73, L, 3) + '.'), 'hovering over 73 on the second picture gives the averages with a 73');
    await p.mouse.click(sxB(73), bb2.y + bb2.height / 2); await p.waitForTimeout(60); await p.mouse.move(5, 5); await p.waitForTimeout(60); { const sb = await text('#sayB'), pk = await p.evaluate(() => [document.getElementById('pickB').getAttribute('visibility'), Number(document.getElementById('pickB').getAttribute('x1'))]);
      must(sb.startsWith('With a coin of 73 added: fewest coins ' + P.meanText(t73, L, 3) + '; with change ' + P.meanText(b73, L, 3) + '.') && pk[0] === 'visible' && Math.abs(pk[1] - (BOX.l + 72.5 / n * (WB - BOX.l - BOX.r))) < 0.5, 'a click on the second picture keeps that coin\\'s averages in the sentence under it, with a dotted line at the coin, after the pointer has gone (a visitor tapped it and nothing happened)'); }""")
    rep("""must(tip300.includes('With a coin of 300: both ways') && !tip300.includes('one way'), 'a coin larger than every amount is priced both ways only');""",
        """must(tip300.includes('With a coin of 300 added: with change') && !tip300.includes('fewest coins'), 'a coin larger than every amount is tried with change only');""")
    rep("""    await p.selectOption('#preset', '0'); await p.waitForTimeout(100); await p.locator('#chartA').scrollIntoViewIfNeeded(); { const b0 = await p.locator('#chartA').boundingBox(); await p.mouse.move(b0.x + (BOX.l + 99.5 / 100 * (1000 - BOX.l - BOX.r)) / 1000 * b0.width, b0.y + b0.height / 2); await p.waitForTimeout(60);
      must((await text('#tipA')).includes('both ways 2 (100 handed over, 1 handed back)'),""",
        """    await p.selectOption('#preset', EURO); await p.waitForTimeout(100); await p.locator('#chartA').scrollIntoViewIfNeeded(); { const b0 = await p.locator('#chartA').boundingBox(); await p.mouse.move(b0.x + (BOX.l + 99.5 / 100 * (WA - BOX.l - BOX.r)) / WA * b0.width, b0.y + b0.height / 2); await p.waitForTimeout(60);
      must((await text('#tipA')).includes('with change 2 (100 handed over, 1 handed back)'),""")
    rep("""await p.fill('#amount', '239'); await p.waitForTimeout(40); await p.selectOption('#preset', '0'); await p.waitForTimeout(120);""", """await p.fill('#amount', '239'); await p.waitForTimeout(40); await p.selectOption('#preset', EURO); await p.waitForTimeout(120);""")
    # adding the best coin
    rep("""  { await p.selectOption('#preset', '0'); await p.waitForTimeout(100); await p.click('#addPlain'); await p.waitForTimeout(120); const t = await tiles();
    must((await p.inputValue('#coins')) === '1, 2, 5, 10, 20, 33, 50, 100, 200' && (await p.inputValue('#preset')) === 'own' && t[0].v === '2.86', 'adding the best coin one way to the euro adds a 33 and the cost is 2.86');
    await p.selectOption('#preset', '1'); await p.waitForTimeout(100); await p.click('#addBoth'); await p.waitForTimeout(120); const t2 = await tiles();
    must((await p.inputValue('#coins')) === '1, 5, 10, 25, 48' && t2[2].v === '2.95', 'adding the best coin both ways to the US cents adds a 48 and the cost is 2.95'); }""",
        """  { await p.selectOption('#preset', EURO); await p.waitForTimeout(100); await p.click('#addPlain'); await p.waitForTimeout(120); const t = await tiles(), said = await text('#addedSay');
    must((await p.inputValue('#coins')) === '1, 2, 5, 10, 20, 33, 50, 100, 200' && (await p.inputValue('#preset')) === 'own' && t[0].v === '2.86' && P.meanText(P.total(P.plain([1, 2, 5, 10, 20, 50, 100, 200], 100)), 100, 3) === '3.4'
      && said === 'Added a 33. The coins are now 1, 2, 5, 10, 20, 33, 50, 100, 200, and the average with the fewest coins has gone from 3.4 to 2.86.', 'adding the best coin for the fewest coins to the euro adds a 33, the average is 2.86, and the page says so where the button was pressed (a visitor pressed it, saw nothing say what was added, and pressed again)');
    await p.selectOption('#preset', US); await p.waitForTimeout(100); const cleared = await text('#addedSay'); await p.click('#addBoth'); await p.waitForTimeout(120); const t2 = await tiles();
    must(cleared === '' && (await p.inputValue('#coins')) === '1, 5, 10, 25, 48' && t2[2].v === '2.95' && (await text('#addedSay')) === 'Added a 48. The coins are now 1, 5, 10, 25, 48, and the average with change has gone from 3.98 to 2.95.', 'adding the best coin for paying with change to the US cents adds a 48 and the average is 2.95; the sentence about the last coin added goes when other coins are chosen');
    await p.selectOption('#preset', US); await p.waitForTimeout(100); let presses = 0; while (presses < 20 && !(await p.evaluate(() => document.getElementById('addPlain').disabled))) { await p.click('#addPlain'); await p.waitForTimeout(150); presses++; }
    const sb = await text('#sayB'); must(presses === 12 && (await p.inputValue('#coins')).split(', ').length === 16 && (await p.evaluate(() => document.getElementById('addBoth').disabled)) && sb.startsWith('There are 16 coins, which is as many as this page takes, so no more can be added.') && !/( or \\d+){6}/.test(sb),
      'twelve presses bring the US coins to sixteen; both buttons then stop, and the page says why; a long list of equally good coins is given as its first four and how many more (a visitor met grey buttons with no word, over thirteen lines of "or")', presses + ' presses; ' + sb.slice(0, 160)); }""")
    # coins of one's own
    rep("""await setCoins('1, 5, 10, 25', 100); must((await p.inputValue('#preset')) === '1', 'typing a listed coinage selects it in the list');""", """await setCoins('1, 5, 10, 25', 100); must((await p.inputValue('#preset')) === US, 'typing a listed coinage selects it in the list');""")
    rep("""if (n.includes(word) && shown === 'block' && JSON.stringify(await tiles()) === before) good++;""", """if (n.includes(word) && n.endsWith(' The page still shows the coins 1, 5, 10, 25.') && shown === 'block' && JSON.stringify(await tiles()) === before) good++;""")
    rep("""must(good === 9, 'nine bad entries are refused with a reason and nothing changes (' + good + ')');""", """must(good === 9, 'nine bad entries are refused with a reason, nothing changes, and the notice says which coins the page still shows (a visitor typed "banana" and read the old tiles as its answer) (' + good + ')');""")
    rep("""(await text('#sayB')).includes('One way the best coin to add is 1,'), 'coins 2 and 4:""", """(await text('#sayB')).includes('For the fewest coins the best coin to add is 1,'), 'coins 2 and 4:""")
    rep("""(await text('#sayB')).includes('One way there is no coin left to try'), 'the smallest case,""", """(await text('#sayB')).includes('For the fewest coins there is no coin left to try'), 'the smallest case,""")
    rep("""must(sb.includes('One way there is no coin left to try') && sb.includes('Both ways no single coin up to 5 lowers the cost of about 0.667.') && !sb.includes('best coin')""", """must(sb.includes('For the fewest coins there is no coin left to try') && sb.includes('With change no single coin up to 5 lowers the average of about 0.667.') && !sb.includes('best coin')""")
    rep("""must(sb.includes('One way there is no coin left to try') && sb.includes('Both ways no single coin up to 3 lowers the cost of 0.5.')""", """must(sb.includes('For the fewest coins there is no coin left to try') && sb.includes('With change no single coin up to 3 lowers the average of 0.5.')""")
    rep("""must(sb.includes('One way the best coin to add is 1, bringing the cost to')""", """must(sb.includes('For the fewest coins the best coin to add is 1, bringing the average to')""")
    rep("""    await p.selectOption('#preset', '0'); await p.fill('#amount', '38'); await p.waitForTimeout(40); { let good = 0;
      for (const bad of ['-1', '2.5', '']) { await p.fill('#amount', bad); await p.locator('#amount').press('Tab'); await p.waitForTimeout(40); if ((await p.inputValue('#amount')) === '38' && (await text('#way-both .k')).includes('3 coins') && (await p.inputValue('#amountR')) === '38') good++; }
      await p.fill('#amount', '100'); await p.waitForTimeout(40); if ((await p.inputValue('#amount')) === '99') good++;
      must(good === 4, 'the amount box: -1, 2.5 and nothing are put back to the amount in force; 100 becomes 99 (' + good + ' of 4)'); }""",
        """    await p.selectOption('#preset', EURO); await p.fill('#amount', '38'); await p.waitForTimeout(40); { let good = 0; const said = [];
      for (const bad of ['-1', '2.5', '']) { await p.fill('#amount', bad); await p.locator('#amount').press('Tab'); await p.waitForTimeout(40); const sy = await text('#amountSay'); said.push(sy);
        if ((await p.inputValue('#amount')) === '38' && (await text('#way-both .k')).includes('3 coins') && (await p.inputValue('#amountR')) === '38' && sy === (bad === '' ? 'That' : '"' + bad + '"') + ' is not a whole number from 0 to 99: the amount is still 38.') good++; }
      await p.fill('#amount', '100'); await p.waitForTimeout(40); if ((await p.inputValue('#amount')) === '99') good++;
      await p.fill('#amount', '41'); await p.waitForTimeout(40); const gone = await text('#amountSay');
      must(good === 4 && gone === '', 'the amount box: -1, 2.5 and nothing are put back to the amount in force, and the page says so under the box (a visitor: "each time the box silently went back to the old number"); 100 becomes 99; a good amount clears the sentence (' + good + ' of 4)', said.join(' | ')); }""")
    # the tables of best sets: two now
    i = s.index("  { const rows = await p.evaluate(() => [...document.querySelectorAll('#best tr')]"); j = s.index("    await p.selectOption('#preset', '4'); await p.waitForTimeout(150);\n    await p.click('#best button[data-set=\"16,19,21\"]');", i)
    s = s[:i] + """  { const rowsOf = id => p.evaluate(id => [...document.querySelectorAll('#' + id + ' tr')].slice(1).map(tr => [...tr.children].map(td => ({ t: td.textContent, sets: [...td.querySelectorAll('button')].map(b => b.getAttribute('data-set')) }))), id);
    const rp = await rowsOf('best-plain'), rb = await rowsOf('best-both'), heads = await p.evaluate(() => [...document.querySelectorAll('table.best tr:first-child')].map(tr => [...tr.children].map(th => th.textContent).join('|'))); let good = 0, sets = 0;
    for (const [rows, way] of [[rp, 'plain'], [rb, 'both']]) for (const r of rows) { const D = Number(r[0].t);
      const ok = r[3].t === P.meanText(P.bound(D, 100, way), 100, 3) && (r[1].sets.length ? r[1].sets.every(s => { const c = s.split(',').map(Number); sets++; return c.length === D && P.meanText(P.total(P[way](c, 100)), 100, 3) === r[2].t; }) : way === 'both' && r[1].t === 'not searched' && r[2].t === '');
      if (ok) good++; }
    must(rp.length === 7 && rb.length === 7 && good === 14 && sets === 20 && heads.length === 2 && heads.every(h => h === 'coins|the best sets|average|least possible'), 'the two tables of best sets, for the fewest coins and with change: seven rows each, twenty sets, each with the average its row says by pcore, with what counting alone allows; headed in the page\\'s new words');
""" + s[j:]
    rep("""    await p.click('#best button[data-set="16,19,21"]'); await p.waitForTimeout(120);""", """    await p.click('#best-both button[data-set="16,19,21"]'); await p.waitForTimeout(120);""")
    rep("""t[2].v === '3.88' && (await p.inputValue('#preset')) === 'own', 'pressing 16, 19, 21 in the table tries it above');""", """t[2].v === '3.88' && (await p.inputValue('#preset')) === '8', 'pressing 16, 19, 21 in the table tries it at the top of the page, and the list of coinages shows it by its name');""")
    # the tables open and close
    rep("""  { await p.selectOption('#preset', '0'); const shown = sel =>""", """  { await p.selectOption('#preset', EURO); const shown = sel =>""")
    rep("""const a1 = await shown('#tabA'), pr = await p.evaluate(() => document.querySelector('#tA').getAttribute('aria-pressed')); await p.click('#tA'); const a2 = await shown('#tabA');""",
        """const a1 = await shown('#tabA'), pr = await p.evaluate(() => document.querySelector('#tA').getAttribute('aria-pressed')), lab1 = await text('#tA'), sticky = await p.evaluate(() => getComputedStyle(document.querySelector('#tabA th')).position); await p.click('#tA'); const a2 = await shown('#tabA'), lab2 = await text('#tA');""")
    rep("""must(a0 === 'none' && a1 === 'block' && pr === 'true' && a2 === 'none' && b1 === 'block', 'the Table buttons open and close the tables'); }""",
        """must(a0 === 'none' && a1 === 'block' && pr === 'true' && a2 === 'none' && b1 === 'block' && lab1 === 'Hide the table' && lab2 === 'Show the table' && sticky === 'sticky', 'the table buttons open and close the tables and say which they will do; the tables\\' headings stay in sight as the rows scroll (a visitor: "its headings scroll away, leaving four unnamed columns of digits")'); }""")
    rep("""  await p.selectOption('#preset', '0'); await p.fill('#amount', '38'); await p.waitForTimeout(150); await p.locator('#fig1').screenshot""", """  await p.selectOption('#preset', EURO); await p.fill('#amount', '38'); await p.waitForTimeout(150); await p.locator('#fig1').screenshot""")
    open(H + 'out27/shot-stage1.js', 'w', encoding='utf8').write(s); print('test, stage 1:', len(s))

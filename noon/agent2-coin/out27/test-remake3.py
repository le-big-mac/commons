"""The coin page's test, third stage: the page's fourth stage (after the reader's second visit).   python -I test-remake3.py
(run after test-remake2.py: it changes tools/shot-change.js in place)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'tools/shot-change.js', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    rep("t[1].d === 'With these coins the cashier never takes more than the fewest, however large the amount.' && gf.length === 0 :", "t[1].d === 'With these coins the cashier never takes more than need be, however large the amount.' && gf.length === 0 :")
    rep("t[1].d.includes('but not for ' + pf + ':')), 'coinage '", "t[1].d.includes('but for ' + pf + ':')), 'coinage '")
    rep("""'coinage ' + i + ': the tile for paying with change; no tile speaks of "cost" or of what no set could do; the picture\\'s heading names the range');""",
        """'coinage ' + i + ': the tile for paying with change; no tile speaks of "cost" or of what no set could do; the picture\\'s heading names the range');
    must((await text('#withThese')) === 'With the coins chosen above (' + c.join(', ') + '), for the amounts from 0 to ' + (L - 1) + ':' && (i < 2 || (await text('#story')).startsWith('For comparison: American coins (1, 5, 10, 25, for the amounts from 0 to 99) take 4.7 on average, and 3.89 with the 10 swapped for an 18.')),
      'coinage ' + i + ': over the tiles a line names the coins chosen and the range; the sentence about American coins is there "for comparison" when other coins are chosen (a visitor read its 4.7 as the average of the coins chosen)');""")
    rep("must(sayB.includes('For the fewest coins the best coin to add is ' + nm(bp) + ', bringing the average '", "must(sayB.includes('Paying exactly, the best coin to add is ' + nm(bp) + ', bringing the average '")
    rep("&& !/cost|one way|both ways|greedy/i.test(sayB),", "&& !/cost|one way|both ways|greedy|fewest/i.test(sayB),")
    rep("""console.log(`coinage ${i} (${c.join(',')}; below ${L}): ${t[0].v} | ${t[1].v} | ${t[2].v}; add ${bp.map(e => e.coin).join('/')} for the fewest coins,""", """console.log(`coinage ${i} (${c.join(',')}; below ${L}): ${t[0].v} | ${t[1].v} | ${t[2].v}; add ${bp.map(e => e.coin).join('/')} for paying exactly,""")
    rep("&& ph.startsWith('Fewest coins: ') : pw.length === 0 && ph.includes('cannot be paid exactly');", "&& ph.startsWith('Paid exactly: ') : pw.length === 0 && ph.includes('it cannot be');")
    rep("const okSchemes = shown.length === Math.min(12, s.total) &&", "const ors = await count('#way-both .or'); const okSchemes = ors === Math.max(0, Math.min(12, s.total) - 1) && shown.length === Math.min(12, s.total) &&")
    rep("'paying an amount: the coins drawn are the ways pcore lists, for ' + n + ' amounts in six coinages (' + good + ' right)');", "'paying an amount: the coins drawn are the ways pcore lists, for ' + n + ' amounts in six coinages, with \"or\" between one way of paying with change and the next (a visitor read two ways as one long transaction) (' + good + ' right)');")
    rep("tip.includes('fewest coins 2 (2 × 24)')", "tip.includes('paid exactly 2 (2 × 24)')")
    rep("tip10.includes('fewest coins ' + P.plain(PRE[4][0], 11)[10] + ' (')", "tip10.includes('paid exactly ' + P.plain(PRE[4][0], 11)[10] + ' (')")
    rep("must(tipB.includes('With a coin of 73 added: fewest coins ' + P.meanText(t73, L, 3)", "must(tipB.includes('With a coin of 73 added: paying exactly ' + P.meanText(t73, L, 3)")
    rep("must(sb.startsWith('With a coin of 73 added: fewest coins ' + P.meanText(t73, L, 3)", "must(sb.startsWith('With a coin of 73 added: paying exactly ' + P.meanText(t73, L, 3)")
    rep("&& !tip300.includes('fewest coins'), 'a coin larger", "&& !tip300.includes('paying exactly'), 'a coin larger")
    rep("""  { await p.selectOption('#preset', EURO); await p.waitForTimeout(100); await p.click('#addPlain');""", """  { await p.selectOption('#preset', US); await p.waitForTimeout(100); const labs = await p.evaluate(() => [document.getElementById('addPlain').textContent, document.getElementById('addBoth').textContent]);
    must(labs[0] === 'Add a 32: the best coin for paying exactly' && labs[1] === 'Add a 48: the best coin for paying with change', 'each button that adds a coin says which coin it will add (a visitor: where several tie "the button adds the first without saying which")', labs.join(' | '));
    await p.selectOption('#preset', EURO); await p.waitForTimeout(100); await p.click('#addPlain');""")
    rep("and the average with the fewest coins has gone from 3.4 to 2.86.', 'adding the best coin for the fewest coins to the euro", "and the average paying exactly has gone from 3.4 to 2.86.', 'adding the best coin for paying exactly to the euro")
    rep("and the average with change has gone from 3.98 to 2.95.', 'adding", "and the average paying with change has gone from 3.98 to 2.95.', 'adding")
    rep("""(await p.evaluate(() => document.getElementById('addBoth').disabled)) && sb.startsWith('There are 16 coins, which is as many as this page takes, so no more can be added.') && !/( or \\d+){6}/.test(sb),""",
        """(await p.evaluate(() => document.getElementById('addBoth').disabled && getComputedStyle(document.getElementById('addBoth')).display === 'none')) && sb === 'There are 16 coins, which is as many as this page takes, so no more can be added.' && (await text('#addPlain')) === 'No coin can be added: 16 is as many as this page takes',""")
    rep("""'twelve presses bring the US coins to sixteen; both buttons then stop, and the page says why; a long list of equally good coins is given as its first four and how many more (a visitor met grey buttons with no word, over thirteen lines of "or")',""",
        """'twelve presses bring the US coins to sixteen; the button then says, where it is pressed, that no coin can be added and why, the other button goes, and the sentence under the picture says the same and names no best coin (a visitor met grey buttons with no word, a screen above the reason, over thirteen lines of "or")',""")
    rep("(await text('#sayB')).includes('For the fewest coins the best coin to add is 1,'), 'coins 2 and 4:", "(await text('#sayB')).includes('Paying exactly, the best coin to add is 1,'), 'coins 2 and 4:")
    rep("(await text('#sayB')).includes('For the fewest coins there is no coin left to try'), 'the smallest case,", "(await text('#sayB')).includes('Paying exactly there is no coin left to try'), 'the smallest case,")
    rep("must(sb.includes('For the fewest coins there is no coin left to try') && sb.includes('With change no single coin up to 5", "must(sb.includes('Paying exactly there is no coin left to try') && sb.includes('With change no single coin up to 5")
    rep("must(sb.includes('For the fewest coins there is no coin left to try') && sb.includes('With change no single coin up to 3", "must(sb.includes('Paying exactly there is no coin left to try') && sb.includes('With change no single coin up to 3")
    rep("must(sb.includes('For the fewest coins the best coin to add is 1, bringing the average to')", "must(sb.includes('Paying exactly, the best coin to add is 1, bringing the average to')")
    rep("tt[1].d.includes('The fewest for every amount here, but not for 30: 25 + 5 × 1 against 3 × 10')", "tt[1].d.includes('No more than need be for any amount here, but for 30: 25 + 5 × 1 against 3 × 10')")
    rep("""      await p.fill('#amount', '100'); await p.waitForTimeout(40); if ((await p.inputValue('#amount')) === '99') good++;
      await p.fill('#amount', '41');""", """      await p.fill('#amount', '100'); await p.waitForTimeout(40); if ((await p.inputValue('#amount')) === '99' && (await text('#amountSay')) === '100 is more than 99, the largest amount here: the amount is 99.') good++;
      await p.fill('#amount', '41');""")
    rep("""100 becomes 99; a good amount clears the sentence (' + good + ' of 4)'""", """100 becomes 99, and the page says that too; a good amount clears the sentence (' + good + ' of 4)'""")
    rep("heads.every(h => h === 'coins|the best sets|average|least possible')", "heads.every(h => h === 'coins in the set|the best sets|average|cannot be below')")
    # the story of the 18, which follows the coins chosen
    i = s.index("    must(mt(us, 'plain') === '4.7' && mt(sh, 'plain') === '3.89'"); j = s.index("    const words = await p.evaluate(() => document.querySelector('main').innerText);", i)
    s = s[:i] + r"""    await p.selectOption('#preset', US); await p.waitForTimeout(80); const st0 = await text('#story');
    must(mt(us, 'plain') === '4.7' && mt(sh, 'plain') === '3.89' && mt(sh, 'greedy') === '4.58' && cap === 'Count every amount once, and take the average number of coins it takes.'
      && st0 === 'American coins take 4.7 on average. Swap the 10 for an 18 and it is 3.89, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, would need 4.58 with those coins.',
      'the sentence over the averages is so by pcore: 4.7 for American coins, 3.89 with an 18 for the 10, and 4.58 the cashier\'s way with those (a visitor: the page "never puts 4.7 beside 3.89", and never said the cashier\'s catch in words)');
    await p.click('#story button'); await p.waitForTimeout(120); const t = await tiles(), st1 = await text('#story');
    must((await p.inputValue('#coins')) === '1, 5, 18, 25' && (await p.inputValue('#preset')) === '1' && t[0].v === '3.89' && t[1].v === '4.58' && t[1].d.includes('first at 28: 25 + 3 × 1 against 18 + 2 × 5')
      && st1 === 'These are the American coins with the 10 swapped for an 18: 3.89 on average where American coins take 4.7, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, needs 4.58 with these. Put the 10 back',
      '"Swap the 10 for an 18" is a button in that sentence: pressed, the coins are 1, 5, 18, 25, the tiles beneath read 3.89 and 4.58, and the sentence is now about these coins');
    await p.click('#story button'); await p.waitForTimeout(120); const st2 = await text('#story'), hb = await p.evaluate(() => document.querySelector('#story button').getBoundingClientRect().height);
    must((await p.inputValue('#coins')) === '1, 5, 10, 25' && (await p.inputValue('#preset')) === US && st2 === st0 && hb >= 32, '   ... and "Put the 10 back" puts it back (a visitor pressed the button a second time: "nothing, and nothing said"); the button is 32 px tall or more and looks like the page\'s other buttons, not like a link', hb.toFixed(0) + ' px');
    await p.selectOption('#preset', EURO); await p.waitForTimeout(100); await p.click('#story button'); await p.waitForTimeout(120);
    must((await p.inputValue('#coins')) === '1, 5, 10, 25' && (await text('#story button')) === 'Swap the 10 for an 18', '   ... with other coins chosen the button reads "Try the American coins", and does that');
""" + s[j:]
    rep("""    must(!/\\bone way\\b|\\bboth ways\\b|\\bgreedy\\b|\\bcost\\b|\\bbound\\b|OEIS|Settle/i.test(words) && /Fewest coins/.test(words) && /The cashier's way/.test(words) && /With change/.test(words),
      'the page\\'s names for its three counts are "fewest coins", "the cashier\\'s way" and "with change"; "one way", "both ways", "greedy", "cost" and "bound" are gone from it (a visitor read "One way" as "the first way" and "Both ways" as "both of the ways above")'); }""",
        """    must(!/\\bone way\\b|\\bboth ways\\b|\\bgreedy\\b|\\bcost\\b|\\bbound\\b|OEIS|Settle|fewest coins|least possible/i.test(words) && /Paying exactly/.test(words) && /Paid exactly: /.test(words) && /The cashier's way/.test(words) && /Paying with change/.test(words),
      'the page\\'s names for its three counts are "paying exactly", "the cashier\\'s way" and "paying with change"; "one way", "both ways", "greedy", "cost", "bound" and "least possible" are gone from it, and so is "fewest coins", which stood above a smaller number (a visitor read "One way" as "the first way" and "Both ways" as "both of the ways above"; and, of the first remake, \\'"Fewest coins" is not the fewest\\')'); }""")
    rep("must(Math.abs(a - want) <= 1 && a !== 24 && sayA.startsWith('Amount ' + a + ': fewest coins ' + P.plain([1, 5, 10, 25], 100)[a] + ' (')", "must(Math.abs(a - want) <= 1 && a !== 24 && sayA.startsWith('Amount ' + a + ': paid exactly ' + P.plain([1, 5, 10, 25], 100)[a] + ' (')")
    rep(r"""m = /^With a coin of (\d+) added: fewest coins ([\d.]+); with change ([\d.]+)\./.exec(sb)""", r"""m = /^With a coin of (\d+) added: paying exactly ([\d.]+); with change ([\d.]+)\./.exec(sb)""")
    rep("must(said === 'Added a 32. The coins are now 1, 5, 10, 25, 32, and the average with the fewest coins has gone from 4.7 to 3.46.' && Math.abs(y1 - y0) < 1 && vis, 'on a phone \"Add the best coin for the fewest coins\" says,",
        "must(said === 'Added a 32. The coins are now 1, 5, 10, 25, 32, and the average paying exactly has gone from 4.7 to 3.46.' && Math.abs(y1 - y0) < 1 && vis, 'on a phone \"Add a 32: the best coin for paying exactly\" says,")
    rep("""    const words = await p.evaluate(() => document.querySelector('main').innerText);""", """    await p.selectOption('#preset', US); await p.waitForTimeout(80); await p.fill('#amount', '71'); await p.waitForTimeout(60); const s71 = await text('#sayA');
    must(P.plain([1, 5, 10, 25], 100)[71] === 5 && P.both([1, 5, 10, 25], 100)[71] === 5 && s71 === 'Amount 71: paid exactly 5 (2 × 25 + 2 × 10 + 1); with change 5 (no fewer).', 'where change saves nothing the sentence says "no fewer" and shows no way with change (a visitor at 71 cents: "with change 5 (3 × 25 + 1 handed over, 5 handed back) when five coins paid exactly would do. So what?")', s71);
    const words = await p.evaluate(() => document.querySelector('main').innerText);""")
    open(H + 'tools/shot-change.js', 'w', encoding='utf8').write(s); print('tools/shot-change.js, third stage:', len(s))

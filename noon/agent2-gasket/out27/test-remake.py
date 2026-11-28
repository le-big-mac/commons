"""The gasket page's test brought to the page as remade on 27 November (stages 1 and 2).   python -I out27/test-remake.py [FILE]
(made from out27/shot-gasket.stage0.js.txt, so that it can be run again; FILE is the test to write, tools/shot-gasket.js if not given)"""
import sys
H = '/home/agent2/gasket/'
if __name__ == '__main__':
    P = sys.argv[1] if len(sys.argv) > 1 else H + 'tools/shot-gasket.js'; s = open(H + 'out27/shot-gasket.stage0.js.txt', encoding='utf8').read()
    def rep(a, b):
        global s
        assert s.count(a) == 1, (a[:100], s.count(a)); s = s.replace(a, b)
    # the third panel no longer speaks of the sign; the sign is still checked, in the program, and the families that follow from it on the page
    rep("""  must((await text('#tsay')).includes('its sign (the paper’s χ2) is −1') && (await text('#tsay')).includes('n² or 3n²'), 'the third panel on (-11, 21, 24, 28)');""",
        """  must(G.type([-11, 21, 24, 28]).chi2 === -1 && (await text('#tsay')).includes('Its numbers leave ' + G.type([-11, 21, 24, 28]).res.join(', ') + ' on division by 24.') && (await text('#tsay')).includes('n² or 3n²') && !/sign|χ/.test(await text('#tsay')),
    'the third panel on (-11, 21, 24, 28): the remainders and the two barred families, with no word of the sign they follow from (a visitor: "What? Nothing is done with it."), which is −1 in the program');""")
    # ---- what the remake added, at desk size
    rep("""  must(errs.length === 0, 'no error on the page');""", """  // ================= the page as remade on 27 November 2026 =================
  const fresh = await b.newPage({ viewport: { width: 1100, height: 1900 } }); const ferrs = []; fresh.on('pageerror', e => ferrs.push(String(e))); await fresh.goto('file://' + page); await fresh.waitForTimeout(700);
  const ftext = sel => fresh.evaluate(q => document.querySelector(q).textContent.replace(/\\s+/g, ' ').trim(), sel), fstate = () => fresh.evaluate(() => ({ view: window.GasketPage.view(), root: window.GasketPage.pack().root.join(','), size: window.GasketPage.size(), chosen: window.GasketPage.chosen(), drawn: window.GasketPage.drawn() }));
  const lit = async () => Number(((await ftext('#gsay')).match(/, ([\\d,]+) of them/) || [0, '-1'])[1].replace(/,/g, ''));
  { const st = await fstate(), story = await ftext('#gstory'), lead = await ftext('#lead');
    must(st.root === '-4,5,20,21' && (await fresh.inputValue('#hi')) === '1' && (await fresh.inputValue('#pack')) === '1' && (await lit()) > 0 && st.drawn.filter(c => c[0] === 36).length === 2 &&
      lead === 'Each circle is marked with a whole number: the smaller the circle, the bigger its number. Squares are lit in orange.' && story.startsWith('In this gasket squares turn up: the two largest orange circles are marked 36, which is 6 × 6.') && story.endsWith('Show a gasket with no square in it'),
      'the page opens on the gasket (−4, 5, 20, 21) with its squares lit, two of them marked 36, under two plain sentences, and the sentence under the picture says so and offers the other gasket (a visitor: "The first thing a visitor sees shows an absence")', story.slice(0, 80) + ' | ' + st.root + ' | ' + (await lit()));
    const order = await fresh.evaluate(() => { const y = id => document.getElementById(id).getBoundingClientRect().top; return [y('lead'), y('g'), y('gstory'), y('zin'), y('gpick'), y('pack'), y('gsay'), y('about'), y('chart')]; });
    must(order.every((v, k) => k === 0 || v > order[k - 1]), 'in order down the page: the two sentences, the picture, its sentence and button, the buttons that magnify, the line for a chosen circle, the two menus, the count, what is going on, the second picture', JSON.stringify(order.map(Math.round)));
    await fresh.click('#swap'); await fresh.waitForTimeout(300); const s2 = await fstate(), story2 = await ftext('#gstory');
    must(s2.root === '-3,5,8,8' && (await lit()) === 0 && (await fresh.inputValue('#pack')) === '0' && story2.startsWith('In this gasket nothing is lit, and nothing will be, however far you magnify: no square is the number of any of its circles. That was proved in 2023') && story2.endsWith('Back to the gasket with squares'),
      'the button under the picture shows (−3, 5, 8, 8), where no square is lit, and the sentence says that none ever will be', story2.slice(0, 60) + ' | ' + s2.root);
    await fresh.selectOption('#hi', '6'); await fresh.waitForTimeout(200); const story3 = await ftext('#gstory'); await fresh.click('#swap'); await fresh.waitForTimeout(300); const s4 = await fstate();
    must(story3 === 'Back to the gasket with squares' && s4.root === '-4,5,20,21' && (await fresh.inputValue('#hi')) === '1' && (await lit()) > 0, 'with something else lit the sentence is only the button, which goes back to the gasket with squares and lights the squares again', story3 + ' | ' + s4.root);
    const about = await ftext('#about');
    must(about.includes('A gasket is named here by its four largest circles, as (−4, 5, 20, 21). The number with the minus is the circle round all the rest.') && about.includes('only numbers that leave 0, 5, 8, 12, 20 or 21 are ever a circle\\'s number. 36 leaves 12, so it passes that test') &&
      G.type([-4, 5, 20, 21]).res.join() === '0,5,8,12,20,21' && G.type([-3, 5, 8, 8]).res.join() === '0,5,8,12,20,21' && 36 % 24 === 12 && (G.type([-3, 5, 8, 8]).quad || []).join() === '1,6' && (G.type([-4, 5, 20, 21]).quad || []).join() === '2,3' &&
      about.includes('In (−3, 5, 8, 8) it is the squares, and the numbers six times a square; in (−4, 5, 20, 21) it is the numbers twice a square and three times a square.'),
      'what is going on, under the picture: how a gasket is named, the test of what is left on division by 24 with 36 as its example, and the families that the two gaskets lack, each as the program has it (a visitor: "the test of remainders" was never explained; "(−3, 5, 8, 8)" was a name nobody had introduced)');
    const all = await fresh.evaluate(() => document.querySelector('main').innerText);
    must(!/the paper proves|the paper’s χ|its sign|Scroll or use the buttons/.test(all) && all.includes('it is proved (Haag, Kertzer, Rickards and Stange, 2023)') === false || true, 'placeholder'); asserts--; }
  // a click chooses a circle; the line under the picture says what its number is; Magnify closes in on a small one
  { const st = await fstate(), c36 = st.drawn.filter(c => c[0] === 36)[0], v = st.view, box = await fresh.locator('#g').boundingBox(), k = box.width / st.size.W;
    const px = c => [box.x + k * (st.size.W / 2 + (c[1] / c[0] - v.cx) * v.s), box.y + k * (st.size.H / 2 - (c[2] / c[0] - v.cy) * v.s)]; const at36 = px(c36);
    await fresh.mouse.click(at36[0], at36[1]); await fresh.waitForTimeout(200); const pick = await ftext('#gpick'), ch = (await fstate()).chosen;
    must(ch && ch[0] === 36 && pick === 'The circle marked 36. 36 = 6 × 6, a square. Divided by 24 it leaves 12. “Magnify” now closes in on this circle.', 'a click on a circle marked 36 chooses it, and the line under the picture says: 36 = 6 × 6, a square, and what it leaves on division by 24 (a visitor: a tap on a circle did nothing)', pick);
    await fresh.click('#zin'); await fresh.waitForTimeout(250); const s5 = await fstate(), v5 = s5.view, now = [box.x + k * (s5.size.W / 2 + (c36[1] / c36[0] - v5.cx) * v5.s), box.y + k * (s5.size.H / 2 - (c36[2] / c36[0] - v5.cy) * v5.s)];
    must(Math.abs(v5.s / v.s - 2) < 1e-9 && Math.abs(now[0] - at36[0]) < 0.01 && Math.abs(now[1] - at36[1]) < 0.01 && s5.drawn.some(c => c[0] === 36), 'Magnify then doubles the picture about the chosen circle, which stays where it was (a visitor: three presses gave an empty picture)', JSON.stringify([v5.s / v.s, now, at36]));
    await fresh.click('#home'); await fresh.waitForTimeout(250); const s6 = await fstate(), big = s6.drawn.filter(c => c[0] > 0).sort((a, b) => a[0] - b[0])[0], v6 = s6.view;
    await fresh.mouse.click(box.x + k * (s6.size.W / 2 + (big[1] / big[0] - v6.cx) * v6.s), box.y + k * (s6.size.H / 2 - (big[2] / big[0] - v6.cy) * v6.s)); await fresh.waitForTimeout(200); const pick2 = await ftext('#gpick');
    await fresh.click('#zin'); await fresh.waitForTimeout(250); const v7 = (await fstate()).view;
    must(pick2.startsWith('The circle marked ' + big[0] + '.') && pick2.endsWith('Choose a small circle, and “Magnify” closes in on it.') && Math.abs(v7.cx - v6.cx) < 1e-12 && Math.abs(v7.cy - v6.cy) < 1e-12 && Math.abs(v7.s / v6.s - 2) < 1e-9, 'with the largest circle chosen the line says to choose a small one, and Magnify doubles the picture about its middle as before', pick2);
    await fresh.click('#home'); await fresh.waitForTimeout(200); for (let i = 0; i < 3; i++) { await fresh.click('#zout'); await fresh.waitForTimeout(150); } const back = await ftext('#gsay');
    await fresh.evaluate(() => { const v = window.GasketPage.view(); window.GasketPage.setView(v.cx + 5000 / v.s, v.cy, v.s); }); await fresh.waitForTimeout(200); const gone = await ftext('#gsay');
    must(back.includes('Drawn back 8 times.') && !/Magnified 0\\./.test(back) && gone.includes('0 circles drawn') && gone.includes('Nothing of the gasket is in view: “The whole gasket” brings it back.'), 'drawn back three times the count says "Drawn back 8 times", and with the gasket out of the frame it says how to bring it back (a visitor: "Magnified 0.125 times"; a thumb threw the gasket away)', back.slice(0, 90) + ' | ' + gone.slice(0, 120));
    await fresh.click('#home'); await fresh.waitForTimeout(200); }
  // the two tables say whether they show or hide; the third panel: the list on request, and "Draw it above" reads the box
  { const n0 = [await ftext('#gtab'), await ftext('#ctab')]; await fresh.click('#gtab'); await fresh.click('#ctab'); const n1 = [await ftext('#gtab'), await ftext('#ctab')]; await fresh.click('#gtab'); await fresh.click('#ctab');
    must(n0.join() === 'Show the table,Show the list' && n1.join() === 'Hide the table,Hide the list' && (await ftext('#gtab')) === 'Show the table', 'the two buttons that open a table and a list say "Show" and then "Hide" (a visitor: neither changed its name, and the second opens a list)', n0 + ' | ' + n1);
    const listShown = () => fresh.evaluate(() => getComputedStyle(document.getElementById('tnums')).display !== 'none' && document.getElementById('tnums').getBoundingClientRect().height > 0);
    const l0 = await listShown(), b0 = await ftext('#tlist'); await fresh.click('#tlist'); const l1 = await listShown(), b1 = await ftext('#tlist'); await fresh.click('#tlist');
    must(!l0 && l1 && b0.startsWith('Show the list of the missing numbers') && b1.startsWith('Hide the list of the missing numbers') && !(await listShown()), 'the third panel keeps its list of missing numbers folded until it is asked for (a visitor: a list 1,861 px tall before the foot)', b0 + ' | ' + b1);
    await fresh.fill('#quad', '-6, 11, 14, 15'); await fresh.click('#show'); await fresh.waitForTimeout(600); const drew = (await fstate()).root;
    await fresh.fill('#quad', '1, 2, 3, 4'); await fresh.click('#show'); await fresh.waitForTimeout(400); const refused = (await fstate()).root, said = await ftext('#tsay');
    must(drew === '-6,11,14,15' && refused === '-6,11,14,15' && said.includes('do not satisfy Descartes'), '"Draw it above" reads the box: with −6, 11, 14, 15 typed and "Look" not pressed it draws that gasket, and with 1, 2, 3, 4 it says why not and draws nothing new (a visitor: it drew the gasket last looked at)', drew + ' | ' + refused + ' | ' + said.slice(0, 60)); }
  must(ferrs.length === 0, 'no error on the page in all of this', ferrs.join(' ; ')); await fresh.close();
  must(errs.length === 0, 'no error on the page');""")
    # the helper "must" takes a third thing to show when an assertion fails
    rep("""const fails = []; let asserts = 0; const must = (cond, what) => { asserts++; if (!cond) fails.push(what); };""", """const fails = []; let asserts = 0; const must = (cond, what, ev) => { asserts++; if (!cond) fails.push(what + (ev ? '   [' + ev + ']' : '')); };""")
    s = s.replace("""    const all = await fresh.evaluate(() => document.querySelector('main').innerText);
    must(!/the paper proves|the paper’s χ|its sign|Scroll or use the buttons/.test(all) && all.includes('it is proved (Haag, Kertzer, Rickards and Stange, 2023)') === false || true, 'placeholder'); asserts--; }""",
        """    const all = await fresh.evaluate(() => document.querySelector('main').innerText);
    must(!/the paper proves|χ|its sign|Scroll or use the buttons|curvatures leave the remainders/.test(all) && all.includes('With fingers: pinch to magnify, drag sideways to move.'), 'gone from the page: "the paper proves" before any paper is named, the sign, "Scroll or use the buttons to magnify"; and it says how fingers work the picture'); }""")
    # a test that stops must still say what it had found
    rep("""const fails = []; let asserts = 0; const must = (cond, what, ev) => { asserts++; if (!cond) fails.push(what + (ev ? '   [' + ev + ']' : '')); };""",
        """const fails = []; let asserts = 0; const must = (cond, what, ev) => { asserts++; if (!cond) fails.push(what + (ev ? '   [' + ev + ']' : '')); };
  process.on('unhandledRejection', e => { console.log('THE TEST STOPPED after ' + asserts + ' assertions, ' + fails.length + ' of them failed' + (fails.length ? ': ' + fails.join(' | ') : '') + '; it stopped at: ' + String((e && e.message) || e).split('\\n')[0].slice(0, 160)); b.close().catch(() => 0).then(() => process.exit(2)); });""")
    open(P, 'w', encoding='utf8').write(s); print('test: the page as remade (stages 1 and 2), at desk size')

// Headless checks of the page "Small change": what it shows against pcore.js run here in node.
// usage: node shot-change.js PAGE.html OUTDIR PCORE.js      (run from ~/web, where playwright is)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])]; const P = require(path.resolve(process.argv[4]));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(400);
  const text = sel => p.evaluate(s => document.querySelector(s).textContent, sel), count = sel => p.evaluate(s => document.querySelectorAll(s).length, sel);
  const fails = []; let asserts = 0; const must = (cond, what) => { asserts++; if (!cond) fails.push(what); };
  const tiles = () => p.evaluate(() => [...document.querySelectorAll('.tile')].map(t => ({ v: t.querySelector('.v').textContent, d: t.querySelector('.d').textContent })));
  const setCoins = async (coins, L) => { await p.fill('#coins', coins); await p.fill('#L', String(L)); await p.click('#apply'); await p.waitForTimeout(80); };
  const fin = v => v < P.INF, BOX = { l: 44, r: 112, t: 26, b: 34 };
  const PRE = [[[1, 2, 5, 10, 20, 50, 100, 200], 100], [[1, 5, 10, 25], 100], [[1, 5, 10, 25, 50, 100], 100], [[1, 5, 18, 25], 100], [[1, 3, 6, 12, 24, 30], 240], [[1, 5, 10, 25, 100, 200], 500],
    [[1, 2, 4, 8, 16, 32, 64], 100], [[1, 3, 9, 27, 81], 100], [[16, 19, 21], 100], [[19, 20, 23, 32], 100], [[1, 5, 16, 23, 33], 100]];
  // read a drawn line back into numbers, using nothing but the picture: the tick labels give the scales
  const readLine = async (chart, line) => {
    const g = await p.evaluate(([chart, line]) => { const svg = document.getElementById(chart), T = [...svg.querySelectorAll('text')];
      return { yt: T.filter(t => t.getAttribute('text-anchor') === 'end').map(t => [Number(t.textContent), Number(t.getAttribute('y')) - 4]),
        xt: T.filter(t => t.getAttribute('text-anchor') === 'middle' && /^\d+$/.test(t.textContent)).map(t => [Number(t.textContent), Number(t.getAttribute('x'))]),
        d: document.getElementById(line).getAttribute('d'), box: (() => { const q = document.getElementById(line).getBBox(); return [q.x, q.y, q.x + q.width, q.y + q.height]; })(),
        marks: [...svg.querySelectorAll('circle')].map(c => [Number(c.getAttribute('cx')), Number(c.getAttribute('cy'))]),
        labels: T.map(t => { const q = t.getBBox(); return [q.x, q.x + q.width, q.y, q.y + q.height]; }) }; }, [chart, line]);
    const lin = (pts) => { const [a, c] = [pts[0], pts[pts.length - 1]]; const k = (c[0] - a[0]) / (c[1] - a[1]); return v => a[0] + (v - a[1]) * k; };
    const yv = lin(g.yt), xv = lin(g.xt), vals = new Map(); let x = 0, y = 0;
    for (const m of g.d.matchAll(/([MVH])([^MVH]*)/g)) { const n = m[2].split(',').map(Number);
      if (m[1] === 'M') { x = n[0]; y = n[1]; } else if (m[1] === 'V') y = n[0]; else { vals.set(Math.round(xv((x + n[0]) / 2)), yv(y)); x = n[0]; } }
    const inside = g.box[0] >= BOX.l - 1 && g.box[2] <= 1000 - BOX.r + 1 && g.box[1] >= BOX.t - 1 && g.box[3] <= 300 - BOX.b + 1;
    const marksIn = g.marks.every(m => m[0] >= BOX.l - 1 && m[0] <= 1000 - BOX.r + 1 && m[1] >= BOX.t - 6 && m[1] <= 300 - BOX.b + 1);
    const labelsIn = g.labels.every(l => l[0] >= -0.5 && l[1] <= 1000.5 && l[2] >= -0.5 && l[3] <= 300.5);
    return { vals, inside, marksIn, labelsIn, marks: g.marks, xv, yv }; };

  must((await count('#preset option')) === 12, 'eleven coinages to choose from, and "your own"');
  // every coinage offered: tiles, both pictures and both tables are what pcore gives
  for (let i = 0; i < PRE.length; i++) {
    const [c, L] = PRE[i]; await p.selectOption('#preset', String(i)); await p.waitForTimeout(L > 300 ? 250 : 100);
    const pl = P.plain(c, L), gr = P.greedy(c, L), bo = P.both(c, L), tp = P.total(pl), tg = P.total(gr), tb = P.total(bo), t = await tiles(), D = c.length;
    must((await p.inputValue('#coins')) === c.join(', ') && (await p.inputValue('#L')) === String(L), 'coinage ' + i + ': the coins and the range are shown in the boxes');
    if (isFinite(tp)) must(t[0].v === P.meanText(tp, L, 3) && t[0].d.includes(P.worst(pl) + ' at worst') && t[0].d.includes('No set of ' + D + ' coins could cost less than ' + P.meanText(P.bound(D, L, 'plain'), L, 3) + '.'), 'coinage ' + i + ': the one-way tile');
    else must(t[0].v === 'cannot make ' + [...pl].filter(v => !fin(v)).length + ' amounts' && t[0].d.includes('no coin of 1'), 'coinage ' + i + ': the one-way tile says what cannot be made');
    if (c[0] === 1) { const pf = P.pearson(c), gf = P.greedyFails(c, L);
      must(t[1].v === P.meanText(tg, L, 3) && (pf === 0 ? t[1].d.startsWith('Always the fewest coins') && gf.length === 0 : gf.length ? t[1].d.includes('for ' + gf.length + ' amount') && t[1].d.includes('first at ' + gf[0] + ':') : t[1].d.includes('but not for ' + pf + ':')), 'coinage ' + i + ': the greedy tile'); }
    else must(t[1].v === 'gets stuck at ' + [...gr].filter(v => !fin(v)).length + ' amounts', 'coinage ' + i + ': the greedy tile says where it gets stuck');
    must(t[2].v === P.meanText(tb, L, 3) && t[2].d.includes(P.worst(bo) + ' at worst') && t[2].d.includes('could cost less than ' + P.meanText(P.bound(D, L, 'both'), L, 3) + '.'), 'coinage ' + i + ': the both-ways tile');
    // picture A
    const A1 = await readLine('chartA', 'lineA-plain'), A2 = await readLine('chartA', 'lineA-both'); let good = 0;
    for (let a = 0; a < L; a++) { const v1 = A1.vals.get(a), v2 = A2.vals.get(a); if ((fin(pl[a]) ? Math.abs(v1 - pl[a]) < 0.02 : v1 === undefined) && (fin(bo[a]) ? Math.abs(v2 - bo[a]) < 0.02 : v2 === undefined)) good++; }
    must(good === L, 'coinage ' + i + ': both lines of the first picture, read back from the drawing, are the counts for every amount (' + good + ' of ' + L + ')');
    must(A1.inside && A2.inside && A1.marksIn && A1.labelsIn, 'coinage ' + i + ': the first picture stays in its frame');
    const gf = c[0] === 1 ? P.greedyFails(c, L) : [];
    must((await count('#chartA .failmark')) === gf.length && gf.every((a, k) => Math.abs(A1.xv(A1.marks[k][0]) - a) < 0.3 && Math.abs(A1.yv(A1.marks[k][1]) - gr[a]) < 0.02), 'coinage ' + i + ': a ring at every amount where greedy takes more, at greedy\'s count');
    // table A
    const rows = await p.evaluate(() => [...document.querySelectorAll('#tabA tr')].slice(1).map(tr => [...tr.children].map(td => td.textContent))); const cell = v => fin(v) ? String(v) : 'cannot';
    must(rows.length === L && rows.every((r, a) => r[0] === String(a) && r[1] === cell(pl[a]) && r[2] === cell(gr[a]) && r[3] === cell(bo[a])), 'coinage ' + i + ': the table of counts');
    // picture B and its sentence
    const ap = P.bestAdd(c, L, 'plain', L - 1), ab = P.bestAdd(c, L, 'both', 2 * L - 1), bp = ap.filter(e => e.total === ap[0].total && isFinite(e.total)), bb = ab.filter(e => e.total === ab[0].total && isFinite(e.total));
    const sayB = await text('#sayB');
    must(sayB.includes('One way the best coin to add is ' + bp.map(e => e.coin).join(' or ') + ', bringing the cost ' + (isFinite(tp) ? 'from ' + P.meanText(tp, L, 3) + ' ' : '') + 'to ' + P.meanText(bp[0].total, L, 3) + '.') &&
      sayB.includes('Both ways it is ' + bb.map(e => e.coin).join(' or ') + ', ' + (isFinite(tb) ? 'from ' + P.meanText(tb, L, 3) + ' ' : '') + 'to ' + P.meanText(bb[0].total, L, 3) + '.'), 'coinage ' + i + ': the sentence under the second picture names the best coins and their costs');
    const B1 = await readLine('chartB', 'lineB-plain'), B2 = await readLine('chartB', 'lineB-both'); good = 0; let n = 0;
    for (const e of ap) { n++; const v = B1.vals.get(e.coin); if (isFinite(e.total) ? Math.abs(v - e.total / L) < 0.004 : v === undefined) good++; }
    for (const e of ab) { n++; const v = B2.vals.get(e.coin); if (isFinite(e.total) ? Math.abs(v - e.total / L) < 0.004 : v === undefined) good++; }
    must(good === n && c.every(x => B2.vals.get(x) === undefined), 'coinage ' + i + ': both lines of the second picture, read back, are the costs with each coin added (' + good + ' of ' + n + ')');
    must(B1.inside && B2.inside && B1.marksIn && B1.labelsIn && (await count('#chartB .bestmark')) === bp.length + bb.length, 'coinage ' + i + ': the second picture stays in its frame and rings the best coins');
    const rowsB = await p.evaluate(() => [...document.querySelectorAll('#tabB tr')].slice(1).map(tr => [...tr.children].map(td => td.textContent)));
    const tb1 = new Map(ap.map(e => [e.coin, e.total])), tb2 = new Map(ab.map(e => [e.coin, e.total])), say = v => isFinite(v) ? P.meanText(v, L, 3) : 'cannot';
    must(rowsB.length === ab.length && rowsB.every(r => { const k = Number(r[0]); return r[2] === say(tb2.get(k)) && r[1] === (k > L - 1 ? '' : say(tb1.get(k))); }), 'coinage ' + i + ': the table of coins to add');
    console.log(`coinage ${i} (${c.join(',')}; below ${L}): ${t[0].v} | ${t[1].v} | ${t[2].v}; add ${bp.map(e => e.coin).join('/')} one way, ${bb.map(e => e.coin).join('/')} both ways; ${gf.length} greedy rings`);
  }
  // settle an amount: the coins drawn are the ways pcore lists
  const schemesShown = () => p.evaluate(() => [...document.querySelectorAll('#way-both .scheme')].map(r => ({ over: [...r.querySelectorAll('.coin.over')].map(c => Number(c.textContent)), back: [...r.querySelectorAll('.coin.back')].map(c => Number(c.textContent)) })));
  const sum = l => l.reduce((s, v) => s + v, 0);
  { let good = 0, n = 0;
    for (const [i, amounts] of [[0, [1, 8, 38, 49, 99, 73]], [4, [48, 50, 113, 239, 7]], [8, [1, 2, 10, 50, 99, 13]], [1, [30, 99, 68, 4]], [7, [5, 40, 77]], [5, [499, 83, 250]]]) {
      const [c, L] = PRE[i]; await p.selectOption('#preset', String(i)); await p.waitForTimeout(150);
      for (const a of amounts) { n++; await p.fill('#amount', String(a)); await p.waitForTimeout(30);
        const s = P.schemes(c, a, 100000), shown = await schemesShown(), head = await text('#way-both .k'), want = new Set(s.ways.map(w => JSON.stringify(w)));
        const asWay = r => { const m = new Map(); r.over.forEach(v => m.set(v, (m.get(v) || 0) + 1)); r.back.forEach(v => m.set(v, (m.get(v) || 0) - 1)); return JSON.stringify([...m.entries()].sort((x, y) => y[0] - x[0])); };
        const okSchemes = shown.length === Math.min(12, s.total) && shown.every(r => sum(r.over) - sum(r.back) === a && r.over.length + r.back.length === s.count && want.has(asWay(r))) && new Set(shown.map(asWay)).size === shown.length;
        const okHead = head.includes(s.count + ' coin') && head.includes('in ' + s.total + ' way') && (s.total > 12) === head.includes('the first 12 shown');
        const pw = await p.evaluate(() => [...document.querySelectorAll('#way-plain .coin')].map(c => Number(c.textContent))), pc = P.plain(c, a + 1)[a], ph = await text('#way-plain .k');
        const okPlain = fin(pc) ? sum(pw) === a && pw.length === pc && ph.includes(pc + ' coin') : pw.length === 0 && ph.includes('cannot be made');
        const gc = P.greedy(c, a + 1)[a], gh = (await count('#way-greedy')) ? await text('#way-greedy .k') : '', gw = await p.evaluate(() => [...document.querySelectorAll('#way-greedy .coin')].map(c => Number(c.textContent)));
        const okGreedy = !fin(pc) ? gh === '' : !fin(gc) ? gh.includes('gets stuck') : gc > pc ? gh.includes(gc + ' coin') && gh.includes((gc - pc) + ' more than need be') && sum(gw) === a && gw.length === gc : gh.includes('the same count');
        if (okSchemes && okHead && okPlain && okGreedy && (await p.inputValue('#amountR')) === String(a)) good++; else console.log('  settle: coinage ' + i + ' amount ' + a + ' wrong', okSchemes, okHead, okPlain, okGreedy, head); } }
    must(good === n, 'settling an amount: the coins drawn are the ways pcore lists, for ' + n + ' amounts in six coinages (' + good + ' right)'); console.log(`settle an amount: ${good} of ${n} right`);
    await p.selectOption('#preset', '0'); await p.fill('#amount', '0'); await p.waitForTimeout(30); must((await text('#ways')).includes('Nothing to settle') && (await count('#ways .coin')) === 0, 'amount 0: nothing to settle');
    await p.fill('#amount', '99'); await p.waitForTimeout(30); const s99 = await schemesShown(); must(s99.length === 1 && s99[0].over.join() === '100' && s99[0].back.join() === '1', '99 with the euro: a 100 handed over and a 1 handed back'); }
  // hover, click and keys on the first picture
  { await p.selectOption('#preset', '4'); await p.waitForTimeout(150); await p.locator('#chartA').scrollIntoViewIfNeeded(); const bx = await p.locator('#chartA').boundingBox(), L = 240;
    const sx = a => bx.x + (BOX.l + (a + 0.5) / L * (1000 - BOX.l - BOX.r)) / 1000 * bx.width;
    await p.mouse.move(sx(48), bx.y + bx.height / 2); await p.waitForTimeout(60); const tip = await text('#tipA'), vis = await p.evaluate(() => getComputedStyle(document.querySelector('#tipA')).display), sayA = await text('#sayA');
    must(vis === 'block' && tip.includes('Amount 48') && tip.includes('one way 2 (2 × 24)') && tip.includes('greedy 3 (30 + 12 + 6)') && sayA.includes('Amount 48') && sayA.includes('greedy 3'), 'hovering over 48 old pence: two florins against half-crown, shilling and sixpence');
    const tb = await p.locator('#tipA').boundingBox(), fb = await p.locator('#fig1').boundingBox(); must(tb.x >= fb.x && tb.x + tb.width <= fb.x + fb.width + 1, 'the tooltip stays inside its figure');
    await p.mouse.move(sx(10), bx.y + bx.height / 2); await p.waitForTimeout(60); const tip10 = await text('#tipA'); must(tip10.includes('Amount 10') && !tip10.includes('greedy') && tip10.includes('one way ' + P.plain(PRE[4][0], 11)[10] + ' (') && tip10.includes('both ways ' + P.both(PRE[4][0], 11)[10] + ' ('), 'where greedy takes no more, the tooltip does not speak of it');
    await p.mouse.move(sx(239), bx.y + bx.height / 2); await p.waitForTimeout(60); { const t2 = await p.locator('#tipA').boundingBox(); console.log('tooltip at the right edge: ' + Math.round(t2.width) + ' px wide'); must((await text('#tipA')).includes('Amount 239') && t2.x >= fb.x && t2.x + t2.width <= fb.x + fb.width + 1 && t2.width >= 200, 'at the right edge the tooltip still stays inside its figure, and is not squeezed'); }
    await p.mouse.click(sx(113), bx.y + bx.height / 2); await p.waitForTimeout(60); must((await p.inputValue('#amount')) === '113' && (await text('#way-greedy .k')).includes('1 more than need be'), 'a click on the picture settles that amount');
    const pick = await p.evaluate(() => Number(document.querySelector('#pickA').getAttribute('x1'))); must(Math.abs(pick - (BOX.l + 113.5 / L * (1000 - BOX.l - BOX.r))) < 0.5, 'the dotted line stands at the amount chosen');
    await p.mouse.move(5, 5); await p.locator('#chartA').focus(); await p.keyboard.press('ArrowRight'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(40); const k1 = await text('#sayA');
    await p.keyboard.press('Enter'); await p.waitForTimeout(40); must(k1.includes('Amount 115') && (await p.inputValue('#amount')) === '115', 'two presses of the right arrow and Enter move the amount by two');
    await p.locator('#chartB').scrollIntoViewIfNeeded(); const bb2 = await p.locator('#chartB').boundingBox(), n = 2 * L - 1, sxB = c => bb2.x + (BOX.l + (c - 0.5) / n * (1000 - BOX.l - BOX.r)) / 1000 * bb2.width;
    await p.mouse.move(sxB(73), bb2.y + bb2.height / 2); await p.waitForTimeout(60); const c = PRE[4][0], t73 = P.total(P.plain(c.concat([73]), L)), b73 = P.total(P.both(c.concat([73]), L)), tipB = await text('#tipB');
    must(tipB.includes('With a coin of 73: one way ' + P.meanText(t73, L, 3) + '; both ways ' + P.meanText(b73, L, 3) + '.'), 'hovering over 73 on the second picture gives the costs with a 73');
    await p.mouse.move(sxB(300), bb2.y + bb2.height / 2); await p.waitForTimeout(60); const tip300 = await text('#tipB'); must(tip300.includes('With a coin of 300: both ways') && !tip300.includes('one way'), 'a coin larger than every amount is priced both ways only');
    await p.mouse.move(sxB(24), bb2.y + bb2.height / 2); await p.waitForTimeout(60); must((await text('#tipB')).includes('A coin of 24 is already there'), 'a coin already there is said to be there');
    await p.mouse.move(5, 5);
    await p.selectOption('#preset', '0'); await p.waitForTimeout(100); await p.locator('#chartA').scrollIntoViewIfNeeded(); { const b0 = await p.locator('#chartA').boundingBox(); await p.mouse.move(b0.x + (BOX.l + 99.5 / 100 * (1000 - BOX.l - BOX.r)) / 1000 * b0.width, b0.y + b0.height / 2); await p.waitForTimeout(60);
      must((await text('#tipA')).includes('both ways 2 (100 handed over, 1 handed back)'), 'the tooltip at 99 with the euro: a 100 handed over, a 1 handed back'); await p.mouse.move(5, 5); }
    await p.selectOption('#preset', '4'); await p.waitForTimeout(150); await p.fill('#amount', '239'); await p.waitForTimeout(40); await p.selectOption('#preset', '0'); await p.waitForTimeout(120);
    must((await p.inputValue('#amount')) === '99' && (await p.inputValue('#amountR')) === '99' && (await text('#way-both .k')).includes('2 coins'), 'an amount beyond the new range is brought back inside it');
    console.log('hover, click, keys: done'); }
  // adding the best coin
  { await p.selectOption('#preset', '0'); await p.waitForTimeout(100); await p.click('#addPlain'); await p.waitForTimeout(120); const t = await tiles();
    must((await p.inputValue('#coins')) === '1, 2, 5, 10, 20, 33, 50, 100, 200' && (await p.inputValue('#preset')) === 'own' && t[0].v === '2.86', 'adding the best coin one way to the euro adds a 33 and the cost is 2.86');
    await p.selectOption('#preset', '1'); await p.waitForTimeout(100); await p.click('#addBoth'); await p.waitForTimeout(120); const t2 = await tiles();
    must((await p.inputValue('#coins')) === '1, 5, 10, 25, 48' && t2[2].v === '2.95', 'adding the best coin both ways to the US cents adds a 48 and the cost is 2.95'); }
  // coins of one's own, and what is refused
  { await setCoins('10 7 1', 30); let t = await tiles(); must(t[0].v === P.meanText(P.total(P.plain([1, 7, 10], 30)), 30, 3) && t[1].d.includes('for 6 amounts here, first at 14: 10 + 4 × 1 against 2 × 7') && (await p.inputValue('#coins')) === '1, 7, 10' && (await p.inputValue('#preset')) === 'own', 'coins typed in any order with spaces are taken: 1, 7, 10');
    await setCoins('1, 5, 10, 25', 100); must((await p.inputValue('#preset')) === '1', 'typing a listed coinage selects it in the list');
    await setCoins('1, 5, 10, 25', 50); must((await p.inputValue('#preset')) === 'own', 'the same coins with another range are your own');
    await setCoins('5, 1, 5, 10, 1', 100); must((await p.inputValue('#coins')) === '1, 5, 10' && (await tiles())[0].v === P.meanText(P.total(P.plain([1, 5, 10], 100)), 100, 3), 'a coin typed twice counts once');
    await setCoins('1, 10, 25', 30); { const tt = await tiles(); must(P.greedyFails([1, 10, 25], 30).length === 0 && P.pearson([1, 10, 25]) === 30 && tt[1].d.includes('The fewest for every amount here, but not for 30: 25 + 5 × 1 against 3 × 10') && (await count('#chartA .failmark')) === 0, 'greedy good for every amount drawn but not beyond: the tile says where it first fails'); }
    await setCoins('1, 5, 10, 25', 100);
    const before = JSON.stringify(await tiles()); let good = 0;
    for (const [c, L, word] of [['1, x, 5', 100, 'could not read'], ['0, 5', 100, 'between 1 and 5000'], ['1, 6000', 100, 'between 1 and 5000'], ['1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17', 100, 'At most 16'], ['', 100, 'at least one coin'], ['1, 5', 1, 'from 2 to 1000'], ['1, 5', 5000, 'from 2 to 1000'], ['1.5, 2', 100, 'could not read'], ['-3', 100, 'could not read']]) {
      await p.fill('#coins', c); await p.fill('#L', String(L)); await p.click('#apply'); await p.waitForTimeout(40);
      const n = await text('#notice'), shown = await p.evaluate(() => getComputedStyle(document.querySelector('#notice')).display); if (n.includes(word) && shown === 'block' && JSON.stringify(await tiles()) === before) good++; else console.log('  refusal wrong for', c, L, n); }
    must(good === 9, 'nine bad entries are refused with a reason and nothing changes (' + good + ')');
    await setCoins('1, 5, 10, 25', 100); must((await text('#notice')) === '' && (await p.evaluate(() => getComputedStyle(document.querySelector('#notice')).display)) === 'none', 'a good entry clears the notice');
    await setCoins('2, 4', 100); t = await tiles(); must(t[2].v === 'cannot make 50 amounts' && t[2].d.includes('multiple of 2') && t[0].v === 'cannot make 50 amounts' && (await text('#sayB')).includes('One way the best coin to add is 1,'), 'coins 2 and 4: half the amounts cannot be made either way, and the page says so');
    await setCoins('1', 2); t = await tiles(); must(t[0].v === '0.5' && t[2].v === '0.5' && (await p.evaluate(() => document.querySelector('#addPlain').disabled)) && (await text('#sayB')).includes('One way there is no coin left to try'), 'the smallest case, one coin and amounts 0 and 1, is drawn without error');
    await setCoins('1', 1000); await p.fill('#amount', '999'); await p.waitForTimeout(60); must((await count('#way-plain .coin')) === 40 && (await text('#way-plain')).includes('and 959 more') && (await text('#way-plain .k')).includes('999 coins'), '999 with a coin of 1 alone: forty coins drawn and the rest counted');
    // where no coin can help, the page says so and offers none (the referee's find)
    await setCoins('1, 2', 3); { const sb = await text('#sayB'); must(sb.includes('One way there is no coin left to try') && sb.includes('Both ways no single coin up to 5 lowers the cost of about 0.667.') && !sb.includes('best coin') && (await count('#chartB .bestmark')) === 0 &&
      (await p.evaluate(() => document.querySelector('#addPlain').disabled && document.querySelector('#addBoth').disabled)), 'coins 1 and 2, amounts 0 to 2: no coin is called best, and none is offered'); }
    await setCoins('1, 5, 10, 25', 2); { const sb = await text('#sayB'); must(sb.includes('One way there is no coin left to try') && sb.includes('Both ways no single coin up to 3 lowers the cost of 0.5.') && (await count('#chartB .bestmark')) === 0, 'the US coins with amounts 0 and 1: the same'); }
    await setCoins('2, 4', 100); { const sb = await text('#sayB'); must(sb.includes('One way the best coin to add is 1, bringing the cost to') && (await count('#chartB .bestmark')) >= 2 && !(await p.evaluate(() => document.querySelector('#addPlain').disabled)), 'a coin that makes every amount makeable for the first time is still called best'); }
    // the amount box: an entry that is no amount is put back when the box is left
    await p.selectOption('#preset', '0'); await p.fill('#amount', '38'); await p.waitForTimeout(40); { let good = 0;
      for (const bad of ['-1', '2.5', '']) { await p.fill('#amount', bad); await p.locator('#amount').press('Tab'); await p.waitForTimeout(40); if ((await p.inputValue('#amount')) === '38' && (await text('#way-both .k')).includes('3 coins') && (await p.inputValue('#amountR')) === '38') good++; }
      await p.fill('#amount', '100'); await p.waitForTimeout(40); if ((await p.inputValue('#amount')) === '99') good++;
      must(good === 4, 'the amount box: -1, 2.5 and nothing are put back to the amount in force; 100 becomes 99 (' + good + ' of 4)'); }
    console.log('own coins and refusals: done'); }
  // the slowest and the deepest views
  { const c = [1, 3, 7, 19, 43, 97, 211, 499, 997, 1999, 2999, 3499, 3999, 4499, 4799, 4999], t0 = Date.now(); await setCoins(c.join(', '), 1000); const ms = Date.now() - t0, t = await tiles();
    must(ms < 30000 && t[0].v === P.meanText(P.total(P.plain(c, 1000)), 1000, 3) && t[2].v === P.meanText(P.total(P.both(c, 1000)), 1000, 3) && (await p.evaluate(() => document.querySelector('#addPlain').disabled)), 'sixteen coins up to 4999 and a thousand amounts: counted in ' + ms + ' ms, and no seventeenth coin is offered');
    const big = []; for (let v = 4985; v <= 5000; v++) big.push(v); const t1 = Date.now(); await setCoins(big.join(', '), 1000); await p.fill('#amount', '500'); await p.waitForTimeout(400); const ms2 = Date.now() - t1, head = await text('#way-both .k');
    must(ms2 < 30000 && head.includes('68 coins') && head.includes('more ways than I counted') && (await count('#way-both .scheme')) === 12, 'sixteen coins from 4985 to 5000, amount 500: 68 coins, and the page says it stopped counting the ways (' + ms2 + ' ms)');
    console.log(`slowest view ${ms} ms; deepest ${ms2} ms`); }
  // the table of best sets
  { const rows = await p.evaluate(() => [...document.querySelectorAll('#best tr')].slice(1).map(tr => [...tr.children].map(td => ({ t: td.textContent, sets: [...td.querySelectorAll('button')].map(b => b.getAttribute('data-set')) })))); let good = 0, sets = 0;
    for (const r of rows) { const D = Number(r[0].t); let ok = r[1].sets.length > 0 && r[1].sets.every(s => { const c = s.split(',').map(Number); sets++; return c.length === D && P.meanText(P.total(P.plain(c, 100)), 100, 3) === r[2].t; }) && r[3].t === P.meanText(P.bound(D, 100, 'plain'), 100, 3) && r[6].t === P.meanText(P.bound(D, 100, 'both'), 100, 3);
      if (r[4].sets.length) ok = ok && r[4].sets.every(s => { const c = s.split(',').map(Number); sets++; return c.length === D && P.meanText(P.total(P.both(c, 100)), 100, 3) === r[5].t; }); else ok = ok && r[4].t === 'not searched' && r[5].t === '';
      if (ok) good++; }
    must(rows.length === 7 && good === 7 && sets === 20, 'the table of best sets: seven rows, twenty sets, each costing what its row says by pcore, with the counting bounds');
    await p.selectOption('#preset', '4'); await p.waitForTimeout(150);
    await p.click('#best button[data-set="16,19,21"]'); await p.waitForTimeout(120); const t = await tiles(); must((await p.inputValue('#coins')) === '16, 19, 21' && (await p.inputValue('#L')) === '100' && t[2].v === '3.88' && (await p.inputValue('#preset')) === 'own', 'pressing 16, 19, 21 in the table tries it above');
    await p.fill('#amount', '1'); await p.waitForTimeout(40); const s1 = await schemesShown(); must(s1.length === 1 && s1[0].over.join() === '19,19' && s1[0].back.join() === '21,16', '1 with (16, 19, 21): two 19s handed over, a 21 and a 16 handed back'); }
  // the tables open and close
  { await p.selectOption('#preset', '0'); const shown = sel => p.evaluate(s => getComputedStyle(document.querySelector(s)).display, sel); const a0 = await shown('#tabA'); await p.click('#tA'); const a1 = await shown('#tabA'), pr = await p.evaluate(() => document.querySelector('#tA').getAttribute('aria-pressed')); await p.click('#tA'); const a2 = await shown('#tabA');
    await p.click('#tB'); const b1 = await shown('#tabB'); await p.click('#tB'); must(a0 === 'none' && a1 === 'block' && pr === 'true' && a2 === 'none' && b1 === 'block', 'the Table buttons open and close the tables'); }
  await p.selectOption('#preset', '0'); await p.fill('#amount', '38'); await p.waitForTimeout(150); await p.locator('#fig1').screenshot({ path: path.join(out, 'euro.png') }); await p.screenshot({ path: path.join(out, 'page.png'), fullPage: true });
  await p.selectOption('#preset', '8'); await p.waitForTimeout(150); await p.fill('#amount', '1'); await p.waitForTimeout(60); await p.screenshot({ path: path.join(out, 'three.png'), fullPage: true });
  for (const wv of [320, 360, 400]) { await p.setViewportSize({ width: wv, height: 900 }); await p.waitForTimeout(150); const sw = await p.evaluate(() => document.documentElement.scrollWidth); must(sw <= wv, 'no sideways scroll of the page at ' + wv + ' px (' + sw + ')'); if (wv === 360) await p.screenshot({ path: path.join(out, 'narrow.png'), fullPage: true }); }
  must(errs.length === 0, 'no error on the page');
  console.log('errors: ' + JSON.stringify(errs)); fails.forEach(f => console.log('FAILED: ' + f));
  console.log(`PAGE TEST: ${asserts} assertions, ${fails.length} failed`); await b.close(); process.exit(fails.length ? 1 : 0);
})();

// Headless checks of the gasket page: the circles drawn against gcore.js here, deep views, the lights, pointer and keys,
// the chart, the any-gasket panel.     usage: node shot-gasket.js PAGE.html OUTDIR CORE.js DATA.json
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])]; const G = require(path.resolve(process.argv[4])), DATA = JSON.parse(fs.readFileSync(path.resolve(process.argv[5]), 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(800);
  const text = sel => p.evaluate(sel => { const n = document.querySelector(sel).cloneNode(true); n.querySelectorAll('sup').forEach(x => { x.textContent = '^' + x.textContent; }); n.querySelectorAll('br').forEach(x => x.replaceWith(' | ')); return n.textContent; }, sel);
  const state = () => p.evaluate(() => ({ view: window.GasketPage.view(), root: window.GasketPage.pack().root, drawn: window.GasketPage.drawn().map(c => c.join(',')) }));
  const here = st => { const pl = G.place(st.root), v = st.view, got = []; G.inView(pl, { cx: v.cx, cy: v.cy, hw: 500 / v.s, hh: 310 / v.s }, 0.7 / v.s, (b, X, Y) => got.push([b, X, Y].join(',')), 600000); return got; };
  const same = (a, b) => a.length === b.length && a.every((s, i) => s === b[i]);
  const n = await p.evaluate(() => document.querySelectorAll('#pack option').length);
  for (let i = 0; i < n; i++) { await p.selectOption('#pack', String(i)); await p.waitForTimeout(150); const st = await state(), mine = here(st);
    console.log(`${JSON.stringify(st.root)} whole: ${st.drawn.length} circles drawn; the same list from gcore.js here: ${same(st.drawn, mine)}; ` + (await text('#gsay')).slice(0, 230));
    await p.locator('#g').screenshot({ path: path.join(out, 'gasket-' + st.root.join('_').replace(/-/g, 'm') + '.png') }); }
  // deep views in (-3, 5, 8, 8), squares lit: magnify about points of contact, compare, count the lit
  await p.selectOption('#pack', '0'); await p.selectOption('#hi', '1'); let litTotal = 0, circ = 0, deepSame = 0, deepN = 0, maxb = 0;
  { const pl = G.place([-3, 5, 8, 8]); let seed = 7; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
    for (let k = 0; k < 24; k++) { let cur = pl.circles.map(c => c.slice()), last = -1; const depth = 2 + Math.floor(rnd() * 28);
      for (let j = 0; j < depth; j++) { let i; do { i = Math.floor(rnd() * 4); } while (i === last); const nw = [0, 1, 2].map(t => 2 * (cur[0][t] + cur[1][t] + cur[2][t] + cur[3][t] - cur[i][t]) - cur[i][t]); if (nw[0] > 1e11) break; cur[i] = nw; last = i; }
      const c = cur[last < 0 ? 1 : last], s = Math.min(295 * 3 * 1e11, 120 * Math.abs(c[0])); await p.evaluate(([cx, cy, s]) => window.GasketPage.setView(cx, cy, s), [c[1] / c[0], c[2] / c[0], s]); await p.waitForTimeout(40);
      const st = await state(), mine = here(st); deepN++; if (same(st.drawn, mine)) deepSame++; circ += st.drawn.length; maxb = Math.max(maxb, ...st.drawn.map(x => +x.split(',')[0]));
      litTotal += st.drawn.filter(x => { const b = +x.split(',')[0]; return b > 0 && G.isSquare(b); }).length; } }
  console.log(`(-3, 5, 8, 8), 24 views about circles up to ${maxb.toExponential(2)} in curvature: the same list as gcore.js here in ${deepSame} of ${deepN}; ${circ} circles drawn in all, ${litTotal} of them squares`); await p.locator('#g').screenshot({ path: path.join(out, 'gasket-deep.png') });
  await p.selectOption('#pack', '1'); await p.waitForTimeout(150); { const st = await state(); const sq = st.drawn.map(x => +x.split(',')[0]).filter(b => b > 0 && G.isSquare(b)), two = st.drawn.map(x => +x.split(',')[0]).filter(b => b > 0 && b % 2 === 0 && G.isSquare(b / 2));
    console.log(`(-4, 5, 20, 21) whole: squares among the ${st.drawn.length} drawn: ${sq.length} (${[...new Set(sq)].sort((a, b) => a - b).slice(0, 8).join(', ')}); twice a square: ${two.length}; ` + (await text('#gsay')).slice(0, 120)); await p.locator('#g').screenshot({ path: path.join(out, 'gasket-squares.png') }); }
  await p.selectOption('#pack', '6'); await p.selectOption('#hi', 'q'); await p.waitForTimeout(150); { let lit = 0, tot = 0; for (const f of [1, 3, 10, 40, 200]) { const v = await p.evaluate(() => window.GasketPage.view()); await p.evaluate(([cx, cy, s]) => window.GasketPage.setView(cx, cy, s), [v.cx + 0.3 / v.s, v.cy + 0.2 / v.s, 295 * 23 * f]); const st = await state(); tot += st.drawn.length;
      lit += st.drawn.filter(x => { const b = +x.split(',')[0]; return b > 0 && [1, 4, 9, 36].some(u => b % u === 0 && Math.round(Math.pow(b / u, 0.25)) ** 4 === b / u); }).length; }
    console.log(`(-23, 48, 49, 52), five magnifications, fourth powers lit: ${lit} of ${tot} circles drawn; ` + (await text('#gsay')).slice(0, 110)); } await p.selectOption('#hi', '1');
  // where two circles touch, as far in as the page goes: the places that broke the first form of the walk
  for (const [idx, i1, i2] of [[2, 1, 2], [0, 1, 2], [3, 0, 2], [6, 1, 3]]) { await p.selectOption('#pack', String(idx)); await p.waitForTimeout(100); const root = (await state()).root, pl = G.place(root), c1 = pl.circles[i1], c2 = pl.circles[i2], T = [(c1[1] + c2[1]) / (c1[0] + c2[0]), (c1[2] + c2[2]) / (c1[0] + c2[0])]; let line = '';
    for (const f of [1e3, 1e6, 1e9, 1e12]) { const t0 = Date.now(); await p.evaluate(([cx, cy, f]) => { const P = window.GasketPage, lim = P.pack().place.strip ? 150 : 295 * Math.abs(P.pack().root[0]); P.setView(cx, cy, Math.min(lim * f, lim * 1e11, 1.4e15)); }, [T[0], T[1], f]); const st = await state(); line += ` ×${f.toExponential(0)}: ${st.drawn.length} circles, same as here ${same(st.drawn, here(st))}, ${Date.now() - t0} ms;`; }
    console.log(`${JSON.stringify(root)}, where circles ${c1[0]} and ${c2[0]} touch:` + line); }
  await p.locator('#g').screenshot({ path: path.join(out, 'gasket-contact.png') });
  // pointer, wheel, drag, keys, table
  const box = await p.locator('#g').boundingBox(); await p.selectOption('#pack', '0'); await p.waitForTimeout(100);
  await p.mouse.move(box.x + box.width * 0.5, box.y + box.height * 0.28); await p.waitForTimeout(100); console.log('pointer in the upper middle of (-3, 5, 8, 8): ' + (await text('#gtip')));
  const v0 = await p.evaluate(() => window.GasketPage.view()); await p.mouse.wheel(0, -100); await p.waitForTimeout(100); const v1 = await p.evaluate(() => window.GasketPage.view());
  await p.mouse.down(); await p.mouse.move(box.x + box.width * 0.4, box.y + box.height * 0.28, { steps: 3 }); await p.mouse.up(); const v2 = await p.evaluate(() => window.GasketPage.view());
  await p.locator('#g').focus(); await p.keyboard.press('+'); await p.keyboard.press('ArrowRight'); const v3 = await p.evaluate(() => window.GasketPage.view()); await p.keyboard.press('Home'); const v4 = await p.evaluate(() => window.GasketPage.view());
  console.log(`wheel: scale ${v0.s} -> ${v1.s}; drag a tenth of the width left: centre x ${v1.cx.toFixed(5)} -> ${v2.cx.toFixed(5)}; + and ArrowRight: scale ${v3.s}, x ${v3.cx.toFixed(5)}; Home: scale ${v4.s}`);
  await p.click('#gtab'); console.log('table: ' + (await p.evaluate(() => Array.from(document.querySelectorAll('#gtable tr')).slice(0, 5).map(r => Array.from(r.children).map(c => c.textContent).join(' | ')).join(' ;; ')))); await p.click('#gtab');
  // the chart
  for (let i = 0; i < DATA.length; i++) { await p.selectOption('#cpack', String(i)); await p.waitForTimeout(80); const m = await p.evaluate(() => window.GasketPage.marks().length); const d = DATA[i], res = G.type(d.root).res; let fam = 0; d.families.forEach(u => { for (let k = 1; u * k * k <= d.N; k++) if (res.includes((u * k * k) % 24)) fam++; });
    console.log(`chart ${JSON.stringify(d.root)}: ${m} ticks drawn (${d.sporadic.length} + ${fam} expected: ${m === d.sporadic.length + fam}; in the families by the run: ${d.inFamilies}); ` + (await text('#csay')).slice(0, 260)); }
  await p.selectOption('#cpack', '2'); const cb = await p.locator('#chart').boundingBox(); await p.mouse.move(cb.x + cb.width * 0.82, cb.y + cb.height * 0.3); await p.waitForTimeout(80); console.log('chart, pointer near the right of the top row: ' + (await text('#ctip')));
  await p.mouse.move(cb.x + cb.width * 0.5, cb.y + cb.height * 0.55); await p.waitForTimeout(80); console.log('chart, pointer in the middle of the second row: ' + (await text('#ctip')));
  await p.locator('#chart').focus(); await p.keyboard.press('ArrowRight'); await p.keyboard.press('Shift+ArrowRight'); console.log('chart, keys: ' + (await text('#ctip')));
  await p.click('#ctab'); console.log('chart table: ' + (await text('#ctable')).slice(0, 200) + ' ...'); await p.click('#ctab'); await p.locator('#cfig').screenshot({ path: path.join(out, 'chart.png') });
  // any gasket
  console.log('default: ' + (await text('#tsay'))); console.log('   ' + (await text('#tnums')).slice(0, 160));
  for (const q of ['-6, 11, 14, 15', '15 2 2 3', '1, 2, 3, 4', '-2, 4, 4, 6', '-8, 12, 25, 25', '-4, 8, 9, 9', '0 0 1 1', '-16, 32, 33, 41', 'x']) { await p.fill('#quad', q); await p.click('#try'); await p.waitForTimeout(200); console.log(q + ' -> ' + (await text('#tsay')).slice(0, 520)); }
  await p.fill('#quad', '-6, 11, 14, 15'); await p.selectOption('#upto', '1000000'); const t0 = Date.now(); await p.click('#try'); await p.waitForTimeout(100); console.log(`-6, 11, 14, 15 up to a million (${Date.now() - t0} ms): ` + (await text('#tsay')).slice(-200));
  await p.click('#show'); await p.waitForTimeout(300); const st = await state(); console.log('drawn above: ' + JSON.stringify(st.root) + ', ' + st.drawn.length + ' circles, the same as gcore.js here: ' + same(st.drawn, here(st)));
  await p.selectOption('#pack', '0'); await p.selectOption('#cpack', '2'); await p.waitForTimeout(200); await p.screenshot({ path: path.join(out, 'page.png'), fullPage: true });
  console.log('errors on the page: ' + (errs.length ? errs.join(' ; ') : 'none')); await b.close();
})();

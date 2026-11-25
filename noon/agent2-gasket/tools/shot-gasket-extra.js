// A few views one step outside the page test, after the referee: combinations of a light, a place far along, and the limit.
// usage: node shot-gasket-extra.js PAGE.html OUTDIR CORE.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])]; const G = require(path.resolve(process.argv[4]));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(800);
  const text = sel => p.evaluate(sel => document.querySelector(sel).textContent, sel);
  const state = () => p.evaluate(() => ({ view: window.GasketPage.view(), root: window.GasketPage.pack().root, drawn: window.GasketPage.drawn().map(c => c.join(',')), left: window.GasketPage.leftOut()[0] }));
  const here = st => { const pl = G.place(st.root), v = st.view, got = []; G.inView(pl, { cx: v.cx, cy: v.cy, hw: 500 / v.s, hh: 310 / v.s }, 0.7 / v.s, (b, X, Y, wx, wy, k) => got.push([b, X, Y, k || 0].join(',')), 600000); return got; };
  const same = (a, b) => a.length === b.length && a.every((s, i) => s === b[i]); let bad = 0;
  const bx = await p.locator('#g').boundingBox(); const at = (fx, fy) => p.mouse.move(bx.x + bx.width * fx, bx.y + bx.height * fy);
  const report = async what => { const st = await state(), ok = same(st.drawn, here(st)), say = await text('#gsay'), missing = say.includes('may be missing'), stopped = say.includes('stopped looking');
    if (!ok || missing || stopped || st.left !== 0) bad++; console.log(`${what}: ${st.drawn.length} drawn, same as gcore.js here: ${ok}; left out ${st.left}; "may be missing": ${missing}; errors so far ${errs.length}; ` + say.slice(0, 90).replace(/\s+/g, ' ')); };
  // A. the strip, each light, inside a unit circle 3,000 units along, to the limit by the wheel
  await p.selectOption('#pack', '3');
  for (const h of ['1', '2', '3', '6', 'q', 'five', 'none']) { await p.selectOption('#hi', h); await p.evaluate(() => window.GasketPage.setView(3000, 0.3, 150)); await at(0.5, 0.5); for (let k = 0; k < 70; k++) { await p.mouse.wheel(0, -100); await p.waitForTimeout(8); } await report('A. strip, light ' + h + ', inside the unit circle at x = 3000, 70 turns'); }
  // B. the strip at its limit on points where unit circles touch, far along both ways; then the pointer and the table there
  await p.selectOption('#hi', '1');
  for (const x of [1000001, 1000000001, -10000001, -1, 123456789013]) { await p.evaluate(x => window.GasketPage.setView(x, 0, 150 * 1e11), x); await p.waitForTimeout(60); await report('B. strip at the limit where unit circles touch, x = ' + x);
    await at(0.5, 0.52); await p.waitForTimeout(60); const tip = await p.evaluate(() => { const n = document.querySelector('#gtip'); return n ? n.textContent : '(no #gtip)'; }); console.log('   pointer just below the middle: ' + tip.slice(0, 150)); }
  for (const x of [1000001.37, -4321.11]) { await p.evaluate(x => window.GasketPage.setView(x, 0.61, 150 * 3e5), x); await p.waitForTimeout(60); await report('B2. strip magnified 300,000 times at x = ' + x + ', y = 0.61'); }
  // C. a gasket from the third panel, a light, the pointer on a lit circle, to the limit
  await p.fill('#quad', '-6, 11, 14, 15'); await p.click('#try'); await p.waitForTimeout(300); await p.click('#show'); await p.waitForTimeout(300);
  for (const h of ['five', '1', '3']) { await p.selectOption('#hi', h); await p.keyboard.press('Home').catch(() => {}); await p.evaluate(() => { const P = window.GasketPage.pack(), c = P.place.circles[2]; window.GasketPage.setView(c[1] / c[0], c[2] / c[0], 295 * 6); }); await at(0.5, 0.5); for (let k = 0; k < 70; k++) { await p.mouse.wheel(0, -100); await p.waitForTimeout(8); } await report('C. (-6, 11, 14, 15), light ' + h + ', inside its circle of curvature ' + (await p.evaluate(() => window.GasketPage.pack().place.circles[2][0])) + ', 70 turns'); }
  // D. on the outer circle's edge, and right outside it, at the limit
  for (const idx of ['0', '2', '6']) { await p.selectOption('#pack', idx); await p.waitForTimeout(100); const st = await state(), pl = G.place(st.root), o = pl.circles[0], R = 1 / Math.abs(o[0]), cx = o[1] / o[0], cy = o[2] / o[0], lim = 295 * Math.abs(o[0]) * 1e11, s = Math.min(lim, 1.4e15);
    for (const [dx, dy, what] of [[0.6, 0.8, 'on the outer circle'], [0.6 * 1.0000001, 0.8 * 1.0000001, 'just outside it'], [3, 4, 'far outside']]) { await p.evaluate(v => window.GasketPage.setView(v[0], v[1], v[2]), [cx + R * dx, cy + R * dy, s]); await p.waitForTimeout(60); await report('D. ' + JSON.stringify(st.root) + ' at the limit ' + what); } }
  // E. many presses of an arrow key at the limit in the strip, then the table
  await p.selectOption('#pack', '3'); await p.evaluate(() => window.GasketPage.setView(1, 0, 150 * 1e11)); await p.locator('#g').focus(); for (let k = 0; k < 300; k++) await p.keyboard.press('ArrowLeft'); await report('E. strip at the limit after 300 presses of the left arrow');
  await p.evaluate(() => window.GasketPage.setView(-70001, 0, 150 * 1e9)); const tb = await p.$('#gtab'); if (tb) { await tb.click(); await p.waitForTimeout(100); } console.log('   table button present: ' + !!tb + '; errors ' + errs.length);
  await p.locator('#g').screenshot({ path: path.join(out, 'extra-last.png') });
  console.log('errors on the page: ' + (errs.length ? errs.join(' ; ') : 'none')); console.log(`EXTRA VIEWS: ${bad} not as gcore.js or with something left out, ${errs.length} errors`); await b.close();
})();

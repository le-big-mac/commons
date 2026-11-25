// Headless checks of the isolated-state page: rings in the page against core.js here, the presets, the pointer, the keyboard, the table.
//   usage: node shot-thunen.js PAGE.html OUTDIR CORE.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])]; const T = require(path.resolve(process.argv[4]));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(600);
  for (const name of ['plain', 'river', 'miss', 'motley']) {
    await p.selectOption('#preset', name); await p.waitForTimeout(500);
    const st = await p.evaluate(() => ({ rivers: window.__thunen.state.rivers, a: window.__thunen.state.a, y: window.__thunen.state.y, w: window.__thunen.state.w, cell: window.__thunen.cell(), labelled: window.__thunen.state.labelled }));
    const net = new T.Net({ x: 60, y: 40 }, st.rivers.map(r => ({ pts: r, ratio: st.w })), 0.5); let same = 0, n = 0, counts = [0, 0, 0, 0, 0, 0, 0, 0];
    const pts = []; for (let k = 0; k < 600; k++) pts.push([(k * 37 % 240) / 2 + 0.13, (k * 53 % 160) / 2 + 0.13]);
    const got = await p.evaluate(pts => pts.map(([x, y]) => { const a = window.__thunen.at(x, y); return [a.ring, a.eq, a.yield]; }), pts);
    pts.forEach(([x, y], k) => { const ring = T.ring(net.eq(x, y), got[k][2], st.a, st.y); n++; if (ring === got[k][0] && Math.abs(net.eq(x, y) - got[k][1]) < 1e-12) same++; counts[got[k][0]]++; });
    console.log(`${name}: ${same} of ${n} places have the same ring and the same miles in the page as in core.js here; places in rings 1 to 6 and beyond: ${counts.slice(1).join(' ')}; drawn at ${st.cell} px; names on the map: ${st.labelled.join(', ')}`);
    await p.locator('#map').screenshot({ path: path.join(out, name + '.png') });
  }
  // plate II in the page: down the river the third ring reaches the foot of the map, and there is no stock farming beside the river
  await p.selectOption('#preset', 'river'); await p.waitForTimeout(500);
  const pl = await p.evaluate(() => { const t = window.__thunen, riv = t.state.rivers[0], end = riv[riv.length - 1], res = { end: end, rings: [], six: 0 };
    for (let dx = -12; dx <= 12; dx += 1) res.rings.push(t.at(end[0] + dx, end[1] - 1).ring); for (const pt of riv) for (let dx = -8; dx <= 8; dx += 2) if (t.at(pt[0] + dx, pt[1]).ring >= 6) res.six++; return res; });
  console.log(`second plate: a mile above the foot of the map, rings from 12 miles left of the river to 12 right: ${pl.rings.join(' ')}; places within 8 miles of the river in the sixth ring or beyond: ${pl.six}`);
  // the pointer and the keyboard give the same words
  const box = await p.locator('#map').boundingBox(); await p.mouse.move(box.x + box.width * 0.75, box.y + box.height * 0.5); await p.waitForTimeout(100);
  const tipText = await p.evaluate(() => document.getElementById('tip').textContent), read1 = await p.evaluate(() => document.getElementById('readout').textContent);
  console.log('pointer at three quarters across, half way down: ' + read1); console.log('the tooltip says the same: ' + (tipText === read1));
  await p.locator('#map').focus(); await p.keyboard.press('ArrowRight'); await p.keyboard.press('Shift+ArrowDown'); const read2 = await p.evaluate(() => document.getElementById('readout').textContent);
  console.log('after ArrowRight and Shift+ArrowDown: ' + read2.slice(0, 90) + ' ...');
  // the sliders, and the table
  await p.selectOption('#preset', 'plain'); await p.locator('#a').fill('1.05'); await p.locator('#y').fill('10'); await p.waitForTimeout(500); await p.click('#tab');
  const tb = await p.evaluate(() => Array.from(document.querySelectorAll('#tables table')[0].querySelectorAll('tr')).slice(1).map(r => Array.from(r.children).map(c => c.textContent).join(' | ')));
  const r = T.rings(1.05, 10); console.log('table at 1.05 Taler and 10 Körner: ' + tb.join(' ; ')); console.log('core.js here: ' + r.map(x => x.toFixed(1)).join(' '));
  await p.locator('#chart').focus(); await p.keyboard.press('Shift+ArrowRight'); await p.keyboard.press('Shift+ArrowRight'); const ct = await p.evaluate(() => Array.from(document.querySelectorAll('#chart g text')).map(t => t.textContent).join(' / '));
  console.log('chart, keyboard to 10 miles: ' + ct);
  // drawing a river with the pointer
  await p.selectOption('#preset', 'plain'); await p.locator('#a').fill('1.5'); await p.locator('#y').fill('8'); await p.selectOption('#tool', 'river');
  for (const [fx, fy] of [[0.5, 0.5], [0.7, 0.35], [0.95, 0.3]]) await p.mouse.click(box.x + box.width * fx, box.y + box.height * fy);
  await p.locator('#map').focus(); await p.keyboard.press('Enter'); await p.waitForTimeout(500); await p.selectOption('#tool', 'look');
  const dr = await p.evaluate(() => ({ n: window.__thunen.state.rivers.length, pts: window.__thunen.state.rivers[0], far: window.__thunen.at(112, 25).ring, mirror: window.__thunen.at(8, 55).ring }));
  console.log(`a river drawn by three clicks and Enter: ${dr.n} river of ${dr.pts.length} points; the ring near its far end (112, 25) is ${dr.far}, and at the place opposite across the town (8, 55) it is ${dr.mirror}`);
  await p.selectOption('#tool', 'sand'); await p.mouse.move(box.x + box.width * 0.42, box.y + box.height * 0.5); await p.mouse.down(); await p.mouse.move(box.x + box.width * 0.44, box.y + box.height * 0.52); await p.mouse.up(); await p.waitForTimeout(400); await p.selectOption('#tool', 'look');
  const sd = await p.evaluate(() => { const a = window.__thunen.at(50.5, 40.2); return [a.ring, a.yield, a.eq.toFixed(1)]; }); console.log(`sand laid 9.5 miles west of the town: ring ${sd[0]}, soil ${sd[1]} Körner, ${sd[2]} miles of carting`);
  await p.screenshot({ path: path.join(out, 'page.png'), fullPage: true });
  console.log('script errors:', JSON.stringify(errs));
  await b.close();
})();

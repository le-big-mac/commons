// Headless checks of the fuses page: every preset's thousand columns against core.js here, the pointer, the keys, the
// table, the bench and its two shows, the one-number panel.     usage: node shot-fuse.js PAGE.html OUTDIR CORE.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])]; const F = require(path.resolve(process.argv[4]));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1700 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(800);
  const text = sel => p.evaluate(sel => { const n = document.querySelector(sel).cloneNode(true); n.querySelectorAll('sup').forEach(x => { x.textContent = '^' + x.textContent; }); n.querySelectorAll('br').forEach(x => x.replaceWith(' | ')); return n.textContent; }, sel);
  const settle = async () => { const t0 = Date.now(); for (;;) { const left = await p.evaluate(() => Array.from(window.FusePage.cols).filter(c => c < 0).length); if (left === 0) return Date.now() - t0; if (Date.now() - t0 > 120000) return -1; await p.waitForTimeout(200); } };
  for (const name of ['whole', 'one', 'two', 'after2', 'wild', 'wild2', 'fivehalves', 'three']) {
    await p.selectOption('#preset', name); const ms = await settle();
    const st = await p.evaluate(() => ({ p: window.FusePage.view().p, Lp: window.FusePage.view().Lp.toString(), cols: Array.from(window.FusePage.cols) }));
    const f = new F.Fusible(); f.maxDepth = 300 + 3 * st.p; const B = Math.min(200000, 4000 + 300 * st.p); let same = 0; const n = [0, 0, 0, 0, 0], diff = [];
    const order = []; for (let i = 0; i < 1000; i++) order.push(i); order.sort((a, b) => Math.abs(a - 500) - Math.abs(b - 500));          // the page works outward from the middle, with a clean memory at each zoom
    for (const i of order) { const c = f.columnMemo(F.D(BigInt(st.Lp) + BigInt(i), st.p), st.p, B); if (c === st.cols[i]) same++; else diff.push(i + ': page ' + st.cols[i] + ', here ' + c); n[st.cols[i]]++; }
    if (diff.length) console.log('   differing: ' + diff.slice(0, 8).join('; '));
    console.log(`${name}: pixel 2^-${st.p}; ${same} of 1000 columns the same in the page as from core.js here; empty ${n[0]}, tame ${n[1]}, wild only ${n[2]}, fusible ${n[3]}, not worked out ${n[4]}; drawn in ${ms < 0 ? 'MORE THAN 120 s' : (ms / 1000).toFixed(1) + ' s'}`);
    await p.locator('#line').screenshot({ path: path.join(out, 'line-' + name + '.png') });
  }
  // the pointer
  await p.selectOption('#preset', 'wild'); await settle(); const box = await p.locator('#line').boundingBox();
  for (const col of [400, 528, 656, 600]) { await p.mouse.move(box.x + (col + 0.5) * box.width / 1000, box.y + 40); await p.waitForTimeout(150); console.log(`pointer at column ${col} of the 33/16 view: ` + (await text('#tip'))); }
  // the keys
  await p.locator('#line').focus(); const v0 = await p.evaluate(() => [window.FusePage.view().p, window.FusePage.view().Lp.toString()]);
  await p.keyboard.press('ArrowRight'); await p.keyboard.press('+'); await settle(); const v1 = await p.evaluate(() => [window.FusePage.view().p, window.FusePage.view().Lp.toString()]);
  console.log(`keys: ArrowRight and + took the view from pixel 2^-${v0[0]}, left edge ${v0[1]} columns, to pixel 2^-${v1[0]}, left edge ${v1[1]} (expected ${2n * (BigInt(v0[1]) + 60n + 500n) - 500n})`);
  await p.keyboard.press('Home'); await settle(); console.log('Home: ' + (await text('#lineSay')).slice(0, 120));
  // the wheel and a drag
  await p.mouse.move(box.x + 500 * box.width / 1000, box.y + 40); await p.mouse.wheel(0, -100); await settle(); const v2 = await p.evaluate(() => window.FusePage.view().p);
  await p.mouse.down(); await p.mouse.move(box.x + 300 * box.width / 1000, box.y + 40, { steps: 4 }); await p.mouse.up(); await settle(); const v3 = await p.evaluate(() => window.FusePage.view().Lp.toString());
  console.log(`wheel up at the middle: pixel 2^-${v2}; then a drag 200 columns to the left: left edge ${v3}`);
  // the table
  await p.selectOption('#preset', 'wild'); await settle(); await p.click('#tab'); await p.waitForTimeout(300);
  const rows = await p.evaluate(() => Array.from(document.querySelectorAll('#lineTable tr')).slice(0, 7).map(r => Array.from(r.children).map(c => { const n = c.cloneNode(true); n.querySelectorAll('sup').forEach(x => { x.textContent = '^' + x.textContent; }); return n.textContent; }).join(' | ')));
  console.log('table at the 33/16 view:\n  ' + rows.join('\n  ')); await p.click('#tab');
  // the bench
  await p.click('#demo45'); await p.waitForTimeout(5600);
  console.log('riddle: ' + (await text('#benchSay')) + ' || chips: ' + (await p.evaluate(() => Array.from(document.querySelectorAll('#chips button')).map(b => b.innerText.replace(/\n/g, ' ')).join(', '))));
  await p.locator('#fuse').screenshot({ path: path.join(out, 'bench-45.png') });
  await p.click('#demoWild'); await p.waitForTimeout(9000);
  console.log('wild: ' + (await text('#benchSay')) + ' || ' + (await p.evaluate(() => document.querySelectorAll('#chips button').length)) + ' chips');
  const chips = p.locator('#chips button'); await chips.first().click(); await chips.last().click(); await p.waitForTimeout(300);
  console.log('first and last chip: ' + (await text('#benchSay')));
  await p.click('#benchReset'); await chips.first().click(); await chips.first().click(); await p.waitForTimeout(700); await p.locator('#fuse').screenshot({ path: path.join(out, 'bench-burning.png') }); await p.waitForTimeout(2400);
  await p.locator('#chips button').nth(1).click(); await p.locator('#chips button').nth(1).click(); await p.waitForTimeout(3000);
  console.log('by hand, 0 twice and then 1/2 twice: ' + (await text('#benchSay')));
  // one number
  console.log('33/16: ' + (await text('#numSay')));
  await p.click('#askProved'); await p.waitForTimeout(500); console.log('  proved: ' + (await text('#numSay')).split(' | ').pop());
  for (const t of ['17/16', '0.1', '2.0625', '8449/4096', '3', '-1', 'x', '2305/1024']) { await p.fill('#num', t); await p.click('#ask'); await p.waitForTimeout(300); console.log(t + ': ' + (await text('#numSay'))); }
  await p.click('#askProved'); await p.waitForTimeout(6000); console.log('  proved, 2305/1024: ' + (await text('#numSay')).split(' | ').pop());
  await p.fill('#num', '5/2'); await p.click('#ask'); await p.click('#toLine'); await settle(); console.log('5/2 found on the line: ' + (await text('#lineSay')).slice(0, 150));
  await p.fill('#num', '9/8'); await p.click('#ask'); await p.click('#toBench'); await p.waitForTimeout(5000); console.log('9/8 on the bench: ' + (await text('#benchSay')));
  console.log('table of gaps:\n  ' + (await p.evaluate(() => Array.from(document.querySelectorAll('#landmarks tr')).map(r => Array.from(r.children).map(c => { const n = c.cloneNode(true); n.querySelectorAll('sup').forEach(x => { x.textContent = '^' + x.textContent; }); return n.textContent; }).join(' | ')).join('\n  '))));
  await p.selectOption('#preset', 'whole'); await settle(); await p.screenshot({ path: path.join(out, 'page.png'), fullPage: true });
  console.log('errors on the page: ' + (errs.length ? errs.join(' ; ') : 'none')); await b.close();
})();

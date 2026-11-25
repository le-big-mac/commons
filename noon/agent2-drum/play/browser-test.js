const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1060, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(400);
  const out = {};
  const names = await p.$$eval('#presets button', bs => bs.map(x => x.textContent));
  for (let i = 0; i < names.length; i++) { await p.click(`#presets button:nth-of-type(${i + 1})`); await p.waitForTimeout(150); out[names[i]] = await p.evaluate(() => ({ miss: document.getElementById('miss').textContent, cents: document.getElementById('missc').textContent, mass: document.getElementById('mass').textContent, bench: document.getElementById('bench').textContent, beat: document.getElementById('beat').textContent, miss16: document.getElementById('miss16').textContent, exact: window.__drum.result.miss })); }
  // a drag across the editor
  await p.click('#presets button:nth-of-type(2)'); const box = await (await p.$('#editor')).boundingBox();
  await p.mouse.move(box.x + 60, box.y + 150); await p.mouse.down(); await p.mouse.move(box.x + 200, box.y + 120, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(150);
  out.afterDrag = await p.evaluate(() => ({ miss: document.getElementById('miss').textContent, mass: document.getElementById('mass').textContent, hover: document.getElementById('hover').textContent }));
  await p.click('#undo'); await p.waitForTimeout(150); out.afterUndo = await p.evaluate(() => document.getElementById('miss').textContent);
  await p.click('#presets button:nth-of-type(4)'); await p.waitForTimeout(150);
  await p.click('#rows tr:nth-child(3)'); await p.waitForTimeout(150); out.shapecap = await p.evaluate(() => document.getElementById('shapecap').textContent);
  await p.click('button[data-at="0.5"]'); await p.waitForTimeout(300); out.heard1 = await p.evaluate(() => document.getElementById('heard').textContent);
  await p.click('#phrase'); await p.waitForTimeout(600); out.heard2 = await p.evaluate(() => document.getElementById('heard').textContent);
  await p.click('#plain'); await p.waitForTimeout(300); out.heard3 = await p.evaluate(() => document.getElementById('heard').textContent);
  await p.click('#presets button:nth-of-type(2)'); await p.waitForTimeout(100); await p.click('#nudge'); await p.waitForTimeout(3600); out.afterNudge = await p.evaluate(() => ({ miss: document.getElementById('miss').textContent, mass: document.getElementById('mass').textContent, hover: document.getElementById('hover').textContent }));
  await p.click('#heavier'); await p.waitForTimeout(150); out.afterHeavier = await p.evaluate(() => document.getElementById('mass').textContent);
  await p.click('summary'); await p.fill('#nums', Array(40).fill(0).map((v, i) => i < 16 ? 8.9375 : 0).join(' ')); await p.click('#usenums'); await p.waitForTimeout(150); out.afterNumbers = await p.evaluate(() => document.getElementById('miss').textContent + ' ' + document.getElementById('numsmsg').textContent);
  await p.fill('#nums', '1 2 3'); await p.click('#usenums'); await p.waitForTimeout(100); out.badNumbers = await p.evaluate(() => document.getElementById('numsmsg').textContent);
  await p.click('#presets button:nth-of-type(4)'); await p.waitForTimeout(150);
  await p.selectOption('#goal', '16'); await p.click('#presets button:nth-of-type(2)'); await p.waitForTimeout(100); await p.click('#nudge'); await p.waitForTimeout(3700); out.afterNudge16 = await p.evaluate(() => ({ miss: document.getElementById('miss').textContent, miss16: document.getElementById('miss16').textContent })); await p.click('#rows tr:nth-child(12)'); await p.waitForTimeout(150); out.shape12 = await p.evaluate(() => document.getElementById('shapecap').textContent); await p.click('#presets button:nth-of-type(7)'); await p.waitForTimeout(200);
  out.timing = await p.evaluate(() => { const t0 = performance.now(); for (let i = 0; i < 20; i++) sixteenRatios(window.__drum.load); const t1 = performance.now(); allModes(window.__drum.load, 6.6); const t2 = performance.now(); return { nine_ms: (t1 - t0) / 20, all_ms: t2 - t1 }; });
  await p.screenshot({ path: process.argv[3], fullPage: true });
  console.log(JSON.stringify({ errs, out }, null, 1)); await b.close();
})();

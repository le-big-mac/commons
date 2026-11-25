// usage (needs playwright): node browser-test.js /path/to/play.html shot.png
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1060, height: 1300 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(300); const out = {};
  const read = () => p.evaluate(() => ({ ahead: document.getElementById('ahead').textContent, alone: document.getElementById('alone').textContent, third: document.getElementById('third').textContent, q: document.getElementById('qsay').textContent, g: document.getElementById('gsay').textContent, tally: document.getElementById('tally').textContent, exact: window.__mk.numbers() }));
  out.start = await read();
  await p.click('#one'); await p.click('#twenty'); await p.waitForTimeout(200); out.afterRuns = (await read()).tally;
  await p.selectOption('#a', '10'); await p.waitForTimeout(200); out.a10 = await read();
  await p.selectOption('#a', '1'); await p.fill('#g', '0'); await p.waitForTimeout(200); out.g0 = await read();
  await p.fill('#g', '1.5'); await p.selectOption('#n', '10000'); await p.waitForTimeout(600); out.g15 = await read(); await p.click('#twenty'); await p.waitForTimeout(300);
  await p.fill('#g', '0.5'); await p.fill('#q', '1.37'); await p.selectOption('#n', '1000'); await p.waitForTimeout(300); out.odd = await read(); await p.click('#twenty'); await p.waitForTimeout(200);
  const box = await (await p.$('#spread')).boundingBox(); await p.mouse.move(box.x + box.width * 0.62, box.y + 60); await p.waitForTimeout(100); out.hover = await p.evaluate(() => document.getElementById('hover').textContent);
  await p.fill('#g', '1'); await p.fill('#q', '1.1'); await p.waitForTimeout(300); await p.click('#twenty'); await p.waitForTimeout(300);
  await p.screenshot({ path: process.argv[3], fullPage: true }); console.log(JSON.stringify({ errs, out }, null, 1)); await b.close();
})();

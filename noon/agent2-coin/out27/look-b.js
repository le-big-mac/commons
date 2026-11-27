/* look-b.js: the second picture after twelve coins have been added (a visitor, 27 November: "the lines are squeezed into the bottom fifth of the frame").
   cd ~/web && node ~/coin/out27/look-b.js ~/coin/change.html OUT.png */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), c = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const p = await c.newPage(); await p.goto('file://' + process.argv[2]); await p.waitForTimeout(500);
  for (let k = 0; k < 12; k++) { const dis = await p.evaluate(() => document.getElementById('addPlain').disabled); if (dis) break; await p.tap('#addPlain'); await p.waitForFunction(() => !window.__coin.pending); await p.waitForTimeout(450); }
  const info = await p.evaluate(() => { const svg = document.getElementById('chartB'), r = svg.getBoundingClientRect(); const lines = ['lineB-plain', 'lineB-both'].map(id => { const e = document.getElementById(id); if (!e) return null; const q = e.getBoundingClientRect(); return [Math.round(q.top - r.top), Math.round(q.bottom - r.top)]; }); return { coins: document.getElementById('coins').value, h: Math.round(r.height), lines, addPlain: document.getElementById('addPlain').textContent }; });
  console.log(JSON.stringify(info)); await p.evaluate(() => document.getElementById('fig2').scrollIntoView()); await p.locator('#fig2').screenshot({ path: process.argv[3] }); await b.close();
})();

// Does the pace change the picture?  1/63 drawn all at once, drawn quick (one clean walk), and redrawn after a resize.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1500 } }); await p.goto('file://' + path.resolve(process.argv[2])); await p.waitForTimeout(300);
  const ink = () => p.evaluate(() => { const c = document.getElementById('field'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let dark = 0, rust = 0;
    for (let i = 0; i < d.length; i += 4) { if (d[i + 3] > 90 && d[i] < 100 && d[i + 1] < 90 && d[i + 2] < 90) dark++; if (d[i + 3] > 150 && d[i] > 130 && d[i + 1] < 110 && d[i + 2] < 85) rust++; } return { dark, rust }; });
  await p.fill('#num', '1'); await p.fill('#den', '63');
  await p.selectOption('#pace', 'once'); await p.click('#go'); await p.waitForTimeout(300); const once = await ink();
  await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(6800); const quick = await ink(), st = await p.evaluate(() => window.GOSPELSTATE().done);
  await p.setViewportSize({ width: 1001, height: 1500 }); await p.waitForTimeout(300); await p.setViewportSize({ width: 1000, height: 1500 }); await p.waitForTimeout(300); const redrawn = await ink();
  console.log('1/63: all at once ' + JSON.stringify(once) + '; quick (done ' + st + ') ' + JSON.stringify(quick) + '; the quick picture redrawn after a resize ' + JSON.stringify(redrawn));
  await p.locator('.stage').screenshot({ path: path.join(process.argv[3], 'c2b-redrawn.png') });
  await b.close();
})().catch(e => { console.log('STOPPED ' + String(e).slice(0, 300)); process.exit(2); });

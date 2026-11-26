// does pressing Go twice leave anything of the first walk on the canvas?  compare with one quick walk
'use strict'; const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1000, height: 1500 } }); await p.goto('file://' + path.resolve(process.argv[2])); await p.waitForTimeout(400);
  const ink = () => p.evaluate(() => { const c = document.getElementById('field'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 0; i < d.length; i += 4) if (d[i + 3] > 90 && d[i] < 100 && d[i + 1] < 90 && d[i + 2] < 90) n++; return n; });
  await p.fill('#angle', '0'); await p.fill('#inc', '7'); await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(6600); const one = await ink(), s1 = await p.evaluate(() => window.INSPISTATE());
  await p.click('#go'); await p.waitForTimeout(1000); await p.click('#go'); await p.waitForTimeout(6600); const two = await ink(), s2 = await p.evaluate(() => window.INSPISTATE());
  await p.selectOption('#pace', 'once'); await p.click('#go'); await p.waitForTimeout(200); const all = await ink();
  console.log('one quick walk: done', s1.done, 'dark px', one, '; Go, then Go again after 1 s: done', s2.done, 'dots', s2.dots, 'dark px', two, '; all at once: dark px', all); await b.close(); })().catch(e => { console.log('STOPPED ' + String(e).slice(0, 300)); process.exit(2); });

// A first look at the page "Small change": screenshots and what the tiles say.  usage: node shot-change-look.js PAGE.html OUTDIR
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1400 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(400);
  const tiles = () => p.evaluate(() => [...document.querySelectorAll('.tile')].map(t => t.querySelector('.v').textContent + ' | ' + t.querySelector('.d').textContent));
  console.log((await tiles()).join('\n')); console.log(await p.evaluate(() => document.querySelector('#sayA').textContent)); console.log(await p.evaluate(() => document.querySelector('#sayB').textContent));
  await p.screenshot({ path: path.join(out, 'look-1.png'), fullPage: true });
  for (const [i, name] of [[4, 'pence'], [8, 'three'], [1, 'us']]) { await p.selectOption('#preset', String(i)); await p.waitForTimeout(300); console.log('--- ' + name); console.log((await tiles()).join('\n'));
    console.log(await p.evaluate(() => document.querySelector('#sayA').textContent)); console.log(await p.evaluate(() => document.querySelector('#sayB').textContent));
    await p.screenshot({ path: path.join(out, 'look-' + name + '.png'), fullPage: true }); }
  await p.setViewportSize({ width: 380, height: 900 }); await p.waitForTimeout(200); await p.screenshot({ path: path.join(out, 'look-narrow.png'), fullPage: true });
  console.log('errors: ' + JSON.stringify(errs)); await b.close();
})();

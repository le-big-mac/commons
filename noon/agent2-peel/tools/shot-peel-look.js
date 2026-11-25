// A first look at the page "Peeling a cloud".  usage: node shot-peel-look.js PAGE.html OUTDIR
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(600);
  const tiles = () => p.evaluate(() => [...document.querySelectorAll('.tile')].map(t => t.querySelector('.v').textContent + ' | ' + t.querySelector('.d').textContent));
  const say = async () => console.log((await tiles()).join('\n') + '\n' + await p.evaluate(() => document.querySelector('#say1').textContent) + '\n' + await p.evaluate(() => document.querySelector('#say2').textContent));
  await say(); await p.screenshot({ path: path.join(out, 'look-disc.png'), fullPage: true });
  await p.fill('#k', '60'); await p.dispatchEvent('#k', 'input'); await p.waitForTimeout(200); await p.screenshot({ path: path.join(out, 'look-disc-60.png'), fullPage: false });
  await p.selectOption('#shape', 'square'); await p.waitForTimeout(500); await say(); await p.screenshot({ path: path.join(out, 'look-square.png'), fullPage: false });
  await p.click('#stretch'); await p.waitForTimeout(500); await say(); await p.screenshot({ path: path.join(out, 'look-stretched.png'), fullPage: false });
  await p.selectOption('#shape', 'triangle'); await p.waitForTimeout(500); await p.fill('#k', '40'); await p.dispatchEvent('#k', 'input'); await p.waitForTimeout(200); await p.screenshot({ path: path.join(out, 'look-triangle.png'), fullPage: false });
  console.log('errors: ' + JSON.stringify(errs)); await b.close();
})();

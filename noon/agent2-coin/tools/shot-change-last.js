// One more look after everything passes.  usage: node shot-change-last.js PAGE.html OUTDIR
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1400 } });
  await p.goto('file://' + page); await p.waitForTimeout(300);
  await p.fill('#coins', '1, 2'); await p.fill('#L', '3'); await p.click('#apply'); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(out, 'last-tiny.png'), fullPage: false });
  await p.selectOption('#preset', '9'); await p.waitForTimeout(200); await p.fill('#amount', '7'); await p.waitForTimeout(100);
  await p.locator('#fig3').scrollIntoViewIfNeeded(); await p.screenshot({ path: path.join(out, 'last-four.png'), fullPage: false });
  await b.close();
})();

// The coin page's first screen at 360 by 640 and at 390 by 844.   node first360.js PAGE OUTDIR
const { chromium } = require('playwright');
(async () => { const [page, out] = process.argv.slice(2), b = await chromium.launch();
  for (const [w, h] of [[360, 640], [390, 844]]) { const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }), p = await c.newPage(); await p.goto('file://' + page); await p.waitForTimeout(400); await p.screenshot({ path: out + '/first-' + w + '.png' }); await c.close(); }
  await b.close(); console.log('shots written'); })();

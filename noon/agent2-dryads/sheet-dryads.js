// A contact sheet's worth of groves in full leaf.   usage: node sheet-dryads.js PAGE.html OUTDIR SEED...
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 800, height: 420 } });
  for (const seed of process.argv.slice(4)) {
    await p.goto('file://' + page + '#seed=' + seed); await p.reload();
    await p.evaluate(() => { const g = window.__dryads.grove(); window.__dryads.drawAt(g.fallAt - 2.5); });
    await p.screenshot({ path: path.join(out, `leaf-${seed}.png`), clip: { x: 0, y: 0, width: 800, height: 362 } });
  }
  await b.close();
})();

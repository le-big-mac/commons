// Leave the braids page running on its own clock and note its state every minute.   usage: node soak-braid.js PAGE.html MINUTES OUTDIR
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), minutes = +process.argv[3], out = path.resolve(process.argv[4]);
  const b = await chromium.launch({ args: ['--enable-precise-memory-info'] }); const p = await b.newPage({ viewport: { width: 1100, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page);
  console.log('started', new Date().toISOString());
  const end = Date.now() + minutes * 60000; let k = 0, last = null, stalled = 0;
  while (Date.now() < end) {
    await p.waitForTimeout(60000); k++;
    const s = await p.evaluate(() => { const bed = window.__braid.bed, m = bed.braiding(0.0035); let bad = 0; for (let i = 0; i < bed.h.length; i++) if (!(bed.h[i] === bed.h[i])) bad++;
      return { steps: bed.steps, streams: m.streams, wet: m.wet, top: m.top, relief: m.relief, cols: window.__braid.cols, bad, heap: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1e6) : null }; });
    if (last !== null && s.steps <= last) stalled++;
    console.log(`minute ${k}: ${s.steps} steps, ${s.streams.toFixed(1)} threads, ${Math.round(100 * s.wet)}% wet, fullest cell ${Math.round(100 * s.top)}%, relief ${s.relief.toFixed(2)}, record strips ${s.cols}, cells that are not numbers ${s.bad}, heap ${s.heap} MB`);
    last = s.steps;
  }
  await p.screenshot({ path: path.join(out, 'soak-end.png'), fullPage: true });
  console.log('ended', new Date().toISOString(), 'minutes', k, 'steps reached', last, 'minutes with no advance', stalled, 'script errors', JSON.stringify(errs.slice(0, 5)));
  await b.close();
})();

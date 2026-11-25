// Leave the clock page running on the real clock and note every chime it rings.   usage: node soak-quarters.js PAGE.html MINUTES
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), minutes = +process.argv[3];
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }); const p = await b.newPage({ viewport: { width: 900, height: 980 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + page); await p.click('#start');
  console.log('started', new Date().toISOString(), JSON.stringify(await p.evaluate(() => window.__clock.state().next)));
  let rung = 0; const end = Date.now() + minutes * 60000;
  while (Date.now() < end) {
    await p.waitForTimeout(1000);
    const s = await p.evaluate(() => window.__clock.state());
    if (s.rung !== rung) { rung = s.rung; console.log('chime', rung, 'machine clock', new Date().toISOString(), 'page clock', s.time, JSON.stringify(s.playing)); }
  }
  console.log('ended', new Date().toISOString(), 'chimes rung', rung, 'script errors', JSON.stringify(errs)); await b.close();
})();

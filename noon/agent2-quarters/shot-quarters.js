// Headless checks of the clock page.   usage: node shot-quarters.js PAGE.html OUTDIR
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }); const p = await b.newPage({ viewport: { width: 900, height: 980 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  // 1. a pretended time just before a quarter to twelve: start the clock and let it cross the boundary by itself
  await p.goto('file://' + page + '#at=11:44:55'); await p.click('#start'); await p.waitForTimeout(1500);
  const before = await p.evaluate(() => window.__clock.state());
  await p.waitForFunction(() => window.__clock.state().playing !== null, null, { timeout: 12000 });
  await p.waitForTimeout(2500); const during = await p.evaluate(() => window.__clock.state()); await p.screenshot({ path: path.join(out, 'clock-1145.png') });
  console.log('started at a pretended 11:44:55:', JSON.stringify({ before: before.next, rung: before.rung }), '; after the boundary:', JSON.stringify(during));
  // 2. across the hour: 11:59:56 -> twelve o'clock, four rows and twelve strokes
  await p.goto('file://' + page + '#at=11:59:56'); await p.reload(); await p.click('#start');
  await p.waitForFunction(() => window.__clock.state().playing !== null, null, { timeout: 12000 }); await p.waitForTimeout(14500);
  const noon = await p.evaluate(() => window.__clock.state()); await p.screenshot({ path: path.join(out, 'clock-noon.png') });
  console.log('across twelve o\'clock:', JSON.stringify(noon));
  // 3. across midnight: 23:59:57 -> rows 117 to 120 and twelve strokes
  await p.goto('file://' + page + '#at=23:59:57'); await p.reload(); await p.click('#start');
  await p.waitForFunction(() => window.__clock.state().playing !== null, null, { timeout: 12000 });
  console.log('across midnight:', JSON.stringify(await p.evaluate(() => window.__clock.state().playing)));
  // 4. the buttons
  await p.goto('file://' + page + '#at=09:20:00'); await p.reload(); await p.click('#ringnext'); await p.waitForTimeout(700);
  const rn = await p.evaluate(() => window.__clock.state()); await p.click('#stop'); await p.waitForTimeout(200); const hushed = await p.evaluate(() => window.__clock.state().playing);
  console.log('ring the next chime at a pretended 09:20:', JSON.stringify(rn.playing), '; after Hush:', JSON.stringify(hushed), '; the clock was not started:', rn.running === false);
  // 5. the page's own sound for twelve o'clock, with no room, as raw floats
  const b64 = await p.evaluate(async () => { const [L, R] = await window.__clock.offline(12, 0); const f = new Float32Array(L.length * 2); f.set(L, 0); f.set(R, L.length);
    const u = new Uint8Array(f.buffer); let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); });
  fs.writeFileSync(path.join(out, 'page-noon-dry.f32'), Buffer.from(b64, 'base64'));
  console.log('script errors:', JSON.stringify(errs)); await b.close();
})();

// Headless checks of the Dryads page: frames at several times, the page's own sound rendered offline, and the buttons.
// usage: node shot-dryads.js PAGE.html OUTDIR SEED
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [page, out, seed] = [path.resolve(process.argv[2]), path.resolve(process.argv[3]), process.argv[4] || '1'];
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page + '#seed=' + seed);
  const info = await p.evaluate(() => { const g = window.__dryads.grove(); return { duration: g.duration, strikes: g.strikes.length, grown: g.grown, fallAt: g.fallAt, roundsAt: g.roundsAt }; });
  console.log('grove', JSON.stringify(info));
  const times = (process.env.TIMES || `6,30,70,${Math.round(info.grown)},${Math.round(info.fallAt + 8)},${Math.round(info.fallAt + 35)},${Math.round(info.duration - 3)}`).split(',').map(Number);
  for (const t of times) {
    await p.evaluate(t => window.__dryads.seek(t), t); await p.waitForTimeout(120);
    await p.screenshot({ path: path.join(out, `seed${seed}-t${String(t).padStart(3, '0')}.png`) });
  }
  // the sound the page makes, with no room: written as raw 32-bit floats, left then right
  const secs = +(process.env.SECS || 45);
  const b64 = await p.evaluate(async secs => {
    const [L, R] = await window.__dryads.offline(secs, true); const f = new Float32Array(L.length * 2); f.set(L, 0); f.set(R, L.length);
    const u = new Uint8Array(f.buffer); let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s);
  }, secs);
  fs.writeFileSync(path.join(out, `seed${seed}-page-dry.f32`), Buffer.from(b64, 'base64'));
  // the buttons
  await p.evaluate(() => window.__dryads.seek(0)); await p.click('#play'); await p.waitForTimeout(5000);
  const a = await p.evaluate(() => ({ now: window.__dryads.now(), scheduled: window.__dryads.scheduled(), label: document.getElementById('play').textContent, clock: document.getElementById('clock').textContent }));
  await p.click('#play'); await p.waitForTimeout(600); const t1 = await p.evaluate(() => window.__dryads.now()); await p.waitForTimeout(800);
  const c = await p.evaluate(() => ({ now: window.__dryads.now(), label: document.getElementById('play').textContent }));
  const due = await p.evaluate(t => window.__dryads.grove().strikes.filter(s => s.t < t + 1.2).length, a.now);
  console.log('after 5 s of ringing:', JSON.stringify(a), '; strikes due by then:', due);
  console.log('paused:', JSON.stringify(c), 'moved while paused by', (c.now - t1).toFixed(3), 's');
  // the line: click its middle while paused, then ring on from there
  const box = await p.locator('#line').boundingBox(); await p.mouse.click(box.x + box.width / 2, box.y + box.height / 2); await p.waitForTimeout(200);
  const mid = await p.evaluate(() => ({ now: window.__dryads.now(), half: window.__dryads.grove().duration / 2 }));
  const before = await p.evaluate(() => window.__dryads.scheduled()); await p.click('#play'); await p.waitForTimeout(3000);
  const on = await p.evaluate(() => ({ now: window.__dryads.now(), scheduled: window.__dryads.scheduled() }));
  const dueOn = await p.evaluate(([t0, t1]) => [1.05, 1.2].map(a => window.__dryads.grove().strikes.filter(s => s.t >= t0 && s.t < t1 + a).length), [mid.now, on.now]);   // the sound is fed every 0.1 s, 1.2 s ahead
  console.log('clicked the middle of the line:', JSON.stringify(mid), '; rang on for 3 s:', JSON.stringify(on), '; strikes handed over since:', on.scheduled - before, '; due by then, 1.05 s and 1.2 s ahead:', dueOn.join(' and '));
  await p.click('#again'); await p.waitForTimeout(400);
  const d = await p.evaluate(() => ({ hash: location.hash, seed: window.__dryads.grove().seed, now: window.__dryads.now(), label: document.getElementById('play').textContent }));
  console.log('another grove:', JSON.stringify(d));
  console.log('script errors:', JSON.stringify(errs));
  await b.close();
})();

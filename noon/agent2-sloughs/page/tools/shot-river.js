// Headless checks of the Sloughs page: the page's own stepping against the model run in node, stills, the buttons, and its bells rendered offline.
// usage: node shot-river.js PAGE.html OUTDIR SEED CORE.js
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [page, out, seed] = [path.resolve(process.argv[2]), path.resolve(process.argv[3]), +(process.argv[4] || 1)];
  const { River, bellFor } = require(path.resolve(process.argv[5]));
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  let p = await b.newPage({ viewport: { width: 1280, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page + '#seed=' + seed + '&still=1');
  // 1. the page's river against the same model run here, at several times
  const r = new River({ P: 3, DC: 0.4, LX: 100 }); r.seed(seed); const mine = [];
  r.onCut = (t, arc, xs) => mine.push(Object.assign(bellFor(arc, xs[0] / 100), { t, arc }));
  let agree = 0, n = 0;
  for (const t of [5, 14, 18, 25, 32, 40]) {      // not beyond: by t = 60 two builds of the same code have parted in the last digit and it shows
    while (r.now < t - 1e-9) r.step();
    const s = await p.evaluate(t => window.__river.runTo(t), t); n++;
    const ok = s.N === r.N && s.ncut === r.ncut && Math.abs(s.now - r.now) < 1e-9 && Math.abs(s.S - r.sinuosity()) < 1e-3;
    agree += ok ? 1 : 0;
    console.log(`t=${t}: page nodes ${s.N}, cutoffs ${s.ncut}, length/valley ${s.S.toFixed(4)}, lakes showing ${s.lakes}; node ${r.N}, ${r.ncut}, ${r.sinuosity().toFixed(4)}  ${ok ? 'agree' : 'DIFFER'}`);
    await p.screenshot({ path: path.join(out, `seed${seed}-t${String(t).padStart(3, '0')}.png`) });
  }
  console.log(`the page's stepping agrees with the model run in node at ${agree} of ${n} times`);
  const ps = await p.evaluate(() => window.__river.strikes());
  const same = ps.length === mine.length && ps.every((s, i) => s.midi === mine[i].midi && s.pan === mine[i].pan && Math.abs(s.t - mine[i].t) < 1e-9);
  console.log(`bells called for by t=40: page ${ps.length}, node ${mine.length}; the same notes at the same times: ${same}`);
  // 2. the bells of t = 22 to 40, at the steady speed (0.2 units a second), rendered by the page with no room and with it, as raw floats
  const speed = 0.2, list = ps.filter(s => s.t >= 22).map(s => ({ t: (s.t - 22) / speed, midi: s.midi, gain: s.gain, pan: s.pan })), secs = 60;
  fs.writeFileSync(path.join(out, `seed${seed}-bells.json`), JSON.stringify({ seed, speed, from: 22, seconds: secs, strikes: list }));
  for (const dry of [true, false]) {
    const b64 = await p.evaluate(async ([list, secs, dry]) => {
      const [L, R] = await window.__river.offline(list, secs, dry); const f = new Float32Array(L.length * 2); f.set(L, 0); f.set(R, L.length);
      const u = new Uint8Array(f.buffer); let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s);
    }, [list, secs, dry]);
    fs.writeFileSync(path.join(out, `seed${seed}-page-${dry ? 'dry' : 'wet'}.f32`), Buffer.from(b64, 'base64'));
  }
  console.log(`bells in the first ${secs} s of that stretch: ${list.filter(s => s.t < secs).length}`);
  // 3. the page on its own clock, and the buttons
  await p.close(); p = await b.newPage({ viewport: { width: 1280, height: 1000 } }); p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + page + '#seed=' + (seed + 1)); await p.waitForTimeout(6000);
  const a = await p.evaluate(() => window.__river.state());
  console.log('a fresh river left alone for 6 s:', JSON.stringify(a));
  await p.waitForTimeout(6000); const a2 = await p.evaluate(() => window.__river.state());
  console.log('and 6 s more:', JSON.stringify(a2));
  await p.click('#play'); await p.waitForTimeout(300); const t1 = await p.evaluate(() => window.__river.state().now); await p.waitForTimeout(1200);
  const c = await p.evaluate(() => ({ now: window.__river.state().now, label: document.getElementById('play').textContent }));
  console.log('paused:', JSON.stringify(c), 'moved while paused by', (c.now - t1).toFixed(4));
  await p.click('#play'); await p.click('#sound'); await p.waitForTimeout(4000);
  const d = await p.evaluate(() => ({ label: document.getElementById('sound').textContent, pressed: document.getElementById('sound').getAttribute('aria-pressed'), state: window.__river.state() }));
  console.log('bells switched on, 4 s on:', JSON.stringify(d));
  await p.screenshot({ path: path.join(out, `seed${seed + 1}-live.png`) });
  await p.click('#again'); await p.waitForTimeout(500);
  const e = await p.evaluate(() => ({ hash: location.hash, state: window.__river.state() }));
  console.log('a new river:', JSON.stringify(e));
  console.log('script errors:', JSON.stringify(errs));
  await b.close();
})();

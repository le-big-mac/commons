// Film the Sloughs page frame by frame, by the page's own stepping, and have the page render the bells of those frames.
// The film hurries (3 units of time a second) to the first cutoff and then goes at the steady speed (0.2 a second).
// usage: node film-river.js PAGE.html FRAMEDIR SEED SECONDS [FPS]     writes frames, FRAMEDIR/bells.json and FRAMEDIR/sound.f32
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]), seed = process.argv[4], secs = +process.argv[5], fps = +(process.argv[6] || 24);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 778 } });
  await p.goto('file://' + page + '#seed=' + seed + '&still=1');
  const n = Math.ceil(secs * fps); let tau1 = null, t1 = null, t = 0;
  for (let k = 0; k < n; k++) {
    const tau = k / fps;
    t = tau1 === null ? 3 * tau : t1 + 0.2 * (tau - tau1);
    const s = await p.evaluate(t => window.__river.runTo(t), t);
    if (tau1 === null && s.firstCut !== null) { tau1 = tau; t1 = s.now; }
    await p.screenshot({ path: path.join(out, 'f-' + String(k).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92, clip: { x: 0, y: 0, width: 1280, height: 720 } });
    if (k % 400 === 0) console.log('frame', k, 'of', n, 'time', s.now.toFixed(2), 'cutoffs', s.ncut);
  }
  const st = await p.evaluate(() => window.__river.state()), strikes = await p.evaluate(() => window.__river.strikes());
  const list = strikes.map(s => ({ t: +(s.t <= t1 ? tau1 : tau1 + (s.t - t1) / 0.2).toFixed(4), midi: s.midi, gain: s.gain, pan: s.pan, arc: +s.arc.toFixed(2), at: +s.t.toFixed(3) }));
  fs.writeFileSync(path.join(out, 'bells.json'), JSON.stringify({ seed: +seed, seconds: secs, fps, hurriedUntil: tau1, timeThen: t1, timeAtEnd: st.now, cutoffs: st.ncut, strikes: list }));
  const total = secs + 8;
  const b64 = await p.evaluate(async ([list, total]) => {
    const [L, R] = await window.__river.offline(list, total, false); const f = new Float32Array(L.length * 2); f.set(L, 0); f.set(R, L.length);
    const u = new Uint8Array(f.buffer); let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s);
  }, [list, total]);
  fs.writeFileSync(path.join(out, 'sound.f32'), Buffer.from(b64, 'base64'));
  console.log('frames', n, '; hurried until', tau1, 's (time', t1 && t1.toFixed(2), '); time at the end', st.now.toFixed(2), '; cutoffs', st.ncut, '; bells', list.length);
  await b.close();
})();

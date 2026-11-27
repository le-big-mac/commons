const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1100, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(500);
  const out = await p.evaluate(() => {
    const scene = document.getElementById('scene'), rows = [];
    function xy(x, z) { const v = window.THUNDERSTATE().view, r = scene.getBoundingClientRect(); return [r.left + (x - v[0]) / (v[1] - v[0]) * r.width, r.top + (1 - (z - v[2]) / (v[3] - v[2])) * r.height]; }
    function ev(type, x, y) { scene.dispatchEvent(new PointerEvent(type, { clientX: x, clientY: y, pointerId: 1, bubbles: true, cancelable: true })); }
    function setL(x) { const c = xy(x, 0); ev('pointerdown', c[0], c[1] + 3); ev('pointerup', c[0], c[1] + 3); }
    function click(id) { document.getElementById(id).click(); }
    function rec(tag, sound) { const s = window.THUNDERSTATE(); let m = null; if (sound) { const x = window.THUNDERSOUND(1); m = 0; for (let i = 0; i < x.length; i++) { const a = Math.abs(x[i]); if (a > m) m = a; } }
      rows.push({ tag, kind: s.kind, crooked: s.crooked, L: s.listener[0], peak: s.peak, level: s.level, energy: s.energy, early: s.early, ends: s.ends, first: s.first, last: s.last, fh: s.firstHeard, tpeak: s.tpeak, say: s.say, sound: m, nearest: s.nearest, length: s.length }); }
    function draw(pts) { if (!window.THUNDERSTATE().draw) click('b-draw'); let c = xy(pts[0][0], pts[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < pts.length; i++) { c = xy(pts[i][0], pts[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); }
    const places = [300, 500, 1500, 3000, 5000, 8000, 9000], five = [500, 1500, 3000, 5000, 8000];
    let n = 0;
    for (const x of places) { setL(x);
      for (let i = 0; i < 16; i++) { click('b-stroke'); rec('stroke', (n++ % 4) === 0); if (i < 4) { click('jag'); rec('stroke-smooth', false); } }
      click('b-straight'); rec('straight', true); for (let i = 0; i < 3; i++) { click('b-straight'); click('jag'); rec('straight-crooked', false); } }
    for (const x of five) { setL(x);
      for (let i = 0; i < 20; i++) { click('b-bow'); if (i === 0) rec('bow', true); click('jag'); rec('bow-crooked', i < 3); }
      for (let i = 0; i < 20; i++) { click('b-away'); rec('away', i < 3); if (i === 0) { click('jag'); rec('away-smooth', true); } } }
    // by hand, close to the listener
    setL(3000);
    function arcPts(R, a0, a1, step) { const q = []; const n = Math.ceil(R * Math.abs(a1 - a0) * Math.PI / 180 / step); for (let i = 0; i <= n; i++) { const a = (a0 + (a1 - a0) * i / n) * Math.PI / 180; q.push([3000 + R * Math.cos(a), R * Math.sin(a)]); } return q; }
    const hands = { 'arc 300 m': arcPts(300, 150, 60, 40), 'arc 600 m': arcPts(600, 150, 60, 40), 'arc 1 km': arcPts(1000, 150, 60, 50), 'arc 2 km': arcPts(2000, 150, 95, 60), 'arc 3 km': arcPts(3000, 150, 95, 60), 'arc 4 km': arcPts(4000, 140, 95, 60),
      'line 60 m over the head': [[1500, 60], [2000, 60], [2500, 60], [3000, 60], [3500, 60], [4500, 60]], 'line 300 m over the head': [[1000, 300], [2000, 300], [3000, 300], [4000, 300], [5000, 300]],
      'upright 100 m off': [[3100, 4000], [3100, 3000], [3100, 2000], [3100, 1000], [3100, 500], [3100, 100]], 'upright 400 m off': [[3400, 4000], [3400, 2000], [3400, 1000], [3400, 400], [3400, 60]],
      'slant to 150 m': [[5000, 4000], [4000, 2000], [3500, 1000], [3150, 300], [3100, 200]], 'low and far': [[7000, 60], [8000, 60], [9000, 60]] };
    for (const k in hands) { draw(hands[k]); const s = window.THUNDERSTATE(); if (s.crooked) { rec('own-crooked: ' + k, true); click('jag'); rec('own-smooth: ' + k, true); click('jag'); } else { rec('own-smooth: ' + k, true); click('jag'); rec('own-crooked: ' + k, true); click('jag'); } }
    return rows;
  });
  fs.writeFileSync(__dirname + '/states.json', JSON.stringify(out));
  console.log('states', out.length, 'script errors', errs.length, errs.join(' | '));
  await b.close();
})();

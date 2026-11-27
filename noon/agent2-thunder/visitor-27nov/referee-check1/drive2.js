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
    function rec(tag) { const s = window.THUNDERSTATE(); const x = window.THUNDERSOUND(1); let m = 0; for (let i = 0; i < x.length; i++) { const a = Math.abs(x[i]); if (a > m) m = a; }
      rows.push({ tag, kind: s.kind, crooked: s.crooked, L: s.listener[0], peak: s.peak, level: s.level, energy: s.energy, early: s.early, ends: s.ends, first: s.first, last: s.last, fh: s.firstHeard, tpeak: s.tpeak, say: s.say, sound: m, nearest: s.nearest, length: s.length }); }
    function draw(pts) { if (!window.THUNDERSTATE().draw) click('b-draw'); let c = xy(pts[0][0], pts[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < pts.length; i++) { c = xy(pts[i][0], pts[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); }
    // close under an upright stroke
    for (const x of [0, 3, 10, 30, 100, 200]) { setL(x); for (let i = 0; i < 3; i++) { click('b-stroke'); rec('stroke close'); } click('b-straight'); rec('straight close'); }
    setL(3000); click('b-stroke');
    function arcPts(R, a0, a1) { const q = [], n = Math.floor(R * Math.abs(a1 - a0) * Math.PI / 180 / 31); for (let i = 0; i <= n; i++) { const a = (a0 + (a1 - a0) * i / n) * Math.PI / 180; q.push([3000 + R * Math.cos(a), R * Math.sin(a)]); } return q; }
    const list = [[600, 150, 120], [600, 150, 100], [600, 150, 60], [600, 150, 30], [800, 150, 115], [1000, 150, 125], [1000, 150, 120], [1000, 150, 115], [1000, 150, 110], [1000, 150, 100], [1000, 150, 90], [1000, 150, 30], [1500, 150, 125], [1500, 150, 115], [1500, 150, 95], [1500, 150, 30], [2000, 150, 120], [2000, 150, 95], [2000, 150, 40], [3000, 150, 95], [3000, 150, 110], [4000, 140, 95]];
    for (const a of list) { draw(arcPts(a[0], a[1], a[2])); const s = window.THUNDERSTATE(); const tag = 'by hand, bow of ' + (a[1] - a[2]) + ' degrees at ' + a[0] + ' m';
      if (s.kind !== 'own') { rows.push({ tag: tag + ' NOT DRAWN', kind: s.kind, L: s.listener[0], peak: s.peak, level: s.level, say: s.say, sound: null, crooked: s.crooked, energy: 0, early: 0, ends: 0, first: 0, last: 0, fh: 0, tpeak: s.tpeak, nearest: s.nearest, length: 0 }); continue; }
      if (s.crooked) { rec('own-crooked: ' + tag); click('jag'); rec('own-smooth: ' + tag); click('jag'); } else { rec('own-smooth: ' + tag); click('jag'); rec('own-crooked: ' + tag); click('jag'); } }
    return rows;
  });
  fs.writeFileSync(__dirname + '/states2.json', JSON.stringify(out));
  console.log('states', out.length, 'script errors', errs.length, errs.join(' | '));
  await b.close();
})();

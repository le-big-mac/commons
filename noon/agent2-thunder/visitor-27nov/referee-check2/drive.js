const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1100, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(500);
  const out = await p.evaluate(() => {
    const scene = document.getElementById('scene'), rows = []; let n = 0;
    function xy(x, z) { const v = window.THUNDERSTATE().view, r = scene.getBoundingClientRect(); return [r.left + (x - v[0]) / (v[1] - v[0]) * r.width, r.top + (1 - (z - v[2]) / (v[3] - v[2])) * r.height]; }
    function ev(type, x, y) { scene.dispatchEvent(new PointerEvent(type, { clientX: x, clientY: y, pointerId: 1, bubbles: true, cancelable: true })); }
    function setL(x) { const c = xy(x, 0); ev('pointerdown', c[0], c[1] + 3); ev('pointerup', c[0], c[1] + 3); }
    function click(id) { document.getElementById(id).click(); }
    function rec(tag, sound) { const s = window.THUNDERSTATE(); let m = null; if (sound === undefined ? (n++ % 3 === 0) : sound) { const x = window.THUNDERSOUND(1); m = 0; for (let i = 0; i < x.length; i++) { const a = Math.abs(x[i]); if (a > m) m = a; } }
      rows.push({ tag, kind: s.kind, crooked: s.crooked, L: s.listener[0], peak: s.peak, level: s.level, energy: s.energy, early: s.early, ends: s.ends, first: s.first, last: s.last, fh: s.firstHeard, tpeak: s.tpeak, say: s.say, sound: m, loud: window.THUNDERLOUD(s.peak) }); }
    function draw(pts) { if (!window.THUNDERSTATE().draw) click('b-draw'); let c = xy(pts[0][0], pts[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < pts.length; i++) { c = xy(pts[i][0], pts[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); }
    const places = [300, 500, 1500, 3000, 5000, 8000, 9000], five = [500, 1500, 3000, 5000, 8000];
    for (const x of places) { setL(x);
      for (let i = 0; i < (x === 3000 ? 40 : 16); i++) { click('b-stroke'); rec('stroke'); if (i < 4) { click('jag'); rec('stroke-smooth'); } }
      click('b-straight'); rec('straight', true); for (let i = 0; i < 3; i++) { click('b-straight'); click('jag'); rec('straight-crooked'); } }
    for (const x of five) { setL(x);
      for (let i = 0; i < (x === 3000 ? 220 : 20); i++) { click('b-bow'); if (i === 0) rec('bow', true); click('jag'); rec('bow-crooked', i < 3); }
      for (let i = 0; i < 20; i++) { click('b-away'); rec('away', i < 3); if (i === 0) { click('jag'); rec('away-smooth', true); } } }
    for (const x of [0, 3, 10, 30, 100, 200]) { setL(x); for (let i = 0; i < 3; i++) { click('b-stroke'); rec('stroke close', true); } click('b-straight'); rec('straight close', true); }
    setL(3000); click('b-stroke');
    function arcPts(R, a0, a1) { const q = [], k = Math.floor(R * Math.abs(a1 - a0) * Math.PI / 180 / 31); for (let i = 0; i <= k; i++) { const a = (a0 + (a1 - a0) * i / k) * Math.PI / 180; q.push([3000 + R * Math.cos(a), R * Math.sin(a)]); } return q; }
    const list = [[600, 150, 120], [600, 150, 100], [600, 150, 60], [600, 150, 30], [800, 150, 115], [1000, 150, 125], [1000, 150, 120], [1000, 150, 115], [1000, 150, 110], [1000, 150, 105], [1000, 150, 102], [1000, 150, 100], [1000, 150, 98], [1000, 150, 96], [1000, 150, 94], [1000, 150, 90], [1000, 150, 30], [1500, 150, 125], [1500, 150, 115], [1500, 150, 95], [1500, 150, 30], [2000, 150, 120], [2000, 150, 95], [2000, 150, 40], [3000, 150, 95], [3000, 150, 110], [4000, 140, 95]];
    for (const a of list) { draw(arcPts(a[0], a[1], a[2])); const s = window.THUNDERSTATE(); const tag = 'by hand, bow of ' + (a[1] - a[2]) + ' degrees at ' + a[0] + ' m'; if (s.kind !== 'own') { rows.push({ tag: 'NOT DRAWN ' + tag, say: '', peak: 1, level: 1, loud: '', sound: null, L: 0 }); continue; }
      if (s.crooked) { rec('own-crooked: ' + tag, true); click('jag'); rec('own-smooth: ' + tag, true); click('jag'); } else { rec('own-smooth: ' + tag, true); click('jag'); rec('own-crooked: ' + tag, true); click('jag'); } }
    const REF = window.THUNDERREF(), borders = [];
    for (const rel of [1 / 1.06, 1, 1.06, Math.pow(1.05, 4), 9.95, 99.5, 995, Math.pow(9.95, 4), 1e6]) for (const f of [1 - 1e-6, 1 + 1e-6]) { const pk = REF / (rel * f); borders.push([rel, f, pk, window.THUNDERLOUD(pk), 0.9 * Math.min(1, Math.pow(pk / REF, 0.25))]); }
    const odd = [0, 1e-12, 1e9].map(v => [v, String(window.THUNDERLOUD(v))]);
    return { rows, REF, borders, odd, tips: [...document.querySelectorAll('li')].map(li => li.textContent) };
  });
  fs.writeFileSync(__dirname + '/states.json', JSON.stringify(out));
  console.log('states', out.rows.length, 'REF', out.REF, 'script errors', errs.length, errs.join(' | '));
  await b.close();
})();

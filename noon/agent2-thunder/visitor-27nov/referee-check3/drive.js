// my own browser script: states and sentences (part 1), tip buttons from each starting state (part 4)
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
    function rec(tag) { const s = window.THUNDERSTATE(); let m = null; if (n++ % 4 === 0) { const x = window.THUNDERSOUND(1); m = 0; for (let i = 0; i < x.length; i++) { const a = Math.abs(x[i]); if (a > m) m = a; } }
      rows.push({ tag, kind: s.kind, crooked: s.crooked, L: s.listener[0], peak: s.peak, level: s.level, energy: s.energy, early: s.early, ends: s.ends, first: s.first, last: s.last, fh: s.firstHeard, tpeak: s.tpeak, say: s.say, sound: m }); }
    function draw(pts) { if (!window.THUNDERSTATE().draw) click('b-draw'); let c = xy(pts[0][0], pts[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < pts.length; i++) { c = xy(pts[i][0], pts[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); }
    const places = [-1700, -1000, -300, 0, 3, 30, 100, 300, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9700];
    for (const x of places) { setL(x);
      for (let i = 0; i < (x === 3000 ? 38 : 8); i++) { click('b-stroke'); rec('stroke'); if (i < 2) { click('jag'); rec('stroke-smooth'); } }
      click('b-straight'); rec('straight'); for (let i = 0; i < 2; i++) { click('b-straight'); click('jag'); rec('straight-crooked'); }
      for (let i = 0; i < (x === 3000 ? 105 : 5); i++) { click('b-bow'); if (i === 0) rec('bow'); click('jag'); rec('bow-crooked'); }
      for (let i = 0; i < 5; i++) { click('b-away'); rec('away'); if (i === 0) { click('jag'); rec('away-smooth'); } } }
    setL(3000); click('b-stroke');
    function arcPts(R, a0, a1) { const q = [], k = Math.floor(R * Math.abs(a1 - a0) * Math.PI / 180 / 31); for (let i = 0; i <= k; i++) { const a = (a0 + (a1 - a0) * i / k) * Math.PI / 180; q.push([3000 + R * Math.cos(a), R * Math.sin(a)]); } return q; }
    const list = [[600, 150, 120], [600, 150, 100], [600, 150, 60], [600, 150, 30], [800, 150, 115], [1000, 150, 125], [1000, 150, 120], [1000, 150, 115], [1000, 150, 110], [1000, 150, 105], [1000, 150, 102], [1000, 150, 100], [1000, 150, 98], [1000, 150, 96], [1000, 150, 94], [1000, 150, 90], [1000, 150, 30], [1500, 150, 125], [1500, 150, 115], [1500, 150, 95], [1500, 150, 30], [2000, 150, 120], [2000, 150, 95], [2000, 150, 40], [3000, 150, 95], [3000, 150, 110], [4000, 140, 95]];
    const hands = list.map(a => ['bow of ' + (a[1] - a[2]) + ' degrees at ' + a[0] + ' m', arcPts(a[0], a[1], a[2])]).concat([['line 300 m over the head', [[1000, 300], [2000, 300], [3000, 300], [4000, 300], [5000, 300]]], ['upright 400 m off', [[3400, 4000], [3400, 2000], [3400, 1000], [3400, 600]]], ['low and far', [[7000, 60], [8000, 60], [9500, 60]]], ['slant', [[6000, 4000], [5000, 2000], [4000, 1000], [3600, 700]]], ['zigzag', [[500, 4500], [2500, 3000], [800, 2000], [2600, 900]]], ['along the ground far', [[8000, 0], [9000, 0], [9900, 0]]]]);
    for (const h of hands) { const c0 = window.THUNDERSTATE().computed; draw(h[1]); const s = window.THUNDERSTATE(); if (s.kind !== 'own' || s.computed === c0) { rows.push({ tag: 'NOT DRAWN ' + h[0], say: s.say, peak: s.peak, level: s.level, sound: null, L: s.listener[0] }); continue; }
      rec((s.crooked ? 'own-crooked: ' : 'own-smooth: ') + h[0]); click('jag'); rec((s.crooked ? 'own-smooth: ' : 'own-crooked: ') + h[0]); click('jag'); }
    // the page's own function over a fine grid of peaks
    const REF = window.THUNDERREF(), grid = []; for (let i = 0; i <= 24000; i++) { const pk = Math.pow(10, -7 + 8 * i / 24000); grid.push([pk, window.THUNDERLOUD(pk)]); }
    // part 4: the seven tip buttons from each starting state
    const tips = [...document.querySelectorAll('button.tip')], tipWords = tips.map(t => t.textContent), cases = [];
    function brief() { const s = window.THUNDERSTATE(); return { kind: s.kind, crooked: s.crooked, draw: s.draw, playing: s.playing, computed: s.computed, say: s.say.slice(0, 40) + ' ... ' + s.say.slice(s.say.indexOf('It is loudest')), lasts: s.last - (s.firstHeard === null ? s.first : s.firstHeard), peak: s.peak, ends: s.ends }; }
    for (const kind of ['stroke', 'straight', 'bow', 'away', 'own']) for (const crooked of [true, false]) for (const dr of [false, true]) for (const playing of [false, true]) for (let t = 0; t < tips.length; t++) {
      setL(3000); if (kind === 'own') { click('b-stroke'); draw([[500, 4500], [2500, 3000], [800, 2000], [2600, 900]]); } else click('b-' + kind);
      if (window.THUNDERSTATE().crooked !== crooked) click('jag'); if (window.THUNDERSTATE().draw !== dr) click('b-draw'); if (playing) click('strike');
      const before = brief(); tips[t].click(); const after = brief(); if (after.playing) click('strike');
      cases.push({ kind, crooked, dr, playing, t, before, after }); }
    return { rows, REF, grid, tipWords, cases, lis: [...document.querySelectorAll('li')].map(li => li.textContent) };
  });
  fs.writeFileSync(__dirname + '/states.json', JSON.stringify(out));
  console.log('states', out.rows.length, 'grid', out.grid.length, 'tip cases', out.cases.length, 'script errors', errs.length, errs.join(' | '));
  await b.close();
})();

// part 1 (tip buttons, each pressed twice, from 40 starting states) and part 3 (the short form against the sentence), desktop width
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
    function rec(tag) { const s = window.THUNDERSTATE(); rows.push({ tag, kind: s.kind, crooked: s.crooked, L: s.listener[0], peak: s.peak, first: s.first, last: s.last, fh: s.firstHeard, tpeak: s.tpeak, say: s.say, brief: s.brief, html: s.sayHTML, short: window.THUNDERLOUDSHORT(s.peak) }); }
    function draw(pts) { if (!window.THUNDERSTATE().draw) click('b-draw'); let c = xy(pts[0][0], pts[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < pts.length; i++) { c = xy(pts[i][0], pts[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); }
    for (const x of [-1700, -1000, -300, 0, 3, 30, 100, 300, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9700]) { setL(x);
      for (let i = 0; i < 4; i++) { click('b-stroke'); rec('stroke'); if (i < 1) { click('jag'); rec('stroke-smooth'); } }
      click('b-straight'); rec('straight'); click('jag'); rec('straight-crooked');
      click('b-bow'); rec('bow'); click('jag'); rec('bow-crooked'); click('b-bow'); click('jag'); rec('bow-crooked');
      click('b-away'); rec('away'); click('b-away'); rec('away'); click('jag'); rec('away-smooth');
      // while dragging
      const c = xy(x, 0); ev('pointerdown', c[0], c[1] + 3); const c2 = xy(Math.min(9600, x + 400), 0); ev('pointermove', c2[0], c2[1] + 3); rec('DRAGGING'); ev('pointerup', c2[0], c2[1] + 3); rec('after drag'); }
    setL(3000); click('b-stroke');
    function arcPts(R, a0, a1) { const q = [], k = Math.floor(R * Math.abs(a1 - a0) * Math.PI / 180 / 31); for (let i = 0; i <= k; i++) { const a = (a0 + (a1 - a0) * i / k) * Math.PI / 180; q.push([3000 + R * Math.cos(a), R * Math.sin(a)]); } return q; }
    const list = [[600, 150, 120], [600, 150, 100], [600, 150, 60], [800, 150, 115], [1000, 150, 120], [1000, 150, 110], [1000, 150, 105], [1000, 150, 102], [1000, 150, 100], [1000, 150, 98], [1000, 150, 94], [1000, 150, 90], [1000, 150, 30], [1500, 150, 115], [1500, 150, 95], [2000, 150, 95], [3000, 150, 95], [3000, 150, 110], [4000, 140, 95]];
    const hands = list.map(a => ['bow of ' + (a[1] - a[2]) + ' degrees at ' + a[0] + ' m', arcPts(a[0], a[1], a[2])]).concat([['line 300 m over the head', [[1000, 300], [2000, 300], [3000, 300], [4000, 300], [5000, 300]]], ['upright 400 m off', [[3400, 4000], [3400, 2000], [3400, 1000], [3400, 600]]], ['zigzag', [[500, 4500], [2500, 3000], [800, 2000], [2600, 900]]]]);
    for (const h of hands) { const c0 = window.THUNDERSTATE().computed; draw(h[1]); const s = window.THUNDERSTATE(); if (s.kind !== 'own' || s.computed === c0) { rows.push({ tag: 'NOT DRAWN ' + h[0] }); continue; } rec('own: ' + h[0]); click('jag'); rec('own: ' + h[0]); click('jag'); }
    // too short
    const before = window.THUNDERSTATE().brief; draw([[5000, 3000], [5040, 3010], [5080, 3020]]); rec('TOO SHORT'); rows[rows.length - 1].briefBefore = before;
    // tries at a stroke in the shadow: low and far, smooth
    for (const [lx, pts] of [[-1700, [[8000, 300], [8200, 4], [9000, 4], [9900, 4]]], [-1700, [[9000, 250], [9300, 2], [9900, 2]]], [9700, [[-1000, 300], [-1300, 3], [-1950, 3]]], [-1700, [[6000, 300], [6300, 2], [8000, 2], [9900, 2]]]]) { setL(lx); draw(pts); if (window.THUNDERSTATE().crooked) click('jag'); rec('LOW AND FAR'); click('jag'); rec('LOW AND FAR crooked'); click('jag'); }
    // part 1
    const tips = [...document.querySelectorAll('button.tip')], tipWords = tips.map(t => t.textContent), cases = [];
    function brief() { const s = window.THUNDERSTATE(); return { kind: s.kind, crooked: s.crooked, draw: s.draw, playing: s.playing, computed: s.computed, loud: s.say.slice(s.say.indexOf('It is loudest')), brief: s.brief, label: document.getElementById('strike').textContent, lasts: s.last - (s.firstHeard === null ? s.first : s.firstHeard), ends: s.ends }; }
    for (const kind of ['stroke', 'straight', 'bow', 'away', 'own']) for (const crooked of [true, false]) for (const dr of [false, true]) for (const playing of [false, true]) for (let t = 0; t < tips.length; t++) {
      setL(3000); if (kind === 'own') { click('b-stroke'); draw([[500, 4500], [2500, 3000], [800, 2000], [2600, 900]]); } else click('b-' + kind);
      if (window.THUNDERSTATE().crooked !== crooked) click('jag'); if (window.THUNDERSTATE().draw !== dr) click('b-draw'); if (playing) click('strike');
      const before = brief(); tips[t].click(); const a1 = brief(); tips[t].click(); const a2 = brief(); if (a2.playing) click('strike');
      cases.push({ kind, crooked, dr, playing, t, before, a1, a2 }); }
    return { rows, REF: window.THUNDERREF(), tipWords, cases, lis: [...document.querySelectorAll('li')].map(li => li.textContent), head: [...document.querySelectorAll('p')].map(e => e.textContent).filter(s => /Things to try/.test(s)) };
  });
  fs.writeFileSync(__dirname + '/states.json', JSON.stringify(out));
  console.log('states', out.rows.length, 'tip cases', out.cases.length, 'script errors', errs.length, errs.join(' | '));
  await b.close();
})();

// part 1 (taps, half-pixel edges, clicks with a count and no pointer, mouse, keyboard) and part 2 (the short form's room at phone widths)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200))); const res = { strike: [], strikeEdge: [], ground: [], groundEdge: [], gap: [], controls: [], counted: [], other: {}, widths: {} };
  const save = () => fs.writeFileSync(__dirname + '/touch.json', JSON.stringify(res));
  async function init() { await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(400);
    await p.evaluate(() => { window.__ev = []; const name = e => e.id ? '#' + e.id : e.className === 'tip' ? 'tip:' + e.textContent : e.tagName.toLowerCase(); window.__name = name;
      document.addEventListener('click', e => { window.__ev.push(name(e.target)); if (e.target.closest && e.target.closest('a')) e.preventDefault(); }, true);
      document.addEventListener('pointerdown', e => { window.__t0 = e.timeStamp; }, true);
      window.__st = () => { const s = window.THUNDERSTATE(); return { kind: s.kind, crooked: s.crooked, draw: s.draw, playing: s.playing, L: s.listener[0], strikes: s.strikes, computed: s.computed, skip: document.getElementById('skip').checked }; };
      window.__quiet = () => { if (window.THUNDERSTATE().playing) document.getElementById('strike').click(); }; }); }
  await init();
  async function tap(x, y) { const a = await p.evaluate(([x, y]) => { window.__quiet(); window.__ev = []; const e = document.elementFromPoint(x, y); return { under: e ? window.__name(e) : null, st: window.__st() }; }, [x, y]);
    await p.touchscreen.tap(x, y); await p.waitForTimeout(20); const c = await p.evaluate(() => ({ clicks: window.__ev.slice(), st: window.__st() })); return { x, y, under: a.under, clicks: c.clicks, before: a.st, after: c.st }; }
  const r = await p.evaluate(() => { window.scrollTo(0, 0); const c = document.getElementById('scene').getBoundingClientRect(), s = document.getElementById('strike').getBoundingClientRect(), v = window.THUNDERSTATE().view; return { l: c.left, t: c.top, r: c.right, b: c.bottom, w: c.width, h: c.height, s: { l: s.left, t: s.top, r: s.right, b: s.bottom }, groundY: c.top + (1 - (0 - v[2]) / (v[3] - v[2])) * c.height, v }; });
  res.rect = r; const S = r.s, wx = x => r.v[0] + (x - r.l) / r.w * (r.v[1] - r.v[0]);
  for (let y = S.t + 1; y < S.b; y += 3) for (let x = S.l + 1; x < S.r; x += 3) res.strike.push(await tap(x, y));
  for (const y of [S.t - 0.5, S.t + 0.5, S.b - 0.5, S.b + 0.5]) for (let x = S.l - 1.5; x < S.r + 2; x += 3) { const t = await tap(x, y); t.edge = 'row y=' + y; res.strikeEdge.push(t); }
  for (const x of [S.l - 0.5, S.l + 0.5, S.r - 0.5, S.r + 0.5]) for (let y = S.t - 1.5; y < S.b + 2; y += 3) { const t = await tap(x, y); t.edge = 'column x=' + x; res.strikeEdge.push(t); }
  save();
  for (let y = r.groundY + 1; y < r.b; y += 3) for (let x = r.l + 3; x < r.r; x += 9) { const t = await tap(x, y); t.worldX = wx(x); res.ground.push(t); }
  for (const y of [r.groundY - 6.5, r.groundY - 5.5, r.b - 0.5, r.b + 0.5]) for (let x = r.l - 1.5; x < r.r + 2; x += 9) { const t = await tap(x, y); t.worldX = wx(x); t.edge = 'row y=' + y.toFixed(1); res.groundEdge.push(t); }
  for (const x of [r.l - 0.5, r.l + 0.5, r.r - 0.5, r.r + 0.5]) for (let y = r.groundY - 5; y < r.b; y += 3) { const t = await tap(x, y); t.worldX = wx(x); t.edge = 'column x=' + x.toFixed(1); res.groundEdge.push(t); }
  for (let y = r.b + 0.5; y < S.t; y += 1) for (let x = 5; x < 388; x += 9) res.gap.push(await tap(x, y));
  save();
  // a click with a count and no pointer, so long after a press
  const mid = [(S.l + S.r) / 2, (S.t + S.b) / 2];
  for (const base of ['picture', 'strike']) for (const wait of [500, 1000, 1400, 1600, 3000]) { await p.evaluate(() => window.__quiet()); await p.touchscreen.tap(base === 'picture' ? r.l + 180 : mid[0], base === 'picture' ? r.groundY + 8 : mid[1]);
    const o = await p.evaluate(async wait => { await new Promise(f => setTimeout(f, 30)); if (window.THUNDERSTATE().playing) document.getElementById('strike').click(); const dt = wait - (performance.now() - window.__t0); await new Promise(f => setTimeout(f, Math.max(0, dt)));
      const s0 = window.THUNDERSTATE().strikes, e = new MouseEvent('click', { detail: 1, bubbles: true, cancelable: true, view: window }); document.getElementById('strike').dispatchEvent(e); const s = window.THUNDERSTATE(); return { elapsed: e.timeStamp - window.__t0, played: s.strikes - s0, playing: s.playing }; }, wait);
    res.counted.push(Object.assign({ base, wait }, o)); }
  await p.evaluate(() => window.__quiet()); save();
  // a mouse and a keyboard
  const o = res.other; async function mouseClick(x, y) { const a = await p.evaluate(() => { window.__quiet(); window.__ev = []; return window.__st(); }); await p.mouse.click(x, y); await p.waitForTimeout(20); const c = await p.evaluate(() => ({ clicks: window.__ev.slice(), st: window.__st() })); return { clicks: c.clicks, before: a, after: c.st }; }
  o.mouseStrike = []; for (const [x, y] of [mid, [S.l + 1, S.t + 1], [S.r - 1, S.t + 1], [S.l + 1, S.b - 1], [S.r - 1, S.b - 1]]) o.mouseStrike.push(await mouseClick(x, y));
  o.mouseGround = await mouseClick(r.l + 200, r.groundY + 8); o.mouseStrikeAfterGround = await mouseClick(mid[0], mid[1]);
  await tap(r.l + 100, r.groundY + 8); await p.evaluate(() => { window.__quiet(); document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); });
  let tabs = 0, focus = null; while (tabs < 12) { await p.keyboard.press('Tab'); tabs++; focus = await p.evaluate(() => document.activeElement && document.activeElement.id); if (focus === 'strike') break; } o.tabsToStrike = tabs; o.focus = focus; o.keys = [];
  for (const k of ['Enter', 'Enter', 'Space', 'Space']) { const a = await p.evaluate(() => { window.__ev = []; return window.__st(); }); await p.keyboard.press(k); await p.waitForTimeout(20); const c = await p.evaluate(() => ({ clicks: window.__ev.slice(), st: window.__st() })); o.keys.push({ key: k, clicks: c.clicks, before: a, after: c.st }); }
  await p.evaluate(() => window.__quiet());
  const n = await p.evaluate(() => { window.__els = [...document.querySelectorAll('#skip, label, #b-stroke, #b-straight, #b-bow, #b-away, #b-draw, #jag, button.tip, a[href]')]; return window.__els.length; });
  for (let k = 0; k < n; k++) { const q = await p.evaluate(k => { const e = window.__els[k]; e.scrollIntoView({ block: 'center' }); const c = e.getBoundingClientRect(); return { name: window.__name(e) + (e.tagName === 'LABEL' ? '[' + e.textContent.trim().slice(0, 12) + ']' : ''), l: c.left, t: c.top, r: c.right, b: c.bottom }; }, k);
    const mx = (q.l + q.r) / 2, my = (q.t + q.b) / 2;
    for (const [where, x, y] of [['inside', mx, my], ['4 px left', q.l - 4, my], ['4 px right', q.r + 4, my], ['4 px above', mx, q.t - 4], ['4 px below', mx, q.b + 4]]) { if (x < 1 || y < 1 || x > 389 || y > 843) continue; await p.evaluate(k => window.__els[k].scrollIntoView({ block: 'center' }), k); const t = await tap(x, y); t.control = q.name; t.where = where; res.controls.push(t); } }
  save();
  // the short form's room
  for (const w of [320, 360, 390]) { await p.setViewportSize({ width: w, height: 800 }); await init(); await p.waitForTimeout(150);
    res.widths[w] = await p.evaluate(() => { const scene = document.getElementById('scene'), out = [];
      function xy(x, z) { const v = window.THUNDERSTATE().view, r = scene.getBoundingClientRect(); return [r.left + (x - v[0]) / (v[1] - v[0]) * r.width, r.top + (1 - (z - v[2]) / (v[3] - v[2])) * r.height]; }
      function ev(type, x, y) { scene.dispatchEvent(new PointerEvent(type, { clientX: x, clientY: y, pointerId: 1, bubbles: true, cancelable: true })); }
      function setL(x) { const c = xy(x, 0); ev('pointerdown', c[0], c[1] + 3); ev('pointerup', c[0], c[1] + 3); }
      const click = id => document.getElementById(id).click();
      function draw(pts) { if (!window.THUNDERSTATE().draw) click('b-draw'); let c = xy(pts[0][0], pts[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < pts.length; i++) { c = xy(pts[i][0], pts[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); return window.THUNDERSTATE().kind === 'own'; }
      function rec(tag) { const pin = document.getElementById('pin').getBoundingClientRect(), br = document.getElementById('brief'), box = br.getBoundingClientRect(), cs = getComputedStyle(br), sk = document.getElementById('strike').getBoundingClientRect(); const rg = document.createRange(); rg.selectNodeContents(br); const rects = [...rg.getClientRects()], tops = [...new Set(rects.map(q => Math.round(q.top)))], bottom = Math.max(...rects.map(q => q.bottom)), right = Math.max(...rects.map(q => q.right));
        out.push({ tag, pin: pin.height, strikeW: sk.width, strikeLabel: document.getElementById('strike').textContent, box: box.height, room: parseFloat(cs.minHeight), lines: tops.length, below: bottom - box.bottom, right, boxRight: box.right, docW: document.documentElement.scrollWidth, winW: window.innerWidth, chars: br.textContent.length, text: br.textContent, kind: window.THUNDERSTATE().kind }); }
      for (const x of [-1700, 0, 3000, 9700]) { setL(x); click('b-stroke'); rec('stroke'); click('strike'); rec('stroke, playing'); click('strike'); click('jag'); rec('stroke smooth'); click('b-straight'); rec('straight'); click('jag'); rec('straight crooked'); click('b-bow'); rec('bow'); click('jag'); rec('bow crooked'); click('b-away'); rec('away'); click('jag'); rec('away smooth');
        const c = xy(x, 0); ev('pointerdown', c[0], c[1] + 3); const c2 = xy(Math.min(9600, x + 500), 0); ev('pointermove', c2[0], c2[1] + 3); rec('dragging'); ev('pointerup', c2[0], c2[1] + 3); }
      function arcPts(R, a0, a1) { const q = [], k = Math.floor(R * Math.abs(a1 - a0) * Math.PI / 180 / 31); for (let i = 0; i <= k; i++) { const a = (a0 + (a1 - a0) * i / k) * Math.PI / 180; q.push([3000 + R * Math.cos(a), R * Math.sin(a)]); } return q; }
      setL(3000); for (const a of [[1500, 150, 115], [1500, 150, 125], [2000, 150, 95], [2000, 150, 120], [3000, 150, 110]]) { const ok = draw(arcPts(a[0], a[1], a[2])); if (window.THUNDERSTATE().crooked) click('jag'); rec((ok ? 'own smooth bow ' : 'NOT DRAWN ') + a[0]); click('jag'); rec((ok ? 'own crooked bow ' : 'NOT DRAWN ') + a[0]); }
      setL(-1700); for (const pts of [[[8000, 400], [8200, 4], [9000, 4], [9900, 4]], [[9000, 400], [9300, 2], [9900, 2]], [[6000, 400], [6300, 2], [8000, 2], [9900, 2]], [[9900, 5800], [8400, 5000], [9900, 4000], [8400, 3000], [9900, 2000], [8400, 1000], [9900, 400]]]) { const ok = draw(pts); if (window.THUNDERSTATE().crooked) click('jag'); rec(ok ? 'own far smooth' : 'NOT DRAWN far'); click('jag'); rec(ok ? 'own far crooked' : 'NOT DRAWN far'); click('strike'); rec('own far crooked, playing'); click('strike'); }
      return out; }); save(); }
  res.errs = errs; save();
  console.log('taps: strike', res.strike.length, '+ edge', res.strikeEdge.length, '| ground', res.ground.length, '+ edge', res.groundEdge.length, '| gap', res.gap.length, '| controls', res.controls.length, '| counted clicks', res.counted.length, '| errors', errs.length, errs.join(' | '));
  await b.close();
})();

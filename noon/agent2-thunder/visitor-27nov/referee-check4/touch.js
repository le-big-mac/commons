// part 2 (who answers a tap, a mouse, a keyboard) and part 3 (the short form's room at 320, 360, 390 wide)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200))); const res = { strike: [], ground: [], gap: [], controls: [], other: {}, widths: {} };
  async function init() { await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(400);
    await p.evaluate(() => { window.__ev = []; const name = e => e.id ? '#' + e.id : e.className === 'tip' ? 'tip:' + e.textContent : e.tagName.toLowerCase(); window.__name = name;
      document.addEventListener('click', e => { window.__ev.push(name(e.target)); if (e.target.closest && e.target.closest('a')) e.preventDefault(); }, true);
      window.__st = () => { const s = window.THUNDERSTATE(); return { kind: s.kind, crooked: s.crooked, draw: s.draw, playing: s.playing, L: s.listener[0], strikes: s.strikes, computed: s.computed, skip: document.getElementById('skip').checked }; };
      window.__quiet = () => { if (window.THUNDERSTATE().playing) document.getElementById('strike').click(); }; }); }
  await init();
  async function pre(x, y) { return p.evaluate(([x, y]) => { window.__quiet(); window.__ev = []; const e = document.elementFromPoint(x, y); return { under: e ? window.__name(e) : null, st: window.__st() }; }, [x, y]); }
  async function post() { await p.waitForTimeout(20); return p.evaluate(() => ({ clicks: window.__ev.slice(), st: window.__st() })); }
  async function tap(x, y) { const a = await pre(x, y); await p.touchscreen.tap(x, y); const c = await post(); return { x, y, under: a.under, clicks: c.clicks, before: a.st, after: c.st }; }
  const g = async () => p.evaluate(() => { window.scrollTo(0, 0); const c = document.getElementById('scene').getBoundingClientRect(), s = document.getElementById('strike').getBoundingClientRect(), v = window.THUNDERSTATE().view; return { l: c.left, t: c.top, r: c.right, b: c.bottom, w: c.width, h: c.height, s: { l: s.left, t: s.top, r: s.right, b: s.bottom }, groundY: c.top + (1 - (0 - v[2]) / (v[3] - v[2])) * c.height, v }; });
  const r = await g(); res.rect = r;
  for (let y = r.s.t + 1; y < r.s.b; y += 3) for (let x = r.s.l + 1; x < r.s.r; x += 3) res.strike.push(await tap(x, y));
  for (let y = r.groundY + 1; y < r.b; y += 3) for (let x = r.l + 3; x < r.r; x += 9) { const t = await tap(x, y); t.worldX = r.v[0] + (x - r.l) / r.w * (r.v[1] - r.v[0]); res.ground.push(t); }
  for (let y = r.b + 0.5; y < r.s.t; y += 1) for (let x = 5; x < 388; x += 9) res.gap.push(await tap(x, y));
  fs.writeFileSync(__dirname + '/touch.json', JSON.stringify(res));
  // a mouse
  const o = res.other, mid = [(r.s.l + r.s.r) / 2, (r.s.t + r.s.b) / 2];
  async function mouseClick(x, y) { const a = await pre(x, y); await p.mouse.click(x, y); const c = await post(); return { x, y, under: a.under, clicks: c.clicks, before: a.st, after: c.st }; }
  o.mouseStrike = []; for (const [x, y] of [mid, [r.s.l + 2, r.s.t + 2], [r.s.r - 2, r.s.t + 2], [r.s.l + 2, r.s.b - 2], [r.s.r - 2, r.s.b - 2]]) o.mouseStrike.push(await mouseClick(x, y));
  o.mouseGround = await mouseClick(r.l + 200, r.groundY + 8); o.mouseStrikeAfterGround = await mouseClick(mid[0], mid[1]);
  // a mouse: press on the ground, let go over Strike
  { const a = await pre(mid[0], mid[1]); await p.mouse.move(r.l + 150, r.groundY + 8); await p.mouse.down(); await p.mouse.move(mid[0], mid[1], { steps: 4 }); await p.mouse.up(); const c = await post(); o.mouseDragOntoStrike = { clicks: c.clicks, before: a.st, after: c.st }; }
  // a keyboard, the last pointer having gone down on the picture
  await tap(r.l + 100, r.groundY + 8); await p.evaluate(() => { window.__quiet(); document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); });
  let tabs = 0, focus = null; while (tabs < 12) { await p.keyboard.press('Tab'); tabs++; focus = await p.evaluate(() => document.activeElement && document.activeElement.id); if (focus === 'strike') break; }
  o.tabsToStrike = tabs; o.focus = focus; o.keys = [];
  for (const k of ['Enter', 'Enter', 'Space', 'Space']) { const a = await p.evaluate(() => { window.__ev = []; return window.__st(); }); await p.keyboard.press(k); const c = await post(); o.keys.push({ key: k, clicks: c.clicks, before: a, after: c.st }); }
  await p.evaluate(() => window.__quiet());
  // a finger drags the listener, then taps Strike at once
  const cdp = await ctx.newCDPSession(p); const a0 = await pre(mid[0], mid[1]);
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: r.l + 120, y: r.groundY + 8 }] });
  for (let i = 1; i <= 6; i++) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: r.l + 120 + 20 * i, y: r.groundY + 8 }] });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); const afterDrag = await p.evaluate(() => window.__st());
  await p.touchscreen.tap(mid[0], mid[1]); const c1 = await post(); o.tapStrikeAfterDrag = { before: a0.st, afterDrag, clicks: c1.clicks, after: c1.st };
  await p.evaluate(() => window.__quiet()); await p.touchscreen.tap(mid[0], mid[1]); await p.touchscreen.tap(mid[0], mid[1]); const c2 = await post(); o.twoQuickTaps = { clicks: c2.clicks, after: c2.st };
  // near the other controls
  await p.evaluate(() => window.__quiet());
  const n = await p.evaluate(() => { window.__els = [...document.querySelectorAll('#skip, label, #b-stroke, #b-straight, #b-bow, #b-away, #b-draw, #jag, button.tip, a[href]')]; return window.__els.length; });
  for (let k = 0; k < n; k++) { const q = await p.evaluate(k => { const e = window.__els[k]; e.scrollIntoView({ block: 'center' }); const c = e.getBoundingClientRect(); return { name: window.__name(e) + (e.tagName === 'LABEL' ? '[' + e.textContent.trim().slice(0, 12) + ']' : ''), l: c.left, t: c.top, r: c.right, b: c.bottom }; }, k);
    const mx = (q.l + q.r) / 2, my = (q.t + q.b) / 2, pts = [['inside', mx, my], ['4 px left', q.l - 4, my], ['4 px right', q.r + 4, my], ['4 px above', mx, q.t - 4], ['4 px below', mx, q.b + 4]];
    for (const [where, x, y] of pts) { if (x < 1 || y < 1 || x > 389 || y > 843) continue; await p.evaluate(k => window.__els[k].scrollIntoView({ block: 'center' }), k); const t = await tap(x, y); t.control = q.name; t.where = where; res.controls.push(t); } }
  fs.writeFileSync(__dirname + '/touch.json', JSON.stringify(res));
  // the short form's room
  for (const w of [320, 360, 390]) { await p.setViewportSize({ width: w, height: 800 }); await init(); await p.waitForTimeout(150);
    res.widths[w] = await p.evaluate(() => { const scene = document.getElementById('scene'), out = [];
      function xy(x, z) { const v = window.THUNDERSTATE().view, r = scene.getBoundingClientRect(); return [r.left + (x - v[0]) / (v[1] - v[0]) * r.width, r.top + (1 - (z - v[2]) / (v[3] - v[2])) * r.height]; }
      function ev(type, x, y) { scene.dispatchEvent(new PointerEvent(type, { clientX: x, clientY: y, pointerId: 1, bubbles: true, cancelable: true })); }
      function setL(x) { const c = xy(x, 0); ev('pointerdown', c[0], c[1] + 3); ev('pointerup', c[0], c[1] + 3); }
      const click = id => document.getElementById(id).click();
      function rec(tag) { const pin = document.getElementById('pin').getBoundingClientRect(), br = document.getElementById('brief'), b = br.getBoundingClientRect(), row = document.getElementById('strikerow').getBoundingClientRect(), cs = getComputedStyle(br), lh = parseFloat(cs.lineHeight);
        out.push({ tag, pin: pin.height, briefH: b.height, lines: Math.round(br.scrollHeight / lh * 100) / 100, minH: parseFloat(cs.minHeight), overflowX: br.scrollWidth > br.clientWidth + 1, right: b.right, rowRight: row.right, display: cs.display, text: br.textContent, docW: document.documentElement.scrollWidth, winW: window.innerWidth }); }
      for (const x of [-1700, 0, 500, 3000, 8000, 9700]) { setL(x); click('b-stroke'); rec('stroke'); click('jag'); rec('stroke smooth'); click('b-straight'); rec('straight'); click('jag'); rec('straight crooked'); click('b-bow'); rec('bow'); click('jag'); rec('bow crooked'); click('b-away'); rec('away'); click('jag'); rec('away smooth');
        const c = xy(x, 0); ev('pointerdown', c[0], c[1] + 3); const c2 = xy(Math.min(9600, x + 500), 0); ev('pointermove', c2[0], c2[1] + 3); rec('dragging'); ev('pointerup', c2[0], c2[1] + 3); }
      setL(3000); click('b-draw'); let pts = [[500, 4500], [2500, 3000], [800, 2000], [2600, 900]], c = xy(pts[0][0], pts[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < pts.length; i++) { c = xy(pts[i][0], pts[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); rec('own'); click('jag'); rec('own smooth');
      return out; }); }
  res.errs = errs; fs.writeFileSync(__dirname + '/touch.json', JSON.stringify(res));
  console.log('taps: strike', res.strike.length, 'ground', res.ground.length, 'gap', res.gap.length, 'controls', res.controls.length, 'errors', errs.length, errs.join(' | '));
  await b.close();
})();

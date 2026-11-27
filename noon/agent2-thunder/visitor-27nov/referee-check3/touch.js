// my own touch-screen script: 390 by 844, real touch taps through the browser (so that the browser's own choice of target is in play)
const { chromium } = require('playwright'); const fs = require('fs'); const page = process.argv[2], tag = process.argv[3];
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + page); await p.waitForTimeout(500);
  await p.evaluate(() => { window.__ev = []; const name = e => e.id ? '#' + e.id : e.className === 'tip' ? 'tip:' + e.textContent : e.tagName.toLowerCase() + (e.getAttribute && e.getAttribute('for') ? '[for=' + e.getAttribute('for') + ']' : ''); window.__name = name;
    document.addEventListener('click', e => { window.__ev.push(name(e.target)); if (e.target.closest && e.target.closest('a')) e.preventDefault(); }, true);
    window.__st = () => { const s = window.THUNDERSTATE(); return { kind: s.kind, crooked: s.crooked, draw: s.draw, playing: s.playing, L: s.listener[0], strikes: s.strikes, computed: s.computed, skip: document.getElementById('skip').checked, y: window.scrollY }; }; });
  async function tap(x, y) { const pre = await p.evaluate(([x, y]) => { window.__ev = []; const e = document.elementFromPoint(x, y); return { under: e ? window.__name(e) : null, st: window.__st() }; }, [x, y]);
    await p.touchscreen.tap(x, y); await p.waitForTimeout(25); const post = await p.evaluate(() => ({ clicks: window.__ev.slice(), st: window.__st() }));
    if (post.st.playing) await p.evaluate(() => document.getElementById('strike').click());       // stop again, quietly
    return { x, y, under: pre.under, clicks: post.clicks, before: pre.st, after: post.st }; }
  const res = { picture: [], controls: [] };
  const r = await p.evaluate(() => { window.scrollTo(0, 0); const c = document.getElementById('scene').getBoundingClientRect(), s = document.getElementById('strike').getBoundingClientRect(), v = window.THUNDERSTATE().view; return { l: c.left, t: c.top, w: c.width, h: c.height, strikeTop: s.top, strikeLeft: s.left, strikeRight: s.right, groundY: c.top + (1 - (0 - v[2]) / (v[3] - v[2])) * c.height, v }; });
  res.rect = r;
  const ys = []; for (let j = 0; j < 9; j++) ys.push(r.t + 4 + (r.h - 8) * j / 8); for (const d of [2, 5, 8]) ys.push(r.t + r.h - d);
  for (const y of ys) for (let i = 0; i < 13; i++) { const x = r.l + 4 + (r.w - 8) * i / 12; const t = await tap(x, y); t.worldX = r.v[0] + (x - r.l) / r.w * (r.v[1] - r.v[0]); t.ground = y > r.groundY - 6; res.picture.push(t); }
  fs.writeFileSync(__dirname + '/touch-' + tag + '.json', JSON.stringify(res));
  if (tag === 'full') {
    const n = await p.evaluate(() => { window.__els = [...document.querySelectorAll('#strike, #skip, label, #b-stroke, #b-straight, #b-bow, #b-away, #b-draw, #jag, button.tip, a[href]')]; return window.__els.length; });
    for (let k = 0; k < n; k++) { const q = await p.evaluate(k => { const e = window.__els[k]; e.scrollIntoView({ block: 'center' }); const c = e.getBoundingClientRect(); return { name: window.__name(e), l: c.left, t: c.top, r: c.right, b: c.bottom }; }, k);
      const mx = (q.l + q.r) / 2, my = (q.t + q.b) / 2, pts = [['inside', mx, my], ['4 px left', q.l - 4, my], ['4 px right', q.r + 4, my], ['4 px above', mx, q.t - 4], ['4 px below', mx, q.b + 4], ['corner out', q.l - 4, q.t - 4], ['corner out', q.r + 4, q.b + 4]];
      for (const [where, x, y] of pts) { if (x < 1 || y < 1 || x > 389 || y > 843) continue; await p.evaluate(k => window.__els[k].scrollIntoView({ block: 'center' }), k); const t = await tap(x, y); t.control = q.name; t.where = where; res.controls.push(t); } } }
  res.errs = errs; fs.writeFileSync(__dirname + '/touch-' + tag + '.json', JSON.stringify(res)); console.log('touch', tag, 'picture taps', res.picture.length, 'control taps', res.controls.length, 'errors', errs.length);
  await b.close();
})();

// a finger drags the listener, then taps Strike (or another button) after a wait: does the tap count?
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(400); const cdp = await ctx.newCDPSession(p);
  await p.evaluate(() => { window.__ev = []; document.addEventListener('click', e => window.__ev.push((e.target.id || e.target.tagName) + '/detail' + e.detail), true); document.addEventListener('pointerdown', e => window.__ev.push('down:' + (e.target.id || e.target.tagName)), true); });
  const r = await p.evaluate(() => { const c = document.getElementById('scene').getBoundingClientRect(), s = document.getElementById('strike').getBoundingClientRect(), bb = document.getElementById('b-bow').getBoundingClientRect(), v = window.THUNDERSTATE().view; return { l: c.left, gy: c.top + (1 - (0 - v[2]) / (v[3] - v[2])) * c.height + 8, sx: (s.left + s.right) / 2, sy: (s.top + s.bottom) / 2, bx: (bb.left + bb.right) / 2, by: (bb.top + bb.bottom) / 2 }; });
  const st = () => p.evaluate(() => { const s = window.THUNDERSTATE(); return { L: s.listener[0], strikes: s.strikes, playing: s.playing, kind: s.kind, ev: window.__ev.splice(0) }; });
  async function drag(slow) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: r.l + 100, y: r.gy }] }); for (let i = 1; i <= 6; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: r.l + 100 + 20 * i, y: r.gy }] }); if (slow) await p.waitForTimeout(60); } if (slow) await p.waitForTimeout(250); await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); }
  for (const slow of [false, true]) for (const wait of [0, 100, 400, 1000]) for (const target of ['strike', 'b-bow']) {
    await p.evaluate(() => { if (window.THUNDERSTATE().playing) document.getElementById('strike').click(); window.scrollTo(0, 0); window.__ev = []; }); const a = await st(); await drag(slow); const d = await st(); if (wait) await p.waitForTimeout(wait);
    await p.touchscreen.tap(target === 'strike' ? r.sx : r.bx, target === 'strike' ? r.sy : r.by); await p.waitForTimeout(40); const c = await st();
    console.log((slow ? 'slow drag' : 'quick drag'), '| listener', a.L, '->', d.L, '| wait', wait, 'ms | tap on', target, '| events:', c.ev.join(' ') || 'NONE', '| strikes +' + (c.strikes - d.strikes), 'playing', c.playing, 'kind', d.kind, '->', c.kind); }
  // without any drag: a plain tap on Strike, twice with a pause
  await p.evaluate(() => { if (window.THUNDERSTATE().playing) document.getElementById('strike').click(); window.__ev = []; }); await p.waitForTimeout(500); await p.touchscreen.tap(r.sx, r.sy); await p.waitForTimeout(40); const c = await st(); console.log('no drag, tap on strike | events:', c.ev.join(' '), '| playing', c.playing);
  await b.close();
})();

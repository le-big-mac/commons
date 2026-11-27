const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage(); const D = '/home/agent2/thunder/out/look4/';
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(600);
  const c = id => p.evaluate(id => { const q = document.getElementById(id).getBoundingClientRect(); return { x: q.left + q.width / 2, y: q.top + q.height / 2, l: q.left, t: q.top, w: q.width, h: q.height }; }, id);
  let r = await c('b-straight'); await p.touchscreen.tap(r.x, r.y); await p.waitForTimeout(700);
  const s = await c('scene'); await p.touchscreen.tap(s.l + s.w * (61 + 30 * 9) / 362, s.t + s.h - 10); await p.waitForTimeout(700);
  await p.evaluate(() => scrollTo(0, 300)); await p.waitForTimeout(300); await p.screenshot({ path: D + 'n1-straight-9km-trace.png' });
  // tick twice in tip 2
  await p.evaluate(() => { const t = document.querySelectorAll('li')[1].getBoundingClientRect(); scrollBy(0, t.top - 252); }); await p.waitForTimeout(300);
  const tb = re => p.evaluate(re => { const e = [...document.querySelectorAll('li')[1].querySelectorAll('button')].find(x => new RegExp(re).test(x.innerText)); const q = e.getBoundingClientRect(); return { x: q.left + q.width / 2, y: q.top + q.height / 2 }; }, re);
  r = await tb('bow'); await p.touchscreen.tap(r.x, r.y); await p.waitForTimeout(600);
  r = await tb('crooked'); await p.touchscreen.tap(r.x, r.y); await p.waitForTimeout(600); const j1 = await p.evaluate(() => document.getElementById('jag').checked);
  await p.touchscreen.tap(r.x, r.y); await p.waitForTimeout(600); const j2 = await p.evaluate(() => document.getElementById('jag').checked);
  console.log('tick "crooked" in tip 2: after first tap crooked=' + j1 + ', after a second tap crooked=' + j2);
  await b.close();
})().catch(e => { console.log('ERR', e.message); process.exit(1); });

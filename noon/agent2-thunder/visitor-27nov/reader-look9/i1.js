const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage(); const D = '/home/agent2/thunder/out/look9/';
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(1000);
  await p.screenshot({ path: D + 'first.png' });
  const t = await p.evaluate(() => document.body.innerText); const i = t.indexOf('What this is:');
  console.log('PAGE ' + await p.evaluate(() => document.documentElement.scrollHeight + ' high, ' + document.documentElement.scrollWidth + ' wide'));
  console.log('FOOT: ' + t.slice(i));
  console.log('BRIEF: ' + await p.evaluate(() => document.getElementById('brief').innerText));
  await p.evaluate(() => { const r = document.getElementById('b-draw').getBoundingClientRect(); scrollBy(0, r.top - 420); }); await p.waitForTimeout(400);
  const r = await p.evaluate(() => { const q = document.getElementById('b-draw').getBoundingClientRect(); return { x: q.left + q.width / 2, y: q.top + q.height / 2 }; });
  await p.touchscreen.tap(r.x, r.y); await p.waitForTimeout(900);
  console.log('after Draw your own: aria-pressed=' + await p.evaluate(() => document.getElementById('b-draw').getAttribute('aria-pressed')) + '; brief: ' + await p.evaluate(() => document.getElementById('brief').innerText) + '; pinned ' + await p.evaluate(() => { const q = document.getElementById('pin').getBoundingClientRect(); return Math.round(q.top) + '..' + Math.round(q.bottom); }));
  await p.screenshot({ path: D + 'draw.png' });
  await b.close();
})().catch(e => { console.log('ERR', e.message); process.exit(1); });

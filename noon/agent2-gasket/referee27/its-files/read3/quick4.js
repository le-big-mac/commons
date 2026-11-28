const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const R = 'file:///home/agent2/referee-gasket-27/read3/';
  for (const f of ['built.html', 'mF-refuses-above-300.html']) { const c = await b.newContext({ viewport: { width: 1100, height: 800 } }); const p = await c.newPage(); await p.goto(R + f); await p.waitForTimeout(400); await p.fill('#quad', '48, 49, 52, 321'); await p.click('#try'); await p.waitForTimeout(400); console.log(f, '| 48, 49, 52, 321 ->', (await p.textContent('#tsay')).slice(0, 170)); await c.close(); }
  for (const f of ['built.html', 'mG-draw-above-stays-below.html']) { const c = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }); const p = await c.newPage(); await p.goto(R + f); await p.waitForTimeout(400); await p.fill('#quad', '-6, 11, 14, 15'); await p.tap('#try'); await p.waitForTimeout(400); const y0 = await p.evaluate(() => window.scrollY); await p.tap('#show'); await p.waitForTimeout(1500);
    const s = await p.evaluate(() => { const r = document.getElementById('g').getBoundingClientRect(); return { y: window.scrollY, canvasTop: r.top, canvasBottom: r.bottom, h: window.innerHeight, root: window.GasketPage.pack().root.join() }; }); console.log(f, '| Draw it above on a phone: scroll', y0, '->', s.y, '| picture now from', Math.round(s.canvasTop), 'to', Math.round(s.canvasBottom), 'on a screen', s.h, 'high | gasket shown:', s.root); await c.close(); }
  await b.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });

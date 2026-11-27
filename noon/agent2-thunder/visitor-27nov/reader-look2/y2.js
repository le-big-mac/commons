const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage();
  const cdp = await ctx.newCDPSession(p);
  const D = '/home/agent2/reader-front-2/thunder2/';
  const shot = async n => { await p.waitForTimeout(250); await p.screenshot({ path: D + n + '.png' }); };
  const rect = name => p.evaluate(n => { const e = [...document.querySelectorAll('button,label')].find(x => (x.innerText || '').trim().startsWith(n)); if (!e) return null; const r = e.getBoundingClientRect(); const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return { x: r.left + r.width / 2, y: r.top + r.height / 2, top: Math.round(r.top), covered: !(top === e || e.contains(top)), text: e.innerText.trim() }; }, name);
  const info = async () => { const g = await p.evaluate(() => { const q = id => { const r = document.getElementById(id).getBoundingClientRect(); return Math.round(r.top) + '..' + Math.round(r.bottom); }; const st = [...document.querySelectorAll('p,div,span')].filter(e => /after the flash/.test(e.innerText || '')).sort((a, b) => a.innerText.length - b.innerText.length)[0]; const sr = st.getBoundingClientRect(); const tt = [...document.querySelectorAll('li')][0].getBoundingClientRect(); return 'scrollY ' + Math.round(scrollY) + ' scene ' + q('scene') + ' trace ' + q('trace') + ' sentence ' + Math.round(sr.top) + '..' + Math.round(sr.bottom) + ' firstTip ' + Math.round(tt.top) + ' | ' + st.innerText.slice(0, 150); }); const s = await rect('Strike') || await rect('Stop'); return g + ' | Strike/Stop: ' + (s ? s.text + ' y ' + s.top + (s.covered ? ' COVERED' : '') : 'none'); };
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(700);
  const r0 = await rect('Another stroke'); await p.evaluate(d => scrollBy(0, d), r0.top - 215); await p.waitForTimeout(400);
  console.log('A buttons just under the stuck picture: ' + await info()); await shot('v1-buttons-under-picture');
  for (const n of ['A bow about you', 'Pointing away', 'A straight one']) {
    const r = await rect(n); await p.touchscreen.tap(r.x, r.y); await p.waitForTimeout(900);
    const r2 = await rect(n);
    console.log('TAP ' + n + (r.covered ? ' (was covered)' : '') + ': button y ' + r.top + ' -> ' + r2.top + ' | ' + await info()); await shot('v2-' + n.replace(/ /g, ''));
  }
  const c = await rect('crooked'); await p.touchscreen.tap(c.x - 85, c.y); await p.waitForTimeout(800);
  console.log('TAP crooked box: ' + JSON.stringify(c) + ' | ' + await info() + ' | checked ' + await p.evaluate(() => document.getElementById('jag').checked)); await shot('v3-crooked');
  // scroll on so the tips are under the picture
  await p.evaluate(() => { const t = [...document.querySelectorAll('li')][1].getBoundingClientRect(); scrollBy(0, t.top - 215); }); await p.waitForTimeout(400);
  const rb = await rect('A bow about you'); const rc = await rect('crooked');
  console.log('B second tip under the picture: ' + await info() + ' | bow button y ' + rb.top + (rb.covered ? ' COVERED' : '') + ' | crooked y ' + rc.top + (rc.covered ? ' COVERED' : '')); await shot('v4-tips');
  const sw = async (x0, y0, x1, y1) => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0 }] }); for (let i = 1; i <= 10; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * i / 10, y: y0 + (y1 - y0) * i / 10 }] }); await p.waitForTimeout(25); } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await p.waitForTimeout(500); };
  let y0 = await p.evaluate(() => scrollY); await sw(200, 60, 200, 180); console.log('SWIPE DOWN starting on the stuck picture (sky): scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY));
  y0 = await p.evaluate(() => scrollY); await sw(200, 170, 200, 40); console.log('SWIPE UP starting on the stuck picture: scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY) + ' | ' + (await info()).slice(0, 260));
  y0 = await p.evaluate(() => scrollY); await sw(200, 400, 200, 650); console.log('SWIPE DOWN starting below it: scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY));
  await shot('v5-after-swipes');
  await b.close();
})().catch(e => { console.log('ERR', e.message); process.exit(1); });

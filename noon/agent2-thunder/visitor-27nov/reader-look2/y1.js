const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage();
  const cdp = await ctx.newCDPSession(p);
  const D = '/home/agent2/reader-front-2/thunder2/';
  const out = []; const say = s => out.push(s);
  const flush = () => fs.writeFileSync(D + 'out.txt', out.join('\n'));
  const shot = async n => { await p.waitForTimeout(250); await p.screenshot({ path: D + n + '.png' }); };
  const step = async (name, f) => { try { await f(); } catch (e) { say('!! ' + name + ' FAILED: ' + e.message.split('\n')[0]); } flush(); };
  const status = () => p.evaluate(() => { const c = [...document.querySelectorAll('p,div,span')].filter(e => /after the flash/.test(e.innerText || '')).sort((a, b) => a.innerText.length - b.innerText.length)[0]; if (!c) return 'NO STATUS'; const r = c.getBoundingClientRect(); return c.innerText.replace(/\n+/g, ' | ') + ' [status y ' + Math.round(r.top) + '..' + Math.round(r.bottom) + ']'; });
  const geo = () => p.evaluate(() => { const c = document.querySelector('canvas'); const r = c.getBoundingClientRect(); let e = c, pos = ''; while (e && e !== document.body) { const s = getComputedStyle(e).position; if (s === 'sticky' || s === 'fixed') { pos = s + ' on ' + e.tagName + '.' + e.className; break; } e = e.parentElement; } const cs = [...document.querySelectorAll('canvas')].map(k => { const q = k.getBoundingClientRect(); return k.id + ' ' + Math.round(q.top) + '..' + Math.round(q.bottom); }).join(', '); return 'scrollY ' + Math.round(scrollY) + ' canvases: ' + cs + ' size ' + Math.round(r.width) + 'x' + Math.round(r.height) + (pos ? ' (' + pos + ')' : ' (not stuck)'); });
  const boxes = () => p.evaluate(() => [...document.querySelectorAll('input[type=checkbox]')].map(e => (e.closest('label') ? e.closest('label').innerText : e.id).trim() + '=' + e.checked).join(' ; '));
  const swipe = async (x0, y0, x1, y1, steps) => {
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0 }] });
    for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * i / steps, y: y0 + (y1 - y0) * i / steps }] }); await p.waitForTimeout(25); }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await p.waitForTimeout(500);
  };
  const kmx = (bb, km) => bb.x + bb.width * (61 + 30 * km) / 362;
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(800);
  await shot('s1-first');
  say('H ' + await p.evaluate(() => document.documentElement.scrollHeight) + ' W ' + await p.evaluate(() => document.documentElement.scrollWidth));
  say('=== FULL TEXT\n' + await p.evaluate(() => document.body.innerText));
  say('=== CONTROLS\n' + await p.evaluate(() => [...document.querySelectorAll('button,input,canvas,label')].filter(e => e.checkVisibility()).map(e => { const r = e.getBoundingClientRect(); return e.tagName + ':' + String(e.innerText || e.id || e.type || '').replace(/\n/g, ' ').slice(0, 50) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + '@' + Math.round(r.top); }).join('\n')));
  say('=== START: ' + await status() + ' || ' + await geo());
  await step('strike', async () => { await p.locator('button', { hasText: /^Strike/ }).first().tap(); await p.waitForTimeout(2000); await shot('s2-strike'); say('=== AFTER STRIKE: ' + await status()); await p.waitForTimeout(6500); });
  // scroll down to Things to try
  await step('scroll', async () => {
    await p.evaluate(() => { const h = [...document.querySelectorAll('*')].find(e => /^Things to try/.test((e.innerText || '').trim()) && e.children.length === 0) || [...document.querySelectorAll('b,strong,h2,h3,p')].find(e => /^Things to try/.test((e.innerText || '').trim())); const r = h.getBoundingClientRect(); scrollBy(0, r.top - 420); });
    await p.waitForTimeout(400); say('=== SCROLLED to Things to try: ' + await geo()); await shot('s3-scrolled');
  });
  const choose = async (name, tag) => step(name, async () => {
    const bt = p.locator('button', { hasText: name }).first();
    await bt.scrollIntoViewIfNeeded(); await p.waitForTimeout(150);
    const bb0 = await bt.boundingBox(); const g0 = await geo();
    await bt.tap(); await p.waitForTimeout(900);
    const bb1 = await bt.boundingBox();
    say('=== CHOOSE ' + name + ': button y ' + Math.round(bb0.y) + ' -> ' + Math.round(bb1.y) + ' | before ' + g0 + ' | after ' + await geo());
    say('status: ' + await status()); say('boxes: ' + await boxes()); await shot(tag);
  });
  const tick = async (tag) => step('tick', async () => {
    const l = p.locator('label', { hasText: /crooked/i }).first(); await l.scrollIntoViewIfNeeded(); const bb0 = await l.boundingBox(); const g0 = await geo();
    await l.locator('input').tap(); await p.waitForTimeout(800); const bb1 = await l.boundingBox();
    say('--- crooked tapped: label y ' + Math.round(bb0.y) + ' -> ' + Math.round(bb1.y) + ' | before ' + g0 + ' | after ' + await geo() + ' | ' + await boxes());
    say('status: ' + await status()); await shot(tag);
  });
  await choose('A bow about you', 's4-bow'); await tick('s4-bow-crooked');
  await choose('Pointing away', 's5-away'); await tick('s5-away-smooth');
  await choose('A straight one', 's6-straight'); await tick('s6-straight-crooked');
  await choose('Another stroke', 's7-another');
  // press and drag the listener
  await step('press', async () => {
    const c = p.locator('canvas').first(); let bb = await c.boundingBox(); const y = bb.y + bb.height - 12;
    await p.touchscreen.tap(kmx(bb, 0.5), y); await p.waitForTimeout(500); say('=== PRESS 0.5 km: ' + await status());
    await shot('s8-near');
    const y0 = await p.evaluate(() => scrollY);
    await swipe(kmx(bb, 0.5), y - 6, kmx(bb, 8), y - 6, 12);
    say('=== DRAG listener 0.5 -> 8 km (scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY) + '): ' + await status()); await shot('s8-far');
    await swipe(kmx(bb, 8), y - 6, kmx(bb, 3), y - 6, 12);
    say('=== DRAG listener 8 -> 3 km: ' + await status());
  });
  // swipes: on the picture (sky), and below it
  await step('swipes', async () => {
    const c = p.locator('canvas').first(); const bb = await c.boundingBox();
    let y0 = await p.evaluate(() => scrollY); const st0 = await status();
    await swipe(200, bb.y + bb.height * 0.4, 200, bb.y + bb.height * 0.4 - 150, 10);
    say('=== SWIPE UP starting on the picture: scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY) + ' ; status changed: ' + (st0 !== await status()));
    y0 = await p.evaluate(() => scrollY);
    await swipe(200, 700, 200, 500, 10);
    say('=== SWIPE UP starting below the picture (y 700): scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY) + ' || ' + await geo());
    y0 = await p.evaluate(() => scrollY);
    await swipe(200, 500, 200, 700, 10);
    say('=== SWIPE DOWN below the picture: scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY));
    await shot('s9-after-swipes');
  });
  // draw your own
  await step('draw', async () => {
    const bt = p.locator('button', { hasText: 'Draw your own' }).first(); await bt.scrollIntoViewIfNeeded(); await bt.tap(); await p.waitForTimeout(600);
    say('=== DRAW pressed: ' + await geo() + ' | text now has: ' + (await p.evaluate(() => document.body.innerText)).split('\n').filter(l => /draw|drag across/i.test(l)).join(' // ').slice(0, 400));
    await shot('s10-draw-armed');
    const c = p.locator('canvas').first(); const bb = await c.boundingBox(); const y0 = await p.evaluate(() => scrollY);
    await swipe(bb.x + bb.width * 0.25, bb.y + bb.height * 0.25, bb.x + bb.width * 0.45, bb.y + bb.height * 0.82, 14);
    say('drawn (scrollY ' + y0 + ' -> ' + await p.evaluate(() => scrollY) + '): ' + await status() + ' | ' + await boxes()); await shot('s10-drawn');
    await p.locator('button', { hasText: /^Strike/ }).first().tap(); await p.waitForTimeout(1500); await shot('s10-drawn-strike');
  });
  await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await p.waitForTimeout(300); say('=== FOOT: ' + await geo()); await shot('s11-foot');
  flush(); await b.close();
})().catch(e => { console.log('ERR', e.message); process.exit(1); });

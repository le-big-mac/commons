const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage();
  const D = '/home/agent2/reader-front-2/thunder/';
  const out = []; const say = s => out.push(s);
  const shot = async n => { await p.waitForTimeout(250); await p.screenshot({ path: D + n + '.png' }); };
  const step = async (name, f) => { try { await f(); } catch (e) { say('!! ' + name + ' FAILED: ' + e.message.split('\n')[0]); } };
  const status = async () => { const t = await p.evaluate(() => document.body.innerText); const j = t.indexOf('Another stroke'); const i = Math.max(t.lastIndexOf('Strike', j), t.lastIndexOf('Stop', j)); return t.slice(i, j).replace(/\n+/g, ' | '); };
  const geo = async () => p.evaluate(() => { const c = document.querySelector('canvas'); const r = c.getBoundingClientRect(); return 'scrollY ' + Math.round(scrollY) + ' canvasTop ' + Math.round(r.top) + ' canvasBottom ' + Math.round(r.bottom); });
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(800);
  await shot('t1-first');
  const full = await p.evaluate(() => document.body.innerText);
  say('H ' + await p.evaluate(() => document.documentElement.scrollHeight) + ' W ' + await p.evaluate(() => document.documentElement.scrollWidth));
  say('=== FULL TEXT\n' + full);
  say('=== CONTROLS\n' + await p.evaluate(() => [...document.querySelectorAll('button,input,canvas,label,audio')].filter(e => e.checkVisibility()).map(e => { const r = e.getBoundingClientRect(); return e.tagName + ':' + ((e.innerText || e.id || e.type || '') + '').replace(/\n/g, ' ').slice(0, 60) + (e.type === 'checkbox' ? ' checked=' + e.checked : '') + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + '@' + Math.round(r.top) + ' font ' + getComputedStyle(e).fontSize; }).join('\n')));
  await step('strike', async () => {
    await p.locator('button', { hasText: /^Strike/ }).first().tap(); await p.waitForTimeout(2500);
    await shot('t2-strike'); say('=== AFTER STRIKE (2.5 s): ' + await status() + ' || ' + await geo());
    await p.waitForTimeout(6000); await shot('t2b-strike-later'); say('after 8.5 s: ' + await status());
  });
  // drag / press to stand
  await step('stand near', async () => {
    const c = p.locator('canvas').first(); const bb = await c.boundingBox();
    await p.touchscreen.tap(bb.x + 76, bb.y + bb.height - 12); await p.waitForTimeout(500);
    say('=== PRESS near 0.5 km: ' + await status()); await shot('t3-near');
    await p.touchscreen.tap(bb.x + 300, bb.y + bb.height - 12); await p.waitForTimeout(500);
    say('=== PRESS near 8 km: ' + await status()); await shot('t3-far');
  });
  const choose = async (name, tag) => {
    await step(name, async () => {
      const bt = p.locator('button', { hasText: name }).first();
      await bt.scrollIntoViewIfNeeded();
      // put the picture off the top: scroll so the button is near the top of the screen
      await p.evaluate(() => scrollBy(0, 250)); await p.waitForTimeout(200);
      const bb0 = await bt.boundingBox(); const g0 = await geo();
      await bt.tap(); await p.waitForTimeout(900);
      const bb1 = await bt.boundingBox();
      say('=== CHOOSE ' + name + ': before ' + g0 + ' button y ' + Math.round(bb0.y) + ' | after ' + await geo() + ' button y ' + (bb1 ? Math.round(bb1.y) : 'gone'));
      await shot(tag); say('status: ' + await status());
      say('boxes: ' + await p.evaluate(() => [...document.querySelectorAll('input[type=checkbox]')].map(e => (e.closest('label') ? e.closest('label').innerText : e.id).trim() + '=' + e.checked + (e.disabled ? ' (disabled)' : '')).join(' ; ')));
    });
  };
  const tick = async (re, tag) => {
    await step('tick ' + re, async () => {
      const l = p.locator('label', { hasText: re }).first(); await l.scrollIntoViewIfNeeded();
      const g0 = await geo(); await l.locator('input').tap(); await p.waitForTimeout(700);
      say('--- ticked ' + re + ': before ' + g0 + ' | after ' + await geo() + ' | boxes: ' + await p.evaluate(() => [...document.querySelectorAll('input[type=checkbox]')].map(e => (e.closest('label') ? e.closest('label').innerText : e.id).trim() + '=' + e.checked).join(' ; ')));
      say('status: ' + await status()); await shot(tag);
    });
  };
  await choose('A bow about you', 't4-bow');
  await tick(/crooked/i, 't4-bow-crooked');
  await choose('Pointing away', 't5-away');
  await tick(/crooked/i, 't5-away-uncrooked');
  await choose('A straight one', 't6-straight');
  await tick(/crooked/i, 't6-straight-crooked');
  await choose('Another stroke', 't7-another');
  await step('draw', async () => {
    const bt = p.locator('button', { hasText: 'Draw your own' }).first(); await bt.scrollIntoViewIfNeeded(); const g0 = await geo(); await bt.tap(); await p.waitForTimeout(600);
    say('=== DRAW YOUR OWN: before ' + g0 + ' after ' + await geo() + ' status: ' + await status()); await shot('t8-draw');
  });
  await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await shot('t9-foot');
  fs.writeFileSync(D + 'out.txt', out.join('\n'));
  await b.close();
})().catch(e => { console.log('ERR', e.message); process.exit(1); });

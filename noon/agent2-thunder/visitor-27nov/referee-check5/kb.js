// can the keyboard reach Strike and play it?  a fresh page each time, wide and phone
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  for (const [name, opt] of [['wide 1100', { viewport: { width: 1100, height: 900 } }], ['phone 390, touch', { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }]]) {
    const ctx = await b.newContext(opt), p = await ctx.newPage(); await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(400);
    const who = () => p.evaluate(() => { const e = document.activeElement; return e ? (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className === 'tip' ? ':' + e.textContent : '')) : 'none'; });
    const seq = []; for (let i = 0; i < 4; i++) { await p.keyboard.press('Tab'); seq.push(await who()); }
    await p.evaluate(() => document.getElementById('strike').focus()); const f = await who(); const st = () => p.evaluate(() => { const s = window.THUNDERSTATE(); return s.playing + '/' + s.strikes; });
    const a = await st(); await p.keyboard.press('Enter'); await p.waitForTimeout(40); const e1 = await st(); await p.keyboard.press('Enter'); await p.waitForTimeout(40); const e2 = await st(); await p.keyboard.press('Space'); await p.waitForTimeout(40); const s1 = await st();
    // after a press on the picture's ground with the mouse, then Tab from there
    await p.evaluate(() => { if (window.THUNDERSTATE().playing) document.getElementById('strike').click(); document.activeElement.blur(); window.scrollTo(0, 0); });
    const g = await p.evaluate(() => { const c = document.getElementById('scene').getBoundingClientRect(); return [c.left + 150, c.bottom - 6]; }); await p.mouse.click(g[0], g[1]); const seq2 = []; for (let i = 0; i < 3; i++) { await p.keyboard.press('Tab'); seq2.push(await who()); }
    const b0 = await st(); await p.keyboard.press('Enter'); await p.waitForTimeout(40); const b1 = await st();
    console.log(name, '| Tab from a fresh page lands on:', seq.join(' > '), '| Strike focused by script:', f, '| playing/strikes', a, '-> Enter', e1, '-> Enter', e2, '-> Space', s1, '| after a mouse press on the ground, Tab lands on:', seq2.join(' > '), '| then Enter:', b0, '->', b1);
    await ctx.close(); }
  await b.close();
})();

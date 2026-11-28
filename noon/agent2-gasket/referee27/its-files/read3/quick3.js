const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const U = 'file:///home/agent2/referee-gasket-27/read3/built.html';
  { const c = await b.newContext({ viewport: { width: 1600, height: 1100 } }); const p = await c.newPage(); await p.goto(U); await p.waitForTimeout(500);
    await p.evaluate(() => window.scrollTo(0, 0)); const r = await p.evaluate(() => { const r = document.getElementById('g').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; });
    const before = await p.textContent('#gsay');
    await p.mouse.move(r[0] + 500, r[1] + 310); await p.mouse.down(); for (let i = 1; i <= 15; i++) await p.mouse.move(r[0] + 500 + 750 * i / 15, r[1] + 310 + 560 * i / 15); await p.mouse.up(); await p.waitForTimeout(100);
    const st = await p.evaluate(() => ({ view: window.GasketPage.view(), size: window.GasketPage.size(), held: window.GasketPage.drawn().map(c => c[0]), gsay: document.getElementById('gsay').textContent }));
    const v = st.view, W = st.size.W, H = st.size.H, ox = 0, oy = -0.25, R = 0.25;   // the outer circle of (-4,5,20,21) as the page places it: [-4, 0, 1]
    const dx = Math.abs(ox - v.cx) * v.s, dy = Math.abs(oy - v.cy) * v.s, near = Math.hypot(Math.max(dx - W / 2, 0), Math.max(dy - H / 2, 0));
    console.log('canvas', r, '| before:', before); console.log('after dragging the gasket past the bottom right corner:', st.gsay, '| held:', JSON.stringify(st.held), '| by my geometry the nearest point of the picture is', near.toFixed(1), 'px from the outer circle\'s centre, whose radius is', (R * v.s).toFixed(1), 'px');
    await p.screenshot({ path: '/home/agent2/referee-gasket-27/read3/corner.png', clip: { x: r[0], y: r[1], width: r[2], height: r[3] } });
    // the same on (-3,5,8,8) by the page's handle, a little further, and far away
    await p.click('#home'); const s0 = await p.evaluate(() => Object.assign({}, window.GasketPage.view()));
    for (const k of [0.8, 0.95, 1.2]) { await p.evaluate(([cx, cy, s]) => window.GasketPage.setView(cx, cy, s), [s0.cx + 500 / s0.s + k * 0.25, s0.cy + 310 / s0.s + k * 0.25, s0.s]); console.log('  outer circle\'s centre ' + k + ' radii beyond the corner each way:', await p.textContent('#gsay')); }
    await p.click('#home');
    await p.fill('#quad', '0, 0, 0, 0'); await p.click('#try'); const now = await p.textContent('#tsay'); await p.waitForTimeout(200); console.log('four noughts: at once:', JSON.stringify(now), '| then:', await p.textContent('#tsay'));
    await p.fill('#quad', '-1, 2, 2, 3'); await p.selectOption('#upto', '1000000'); await p.click('#try'); const now2 = await p.textContent('#tsay'); console.log('a long look, at once:', JSON.stringify(now2), '| Draw it above disabled meanwhile:', await p.evaluate(() => document.getElementById('show').disabled)); await p.waitForTimeout(300);
    await p.selectOption('#pack', '2'); await p.selectOption('#hi', '1'); console.log('(-1,2,2,3) with squares:', await p.textContent('#lead'), '|', await p.textContent('#gsay'), '|', (await p.textContent('#gkind')).slice(-110));
    await c.close(); }
  { const c = await b.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } }); const p = await c.newPage(); await p.goto(U); await p.waitForTimeout(300); console.log('script off:', JSON.stringify((await p.locator('main').innerText()).slice(0, 520)), '| canvas shown:', await p.locator('#g').isVisible(), '| headings shown:', await p.locator('h2').evaluateAll(hs => hs.map(h => h.textContent + ':' + (h.offsetParent !== null)))); await c.close(); }
  await b.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });

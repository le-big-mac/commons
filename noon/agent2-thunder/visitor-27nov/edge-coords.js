// When the browser hands a tap to a neighbour, what coordinates do the events carry: the finger's, or a point moved into the neighbour?   node edge-coords.js PAGE
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  for (const [dx, dy] of [[8, 3], [2, 10], [8, -3], [46, 3], [130, 8]]) { const p = await ctx.newPage(); await p.goto('file://' + process.argv[2]); await p.waitForTimeout(250);
    const g = await p.evaluate(() => { const k = document.getElementById('strike').getBoundingClientRect(); window.__who = [];
      for (const t of ['pointerdown', 'pointerup', 'touchstart', 'click']) document.addEventListener(t, e => { const q = e.touches && e.touches[0] ? e.touches[0] : e.changedTouches ? e.changedTouches[0] : e; window.__who.push(t + ' ' + (e.target.id || e.target.tagName) + ' (' + q.clientX.toFixed(1) + ', ' + q.clientY.toFixed(1) + ')' + (e.width ? ' w' + e.width.toFixed(0) + ' h' + e.height.toFixed(0) : '')); }, true); return { kl: k.left, kt: k.top }; });
    await p.touchscreen.tap(g.kl + dx, g.kt + dy); await p.waitForTimeout(250);
    console.log('finger at (' + (g.kl + dx).toFixed(1) + ', ' + (g.kt + dy).toFixed(1) + '): ' + (await p.evaluate(() => window.__who.join('; ')))); await p.close(); }
  await b.close();
})();

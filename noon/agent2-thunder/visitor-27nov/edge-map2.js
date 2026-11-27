// The same map, each tap on a fresh page, with what lies under the point and whether the view has moved or zoomed.   node edge-map2.js PAGE
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  for (const dx of [2, 8, 16, 46, 98]) { const row = [];
    for (const dy of [-3, 1, 3, 6, 10, 15]) { const p = await ctx.newPage(); await p.goto('file://' + process.argv[2]); await p.waitForTimeout(250);
      const g = await p.evaluate(() => { const k = document.getElementById('strike').getBoundingClientRect(); window.__who = []; for (const t of ['pointerdown', 'touchstart', 'click']) document.addEventListener(t, e => window.__who.push(t[0] + ':' + (e.target.id || e.target.tagName)), true); return { kl: k.left, kt: k.top }; });
      const x = g.kl + dx, y = g.kt + dy, under = await p.evaluate(([x, y]) => { const e = document.elementFromPoint(x, y); return e.id || e.tagName; }, [x, y]);
      await p.touchscreen.tap(x, y); await p.waitForTimeout(250);
      const r = await p.evaluate(() => [window.__who.join(' '), visualViewport.scale, scrollY, window.THUNDERSTATE().playing]);
      row.push((dy >= 0 ? '+' : '') + dy + ' under=' + under + ' got[' + r[0] + ']' + (r[1] !== 1 ? ' ZOOM ' + r[1] : '') + (r[3] ? ' plays' : '')); await p.close(); }
    console.log('x = Strike left + ' + dx + '\n   ' + row.join('\n   ')); }
  await b.close();
})();

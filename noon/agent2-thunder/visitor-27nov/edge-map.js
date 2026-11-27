// Who answers a tap near the border between the picture's ground and Strike, on a phone?   node edge-map.js PAGE
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }), p = await ctx.newPage();
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(400);
  const g = await p.evaluate(() => { const k = document.getElementById('strike').getBoundingClientRect(), s = document.getElementById('scene').getBoundingClientRect(); return { kl: k.left, kr: k.right, kt: k.top, kb: k.bottom, sb: s.bottom }; });
  console.log('picture ends at ' + g.sb.toFixed(1) + '; Strike from ' + g.kt.toFixed(1) + ' to ' + g.kb.toFixed(1) + ', x ' + g.kl.toFixed(0) + ' to ' + g.kr.toFixed(0));
  await p.evaluate(() => { window.__who = []; document.addEventListener('pointerdown', e => window.__who.push(e.target.id || e.target.tagName), true); });
  const who = async () => { const w = await p.evaluate(() => { const q = window.__who.slice(); window.__who.length = 0; return q; }); return w.join('+') || 'nobody'; };
  for (const x of [g.kl + 2, g.kl + 8, g.kl + 16, (g.kl + g.kr) / 2, g.kr - 16, g.kr - 8, g.kr - 2, g.kr + 6, g.kr + 30]) { const row = [];
    for (const dy of [-10, -6, -3, -1, 1, 3, 6, 10, 15, 20, 30]) { await p.touchscreen.tap(x, g.kt + dy); await p.waitForTimeout(200); row.push((dy >= 0 ? '+' : '') + dy + ':' + await who());
      if (await p.evaluate(() => window.THUNDERSTATE().playing)) { await p.evaluate(() => document.getElementById('strike').click()); await p.waitForTimeout(100); await who(); } }
    console.log('x ' + x.toFixed(0) + '  ' + row.join('  ')); }
  await b.close();
})();

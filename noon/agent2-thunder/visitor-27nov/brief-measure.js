// The short form beside Strike on a phone: how tall does it get, over many states and three widths?   node brief-measure.js PAGE OUTDIR
const { chromium } = require('playwright');
(async () => {
  const [page, out] = process.argv.slice(2), b = await chromium.launch();
  for (const [W, H] of [[390, 844], [360, 640], [320, 568]]) {
    const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }), p = await ctx.newPage();
    await p.goto('file://' + page); await p.waitForTimeout(400);
    let tall = 0, longest = '', n = 0; const hs = {};
    const read = async () => { const q = await p.evaluate(() => { const e = document.getElementById('brief'), r = document.createRange(); r.selectNodeContents(e); return [r.getBoundingClientRect().height, e.textContent, e.getBoundingClientRect().height, document.getElementById('pin').getBoundingClientRect().height, e.getBoundingClientRect().right]; });
      n++; hs[q[0].toFixed(0)] = (hs[q[0].toFixed(0)] || 0) + 1; if (q[0] > tall || (q[0] === tall && q[1].length > longest.length)) { tall = q[0]; longest = q[1]; } return q; };
    let last;
    for (const k of ['b-stroke', 'b-straight', 'b-bow', 'b-away']) for (const on of [false, true]) for (let i = 0; i < 4; i++) for (const x of [0.12, 0.3, 0.5, 0.7, 0.93]) {
      await p.evaluate(([k, on]) => { document.getElementById(k).click(); const j = document.getElementById('jag'); if (j.checked !== on) j.click(); }, [k, on]);
      const g = await p.evaluate(() => { const sc = document.getElementById('scene').getBoundingClientRect(); return [sc.left, sc.width, sc.bottom]; });
      await p.evaluate(() => window.scrollTo(0, 0)); await p.touchscreen.tap(g[0] + x * g[1], g[2] - 5); await p.waitForTimeout(40); last = await read(); }
    await p.screenshot({ path: out + '/brief-' + W + '.png' });
    const worst = await p.evaluate(() => { const e = document.getElementById('brief'), r = document.createRange(), hs = []; for (const t of ['Your own stroke, crooked. First sound 28.9\u00a0s, from 9.9\u00a0km; lasts 12.3\u00a0s, loudest 10.7\u00a0s\u00a0in; about 12,000 times less pressure than the bow\u2019s crack.', 'Your own stroke, crooked. First sound 28.9\u00a0s, from 9.9\u00a0km; lasts 174.9\u00a0s, loudest 150.3\u00a0s\u00a0in; about 110,000 times less pressure than the bow\u2019s crack.']) { e.textContent = t; r.selectNodeContents(e); hs.push(r.getBoundingClientRect().height.toFixed(0)); } return hs.join(', ') + ' px in a box of ' + e.getBoundingClientRect().height.toFixed(0); });
    console.log('   two made-up longest texts: ' + worst);
    console.log(W + ' wide: ' + n + ' states; text heights ' + JSON.stringify(hs) + '; box ' + last[2].toFixed(0) + ' px, pin ' + last[3].toFixed(0) + ' px of ' + H + ' (' + (100 * last[3] / H).toFixed(0) + '%); right edge ' + last[4].toFixed(0) + '; tallest: ' + longest);
    await ctx.close(); }
  await b.close();
})();

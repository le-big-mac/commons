// Which elements reach past the right edge of a phone's screen?   node wide.js PAGE [WIDTH]
const { chromium } = require('playwright');
(async () => {
  const W = Number(process.argv[3] || 390), b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: W, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }), p = await ctx.newPage();
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(500);
  const r = await p.evaluate(WIDE => [...document.querySelectorAll('body *')].map(e => [e, e.getBoundingClientRect()]).filter(q => q[1].right > WIDE + 0.5 && q[1].width > 0).map(q => q[0].tagName + '#' + q[0].id + '.' + String(q[0].className.baseVal || q[0].className).slice(0, 20) + ' right ' + q[1].right.toFixed(0) + ' width ' + q[1].width.toFixed(0)).slice(0, 14), W);
  console.log('scrollWidth ' + await p.evaluate(() => document.documentElement.scrollWidth) + ' of ' + W + '\n' + r.join('\n')); await b.close();
})();

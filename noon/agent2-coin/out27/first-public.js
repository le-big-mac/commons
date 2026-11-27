/* first-public.js: what a phone's first screen holds on the page as built for the public site, which has a line above it saying who wrote it
   (four phones since the evening of 27 November: 390 by 844, 360 by 640, 320 by 568, and one held sideways; and where the key to the rings stands).
   cd ~/web && node ~/coin/out27/first-public.js PAGE.html OUT-PREFIX      (prints one JSON object; writes OUT-PREFIX-390.png and -360.png) */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), o = {};
  for (const [w, h] of [[390, 844], [360, 640], [320, 568], [844, 390]]) {
    const cx = await b.newContext({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }), q = await cx.newPage(); await q.goto('file://' + process.argv[2]); await q.waitForTimeout(600);
    o[w + 'x' + h] = await q.evaluate(() => { const r = e => { const x = e.getBoundingClientRect(); return [Math.round(x.top), Math.round(x.bottom)]; }; const line = document.body.firstElementChild;
      return { line: line && /Written by Noon/.test(line.textContent) ? r(line) : null, title: r(document.querySelector('h1')), amountBox: r(document.getElementById('amount')), plain: r(document.getElementById('way-plain')), firstRing: r(document.querySelector('#way-plain .coin')), greedy: r(document.getElementById('way-greedy')), both: r(document.getElementById('way-both')), key: document.getElementById('ringkey') ? r(document.getElementById('ringkey')) : null, screen: window.innerHeight }; });
    if (w === 390 || w === 360) await q.screenshot({ path: process.argv[3] + '-' + w + '.png' }); await cx.close(); }
  console.log(JSON.stringify(o)); await b.close();
})();

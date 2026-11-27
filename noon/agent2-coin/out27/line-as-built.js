/* line-as-built.js: the words of the line above this page as built for the public site, at a phone's size and at a desk's, and the links' sizes.
   cd ~/web && node ~/coin/out27/line-as-built.js BUILT-PAGE.html [BUILT-EARLIER-COPY.html]   (prints JSON) */
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(), o = {};
  for (const f of process.argv.slice(2)) { const name = f.split('/').pop(); o[name] = {};
    for (const [w, h, phone] of [[390, 844, true], [360, 640, true], [320, 568, true], [844, 390, true], [760, 900, false], [761, 900, false], [1280, 800, false]]) { const c = await b.newContext({ viewport: { width: w, height: h }, isMobile: phone, hasTouch: phone }), p = await c.newPage(); await p.goto('file://' + f); await p.waitForTimeout(250);
      o[name][w + 'x' + h] = await p.evaluate(() => { const e = document.querySelector('p.noon-by'), q = e.getBoundingClientRect(); return { words: e.innerText.replace(/\s+/g, ' ').trim(), height: Math.round(q.height), links: [...e.querySelectorAll('a')].filter(a => a.getBoundingClientRect().width > 0).map(a => { const t = a.getBoundingClientRect(); return [a.textContent, Math.round(t.width), Math.round(t.height)]; }) }; }); await c.close(); } }
  console.log(JSON.stringify(o, null, 1)); await b.close(); })();

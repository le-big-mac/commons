/* layout.js: where the things on the coin page's first screen stand, on a phone.   cd ~/web && node ~/coin/out27/layout.js PAGE.html W H */
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(), w = Number(process.argv[3] || 360), h = Number(process.argv[4] || 640);
  const c = await b.newContext({ viewport: { width: w, height: h }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }), p = await c.newPage(); await p.goto('file://' + process.argv[2]); await p.waitForTimeout(500);
  const r = await p.evaluate(() => { const out = []; const add = (name, e) => { if (!e) return; const q = e.getBoundingClientRect(), s = getComputedStyle(e); out.push(name + ': ' + Math.round(q.top) + ' to ' + Math.round(q.bottom) + ' (' + Math.round(q.height) + '; margins ' + s.marginTop + ' ' + s.marginBottom + '; padding ' + s.paddingTop + ' ' + s.paddingBottom + '; font ' + s.fontSize + '/' + s.lineHeight + ')'); };
    add('line above', document.querySelector('p.noon-by')); add('main or wrapper', document.querySelector('main') || document.body.children[0]); add('h1', document.querySelector('h1')); add('lead', document.getElementById('lead')); add('fig0', document.getElementById('fig0'));
    [...document.querySelectorAll('#fig0 > *')].forEach((e, i) => add('  fig0 child ' + i + ' <' + e.tagName.toLowerCase() + (e.className ? '.' + e.className : '') + '>', e));
    add('h2 before fig3', document.getElementById('fig3').previousElementSibling); add('fig3', document.getElementById('fig3'));
    [...document.querySelectorAll('#fig3 > *')].forEach((e, i) => add('  fig3 child ' + i + ' <' + e.tagName.toLowerCase() + (e.className ? '.' + e.className : '') + (e.id ? '#' + e.id : '') + '>', e));
    add('way-plain', document.getElementById('way-plain')); add('first ring', document.querySelector('#way-plain .coin')); add('body', document.body); return out; });
  console.log(r.join('\n')); await b.close(); })();

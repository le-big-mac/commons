// shot-svg.js: an SVG opened in a headless browser: a picture of it, and the real box of every line of words (none may leave the picture or overlap another).
// node shot-svg.js FILE.svg WIDTH HEIGHT OUT.png
const { chromium } = require('playwright');
(async () => {
  const [file, w, h, out] = process.argv.slice(2); const W = +w, H = +h;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + file);
  const boxes = await p.evaluate(() => [...document.querySelectorAll('text')].map(t => { const r = t.getBBox(); return { t: t.textContent, x: r.x, y: r.y, w: r.width, h: r.height }; }));
  const outside = boxes.filter(q => q.x < 0 || q.y < 0 || q.x + q.w > W || q.y + q.h > H).map(q => q.t);
  const hit = []; for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) { const a = boxes[i], c = boxes[j]; if (a.x < c.x + c.w && c.x < a.x + a.w && a.y < c.y + c.h && c.y < a.y + a.h) hit.push(a.t + ' / ' + c.t); }
  await p.screenshot({ path: out });
  console.log('script errors:', errs.length, '| lines of words:', boxes.length, '| outside the picture:', JSON.stringify(outside), '| overlapping:', JSON.stringify(hit));
  console.log(outside.length === 0 && hit.length === 0 && errs.length === 0 ? 'PICTURE: ok' : 'PICTURE: FAULTS');
  await b.close();
})();

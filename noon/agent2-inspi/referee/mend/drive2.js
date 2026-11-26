// Referee's drive of the mended cases only (read-only on the page).
'use strict';
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]);
  const b = await chromium.launch();
  const run = async (w, h, cases) => {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    const errs = []; p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + page); await p.waitForTimeout(500);
    for (const [a, i] of cases) {
      await p.fill('#angle', a); await p.fill('#inc', i); await p.waitForTimeout(80);
      let s = await p.evaluate(() => window.INSPISTATE());
      if (!s.valid) { console.log(w + 'px', JSON.stringify([a, i]), 'REFUSED | say:', s.say); continue; }
      await p.selectOption('#pace', 'once'); await p.click('#go'); await p.waitForTimeout(250);
      s = await p.evaluate(() => window.INSPISTATE());
      const g = s.guide, v = s.view; let over = null;
      if (g && g.kind === 'circle' && v) over = Math.max(0 - (v.ox + v.k * (g.cx - g.r)), (v.ox + v.k * (g.cx + g.r)) - s.W, 0 - (v.oy - v.k * (g.cy + g.r)), (v.oy - v.k * (g.cy - g.r)) - s.H);
      const pix = await p.evaluate(() => { const c = document.getElementById('field'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let edgeRust = 0, rust = 0;
        for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const k = 4 * (y * c.width + x), r = d[k], gg = d[k + 1], bl = d[k + 2], al = d[k + 3]; const edge = x < 2 || y < 2 || x >= c.width - 2 || y >= c.height - 2;
          if (al > 40 && r > 130 && gg < 110 && bl < 85) { rust++; if (edge) edgeRust++; } } return { rust, edgeRust, w: c.width, h: c.height }; });
      console.log(w + 'px', JSON.stringify([a, i]), '| SAY:', s.say, '| REPORT:', s.report, '| dots', s.dots, '| guide', g ? g.kind : null, '| circle outside canvas by (state)', over === null ? null : over.toFixed(1), '| rust px', pix.rust, 'at edge', pix.edgeRust, '| canvas', pix.w, pix.h, '| page fails', (s.fails || []).length);
      await p.screenshot({ path: path.join(process.argv[3], 'm-' + w + '-' + a.replace(/[^0-9a-z]/gi, '_') + '-' + i.replace(/[^0-9a-z]/gi, '_') + '.png') });
    }
    const key = await p.evaluate(() => { const c = document.getElementById('ramp'); return c && c.parentElement ? c.parentElement.textContent : null; });
    const mapsay = await p.evaluate(() => { const t = document.body.innerText; const k = t.indexOf('whole-degree'); return k < 0 ? null : t.slice(Math.max(0, k - 200), k + 260); });
    const sw = await p.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]);
    console.log(w + 'px KEY:', JSON.stringify(key), '| MAP SENTENCE:', JSON.stringify(mapsay), '| page width', sw, '| script errors', errs.length);
    await p.close();
  };
  await run(1000, 1500, [['25', '210'], ['0.1', '0'], ['10', '20'], ['22.5', '45'], ['.5', '20'], ['−5', '20'], ['1234567', '20'], ['1e9', '20'], ['312', '144'], ['155', '2']]);
  await run(320, 700, [['312', '144'], ['25', '210']]);
  await b.close();
})();

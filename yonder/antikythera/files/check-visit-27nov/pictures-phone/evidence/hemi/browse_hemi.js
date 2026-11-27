// Opens the built page on the half of the Earth at several widths with the headless browser and reports which file each picture shows.
// No network: every request that is not a local file is refused. Writes screenshots into ./shots only.
const { chromium } = require('/home/agent3/web/node_modules/playwright');
const fs = require('fs');
const FILE = '/home/agent3/site/pic-preview-hemi/hemispheres/index.html';
const SIZES = [[390, 844, 1], [390, 844, 3], [520, 844, 1], [521, 844, 1], [1000, 800, 1]];
const HERE = '/home/agent3/site/check-pictures-phone/hemi';
(async () => {
  const browser = await chromium.launch();
  const out = [];
  try {
    for (const [w, h, dpr] of SIZES) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
      await ctx.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
      const page = await ctx.newPage();
      await page.goto('file://' + FILE);
      await page.waitForTimeout(300);
      // first as the page opens (folds closed): which pictures are in the open text, and what do they show
      const closed = await page.evaluate(() => [...document.querySelectorAll('img')].map(i => {
        let e = i.parentElement, hidden = false; while (e) { if (e.tagName === 'DETAILS' && !e.open) hidden = true; e = e.parentElement; }
        return { src: i.getAttribute('src'), hidden, shown: i.currentSrc.split('/').slice(-1)[0] };
      }));
      // then open the section on people by its heading, as a visitor would, and after that every other fold
      await page.locator('summary', { hasText: 'The half with the most people' }).click();
      await page.waitForTimeout(300);
      await page.evaluate(() => { document.querySelectorAll('details').forEach(d => { d.open = true; }); });
      await page.waitForTimeout(300);
      await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))); });
      const rows = await page.evaluate(() => [...document.querySelectorAll('img')].map(i => {
        const det = []; let e = i.parentElement;
        while (e) { if (e.tagName === 'DETAILS') det.push(e.querySelector(':scope > summary').textContent.trim()); e = e.parentElement; }
        const fig = i.closest('figure'); const a = fig ? fig.querySelector('a.fullsize') : null;
        const r = i.getBoundingClientRect();
        return { src: i.getAttribute('src'), shown: i.currentSrc.split('/').slice(-1)[0], inPicture: i.parentElement.tagName === 'PICTURE', folded: det.reverse().join(' > ') || '(open text)',
                 natural: i.naturalWidth + 'x' + i.naturalHeight, drawn: Math.round(r.width * 10) / 10 + 'x' + Math.round(r.height * 10) / 10, link: a ? a.getAttribute('href') : null };
      }));
      const sizes = await page.evaluate(() => { const c = document.querySelector('figcaption'); const p = document.querySelector('h2 + p'); return { caption: getComputedStyle(c).fontSize, text: getComputedStyle(p).fontSize, scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth }; });
      out.push({ width: w, dpr, sizes, closed, rows });
      if (w === 390 || w === 1000) {
        const n = await page.$$eval('picture', a => a.length);
        for (let k = 0; k < n; k++) {
          const fig = await page.evaluateHandle(k => document.querySelectorAll('picture')[k].closest('figure'), k);
          await fig.asElement().screenshot({ path: `${HERE}/shots/fig${k + 1}-${w}-dpr${dpr}.png` });
          if (w === 390 && dpr === 1) {
            await page.evaluate(k => { document.querySelectorAll('picture')[k].scrollIntoView({ block: 'start' }); window.scrollBy(0, -20); }, k);
            await page.waitForTimeout(200);
            await page.screenshot({ path: `${HERE}/shots/screen${k + 1}-390x844.png` });
          }
        }
      }
      await ctx.close();
    }
  } finally { await browser.close(); }
  fs.writeFileSync(`${HERE}/out/browse_hemi.json`, JSON.stringify(out, null, 1));
  for (const o of out) {
    console.log(`\n== at ${o.width} wide, ${o.dpr} device pixels to one; text ${o.sizes.text}, caption ${o.sizes.caption}; page scroll width ${o.sizes.scrollW} of ${o.sizes.clientW}`);
    console.log('  as the page opens: ' + o.closed.map(c => `${c.src.split('/').pop()}${c.hidden ? ' (in a closed fold)' : ''} -> ${c.shown || '(not loaded)'}`).join('; '));
    for (const r of o.rows) console.log(`  src=${r.src}  SHOWN=${r.shown}  in<picture>=${r.inPicture}  natural=${r.natural} drawn=${r.drawn}  section: ${r.folded}  link=${r.link}`);
  }
})();

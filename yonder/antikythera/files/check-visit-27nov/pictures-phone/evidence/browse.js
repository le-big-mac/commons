// Opens the two built pages at several widths with the headless browser and reports which file each picture shows.
// No network: every request that is not a local file is refused. Writes screenshots into ./shots only.
const { chromium } = require('/home/agent3/web/node_modules/playwright');
const fs = require('fs');
const PAGES = { antikythera: '/home/agent3/site/pic-preview/antikythera/index.html', handshake: '/home/agent3/site/pic-preview/handshake/index.html' };
const SIZES = [[390, 844, 1], [390, 844, 3], [520, 844, 1], [521, 844, 1], [1000, 800, 1]];
const HERE = '/home/agent3/site/check-pictures-phone';
(async () => {
  const browser = await chromium.launch();
  const out = [];
  try {
    for (const [name, file] of Object.entries(PAGES)) {
      for (const [w, h, dpr] of SIZES) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
        await ctx.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
        const page = await ctx.newPage();
        await page.goto('file://' + file);
        // open every folded section so that every picture loads and can be measured
        await page.evaluate(() => { document.querySelectorAll('details').forEach(d => { d.open = true; }); });
        await page.waitForTimeout(400);
        await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))); });
        const rows = await page.evaluate(() => [...document.querySelectorAll('img')].map(i => {
          const det = []; let e = i.parentElement;
          while (e) { if (e.tagName === 'DETAILS') det.push(e.querySelector(':scope > summary').textContent.trim()); e = e.parentElement; }
          const fig = i.closest('figure'); const a = fig ? fig.querySelector('a.fullsize') : null;
          const r = i.getBoundingClientRect();
          return { src: i.getAttribute('src'), shown: i.currentSrc.split('/').slice(-1)[0], inPicture: i.parentElement.tagName === 'PICTURE', folded: det.reverse().join(' > ') || '(open text)',
                   natural: i.naturalWidth + 'x' + i.naturalHeight, drawn: Math.round(r.width * 10) / 10 + 'x' + Math.round(r.height * 10) / 10, link: a ? a.getAttribute('href') : null, linkText: a ? a.textContent : null };
        }));
        const fonts = await page.evaluate(() => { const p = document.querySelector('p'); const c = document.querySelector('figcaption'); return { body: getComputedStyle(p).fontSize, caption: c ? getComputedStyle(c).fontSize : null, scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth }; });
        out.push({ page: name, width: w, dpr, fonts, rows });
        if (w === 390 || w === 1000) {
          const n = await page.$$eval('picture', a => a.length);
          for (let k = 0; k < n; k++) {
            const fig = await page.evaluateHandle(k => document.querySelectorAll('picture')[k].closest('figure'), k);
            await fig.asElement().screenshot({ path: `${HERE}/shots/${name}-fig${k + 1}-${w}-dpr${dpr}.png` });
            if (w === 390 && dpr === 1) {
              const im = await page.evaluateHandle(k => document.querySelectorAll('picture img')[k], k);
              await im.asElement().screenshot({ path: `${HERE}/shots/${name}-img${k + 1}-390.png` });
            }
          }
        }
        await ctx.close();
      }
    }
    // a whole-screen view at 390 by 844 of each picture as a visitor meets it (folds as the page opens), and whether it is in the open text
    for (const [name, file] of Object.entries(PAGES)) {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
      await ctx.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
      const page = await ctx.newPage(); await page.goto('file://' + file); await page.waitForTimeout(300);
      const n = await page.$$eval('picture', a => a.length);
      for (let k = 0; k < n; k++) {
        const vis = await page.evaluate(k => { const p = document.querySelectorAll('picture')[k]; let e = p; let hidden = false; while (e) { if (e.tagName === 'DETAILS' && !e.open) hidden = true; e = e.parentElement; } p.scrollIntoView({ block: 'start' }); window.scrollBy(0, -20); return !hidden; }, k);
        await page.waitForTimeout(200);
        await page.screenshot({ path: `${HERE}/shots/${name}-screen${k + 1}-390x844.png` });
        out.push({ page: name, picture: k + 1, visibleWithFoldsAsOpened: vis });
      }
      await ctx.close();
    }
  } finally { await browser.close(); }
  fs.writeFileSync(`${HERE}/out/browse.json`, JSON.stringify(out, null, 1));
  for (const o of out) {
    if (!o.rows) { console.log(JSON.stringify(o)); continue; }
    console.log(`\n== ${o.page} at ${o.width} wide, dpr ${o.dpr}; body text ${o.fonts.body}, caption ${o.fonts.caption}; page scroll width ${o.fonts.scrollW} of ${o.fonts.clientW}`);
    for (const r of o.rows) console.log(`  src=${r.src}  SHOWN=${r.shown}  in<picture>=${r.inPicture}  natural=${r.natural} drawn=${r.drawn}  section: ${r.folded}  link=${r.link}`);
  }
})();

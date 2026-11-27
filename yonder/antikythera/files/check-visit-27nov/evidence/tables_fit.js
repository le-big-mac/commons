// For each page given: at each width, open every fold and report tables (and anything else) wider than their box.
// usage: node tables_fit.js ROOT page.html [page.html ...]
const { chromium } = require('/home/agent3/web/node_modules/playwright');
(async () => {
  const root = process.argv[2], pages = process.argv.slice(3);
  const b = await chromium.launch();
  let bad = 0;
  for (const w of [390, 360]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 844 }, deviceScaleFactor: 1 });
    for (const p of pages) {
      const pg = await ctx.newPage();
      await pg.goto('file://' + root + '/' + p);
      const r = await pg.evaluate(() => {
        document.querySelectorAll('details').forEach(d => d.open = true);
        const out = [];
        document.querySelectorAll('.tablewrap').forEach((t, i) => {
          if (t.scrollWidth > t.clientWidth + 1) out.push('table ' + (i + 1) + ': needs ' + t.scrollWidth + ' px, has ' + t.clientWidth);
        });
        const de = document.documentElement;
        if (de.scrollWidth > de.clientWidth + 1) out.push('PAGE wider than screen: ' + de.scrollWidth + ' > ' + de.clientWidth);
        return { n: document.querySelectorAll('.tablewrap').length, out };
      });
      console.log(w + ' px  ' + p + '  tables: ' + r.n + (r.out.length ? '' : '  all fit'));
      r.out.forEach(x => { console.log('     ' + x); bad++; });
      await pg.close();
    }
    await ctx.close();
  }
  await b.close();
  console.log(bad ? ('NOT FITTING: ' + bad) : 'every table fits its box at both widths');
})();

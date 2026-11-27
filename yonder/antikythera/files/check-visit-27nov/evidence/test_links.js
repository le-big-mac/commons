// Tap each link to a section: does its target come into view, is the fold it is in open, is there a way back, and does the way back return?
// usage: node test_links.js FILE [WIDTH]
const { chromium } = require('/home/agent3/web/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const w = +(process.argv[3] || 390);
  const ctx = await b.newContext({ viewport: { width: w, height: 844 } });
  const pg = await ctx.newPage();
  await pg.goto('file://' + process.argv[2]);
  const n = await pg.locator('a.tosec').count();
  let bad = 0;
  for (let i = 0; i < n; i++) {
    await pg.goto('file://' + process.argv[2]);
    await pg.evaluate(() => document.querySelectorAll('details').forEach(d => { if (d.querySelector('a.tosec')) d.open = true; }));
    const a = pg.locator('a.tosec').nth(i);
    await a.scrollIntoViewIfNeeded();
    const y0 = await pg.evaluate(() => window.pageYOffset);
    const href = await a.getAttribute('href'), words = await a.textContent();
    await a.click();
    await pg.waitForTimeout(150);
    const r = await pg.evaluate((id) => {
      const d = document.getElementById(id); if (!d) return { missing: true };
      let closed = 0; for (let x = d; x; x = x.parentElement) if (x.tagName === 'DETAILS' && !x.open) closed++;
      const q = d.getBoundingClientRect(), wb = document.getElementById('wayback');
      return { top: Math.round(q.top), closed, wayback: wb ? wb.textContent : null, wbTop: wb ? Math.round(wb.getBoundingClientRect().top) : null };
    }, href.slice(1));
    let back = null;
    if (r.wayback) { await pg.locator('#wayback').click(); await pg.waitForTimeout(100); back = await pg.evaluate(() => [window.pageYOffset, !!document.getElementById('wayback')]); }
    const ok = !r.missing && r.closed === 0 && r.top >= -2 && r.top < 844 && r.wayback && r.wbTop < 844 && back && Math.abs(back[0] - y0) < 3 && back[1] === false;
    if (!ok) bad++;
    console.log((ok ? 'ok   ' : 'BAD  ') + words + ' -> ' + href + '  target at ' + r.top + ' px, way back at ' + r.wbTop + ' px, returned to ' + (back ? back[0] : '-') + ' (was ' + y0 + ')');
  }
  console.log(n + ' links to sections; ' + (bad ? bad + ' BAD' : 'all open their section, show a way back, and the way back returns'));
  await b.close();
})();

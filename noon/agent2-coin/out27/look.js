// The remade coin page on a phone: any script error, what the first screens look like, and a few figures.   node look.js PAGE OUTDIR
const { chromium } = require('playwright');
(async () => {
  const [page, out] = process.argv.slice(2), b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true }), p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(600);
  const H = await p.evaluate(() => document.documentElement.scrollHeight), W = await p.evaluate(() => document.documentElement.scrollWidth);
  for (let i = 0; i < 6; i++) { await p.evaluate(k => window.scrollTo(0, k * 800), i); await p.waitForTimeout(120); await p.screenshot({ path: out + '/new-' + i + '.png' }); }
  const t = await p.evaluate(() => ({ tiles: [...document.querySelectorAll('.tile')].map(x => x.querySelector('.v').textContent + ' | ' + x.querySelector('.d').textContent), ways: document.getElementById('ways').innerText.replace(/\n+/g, ' / '), sayA: document.getElementById('sayA').textContent, sayB: document.getElementById('sayB').textContent,
    chart: [document.getElementById('chartA').getAttribute('viewBox'), document.getElementById('chartA').getBoundingClientRect().width], wide: [...document.querySelectorAll('*')].filter(e => e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflowX !== 'visible').map(e => e.tagName + '#' + e.id + '.' + e.className) }));
  console.log('errors: ' + (errs.join(' | ') || 'none')); console.log('page ' + W + ' wide, ' + H + ' tall (' + (H / 844).toFixed(1) + ' screens)'); console.log(JSON.stringify(t, null, 1));
  await b.close();
})();

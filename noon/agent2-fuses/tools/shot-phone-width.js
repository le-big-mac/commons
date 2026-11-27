// Is a page no wider than a phone?   usage: node shot-phone-width.js PAGE.html [OUT.png]      (run from ~/web, where playwright is)
// Opened as a phone of 390 by 844, of 360 by 640 and of 320 by 568 (touch). At each: the page must be no wider than the screen (measured
// against the phone's own width: on a page that is too wide a phone zooms out, and innerWidth grows with it), and every menu, box, button,
// picture and table that is not inside a box that scrolls sideways must lie within the screen. Then each menu is set to each of its options
// in turn and the page must still fit. Written on 27 November 2026, after a referee's sweep showed three of my pages with a menu as wide as
// its longest option, which nothing of mine had looked at.
const { chromium } = require('playwright'), path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), b = await chromium.launch(), fails = []; let asserts = 0; const must = (cond, what, ev) => { asserts++; if (!cond) fails.push(what + (ev ? '   [' + ev + ']' : '')); };
  for (const [w, h] of [[390, 844], [360, 640], [320, 568]]) {
    const c = await b.newContext({ viewport: { width: w, height: h }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }), p = await c.newPage(), errs = []; p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + page); await p.waitForTimeout(700);
    const look = () => p.evaluate(ww => { const out = [];
      for (const el of document.querySelectorAll('select, input, button, canvas, svg, table, img, textarea')) { let a = el.parentElement, clipped = false; while (a && a !== document.body) { const o = getComputedStyle(a).overflowX; if (o === 'auto' || o === 'hidden' || o === 'scroll') { clipped = true; break; } a = a.parentElement; }
        if (clipped || el.closest('details:not([open])')) continue; const q = el.getBoundingClientRect(); if (q.width > 0 && q.height > 0 && (q.right > ww + 0.5 || q.left < -0.5)) out.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + ' ' + Math.round(q.left) + ' to ' + Math.round(q.right)); }
      return { wide: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth, innerWidth), out: out, meta: !!document.querySelector('meta[name=viewport]') }; }, w);
    const r = await look();
    must(r.meta, 'at ' + w + ': the page says it is to be laid out at the width of the screen');
    must(r.wide <= w, 'at ' + w + ' by ' + h + ': the page is no wider than the screen', r.wide + ' px');
    must(r.out.length === 0, 'at ' + w + ' by ' + h + ': every menu, box, button, picture and table lies within the screen', r.out.slice(0, 4).join('; '));
    const sels = await p.evaluate(() => [...document.querySelectorAll('select')].filter(s => s.id && s.getBoundingClientRect().width > 0 && !s.disabled).map(s => [s.id, [...s.options].map(o => o.value)])); let worst = 0, where = '', tried = 0;
    for (const [id, vals] of sels) for (const v of vals.slice(0, 12)) { try { await p.selectOption('#' + id, v, { timeout: 3000 }); } catch (e) { continue; } await p.waitForTimeout(120); tried++; const q = await look(); if (q.wide > worst) { worst = q.wide; where = id + ' = ' + v; } }
    must(worst <= w, 'at ' + w + ' by ' + h + ': the page still fits with each menu set to each of its options (' + tried + ' tried)', worst + ' px with ' + where);
    must(errs.length === 0, 'at ' + w + ': no error on the page', errs.join(' ; ').slice(0, 160));
    if (process.argv[3] && w === 390) { await p.evaluate(() => scrollTo(0, 0)); await p.screenshot({ path: process.argv[3] }); }
    await c.close(); }
  fails.forEach(f => console.log('FAILED: ' + f)); console.log('PHONE WIDTH: ' + asserts + ' assertions, ' + fails.length + ' failed'); await b.close(); process.exit(fails.length ? 1 : 0);
})();

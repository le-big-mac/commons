// Can every control of every hand-made page be reached?  For each page, at a phone's size and a desk's: a button, link, input or select
// counts as out of reach if it ends below what the page can scroll to, or begins beyond its right edge.   usage: node reach.js ROOT LIST [w h ...]
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
(async () => {
  const root = path.resolve(process.argv[2]), list = fs.readFileSync(process.argv[3], 'utf8').split('\n').filter(Boolean), sizes = [[390, 844, true], [1000, 800, false]];
  const b = await chromium.launch(); let bad = 0, pages = 0;
  for (const rel of list) { let line = '';
    for (const [w, h, touch] of sizes) {
      const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, hasTouch: touch, isMobile: touch }); const p = await ctx.newPage();
      try { await p.goto('file://' + path.join(root, rel)); await p.waitForTimeout(350);
        const r = await p.evaluate(() => { const de = document.documentElement, canY = getComputedStyle(de).overflowY !== 'hidden' && getComputedStyle(document.body).overflowY !== 'hidden';
          const reachY = canY ? Math.max(de.scrollHeight, document.body.scrollHeight) : innerHeight, out = [];
          document.querySelectorAll('button, input, select, summary, a[href]').forEach(el => { const q = el.getBoundingClientRect(); if (!q.width || !q.height) return; if (getComputedStyle(el).visibility === 'hidden') return;
            const shut = el.closest('details:not([open])'); if (shut && el.tagName !== 'SUMMARY') return;      // inside a note that is folded shut: reached by opening the note
            const top = q.top + scrollY, bottom = q.bottom + scrollY; if (bottom > reachY + 1) out.push((el.textContent || el.value || el.id || el.tagName).trim().slice(0, 24) + ' ends at ' + Math.round(bottom) + ' of ' + Math.round(reachY)); });
          return { out: out, canY: canY, docH: de.scrollHeight, H: innerHeight }; });
        if (r.out.length) line += '  ' + w + 'x' + h + (r.canY ? '' : ' (cannot scroll)') + ': ' + r.out.slice(0, 4).join('; ') + (r.out.length > 4 ? '; and ' + (r.out.length - 4) + ' more' : '');
      } catch (e) { line += '  ' + w + 'x' + h + ': ' + String(e).slice(0, 80); }
      await ctx.close(); }
    pages++; if (line) { bad++; console.log(rel + line); } }
  console.log('REACH: ' + pages + ' pages, ' + bad + ' with a control out of reach'); await b.close(); process.exit(bad ? 1 : 0);
})();

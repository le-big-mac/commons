/* read-page.js: what the built page says at the points the write-up quotes.   cd ~/web && node ~/coin/out27/read-page.js ~/coin/change.html
   Prints one JSON object. Opened as a phone (390 by 844, touch). */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), c = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const p = await c.newPage(); await p.goto('file://' + process.argv[2]); await p.waitForTimeout(600);
  const txt = id => p.evaluate(i => document.getElementById(i).innerText.replace(/\s+/g, ' ').trim(), id);
  const o = {};
  o.lead = await txt('lead'); o.story = await txt('story'); o.addPlain = await txt('addPlain'); o.addBoth = await txt('addBoth');
  o.storyButton = await p.evaluate(() => document.querySelector('#story button').innerText);
  o.tiles = await p.evaluate(() => Array.from(document.querySelectorAll('#fig1 .tile, #fig1 .stat')).map(e => e.innerText.replace(/\s+/g, ' ').trim()));
  await p.tap('#story button'); await p.waitForTimeout(900);
  o.storyAfterSwap = await txt('story'); o.storyButtonAfterSwap = await p.evaluate(() => document.querySelector('#story button').innerText);
  await p.tap('#story button'); await p.waitForTimeout(900);
  o.storyAfterBack = await txt('story');
  await p.selectOption('#preset', '2'); await p.waitForTimeout(900);
  o.storyOtherCoins = await txt('story');
  await p.selectOption('#preset', '0'); await p.waitForTimeout(900);
  await p.tap('#addPlain'); await p.waitForTimeout(1200);
  o.addedSay = await txt('addedSay'); o.addPlainAfter = await txt('addPlain');
  o.labels = [];
  for (let k = 0; k <= 10; k++) { await p.selectOption('#preset', String(k)); await p.waitForTimeout(1500);
    o.labels.push({ preset: k, coins: await p.inputValue('#coins'), upTo: await p.inputValue('#L'), addPlain: await txt('addPlain'), addBoth: await txt('addBoth') }); }
  o.pageSays = await p.evaluate(() => document.body.innerText.replace(/\s+/g, ' '));
  /* three small things the reader met and I left (27 November), as the page now does them */
  o.left = {};
  await p.selectOption('#preset', '0'); await p.waitForTimeout(600); await p.fill('#L', '49'); await p.tap('#apply'); await p.waitForFunction(() => !window.__coin.pending); await p.waitForTimeout(500);
  o.left.menuAfterRangeOnly = await p.evaluate(() => { const s = document.getElementById('preset'); return [s.value, s.options[s.selectedIndex].textContent.trim(), document.getElementById('coins').value, document.getElementById('L').value]; });
  await p.fill('#coins', '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16'); await p.fill('#L', '999'); await p.tap('#apply'); await p.waitForFunction(() => !window.__coin.pending, null, { timeout: 60000 }); await p.waitForTimeout(500);
  await p.fill('#amount', '999'); await p.waitForTimeout(1500);
  o.left.ways999 = await p.evaluate(() => { const w = document.getElementById('way-both'), r = w.getBoundingClientRect(); return { height: Math.round(r.height), screen: window.innerHeight, rows: w.querySelectorAll('.inwords, .row, p').length, says: w.querySelector('p.k').innerText.replace(/\s+/g, ' ').slice(0, 120) }; });
  /* the first screen at two sizes: where each of the three ways of paying 24 cents stands before any scrolling; and the pictures' lettering as shown */
  o.first = {};
  for (const [w, h] of [[390, 844], [360, 640]]) {
    const cx = await b.newContext({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }), q = await cx.newPage(); await q.goto('file://' + process.argv[2]); await q.waitForTimeout(600);
    o.first[w + 'x' + h] = await q.evaluate(() => { const box = id => { const e = document.getElementById(id); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom)]; };
      const letter = id => { const svg = document.getElementById(id), k = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width; return [...new Set([...svg.querySelectorAll('text')].map(t => Math.round(parseFloat(getComputedStyle(t).fontSize) * k * 10) / 10))]; };
      return { scrollY: window.scrollY, screen: window.innerHeight, plain: box('way-plain'), greedy: box('way-greedy'), both: box('way-both'), amount: document.getElementById('amount').value, coins: document.getElementById('coins').value,
        letteringA: letter('chartA'), letteringB: letter('chartB'), widthA: Math.round(document.getElementById('chartA').getBoundingClientRect().width), pageWidth: document.documentElement.scrollWidth }; });
    await cx.close(); }
  console.log(JSON.stringify(o, null, 1)); await b.close();
})();

// A few views one step outside the page test: states of the controls combined, the longest lists, odd words, a narrow window.
// usage: node shot-rhyme-extra.js PAGE.html OUTDIR RCORE.js DATA.json
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])]; const R = require(path.resolve(process.argv[4])), D = JSON.parse(fs.readFileSync(path.resolve(process.argv[5]), 'utf8')), X = R.index(D);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1400 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(600); let bad = 0; const text = sel => p.evaluate(sel => document.querySelector(sel).textContent, sel), count = sel => p.evaluate(sel => document.querySelectorAll(sel).length, sel);
  const say = (what, ok, extra) => { if (!ok) bad++; console.log((ok ? 'ok    ' : 'NOT   ') + what + (extra ? ': ' + extra : '')); };
  // a. every poet chosen in turn with every measure: the line names the poet and the dot chosen is the poet's
  { let good = 0, n = 0; for (let i = 0; i < 32; i += 1) { await p.selectOption('#poetSel', String(i)); for (const key of ['M', 'M_B', 'M_A', 'M_Along']) { await p.selectOption('#measure', key); n++; const s = await text('#say1'), r = await p.evaluate(i => +document.querySelector('#s1 circle.dot[data-i="' + i + '"]').getAttribute('r'), i); if (s.includes(D.poets[i].name) && s.includes(R.pct(D.poets[i].M) + '%') && r === 7) good++; } }
    say('a. 32 poets by 4 measures: the poet chosen is named, with the share, and drawn larger', good === n, good + ' of ' + n); await p.selectOption('#measure', 'M'); }
  // b. every poet with every family: the list holds the poet's failing rhymes; the longest list shown to its end
  { let good = 0; for (let i = 0; i < 32; i++) { await p.evaluate(i => window.RhymePage.choose(-1, i), i); const st = await p.evaluate(() => window.RhymePage.state()); if (st.listed === R.failsOf(D, X, -1, i).length && (await text('#say2')).includes(D.poets[i].name)) good++; }
    say('b. every family, each poet in turn: the list is as long as the poet\'s failing rhymes', good === 32, good + ' of 32');
    const big = D.poets.map((q, i) => [R.failsOf(D, X, -1, i).length, i]).sort((a, b) => b[0] - a[0])[0]; await p.evaluate(i => window.RhymePage.choose(-1, i), big[1]); const t0 = Date.now(); let clicks = 0; while (!(await p.evaluate(() => document.querySelector('#more2').hidden)) && clicks < 60) { await p.click('#more2'); clicks++; }
    const items = await count('#list2 li'); say('b. the longest list (' + D.poets[big[1]].name + ', every family) shown to its end', items === big[0], items + ' of ' + big[0] + ' couplets after ' + clicks + ' presses, ' + (Date.now() - t0) + ' ms'); }
  // c. the word with the most partners, and the commonest words
  { const most = D.words.map((w, i) => [(X.byWord[i] || []).length, w]).sort((a, b) => b[0] - a[0]).slice(0, 5); for (const [n, w] of most) { const t0 = Date.now(); await p.evaluate(w => window.RhymePage.look(w), w); const chips = await count('#chips button'), more = await p.evaluate(() => { const li = document.querySelector('#chips li:last-child'); return li ? li.textContent : ''; });
      say('c. "' + w + '", ' + n + ' partners', chips === Math.min(150, n) && (n <= 150 || more.includes('and ' + (n - 150) + ' more')), chips + ' shown, "' + more.slice(0, 22) + '", ' + (Date.now() - t0) + ' ms'); } }
  // d. odd things typed
  for (const [w, want] of [["O'er", 'oer'], ['o’er', 'oer'], ['LOVE!', 'love'], ['  sea  ', 'sea'], ['constructor', null], ['toString', null], ['__proto__', null], ['123', ''], ['x'.repeat(5000), null], ['<img src=x onerror=alert(1)>', null]]) { await p.fill('#word', w); await p.click('#look'); await p.waitForTimeout(40); const s = await text('#say3');
    const ok = want === '' ? s.includes('Type a word') : want === null ? s.includes('does not end a rhyming line') : s.startsWith(want + ' is in '); say('d. typed ' + JSON.stringify(w.slice(0, 30)), ok && (await count('#fig3 img')) === 0, s.slice(0, 70)); }
  // e. a narrow window: nothing wider than the window, no error
  { await p.setViewportSize({ width: 400, height: 900 }); await p.waitForTimeout(200); const w = await p.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]); say('e. in a window 400 wide the page is no wider than the window', w[0] <= w[1] + 1, w.join(' / ')); await p.screenshot({ path: path.join(out, 'narrow.png') }); await p.setViewportSize({ width: 1100, height: 1400 }); }
  // f. every cell of the second figure by the two lists: the count listed is the cell's
  { let good = 0, n = 0; for (let f = 0; f < D.families.length; f++) { await p.selectOption('#famSel', String(f)); for (let i = 0; i < 32; i += 3) { await p.selectOption('#poetSel2', String(i)); n++; const st = await p.evaluate(() => window.RhymePage.state()); if (st.listed === D.families[f].byPoet[i] && (await count('#list2 li')) === Math.min(40, st.listed)) good++; } }
    say('f. the two lists of the second figure, every family with every third poet', good === n, good + ' of ' + n); }
  console.log('errors on the page: ' + (errs.length ? errs.slice(0, 3).join(' ; ') : 'none')); console.log(`EXTRA VIEWS: ${bad} not as they should be, ${errs.length} errors`); await b.close();
})();

// node pagetest.js [PAGE] : braille.html opened in a headless browser, and what it shows set beside page-expect.json
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const here = __dirname; const file = path.resolve(process.argv[2] || path.join(here, 'braille.html')); const E = JSON.parse(fs.readFileSync(path.join(here, 'page-expect.json'), 'utf8'));
  let bad = 0, n = 0; const must = (ok, what) => { n++; if (!ok) { bad++; console.log('FAILED: ' + what); } };
  const pct = (x, d) => (100 * x).toFixed(d === undefined ? 1 : d) + '%';
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + file);
  // the sentences
  const labels = await p.$$eval('#which button', bs => bs.map(x => x.textContent));
  must(JSON.stringify(labels) === JSON.stringify(E.passages.map(x => x.label)), 'a button for each sentence: ' + labels.join(' '));
  for (let i = 0; i < E.passages.length; i++) {
    await p.click(`#which button:nth-child(${i + 1})`); const want = E.passages[i];
    const got = await p.$$eval('#passage .w', ws => ws.map(w => [w.querySelector('.p').textContent, w.querySelector('.b').textContent]));
    must(JSON.stringify(got.map(g => g[0])) === JSON.stringify(want.words), `${want.label}: the print words are the sentence's, in order`);
    must(JSON.stringify(got.map(g => g[1])) === JSON.stringify(want.braille), `${want.label}: under each word the translator's own cells for it`);
    const said = await p.textContent('#pcount'); const m = said.match(/^(\d+) cells written letter for letter; (\d+) with the signs; (\d+) saved, which is ([\d.]+)%\.$/);
    must(m && Number(m[1]) === want.U && Number(m[2]) === want.C && Number(m[3]) === want.U - want.C && m[4] === (100 * (1 - want.C / want.U)).toFixed(1), `${want.label}: the count says ${want.U}, ${want.C}, ${want.U - want.C}: "${said}"`);
    const marked = await p.$$eval('#passage .p mark', ms => ms.map(x => x.textContent)); const cellsSaved = await p.$$eval('#passage .w', ws => ws.reduce((a, w) => a + w.querySelector('.p').textContent.length - w.querySelector('.b').textContent.length, 0));
    must(marked.length > 3 && marked.every(t => /^[A-Za-z]{2,}$/.test(t)), `${want.label}: the marked stretches are runs of two or more letters: ${marked.length}`);
    must(await p.$eval(`#which button:nth-child(${i + 1})`, x => x.getAttribute('aria-pressed')) === 'true' && (await p.$$eval('#which button[aria-pressed="true"]', x => x.length)) === 1, `${want.label}: its button, and only its button, is marked pressed`);
  }
  const under = () => p.$eval('#passage .p mark', m => getComputedStyle(m).borderBottomWidth);
  const before = await under(); await p.click('#marks'); const after = await under(); await p.click('#marks'); const again = await under();
  must(before !== '0px' && after === '0px' && again === before, `the marking can be put off and on: ${before}, ${after}, ${again}`);
  // the books
  const dots = await p.$$eval('#chart .dot', ds => ds.map(d => ({ label: d.getAttribute('aria-label'), cx: Number(d.getAttribute('cx')), cy: Number(d.getAttribute('cy')) })));
  const novels = E.books.filter(x => x.era !== 0);
  must(dots.length === 18 && novels.every(bk => dots.some(d => d.label === `${bk.title}, ${bk.year}: ${pct(bk.s, 2)}`)), 'eighteen dots, each named with its book, year and share to two places');
  const byLabel = Object.fromEntries(dots.map(d => [d.label.split(',')[0], d])); let order = true;
  for (const a of novels) for (const c of novels) { const da = byLabel[a.title], dc = byLabel[c.title]; if (a.s > c.s + 1e-9 && !(da.cy < dc.cy)) order = false; if (a.year > c.year && !(da.cx > dc.cx)) order = false; }
  must(order, 'a higher share is a higher dot, and a later year is further right, for every pair of books');
  must(dots.every(d => d.cx > 50 && d.cx < 750 && d.cy > 15 && d.cy < 365), 'every dot is inside the frame of the picture');
  const means = await p.$$eval('#chart text.mean', ts => ts.map(t => [t.getAttribute('data-era'), t.textContent]));
  must(means.length === 3 && means.every(([e, t]) => t === 'mean ' + pct(E.mean[e])), 'the three means are the means of the books: ' + means.map(m => m[1]).join(', '));
  const kjv = E.books.find(x => x.era === 0); must((await p.textContent('#kjvlabel')) === 'the King James Bible of 1611: ' + pct(kjv.s), 'the Bible\'s line says its share');
  const meanY = await p.$$eval('#chart .meanline', ls => ls.map(l => Number(l.getAttribute('y1')))); must(meanY[0] < meanY[1] && meanY[1] < meanY[2], 'the three mean bars step down');
  await p.hover('#chart .dot >> nth=0'); const tip = await p.$eval('#tip', t => [t.hidden, t.textContent]); must(!tip[0] && dots.some(d => d.label === tip[1]), 'pointing at a dot shows its book: ' + tip[1]);
  const tb = await p.$eval('#tip', t => t.getBoundingClientRect().toJSON()); const fb = await p.$eval('#chart', t => t.getBoundingClientRect().toJSON()); must(tb.left >= fb.left - 2 && tb.right <= fb.right + 2 && tb.bottom <= fb.bottom, 'the label that appears stays within the picture');
  await p.mouse.move(5, 5); must(await p.$eval('#tip', t => t.hidden), 'moving the pointer away takes the label off');
  await p.focus('#chart .dot >> nth=5'); const t2 = await p.$eval('#tip', t => [t.hidden, t.textContent]); must(!t2[0] && t2[1] === dots[5].label, 'a dot reached by the keyboard shows its own book: ' + t2[1]);
  await p.evaluate(() => document.activeElement.blur()); must(await p.$eval('#tip', t => t.hidden), 'and leaving it takes the label off');
  const rows = await p.$$eval('#booktable tbody tr', rs => rs.map(r => [...r.children].map(c => c.textContent)));
  must(rows.length === 19 && E.books.every(bk => rows.some(r => r[0] === String(bk.year) && r[1] === bk.title && r[2] === pct(bk.s, 2))), 'the table has all nineteen texts with the same figures');
  // the signs
  const bars = await p.$$eval('.row', rs => rs.map(r => ({ sign: r.getAttribute('data-sign'), then: r.querySelector('.thenv').textContent, now: r.querySelector('.nowv').textContent, wt: r.querySelector('.bar.then').getBoundingClientRect().width, wn: r.querySelector('.bar.now').getBoundingClientRect().width, side: r.parentNode.id })));
  const fmt = v => Math.round(v).toLocaleString('en-GB');
  must(bars.length === Object.keys(E.signs).length - 3 && bars.every(r => E.signs[r.sign] && r.then === fmt(E.signs[r.sign][0]) && r.now === fmt(E.signs[r.sign][1])), 'each sign\'s two figures are those counted straight from the books\' records');
  must(bars.every(r => (r.side === 'losers') === (E.signs[r.sign][1] < E.signs[r.sign][0])), 'every sign under "Lost" fell and every sign under "Gained" rose');
  const kmax = Math.max(...bars.map(r => Math.max(r.wt, r.wn))); const vmax = Math.max(...bars.map(r => Math.max(...E.signs[r.sign])));
  const big = await p.textContent('#big'); must(['the', 'ing', 'ed'].every(s => big.includes(`${s} (${fmt(E.signs[s][0])} to ${fmt(E.signs[s][1])})`) && E.signs[s][1] > E.signs[s][0]), 'the three largest signs are given in a sentence with their figures, and each did gain: ' + big);
  must(bars.every(r => Math.abs(r.wt / kmax - E.signs[r.sign][0] / vmax) < 0.02 && Math.abs(r.wn / kmax - E.signs[r.sign][1] / vmax) < 0.02), 'the bars are as long as their figures, on one scale');
  const never = await p.textContent('#never'); must(E.never['3'].every(w => never.includes(w)) && never.includes(E.never['1'].join(', ')), 'the signs that never occur are named');
  // the four added texts
  const add = await p.$$eval('#added tbody tr', rs => rs.map(r => [...r.children].map(c => c.textContent)));
  must(add.length === 6 && E.added.every(a => add.some(r => r[0] === `${a.title}, ${a.year}` && r[1] === a.rate.toFixed(1) && r[2] === pct(a.L, 2))), 'the four added texts are in the table with their own figures, counted straight from their records');
  must(add[0][2] === pct(E.sixL[0], 2) && add[5][2] === pct(E.sixL[1], 2) && add[0][1] === '' , 'with the means of the first six and the last six novels above and below them: ' + add[0][2] + ', ' + add[5][2]);
  const yrs = add.slice(1, 5).map(r => Number(r[0].slice(-4))); must(yrs.every((y, i) => i === 0 || y >= yrs[i - 1]), 'the four are in order of year: ' + yrs.join(' '));
  must((await p.textContent('#held3')) === (E.held3 === 1 ? 'One of six held.' : null), 'the page says how many of the six predictions held: ' + await p.textContent('#held3'));
  // speech
  const sp = await p.$$eval('#speech tbody tr', rs => rs.map(r => [...r.querySelectorAll('td')].map(c => c.textContent)));
  must(sp.length === 3 && ['out', 'ins', 'share'].every((k, i) => ['1', '2', '3'].every((e, j) => sp[i][j] === pct(E.speech[k][e]))), 'the table of speech and narration has the nine figures of the second sheet');
  must(errs.length === 0, 'no script error: ' + errs.slice(0, 2));
  for (const w of [1000, 600, 390, 320]) { await p.setViewportSize({ width: w, height: 800 }); must(await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth) <= 0, `at ${w} wide nothing runs off the side`); }
  console.log(`${n - bad} of ${n} checks passed`); await b.close(); process.exit(bad ? 1 : 0);
})();

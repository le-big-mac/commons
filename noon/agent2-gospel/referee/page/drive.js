// The referee's own turtles on the page.  usage: node drive.js PAGE.html TRUTH.json OUTDIR
// Every sentence the page prints for each turtle is set beside truth.json (made by truth.py from the blind step's programs).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const page = path.resolve(process.argv[2]), truth = JSON.parse(fs.readFileSync(process.argv[3], 'utf8')), out = path.resolve(process.argv[4]);
const faults = []; let checked = 0;
const log = (...a) => console.log(...a);
const commas = n => String(n).replace(/\B(?=(\d{3})+$)/g, ',');
const num = s => parseInt(String(s).replace(/,/g, ''), 10);
const ord2 = m => { if (m === 1) return 1; let n = 1, x = 2 % m; while (x !== 1) { x = x * 2 % m; n++; } return n; };
const pw = s => { let m = /^(\d+)(²|³|\^(\d+))?$/.exec(s.replace(/,/g, '')); if (!m) return null; const e = !m[2] ? 1 : m[2] === '²' ? 2 : m[2] === '³' ? 3 : +m[3]; return Math.pow(+m[1], e); };
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(400);
  const state = (pg) => (pg || p).evaluate(() => window.GOSPELSTATE());
  const typed = async (a, i) => { await p.fill('#num', a); await p.fill('#den', i); };
  const finish = async () => { for (let k = 0; k < 60; k++) { const s = await state(); if (s.done || !s.valid) return s; await p.waitForTimeout(50); } return state(); };
  const fault = (who, what) => { faults.push(who + ': ' + what); log('FAULT ' + who + ': ' + what); };

  // ---- A. values
  await p.selectOption('#pace', 'once');
  for (const t of truth.cases) {
    const who = t.P + '/' + t.Q; await typed(String(t.P), String(t.Q)); const before = await state(); await p.click('#go'); const s = await finish(); checked++;
    log('--- ' + who + '\n  deg:    ' + s.deg + '\n  say:    ' + s.say + '\n  report: ' + s.report + '\n  total ' + s.total + ', rounds ' + s.rounds + ', dots ' + s.dots + ', home ' + s.home + ', gain ' + s.gain);
    if (!s.valid) { fault(who, 'not taken as valid'); continue; }
    const f = s.forecast, n = t.round, T = t.tail, m = t.m;
    if (f.p !== t.p || f.q !== t.q || f.tail !== T || f.round !== n || f.bounded !== t.bounded) fault(who, 'forecast p,q,tail,round,bounded ' + [f.p, f.q, f.tail, f.round, f.bounded] + ' against ' + [t.p, t.q, T, n, t.bounded]);
    if (before.say !== s.say) fault(who, 'the forecast changed when Go was pressed');
    const wantDeg = '= ' + (Math.round(360 * t.p / t.q * 10000) / 10000) + '° (' + commas(t.p) + '/' + commas(t.q) + ' in lowest terms)'; if (s.deg !== wantDeg) fault(who, 'deg "' + s.deg + '" against "' + wantDeg + '"');
    // what should be drawn
    let total, rounds, cut = false;
    if (m === 1) { total = T + 30; rounds = 30; } else if (t.bounded) { total = T + n; rounds = 1; if (total > 20000) { total = 20000; cut = true; } }
    else { rounds = Math.max(4, Math.min(40, Math.round(240 / n))); total = T + n * rounds; if (total > 20000) { rounds = Math.floor((20000 - T) / n); if (rounds >= 1) total = T + n * rounds; else { total = 20000; cut = true; } } }
    if (s.total !== total) fault(who, 'draws ' + s.total + ' steps, I expected ' + total);
    const saysCut = s.say.includes('That is more than this page draws');
    if (saysCut !== cut) fault(who, (saysCut ? 'says "That is more than this page draws: it will stop at step ' + commas(s.total) + '" though it draws ' + (t.bounded ? 'the whole round' : rounds + ' whole rounds') : 'does not say it stops short') + ' (tail ' + T + ', round ' + n + ', total ' + s.total + ')');
    // the forecast's sentence
    if (m === 1) { if (!s.say.includes('walks straight on for ever') || (T > 0 && !s.say.includes('After ' + commas(T) + (T === 1 ? ' step ' : ' steps ')))) fault(who, 'straight-on sentence: ' + s.say); }
    else if (t.bounded && T === 0) { if (!s.say.includes('it comes home after ' + commas(n) + ' steps.') || !s.say.includes('come round again every ' + commas(n) + ' steps, and that round closes')) fault(who, 'home sentence: ' + s.say.slice(0, 120)); }
    else if (t.bounded) { if (!s.say.includes('it never comes home, and never gets away.') || !s.say.includes('After a tail of ' + commas(T) + (T === 1 ? ' step ' : ' steps ')) || !s.say.includes('one loop of ' + commas(n) + ' steps for ever')) fault(who, 'loop sentence: ' + s.say.slice(0, 160)); }
    else { if (!s.say.includes('it never comes home.') || !s.say.includes('come round again every ' + commas(n) + ' steps, and a round does not close') || (T > 0 && !s.say.includes('After a tail of ' + commas(T) + (T === 1 ? ' step ' : ' steps ')))) fault(who, 'marching sentence: ' + s.say.slice(0, 160)); }
    // the reason: every arithmetical clause
    if (m > 1) {
      const primes = t.factors.map(x => x[0]), others = (l) => primes.filter(r => r !== l);
      const prod = /([\d,]+) = ([\d²³^ ×,]+?),? holds/.exec(s.say); if (prod) { const v = prod[2].split(' × ').map(pw).reduce((a, c) => a * c, 1); if (v !== m || num(prod[1]) !== m) fault(who, 'factorisation "' + prod[0] + '" is not of ' + m); }
      else if (t.factors.length > 1 || t.factors[0][1] > 1) fault(who, 'no factorisation printed');
      if (!s.say.includes(commas(m))) fault(who, 'the odd part ' + m + ' is not named');
      if (T > 0 && !s.say.includes('The odd part of the denominator, ')) fault(who, 'even denominator, but the reason does not say "odd part"');
      const sq = /holds the square of (\d+)/.exec(s.say); if (sq) { const l = +sq[1]; if (m % (l * l) !== 0) fault(who, 'says it holds the square of ' + l); if (!t.bounded) fault(who, '"holds the square of" on an unbounded turtle'); }
      if (s.say.includes('holds no square of a prime') && t.factors.some(x => x[1] >= 2)) fault(who, 'says no square, but there is one');
      let nNot = 0;
      const re1 = /(?:^|[ :])([\d,]+(?:²|³|\^\d+)?) does not divide the order of 2 modulo ([^.]*)\./.exec(s.say);
      if (re1) { const X = pw(re1[1]); for (const part of re1[2].split(', or modulo ')) { const mm = /^(\d+) \(which is ([\d,]+)\)$/.exec(part); if (!mm) { fault(who, 'cannot read "' + part + '"'); continue; } nNot++;
          const r = +mm[1], o = num(mm[2]); if (o !== ord2(r)) fault(who, 'order of 2 modulo ' + r + ' printed as ' + o + ', is ' + ord2(r)); if (o % X === 0) fault(who, 'FALSE REASON: "' + re1[1] + ' does not divide the order of 2 modulo ' + r + ' (which is ' + o + ')"'); }
        if (sq && nNot !== others(+sq[1]).length) fault(who, 'reason names ' + nNot + ' other primes, there are ' + others(+sq[1]).length); }
      else if (t.bounded && t.factors.length > 1) fault(who, 'bounded with other primes, but no "does not divide" clause');
      const re2 = /([\d,]+(?:²|³|\^\d+)?) divides the order of 2 modulo (\d+) \(which is ([\d,]+)\)/g; let mm;
      while ((mm = re2.exec(s.say))) { const X = pw(mm[1]), r = +mm[2], o = num(mm[3]); if (o !== ord2(r)) fault(who, 'order of 2 modulo ' + r + ' printed as ' + o); if (o % X !== 0) fault(who, 'FALSE REASON: "' + mm[0] + '"'); if (m % r !== 0) fault(who, r + ' is not a prime of the odd part'); }
      const re3 = /2 has the same order modulo ([\d²³^]+) as modulo ([\d²³^]+)/g;
      while ((mm = re3.exec(s.say))) { if (ord2(pw(mm[1])) !== ord2(pw(mm[2]))) fault(who, 'FALSE REASON: "' + mm[0] + '"'); }
      if (!t.bounded && t.factors.some(x => x[1] >= 2) && !s.say.includes('spoilt')) fault(who, 'unbounded with a square, but no "spoilt"');
    }
    // the report
    if (s.fails.length) fault(who, 'the page\'s own must() failed: ' + s.fails.join('; '));
    if (s.report.includes('disagree')) fault(who, 'report: ' + s.report);
    if (cut) { if (!s.report.startsWith('Stopped at step 20,000, before the end of')) fault(who, 'report when cut: ' + s.report); }
    else if (m === 1) { if (s.report !== 'Step ' + commas(total) + ': not home, and it will not be. It is walking straight on.') fault(who, 'report: ' + s.report); }
    else if (t.bounded && T === 0) { if (s.home !== n || s.report !== 'Step ' + commas(n) + ': home. It is where it began, facing as it began, and its next turn would be ' + commas(t.p) + '/' + commas(t.q) + ' of a turn again.') fault(who, 'report: ' + s.report); }
    else if (t.bounded) { if (s.home !== 0 || !s.report.startsWith('Step ' + commas(total) + ': back where it stood at step ' + commas(T) + ', at the end of its tail. From here it goes round the same loop of ' + commas(n) + ' steps for ever.')) fault(who, 'report: ' + s.report); }
    else { const g = /has carried it ([\d.]+) steps further/.exec(s.report); if (s.home !== 0 || !g || Math.abs(+g[1] - t.sum) > 0.00051 || !s.report.startsWith('Step ' + commas(total) + ': not home, and it will not be. Each round of ' + commas(n) + ' steps has carried it')) fault(who, 'report: ' + s.report + '  [my round sum ' + t.sum + ']');
      if (rounds >= 2 && !s.report.includes('each of the ' + commas(rounds) + ' rounds drawn')) fault(who, 'rounds drawn: ' + s.report); if (s.dots !== rounds + (T > 0 ? 1 : 0)) fault(who, 'dots ' + s.dots + ' for ' + rounds + ' rounds, tail ' + T); }
  }
  // the two that come to exactly 20,000 steps without being cut
  for (const [a, m, n, kind] of truth.exact20000.slice(0, 1).concat(truth.exact20000.filter(x => x[3] === 'bounded').slice(0, 1))) {
    const q = m * Math.pow(2, a); await typed('1', String(q)); await p.click('#go'); const s = await finish(); checked++;
    log('--- exactly 20,000: 1/' + q + ' (' + kind + ', tail ' + a + ', round ' + n + ')\n  say:    ' + s.say + '\n  report: ' + s.report + '\n  total ' + s.total + ', rounds ' + s.rounds);
    if (s.say.includes('That is more than this page draws')) fault('1/' + q, 'says "That is more than this page draws: it will stop at step 20,000" though the ' + (kind === 'bounded' ? 'whole loop (tail ' + a + ' + round ' + n + ')' : s.rounds + ' whole rounds of ' + n) + ' are drawn and the report is: ' + s.report.slice(0, 90));
  }
  // the grid's sentence
  { const s = await state(), g = truth.grid; const want = 'Of these 1,000, ' + g.closes + ' come home; ' + g.spoilt + ' hold the square of a prime and march away all the same; ' + g.plain + ' hold no square, and march away.';
    log('--- grid: ' + s.mapcount + ' | note: ' + s.spoiltcount); if (s.mapcount !== want) fault('grid', '"' + s.mapcount + '" against my "' + want + '"'); }

  // ---- B. what is typed
  for (const [a, i] of [['', '9'], ['1', ''], ['abc', '9'], ['1.5', '9'], ['1e3', '9'], ['0x10', '9'], [' 7 ', ' 45 '], ['+7', '45'], ['−1', '9'], ['12345678', '9'], ['1234567', '9'], ['00009', '00045'], ['-0', '9'], ['1', '-9'], ['1', '0'], ['1', '2000000'], ['1', '2000001'], ['1/3', '9'], ['１', '９']]) {
    await typed(a, i); const s = await state(); log('--- typed [' + a + '] / [' + i + ']: valid ' + s.valid + ' | deg ' + s.deg + ' | say ' + s.say.slice(0, 140) + ' | go disabled ' + await p.isDisabled('#go')); checked++; }

  // ---- C. states
  const inkOf = (pg) => (pg || p).evaluate(() => { const c = document.getElementById('field'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data, t = document.getElementById('turtle'), e = t.getContext('2d').getImageData(0, 0, t.width, t.height).data; let dark = 0, rust = 0, blue = 0;
    for (let i = 0; i < d.length; i += 4) { if (d[i + 3] > 90 && d[i] < 100 && d[i + 1] < 90 && d[i + 2] < 90) dark++; if (d[i + 3] > 40 && d[i] > 130 && d[i + 1] < 110 && d[i + 2] < 85) rust++; }
    for (let i = 0; i < e.length; i += 4) if (e[i + 3] > 120 && e[i + 2] > 110 && e[i] < 90) blue++; return { dark, rust, blue, w: c.width, h: c.height }; });
  // C1 a number changed while it walks
  await typed('1', '63'); await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(1500); let a = await state(); await p.fill('#num', '2'); let c = await state(), ik = await inkOf(); await p.waitForTimeout(500); let d = await state();
  log('--- C1 number changed mid-walk: before drawn ' + a.drawn + ' running ' + a.running + '; after: running ' + c.running + ' drawn ' + c.drawn + ' report "' + c.report + '" deg ' + c.deg + ' dark pixels ' + ik.dark + '; later drawn ' + d.drawn);
  if (c.running || c.drawn !== 0 || ik.dark !== 0 || d.drawn !== 0 || !c.deg.includes('2/63')) fault('C1', 'number changed mid-walk: ' + JSON.stringify([c.running, c.drawn, ik.dark, d.drawn, c.deg]));
  // C2 Go pressed twice
  await typed('1', '63'); await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(1500); a = await state(); await p.click('#go'); await p.waitForTimeout(300); c = await state(); await p.waitForTimeout(6600); d = await state(); ik = await inkOf();
  log('--- C2 Go twice: first ' + a.drawn + ' drawn; just after second Go ' + c.drawn + ' (goes ' + c.goes + '); at the end done ' + d.done + ' drawn ' + d.drawn + ' dots ' + d.dots + ' report "' + d.report + '"');
  if (!(c.drawn < a.drawn && c.goes === a.goes + 1 && d.done && d.drawn === 240 && d.dots === 40 && d.fails.length === 0)) fault('C2', 'Go twice: ' + JSON.stringify([a.drawn, c.drawn, c.goes, d.done, d.drawn, d.dots]));
  const onceInk = ik; await p.selectOption('#pace', 'once'); await p.click('#go'); await p.waitForTimeout(200); const ik2 = await inkOf(); if (Math.abs(ik2.dark - onceInk.dark) > 0.02 * ik2.dark || Math.abs(ik2.rust - onceInk.rust) > 0.05 * ik2.rust) fault('C2', 'picture after Go twice differs from a clean walk: ' + JSON.stringify([onceInk, ik2]));
  // C3 the grid clicked while it walks
  await typed('1', '63'); await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(1200);
  { const bx = await p.locator('#map').boundingBox(), cl = await p.evaluate((m) => window.GOSPELCELL(m), 189); await p.locator('#map').scrollIntoViewIfNeeded(); const bx2 = await p.locator('#map').boundingBox(); await p.mouse.click(bx2.x + cl[0] / cl[2] * bx2.width, bx2.y + cl[1] / cl[3] * bx2.height); await p.waitForTimeout(1000); c = await state();
    log('--- C3 grid clicked mid-walk (189): Q ' + c.Q + ' running ' + c.running + ' drawn ' + c.drawn + ' of ' + c.total + ' report "' + c.report + '" boxes ' + await p.inputValue('#num') + '/' + await p.inputValue('#den') + ' pick ' + c.pick + '\n  mapsay: ' + c.mapsay + '\n  say: ' + c.say);
    if (c.Q !== 189 || !c.running || c.pick !== 189 || c.drawn < 3 || c.drawn > 7 || await p.inputValue('#den') !== '189') fault('C3', 'grid clicked mid-walk: ' + JSON.stringify([c.Q, c.running, c.pick, c.drawn])); }
  // C4 invalid, then the window resized: is the picture still clear?
  await typed('abc', '9'); const k0 = await inkOf(); await p.setViewportSize({ width: 700, height: 900 }); await p.waitForTimeout(300); const k1 = await inkOf(), s4 = await state();
  log('--- C4 junk typed, then window resized: before ' + JSON.stringify(k0) + ' after ' + JSON.stringify(k1) + ' say "' + s4.say.slice(0, 60) + '" report "' + s4.report + '"');
  if (k1.blue > 0 || k1.rust > 0 || k1.dark > 0) fault('C4', 'after junk is typed the picture is cleared, but resizing the window draws the ring and the turtle again (' + k1.rust + ' rust, ' + k1.blue + ' blue pixels) while the page asks for two whole numbers and Go is disabled');
  // C5 resized mid-walk, and after: the dashed line
  await typed('1', '37'); await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(1200); a = await state(); await p.setViewportSize({ width: 520, height: 900 }); await p.waitForTimeout(400); c = await state();
  const fr = await p.evaluate(() => { const e = window.GOSPELPIXELS(); return e; }); await p.waitForTimeout(6500); d = await state(); const k5 = await inkOf();
  log('--- C5 resized mid-walk (1/37 quick): ' + a.drawn + ' then ' + c.drawn + ' running ' + c.running + '; end done ' + d.done + ' dots ' + d.dots + ' rounds ' + d.rounds + ' W ' + d.W + ' ink ' + JSON.stringify(k5) + ' report "' + d.report + '"');
  if (!(c.running && c.drawn > a.drawn && d.done && d.dots === d.rounds && fr.x0 >= 0 && fr.x1 <= fr.W && fr.y0 >= 0 && fr.y1 <= fr.H)) fault('C5', 'resize mid-walk: ' + JSON.stringify([a.drawn, c.drawn, c.running, d.done, d.dots, d.rounds, fr]));
  const dashNow = async () => p.evaluate(() => { const st = window.GOSPELSTATE(), P = window.GOSPELPATH(1), n = st.forecast.round, A = P[n], C = P[2 * n], mid = window.GOSPELPX((A[0] + C[0]) / 2, (A[1] + C[1]) / 2), c = document.getElementById('field'), d = c.getContext('2d').getImageData(Math.round(mid[0]) - 8, Math.round(mid[1]) - 8, 17, 17).data; let k = 0; for (let i = 0; i < d.length; i += 4) if (d[i + 3] > 40 && d[i] > 130 && d[i + 1] < 110 && d[i + 2] < 85) k++; return k; });
  const dash1 = await dashNow(); await p.setViewportSize({ width: 900, height: 900 }); await p.waitForTimeout(400); const dash2 = await dashNow(), s5 = await state();
  log('--- C5b dashed line midway between two dots: ' + dash1 + ' rust pixels after the walk, ' + dash2 + ' after a resize; report "' + s5.report.slice(0, 120) + '"');
  if (dash1 === 0 || dash2 === 0) fault('C5b', 'dashed line missing (' + dash1 + ', ' + dash2 + ') while the report speaks of it');
  // C6 narrow screen, 320 px, a long reason
  const ph = await b.newPage({ viewport: { width: 320, height: 700 }, deviceScaleFactor: 3 }); await ph.goto('file://' + page); await ph.waitForTimeout(300);
  await ph.fill('#num', '1'); await ph.fill('#den', '1576575'); await ph.selectOption('#pace', 'once'); await ph.click('#go'); await ph.waitForTimeout(600);
  const lay = await ph.evaluate(() => { const r = id => document.getElementById(id).getBoundingClientRect(); const all = [...document.querySelectorAll('main *')].map(e => e.getBoundingClientRect().right); return { sw: document.documentElement.scrollWidth, iw: window.innerWidth, maxRight: Math.max(...all), say: r('say').height, num: r('num').width, go: r('go').right }; });
  const s6 = await state(ph); log('--- C6 320 px: ' + JSON.stringify(lay) + '\n  say: ' + s6.say + '\n  report: ' + s6.report);
  if (lay.sw > lay.iw || lay.maxRight > lay.iw + 0.5) fault('C6', 'something runs off a 320 px screen: ' + JSON.stringify(lay));
  await ph.screenshot({ path: path.join(out, 'narrow-320.png'), fullPage: false }); await ph.close();
  await p.screenshot({ path: path.join(out, 'after-states.png'), fullPage: true });
  if (errs.length) fault('script', errs.join(' | ').slice(0, 300));
  log('DRIVE: ' + checked + ' turtles and inputs, ' + faults.length + ' faults'); for (const f of faults) log('  * ' + f);
  await b.close();
})().catch(e => { console.log('DRIVE STOPPED: ' + String(e).slice(0, 400)); process.exit(2); });

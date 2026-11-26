// Headless checks of the doubling turtle's page.   usage: node shot-gospel.js PAGE.html OUTDIR CORE.js TABLE.json GOSPEL.out MORE.out
// TABLE.json is made by table.py in Python, by walking and adding up; GOSPEL.out and MORE.out are the sealed runs' records.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const fails = []; let asserts = 0, browser = null;
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]), T = require(path.resolve(process.argv[4])), table = JSON.parse(fs.readFileSync(path.resolve(process.argv[5]), 'utf8'));
  const sealed = fs.readFileSync(path.resolve(process.argv[6]), 'utf8'), more = fs.readFileSync(path.resolve(process.argv[7]), 'utf8');
  const b = await chromium.launch(); browser = b;
  const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(500);
  const must = (cond, what, detail) => { asserts++; if (!cond) fails.push(what); console.log((cond ? 'ok   ' : 'FAIL ') + what + (detail ? '   [' + detail + ']' : '')); };
  const state = (pg) => (pg || p).evaluate(() => window.GOSPELSTATE());
  const typed = async (a, i) => { await p.fill('#num', a); await p.fill('#den', i); };
  const once = async () => { await p.selectOption('#pace', 'once'); await p.click('#go'); await p.waitForTimeout(120); return state(); };
  const py = (P, Q) => table.fracs.find(r => r.P === P && r.Q === Q);
  const ink = (pg) => (pg || p).evaluate(() => { const c = document.getElementById('field'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let line = 0, x0 = 1e9, x1 = -1, y0 = 1e9, y1 = -1;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x), r = d[i], g = d[i + 1], bl = d[i + 2], a = d[i + 3];
      if (a > 90 && r < 100 && g < 90 && bl < 90) { line++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } }
    return { line, x0, x1, y0, y1, w: c.width, h: c.height }; });
  const rustNear = (x, y, rad, minAlpha) => p.evaluate(([x, y, rad, minAlpha]) => { const c = document.getElementById('field'), X = Math.round(x), Y = Math.round(y), d = c.getContext('2d').getImageData(X - rad, Y - rad, 2 * rad + 1, 2 * rad + 1).data; let n = 0;
    for (let i = 0; i < d.length; i += 4) if (d[i + 3] > minAlpha && d[i] > 130 && d[i + 1] < 110 && d[i + 2] < 85) n++; return n; }, [x, y, rad, minAlpha]);
  // the turtle's blue triangle: where its middle is, where its point is, and the step it has just taken, on the screen
  const pointing = (pg) => (pg || p).evaluate(() => { const c = document.getElementById('turtle'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data, blue = []; let sx = 0, sy = 0;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i + 3] > 120 && d[i + 2] > 110 && d[i] < 90) { blue.push([x, y]); sx += x; sy += y; } }
    const n = blue.length, cx = sx / Math.max(n, 1), cy = sy / Math.max(n, 1); let far = 0, tip = [cx, cy]; for (const [x, y] of blue) { const r = Math.hypot(x - cx, y - cy); if (r > far) { far = r; tip = [x, y]; } }
    const st = window.GOSPELSTATE(), P = window.GOSPELPATH(1), k = st.drawn, at = window.GOSPELPX(P[k][0], P[k][1]); let want = null;
    if (k > 0) { const a = window.GOSPELPX(P[k - 1][0], P[k - 1][1]); want = [at[0] - a[0], at[1] - a[1]]; }
    return { n, x: cx, y: cy, at, tip: [tip[0] - cx, tip[1] - cy], want, drawn: k }; });
  const cosBetween = (u, v) => (u[0] * v[0] + u[1] * v[1]) / (Math.hypot(u[0], u[1]) * Math.hypot(v[0], v[1]) || 1);
  const pathOf = () => p.evaluate(() => window.GOSPELPATH(1));
  const samePath = (pts, w) => { if (pts.length !== w.xs.length) return 9; let worst = 0; for (let k = 0; k < pts.length; k++) worst = Math.max(worst, Math.abs(pts[k][0] - w.xs[k]), Math.abs(pts[k][1] - w.ys[k])); return worst; };
  const pyCorners = (P, Q, pts) => { const c = table.corners.find(c => c.P === P && c.Q === Q); if (!c) return null; let worst = 0, n = 0; for (const [k, x, y] of c.at) if (pts[k]) { worst = Math.max(worst, Math.abs(pts[k][0] - x), Math.abs(pts[k][1] - y)); n++; } return { worst, n }; };
  // the dark line against the page's own corners: a rust dot (3 px by the screen's pixel ratio) may cover the line's very end, so the allowance grows with that ratio
  const frame = async (pg) => { const e = await (pg || p).evaluate(() => window.GOSPELPIXELS()), ik = await ink(pg), dpr = (await state(pg)).DPR, tol = 2 + 3.5 * dpr;
    return { ok: e.x0 >= 4 && e.y0 >= 4 && e.x1 <= e.W - 4 && e.y1 <= e.H - 4 && ik.line > 20 && Math.abs(ik.x0 - e.x0) < tol && Math.abs(ik.x1 - e.x1) < tol && Math.abs(ik.y0 - e.y0) < tol && Math.abs(ik.y1 - e.y1) < tol && ik.x0 >= 2 && ik.y0 >= 2 && ik.x1 <= ik.w - 3 && ik.y1 <= ik.h - 3, e, ik }; };
  const hasSquare = m => T.factor(m).some(f => f[1] >= 2);
  // the reason the page should print for an odd denominator m, worked here from nothing but arithmetic (orders found by doubling)
  const ord = r => { let k = 1, x = 2 % r; while (x !== 1) { x = x * 2 % r; k++; } return k; };
  const vl = (o, l) => { let k = 0; while (o % l === 0) { o /= l; k++; } return k; };
  const fac = m => { const out = []; for (let l = 3; l * l <= m; l += 2) if (m % l === 0) { let e = 0; while (m % l === 0) { m /= l; e++; } out.push([l, e]); } if (m > 1) out.push([m, 1]); return out; };
  const pw = (l, e) => e === 1 ? String(l) : l + (e === 2 ? '²' : e === 3 ? '³' : '^' + e);
  const reason = (m, tail) => { const f = fac(m), name = T.commas(m) + (f.length > 1 || (f.length === 1 && f[0][1] > 1) ? ' = ' + f.map(x => pw(x[0], x[1])).join(' × ') : ''), odd = tail ? 'The odd part of the denominator, ' + name + ',' : name;
    let serves = null; const spoilt = [];
    for (const [l, e] of f) { if (e < 2) continue; const here = vl(ord(l ** e), l); let by = null;
      if (here <= vl(ord(l ** (e - 1)), l)) by = '2 has the same order modulo ' + pw(l, e) + ' as modulo ' + pw(l, e - 1) + ', so ' + pw(l, e) + ' is of no use';
      for (const [r] of f) if (!by && r !== l && vl(ord(r), l) >= here) by = pw(l, here) + ' divides the order of 2 modulo ' + r + ' (which is ' + T.commas(ord(r)) + ')';
      if (by) spoilt.push(by); else if (!serves) serves = [l, e, here]; }
    if (serves) { const others = f.filter(x => x[0] !== serves[0]);
      return { home: true, text: others.length ? odd + ' holds ' + pw(serves[0], serves[1]) + ', and nothing spoils it: ' + pw(serves[0], serves[2]) + ' does not divide the order of 2 modulo ' + others.map(x => x[0] + ' (which is ' + T.commas(ord(x[0])) + ')').join(', or modulo ') + '.'
                                                 : odd + ' holds its prime ' + serves[0] + ' at least squared, and there is no other prime in it to spoil that.' }; }
    if (!spoilt.length) return { home: false, text: odd + ' holds no square of a prime, and without one a round cannot close.' };
    return { home: false, text: odd + ' holds ' + (spoilt.length > 1 ? 'squares, but each is spoilt' : 'a square, but it is spoilt') + ': ' + spoilt.join('; and ') + '.' }; };
  // where the middle of the square for 1/m ought to be on the grid's canvas: forty to a row, read like a page, 25 rows
  const place = (m, w, h) => { const i = (m - 3) / 2; return [((i % 40) + 0.5) * w / 40, (Math.floor(i / 40) + 0.5) * h / 25]; };

  // ---- 1. as it opens
  let s = await state();
  must(errs.length === 0, 'the page opens without a script error', errs.join(' | ').slice(0, 200));
  must(s.valid && s.P === 1 && s.Q === 9 && s.drawn === 0 && !s.running && !s.done && s.goes === 0 && s.report === 'The turtle is waiting at its start.' && await p.inputValue('#num') === '1' && await p.inputValue('#den') === '9', 'it opens on the book\'s turtle (first turn 1/9 of a turn), waiting');
  { const r = py(1, 9);
    must(r.home === 6 && r.bounded && s.say.includes('it comes home after 6 steps') && s.say.includes('come round again every 6 steps, and that round closes') && s.say.includes(reason(9, 0).text) && s.say.includes('9 = 3² holds its prime 3 at least squared, and there is no other prime in it to spoil that.') && s.deg === '= 40° (1/9 in lowest terms)',
      'before it moves the forecast says home after 6 steps and gives the reason, and the first turn is shown as 40 degrees; 6 is the step at which Python\'s walk is home', s.say.slice(0, 110)); }
  { const pt = await pointing(), i0 = await ink(), o = await p.evaluate(() => window.GOSPELPX(0, 0));
    must(pt.n > 40 && Math.hypot(pt.x - o[0], pt.y - o[1]) < 6 && pt.tip[1] < -5 && Math.abs(pt.tip[0]) < 3 && (await rustNear(o[0], o[1], 10, 150)) > 20 && i0.line === 0, 'the turtle is drawn at the start, inside the ring, pointing up the page, and no line is drawn yet');
    const rects = await p.evaluate(() => ['field', 'turtle'].map(id => { const r = document.getElementById(id).getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }));
    must(rects[0].every((v, k) => Math.abs(v - rects[1][k]) < 0.5), 'the sheet the turtle is drawn on lies exactly over the sheet the line is drawn on'); }
  // the grid as it opens
  { let closes = 0, spoilt = 0, plain = 0; for (let m = 3; m <= 2001; m += 2) { if (table.odd[m][0]) closes++; else if (hasSquare(m)) spoilt++; else plain++; }
    must(closes + spoilt + plain === 1000 && s.census.closes === closes && s.census.spoilt === spoilt && s.census.plain === plain && s.mapcount === 'Of these 1,000, ' + closes + ' come home; ' + spoilt + ' hold the square of a prime and march away all the same; ' + plain + ' hold no square, and march away.',
      'the grid\'s sentence counts those that come home, those that hold a square and march away, and the rest, as Python\'s sums have them', s.mapcount);
    const res = await p.evaluate((odd) => { const c = document.getElementById('map'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let wrong = 0, seen = 0, off = 0; const tally = {};
      for (let m = 3; m <= 2001; m += 2) { const k = (m - 3) / 2, q = [((k % 40) + 0.5) * c.width / 40, (Math.floor(k / 40) + 0.5) * c.height / 25], hook = window.GOSPELCELL(m), i = 4 * (Math.floor(q[1]) * c.width + Math.floor(q[0])), col = d[i] + ',' + d[i + 1] + ',' + d[i + 2]; seen++;
        if (Math.abs(hook[0] - q[0]) > 0.01 || Math.abs(hook[1] - q[1]) > 0.01) off++;
        let sq = false; for (let l = 3; l * l <= m; l += 2) if (m % (l * l) === 0) sq = true;
        const want = odd[m][0] ? '168,72,42' : sq ? '43,38,34' : '233,225,207'; if (col !== want) wrong++; tally[col] = (tally[col] || 0) + 1; }
      return { wrong, seen, off, tally }; }, table.odd);
    must(res.wrong === 0 && res.off === 0 && res.seen === 1000 && res.tally['168,72,42'] === closes && res.tally['43,38,34'] === spoilt, 'every square of the grid, at the place the page\'s words give it (forty to a row, read like a page), has the colour that goes with Python\'s sum for its denominator: rust for home, dark for a square that does not save it, pale for none', JSON.stringify(res.tally) + '; ' + res.off + ' places differ from the page\'s own');
    const key = await p.evaluate(() => [].map.call(document.querySelectorAll('.key > span'), el => [getComputedStyle(el.querySelector('.sw')).backgroundColor, el.textContent.trim()]));
    must(JSON.stringify(key) === JSON.stringify([['rgb(168, 72, 42)', 'comes home'], ['rgb(43, 38, 34)', 'holds the square of a prime, and marches away all the same'], ['rgb(233, 225, 207)', 'holds no square: marches away']]), 'the key under the grid gives each of the three colours its right meaning', JSON.stringify(key.map(k => k[0]))); }
  await p.screenshot({ path: path.join(out, 'double-open.png'), fullPage: true });

  // ---- 2. Go, all at once: the book's figure
  s = await once();
  { const w = T.walk(1, 9, 6), pts = await pathOf(), pc = pyCorners(1, 9, pts), fr = await frame(), pt = await pointing(), q6 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), pts[pts.length - 1]);
    must(s.done && !s.running && s.drawn === 6 && s.total === 6 && s.goes === 1 && s.home === 6 && samePath(pts, w) < 1e-12 && pc && pc.n >= 5 && pc.worst < 1e-9, 'Go draws the 6 steps and stops; the path is core.js\'s walk for 1/9 and its corners are where Python\'s walk stands', pc ? pc.n + ' places, worst ' + pc.worst.toExponential(1) : 'no places');
    must(s.report === 'Step 6: home. It is where it began, facing as it began, and its next turn would be 1/9 of a turn again.' && s.fails.length === 0, 'the report says so: Step 6, home', s.report);
    must(fr.ok, 'the figure is inside the frame, and the dark line on the canvas reaches just as far as the page\'s own corners do', 'line x ' + fr.ik.x0 + ' to ' + fr.ik.x1 + ', y ' + fr.ik.y0 + ' to ' + fr.ik.y1 + ' of ' + fr.ik.w + ' by ' + fr.ik.h);
    must(s.dots === 1 && (await rustNear(q6[0], q6[1], 4, 150)) >= 5 && s.guide === null, 'one dot, at the end of the one round, and no dashed line');
    must(pt.n > 40 && Math.hypot(pt.x - pt.at[0], pt.y - pt.at[1]) < 6 && pt.want && cosBetween(pt.tip, pt.want) > 0.9, 'the turtle is drawn at the last corner, which is the start, pointing the way it last stepped'); }
  await p.locator('.stage').screenshot({ path: path.join(out, 'double-book.png') });

  // ---- 3. the paces, on a turtle that marches away (1/63: 240 steps are drawn)
  await typed('1', '63'); await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(1000);
  { const a = await state(), pt = await pointing(), ia = await ink(); await p.waitForTimeout(500); const c = await state();
    must(a.total === 240 && a.running && !a.done && a.drawn >= 30 && a.drawn <= 54 && c.drawn - a.drawn >= 14 && c.drawn - a.drawn <= 27, 'quick: 240 steps at 40 a second, so about 40 are drawn after one second and 20 more half a second later', a.drawn + ' then ' + c.drawn);
    must(a.report === 'Step ' + a.drawn + ' of 240.', 'while it walks the report counts the steps', a.report);
    must(pt.n > 40 && Math.hypot(pt.x - pt.at[0], pt.y - pt.at[1]) < 6 && pt.want && cosBetween(pt.tip, pt.want) > 0.9, 'and the turtle is drawn at the corner it has reached, pointing the way it last stepped', 'step ' + pt.drawn + ', cosine ' + (pt.want ? cosBetween(pt.tip, pt.want).toFixed(3) : 'none'));
    await p.waitForTimeout(5200); const e = await state(), ie = await ink();
    must(e.done && e.drawn === 240 && ia.line > 0.05 * ie.line && ia.line < 0.6 * ie.line, 'only the part walked so far is drawn, and it finishes in about six seconds', ia.line + ' dark pixels then, ' + ie.line + ' at the end'); }
  await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(2000);
  { const a = await state(); must(a.running && a.drawn >= 8 && a.drawn <= 12, 'slow: 5 steps a second, so about 10 after two seconds', String(a.drawn));
    await typed('1', '25'); const c = await state();
    must(!c.running && c.drawn === 0 && !c.done && c.Q === 25 && c.report === 'The turtle is waiting at its start.' && c.say.includes('it comes home after 20 steps') && table.odd[25][0] && table.odd[25][1] === 20, 'changing a number while it walks stops it, puts it back at the start, and gives the new forecast', c.say.slice(0, 70));
    await p.waitForTimeout(400); const d = await state(); must(d.drawn === 0 && !d.running, 'and it stays stopped until Go is pressed'); }

  // ---- 4. the turtles on the buttons
  const want = [['1', '9', '1/9, the book’s figure'], ['1', '45', '1/45: home, against the claim'], ['1', '63', '1/63: away, though it holds 9'], ['1', '171', '1/171, the memo’s exception'], ['1', '7', '1/7: no square'], ['1', '36', '1/36: a tail, then a loop'], ['1', '441', '1/441: one square spoilt, one not'], ['1', '1194649', '1 over 1093 squared']];
  must(JSON.stringify(s.presets) === JSON.stringify(want), 'eight buttons, with the numbers the tests expect');
  await p.selectOption('#pace', 'once');
  for (let n = 0; n < want.length; n++) {
    const [a, i, name] = want[n], P = +a, Q = +i; await p.click('#preset' + n); await p.waitForTimeout(200); s = await state();
    const r = py(P, Q), f = T.forecast(P, Q), pts = await pathOf(), fr = await frame(), pc = pyCorners(P, Q, pts), boxes = await p.inputValue('#num') === a && await p.inputValue('#den') === i;
    const rs = reason(f.m, f.tail);
    let ok = !!r && boxes && s.done && s.fails.length === 0 && fr.ok && rs.home === r.bounded && s.say.endsWith(rs.text) && samePath(pts, T.walk(P, Q, s.total)) < 1e-12 && pc && pc.worst < 1e-9 && f.tail === r.tail && f.round === r.round && f.bounded === r.bounded && s.home === r.home, detail = '';
    const ends = []; for (let j = (r.tail ? 0 : 1); j <= s.rounds; j++) ends.push(r.tail + j * r.round);
    let found = 0; for (const k of [...new Set([ends[0], ends[Math.floor(ends.length / 2)], ends[ends.length - 1]])]) { const q2 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), pts[k]); if ((await rustNear(q2[0], q2[1], 4, 150)) >= 5) found++; else found -= 99; }
    ok = ok && s.dots === ends.length && found > 0;
    if (r.home) { ok = ok && s.total === r.round && s.say.includes('it comes home after ' + T.commas(r.round) + ' steps') && s.report.startsWith('Step ' + T.commas(r.round) + ': home.'); detail = 'home at step ' + s.home; }
    else if (r.bounded) { const back = Math.hypot(pts[r.tail + r.round][0] - pts[r.tail][0], pts[r.tail + r.round][1] - pts[r.tail][1]);
      ok = ok && s.total === r.tail + r.round && back < 1e-9 && s.say.includes('it never comes home, and never gets away') && s.say.includes('After a tail of ' + r.tail + ' steps') && s.report.startsWith('Step ' + s.total + ': back where it stood at step ' + r.tail) && s.report.includes('It is not home'); detail = 'tail ' + r.tail + ', loop ' + r.round; }
    else { let even = true; const B = [pts[r.tail + r.round][0] - pts[r.tail][0], pts[r.tail + r.round][1] - pts[r.tail][1]]; for (let j = 0; j <= s.rounds; j++) if (Math.hypot(pts[r.tail + j * r.round][0] - pts[r.tail][0] - j * B[0], pts[r.tail + j * r.round][1] - pts[r.tail][1] - j * B[1]) > 1e-8) even = false;
      const mid = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), [pts[r.tail][0] + (s.rounds / 2 + 0.25) * B[0], pts[r.tail][1] + (s.rounds / 2 + 0.25) * B[1]]);
      ok = ok && even && s.rounds >= 4 && s.total === r.tail + s.rounds * r.round && Math.abs(Math.hypot(B[0], B[1]) - r.gain) < 1e-9 && Math.abs(s.gain - r.gain) < 1e-9 && s.say.includes('it never comes home.') && s.say.includes('a round does not close')
        && s.report.includes('Each round of ' + T.commas(r.round) + ' steps has carried it ' + r.gain.toFixed(3) + ' steps further along the dashed line, where the dots mark the end of each of the ' + s.rounds + ' rounds drawn.') && (await rustNear(mid[0], mid[1], 8, 40)) > 0;
      detail = s.rounds + ' rounds of ' + r.round + ', ' + r.gain.toFixed(3) + ' steps each'; }
    must(ok, 'the button "' + name + '" puts ' + a + ' and ' + i + ' in the boxes and sends the turtle off; forecast, walk, dots, guide and report agree with core.js and with Python\'s walk; the figure is in the frame', detail + '; ' + s.dots + ' dots');
    if (n === 1) must(r.home === 12 && s.say.endsWith('45 = 3² × 5 holds 3², and nothing spoils it: 3 does not divide the order of 2 modulo 5 (which is 4).'), '1/45: the prime 5 occurs once, and the turtle is home at step 12 all the same; the reason printed is the rule\'s, worked afresh by the test');
    if (n === 2) must(!r.bounded && s.say.endsWith('63 = 3² × 7 holds a square, but it is spoilt: 3 divides the order of 2 modulo 7 (which is 3).'), '1/63: it holds 9 and marches away; the reason printed is the rule\'s');
    if (n === 3) must(!r.bounded && s.say.endsWith('171 = 3² × 19 holds a square, but it is spoilt: 3 divides the order of 2 modulo 19 (which is 18).'), '1/171, the memo\'s exception: spoilt by 19');
    if (n === 4) must(s.say.endsWith('7 holds no square of a prime, and without one a round cannot close.'), '1/7: no square');
    if (n === 5) must(s.say.includes('After a tail of 2 steps its turns') && s.say.endsWith('The odd part of the denominator, 9 = 3², holds its prime 3 at least squared, and there is no other prime in it to spoil that.') && s.pick === null, '1/36: a tail of 2 steps, the reason given for the odd part, 9, and no square of the grid marked');
    if (n === 6) must(r.home === 42 && s.say.endsWith('441 = 3² × 7² holds 7², and nothing spoils it: 7 does not divide the order of 2 modulo 3 (which is 2).') && f.spoilt.length === 1 && f.spoilt[0].l === 3, '1/441: 49 serves (and 9 is spoilt by 7)');
    if (n === 7) must(!r.bounded && r.round === 364 && s.say.endsWith('1,194,649 = 1093² holds a square, but it is spoilt: 2 has the same order modulo 1093² as modulo 1093, so 1093² is of no use.'), '1 over 1093 squared: rounds of 364, and it marches away'),
      await p.setViewportSize({ width: 700, height: 1500 }), await p.waitForTimeout(300),
      must((await rustNear(...(await p.evaluate(([x, y]) => window.GOSPELPX(x, y), [(pts[r.round][0] + pts[2 * r.round][0]) / 2, (pts[r.round][1] + pts[2 * r.round][1]) / 2])), 6, 40)) > 0 && (await state()).report.includes('along the dashed line'), 'and when the window is made narrower the dashed line it speaks of is drawn again'),
      await p.setViewportSize({ width: 1000, height: 1500 }), await p.waitForTimeout(300);
    await p.locator('.stage').screenshot({ path: path.join(out, 'double-' + name.replace(/[^a-z0-9]+/gi, '-').toLowerCase() + '.png') });
  }
  { // which way round and which way up: the turtle's own pixels before and after a walk that ends away from its start
    await typed('1', '63'); const m0 = await pointing(); await once(); const m1 = await pointing(), st = await state(), pts = await pathOf(), e = pts[st.total], k = st.view.k;
    must(m0.n > 40 && m1.n > 40 && Math.abs((m1.x - m0.x) - k * e[0]) < 5 && Math.abs((m1.y - m0.y) + k * e[1]) < 5 && Math.hypot(e[0], e[1]) > 20, 'on the screen the marching turtle ends as far to the right of its start, and as far up, as the walk puts it (neither mirrored nor upside down)', 'walk ' + e[0].toFixed(2) + ', ' + e[1].toFixed(2));
    await typed('1', '4'); await once(); const q4 = await pathOf(); must(q4.length === 33 && q4[1][0] < -0.99 && Math.abs(q4[1][1]) < 1e-9, 'and on the page a first turn of a quarter sends the first step to the left: the turtle turns left', q4[1].map(v => v.toFixed(3)).join(', ')); }

  // ---- 5. what is typed
  await typed('abc', '9'); s = await state();
  { const i5 = await ink();
    must(!s.valid && s.say === 'Type the first turn as two whole numbers, such as 1 and 45; the lower one from 1 to 2,000,000.' && await p.isDisabled('#go') && (await p.getAttribute('#num', 'class') || '').includes('bad') && !(await p.getAttribute('#den', 'class') || '').includes('bad') && i5.line === 0 && s.report === '' && s.deg === '',
      'an upper number that is not a number: the page says what to type, marks that box, disables Go and clears the picture', s.say); }
  { const taken = []; for (const bad of ['0', '2000001', '1.5', '']) { await typed('1', bad); s = await state(); if (s.valid || !(await p.getAttribute('#den', 'class') || '').includes('bad') || !(await p.isDisabled('#go'))) taken.push(bad); }
    must(taken.length === 0, 'a lower number of nought, of more than 2,000,000, with a decimal point, or left empty is refused', taken.length ? 'taken: ' + JSON.stringify(taken) : 'four tried'); }
  await typed('abc', '9'); await p.setViewportSize({ width: 800, height: 1500 }); await p.waitForTimeout(300);
  { const i6 = await ink(), t6 = await p.evaluate(() => { const c = document.getElementById('turtle'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 0) n++; const f = document.getElementById('field'), e = f.getContext('2d').getImageData(0, 0, f.width, f.height).data; let m = 0; for (let i = 3; i < e.length; i += 4) if (e[i] > 0) m++; return [n, m]; });
    must(i6.line === 0 && t6[0] === 0 && t6[1] === 0, 'a refused number, then the window made narrower: the picture stays empty', t6.join(', ') + ' pixels drawn'); }
  await p.setViewportSize({ width: 1000, height: 1500 }); await p.waitForTimeout(200);
  await typed('10', '90'); s = await state();
  must(s.valid && s.forecast.p === 1 && s.forecast.q === 9 && s.deg === '= 40° (1/9 in lowest terms)' && s.say.includes('it comes home after 6 steps'), '10/90 is taken in lowest terms, 1/9, and the page says so');
  await typed('10', '9'); s = await state(); must(s.forecast.p === 1 && s.deg === '= 40° (1/9 in lowest terms, whole turns left out)', '10/9 is taken as 1/9, and the page says that whole turns are left out', s.deg);
  await p.selectOption('#pace', 'once'); await p.press('#den', 'Enter'); await p.waitForTimeout(150); s = await state();
  must(s.done && s.home === 6 && s.report.includes('its next turn would be 1/9 of a turn again'), 'Enter in a box starts it');
  await typed('-1', '9'); s = await once();
  { const pts = await pathOf(), w = T.walk(1, 9, 6); let mirror = 0; for (let k = 0; k <= 6; k++) mirror = Math.max(mirror, Math.abs(pts[k][0] + w.xs[k]), Math.abs(pts[k][1] - w.ys[k]));
    must(s.home === 6 && mirror < 1e-9 && s.forecast.p === 8 && s.deg === '= 320° (8/9 in lowest terms, whole turns left out)' && s.pick === null, '−1/9 is 8/9: the book\'s figure in a mirror, home at step 6; and it is not marked on the grid, whose squares are the turns of 1 over something', 'worst ' + mirror.toExponential(1)); }
  await typed('3', '8'); s = await once();
  { const r = py(3, 8), pts = await pathOf(); must(r.tail === 3 && !r.bounded && s.say.includes('After 3 steps its turn is a whole number of turns, which is no turn, and it walks straight on for ever.') && s.report === 'Step 33: not home, and it will not be. It is walking straight on.' && Math.abs(Math.hypot(pts[33][0] - pts[3][0], pts[33][1] - pts[3][1]) - 30) < 1e-9 && (await frame()).ok,
      '3/8: after 3 steps the turn is whole turns and it walks straight on (30 steps in one line are drawn)', s.report); }
  await typed('1', '1'); s = await once();
  { const pts = await pathOf(), n = pts.length - 1; must(s.forecast.straight && s.forecast.m === 1 && s.forecast.tail === 0 && !s.forecast.bounded && s.home === 0 && s.report.includes('It is walking straight on.') && n >= 20 && Math.abs(Math.hypot(pts[n][0], pts[n][1]) - n) < 1e-9 && (await frame()).ok,
      'a denominator of 1 (no prime in it at all): the turtle walks straight on and is not home', s.say.slice(0, 160) + ' | ' + s.report); }
  await typed('1', '37'); s = await once();
  { const r = table.odd[37], pts = await pathOf(), n = r[1], a = pts[n], c = pts[2 * n], mid = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), [(a[0] + c[0]) / 2, (a[1] + c[1]) / 2]), pa = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), a), pc2 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), c);
    const apart = Math.hypot(pa[0] - pc2[0], pa[1] - pc2[1]), dash = await rustNear(mid[0], mid[1], 6, 40), solid = await rustNear(mid[0], mid[1], 6, 200);
    must(!r[0] && n === 36 && s.rounds === 7 && apart > 40 && dash > 0 && solid === 0, '1/37 (rounds of 36, far apart on the screen): midway between two dots there is the dashed line and no dot', 'dots ' + apart.toFixed(0) + ' px apart; ' + dash + ' dashed pixels, ' + solid + ' solid'); }
  await typed('1', '12'); s = await once();
  { const r = py(1, 12); must(r.tail === 2 && !r.bounded && s.say.includes('After a tail of 2 steps its turns come round again every 2 steps, and a round does not close') && s.say.includes('The odd part of the denominator, 3, holds no square of a prime') && Math.abs(s.gain - r.gain) < 1e-9 && s.fails.length === 0,
      '1/12: a tail of 2, then rounds of 2 that do not close; the reason is given for the odd part, 3', s.say.slice(28, 150)); }
  let asserts5 = 0; const bad5 = [];
  for (const r of table.fracs.filter(r => r.q <= 4000 && r.tail + 40 * r.round <= 20000).slice(40, 64)) {
    await typed(String(r.P), String(r.Q)); s = await once(); const f = s.forecast;
    const rsn = reason(r.q / 2 ** r.tail, r.tail), tailOK = r.round === 1 && !r.bounded && f.straight ? true : (s.say.endsWith(rsn.text) && rsn.home === r.bounded && (r.tail === 0 || r.bounded && r.tail > 0 && s.say.includes('After a tail of ' + r.tail + (r.tail === 1 ? ' step its' : ' steps its')) || !r.bounded && s.say.includes('After a tail of ' + r.tail + (r.tail === 1 ? ' step its' : ' steps its'))));
    const okf = tailOK && f.p === r.p && f.q === r.q && f.tail === r.tail && f.round === r.round && f.bounded === r.bounded && s.home === r.home && s.fails.length === 0 && (r.round === 1 && !r.bounded && f.straight ? true : Math.abs(s.gain - r.gain) < 1e-8);
    const oks = r.home ? s.report.startsWith('Step ' + T.commas(r.round) + ': home.') : r.bounded ? s.report.includes('back where it stood at step') : s.report.includes('not home, and it will not be');
    asserts5++; if (!(okf && oks && (await frame()).ok)) bad5.push(r.P + '/' + r.Q + ': ' + s.report.slice(0, 50)); }
  must(asserts5 === 24 && bad5.length === 0, 'twenty-four made-up fractions from Python\'s table, odd and even denominators: forecast, tail, reason (worked afresh by the test), walk and report agree with Python, and each figure is in the frame', asserts5 + ' tried' + (bad5.length ? '; wrong: ' + bad5.join(' | ') : ''));
  // longer than the page draws
  await typed('1', '59049'); s = await once();
  { const r = py(1, 59049); must(r.bounded && r.round === 39366 && s.total === 20000 && s.say.includes('it comes home after 39,366 steps') && s.say.includes('That is more than this page draws: it will stop at step 20,000.') && s.report === 'Stopped at step 20,000, before the end of its first round of 39,366 steps.' && s.home === 0 && s.fails.length === 0,
      'a turtle whose round is longer than the page draws (3 to the tenth): the forecast still says home after 39,366 steps and that the page will stop at 20,000; the report says it stopped inside its first round', s.report); }
  await typed('1', '160001'); s = await once();
  { const f = T.forecast(1, 160001), w = T.walk(1, 160001, 20000), gain = Math.hypot(w.xs[f.round], w.ys[f.round]);
    must(f.round === 5000 && !f.bounded && s.total === 20000 && s.rounds === 4 && gain > 1 && !s.say.includes('more than this page draws') && s.report.includes('where the dots mark the end of each of the 4 rounds drawn') && s.fails.length === 0,
      '1/160001 (four whole rounds of 5,000 make exactly the 20,000 steps the page draws): nothing is cut, and the page does not say that it is', s.report.slice(0, 80)); }
  await typed('1', '18'); s = await state();
  must(s.say.includes('After a tail of 1 step its turns come round again every 6 steps') && s.forecast.tail === 1, '1/18: a tail of 1 step, said in the singular');
  await typed('1', '19683'); s = await once();
  { const r = py(1, 19683); must(r.home === 13122 && s.home === 13122 && s.report.startsWith('Step 13,122: home.') && (await frame()).ok, '3 to the ninth: home after 13,122 steps, all drawn'); }
  await typed('7', '2000000'); s = await once();
  { const r = py(7, 2000000); must(s.valid && s.forecast.tail === r.tail && s.forecast.round === r.round && s.forecast.bounded === r.bounded && s.fails.length === 0, 'the largest denominator taken, 2,000,000: tail and round as Python found them', 'tail ' + r.tail + ', round ' + r.round + ', bounded ' + r.bounded); }

  // ---- 6. the grid, by hand
  const mbox = async () => p.locator('#map').boundingBox();
  const cell = async (m) => { const bx = await mbox(), c = await p.evaluate((m) => window.GOSPELCELL(m), m); return [bx.x + c[0] / c[2] * bx.width, bx.y + c[1] / c[3] * bx.height]; };
  await p.locator('#map').scrollIntoViewIfNeeded();
  { let tried = 0; const badm = [];
    const ms = [9, 45, 63, 7, 171, 441, 3, 2001, 1125, 1323, 81, 83, 189, 513, 1539, 1143, 275, 1025, 1875, 99, 693]; for (let m = 5; m <= 2001; m += 26) ms.push(m); let homes = 0, spoilts = 0;
    for (const m of ms) { const bx = await mbox(), pl = place(m, bx.width, bx.height); await p.mouse.move(bx.x + pl[0], bx.y + pl[1]); await p.waitForTimeout(20); const txt = (await state()).mapsay, o = table.odd[m], rs = reason(m, 0); tried++; if (o[0]) homes++; else if (hasSquare(m)) spoilts++;
      const okm = txt === '1/' + T.commas(m) + ': ' + (o[0] ? 'comes home after ' + T.commas(o[1]) + ' steps. ' : 'marches away. ') + rs.text && rs.home === o[0];
      if (!okm) badm.push(txt.slice(0, 90)); }
    must(tried === ms.length && tried > 95 && homes > 15 && spoilts >= 6 && badm.length === 0, 'pointing at a square, at the place the page\'s words give it, names its turtle, says whether Python\'s sum has it home (and after how many steps), and gives the reason word for word as the test works it out afresh', tried + ' squares, ' + homes + ' that come home and ' + spoilts + ' with a square that does not save them' + (badm.length ? '; wrong: ' + badm.slice(0, 3).join(' | ') : '')); }
  { const xy = await cell(99); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(700); s = await state();
    must(await p.inputValue('#num') === '1' && await p.inputValue('#den') === '99' && s.Q === 99 && s.pick === 99 && s.done && s.home === table.odd[99][1] && table.odd[99][0], 'clicking a square puts 1 and its denominator in the boxes and sends that turtle off', '1/99: home at step ' + s.home);
    const ring = await p.evaluate((m) => { const c = document.getElementById('map'), q = window.GOSPELCELL(m), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let on = 0, far = 0;
      for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i] < 70 && d[i + 1] > 70 && d[i + 1] < 120 && d[i + 2] > 120) { if (Math.abs(x - q[0]) < 12 && Math.abs(y - q[1]) < 12) on++; else far++; } } return { on, far }; }, 99);
    must(ring.on > 40 && ring.far === 0, 'and a blue frame on the grid marks that square and no other', ring.on + ' pixels, ' + ring.far + ' elsewhere'); }
  { const xy = await cell(63); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(700); s = await state();
    must(s.pick === 63 && s.home === 0 && s.say.includes('it never comes home.') && !table.odd[63][0], 'clicking a dark square sends off a turtle that marches away'); }
  await p.screenshot({ path: path.join(out, 'double-after.png'), fullPage: true });

  // ---- 7. the texts that do not change, against the sealed runs' records and Python's table
  { const txt = await p.evaluate(() => document.querySelector('main').textContent.replace(/\s+/g, ' '));
    const m7 = /up to 10000000: odd m 4999999; with a square (\d+) = [\d.]+; bounded (\d+)/.exec(more), a3 = /A3: m all of whose primes are at least squared: (\d+); of these not bounded: (\d+) \[1194649\]; bounded m with a prime that divides them once: (\d+) \(the least is 45\)/.exec(more.split('up to 10000000')[1] || '');
    must(m7 && a3 && txt.includes('636,963 have such a prime and 2,456 do not') && +a3[3] === 636963 && +m7[2] - +a3[3] === 2456 && +a3[1] - +a3[2] === 2456, 'the note\'s two counts up to ten million (636,963 that come home with a prime occurring once; 2,456 without) are the sealed run\'s', a3 ? a3.slice(1).join(', ') : 'not found');
    const w6 = /up to 1000000: .*weighted by the number of fractions: bounded ([\d.]+), with a square ([\d.]+)/.exec(sealed);
    must(w6 && w6[1] === '0.1090' && txt.includes('0.109 for odd denominators up to a million') && /G1: odd m from 3 to 20,000, p = 1: the round sums to nought exactly when the rule says so in 9999; otherwise in 0/.test(sealed) && txt.includes('for every odd denominator up to 20,000 the steps of a round were added up'),
      'and its weighted share, 0.109 for odd denominators up to a million, and its "every odd denominator up to 20,000" are the sealed run\'s', w6 ? w6[1] : 'not found');
    must(txt.includes('“it seems that your locus is bounded (in fact, eventually periodic) iff the denominator contains as a factor the square of an odd prime other than 1093 and 3511, which must occur at least cubed”') && txt.includes('“a denominator of 171 = 9 * 19 never loops, probably because 9 divides phi(19)”') && txt.includes("which is the share whose denominators hold the square of an odd prime, with the memo's own exceptions not taken off") && !txt.includes('salvaged')
      && txt.includes('“Schroeppel claims that a complete solution to the GOSPEL problem is that the figure will be closed”') && txt.includes('and asks: “Can you prove or disprove this claim?”') && txt.includes('Nobody has checked any of it by hand'),
      'the note quotes the memo (its partial answer, its own exception; of its .155 it says only what the figure counts) and the book (the claim, and the question it asks), and says nobody has checked it by hand');
    must(txt.includes('A memo of 1972 gave a partial answer, and a book of 1981 set a stronger claim as an exercise to prove or disprove. Neither is right as printed, and a theorem of 1863 settles both') && txt.includes('Neither statement is right as printed, and they err in opposite directions')
      && txt.includes("the memo's own rule gets 45 right") && hasSquare(45) && table.odd[45][0] && txt.includes('if every prime of an odd denominator greater than 1 divides it at least squared'), 'the page says what the memo and the book each said, that the memo\'s own rule gets 45 right (45 holds 9, and Python\'s sum has it home), and that the true half of the claim is for odd denominators greater than 1');
    must(txt.includes('The rule is not mine. L. Fuchs proved it in a paper dated Berlin, 1862, and printed in 1863') && txt.includes('D. H. and Emma Lehmer restated it in 1981, and K. Mahler studied these very sums in 1980') && txt.includes('This is a theorem of L. Fuchs, printed in 1863 (below). The write-up has an argument for it that I made before I knew of his.') && !txt.includes('A proof is in the write-up')
      && txt.includes('reached the same rule, the same two counter-examples and the same counts, and found Fuchs') && txt.includes("Mahler's papers and the Lehmers' are unread, and may hold either"), 'the page says, in three places, that the rule is Fuchs\'s; who found that out; and what is unread');
    must(txt.includes('in the grid, ' + s.spoiltcount + '.') && s.spoiltcount === s.census.spoilt + ' of the ' + (s.census.spoilt + s.census.closes) + ' denominators that hold one do' && txt.includes('The least denominator that holds one and marches away all the same is 63')
      && !table.odd[63][0] && hasSquare(63) && Object.keys(table.odd).map(Number).filter(m => m < 63 && hasSquare(m)).every(m => table.odd[m][0]), 'its count of squares that do not save their denominators is the grid\'s, and 63 is the least such in Python\'s table', s.spoiltcount);
    // the folded rule, taken as it is printed, tried by the test on every odd denominator of Python's table
    const printed = txt.includes('A round closes exactly when, for some l, that order is divisible by l, and by l more times than the order of 2 modulo any other prime of q is.'); let agree = 0, nn = 0;
    for (const m of Object.keys(table.odd).map(Number)) { const f = fac(m); nn++; const says = f.some(([l, e]) => { const k = vl(ord(l ** e), l); return k >= 1 && f.filter(x => x[0] !== l).every(x => k > vl(ord(x[0]), l)); }); if (says === table.odd[m][0]) agree++; }
    must(printed && agree === nn && nn === 1500, 'the folded rule, taken as it is printed and tried by the test on every odd denominator from 3 to 3001, says "closes" exactly where Python\'s sums are nought', agree + ' of ' + nn);
    must(txt.includes('So 1/9 comes home (2 has order 6 modulo 9); 1/45 comes home, because 2 has order 4 modulo 5 and 3 does not divide 4; and 1/63 does not, because 2 has order 3 modulo 7, which 3 divides as often as it divides 6.')
      && ord(9) === 6 && ord(5) === 4 && ord(7) === 3 && table.odd[9][0] && table.odd[45][0] && !table.odd[63][0] && ord(1093) === ord(1093 * 1093) && txt.includes('the squares of 1093 and 3511 do not serve either, 2 having the same order modulo each as modulo the prime itself'), 'its three examples are so, and so is what it says of 1093 (the order of 2 is the same modulo 1093 and its square)');
    must(await p.locator('a[href="README.md"]').count() === 1 && fs.existsSync(path.join(path.dirname(path.resolve(process.argv[4])), 'README.md')), 'and it links to the write-up, which is there beside the page\'s files'); }

  // ---- 8. narrow screens, and a change of width
  for (const wpx of [390, 320]) {
    const ph = await b.newPage({ viewport: { width: wpx, height: 800 }, deviceScaleFactor: 3 }); await ph.goto('file://' + page); await ph.waitForTimeout(400);
    await ph.selectOption('#pace', 'once'); await ph.click('#preset2'); await ph.waitForTimeout(250);
    const lay = await ph.evaluate(() => { const r = id => document.getElementById(id).getBoundingClientRect(), f = r('field'), t = r('turtle'), m = r('map'), st = document.querySelector('.stage').getBoundingClientRect();
      return { sw: document.documentElement.scrollWidth, iw: window.innerWidth, right: Math.max(f.right, m.right, st.right), over: Math.max(Math.abs(f.left - t.left), Math.abs(f.top - t.top), Math.abs(f.width - t.width), Math.abs(f.height - t.height)) }; });
    const st = await state(ph), fr = await frame(ph);
    must(lay.sw <= lay.iw && lay.right <= lay.iw - 13.5 && lay.over < 0.5 && st.done && st.home === 0 && st.total === 240 && fr.ok, 'on a screen ' + wpx + ' px wide nothing runs off the side, and the marching figure is drawn whole inside its frame', 'page ' + lay.sw + ' of ' + lay.iw + ' px; canvas ' + fr.ik.w + ' by ' + fr.ik.h);
    if (wpx === 390) await ph.screenshot({ path: path.join(out, 'double-phone.png'), fullPage: true });
    await ph.close(); }
  { const ph = await b.newPage({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 2 }); await ph.goto('file://' + page); await ph.waitForTimeout(400);
    const where = () => ph.evaluate(() => { const r = document.querySelector('.stage').getBoundingClientRect(); return [Math.round(r.top * 10) / 10, Math.round(r.bottom * 10) / 10, window.innerHeight]; });
    const before = await where(); await ph.click('#go'); await ph.waitForTimeout(700); const after = await where(), st = await state(ph);
    must(before[1] > before[2] && after[0] >= 0 && after[1] <= after[2] + 0.05 && st.goes === 1, 'on a small phone (360 by 640) the picture begins below the foot of the screen, and pressing Go brings the whole of it, frame and all, onto the screen', 'picture from ' + before[0] + ' to ' + before[1] + ' px before, ' + after[0] + ' to ' + after[1] + ' after, on a screen ' + after[2] + ' high');
    { const top = await ph.evaluate(() => document.getElementById('map').getBoundingClientRect().top + window.scrollY);
      await ph.evaluate((y) => window.scrollTo(0, y - 40), top); await ph.waitForTimeout(200);
      const b2 = await where(), r2 = await ph.evaluate(() => { const r = document.getElementById('map').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; }), xy = place(45, r2.w, r2.h);
      await ph.mouse.click(r2.x + xy[0], r2.y + xy[1]); await ph.waitForTimeout(700); const a2 = await where(), s2 = await state(ph);
      must((b2[0] < 0 || b2[1] > b2[2]) && a2[0] >= 0 && a2[1] <= a2[2] + 0.05 && s2.Q === 45 && s2.goes === 2 && s2.done && s2.home === 12, 'and there, with the grid on the screen and the picture off it, clicking the square of 45 (at the place the page\'s words give it) sends that turtle off and brings the picture onto the screen', 'picture from ' + b2[0] + ' to ' + b2[1] + ' px before, ' + a2[0] + ' to ' + a2[1] + ' after; home at step ' + s2.home); }
    await ph.close(); }
  await p.click('#preset1'); await p.waitForTimeout(150); await p.setViewportSize({ width: 640, height: 900 }); await p.waitForTimeout(300);
  { const st = await state(), fr = await frame(), pt = await pointing();
    must(st.done && st.drawn === 12 && fr.ok && pt.n > 40 && Math.hypot(pt.x - pt.at[0], pt.y - pt.at[1]) < 6, 'when the window is made narrower the finished figure is drawn again to fit, with its turtle', 'canvas ' + fr.ik.w + ' px wide'); }

  must(errs.length === 0, 'no script error in all of this', errs.join(' | ').slice(0, 200));
  console.log('PAGE TEST: ' + asserts + ' assertions, ' + fails.length + ' failed' + (fails.length ? ': ' + fails.join('; ').slice(0, 400) : ''));
  await b.close(); process.exit(fails.length ? 1 : 0);
})().catch(async e => { asserts++; fails.unshift('the test stopped (' + String(e).split('\n')[0].slice(0, 120) + ')');
  console.log('FAIL the test stopped: ' + String(e).slice(0, 300));
  console.log('PAGE TEST: ' + asserts + ' assertions, ' + fails.length + ' failed: ' + fails.join('; ').slice(0, 400));
  try { if (browser) await browser.close(); } catch (x) {} process.exit(2); });

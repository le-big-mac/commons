// Headless checks of the doubling turtle's page.   usage: node shot-gospel.js PAGE.html OUTDIR CORE.js TABLE.json GOSPEL.out MORE.out SMALL.out
// TABLE.json is made by table.py in Python, by walking and adding up; GOSPEL.out and MORE.out are the sealed runs' records;
// SMALL.out is the record of small.c, which added up every round for every odd denominator up to two million.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const fails = []; let asserts = 0, browser = null;
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]), T = require(path.resolve(process.argv[4])), table = JSON.parse(fs.readFileSync(path.resolve(process.argv[5]), 'utf8'));
  const sealed = fs.readFileSync(path.resolve(process.argv[6]), 'utf8'), more = fs.readFileSync(path.resolve(process.argv[7]), 'utf8'), small = fs.readFileSync(path.resolve(process.argv[8]), 'utf8');
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
  const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹', pw = (l, e) => e === 1 ? String(l) : l + String(e).split('').map(d => SUP[+d]).join('');
  const TIMES = { 2: 'twice', 3: 'three times', 4: 'four times', 5: 'five times', 6: 'six times', 7: 'seven times', 8: 'eight times', 9: 'nine times', 10: 'ten times', 11: 'eleven times', 12: 'twelve times' };
  const andList = a => a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  const num = x => x >= 10000 ? T.commas(x) : String(x);      // 59,393, but 1093
  const rnd = r => 'the round of 1/' + num(r) + ' has ' + T.commas(ord(r)) + (ord(r) === 1 ? ' step' : ' steps');
  // The rule in the turtle's words, as the folded note prints it: a prime l that comes in e times helps if l divides the number of
  // steps in the round of 1/l^e (k times); another prime r undoes it if l^k divides the number of steps in the round of 1/r.
  // one pointer to the folded note, where another prime is spoken of and the sentence does not already send the reader to the rule
  const reason = (m, tail) => { const r = reasonBody(m, tail); return { home: r.home, text: r.text.includes('see the rule below') || !r.text.includes('undo') ? r.text : r.text + ' Why that is the test is in the first note below.' }; };
  const reasonBody = (m, tail) => { const f = fac(m), nf = f.reduce((t, x) => t + x[1], 0), prod = nf <= 4 ? f.flatMap(x => Array(x[1]).fill(num(x[0]))).join(' × ') : f.map(x => num(x[0]) + (x[1] > 1 ? pw(1, x[1]).slice(1) : '')).join(' × '), name = T.commas(m) + (nf > 1 ? ' = ' + prod : ''), odd = tail ? 'The odd part of the bottom number, ' + name + ',' : name;
    let helps = null; const undone = [];
    for (const [l, e] of f) { if (e < 2) continue; const k = vl(ord(l ** e), l);
      if (k < 1) { undone.push({ l, e, self: true }); continue; }
      const by = f.find(([r]) => r !== l && ord(r) % (l ** k) === 0);
      if (by) undone.push({ l, e, k, r: by[0] }); else if (!helps) helps = { l, e, k }; }
    const note = (k, lk) => k > 1 ? ' (the test is with ' + lk + ': see the rule below)' : '';
    if (helps) { const others = f.filter(x => x[0] !== helps.l).map(x => x[0]), lk = T.commas(helps.l ** helps.k), has = ' contains the prime ' + num(helps.l) + ' ' + TIMES[helps.e];
      const too = undone.length ? ' (The prime' + (undone.length > 1 ? 's ' : ' ') + andList(undone.map(b => num(b.l))) + (undone.length > 1 ? ' come' : ' comes') + ' in more than once as well, and ' + (undone.length > 1 ? 'are' : 'is') + ' undone; one prime that helps is enough.)' : '';
      return { home: true, text: !others.length ? odd + has + ', which is what closes the round.'
        : others.length === 1 ? odd + has + ', and its other prime, ' + num(others[0]) + ', does not undo that: ' + rnd(others[0]) + ', which ' + lk + ' does not divide' + note(helps.k, lk) + '.' + too
        : odd + has + ', and its other primes, ' + andList(others.map(num)) + ', do not undo that: ' + andList(others.map(rnd)) + ', and ' + lk + ' divides none of those numbers of steps' + note(helps.k, lk) + '.' + too }; }
    if (nf === 1) return { home: false, text: odd + ' is itself a prime: no prime comes into it more than once, and without that a round cannot close.' };
    if (!undone.length) return { home: false, text: odd + ' contains no prime more than once, and without that a round cannot close.' };
    const each = b => b.self ? 'the round of 1/' + pw(b.l, b.e) + ' is no longer than the round of 1/' + pw(b.l, b.e - 1) + ' (' + T.commas(ord(b.l ** b.e)) + ' steps each)' : rnd(b.r) + ', which ' + T.commas(b.l ** b.k) + ' divides' + note(b.k, T.commas(b.l ** b.k));
    if (undone.length === 1) { const b = undone[0]; return { home: false, text: odd + ' contains the prime ' + num(b.l) + ' ' + TIMES[b.e] + ', but ' + (b.self ? 'for this prime that is not enough: ' : (f.length === 2 ? 'its other prime, ' : 'another of its primes, ') + num(b.r) + ', undoes that: ') + each(b) + '.' }; }
    return { home: false, text: odd + ' contains the primes ' + andList(undone.map(b => num(b.l))) + ' more than once, but each is undone: ' + undone.map(b => 'for ' + num(b.l) + ', ' + (b.self ? '' : 'by ' + num(b.r) + ': ') + each(b)).join('; ') + '.' }; };
  // the turns, from p times a power of 2 (found by squaring, not by doubling step by step), and the whole forecast for a row of Python's table
  const mp = (e, m) => { let r = 1n, x = 2n % BigInt(m), k = BigInt(e); const M = BigInt(m); while (k > 0n) { if (k & 1n) r = r * x % M; x = x * x % M; k >>= 1n; } return r; };
  // a turn as the page should print it: in whole degrees when the bottom number divides 360, and if not as a whole number of q-ths of a turn
  const turnNum = (p0, q, k) => Number(BigInt(p0) * mp(k, q) % BigInt(q));
  const showT = (t, q) => 360 % q === 0 ? (t * (360 / q)) + '°' : T.commas(t);
  const fturn = (p0, q, k) => showT(turnNum(p0, q, k), q);
  let wrapsSeen = 0, wrapsWrong = 0;
  const turnsWant = r => { const s = r.tail, n = r.round, q = r.q, deg = 360 % q === 0, steps = T.commas(n) + (n === 1 ? ' step' : ' steps');
    // a long list of large numbers tells nothing: for a bottom number over 999 that does not divide 360, only how long the round is
    if (!deg && q > 999) return s ? 'Its first ' + (s === 1 ? 'turn never comes again: that step is its tail. After it' : T.commas(s) + ' turns never come again: they are its tail. After them') + ' its turns come round again every ' + steps + '.' : 'Its turns come round again after ' + steps + ': a round of ' + steps + '.';
    const show = n <= 12 && !(s && n > 6) ? n : 6, N = [], R = []; for (let k = 0; k < show; k++) { N.push(turnNum(r.p, q, s + k)); R.push(showT(N[k], q)); }
    // the first turn in the list whose double passes a whole turn is said in full, with the turn that follows it; the test checks that sum itself
    let wrap = ''; for (let i = 0; i < show && !wrap; i++) { const nxt = i + 1 < show ? N[i + 1] : show === n ? N[0] : null;
      if (nxt !== null && 2 * N[i] >= q) { wrapsSeen++; if (2 * N[i] - q !== nxt) wrapsWrong++;
        wrap = deg ? ' (twice ' + R[i] + ' is ' + (2 * N[i] * (360 / q)) + '°, which is a whole turn and ' + showT(nxt, q) + ')' : ' (twice ' + R[i] + ' is ' + T.commas(2 * N[i]) + ', which is ' + T.commas(q) + ' and ' + showT(nxt, q) + ')'; } }
    const unit = deg ? '' : ', in units of 1/' + T.commas(q) + ' of a whole turn';
    const round = (show === n ? R.join(', ') + ', then ' + R[0] + ' again' : R.join(', ') + ' and so on, ' + T.commas(n) + ' turns before ' + R[0] + ' comes again') + wrap;
    if (!s) return 'Its turns' + unit + ': ' + round + ': a round of ' + steps + '.';
    const Tl = []; for (let k = 0; k < Math.min(s, 3); k++) Tl.push(fturn(r.p, r.q, k));
    return 'Its first ' + (s === 1 ? 'turn' + unit + ', ' + Tl[0] + ', never comes again: that step is its tail' : T.commas(s) + ' turns' + unit + ', ' + (s <= 3 ? andList(Tl) : Tl.join(', ') + ' and so on') + ', never come again: they are its tail') + '. After ' + (s === 1 ? 'it' : 'them') + ' its turns go round every ' + steps + ': ' + round + '.'; };
  const sayWant = r => { const rs = reason(r.q / 2 ** r.tail, r.tail), head = 'Forecast, before it moves: ', N = T.commas(r.round);
    if (r.home) return head + 'it comes home after ' + N + ' steps. ' + turnsWant(r) + ' Those ' + N + ' steps end where they began: the round closes. ' + rs.text;
    if (r.bounded) return head + 'it never comes home, and never gets away. ' + turnsWant(r) + ' Those ' + N + ' steps end where they began: the round closes, and it goes round that one loop for ever. ' + rs.text;
    return head + 'it never comes home. ' + turnsWant(r) + ' Those ' + N + (r.round === 1 ? ' step does' : ' steps do') + ' not end where they began: the round does not close, and each round carries it the same distance further along a straight line. ' + rs.text; };
  // the line under the picture: whose walk it is, and the forecast in a few words (so that it is in sight when the forecast itself is off the screen)
  const whoWant = r => 'First turn ' + T.commas(r.p) + '/' + T.commas(r.q) + ' of a whole turn. Forecast: ' + (r.q === 2 ** r.tail ? 'it will walk straight on' : r.home ? 'it will come home after ' + T.commas(r.round) + ' steps' : r.bounded ? 'it will never come home, and never get away' : 'it will never come home') + '.';
  // where the middle of the square for 1/m ought to be on the grid's canvas: forty to a row, read like a page, 25 rows
  const place = (m, w, h) => { const i = (m - 3) / 2; return [((i % 40) + 0.5) * w / 40, (Math.floor(i / 40) + 0.5) * h / 25]; };

  // ---- 1. as it opens
  let s = await state();
  must(errs.length === 0, 'the page opens without a script error', errs.join(' | ').slice(0, 200));
  must(s.valid && s.P === 1 && s.Q === 9 && s.drawn === 0 && !s.running && !s.done && s.goes === 0 && s.report === 'The turtle is waiting at its start.' && await p.inputValue('#num') === '1' && await p.inputValue('#den') === '9', 'it opens on the book\'s turtle (first turn 1/9 of a turn), waiting');
  { const r = py(1, 9);
    must(r.home === 6 && r.bounded && s.say === 'Forecast, before it moves: it comes home after 6 steps. Its turns: 40°, 80°, 160°, 320°, 280°, 200°, then 40° again (twice 320° is 640°, which is a whole turn and 280°): a round of 6 steps. Those 6 steps end where they began: the round closes. 9 = 3 × 3 contains the prime 3 twice, which is what closes the round.' && s.say === sayWant(r) && s.deg === '= 40° (1/9 in lowest terms)' && s.who === 'First turn 1/9 of a whole turn. Forecast: it will come home after 6 steps.' && s.who === whoWant(r) && 640 === 360 + 280,
      'before it moves the forecast says home after 6 steps, lists the six turns (40, 80, 160, 320, 280 and 200 degrees, then 40 again), says in full where the doubling first passes a whole turn (twice 320 is 640, a whole turn and 280) and gives the reason; the line under the picture names the turtle and repeats the forecast in a few words; 6 is the step at which Python\'s walk is home', s.say.slice(0, 110)); }
  { const pt = await pointing(), i0 = await ink(), o = await p.evaluate(() => window.GOSPELPX(0, 0));
    must(pt.n > 40 && Math.hypot(pt.x - o[0], pt.y - o[1]) < 6 && pt.tip[1] < -5 && Math.abs(pt.tip[0]) < 3 && (await rustNear(o[0], o[1], 10, 150)) > 20 && i0.line === 0, 'the turtle is drawn at the start, inside the ring, pointing up the page, and no line is drawn yet');
    const rects = await p.evaluate(() => ['field', 'turtle'].map(id => { const r = document.getElementById(id).getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }));
    must(rects[0].every((v, k) => Math.abs(v - rects[1][k]) < 0.5), 'the sheet the turtle is drawn on lies exactly over the sheet the line is drawn on'); }
  // the grid as it opens
  { let closes = 0, spoilt = 0, plain = 0; for (let m = 3; m <= 2001; m += 2) { if (table.odd[m][0]) closes++; else if (hasSquare(m)) spoilt++; else plain++; }
    must(closes + spoilt + plain === 1000 && s.census.closes === closes && s.census.spoilt === spoilt && s.census.plain === plain && s.mapcount === 'Of these 1,000, ' + closes + ' come home; ' + spoilt + ' contain a prime more than once and march away all the same; ' + plain + ' contain no prime more than once, and march away.',
      'the grid\'s sentence counts those that come home, those that contain a prime more than once and march away, and the rest, as Python\'s sums have them', s.mapcount);
    const res = await p.evaluate((odd) => { const c = document.getElementById('map'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let wrong = 0, seen = 0, off = 0; const tally = {};
      for (let m = 3; m <= 2001; m += 2) { const k = (m - 3) / 2, q = [((k % 40) + 0.5) * c.width / 40, (Math.floor(k / 40) + 0.5) * c.height / 25], hook = window.GOSPELCELL(m), i = 4 * (Math.floor(q[1]) * c.width + Math.floor(q[0])), col = d[i] + ',' + d[i + 1] + ',' + d[i + 2]; seen++;
        if (Math.abs(hook[0] - q[0]) > 0.01 || Math.abs(hook[1] - q[1]) > 0.01) off++;
        let sq = false; for (let l = 3; l * l <= m; l += 2) if (m % (l * l) === 0) sq = true;
        const want = odd[m][0] ? '168,72,42' : sq ? '43,38,34' : '233,225,207'; if (col !== want) wrong++; tally[col] = (tally[col] || 0) + 1; }
      return { wrong, seen, off, tally }; }, table.odd);
    must(res.wrong === 0 && res.off === 0 && res.seen === 1000 && res.tally['168,72,42'] === closes && res.tally['43,38,34'] === spoilt, 'every square of the grid, at the place the page\'s words give it (forty to a row, read like a page), has the colour that goes with Python\'s sum for its denominator: rust for home, dark for a square that does not save it, pale for none', JSON.stringify(res.tally) + '; ' + res.off + ' places differ from the page\'s own');
    const key = await p.evaluate(() => [].map.call(document.querySelectorAll('.key > span'), el => [getComputedStyle(el.querySelector('.sw')).backgroundColor, el.textContent.trim()]));
    must(JSON.stringify(key) === JSON.stringify([['rgb(168, 72, 42)', 'comes home'], ['rgb(43, 38, 34)', 'contains a prime more than once, and marches away all the same'], ['rgb(233, 225, 207)', 'contains no prime more than once: marches away']]) && (await p.evaluate(() => document.querySelector('main').textContent.replace(/\s+/g, ' '))).includes('Tap or click a square to learn what its turtle does; the rust ones come home.'), 'the key under the grid gives each of the three colours its right meaning, and the sentence above it says that the rust ones come home', JSON.stringify(key.map(k => k[0]))); }
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
    must(a.report === 'Step ' + a.drawn + ' of the 240 drawn here.' && a.who === 'First turn 1/63 of a whole turn. Forecast: it will never come home.' && !table.odd[63][0], 'while it walks the line under the picture counts the steps (of the 240 drawn here: this walk has no end), and the line above it says whose walk it is and what the forecast was', a.report);
    must(pt.n > 40 && Math.hypot(pt.x - pt.at[0], pt.y - pt.at[1]) < 6 && pt.want && cosBetween(pt.tip, pt.want) > 0.9, 'and the turtle is drawn at the corner it has reached, pointing the way it last stepped', 'step ' + pt.drawn + ', cosine ' + (pt.want ? cosBetween(pt.tip, pt.want).toFixed(3) : 'none'));
    await p.waitForTimeout(5200); const e = await state(), ie = await ink();
    must(e.done && e.drawn === 240 && ia.line > 0.05 * ie.line && ia.line < 0.6 * ie.line, 'only the part walked so far is drawn, and it finishes in about six seconds', ia.line + ' dark pixels then, ' + ie.line + ' at the end'); }
  await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(2000);
  { const a = await state(); must(a.running && a.drawn >= 8 && a.drawn <= 12, 'slow: 5 steps a second, so about 10 after two seconds', String(a.drawn));
    await typed('1', '25'); const c = await state();
    must(!c.running && c.drawn === 0 && !c.done && c.Q === 25 && c.report === 'The turtle is waiting at its start.' && c.say.includes('it comes home after 20 steps') && table.odd[25][0] && table.odd[25][1] === 20, 'changing a number while it walks stops it, puts it back at the start, and gives the new forecast', c.say.slice(0, 70));
    await p.waitForTimeout(400); const d = await state(); must(d.drawn === 0 && !d.running, 'and it stays stopped until Go is pressed'); }
  // a change of pace is obeyed at once
  await typed('1', '63'); await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(1000);
  { const a = await state(); await p.selectOption('#pace', 'quick'); await p.waitForTimeout(200); const b1 = await state(); await p.waitForTimeout(800); const c = await state(); await p.selectOption('#pace', 'once'); await p.waitForTimeout(150); const d = await state();
    must(a.running && a.drawn >= 3 && a.drawn <= 7 && b1.drawn - a.drawn >= 4 && b1.drawn - a.drawn <= 14 && c.running && c.drawn - a.drawn >= 30 && c.drawn - a.drawn <= 50 && d.done && d.drawn === 240 && d.goes === a.goes, 'a change of pace is obeyed at once, from the step reached: slow for a second (about 5 steps), then quick (about 8 more within a fifth of a second, about 40 more in a second), then all at once (done), with Go pressed once', a.drawn + ', ' + b1.drawn + ', ' + c.drawn + ', ' + d.drawn); }
  // a short walk at "quick" can still be watched
  await typed('1', '9'); await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(700);
  { const a = await state(); await p.waitForTimeout(1200); const c = await state(); await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(1200); const d = await state(); await p.waitForTimeout(2300); const e = await state();
    must(a.running && a.drawn >= 2 && a.drawn <= 3 && c.done && c.home === 6 && d.running && d.drawn >= 2 && d.drawn <= 3 && e.done, 'the six steps of 1/9 can be watched: at "quick" they take a second and a half (two or three drawn after 0.7 s, home by 1.9 s), at "slow" three seconds (two or three drawn after 1.2 s, home by 3.5 s)', a.drawn + ' steps at 0.7 s quick; ' + d.drawn + ' at 1.2 s slow'); }

  // ---- 4. the turtles on the buttons
  const want = [['1', '9', '1/9: home in six steps'], ['1635', '1009681', 'looks home, is not (1635/1009681)'], ['1', '7', '1/7: marches away'], ['1', '36', '1/36: a tail, then a loop'], ['1', '45', '1/45: home (breaks the stricter rule)'], ['1', '63', '1/63: away (breaks the rule of thumb)'], ['1', '171', '1/171: the memo’s own exception'], ['1', '441', '1/441: home, thanks to the two 7s'], ['1', '1194649', '1/1093²: twice is not enough'], ['1', '1000000', '1/1000000: a tail, then a great loop']];
  must(JSON.stringify(s.presets) === JSON.stringify(want), 'ten buttons, with the numbers the tests expect');
  const gsay = g => g >= 0.0005 ? g.toFixed(3) + ' steps' : (g * 1e6).toPrecision(3) + ' millionths of a step';      // how the report should give a distance, written again here
  const txt0 = await p.evaluate(() => document.querySelector('main').textContent.replace(/\s+/g, ' '));
  await p.selectOption('#pace', 'once');
  for (let n = 0; n < want.length; n++) {
    const [a, i, name] = want[n], P = +a, Q = +i; await p.click('#preset' + n); await p.waitForTimeout(200); s = await state();
    const r = py(P, Q), f = T.forecast(P, Q), pts = await pathOf(), fr = await frame(), pc = pyCorners(P, Q, pts), boxes = await p.inputValue('#num') === a && await p.inputValue('#den') === i;
    const rs = reason(f.m, f.tail);
    let ok = !!r && boxes && s.done && s.fails.length === 0 && fr.ok && rs.home === r.bounded && s.say === sayWant(r) && s.who === whoWant(r) && samePath(pts, T.walk(P, Q, s.total)) < 1e-12 && pc && pc.worst < 1e-9 && f.tail === r.tail && f.round === r.round && f.bounded === r.bounded && s.home === r.home, detail = '';
    const ends = []; for (let j = (r.tail ? 0 : 1); j <= s.rounds; j++) ends.push(r.tail + j * r.round);
    let found = 0; for (const k of [...new Set([ends[0], ends[Math.floor(ends.length / 2)], ends[ends.length - 1]])]) { const q2 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), pts[k]); if ((await rustNear(q2[0], q2[1], 4, 150)) >= 5) found++; else found -= 99; }
    ok = ok && s.dots === ends.length && found > 0;
    if (r.home) { ok = ok && s.total === r.round && s.say.includes('it comes home after ' + T.commas(r.round) + ' steps') && s.report.startsWith('Step ' + T.commas(r.round) + ': home.'); detail = 'home at step ' + s.home; }
    else if (r.bounded) { const back = Math.hypot(pts[r.tail + r.round][0] - pts[r.tail][0], pts[r.tail + r.round][1] - pts[r.tail][1]);
      ok = ok && s.total === r.tail + r.round && back < 1e-9 && s.say.includes('it never comes home, and never gets away') && s.say.includes('Its first ' + r.tail + ' turns') && s.say.includes('never come again: they are its tail') && s.report.startsWith('Step ' + T.commas(s.total) + ': back where it stood at step ' + T.commas(r.tail) + ',') && s.report.includes('It is not home'); detail = 'tail ' + r.tail + ', loop ' + r.round; }
    else { let even = true; const B = [pts[r.tail + r.round][0] - pts[r.tail][0], pts[r.tail + r.round][1] - pts[r.tail][1]]; for (let j = 0; j <= s.rounds; j++) if (Math.hypot(pts[r.tail + j * r.round][0] - pts[r.tail][0] - j * B[0], pts[r.tail + j * r.round][1] - pts[r.tail][1] - j * B[1]) > 1e-8) even = false;
      const mid = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), [pts[r.tail][0] + (s.rounds / 2 + 0.25) * B[0], pts[r.tail][1] + (s.rounds / 2 + 0.25) * B[1]]);
      const e0 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), pts[r.tail]), e1 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), pts[r.tail + s.rounds * r.round]), unseen = Math.hypot(e1[0] - e0[0], e1[1] - e0[1]) < s.DPR;
      const rest = unseen ? ', along a line too short to be seen here: the dots that mark the ends of the ' + s.rounds + ' rounds drawn lie on top of one another. At that rate about ' + T.commas(Number((r.round / r.gain).toPrecision(3))) + ' steps carry it one step along that line.'
        : ' along the dashed line, where the dots mark the end of each of the ' + s.rounds + ' rounds drawn.';
      ok = ok && even && s.rounds >= 4 && s.total === r.tail + s.rounds * r.round && Math.abs(Math.hypot(B[0], B[1]) - r.gain) < 1e-12 && Math.abs(s.gain - r.gain) < 1e-12 && s.say.includes('it never comes home.') && s.say.includes('the round does not close')
        && s.report.endsWith('Each round of ' + T.commas(r.round) + ' steps has carried it ' + gsay(r.gain) + ' further' + rest) && (unseen || (await rustNear(mid[0], mid[1], 8, 40)) > 0) && unseen === (Q === 1009681);
      detail = s.rounds + ' rounds of ' + r.round + ', ' + gsay(r.gain) + ' each' + (unseen ? ', the dashed line under a pixel long' : ''); }
    must(ok, 'the button "' + name + '" puts ' + a + ' and ' + i + ' in the boxes and sends the turtle off; forecast, the line under the picture, walk, dots, guide and report agree with core.js and with Python\'s walk; the figure is in the frame', detail + '; ' + s.dots + ' dots');
    if (Q === 45) must(r.home === 12 && s.say.includes('Its turns: 8°, 16°, 32°, 64°, 128°, 256°, 152°, 304°, 248°, 136°, 272°, 184°, then 8° again (twice 256° is 512°, which is a whole turn and 152°): a round of 12 steps.') && 512 === 360 + 152 && s.say.endsWith('45 = 3 × 3 × 5 contains the prime 3 twice, and its other prime, 5, does not undo that: the round of 1/5 has 4 steps, which 3 does not divide. Why that is the test is in the first note below.') && ord(5) === 4, '1/45: the prime 5 comes in once, and the turtle is home at step 12 all the same; its twelve turns are listed, and the reason printed is the rule\'s, worked afresh by the test');
    if (Q === 63) must(!r.bounded && s.say.endsWith('63 = 3 × 3 × 7 contains the prime 3 twice, but its other prime, 7, undoes that: the round of 1/7 has 3 steps, which 3 divides. Why that is the test is in the first note below.') && s.say.includes('Its turns, in units of 1/63 of a whole turn: 1, 2, 4, 8, 16, 32, then 1 again (twice 32 is 64, which is 63 and 1): a round of 6 steps.') && ord(7) === 3, '1/63: it contains 9 and marches away; the reason printed is the rule\'s');
    if (Q === 171) must(!r.bounded && s.say.endsWith('171 = 3 × 3 × 19 contains the prime 3 twice, but its other prime, 19, undoes that: the round of 1/19 has 18 steps, which 3 divides. Why that is the test is in the first note below.') && ord(19) === 18, '1/171, the memo\'s exception: undone by 19');
    if (Q === 7) must(s.say.endsWith('7 is itself a prime: no prime comes into it more than once, and without that a round cannot close.') && s.say.includes('Its turns, in units of 1/7 of a whole turn: 1, 2, 4, then 1 again (twice 4 is 8, which is 7 and 1): a round of 3 steps. Those 3 steps do not end where they began: the round does not close'), '1/7: itself a prime; its three turns are listed in sevenths of a turn, where they double exactly (twice 4 is 8, which is 7 and 1)');
    if (Q === 36) must(s.say.includes('Its first 2 turns, 10° and 20°, never come again: they are its tail. After them its turns go round every 6 steps: 40°, 80°, 160°, 320°, 280°, 200°, then 40° again (twice 320° is 640°, which is a whole turn and 280°). Those 6 steps end where they began: the round closes, and it goes round that one loop for ever.') && s.say.endsWith('The odd part of the bottom number, 9 = 3 × 3, contains the prime 3 twice, which is what closes the round.') && s.pick === null && s.who === 'First turn 1/36 of a whole turn. Forecast: it will never come home, and never get away.', '1/36: a tail of 2 steps (10 and 20 degrees), then the round of 1/9; the reason given for the odd part, 9, and no square of the grid marked');
    if (Q === 441) must(r.home === 42 && s.say.endsWith('441 = 3 × 3 × 7 × 7 contains the prime 7 twice, and its other prime, 3, does not undo that: the round of 1/3 has 2 steps, which 7 does not divide. (The prime 3 comes in more than once as well, and is undone; one prime that helps is enough.) Why that is the test is in the first note below.') && ord(3) === 2 && ord(7) % 3 === 0, '1/441: the 49 helps, and the page says that the 9 is there too and is undone (by 7, whose round of 3 steps 3 divides)');
    if (Q === 1009681) { const top = [...small.matchAll(/^\s+([0-9.e+-]+)\s+m = (\d+)\s+a = (\d+)\s+round of (\d+) steps\s+(real|complex)/gm)].map(x => [parseFloat(x[1]), +x[2], +x[3], +x[4], x[5]]);
      const below6 = /below 1e-06: 0 real, 0 pairs/.test(small), upto = /^odd m from 3 to 2000000:/.test(small), cnt = small.match(/cosets added up: (\d+) real \(the coset is its own negative\), (\d+) pairs/);
      must(!r.bounded && r.round === 232 && r.home === 0 && s.home === 0 && s.fails.length === 0 && s.say.endsWith('1,009,681 = 17 × 59,393 contains no prime more than once, and without that a round cannot close.') && s.say.includes('it never comes home. Its turns come round again after 232 steps: a round of 232 steps. Those 232 steps do not end where they began') && 17 * 59393 === 1009681
        && s.report === 'Step 928: not home, and it will not be. Each round of 232 steps has carried it 1.04 millionths of a step further, along a line too short to be seen here: the dots that mark the ends of the 4 rounds drawn lie on top of one another. At that rate about 223,000,000 steps carry it one step along that line.'
        && Math.abs(232 / r.gain / 223e6 - 1) < 0.005, 'the nearest miss, 1635/1009681: forecast never home; the walk is not home either, and the report gives the miss in millionths of a step, says that the dashed line is too short to see, and how many steps make one step of headway (232 over Python\'s gain)', s.report.slice(40, 130));
      must(upto && below6 && top.length >= 2 && top[0][1] === 1009681 && top[0][2] === 1635 && top[0][3] === 232 && Math.abs(top[0][0] - r.gain) < 1e-12 && Math.abs(s.gain - top[0][0]) < 1e-12 && top[0][0] > 1e-6,
        'and it is the least sum in the record of the program that added up every round for odd denominators up to two million; the page\'s walk gives the same miss as that record and as Python; no round in the record misses by less than a millionth', top.length ? top[0][0].toExponential(6) + ' against the page\'s ' + s.gain.toExponential(6) : 'no list in the record');
      must(txt0.includes('the nearest is 1635/1,009,681, with the 231 other first turns that its doubling passes through: each of its rounds of 232 steps ends ' + (top[0][0] * 1e6).toPrecision(3) + ' millionths of a step from where it began') && txt0.includes('The next nearest misses by ' + (top[1][0] * 1e6).toPrecision(3) + ' millionths.')
        && cnt && txt0.includes('some ' + Math.round((+cnt[1] + +cnt[2]) / 1e6) + ' million of them') && txt0.includes('found the same turtle and the same miss. No person has checked either.') && top[0][3] - 1 === 231, 'the note\'s figures for the nearest miss (the miss, the 231 that tie with it, the next nearest, how many rounds were added up) are the record\'s, and it says that a second program found the same and that no person has checked', cnt ? (+cnt[1] + +cnt[2]) + ' rounds' : ''); }
    if (Q === 1000000) must(r.tail === 6 && r.round === 12500 && r.bounded && !r.home && s.total === 12506 && s.say === 'Forecast, before it moves: it never comes home, and never gets away. Its first 6 turns never come again: they are its tail. After them its turns come round again every 12,500 steps. Those 12,500 steps end where they began: the round closes, and it goes round that one loop for ever. The odd part of the bottom number, 15,625 = 5⁶, contains the prime 5 six times, which is what closes the round.'
      && s.report.startsWith('Step 12,506: back where it stood at step 6') && 15625 === 5 ** 6 && 15625 * 64 === 1000000 && ord(15625) === 12500, '1/1000000: a tail of 6 steps, then one loop of 12,500 for ever; its turns are not listed (a bottom number over 999), only how long the round is; the reason is given for the odd part, 15,625');
    if (Q === 1194649) must(!r.bounded && r.round === 364 && s.say.endsWith('1,194,649 = 1093 × 1093 contains the prime 1093 twice, but for this prime that is not enough: the round of 1/1093² is no longer than the round of 1/1093 (364 steps each).') && ord(1093) === 364 && ord(1093 * 1093) === 364, '1 over 1093 squared: rounds of 364, the same as for 1093, and it marches away'),
      await p.setViewportSize({ width: 700, height: 1500 }), await p.waitForTimeout(300),
      must((await rustNear(...(await p.evaluate(([x, y]) => window.GOSPELPX(x, y), [(pts[r.round][0] + pts[2 * r.round][0]) / 2, (pts[r.round][1] + pts[2 * r.round][1]) / 2])), 6, 40)) > 0 && (await state()).report.includes('along the dashed line'), 'and when the window is made narrower the dashed line it speaks of is drawn again'),
      await p.setViewportSize({ width: 1000, height: 1500 }), await p.waitForTimeout(300);
    await p.locator('.stage').screenshot({ path: path.join(out, 'double-' + name.replace(/[^a-z0-9]+/gi, '-').toLowerCase() + '.png') });
  }
  { // which way round and which way up: the turtle's own pixels before and after a walk that ends away from its start
    await typed('1', '63'); const m0 = await pointing(); await once(); const m1 = await pointing(), st = await state(), pts = await pathOf(), e = pts[st.total], k = st.view.k;
    must(m0.n > 40 && m1.n > 40 && Math.abs((m1.x - m0.x) - k * e[0]) < 5 && Math.abs((m1.y - m0.y) + k * e[1]) < 5 && Math.hypot(e[0], e[1]) > 20, 'on the screen the marching turtle ends as far to the right of its start, and as far up, as the walk puts it (neither mirrored nor upside down)', 'walk ' + e[0].toFixed(2) + ', ' + e[1].toFixed(2));
    await typed('1', '4'); await once(); const q4 = await pathOf(); must(q4.length === 33 && q4[1][0] < -0.99 && Math.abs(q4[1][1]) < 1e-9, 'and on the page a first turn of a quarter sends the first step to the left: the turtle turns left', q4[1].map(v => v.toFixed(3)).join(', ')); }

  // on a wide screen, with boxes, forecast, picture and buttons all in sight: a button that makes the forecast longer leaves the picture where it is
  { await typed('1', '4'); await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(100);
    const look = () => p.evaluate(() => ({ top: document.getElementById('result').getBoundingClientRect().top, say: document.getElementById('say').getBoundingClientRect().height, sayTop: document.getElementById('say').getBoundingClientRect().top, btn: document.getElementById('preset5').getBoundingClientRect().bottom, H: window.innerHeight }));
    const m0 = await look(); await p.click('#preset5'); await p.waitForTimeout(300); const m1 = await look(), st = await state();
    must(m0.btn < m0.H && m0.sayTop > 0 && m1.say - m0.say > 20 && Math.abs(m1.top - m0.top) < 1 && st.done && st.Q === 63, 'on a wide screen, with the forecast, the picture and the buttons all in sight, a button whose forecast is longer (by ' + Math.round(m1.say - m0.say) + ' px) leaves the picture where it was on the screen, to within a pixel: the page scrolls by the difference, in whole pixels', 'picture top ' + m0.top.toFixed(1) + ', then ' + m1.top.toFixed(1)); }
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
  // near misses, typed: the miss in millionths, the headway, a tail, a mirror image; Python's table gives the miss and the round
  { const bad = [], says = { '1739/1094420': '18.0', '12605/1741011': '5.59', '2195/65537': '141', '1008046/1009681': '1.04' };
    for (const key of Object.keys(says)) { const [P, Q] = key.split('/').map(Number);
      await typed(String(P), String(Q)); s = await once(); const r = py(P, Q), pts = await pathOf();
      const e0 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), pts[r.tail]), e1 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), pts[r.tail + s.rounds * r.round]), unseen = Math.hypot(e1[0] - e0[0], e1[1] - e0[1]) < s.DPR;
      const want = 'Step ' + T.commas(r.tail + s.rounds * r.round) + ': not home, and it will not be. Each round of ' + T.commas(r.round) + ' steps has carried it ' + says[key] + ' millionths of a step further, along a line too short to be seen here: the dots that mark the ends of the '
        + s.rounds + ' rounds drawn lie on top of one another. At that rate about ' + T.commas(Number((r.round / r.gain).toPrecision(3))) + ' steps carry it one step along that line.';
      if (!(r && !r.bounded && r.home === 0 && (r.gain * 1e6).toPrecision(3) === says[key] && unseen && s.report === want && s.fails.length === 0 && s.home === 0 && Math.abs(s.gain - r.gain) < 1e-12
            && (P === 1739 ? r.tail === 2 && s.say.includes('Its first 2 turns never come again: they are its tail.') : r.tail === 0) && s.who === whoWant(r) && s.say === sayWant(r) && (P !== 1008046 || Math.abs(r.gain - py(1635, 1009681).gain) < 1e-12))) bad.push(key + ': ' + s.report.slice(40, 150)); }
    must(bad.length === 0, 'four more near misses, typed (18.0 millionths after a tail of 2 steps, 5.59 and 141 millionths, and the mirror image of the nearest, which misses by the same 1.04): each report gives Python\'s miss in millionths, and the steps for one step of headway from Python\'s round and miss', bad.join(' | ')); }
  await typed('1', '1'); s = await once();
  { const pts = await pathOf(), n = pts.length - 1; must(s.forecast.straight && s.forecast.m === 1 && s.forecast.tail === 0 && !s.forecast.bounded && s.home === 0 && s.report.includes('It is walking straight on.') && n >= 20 && Math.abs(Math.hypot(pts[n][0], pts[n][1]) - n) < 1e-9 && (await frame()).ok,
      'a denominator of 1 (no prime in it at all): the turtle walks straight on and is not home', s.say.slice(0, 160) + ' | ' + s.report); }
  await typed('1', '37'); s = await once();
  { const r = table.odd[37], pts = await pathOf(), n = r[1], a = pts[n], c = pts[2 * n], mid = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), [(a[0] + c[0]) / 2, (a[1] + c[1]) / 2]), pa = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), a), pc2 = await p.evaluate(([x, y]) => window.GOSPELPX(x, y), c);
    const apart = Math.hypot(pa[0] - pc2[0], pa[1] - pc2[1]), dash = await rustNear(mid[0], mid[1], 6, 40), solid = await rustNear(mid[0], mid[1], 6, 200);
    must(!r[0] && n === 36 && s.rounds === 7 && apart > 40 && dash > 0 && solid === 0, '1/37 (rounds of 36, far apart on the screen): midway between two dots there is the dashed line and no dot', 'dots ' + apart.toFixed(0) + ' px apart; ' + dash + ' dashed pixels, ' + solid + ' solid'); }
  await typed('1', '12'); s = await once();
  { const r = py(1, 12); must(r.tail === 2 && !r.bounded && s.say === 'Forecast, before it moves: it never comes home. Its first 2 turns, 30° and 60°, never come again: they are its tail. After them its turns go round every 2 steps: 120°, 240°, then 120° again (twice 240° is 480°, which is a whole turn and 120°). Those 2 steps do not end where they began: the round does not close, and each round carries it the same distance further along a straight line. The odd part of the bottom number, 3, is itself a prime: no prime comes into it more than once, and without that a round cannot close.' && s.say === sayWant(r) && Math.abs(s.gain - r.gain) < 1e-9 && s.fails.length === 0,
      '1/12: a tail of 2, then rounds of 2 that do not close; the reason is given for the odd part, 3', s.say.slice(28, 150)); }
  let asserts5 = 0; const bad5 = [];
  for (const r of table.fracs.filter(r => r.q <= 4000 && r.tail + 40 * r.round <= 20000).slice(40, 64)) {
    await typed(String(r.P), String(r.Q)); s = await once(); const f = s.forecast;
    const rsn = reason(r.q / 2 ** r.tail, r.tail), tailOK = (r.round === 1 && !r.bounded && f.straight ? true : (s.say === sayWant(r) && rsn.home === r.bounded)) && s.who === whoWant(r);
    const okf = tailOK && f.p === r.p && f.q === r.q && f.tail === r.tail && f.round === r.round && f.bounded === r.bounded && s.home === r.home && s.fails.length === 0 && (r.round === 1 && !r.bounded && f.straight ? true : Math.abs(s.gain - r.gain) < 1e-8);
    const oks = r.home ? s.report.startsWith('Step ' + T.commas(r.round) + ': home.') : r.bounded ? s.report.includes('back where it stood at step') : s.report.includes('not home, and it will not be');
    asserts5++; if (!(okf && oks && (await frame()).ok)) bad5.push(r.P + '/' + r.Q + ': ' + s.report.slice(0, 50)); }
  must(asserts5 === 24 && bad5.length === 0, 'twenty-four made-up fractions from Python\'s table, odd and even denominators: the whole forecast (verdict, the turns listed, tail, reason) and the line under the picture are the sentences the test builds afresh from Python\'s table, and walk and report agree with Python; each figure is in the frame', asserts5 + ' tried' + (bad5.length ? '; wrong: ' + bad5.join(' | ') : ''));
  // longer than the page draws
  await typed('1', '59049'); s = await once();
  { const r = py(1, 59049); must(r.bounded && r.round === 39366 && s.total === 20000 && s.say.includes('it comes home after 39,366 steps') && s.say.includes('That is more than this page draws: it will stop at step 20,000.') && s.report === 'Stopped at step 20,000, before the end of its first round of 39,366 steps.' && s.home === 0 && s.fails.length === 0,
      'a turtle whose round is longer than the page draws (3 to the tenth): the forecast still says home after 39,366 steps and that the page will stop at 20,000; the report says it stopped inside its first round', s.report); }
  await typed('1', '160001'); s = await once();
  { const f = T.forecast(1, 160001), w = T.walk(1, 160001, 20000), gain = Math.hypot(w.xs[f.round], w.ys[f.round]);
    must(f.round === 5000 && !f.bounded && s.total === 20000 && s.rounds === 4 && gain > 1 && !s.say.includes('more than this page draws') && s.report.includes('where the dots mark the end of each of the 4 rounds drawn') && s.fails.length === 0,
      '1/160001 (four whole rounds of 5,000 make exactly the 20,000 steps the page draws): nothing is cut, and the page does not say that it is', s.report.slice(0, 80)); }
  await typed('1', '18'); s = await state();
  must(s.say.includes('Its first turn, 20°, never comes again: that step is its tail. After it its turns go round every 6 steps: 40°, 80°, 160°, 320°, 280°, 200°, then 40° again (twice 320° is 640°, which is a whole turn and 280°).') && s.forecast.tail === 1 && s.say === sayWant(py(1, 18)), '1/18: a tail of 1 step, said in the singular');
  await typed('3', '8'); s = await state(); must(s.who === 'First turn 3/8 of a whole turn. Forecast: it will walk straight on.' && s.who === whoWant(py(3, 8)), 'for 3/8 the line under the picture says that it will walk straight on');
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
  // blue pixels of the grid's canvas, by how far they are from the middle of the square of 1/m: inside it (the frame of the turtle in the picture), on the ring (the square last tapped), elsewhere
  const blueAt = (m) => p.evaluate((m) => { const c = document.getElementById('map'), q = window.GOSPELCELL(m), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data, cw = c.width / 40; let frame = 0, ring = 0, far = 0;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i] < 70 && d[i + 1] > 70 && d[i + 1] < 120 && d[i + 2] > 120) { const r = Math.hypot(x + 0.5 - q[0], y + 0.5 - q[1]);
      if (Math.abs(x + 0.5 - q[0]) <= cw / 2 + 2 && Math.abs(y + 0.5 - q[1]) <= cw / 2 + 2) frame++; else if (r > 1.5 * cw - 4 && r < 1.5 * cw + 4) ring++; else far++; } } return { frame, ring, far, cw }; }, m);
  { const mapTop = () => p.evaluate(() => document.getElementById('map').getBoundingClientRect().top), wbox = () => p.evaluate(() => { const r = document.getElementById('watchp').getBoundingClientRect(); return [r.top, r.height]; });
    await typed('1', '4'); await p.locator('#map').scrollIntoViewIfNeeded(); await p.waitForTimeout(80);
    const s0 = await state(), y0 = await mapTop(), w0 = await wbox(), xy = await cell(99); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(300); const s1 = await state(), y1 = await mapTop(), w1 = await wbox(), bl = await blueAt(99);
    must(await p.inputValue('#num') === '1' && await p.inputValue('#den') === '4' && s1.Q === 4 && s1.say === s0.say && s1.who === s0.who && s1.report === s0.report && s1.pick === null && s1.goes === s0.goes && !s1.running && s1.drawn === s0.drawn && s1.from === null && s0.watch === null && s0.pend === null
      && s1.pend === 99 && s1.watch === 'Watch 1/99 walk' && s1.mapsay === '1/99: comes home after ' + table.odd[99][1] + ' steps. ' + reason(99, 0).text && table.odd[99][0] && Math.abs(y1 - y0) < 0.5 && Math.abs(w1[0] - w0[0]) < 0.5 && Math.abs(w1[1] - w0[1]) < 0.5 && w0[1] >= 44,
      'clicking a square says under the grid what its turtle does and shows a button to watch it, and changes nothing else: the boxes, the forecast, the picture and its lines are as they were, nothing is sent off, and neither the grid nor the room kept for the button moves on the screen', s1.mapsay.slice(0, 60) + '; boxes ' + await p.inputValue('#num') + ' and ' + await p.inputValue('#den') + '; grid at ' + y0.toFixed(1) + ', then ' + y1.toFixed(1) + '; the button\'s room ' + w0[1].toFixed(0) + ' px, then ' + w1[1].toFixed(0));
    must(bl.ring > 300 && bl.far === 0 && bl.frame === 0, 'a blue ring is drawn round that square, a square and a half in radius, and nothing else on the grid is blue (the turtle in the picture, 1/4, is not one of the grid\'s)', JSON.stringify(bl));
    // pointing elsewhere changes the words; leaving the grid gives back the ringed square's words, which are the button's
    { const xy2 = await cell(63); await p.mouse.move(xy2[0], xy2[1]); await p.waitForTimeout(40); const a = await state(); const bx = await mbox(); await p.mouse.move(bx.x + bx.width + 30, bx.y - 30); await p.waitForTimeout(40); const c = await state();
      must(a.mapsay.startsWith('1/63: marches away.') && a.watch === 'Watch 1/99 walk' && a.pend === 99 && c.mapsay === s1.mapsay && c.watch === 'Watch 1/99 walk', 'pointing at another square shows that square\'s words without choosing it; when the pointer leaves the grid the words are the ringed square\'s again, the one the button names', a.mapsay.slice(0, 22) + ' | ' + c.mapsay.slice(0, 22)); }
    await p.click('#watch'); await p.waitForTimeout(900); s = await state();
    must(s.goes === s0.goes + 1 && s.done && s.Q === 99 && await p.inputValue('#num') === '1' && await p.inputValue('#den') === '99' && s.home === table.odd[99][1] && s.who === 'First turn 1/99 of a whole turn. Forecast: it will come home after ' + table.odd[99][1] + ' steps. Back to the grid.' && s.from === 'grid' && await p.locator('#who a[href="#grid"]').count() === 1 && await p.locator('h2#grid').count() === 1 && s.pick === 99 && s.pend === 99,
      'the button under the grid puts that turtle in the boxes and sends it off; the line under its picture names it, repeats the forecast and has a link back to the grid', '1/99: home at step ' + s.home);
    await p.locator('#map').scrollIntoViewIfNeeded(); await p.waitForTimeout(80);
    { const b2 = await blueAt(99); must(b2.frame > 40 && b2.ring > 300 && b2.far === 0, 'and now that square has a blue frame as well (it is the turtle in the picture), inside its ring, and nothing else is blue', JSON.stringify(b2)); } }
  { const xy = await cell(63); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(200); const s1 = await state(), b99 = await blueAt(99), b63 = await blueAt(63); await p.click('#watch'); await p.waitForTimeout(900); s = await state();
    must(s1.watch === 'Watch 1/63 walk' && s1.mapsay.startsWith('1/63: marches away. ') && s1.pend === 63 && s1.Q === 99 && s1.pick === 99 && b99.frame > 40 && b99.ring === 0 && b63.ring > 300 && b63.frame === 0 && s.pick === 63 && s.Q === 63 && s.home === 0 && s.done && s.say.includes('it never comes home.') && !table.odd[63][0],
      'a dark square, tapped next: the ring moves to it and the button names it, while the picture, the boxes and the frame stay with 1/99 until the button is pressed; then its turtle marches away, as the grid said', JSON.stringify(b99) + ' ' + JSON.stringify(b63));
    await typed('1', '9'); const s2 = await state(), b3 = await blueAt(63); await typed('abc', '9'); const s3 = await state(), b4 = await blueAt(63); await typed('1', '9');
    must(s2.watch === 'Watch 1/63 walk' && s2.pend === 63 && s2.from === null && s2.who === 'First turn 1/9 of a whole turn. Forecast: it will come home after 6 steps.' && await p.locator('#who a').count() === 0 && b3.ring > 300 && !s3.valid && s3.pend === 63 && s3.watch === 'Watch 1/63 walk' && b4.ring > 300 && b4.frame === 0,
      'typing a fraction takes the link back to the grid away, and leaves the grid\'s own choice alone: the ring, the words and the button stay, also while what is typed is not a number'); }
  // a tap on the grid does not stop a walk
  { await typed('1', '63'); await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(700); await p.locator('#map').scrollIntoViewIfNeeded(); const a = await state(), xy = await cell(45); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(700); const c = await state();
    await p.selectOption('#pace', 'once'); await p.waitForTimeout(200); const d = await state();
    must(a.running && c.running && c.drawn >= a.drawn + 2 && c.Q === 63 && c.pend === 45 && c.watch === 'Watch 1/45 walk' && c.goes === a.goes && d.done && d.Q === 63 && d.drawn === 240, 'a tap on the grid while a turtle is walking does not stop it: 1/63 walks on (' + a.drawn + ' steps, then ' + c.drawn + ') and finishes, with the square of 45 ringed and waiting'); }
  await p.screenshot({ path: path.join(out, 'double-after.png'), fullPage: true });

  // ---- 7. the texts that do not change, against the sealed runs' records and Python's table
  { const txt = await p.evaluate(() => document.querySelector('main').textContent.replace(/\s+/g, ' '));
    const m7 = /up to 10000000: odd m 4999999; with a square (\d+) = [\d.]+; bounded (\d+)/.exec(more), a3 = /A3: m all of whose primes are at least squared: (\d+); of these not bounded: (\d+) \[1194649\]; bounded m with a prime that divides them once: (\d+) \(the least is 45\)/.exec(more.split('up to 10000000')[1] || '');
    must(m7 && a3 && txt.includes('636,963 have such a prime and 2,456 do not') && +a3[3] === 636963 && +m7[2] - +a3[3] === 2456 && +a3[1] - +a3[2] === 2456, 'the note\'s two counts up to ten million (636,963 that come home with a prime occurring once; 2,456 without) are the sealed run\'s', a3 ? a3.slice(1).join(', ') : 'not found');
    const w6 = /up to 1000000: .*weighted by the number of fractions: bounded ([\d.]+), with a square ([\d.]+)/.exec(sealed);
    must(w6 && w6[1] === '0.1090' && txt.includes('0.109 for odd denominators up to a million') && /G1: odd m from 3 to 20,000, p = 1: the round sums to nought exactly when the rule says so in 9999; otherwise in 0/.test(sealed) && txt.includes('for every odd denominator up to 20,000 the steps of a round were added up'),
      'and its weighted share, 0.109 for odd denominators up to a million, and its "every odd denominator up to 20,000" are the sealed run\'s', w6 ? w6[1] : 'not found');
    must(txt.includes('“it seems that your locus is bounded (in fact, eventually periodic) iff the denominator contains as a factor the square of an odd prime other than 1093 and 3511, which must occur at least cubed”') && txt.includes('“a denominator of 171 = 9 * 19 never loops, probably because 9 divides phi(19)”') && txt.includes("which is the share whose denominators contain the square of an odd prime, with the memo's own exceptions not taken off") && !txt.includes('salvaged')
      && txt.includes('“Schroeppel claims that a complete solution to the GOSPEL problem is that the figure will be closed”') && txt.includes('and asks: “Can you prove or disprove this claim?”') && txt.includes('Nobody has checked any of it by hand'),
      'the note quotes the memo (its partial answer, its own exception; of its .155 it says only what the figure counts) and the book (the claim, and the question it asks), and says nobody has checked it by hand');
    { // the sum of the steps of one round for 1/9009, added up here (the memo's third exception is beyond Python's table of odd denominators to 3001)
      let n9 = 1, t9 = 2 % 9009; while (t9 !== 1) { t9 = t9 * 2 % 9009; n9++; } let x9 = 0, y9 = 0, h9 = 0, tt = 1; for (let k = 0; k < n9; k++) { h9 = (h9 + tt) % 9009; x9 += Math.cos(2 * Math.PI * h9 / 9009); y9 += Math.sin(2 * Math.PI * h9 / 9009); tt = tt * 2 % 9009; }
      const above = await p.evaluate(() => { const ps = [].filter.call(document.querySelectorAll('main > p'), el => el.textContent.trim().startsWith('Which turtles come home?')); return ps.length === 1 && ps[0].getBoundingClientRect().bottom <= document.getElementById('presets').getBoundingClientRect().top && ps[0].getBoundingClientRect().top >= document.getElementById('result').getBoundingClientRect().bottom; });
      must(txt.includes('Which turtles come home? Only some of those whose bottom number has a repeated odd prime, as 9 = 3 × 3 has. A memo of 1972 gave that as its rule of thumb for a turtle that does not march away (of two special primes, 1093 and 3511, it asked for three), and named three exceptions of its own, 1/171 the smallest of them. The smallest exception of all is 1/63.')
        && txt.includes('A book of 1981 set a stricter rule as a puzzle, to prove or disprove: every prime of the bottom number repeated, and none of them special. 1/45 breaks it. The rule that holds was printed in 1863, and is in the first note below.') && above
        && !table.odd[171][0] && hasSquare(171) && !table.odd[2525][0] && hasSquare(2525) && hasSquare(9009) && Math.hypot(x9, y9) > 5 && Math.hypot(x9, y9) < 5.2 && 171 < 2525 && 2525 < 9009
        && Object.keys(table.odd).map(Number).filter(m => hasSquare(m) && !table.odd[m][0]).sort((a, b) => a - b)[0] === 63
        && Object.keys(table.odd).map(Number).filter(m => table.odd[m][0] && fac(m).some(x => x[1] === 1)).sort((a, b) => a - b)[0] === 45
        && txt.includes('Neither statement is right as printed, and they err in opposite directions')
        && txt.includes("the memo's own rule gets 45 right") && hasSquare(45) && table.odd[45][0] && hasSquare(63) && !table.odd[63][0] && txt.includes('if every prime of an odd denominator greater than 1 divides it at least squared'),
        'the paragraph above the buttons states in plain words the memo\'s rule of thumb, its two special primes and its three exceptions (171 and 2525 march away in Python\'s table, and the round of 1/9009, added up here, does not close; 171 is the smallest of the three), that the smallest exception of all is 63 (so it is in Python\'s table), and the stricter rule the book set as a puzzle, which 45 breaks (the least denominator in Python\'s table that comes home with a prime that comes in once); and the note says that the memo\'s own rule gets 45 right, and that the true half of the claim is for odd denominators greater than 1', 'one round of 1/9009 (' + n9 + ' steps) ends ' + Math.hypot(x9, y9).toFixed(2) + ' steps from where it began'); }
    { const odds = Object.keys(table.odd).map(Number), closing = odds.filter(m => table.odd[m][0]);
      must(txt.includes('it will come home, or march away for ever, or go round one loop for ever without getting home. Most first turns send it marching away.') && txt.includes('Which turtles come home? Only some of those whose bottom number has a repeated odd prime, as 9 = 3 × 3 has.') && closing.length > 200 && closing.every(hasSquare) && closing.length < odds.length / 2 && odds.some(m => hasSquare(m) && !table.odd[m][0]) && table.fracs.filter(r => r.bounded).every(r => hasSquare(r.q / 2 ** r.tail)),
        'the page\'s plain rule of thumb is so in Python\'s table: every denominator whose round closes contains an odd prime more than once; some that do are not saved; and fewer than half of the odd denominators to 3001 close', closing.length + ' of ' + odds.length + ' close'); }
    must(txt.includes('Noon is an AI, one of three that keep this notebook; no person has checked this page.') && txt.includes('(the first page calls it a lap)') && await p.locator('a[href="../agent2-inspi/turtle.html"]').count() === 1, 'the foot of the page says what Noon is and that no person has checked the page, and links to the easier page');
    must(txt.includes('The rule is not mine. L. Fuchs proved it in a paper dated Berlin, 1862, and printed in 1863') && txt.includes('D. H. and Emma Lehmer restated it in 1981, and K. Mahler studied these very sums in 1980') && txt.includes('This is a theorem of L. Fuchs, printed in 1863 (below), put into the turtle\'s words: the number of steps in the round of 1/r is what books call the order of 2 modulo r. The write-up has an argument for it that I made before I knew of his.') && !txt.includes('A proof is in the write-up')
      && txt.includes('reached the same rule, the same two counter-examples and the same counts, and found Fuchs') && txt.includes("Mahler's papers and the Lehmers' are unread, and may hold either"), 'the page says, in three places, that the rule is Fuchs\'s; who found that out; and what is unread');
    must(txt.includes('in the grid, ' + s.spoiltcount + '.') && s.spoiltcount === s.census.spoilt + ' of the ' + (s.census.spoilt + s.census.closes) + ' denominators that contain one do' && txt.includes('The least denominator that contains one and marches away all the same is 63')
      && !table.odd[63][0] && hasSquare(63) && Object.keys(table.odd).map(Number).filter(m => m < 63 && hasSquare(m)).every(m => table.odd[m][0]), 'its count of squares that do not save their denominators is the grid\'s, and 63 is the least such in Python\'s table', s.spoiltcount);
    // the folded rule, taken as it is printed, tried by the test on every odd denominator of Python's table
    const printed = txt.includes('A prime that comes into q only once never helps. For a prime l that comes in e times, with e at least 2, take the turtle whose first turn is 1 over le, and count how many times l divides the number of steps in its round: say k times.')
      && txt.includes('The prime l helps if k is at least 1. Another prime r of q undoes it if lk divides the number of steps in the round of 1/r. A round closes exactly when q has a prime that helps and that no other prime of q undoes.'); let agree = 0, nn = 0, kIsE = true;
    // to the letter: "the number of steps in the round of 1/x" is found here by walking the turns of 1/x until the first comes again
    const roundSteps = x => { let k = 1, t = 2 % x; while (t !== 1 % x) { t = t * 2 % x; k++; } return k; };
    for (const m of Object.keys(table.odd).map(Number)) { const f = fac(m); nn++;
      const says = f.some(([l, e]) => { if (e < 2) return false; let k = 0, st = roundSteps(l ** e); while (st % l === 0) { st /= l; k++; } if (l !== 1093 && l !== 3511 && k !== e - 1) kIsE = false; if (k < 1) return false; return !f.some(([r]) => r !== l && roundSteps(r) % (l ** k) === 0); });
      if (says === table.odd[m][0]) agree++; }
    must(printed && agree === nn && nn === 1500 && kIsE && txt.includes('(For every prime but 1093 and 3511, as far as anyone knows, k is e − 1.)'), 'the folded rule, taken as it is printed (helps, undoes) and tried by the test on every odd denominator from 3 to 3001, says "closes" exactly where Python\'s sums are nought; and k is e − 1 each time', agree + ' of ' + nn);
    must(txt.includes('When a round closes: three examples. 1/9 comes home: the round of 1/9 has 6 steps, which 3 divides once, and 9 has no other prime. 1/45 comes home, because the round of 1/5 has 4 steps, which 3 does not divide. And 1/63 does not, because the round of 1/7 has 3 steps, which 3 divides. (For 1093 twice is not enough: the round of 1/1093² is no longer than the round of 1/1093.)') && txt.indexOf('three examples') < txt.indexOf('The rule in general')
      && ord(9) === 6 && vl(6, 3) === 1 && ord(5) === 4 && 4 % 3 !== 0 && ord(7) === 3 && table.odd[9][0] && table.odd[45][0] && !table.odd[63][0] && ord(1093) === ord(1093 * 1093), 'its three examples are so, and so is what it says of 1093 (the round is no longer for its square)');
    must(await p.locator('a[href="README.md"]').count() === 1 && fs.existsSync(path.join(path.dirname(path.resolve(process.argv[4])), 'README.md')), 'and it links to the write-up, which is there beside the page\'s files'); }

  // ---- 8. narrow screens, and a change of width
  for (const wpx of [390, 320]) {
    const ph = await b.newPage({ viewport: { width: wpx, height: 800 }, deviceScaleFactor: 3 }); await ph.goto('file://' + page); await ph.waitForTimeout(400);
    await ph.selectOption('#pace', 'once'); await ph.click('#preset5'); await ph.waitForTimeout(250);
    const lay = await ph.evaluate(() => { const r = id => document.getElementById(id).getBoundingClientRect(), f = r('field'), t = r('turtle'), m = r('map'), st = document.querySelector('.stage').getBoundingClientRect();
      return { sw: document.documentElement.scrollWidth, iw: window.innerWidth, right: Math.max(f.right, m.right, st.right), over: Math.max(Math.abs(f.left - t.left), Math.abs(f.top - t.top), Math.abs(f.width - t.width), Math.abs(f.height - t.height)) }; });
    const st = await state(ph), fr = await frame(ph);
    must(lay.sw <= lay.iw && lay.right <= lay.iw - 13.5 && lay.over < 0.5 && st.done && st.home === 0 && st.total === 240 && fr.ok, 'on a screen ' + wpx + ' px wide nothing runs off the side, and the marching figure is drawn whole inside its frame', 'page ' + lay.sw + ' of ' + lay.iw + ' px; canvas ' + fr.ik.w + ' by ' + fr.ik.h);
    if (wpx === 390) await ph.screenshot({ path: path.join(out, 'double-phone.png'), fullPage: true });
    if (wpx === 390) {
      const goAt = () => ph.evaluate(() => { const r = document.getElementById('go').getBoundingClientRect(); return [r.left, r.top + window.scrollY]; });
      await ph.fill('#num', '1'); await ph.fill('#den', '9'); const g0 = await goAt(); await ph.fill('#den', '63'); const g1 = await goAt(); await ph.fill('#den', '1000000'); const g2 = await goAt(); await ph.fill('#num', '1635'); await ph.fill('#den', '1009681'); const g3 = await goAt();
      must([g1, g2, g3].every(g => Math.abs(g[0] - g0[0]) < 0.5 && Math.abs(g[1] - g0[1]) < 0.5), 'Go stays where it is while the fraction is typed (1/9, 1/63, 1/1000000, 1635/1009681), on a screen 390 px wide', JSON.stringify([g0, g1, g2, g3].map(g => g.map(Math.round))));
      // the picture stays put when a button changes the words above it
      await ph.click('#preset0'); await ph.waitForTimeout(250);
      await ph.evaluate(() => window.scrollBy(0, document.getElementById('result').getBoundingClientRect().top - 30)); await ph.waitForTimeout(100);
      const look = () => ph.evaluate(() => ({ top: document.getElementById('result').getBoundingClientRect().top, say: document.getElementById('say').getBoundingClientRect().height }));
      const m0 = await look(); await ph.click('#preset1'); await ph.waitForTimeout(350); const m1 = await look(), s8 = await state(ph), blk = await ph.evaluate(() => { const a = document.getElementById('say').getBoundingClientRect(), r = document.getElementById('result').getBoundingClientRect(); return [a.top, r.bottom, window.innerHeight]; });
      must(Math.abs(m1.say - m0.say) > 20 && m0.top < 60 && blk[0] >= 0 && blk[0] < 2 && blk[1] <= blk[2] && s8.Q === 1009681 && s8.done, 'with the picture near the top of the screen and its forecast off the top, a button brings the new forecast, the picture and the lines under it onto the screen together, the forecast at the top', 'forecast ' + Math.round(m0.say) + ' px tall, then ' + Math.round(m1.say) + '; the forecast now begins at ' + blk[0].toFixed(1) + ' and the lines end at ' + blk[1].toFixed(1) + ' of ' + blk[2]);
      const tall = await ph.evaluate(() => ({ b: Array.from(document.querySelectorAll('#presets button')).map(b => b.getBoundingClientRect().height), s: Array.from(document.querySelectorAll('summary')).map(b => b.getBoundingClientRect().height), go: document.getElementById('go').getBoundingClientRect().height }));
      must(tall.b.length === 10 && Math.min(...tall.b) >= 44 && Math.min(...tall.s) >= 34 && tall.go >= 40 && (await ph.evaluate(() => Array.from(document.querySelectorAll('#presets button')).every(b => getComputedStyle(b).minHeight === '44px'))), 'on a phone every button is at least 44 px tall, and is told to be whatever its label (a least height of 44 px: as the labels stand, each row holds one that runs to two lines, so the rule itself is looked at); Go is at least 40, and the headings of the folded notes at least 34', 'buttons ' + Math.round(Math.min(...tall.b)) + ', notes ' + Math.round(Math.min(...tall.s)) + ', Go ' + Math.round(tall.go));
    }
    await ph.close(); }
  { const ph = await b.newPage({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 2 }); await ph.goto('file://' + page); await ph.waitForTimeout(400);
    const where = () => ph.evaluate(() => { const r = document.getElementById('result').getBoundingClientRect(), st = document.querySelector('.stage').getBoundingClientRect(), rp = document.getElementById('report').getBoundingClientRect(), sy = document.getElementById('say').getBoundingClientRect(), wh = document.getElementById('who').getBoundingClientRect();
      return [Math.round(r.top * 10) / 10, Math.round(r.bottom * 10) / 10, window.innerHeight, st.top >= r.top - 0.5 && wh.top >= st.bottom - 0.5 && rp.top >= wh.bottom - 0.5 && rp.bottom <= r.bottom + 0.5, Math.round(sy.top * 10) / 10, r.bottom - sy.top]; });
    const before = await where(); await ph.click('#go'); await ph.waitForTimeout(2000); const after = await where(), st = await state(ph);
    // here the forecast, the picture and its lines are together taller than the screen: the picture and its lines must be wholly in sight, and the first of those lines repeats the forecast
    must(before[1] > before[2] && after[5] > after[2] - 1 && after[0] >= 0 && after[1] <= after[2] && after[1] > after[2] - 1 && after[3] && st.goes === 1 && st.done && st.report.startsWith('Step 6: home.') && st.who === 'First turn 1/9 of a whole turn. Forecast: it will come home after 6 steps.',
      'on a small phone (360 by 640) the picture begins below the foot of the screen, and the forecast with the picture and its lines is taller than the screen; pressing Go brings the picture and, under it, the line that names the turtle and repeats the forecast ("it will come home after 6 steps") and the line that says what happened ("Step 6: home.") wholly onto the screen, at its foot, so that as much of the forecast as there is room for is above them', 'picture and lines from ' + before[0] + ' to ' + before[1] + ' px before; after, from ' + after[0] + ' to ' + after[1] + ' on a screen ' + after[2] + ' high; the forecast begins at ' + after[4]);
    { const top = await ph.evaluate(() => document.getElementById('map').getBoundingClientRect().top + window.scrollY);
      await ph.evaluate((y) => window.scrollTo(0, y - 40), top); await ph.waitForTimeout(200);
      const b2 = await where(), r2 = await ph.evaluate(() => { const r = document.getElementById('map').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; }), xy = place(45, r2.w, r2.h);
      const gridTop = () => ph.evaluate(() => document.getElementById('map').getBoundingClientRect().top); const y0 = await gridTop(); await ph.mouse.click(r2.x + xy[0], r2.y + xy[1]); await ph.waitForTimeout(300); const s1 = await state(ph), y1 = await gridTop();
      const wb = await ph.evaluate(() => { const r = document.getElementById('watch').getBoundingClientRect(), m = document.getElementById('map').getBoundingClientRect(), t = document.getElementById('mapsay').getBoundingClientRect(); return { top: r.top, bottom: r.bottom, h: r.height, under: r.top - m.bottom, sayTop: t.top, H: window.innerHeight }; });
      await ph.click('#watch'); await ph.waitForTimeout(3600); const a2 = await where(), s2 = await state(ph), link = await ph.evaluate(() => { const a = document.querySelector('#who a'); return a ? Math.min(...Array.from(a.getClientRects()).map(r => r.height)) : 0; })      // the least of its boxes: a link broken over two lines of small print is not thereby tall;
      must((b2[0] < 0 || b2[1] > b2[2]) && s1.Q === 9 && s1.pend === 45 && s1.goes === 1 && Math.abs(y1 - y0) < 0.5 && s1.watch === 'Watch 1/45 walk' && s1.mapsay.startsWith('1/45: comes home after 12 steps. ') && wb.under >= 0 && wb.under < 16 && wb.h >= 44 && wb.bottom <= wb.H && wb.sayTop >= wb.bottom && wb.sayTop < wb.H
        && a2[0] >= 0 && a2[1] <= a2[2] + 0.05 && s2.Q === 45 && s2.goes === 2 && s2.done && s2.home === 12 && s2.who === 'First turn 1/45 of a whole turn. Forecast: it will come home after 12 steps. Back to the grid.' && link >= 30,
        'and there, with the grid on the screen and the picture off it, a tap on the square of 45 (at the place the page\'s words give it) leaves the grid where it is on the screen and the turtle in the boxes as it was (1/9); directly under the grid, on the screen, are a button at least 44 px tall that names 1/45 and, under it, what that turtle does; the button then sends it off and brings the picture and the lines under it onto the screen, where the link back to the grid is at least 30 px tall in every line it runs over', 'link ' + link.toFixed(0) + ' px tall; grid at ' + y0.toFixed(1) + ' px before the tap and ' + y1.toFixed(1) + ' after; button ' + wb.under.toFixed(0) + ' px under the grid, ' + wb.h.toFixed(0) + ' tall; picture and lines from ' + a2[0] + ' to ' + a2[1] + ' after the button; home at step ' + s2.home); }
    { await ph.selectOption('#pace', 'once'); await ph.evaluate(() => window.scrollTo(0, 0)); await ph.click('#preset5'); await ph.waitForTimeout(300);
      // further down, where the buttons are on the screen and the picture is partly off its top
      await ph.evaluate(() => document.getElementById('preset1').scrollIntoView({ block: 'end' })); await ph.waitForTimeout(150);
      const look = () => ph.evaluate(() => { const r = document.getElementById('result').getBoundingClientRect(), w = document.getElementById('who').getBoundingClientRect(); return { top: r.top, bottom: r.bottom, say: document.getElementById('say').getBoundingClientRect().height, H: window.innerHeight, whoTop: w.top, whoBottom: w.bottom, btn: document.getElementById('preset1').getBoundingClientRect().bottom }; });
      const m0 = await look(); await ph.click('#preset1'); await ph.waitForTimeout(350); const m1 = await look(), s8 = await state(ph);
      must(m0.top < -20 && m0.btn < m0.H + 1 && m1.say + (m1.bottom - m1.top) > m1.H && m1.top >= 0 && m1.top < 1.01 && m1.bottom <= m1.H && m1.whoTop >= 0 && m1.whoBottom <= m1.H && s8.Q === 1009681 && s8.done && s8.who === 'First turn 1,635/1,009,681 of a whole turn. Forecast: it will never come home.',
        'further down the small phone\'s screen, where the buttons are in sight and the picture is partly off the top, a button whose forecast, picture and lines are together taller than the screen (the nearest miss) brings the picture to the top of the screen with the lines under it in sight, and the first of those lines says which turtle it is and repeats the forecast', 'together ' + Math.round(m1.say + m1.bottom - m1.top) + ' px on a screen ' + m1.H + ' high; picture top ' + m0.top.toFixed(1) + ' before the tap, ' + m1.top.toFixed(1) + ' after; lines end at ' + m1.bottom.toFixed(1)); }
    { await ph.selectOption('#pace', 'once'); await ph.fill('#num', '1635'); await ph.fill('#den', '1009681'); await ph.evaluate(() => window.scrollTo(0, 0)); await ph.click('#go'); await ph.waitForTimeout(400);
      const a3 = await where(), s3 = await state(ph), lines = await ph.evaluate(() => { const r = document.getElementById('report'); return [r.getBoundingClientRect().height, parseFloat(getComputedStyle(r).minHeight)]; });
      must(s3.done && s3.report.endsWith('steps carry it one step along that line.') && lines[0] > lines[1] + 10 && a3[0] >= 0 && a3[1] <= a3[2] + 0.05 && a3[3], 'and there the nearest miss, whose line under the picture is longer than the room kept for it, is still wholly on the screen with its picture when the walk ends', 'the line is ' + Math.round(lines[0]) + ' px tall, the room kept ' + Math.round(lines[1]) + '; picture and line from ' + a3[0] + ' to ' + a3[1] + ' on a screen ' + a3[2] + ' high'); }
    await ph.close(); }
  await p.click('#preset4'); await p.waitForTimeout(150); await p.setViewportSize({ width: 640, height: 900 }); await p.waitForTimeout(300);
  { const st = await state(), fr = await frame(), pt = await pointing();
    must(st.done && st.drawn === 12 && fr.ok && pt.n > 40 && Math.hypot(pt.x - pt.at[0], pt.y - pt.at[1]) < 6, 'when the window is made narrower the finished figure is drawn again to fit, with its turtle', 'canvas ' + fr.ik.w + ' px wide'); }

  must(wrapsSeen >= 20 && wrapsWrong === 0, 'in every forecast built above that says where the doubling first passes a whole turn, the sum is right: twice the turn, less a whole turn, is the turn that follows', wrapsSeen + ' such sentences');
  must(errs.length === 0, 'no script error in all of this', errs.join(' | ').slice(0, 200));
  console.log('PAGE TEST: ' + asserts + ' assertions, ' + fails.length + ' failed' + (fails.length ? ': ' + fails.join('; ').slice(0, 400) : ''));
  await b.close(); process.exit(fails.length ? 1 : 0);
})().catch(async e => { asserts++; fails.unshift('the test stopped (' + String(e).split('\n')[0].slice(0, 120) + ')');
  console.log('FAIL the test stopped: ' + String(e).slice(0, 300));
  console.log('PAGE TEST: ' + asserts + ' assertions, ' + fails.length + ' failed: ' + fails.join('; ').slice(0, 400));
  try { if (browser) await browser.close(); } catch (x) {} process.exit(2); });

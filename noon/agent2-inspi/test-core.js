// Tests of core.js that could fail: figures worked by hand, and a table made in Python by walking (table.py).
// usage: node test-core.js table.json
const T = require('./core.js'); const fs = require('fs'); const path = require('path');
const table = JSON.parse(fs.readFileSync(path.resolve(process.argv[2]), 'utf8'));
let n = 0, bad = 0;
function must(ok, what, detail) { n++; if (!ok) bad++; console.log((ok ? 'ok   ' : 'FAIL ') + what + (detail ? '   [' + detail + ']' : '')); }
const U = T.UNIT, near = (a, b, e) => Math.abs(a - b) < (e || 1e-9);

// 1. reading what is typed
{ const cases = [['2', 2000], [' 20 ', 20000], ['2.5', 2500], ['0.125', 125], ['-0.125', -125], ['+7', 7000], ['7.', 7000], ['359.999', 359999], ['.5', 500], ['-.25', -250], ['\u22122', -2000], ['\u22120.5', -500], ['999999.999', 999999999], ['', null], ['.', null], ['-', null], ['abc', null], ['1.2345', null], ['1e3', null], ['1,5', null], ['--2', null], ['1234567', null]];
  const wrong = cases.filter(([s, v]) => T.parse(s) !== v);
  must(wrong.length === 0, 'what is typed is read as whole thousandths of a degree, and anything else is refused', cases.length + ' cases' + (wrong.length ? '; wrong: ' + JSON.stringify(wrong) : ''));
  must(T.show(2500) === '2.5' && T.show(20000) === '20' && T.show(125) === '0.125' && T.show(-2000) === '−2' && T.show(0) === '0', 'and written back short'); }

// 2. figures worked by hand
{ const w = T.walk(90 * U, 0, 4), c = k => [w.xs[k], w.ys[k]];
  must(near(c(1)[0], 0) && near(c(1)[1], 1) && near(c(2)[0], 1) && near(c(2)[1], 1) && near(c(3)[0], 1) && near(c(3)[1], 0) && near(c(4)[0], 0) && near(c(4)[1], 0) && w.home === 4,
    'ANGLE 90, INC 0: a square, first up the page and then to the right, home at step 4', JSON.stringify([c(1), c(2), c(3), c(4)].map(p => p.map(v => +v.toFixed(6)))));
  const f = T.forecast(90 * U, 0); must(f.home && f.steps === 4 && f.laps === 4 && f.q === 1, '   and the forecast says 4 steps'); }
{ const w = T.walk(0, 0, 50), f = T.forecast(0, 0);
  must(!f.home && f.q === 1 && near(f.gain, 1) && w.home === 0 && near(w.xs[50], 0) && near(w.ys[50], 50), 'ANGLE 0, INC 0: straight up the page for ever, one step a lap'); }
{ const w = T.walk(180 * U, 180 * U, 4), f = T.forecast(180 * U, 180 * U);
  must(near(w.ys[1], 1) && near(w.ys[2], 0) && near(w.ys[3], -1) && near(w.ys[4], 0) && w.there === 2 && w.home === 4 && f.home && f.steps === 4,
    'ANGLE 180, INC 180: out, back, out the other way, back; at its start after 2 steps but facing the wrong way, home after 4', 'there ' + w.there + ', home ' + w.home); }
{ const w = T.walk(60 * U, 0, 6); let ok = w.home === 6;
  // its middle is at (cos 30, 1/2); the start is the corner at 210 degrees from it, and the corners go round clockwise
  for (let k = 0; k <= 6; k++) { const cx = 0.8660254037844386, a = 7 * Math.PI / 6 - k * Math.PI / 3; ok = ok && near(w.xs[k], cx + Math.cos(a), 1e-12) && near(w.ys[k], 0.5 + Math.sin(a), 1e-12); }
  must(ok, 'ANGLE 60, INC 0: a regular hexagon of side 1 to the right of the start, gone round clockwise'); }
{ // ANGLE 0, INC 120: up, up, then turns 120, 240+120.. : the three headings of a lap are 0, 0, 120
  const w = T.walk(0, 120 * U, 9), f = T.forecast(0, 120 * U);
  const B = [w.xs[3], w.ys[3]], want = [Math.sin(2 * Math.PI / 3), 2 + Math.cos(2 * Math.PI / 3)];
  must(near(B[0], want[0]) && near(B[1], want[1]) && near(Math.hypot(B[0], B[1]), Math.sqrt(3)) && !f.home && f.q === 3 && w.home === 0 && near(w.xs[9], 3 * B[0]) && near(w.ys[9], 3 * B[1]),
    'ANGLE 0, INC 120: a lap is up, up, and one step at 120 degrees: the square root of 3 from the start, and three laps are three times that', B.map(v => v.toFixed(6)).join(', ')); }

// 3. the book's example and the sealed sheet's
{ const a = T.forecast(2 * U, 20 * U), b = T.forecast(0, 7 * U), c = T.forecast(10 * U, 20 * U);
  must(a.home && a.q === 18 && a.T === 216 * U && a.laps === 5 && a.steps === 90, 'ANGLE 2, INC 20 (the book\'s): laps of 18, 216 degrees a lap, home after 90 steps in 5 laps');
  must(b.home && b.q === 360 && b.T === 180 * U && b.laps === 2 && b.steps === 720, 'ANGLE 0, INC 7: laps of 360, half a turn a lap, home after 720 steps');
  must(!c.home && c.q === 18 && near(c.gain, Math.sqrt(18)), 'ANGLE 10, INC 20: never home, the square root of 18 every 18 steps');
  must(a.p === 1 && b.p === 7 && T.forecast(0, 340 * U).p === 17 && T.forecast(0, 340 * U).q === 18 && T.forecast(5 * U, 0).p === 0, 'the amount added as a part of a turn in lowest terms: 20 degrees is 1/18, 7 is 7/360, 340 is 17/18, nought is 0/1');
  const m = T.forecast(-2 * U, -20 * U); must(m.home && m.steps === 90 && m.laps === 5 && m.q === 18 && m.p === 17 && m.T === 144 * U, 'turning left instead (ANGLE -2, INC -20): the same 90 steps and 5 laps; the amount is 17/18 of a turn and the lap turns 144 degrees, both brought into one whole turn', 'p ' + m.p + ', T ' + m.T / U);
  const wl = T.walk(-2 * U, -20 * U, 90), wr = T.walk(2 * U, 20 * U, 90); let worst = 0; for (let k = 0; k <= 90; k++) worst = Math.max(worst, Math.abs(wl.xs[k] + wr.xs[k]), Math.abs(wl.ys[k] - wr.ys[k]));
  must(wl.home === 90 && worst < 1e-9 && Math.abs(wr.xs[2]) > 0.01 && wr.xs[2] > 0, '   and the walk is the book\'s figure in a mirror; the book\'s own first bends to the right', 'worst ' + worst.toExponential(1) + '; x after two steps ' + wr.xs[2].toFixed(4)); }

// 4. every whole-degree pair against the table Python made by walking
{ let agree = 0, wrong = 0, away = 0, first = null;
  for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) {
    const f = T.forecast(a * U, inc * U), py = table.whole[inc][a];
    if ((f.home ? f.steps : 0) === py) agree++; else { wrong++; if (!first) first = [inc, a, f, py]; } if (!f.home) away++; }
  must(wrong === 0 && agree === 129240, 'the forecast for every whole-degree pair (INC 1 to 359, ANGLE 0 to 359) is what Python found by walking: the step it comes home, or never in 720', agree + ' agree, ' + wrong + ' do not' + (first ? '; first: ' + JSON.stringify(first) : ''));
  must(away === 14090, 'of those, 14,090 never come home', String(away)); }
{ let agree = 0, wrong = 0, worst = 0, cases = 0; const t0 = Date.now();
  for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) {
    const w = T.walk(a * U, inc * U, 720), py = table.whole[inc][a];
    if (w.home === py) agree++; else wrong++;
    if (py === 0) { const q = 360 / T.gcd(inc, 360); worst = Math.max(worst, Math.abs(Math.hypot(w.xs[q], w.ys[q]) - Math.sqrt(q)), Math.abs(Math.hypot(w.xs[720], w.ys[720]) - 720 / q * Math.sqrt(q))); cases++; } }
  must(wrong === 0 && agree === 129240, 'the walk in this file comes home at the same step as Python\'s walk, for every whole-degree pair', agree + ' agree, ' + wrong + ' do not; ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');
  must(cases === 14090 && worst < 1e-9, 'each pair that never comes home is the square root of q from its start after one lap, and 720/q times that after 720 steps', cases + ' pairs, worst difference ' + worst.toExponential(2)); }
{ let stood = 0, n = 0, nearest = 9; const all = [];      // extras.py: none of them ever stands on its starting point again; the nearest is 0.014 of a step off
  for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) { if (table.whole[inc][a] !== 0) continue; n++; const q = 360 / T.gcd(inc, 360), w = T.walk(a * U, inc * U, q * (Math.floor(Math.sqrt(q)) + 2));
    if (w.there) stood++; let best = 9, bk = 0; for (let k = 1; k < w.xs.length; k++) { const d = Math.hypot(w.xs[k], w.ys[k]); if (d < best) { best = d; bk = k; } } all.push([best, inc, a, bk]); if (best < nearest) nearest = best; }
  const ties = all.filter(r => r[0] < nearest + 1e-9).map(r => 'INC ' + r[1] + ' ANGLE ' + r[2] + ' step ' + r[3]);
  must(n === 14090 && stood === 0 && Math.abs(nearest - 0.014031) < 1e-6 && ties.includes('INC 2 ANGLE 155 step 15'), 'none of the pairs that never come home stands on its starting point again; the nearest comes within 0.014 of a step, and INC 2, ANGLE 155 at step 15 (Python\'s) is one that does', stood + ' stood on it; nearest ' + nearest.toFixed(6) + ', reached by ' + ties.join('; ')); }
{ let odd = 0, n = 0;      // "home" has three clauses; does the third ever decide?  Standing on the start, facing as it began, with a different turn next:
  for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) { n++; const a0 = a * U, I = inc * U, K = 2 * Math.PI / T.FULL; let ang = a0, head = 0, x = 0, y = 0;
    for (let k = 1; k <= 720; k++) { x += Math.sin(head * K); y += Math.cos(head * K); head = (head + ang) % T.FULL; ang = (ang + I) % T.FULL; if (x * x + y * y < 1e-14 && head === 0 && ang !== a0) { odd++; break; } } }
  must(n === 129240 && odd === 0, 'no whole-degree turtle ever stands on its start, facing as it began, with a turn other than its first to come (so among these the third clause of "home" never decides, and a broken copy without it cannot be told from the true one)', odd + ' of ' + n); }
{ const c = T.census(); let same = true; for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) if (c.steps[inc * 360 + a] !== table.whole[inc][a]) same = false;
  let least = 1e9; for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) if (table.whole[inc][a] && table.whole[inc][a] < least) least = table.whole[inc][a];
  must(same && c.away === 14090 && c.home === 115150 && c.longest === 720 && c.least === 4 && least === 4, 'the census the map is drawn from: 14,090 never, 115,150 home, none taking more than 720 steps or fewer than 4 (Python\'s least too)', c.away + ', ' + c.home + ', ' + c.longest + ', ' + c.least); }
{ let worst = 0, n = 0;      // the walk's places against places Python walked
  for (const c of table.corners) { const w = T.walk(c.A, c.I, c.n); for (const [k, x, y] of c.at) { worst = Math.max(worst, Math.abs(w.xs[k] - x), Math.abs(w.ys[k] - y)); n++; } }
  must(table.corners.length === 12 && n > 80 && worst < 1e-9, 'where the walk stands after chosen steps is where Python\'s walk stands, for twelve turtles', n + ' places, worst difference ' + worst.toExponential(1)); }

// 5. pairs with decimals, against exact fractions and Python's walk
{ let agree = 0, wrong = 0, walked = 0, wwrong = 0, far = 0, farwrong = 0, first = null;
  for (const r of table.decimal) {
    const f = T.forecast(r.A, r.I);
    if (f.q === r.q && (f.home ? f.steps : null) === r.steps) agree++; else { wrong++; if (!first) first = [r, f]; }
    if (r.steps !== null && 'home' in r) { walked++; const w = T.walk(r.A, r.I, r.steps + 50); if (w.home !== r.home || w.home !== r.steps) wwrong++; }
    if (r.steps === null && 'after3' in r) { far++; const w = T.walk(r.A, r.I, 3 * r.q); if (w.home !== 0 || !near(Math.hypot(w.xs[3 * r.q], w.ys[3 * r.q]), 3 * Math.sqrt(r.q), 1e-8) || !near(r.after3, 3 * Math.sqrt(r.q), 1e-8)) farwrong++; } }
  must(wrong === 0 && agree === table.decimal.length && agree >= 400, 'with decimals: the length of a lap and the forecast are what exact fractions give in Python', agree + ' pairs agree, ' + wrong + ' do not' + (first ? '; first: ' + JSON.stringify(first) : ''));
  must(wwrong === 0 && walked > 150, '   those that come home within 30,000 steps: this file\'s walk comes home at the forecast step, and so does Python\'s', walked + ' walked, ' + wwrong + ' wrong');
  must(farwrong === 0 && far > 20, '   those that never do: three laps on they are three times the square root of q away, in both', far + ' walked, ' + farwrong + ' wrong'); }

// 6. a closed figure looks the same turned by the lap's turning about its middle
{ let ok = 0, tried = 0;
  for (const [a, i] of [[2, 20], [0, 7], [1, 90], [30, 40], [3, 11], [1, 120], [89, 180], [5, 72], [112, 135], [30, 180], [2.5, 20], [0, 0.5]]) {
    const A = Math.round(a * U), I = Math.round(i * U), f = T.forecast(A, I); if (!f.home) continue; tried++;
    const w = T.walk(A, I, f.steps); let cx = 0, cy = 0; for (let k = 0; k < f.steps; k++) { cx += w.xs[k]; cy += w.ys[k]; } cx /= f.steps; cy /= f.steps;
    const th = -2 * Math.PI * f.T / T.FULL, c = Math.cos(th), s = Math.sin(th); let worst = 0;
    const key = (x, y) => Math.round(x * 1e5) + ',' + Math.round(y * 1e5), set = new Set(); for (let k = 0; k < f.steps; k++) set.add(key(w.xs[k], w.ys[k]));
    for (let k = 0; k < f.steps; k++) { const x = cx + (w.xs[k] - cx) * c - (w.ys[k] - cy) * s, y = cy + (w.xs[k] - cx) * s + (w.ys[k] - cy) * c;
      let hit = false; for (const dx of [-1, 0, 1]) for (const dy of [-1, 0, 1]) if (set.has((Math.round(x * 1e5) + dx) + ',' + (Math.round(y * 1e5) + dy))) hit = true; if (!hit) worst++; }
    if (w.home === f.steps && worst === 0) ok++; }
  must(ok === tried && tried === 12, 'a figure that closes is carried into itself by turning it through one lap\'s turning about the middle of its corners', ok + ' of ' + tried); }
{ // the control: turning by something else does not
  const f = T.forecast(2 * U, 20 * U), w = T.walk(2 * U, 20 * U, 90); let cx = 0, cy = 0; for (let k = 0; k < 90; k++) { cx += w.xs[k]; cy += w.ys[k]; } cx /= 90; cy /= 90;
  const th = -2 * Math.PI / 7, c = Math.cos(th), s = Math.sin(th); let miss = 0;
  for (let k = 0; k < 90; k++) { const x = cx + (w.xs[k] - cx) * c - (w.ys[k] - cy) * s, y = cy + (w.xs[k] - cx) * s + (w.ys[k] - cy) * c; let best = 1e9; for (let j = 0; j < 90; j++) best = Math.min(best, Math.hypot(x - w.xs[j], y - w.ys[j])); if (best > 1e-4) miss++; }
  must(miss > 60, '   control: turned a seventh of the way round instead, the book\'s fivefold figure does not fit itself', miss + ' of 90 corners miss'); }

// 7. the frame and the words
{ const w = T.walk(90 * U, 0, 4), b = T.box(w); must(near(b[0], 0) && near(b[1], 1) && near(b[2], 0) && near(b[3], 1), 'the box round the square is 0 to 1 each way');
  const w2 = T.walk(0, 0, 10), b2 = T.box(w2, 4); must(near(b2[3], 4) && near(b2[2], 0) && near(T.box(w2)[3], 10), 'and round the first 4 steps of a straight walk it is 4 high, from the start up'); }
must(T.commas(129240) === '129,240' && T.commas(720) === '720' && T.commas(1440000) === '1,440,000', 'thousands are set off with commas');

console.log('CORE TEST: ' + n + ' assertions, ' + bad + ' failed');
process.exit(bad ? 1 : 0);

// Tests of core.js that could fail: cases worked by hand, and a table made in Python by walking and adding up (table.py).
// usage: node test-core.js table.json
const T = require('./core.js'); const fs = require('fs'); const path = require('path');
const table = JSON.parse(fs.readFileSync(path.resolve(process.argv[2]), 'utf8'));
let n = 0, bad = 0;
function must(ok, what, detail) { n++; if (!ok) bad++; console.log((ok ? 'ok   ' : 'FAIL ') + what + (detail ? '   [' + detail + ']' : '')); }
const near = (a, b, e) => Math.abs(a - b) < (e || 1e-9);

// 1. reading what is typed
{ const cases = [['9', 9], [' 45 ', 45], ['-1', -1], ['−1', -1], ['+7', 7], ['0', 0], ['1234567', 1234567], ['', null], ['abc', null], ['1.5', null], ['1e3', null], ['12345678', null], ['--2', null], ['1/9', null]];
  const wrong = cases.filter(([s, v]) => T.parse(s) !== v);
  must(wrong.length === 0, 'what is typed is read as a whole number of at most seven figures, and anything else is refused', cases.length + ' cases' + (wrong.length ? '; wrong: ' + JSON.stringify(wrong) : '')); }

// 2. arithmetic worked by hand
must(JSON.stringify(T.factor(45)) === '[[3,2],[5,1]]' && JSON.stringify(T.factor(9009)) === '[[3,2],[7,1],[11,1],[13,1]]' && JSON.stringify(T.factor(1)) === '[]' && JSON.stringify(T.factor(1194649)) === '[[1093,2]]' && JSON.stringify(T.factor(64)) === '[[2,6]]',
  'factors: 45 = 3² × 5, 9009 = 3² × 7 × 11 × 13, 1194649 = 1093²');
must(T.order2(7) === 3 && T.order2(9) === 6 && T.order2(5) === 4 && T.order2(45) === 12 && T.order2(19) === 18 && T.order2(101) === 100 && T.order2(1) === 1 && T.order2(1093) === 364 && T.order2(1194649) === 364,
  'orders of 2: 3 modulo 7, 6 modulo 9, 4 modulo 5, 12 modulo 45, 18 modulo 19, 100 modulo 101, and 364 modulo 1093 and modulo 1093² alike');
must(T.val(18, 3) === 2 && T.val(12, 3) === 1 && T.val(4, 3) === 0 && T.val(100, 5) === 2, 'how often a prime divides a number');

// 3. forecasts worked by hand
{ const a = T.forecast(1, 9), b = T.forecast(1, 45), c = T.forecast(1, 63), d = T.forecast(1, 171), e = T.forecast(1, 7);
  must(a.bounded && a.home && a.round === 6 && a.tail === 0 && a.m === 9 && a.serves.l === 3 && a.serves.e === 2, '1/9 (the book\'s 40 degrees): home after a round of 6 steps; 9 = 3² serves');
  must(b.bounded && b.home && b.round === 12 && b.serves.l === 3 && b.serves.e === 2 && b.spoilt.length === 0 && b.factors.some(f => f[0] === 5 && f[1] === 1), '1/45 (8 degrees): home after 12 steps, though 5 divides 45 only once: the book\'s printed claim says it should not close');
  must(!c.bounded && !c.home && c.round === 6 && c.squares === 1 && c.spoilt.length === 1 && c.spoilt[0].l === 3 && c.spoilt[0].r === 7 && c.spoilt[0].ord === 3, '1/63: not bounded, though 63 holds 9: spoilt by 7, modulo which 2 has order 3');
  must(!d.bounded && d.spoilt[0].r === 19 && d.spoilt[0].ord === 18 && d.round === 18, '1/171 (HAKMEM\'s exception): spoilt by 19, modulo which 2 has order 18');
  must(!e.bounded && e.squares === 0 && e.round === 3 && e.spoilt.length === 0, '1/7: no square of a prime, not bounded, rounds of 3'); }
{ const w = T.forecast(1, 1194649), x = T.forecast(1, 12), y = T.forecast(1, 36), z = T.forecast(3, 8), u = T.forecast(10, 90), v = T.forecast(-1, 9), t = T.forecast(1, 441), h = T.forecast(1, 9009), k = T.forecast(1, 2525);
  must(!w.bounded && w.squares === 1 && w.spoilt[0].self === true && w.round === 364, '1/1093²: not bounded: 2 has the same order modulo 1093² as modulo 1093');
  must(!x.bounded && x.tail === 2 && x.m === 3 && x.round === 2 && !x.straight, '1/12: a tail of 2 steps, then rounds of 2 that do not close');
  must(y.bounded && !y.home && y.tail === 2 && y.m === 9 && y.round === 6, '1/36: a tail of 2 steps, then a loop of 6 for ever: bounded, and never home');
  must(!z.bounded && z.straight && z.tail === 3 && z.m === 1, '3/8: after 3 steps the turn is a whole number of turns: straight on');
  must(u.p === 1 && u.q === 9 && u.bounded && v.p === 8 && v.q === 9 && v.bounded, '10/90 is 1/9, and −1/9 is 8/9');
  must(t.bounded && t.serves.l === 7 && t.spoilt.length === 1 && t.spoilt[0].l === 3 && t.spoilt[0].r === 7, '1/441 = 1/(9 × 49): 9 is spoilt by 7, and 49 serves');
  must(!h.bounded && !k.bounded && h.spoilt[0].l === 3 && k.spoilt[0].l === 5 && k.spoilt[0].r === 101, 'HAKMEM\'s 9009 and 2525: not bounded'); }

// 4. every odd denominator from 3 to 3001 against Python's sums
{ let agree = 0, wrong = 0, rounds = 0, closes = 0, first = null; const ms = Object.keys(table.odd).map(Number);
  for (const m of ms) { const f = T.forecast(1, m), py = table.odd[m]; if (f.bounded === py[0]) agree++; else { wrong++; if (!first) first = m; } if (f.round === py[1]) rounds++; if (f.bounded) closes++; }
  must(ms.length === 1500 && wrong === 0 && rounds === 1500, 'the forecast for 1/m, every odd m from 3 to 3001, is what Python found by adding up a round: bounded or not, and the round\'s length', agree + ' agree, ' + wrong + ' do not' + (first ? '; first ' + first : ''));
  must(closes === 224, 'of those, 224 are bounded', String(closes)); }
{ let agree = 0, worst = 0, homes = 0, wrongHome = 0; const t0 = Date.now(), ms = Object.keys(table.odd).map(Number);
  for (const m of ms) { const py = table.odd[m], w = T.walk(1, m, 2 * py[1]), gain = Math.hypot(w.xs[2 * py[1]] - w.xs[py[1]], w.ys[2 * py[1]] - w.ys[py[1]]);
    worst = Math.max(worst, Math.abs(gain - py[2])); if ((gain < 1e-9) === py[0]) agree++; if (w.home) homes++; if ((w.home === py[1]) !== py[0]) wrongHome++; }
  must(agree === 1500 && worst < 1e-8 && homes === 224 && wrongHome === 0, 'the walk in this file: one round carries the turtle as far as Python\'s sum says, for every odd m to 3001; it is home after one round exactly for the 224', 'worst difference ' + worst.toExponential(1) + '; ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s'); }

// 5. made-up fractions, odd and even denominators
{ let agree = 0, wrong = 0, walked = 0, wwrong = 0, first = null;
  for (const r of table.fracs) { const f = T.forecast(r.P, r.Q);
    if (f.p === r.p && f.q === r.q && f.tail === r.tail && f.round === r.round && f.bounded === r.bounded && f.home === (r.home > 0)) agree++; else { wrong++; if (!first) first = [r.P, r.Q]; }
    const tot = r.tail + 3 * r.round, w = T.walk(r.P, r.Q, tot), gain = Math.hypot(w.xs[r.tail + r.round] - w.xs[r.tail], w.ys[r.tail + r.round] - w.ys[r.tail]); walked++;
    if (w.home !== r.home || Math.abs(gain - r.gain) > 1e-8) wwrong++; }
  must(wrong === 0 && agree === table.fracs.length && agree >= 300, 'fractions p/q with odd and even q: lowest terms, tail, round, bounded and home are what Python found', agree + ' agree, ' + wrong + ' do not' + (first ? '; first ' + first : ''));
  must(wwrong === 0 && walked >= 300, '   and this file\'s walk is home at Python\'s step (or never), and a round carries it as far as Python\'s', walked + ' walked, ' + wwrong + ' wrong'); }

// 6. where the walk stands
{ let worst = 0, k = 0; for (const c of table.corners) { const w = T.walk(c.P, c.Q, c.n); for (const [i, x, y] of c.at) { worst = Math.max(worst, Math.abs(w.xs[i] - x), Math.abs(w.ys[i] - y)); k++; } }
  must(table.corners.length === 17 && k > 90 && worst < 1e-9, 'where the walk stands after chosen steps is where Python\'s walk stands, for seventeen turtles', k + ' places, worst ' + worst.toExponential(1)); }
{ const w = T.walk(1, 4, 4);
  must(near(w.xs[1], -1) && near(w.ys[1], 0) && near(w.xs[2], 0) && near(w.ys[2], 0) && near(w.xs[3], 1) && near(w.xs[4], 2) && near(w.ys[4], 0), '1/4: it turns left a quarter and steps (to the left), turns a half and steps back, and then walks straight on to the right',
    [1, 2, 3, 4].map(k => w.xs[k].toFixed(3) + ',' + w.ys[k].toFixed(3)).join(' ')); }
{ const w = T.walk(1, 3, 4);
  must(near(w.xs[1], -Math.sqrt(3) / 2) && near(w.ys[1], -0.5) && near(w.xs[2], -Math.sqrt(3) / 2) && near(w.ys[2], 0.5) && near(Math.hypot(w.xs[4] - w.xs[2], w.ys[4] - w.ys[2]), 1), '1/3: a third of a turn to the left, then two thirds more, which is straight up: each round of 2 carries it 1 step'); }
{ const b = T.box(T.walk(1, 4, 4)), c = T.box(T.walk(1, 3, 2)); must(near(b[0], -1) && near(b[1], 2) && near(b[2], 0) && near(b[3], 0) && near(c[1], 0) && near(c[0], -Math.sqrt(3) / 2), 'the box round the first four corners of 1/4 runs from −1 to 2, and the box of 1/3 holds the start');
  const w = T.walk(1, 4, 4); must(w.there === 2 && w.home === 0, '1/4 stands on its start again at step 2, facing another way, and is not home', 'there ' + w.there + ', home ' + w.home); }

// 7. the census the map is drawn from
{ const c = T.census(2001); let closes = 0, spoilt = 0, plain = 0, same = true;
  for (let m = 3, i = 0; m <= 2001; m += 2, i++) { const py = table.odd[m][0], sq = T.factor(m).some(f => f[1] >= 2); if (py) closes++; else if (sq) spoilt++; else plain++; if (c.kind[i] !== (py ? 2 : sq ? 1 : 0)) same = false; }
  must(same && c.closes === closes && c.spoilt === spoilt && c.plain === plain && closes + spoilt + plain === 1000, 'the census of odd denominators from 3 to 2001: bounded, holding a square and not bounded, holding none: as Python\'s sums have them', closes + ', ' + spoilt + ', ' + plain); }
must(T.commas(1194649) === '1,194,649' && T.commas(45) === '45', 'thousands are set off with commas');

console.log('CORE TEST: ' + n + ' assertions, ' + bad + ' failed');
process.exit(bad ? 1 : 0);

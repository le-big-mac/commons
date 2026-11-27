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

// 8. the clock: the hours of a round, the polygons they fall into, and their balance point
{ const a = T.clock(1, 9), b = T.clock(1, 45), c = T.clock(1, 63), d = T.clock(1, 36), e = T.clock(1, 441), g = T.clock(1, 225), h = T.clock(1, 7), i = T.clock(3, 8);
  const sorted = x => Array.from(x.hours).sort((u, v) => u - v).join(' ');
  must(sorted(a) === '1 2 4 5 7 8' && String(a.kinds) === '3' && a.off < 1e-12 && Array.from(a.hours).join(' ') === '1 2 4 8 7 5', '1/9: the hours 1, 2, 4, 8, 7, 5 are two triangles (1, 4, 7 and 2, 5, 8) and balance');
  must(sorted(b) === '1 2 4 8 16 17 19 23 31 32 34 38' && String(b.kinds) === '3' && b.off < 1e-12 && [1, 2, 4, 8].every(x => T.polygon(x, 45, 3).every(y => b.hours.indexOf(y) >= 0)) && String(T.polygon(1, 45, 3)) === '1,16,31', '1/45: twelve hours in four triangles (1, 16, 31 and three more)');
  must(sorted(c) === '1 2 4 8 16 32' && c.kinds.length === 0 && Math.abs(6 * c.off - 3.4846) < 1e-4 && Math.abs(c.off - 0.5808) < 1e-4 && c.hours.indexOf(22) < 0 && c.hours.indexOf(43) < 0, '1/63: six hours, no triangle among them (of 1, 22, 43 only the 1), and their balance point is 0.581 of a radius off the centre: six steps carry 3.485');
  must(sorted(d) === '4 8 16 20 28 32' && String(d.kinds) === '3' && d.tail === 2 && d.off < 1e-12, '1/36: after the tail of 2 the hours are 4, 8, 16, 32, 28, 20 on a clock of 36: two triangles');
  must(String(e.kinds) === '7' && e.n === 42 && String(g.kinds) === '3,5' && h.kinds.length === 0 && sorted(h) === '1 2 4' && i.n === 1 && sorted(i) === '0' && Math.abs(i.off - 1) < 1e-12, '1/441: heptagons and no triangles; 1/225: triangles and pentagons both; 1/7: none; 3/8 after its tail: the one hour 0'); }
{ let agree = 0, kindsOK = 0, worst = 0, n = 0, worstC = 0;
  for (const m of Object.keys(table.odd).map(Number)) { const py = table.odd[m], c = T.clock(1, m); n++;
    if ((c.kinds.length > 0) === py[0]) agree++; if (String(c.kinds) === String(py[3])) kindsOK++;
    worst = Math.max(worst, Math.abs(c.n * c.off - py[2])); worstC = Math.max(worstC, Math.abs(c.cx - py[4]), Math.abs(c.cy - py[5])); }
  must(n === 1500 && agree === 1500 && kindsOK === 1500, 'the clock for 1/m, every odd m from 3 to 3001: the hours fall into polygons exactly when Python\'s sum of the round is nought, and into the same kinds of polygon as Python finds', agree + ' agree; ' + kindsOK + ' with the same kinds');
  must(worst < 1e-8 && worstC < 1e-10, '   and the balance point is where Python puts it; the number of hours times its distance from the centre is how far Python\'s round carries the turtle', 'worst difference ' + worst.toExponential(1) + ' steps, ' + worstC.toExponential(1) + ' radii'); }
{ let agree = 0, worst = 0, hoursOK = 0, withHours = 0;
  for (const r of table.fracs) { const c = T.clock(r.P, r.Q);
    if (String(c.kinds) === String(r.kinds) && (c.kinds.length > 0) === r.bounded && c.n === r.round && c.tail === r.tail) agree++;
    worst = Math.max(worst, Math.abs(c.n * c.off - r.gain));
    if (r.hours) { withHours++; if (Array.from(c.hours).sort((u, v) => u - v).join(',') === r.hours.join(',')) hoursOK++; } }
  must(agree === table.fracs.length && worst < 1e-7 && hoursOK === withHours && withHours > 150, 'the clock for the made-up fractions, odd and even q: kinds of polygon, hours (where a round has at most 60) and the distance a round carries, as Python has them', agree + ' of ' + table.fracs.length + '; ' + hoursOK + ' of ' + withHours + ' lists of hours; worst ' + worst.toExponential(1)); }

// 9. the rule in the Lehmers' form: with one l taken out, is the round l times as long?
{ const a = T.takeOut(1, 9), b = T.takeOut(1, 45), c = T.takeOut(1, 63), d = T.takeOut(1, 441), e = T.takeOut(1, 7), g = T.takeOut(5, 36), h = T.takeOut(1, 1194649), i = T.takeOut(1, 189);
  must(JSON.stringify(a) === '[{"l":3,"e":2,"n1":2,"long":true}]' && JSON.stringify(b) === '[{"l":3,"e":2,"n1":4,"long":true}]' && JSON.stringify(c) === '[{"l":3,"e":2,"n1":6,"long":false}]',
    '1/9: with one 3 out the round of 1/3 has 2 steps, and 6 is three times 2; 1/45: 1/15 has 4, and 12 is three times 4; 1/63: 1/21 has 6, and 6 is no more');
  must(JSON.stringify(d) === '[{"l":3,"e":2,"n1":42,"long":false},{"l":7,"e":2,"n1":6,"long":true}]' && e.length === 0 && JSON.stringify(g) === JSON.stringify(a) && JSON.stringify(h) === '[{"l":1093,"e":2,"n1":364,"long":false}]' && JSON.stringify(i) === '[{"l":3,"e":3,"n1":6,"long":true}]',
    '1/441: the 3 gives nothing (42 and 42) and the 7 does (6 and 42); 1/7: no repeated prime; 5/36 as 1/9; 1/1093²: 364 and 364; 1/189: 6 and 18'); }
{ let agree = 0, same = 0, either = 0, n2 = 0;
  for (const m of Object.keys(table.odd).map(Number)) { const py = table.odd[m], t = T.takeOut(1, m); n2++;
    if (t.some(x => x.long) === py[0]) agree++; if (JSON.stringify(t.map(x => [x.l, x.e, x.n1])) === JSON.stringify(py[6])) same++;
    if (t.every(x => py[1] === x.n1 || py[1] === x.l * x.n1)) either++; }
  let fr = 0; for (const r of table.fracs) { const t = T.takeOut(r.P, r.Q); if (t.some(x => x.long) === r.bounded && JSON.stringify(t.map(x => [x.l, x.e, x.n1])) === JSON.stringify(r.out)) fr++; }
  must(n2 === 1500 && agree === 1500 && same === 1500 && either === 1500 && fr === table.fracs.length, 'the rule in that form, for every odd m from 3 to 3001 and for the made-up fractions: some repeated prime makes the round l times as long exactly when Python\'s sum of the round is nought; the lengths with one l out are those Python finds by doubling; and a round is always either l times as long or no longer', agree + ', ' + same + ', ' + either + ' of 1500; ' + fr + ' of ' + table.fracs.length); }
{ // the clock against the walk and the rule, a little wider than Python's table goes (a run to 100,001 is in clock/wide.js)
  let bad2 = 0, n3 = 0; for (let m = 3; m <= 12001; m += 2) { const f = T.forecast(1, m), c = T.clock(1, m), t = T.takeOut(1, m); n3++; if ((c.kinds.length > 0) !== f.bounded || t.some(x => x.long) !== f.bounded || String(c.kinds) !== String(t.filter(x => x.long).map(x => x.l))) bad2++; }
  must(n3 === 6000 && bad2 === 0, 'for every odd m from 3 to 12,001 the three ways of telling agree: the forecast\'s rule, the hours falling into polygons, and the round being l times as long with one l out; and the polygons are of exactly the primes for which it is', n3 + ' denominators, ' + bad2 + ' disagreements'); }

console.log('CORE TEST: ' + n + ' assertions, ' + bad + ' failed');
process.exit(bad ? 1 : 0);

/* ctest.js: tests of pcore.js and of the C search, on cases worked by hand or by a second method.
   Run: node ctest.js   (needs ./search built from search.c) */
'use strict';
var P = require('./pcore.js');
var cp = require('child_process');
var path = require('path');
var pass = 0, fail = 0;
function ok(name, cond, detail) {
  if (cond) { pass++; console.log('pass  ' + name); }
  else { fail++; console.log('FAIL  ' + name + (detail ? '   ' + detail : '')); }
}
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function rng(seed) { var s = seed >>> 0; return function () { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
function randomCoins(r, n, top, withOne) {
  var set = Object.create(null), out = [];
  if (withOne) { set[1] = 1; out.push(1); }
  while (out.length < n) { var c = 1 + Math.floor(r() * top); if (!set[c]) { set[c] = 1; out.push(c); } }
  return out;
}
var US = [1, 5, 10, 25], EURO = [1, 2, 5, 10, 20, 50, 100, 200], LSD = [1, 3, 6, 12, 24, 30];

/* ---- plain, by hand ---- */
var m = P.plain(US, 100);
ok('plain US: 0 takes 0, 30 takes 2, 99 takes 9', m[0] === 0 && m[30] === 2 && m[99] === 9, [m[0], m[30], m[99]].join());
ok('plain (1,7,10): 14 takes 2 (Shallit)', P.plain([1, 7, 10], 15)[14] === 2);
ok('plain (1,12,19): 24 takes 2 (Shallit)', P.plain([1, 12, 19], 25)[24] === 2);
ok('plain without a 1: (2,5) cannot make 1 or 3, makes 6 with 3', (function () {
  var t = P.plain([2, 5], 8); return t[1] >= P.INF && t[3] >= P.INF && t[6] === 3 && t[7] === 2; })());
ok('plain takes coins in any order and twice over', eq(Array.from(P.plain([25, 1, 10, 5, 5], 60)), Array.from(P.plain(US, 60))));

/* ---- greedy, by hand ---- */
ok('greedy (1,7,10): 14 takes 5 (Shallit)', P.greedy([1, 7, 10], 15)[14] === 5);
ok('greedy (1,12,19): 24 takes 6 (Shallit)', P.greedy([1, 12, 19], 25)[24] === 6);
ok('greedy old pence: 48 takes 3, plain 2', P.greedy(LSD, 49)[48] === 3 && P.plain(LSD, 49)[48] === 2);
ok('greedy without a 1 gets stuck: (2,5) at 6', P.greedy([2, 5], 8)[6] >= P.INF && P.greedy([2, 5], 8)[7] === 2);
ok('greedyWay US 68 = 25,25,10,5,1,1,1', eq(P.greedyWay(US, 68), [[25, 2], [10, 1], [5, 1], [1, 3]]));
ok('greedyWay stuck gives null', P.greedyWay([2, 5], 6) === null);

/* ---- both ways, by hand ---- */
var b = P.both(EURO, 100);
ok('both euro: 99 takes 2, 49 takes 2, 38 takes 3, 8 takes 2, 0 takes 0', b[99] === 2 && b[49] === 2 && b[38] === 3 && b[8] === 2 && b[0] === 0,
  [b[99], b[49], b[38], b[8], b[0]].join());
ok('both (1,3,9,27): 5 takes 3, 2 takes 2, 13 takes 3', (function () { var t = P.both([1, 3, 9, 27], 14); return t[5] === 3 && t[2] === 2 && t[13] === 3; })());
ok('both without a 1: (2,3) makes 1 with 2', P.both([2, 3], 3)[1] === 2);
ok('both far outside the window: (99,100) makes 50 with 99 (50 x 99 back, 49 x 100 ... )', P.both([99, 100], 51)[50] === 99, String(P.both([99, 100], 51)[50]));
ok('both (2,4) cannot make 1', P.both([2, 4], 4)[1] >= P.INF && P.both([2, 4], 4)[2] === 1);
ok('both never more than plain (500 random coinages)', (function () {
  var r = rng(7), i, a;
  for (i = 0; i < 500; i++) {
    var c = randomCoins(r, 2 + Math.floor(r() * 5), 60, true), p = P.plain(c, 120), q = P.both(c, 120);
    for (a = 0; a < 120; a++) if (q[a] > p[a]) return false;
  }
  return true; })());

/* both ways by a second method: the least over what is handed over, p, of plain(p) + plain(p - amount) */
ok('both = least of plain(p) + plain(p - a) (300 random coinages with a 1)', (function () {
  var r = rng(11), i, a, p, bad = 0;
  for (i = 0; i < 300; i++) {
    var c = randomCoins(r, 2 + Math.floor(r() * 4), 40, true), Lx = 60, cmax = Math.max.apply(null, c);
    var top = Lx * cmax + Lx, pl = P.plain(c, top + 1), q = P.both(c, Lx);
    for (a = 0; a < Lx; a++) {
      var best = P.INF;
      for (p = a; p <= top; p++) { var v = pl[p] + pl[p - a]; if (v < best) best = v; }
      if (best !== q[a]) bad++;
    }
  }
  return bad === 0; })());

/* ---- totals, worst ---- */
ok('total and worst of US below 100: 470 and 9', P.total(P.plain(US, 100)) === 470 && P.worst(P.plain(US, 100)) === 9);
ok('total is Infinity when an amount cannot be made', P.total(P.plain([2, 5], 10)) === Infinity && P.worst(P.plain([2, 5], 10)) === Infinity);

/* ---- greedy failures ---- */
ok('greedyFails (1,7,10) below 30: 14,15,16,24,25,26', (function () {
  /* by hand: 14=7+7 (greedy 10+1x4); 15, 16 the same with one or two 1s; 24=10+7+7 (greedy 10+10+1x4); 25, 26 likewise.
     Not failures: 21 = 10+10+1 ties with 7+7+7; 28 = 10+10+7+1 ties with 7x4. (My first list had these wrong.) */
  return eq(P.greedyFails([1, 7, 10], 30), [14, 15, 16, 24, 25, 26]); })(), JSON.stringify(P.greedyFails([1, 7, 10], 30)));
ok('greedyFails US: none below 1000', P.greedyFails(US, 1000).length === 0);

/* ---- Pearson's test ---- */
ok('pearson (1,7,10) = 14', P.pearson([1, 7, 10]) === 14, String(P.pearson([1, 7, 10])));
ok('pearson (1,3,4) = 6', P.pearson([1, 3, 4]) === 6);
ok('pearson US = 0, euro = 0', P.pearson(US) === 0 && P.pearson(EURO) === 0);
ok('pearson (1,12,19) = 24', P.pearson([1, 12, 19]) === 24, String(P.pearson([1, 12, 19])));
ok('pearson (1,5,18,25) = 28', P.pearson([1, 5, 18, 25]) === 28, String(P.pearson([1, 5, 18, 25])));
ok('pearson agrees with trying every amount (3000 random coinages)', (function () {
  var r = rng(3), i, bad = 0, some = 0;
  for (i = 0; i < 3000; i++) {
    var c = randomCoins(r, 3 + Math.floor(r() * 5), 30 + Math.floor(r() * 200), true);
    var a = P.pearson(c), f = P.firstFailure(c);
    if (a !== f) bad++;
    if (a > 0) some++;
  }
  console.log('      (' + some + ' of 3000 had a failure)');
  return bad === 0 && some > 500 && some < 2990; })());
ok('firstFailure is not fooled by its bound: no failure at or above the two largest coins summed (400 coinages, tried to 3 times as far)', (function () {
  var r = rng(5), i;
  for (i = 0; i < 400; i++) {
    var c = randomCoins(r, 3 + Math.floor(r() * 4), 80, true).sort(function (x, y) { return x - y; });
    var far = P.greedyFails(c, 3 * (c[c.length - 1] + c[c.length - 2]));
    var f = P.firstFailure(c);
    if ((far.length ? far[0] : 0) !== f) return false;
  }
  return true; })());
ok('pearson without a 1 refuses', (function () { try { P.pearson([2, 5]); return false; } catch (e) { return /needs a coin of 1/.test(e.message); } })());

/* ---- bestAdd ---- */
ok('bestAdd lists every candidate once, best first', (function () {
  var l = P.bestAdd([1, 4], 20, 'plain', 19), i;
  if (l.length !== 17) return false;
  for (i = 1; i < l.length; i++) if (l[i].total < l[i - 1].total) return false;
  return l.every(function (e) { return e.coin !== 1 && e.coin !== 4; }); })());
ok('bestAdd by hand: to (1) below 5, plain, the best is 2 (0,1,1,2,2 = 6), then 3 (0,1,2,1,2 = 6): tie, 2 first; 4 gives 0,1,2,3,1 = 7', (function () {
  var l = P.bestAdd([1], 5, 'plain', 4);
  return l[0].coin === 2 && l[0].total === 6 && l[1].coin === 3 && l[1].total === 6 && l[2].coin === 4 && l[2].total === 7; })());

/* ---- plainWay ---- */
ok('plainWay old pence 48 = two florins', eq(P.plainWay(LSD, 48), [[24, 2]]));
ok('plainWay sums to the amount with the right count (200 random)', (function () {
  var r = rng(21), i;
  for (i = 0; i < 200; i++) {
    var c = randomCoins(r, 2 + Math.floor(r() * 5), 50, true), a = Math.floor(r() * 200), w = P.plainWay(c, a);
    var s = 0, n = 0; w.forEach(function (e) { s += e[0] * e[1]; n += e[1]; });
    if (s !== a || n !== P.plain(c, a + 1)[a]) return false;
  }
  return true; })());
ok('plainWay of what cannot be made is null', P.plainWay([2, 4], 5) === null);

/* ---- schemes ---- */
ok('schemes (1,2,5) for 4: 2 tokens, two ways: 5-1 and 2+2', (function () {
  var s = P.schemes([1, 2, 5], 4);
  return s.count === 2 && s.total === 2 && eq(s.ways, [[[5, 1], [1, -1]], [[2, 2]]]); })(), JSON.stringify(P.schemes([1, 2, 5], 4)));
ok('schemes (1,2,5,10) for 8: 2 tokens, one way, 10 - 2', (function () {
  var s = P.schemes([1, 2, 5, 10], 8); return s.count === 2 && s.total === 1 && eq(s.ways, [[[10, 1], [2, -1]]]); })());
ok('schemes: every way sums to the amount and has the least count; none twice (300 random)', (function () {
  var r = rng(33), i;
  for (i = 0; i < 300; i++) {
    var c = randomCoins(r, 2 + Math.floor(r() * 4), 30, true), a = Math.floor(r() * 80), s = P.schemes(c, a, 100000);
    var seen = Object.create(null);
    if (s.count !== P.both(c, a + 1)[a] || s.total !== s.ways.length || (a > 0 && s.total < 1)) return false;
    for (var k = 0; k < s.ways.length; k++) {
      var sum = 0, n = 0; s.ways[k].forEach(function (e) { sum += e[0] * e[1]; n += Math.abs(e[1]); });
      var key = JSON.stringify(s.ways[k]);
      if (sum !== a || n !== s.count || seen[key]) return false;
      seen[key] = 1;
    }
  }
  return true; })());
ok('schemes counted a second way: all signed lists with the least count, by plain enumeration (60 small cases)', (function () {
  var r = rng(44), i;
  for (i = 0; i < 60; i++) {
    var c = randomCoins(r, 2 + Math.floor(r() * 2), 12, true).sort(function (x, y) { return x - y; }), a = 1 + Math.floor(r() * 30);
    var k = P.both(c, a + 1)[a], n = 0;
    (function rec(idx, rest, left) {
      if (idx === c.length) { if (rest === 0 && left === 0) n++; return; }
      for (var v = -left; v <= left; v++) rec(idx + 1, rest - v * c[idx], left - Math.abs(v));
    })(0, a, k);
    if (n !== P.schemes(c, a, 100000).total) return false;
  }
  return true; })());
ok('schemes stops at its limit and says so', (function () {
  var s = P.schemes([1, 2, 3, 4, 5, 6, 7, 8, 9], 20, 3); return s.ways.length === 3 && s.more === true && s.total > 3; })());

/* ---- schemes gives up when the walk is too long ---- */
ok('schemes gives up at its budget and says so; with room it does not', (function () {
  var c = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], a = P.schemes(c, 95, 5, 20), b2 = P.schemes(c, 95, 5);
  return a.gaveUp === true && a.more === true && a.total < b2.total && b2.gaveUp === false && b2.total === 7 && b2.count === 10; })());

/* ---- counting bounds, by hand ---- */
ok('signed lists by hand: two coins 4, 8, 12; three coins 6, 18, 38; multisets of 3 from 4 coins: 20', P.signedLists(2, 1) === 4 && P.signedLists(2, 2) === 8 && P.signedLists(2, 3) === 12 &&
  P.signedLists(3, 1) === 6 && P.signedLists(3, 2) === 18 && P.signedLists(3, 3) === 38 && P.multisets(4, 3) === 20);
ok('signed lists against plain counting (D to 4, k to 6)', (function () {
  for (var D = 1; D <= 4; D++) for (var k = 0; k <= 6; k++) {
    var n = 0; (function rec(i, left) { if (i === D) { if (left === 0) n++; return; } for (var v = -left; v <= left; v++) rec(i + 1, left - Math.abs(v)); })(0, k);
    if (n !== P.signedLists(D, k)) return false;
  }
  return true; })());
ok('bound by hand, amounts 1 to 99: both ways 660 (two coins), 385 (three), 308 (four); one way 490 (three), 374 (four); one coin 4950 each way', P.bound(2, 100, 'both') === 660 &&
  P.bound(3, 100, 'both') === 385 && P.bound(4, 100, 'both') === 308 && P.bound(3, 100, 'plain') === 490 && P.bound(4, 100, 'plain') === 374 && P.bound(1, 100, 'plain') === 4950 && P.bound(1, 100, 'both') === 4950,
  [P.bound(2, 100, 'both'), P.bound(3, 100, 'both'), P.bound(4, 100, 'both'), P.bound(3, 100, 'plain'), P.bound(4, 100, 'plain')].join());
ok('no coinage beats its bound (400 random, both counts)', (function () {
  var r = rng(77), i;
  for (i = 0; i < 400; i++) {
    var D = 1 + Math.floor(r() * 6), c = randomCoins(r, D, 80, r() < 0.6), Lx = 20 + Math.floor(r() * 100);
    var p = P.total(P.plain(c, Lx)), q = P.total(P.both(c, Lx));
    if (p < P.bound(D, Lx, 'plain') || q < P.bound(D, Lx, 'both')) return false;
  }
  return true; })());

/* ---- clean ---- */
ok('clean refuses 0, a fraction, a negative, a string', [0, 2.5, -3, '5'].every(function (x) {
  try { P.clean([1, x]); return false; } catch (e) { return true; } }));

ok('a coin given twice is one coin: clean gives each once, sorted; the ways of settling and Pearson\'s test do not change', (function () {
  var s1 = P.schemes([5, 1, 2, 5, 1], 4), s2 = P.schemes([1, 2, 5], 4);
  return eq(P.clean([5, 1, 2, 5, 1]), [1, 2, 5]) && s1.total === 2 && eq(s1.ways, s2.ways) && P.pearson([1, 5, 5, 10, 25, 25]) === 0 && P.pearson([10, 1, 7, 7]) === 14; })());

/* ---- meanText ---- */
ok('meanText: 470/100 is 4.7; 389/99 is about 3.929; Infinity is said', P.meanText(470, 100) === '4.7' && P.meanText(389, 99) === 'about 3.929' &&
  P.meanText(Infinity, 100) === 'cannot make every amount' && P.meanText(2289, 500) === '4.578', [P.meanText(470, 100), P.meanText(389, 99), P.meanText(2289, 500)].join(' | '));
/* added 27 November 2026: half up, exactly. Every total from 0 to 12 L for L from 2 to 320, at three places and at two,
   against whole-number arithmetic done here in BigInt (not the function's own formula in floating point) */
var halfUp = (function () {
  var bad = [], half = 0, n = 0, L, tot, places;
  for (places = 2; places <= 3; places++) for (L = 2; L <= 320; L++) for (tot = 0; tot <= 12 * L; tot++) {
    var T = BigInt(tot), LL = BigInt(L), sc = places === 3 ? 1000n : 100n, q = (2n * sc * T + LL) / (2n * LL), exact = q * LL === sc * T;
    if ((2n * sc * T) % LL === 0n && (sc * T) % LL !== 0n) half++;
    var str = (q / sc) + '.' + String(q % sc).padStart(places, '0'); str = str.replace(/0+$/, '').replace(/\.$/, '');
    var want = (exact ? '' : 'about ') + str, got = P.meanText(tot, L, places); n++;
    if (got !== want && bad.length < 5) bad.push(tot + '/' + L + ' to ' + places + ' places: ' + got + ' where ' + want + ' is right');
  }
  return { bad: bad, half: half, n: n };
})();
ok('meanText: rounded half up, and "about" exactly when the decimal does not end: ' + halfUp.n + ' totals and ranges, ' + halfUp.half + ' of them half-way',
  halfUp.bad.length === 0 && halfUp.half > 1000 && P.meanText(3, 80) === 'about 0.038' && P.meanText(1323, 240) === 'about 5.513' && P.meanText(1, 16) === 'about 0.063' &&
  P.meanText(1, 8) === '0.125' && P.meanText(1, 8, 2) === 'about 0.13' && P.meanText(0, 7) === '0',
  halfUp.bad.join('; ') || [P.meanText(3, 80), P.meanText(1323, 240), P.meanText(1, 16), P.meanText(1, 8), P.meanText(1, 8, 2), P.meanText(0, 7)].join(' | '));

/* ---- the C search against the core, every set tried here too ---- */
function search(mode, D, L, M) {
  var out = cp.execFileSync(path.join(__dirname, 'search'), [mode, String(D), String(L), String(M)], { encoding: 'utf8' });
  var best = [], tot = Number(/least total (-?\d+)/.exec(out)[1]), worst = Number(/least worst case (-?\d+)/.exec(out)[1]);
  out.split('\n').forEach(function (l) { var q = /^\s+best (.*)$/.exec(l); if (q) best.push(q[1].trim().split(/\s+/).map(Number)); });
  return { total: tot, best: best, worst: worst, nWorst: Number(/sets with the least worst case (\d+)/.exec(out)[1]), sets: Number(/sets scored (\d+)/.exec(out)[1]) };
}
function brute(mode, D, L, M) {
  var best = Infinity, sets = [], w = Infinity, nW = 0, n = 0, cur = [];
  (function rec(d, from) {
    if (d === D) {
      var t = P.counts(cur, L, mode), s = P.total(t), ww = P.worst(t);
      if (!isFinite(s)) return;
      n++;
      if (s < best) { best = s; sets = []; }
      if (s === best) sets.push(cur.slice());
      if (ww < w) { w = ww; nW = 0; }
      if (ww === w) nW++;
      return;
    }
    for (var c = from; c <= M; c++) { cur[d] = c; rec(d + 1, c + 1); }
    cur.length = d;
  })(mode === 'both' ? 0 : 1, mode === 'both' ? 1 : 2, (mode === 'both' ? 0 : (cur[0] = 1)));
  return { total: best, best: sets, worst: w, nWorst: nW, sets: n };
}
[['plain', 2, 30, 29], ['plain', 3, 40, 39], ['plain', 4, 25, 24], ['greedy', 3, 40, 39], ['greedy', 4, 25, 24],
 ['both', 1, 12, 20], ['both', 2, 30, 40], ['both', 3, 25, 30]].forEach(function (q) {
  var a = search(q[0], q[1], q[2], q[3]), b2 = brute(q[0], q[1], q[2], q[3]);
  ok('C search = every set tried in JS: ' + q.join(' '), a.total === b2.total && eq(a.best, b2.best) && a.worst === b2.worst && a.nWorst === b2.nWorst && a.sets === b2.sets,
    JSON.stringify(a) + ' vs ' + JSON.stringify(b2));
});
ok('C search, by hand: one coin, plain, below 5 is 0+1+2+3+4 = 10', search('plain', 1, 5, 4).total === 10);
ok('C search, by hand: one coin both ways below 4, coins to 3: coin 1 gives 0,1,2,3 = 6 and nothing else makes 1', (function () {
  var s = search('both', 1, 4, 3); return s.total === 6 && eq(s.best, [[1]]) && s.sets === 1; })());

/* ---- a search shared out by FIRST and put together by merge.py is the whole search ---- */
ok('a search shared out and put together again by merge.py is the whole search (four coins one way below 30; three both ways below 25)', (function () {
  var fs = require('fs'), os = require('os'), PY = process.env.PYTHON || (fs.existsSync('/home/agent2/vuza/.venv/bin/python') ? '/home/agent2/vuza/.venv/bin/python' : 'python3');
  function whole(mode, D, L, M) { return cp.execFileSync(path.join(__dirname, 'search'), [mode, D, L, M].map(String), { encoding: 'utf8' }); }
  function shared(mode, D, L, M, from, to) {
    var dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agent2-coin-')), f;
    for (f = from; f <= to; f++) fs.writeFileSync(path.join(dir, 'first-' + f + '.out'), cp.execFileSync(path.join(__dirname, 'search'), [mode, D, L, M, f].map(String), { encoding: 'utf8' }));
    var out = cp.execFileSync(PY, ['-I', path.join(__dirname, 'merge.py'), dir], { encoding: 'utf8' });
    fs.rmSync(dir, { recursive: true });
    return out;
  }
  function key(s) {
    return ['sets scored', 'least total', 'sets with the least total', 'least worst case', 'sets with the least worst case'].map(function (k) { return new RegExp(k + ' (-?\\d+)').exec(s)[1]; }).join('|') +
      '|' + s.split('\n').filter(function (l) { return /^  best/.test(l); }).join(';');
  }
  var a = key(whole('plain', 4, 30, 29)), b2 = key(shared('plain', 4, 30, 29, 2, 27)), c = key(whole('both', 3, 25, 30)), d = key(shared('both', 3, 25, 30, 1, 28));
  if (a !== b2 || c !== d) console.log('      ' + a + '\n      ' + b2 + '\n      ' + c + '\n      ' + d);
  return a === b2 && c === d; })());

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);

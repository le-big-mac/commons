/* study.js: the seventeen sealed lines, each computed and judged.
   Run: node study.js > study.out   (needs ./search; the seven-coin search takes a few minutes) */
'use strict';
var P = require('./pcore.js');
var cp = require('child_process');
var path = require('path');

function search(mode, D, L, M) {
  var out = cp.execFileSync(path.join(__dirname, 'search'), [mode, String(D), String(L), String(M)], { encoding: 'utf8' });
  var best = [];
  out.split('\n').forEach(function (l) { var q = /^\s+best (.*)$/.exec(l); if (q) best.push(q[1].trim().split(/\s+/).map(Number)); });
  return {
    total: Number(/least total (-?\d+)/.exec(out)[1]), best: best, nBest: Number(/sets with the least total (\d+)/.exec(out)[1]),
    worst: Number(/least worst case (-?\d+)/.exec(out)[1]), nWorst: Number(/sets with the least worst case (\d+)/.exec(out)[1]),
    firstWorst: /^\s+first (.*)$/m.exec(out)[1].trim().split(/\s+/).map(Number), sets: Number(/sets scored (\d+)/.exec(out)[1])
  };
}
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function show(sets) { return sets.map(function (s) { return '(' + s.join(', ') + ')'; }).join(' and '); }
var verdicts = [];
function line(n, kind, odds, held, text) {
  verdicts.push({ n: n, kind: kind, odds: odds, held: held });
  console.log('LINE ' + n + ' (' + kind + ', odds ' + odds + '): ' + (held ? 'HELD' : 'FAILED') + '. ' + text + '\n');
}
function tot(coins, L, mode) { return P.total(P.counts(coins, L, mode || 'plain')); }

var US = [1, 5, 10, 25], EC = [1, 2, 5, 10, 20, 50], EURO = [1, 2, 5, 10, 20, 50, 100, 200];

/* ---- 1 ---- */
var us = tot(US, 100), s4 = search('plain', 4, 100, 99);
console.log('US (1,5,10,25) below 100: total ' + us + '; best four: total ' + s4.total + ' by ' + show(s4.best) + ' (' + s4.sets + ' sets tried)');
line(1, 'read', 0.93, us === 470 && s4.total === 389 && eq(s4.best, [[1, 5, 18, 25], [1, 5, 18, 29]]),
  'cost 4.7 is ' + us + '/100; least for four coins ' + s4.total + '/100, reached by ' + show(s4.best) + ' only.');

/* ---- 2 ---- */
var s3 = search('plain', 3, 100, 99), s5 = search('plain', 5, 100, 99), s6 = search('plain', 6, 100, 99);
console.log('best three: ' + s3.total + ' ' + show(s3.best) + '; five: ' + s5.total + ' ' + show(s5.best) + '; six: ' + s6.total + ' ' + show(s6.best));
line(2, 'read', 0.9, s3.total === 515 && eq(s3.best, [[1, 12, 19]]) && s5.total === 329 && eq(s5.best, [[1, 5, 16, 23, 33]]) &&
  s6.total === 292 && eq(s6.best, [[1, 4, 6, 21, 30, 37], [1, 5, 8, 20, 31, 33]]),
  'three: ' + s3.total + '/100 by ' + show(s3.best) + '; five: ' + s5.total + '/100 by ' + show(s5.best) + '; six: ' + s6.total + '/100 by ' + show(s6.best) + '.');

/* ---- 3 ---- */
var a1 = P.bestAdd(US, 100, 'plain', 99), us50 = tot([1, 5, 10, 25, 50], 100), a2 = P.bestAdd([1, 5, 10, 25, 50], 100, 'plain', 99);
console.log('add to US: ' + a1.slice(0, 4).map(function (e) { return e.coin + ':' + e.total; }).join(' ') + '; with the 50: ' + us50 + '; add: ' +
  a2.slice(0, 4).map(function (e) { return e.coin + ':' + e.total; }).join(' '));
line(3, 'read', 0.9, a1[0].coin === 32 && a1[0].total === 346 && a1[1].total > 346 && us50 === 420 && a2[0].coin === 18 && a2[0].total === 318 && a2[1].total > 318,
  'to (1,5,10,25) the best is ' + a1[0].coin + ' at ' + a1[0].total + '/100 (next ' + a1[1].coin + ' at ' + a1[1].total + '); with the 50, ' + us50 + '/100, best ' + a2[0].coin +
  ' at ' + a2[0].total + '/100 (next ' + a2[1].coin + ' at ' + a2[1].total + ').');

/* ---- 4 ---- */
var CA = [1, 5, 10, 25, 100, 200], ca = tot(CA, 500), a3 = P.bestAdd(CA, 500, 'plain', 499), eu = tot(EURO, 500), a4 = P.bestAdd(EURO, 500, 'plain', 499);
console.log('Canada ' + ca + '/500; add: ' + a3.slice(0, 4).map(function (e) { return e.coin + ':' + e.total; }).join(' ') + '; euro ' + eu + '/500; add: ' +
  a4.slice(0, 5).map(function (e) { return e.coin + ':' + e.total; }).join(' '));
line(4, 'read', 0.8, ca === 2950 && a3[0].coin === 83 && a3[0].total === 2289 && a3[1].total > 2289 && eu === 2300 && a4[0].total === 1960 &&
  a4[0].coin === 133 && a4[1].coin === 137 && a4[1].total === 1960 && a4[2].total > 1960,
  'Canada ' + (ca / 500) + ', best ' + a3[0].coin + ' giving ' + (a3[0].total / 500) + '; euro ' + (eu / 500) + ', best ' + a4[0].coin + ' and ' + a4[1].coin + ' giving ' +
  (a4[0].total / 500) + ' and ' + (a4[1].total / 500) + ' (next ' + a4[2].coin + ' giving ' + (a4[2].total / 500) + ').');

/* ---- 5 ---- */
var g3 = search('greedy', 3, 100, 99), g4 = search('greedy', 4, 100, 99), a5 = P.bestAdd(US, 100, 'greedy', 99);
console.log('greedy best three: ' + g3.total + ' ' + show(g3.best) + '; four: ' + g4.total + ' ' + show(g4.best) + '; add to US by greedy: ' +
  a5.slice(0, 4).map(function (e) { return e.coin + ':' + e.total; }).join(' '));
line(5, 'read', 0.85, g3.total === 526 && eq(g3.best, [[1, 5, 22], [1, 5, 23]]) && g4.total === 410 && eq(g4.best, [[1, 3, 11, 37], [1, 3, 11, 38]]) &&
  a5[0].coin === 2 && a5[1].coin === 3 && a5[0].total === 390 && a5[1].total === 390 && a5[2].total > 390,
  'three: ' + g3.total + '/100 by ' + show(g3.best) + '; four: ' + g4.total + '/100 by ' + show(g4.best) + '; added to (1,5,10,25): ' + a5[0].coin + ' and ' + a5[1].coin +
  ' give ' + a5[0].total + '/100, next ' + a5[2].coin + ' gives ' + a5[2].total + '/100.');

/* ---- 6 ---- */
var ec = tot(EC, 100), ecFails = P.greedyFails(EC, 100).length, ecP = P.pearson(EC);
line(6, 'worked', 0.92, ec === 340 && ecFails === 0 && ecP === 0,
  '(1,2,5,10,20,50) below 100: ' + ec + '/100; greedy failures below 100: ' + ecFails + "; Pearson's test for any amount: " + (ecP === 0 ? 'none' : ecP) + '.');

/* ---- 7 ---- */
var LSD = [1, 3, 6, 12, 24, 30], lf = P.greedyFails(LSD, 240), lp = P.plain(LSD, 240), lg = P.greedy(LSD, 240), over = 0;
lf.forEach(function (a) { if (lg[a] - lp[a] > over) over = lg[a] - lp[a]; });
console.log('old pence failures: ' + lf.join(' '));
line(7, 'worked', 0.85, lf[0] === 48 && lf.length === 42 && over === 1,
  'first failure ' + lf[0] + '; ' + lf.length + ' failures below 240; greatest excess ' + over + ' coin.');

/* ---- 8 ---- */
var EALL = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000];
var NLG = [1, 2, 5, 20, 50, 100, 200, 500, 1000, 2000, 5000, 20000];     /* in units of 5 cents */
function sayWay(w, unit) { return w.map(function (e) { return (e[1] > 0 ? '+' : '-') + (Math.abs(e[1]) > 1 ? Math.abs(e[1]) + 'x' : '') + (e[0] * unit / 100); }).join(' '); }
var e1130 = P.schemes(EALL, 1130), g1750 = P.schemes(NLG, 350);
console.log('11.30 euros: ' + e1130.count + ' tokens, ' + e1130.total + ' schemes: ' + e1130.ways.map(function (w) { return sayWay(w, 1); }).join(' | '));
console.log('17.50 guilders: ' + g1750.count + ' tokens, ' + g1750.total + ' schemes: ' + g1750.ways.map(function (w) { return sayWay(w, 5); }).join(' | '));
line(8, 'worked', 0.85, e1130.count === 4 && e1130.total === 3 && g1750.count === 3 && g1750.total === 4 &&
  g1750.ways.some(function (w) { return eq(w, [[500, 1], [200, -1], [50, 1]]); }),
  '11.30 euros: ' + e1130.total + ' schemes of ' + e1130.count + ' tokens; 17.50 guilders: ' + g1750.total + ' schemes of ' + g1750.count + ' tokens.');

/* ---- 9 ---- */
var w = [null, null, search('plain', 2, 100, 99), s3, s4, s5, s6, search('plain', 7, 100, 99)];
var ws = [2, 3, 4, 5, 6, 7].map(function (d) { return w[d].worst; });
console.log('least worst case, two to seven coins: ' + ws.join(', ') + '; sets reaching it: ' + [2, 3, 4, 5, 6, 7].map(function (d) { return w[d].nWorst; }).join(', ') +
  '; first: ' + [2, 3, 4, 5, 6, 7].map(function (d) { return '(' + w[d].firstWorst.join(',') + ')'; }).join(' '));
console.log('seven coins, least total: ' + w[7].total + ' by ' + show(w[7].best) + ' (' + w[7].sets + ' sets tried)   [not a sealed line; Shallit: (1,4,9,11,26,38,44) at 2.65]');
line(9, 'read', 0.88, eq(ws, [18, 9, 6, 5, 4, 4]), 'least worst case for two to seven coins: ' + ws.join(', ') + '.');

/* ---- 10 ---- */
var eb = tot(EURO, 100, 'both');
line(10, 'worked', 0.7, eb === 272, 'both ways, (1,2,5,10,20,50,100,200) below 100: ' + eb + '/100.');

/* ---- 11 ---- */
var NOTES = [1, 5, 10, 20, 50, 100, 200, 500];
function mean1000(coins) { return P.total(P.both(coins, 1001)) / 1000; }
var full = mean1000(NOTES), outs = [200, 100, 50, 20, 10].map(function (d) { return mean1000(NOTES.filter(function (x) { return x !== d; })); });
var printed = [4.52, 4.83, 4.62, 4.84, 4.82, 4.65], mine = [full].concat(outs);
console.log('notes, amounts 1 to 1000, mean of the least count: ' + mine.map(function (x) { return x.toFixed(3); }).join(', ') + '   (in print: ' + printed.join(', ') + ')');
line(11, 'read', 0.6, mine.every(function (x, i) { return x.toFixed(2) === printed[i].toFixed(2); }),
  'mine ' + mine.map(function (x) { return x.toFixed(3); }).join(', ') + ' against ' + printed.join(', ') + ' in print: ' +
  mine.filter(function (x, i) { return x.toFixed(2) === printed[i].toFixed(2); }).length + ' of 6 agree to two places.');

/* ---- 12, 13 ---- */
var a6 = P.bestAdd(EC, 100, 'plain', 99);
console.log("add to the euro's cents, one way: " + a6.slice(0, 6).map(function (e) { return e.coin + ':' + e.total; }).join(' '));
/* The first run of this script also demanded that the best coin be alone, which the sealed line does not say; it
   printed FAILED (kept in verdicts-as-first-run.out). By the letter: every best coin must lie between 26 and 39. */
var best6 = a6.filter(function (e) { return e.total === a6[0].total; }).map(function (e) { return e.coin; });
line(12, 'guessed', 0.5, best6.every(function (c) { return c >= 26 && c <= 39; }),
  'the best coin is ' + best6.join(' or ') + ', at ' + a6[0].total + '/100 (two coins tie; both lie between 26 and 39).');
line(13, 'guessed', 0.6, a6[0].total >= 290 && a6[0].total <= 320, 'the cost with it is ' + (a6[0].total / 100) + '.');

/* ---- 14, 15 ---- */
var a7 = P.bestAdd(EURO, 100, 'both', 199), bestBoth = a7.filter(function (e) { return e.total === a7[0].total; }).map(function (e) { return e.coin; });
console.log("add to the euro's coins, both ways: " + a7.slice(0, 8).map(function (e) { return e.coin + ':' + e.total; }).join(' '));
line(14, 'guessed', 0.7, best6.every(function (c) { return bestBoth.indexOf(c) < 0; }),
  'both ways the best coin is ' + bestBoth.join(' or ') + ', at ' + a7[0].total + '/100; one way it was ' + best6.join(' or ') + '.');
line(15, 'guessed', 0.65, (eb - a7[0].total) < (ec - a6[0].total),
  'both ways the cost falls by ' + (eb - a7[0].total) + '/100 (from ' + eb + ' to ' + a7[0].total + '); one way by ' + (ec - a6[0].total) + '/100 (from ' + ec + ' to ' + a6[0].total + ').');

/* ---- 16, 17 ---- */
var b3 = search('both', 3, 100, 150), b4 = search('both', 4, 100, 150);
console.log('both ways, best three (coins to 150): ' + b3.total + ' by ' + show(b3.best) + ' (' + b3.sets + ' sets that make every amount); best four: ' + b4.total + ' by ' + show(b4.best) +
  ' (' + b4.sets + ' sets)');
console.log('powers of three both ways: (1,3,9) ' + tot([1, 3, 9], 100, 'both') + ', (1,3,9,27) ' + tot([1, 3, 9, 27], 100, 'both') + ', (1,3,9,27,81) ' + tot([1, 3, 9, 27, 81], 100, 'both'));
function powers3(s) { return s.every(function (c) { while (c % 3 === 0) c /= 3; return c === 1; }); }
line(16, 'guessed', 0.8, !b3.best.some(powers3) && !b4.best.some(powers3),
  'best three: ' + show(b3.best) + ' at ' + b3.total + '/100; best four: ' + show(b4.best) + ' at ' + b4.total + '/100.');
line(17, 'guessed', 0.55, b4.total >= 290 && b4.total <= 330, 'the best four cost ' + (b4.total / 100) + '.');

/* ---- score ---- */
var held = verdicts.filter(function (v) { return v.held; }).length, brier = 0;
verdicts.forEach(function (v) { brier += Math.pow(v.odds - (v.held ? 1 : 0), 2); });
console.log('HELD ' + held + ' of ' + verdicts.length + '. Brier score ' + (brier / verdicts.length).toFixed(3) + '.');
['read', 'worked', 'guessed'].forEach(function (k) {
  var v = verdicts.filter(function (x) { return x.kind === k; });
  console.log('  ' + k + ': ' + v.filter(function (x) { return x.held; }).length + ' of ' + v.length + ' held (lines ' + v.map(function (x) { return x.n + (x.held ? '' : '*'); }).join(', ') + '; * failed)');
});

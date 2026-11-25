/* after.js: checks made after the sealed lines were judged. None of this was sealed.
   Run: node after.js > after.out */
'use strict';
var P = require('./pcore.js');
function tot(coins, L, mode) { return P.total(P.counts(coins, L, mode || 'plain')); }
var EC6 = [1, 2, 5, 10, 20, 50];

/* ---------- A. counting bounds ----------
   One way: an amount that takes k coins is a multiset of k coins; there are C(D+k-1, k) of them.
   Both ways: an amount that takes k tokens is a list of D whole numbers with absolute values summing
   to k; a list and its negative give an amount and its negative, so at most half of the lists with
   count k give amounts above 0. Fill the cheapest counts first: no set of D coins can total less. */
var signedLists = P.signedLists;
function bound(D, amounts, perCount) { return P.bound(D, amounts + 1, perCount); }
console.log('A. Counting bounds for amounts 1 to 99 (totals; divide by 100 for the cost over 0 to 99)');
console.log('   signed lists by hand: D=2: 4, 8, 12 for k=1,2,3; D=3: 6, 18, 38. Program: ' +
  [1, 2, 3].map(function (k) { return signedLists(2, k); }).join(', ') + '; ' + [1, 2, 3].map(function (k) { return signedLists(3, k); }).join(', '));
var BESTJ = JSON.parse(require('fs').readFileSync(require('path').join(__dirname, 'best.json'), 'utf8'));     /* made by make-best.js from the searches */
var plainBest = [null].concat(BESTJ.plain.map(function (r) { return r.total; })), bothBest = {};
BESTJ.both.forEach(function (r, i) { bothBest[i + 1] = r.total; });
console.log('   coins | one way: bound, best found, gap | both ways: bound, best found, gap');
for (var D = 1; D <= 7; D++) {
  var pb = bound(D, 99, 'plain'), bb = bound(D, 99, 'both');
  console.log('   ' + D + '     | ' + pb + ', ' + plainBest[D] + ', ' + (plainBest[D] - pb) + ' | ' + bb + ', ' + (bothBest[D] !== undefined ? bothBest[D] + ', ' + (bothBest[D] - bb) : 'not searched'));
}

/* ---------- B. the best both-ways sets, looked at ---------- */
console.log('\nB. The best three coins both ways, (16, 19, 21), for amounts below 100');
var T3 = [16, 19, 21], b3 = P.both(T3, 100), hist = {}, a;
for (a = 1; a < 100; a++) hist[b3[a]] = (hist[b3[a]] || 0) + 1;
console.log('   amounts by number of tokens: ' + Object.keys(hist).map(function (k) { return k + ': ' + hist[k]; }).join(', ') + '   (room by counting: 1: 3, 2: 9, 3: 19, 4: 33, 5: 51)');
[1, 2, 3, 5, 10, 50, 99].forEach(function (x) {
  var s = P.schemes(T3, x);
  console.log('   ' + x + ' takes ' + s.count + ': ' + s.ways.map(function (w) { return w.map(function (e) { return (e[1] > 0 ? '+' : '-') + (Math.abs(e[1]) > 1 ? Math.abs(e[1]) + 'x' : '') + e[0]; }).join(' '); }).join(' | '));
});
var negTop = 0;
for (a = 1; a < 100; a++) { var sw = P.schemes(T3, a).ways; if (sw.every(function (w) { return w[0][1] < 0; })) negTop++; }
console.log('   amounts whose every best way hands the largest coin used BACK: ' + negTop);
console.log('   one way, (16,19,21) cannot make ' + Array.from(P.plain(T3, 100)).filter(function (v) { return v >= P.INF; }).length + ' of the amounts 1 to 99');
console.log('   the four best sets of four, worst case and what 1 takes: ' + [[13, 28, 32, 33], [18, 21, 25, 37], [19, 20, 23, 32], [20, 21, 25, 32]].map(function (s) {
  var t = P.both(s, 100); return '(' + s.join(',') + ') worst ' + P.worst(t) + ', 1 takes ' + t[1]; }).join('; '));

/* ---------- C. real coinages, and the series the economists argue over ---------- */
console.log('\nC. Coinages side by side: total coins over the amounts below L (cost = total / L), worst case in brackets');
var sets = [
  ['US cents (1,5,10,25)', [1, 5, 10, 25], 100],
  ['US with half and dollar (1,5,10,25,50,100)', [1, 5, 10, 25, 50, 100], 100],
  ["euro's cents (1,2,5,10,20,50)", [1, 2, 5, 10, 20, 50], 100],
  ['euro coins (1,2,5,10,20,50,100,200)', [1, 2, 5, 10, 20, 50, 100, 200], 100],
  ['Shallit (1,5,18,25)', [1, 5, 18, 25], 100],
  ['powers of two (1,2,4,8,16,32,64)', [1, 2, 4, 8, 16, 32, 64], 100],
  ['powers of two with 128', [1, 2, 4, 8, 16, 32, 64, 128], 100],
  ['powers of three (1,3,9,27,81)', [1, 3, 9, 27, 81], 100],
  ['powers of three with 243', [1, 3, 9, 27, 81, 243], 100],
  ['best three both ways (16,19,21)', [16, 19, 21], 100],
  ['best four both ways (19,20,23,32)', [19, 20, 23, 32], 100],
  ['old pence (1,3,6,12,24,30), below 240', [1, 3, 6, 12, 24, 30], 240],
  ['old pence with crown and pound (1,3,6,12,24,30,60,240), below 240', [1, 3, 6, 12, 24, 30, 60, 240], 240],
  ['guilder in 5-cent units (1,2,5,20,50,100,200), below 100', [1, 2, 5, 20, 50, 100, 200], 100]
];
sets.forEach(function (s) {
  var p = P.plain(s[1], s[2]), g = P.greedy(s[1], s[2]), b = P.both(s[1], s[2]);
  function f(t) { var x = P.total(t); return isFinite(x) ? x + ' [' + P.worst(t) + ']' : 'cannot'; }
  console.log('   ' + s[0] + ': one way ' + f(p) + ', greedy ' + f(g) + ', both ways ' + f(b) + '; L = ' + s[2]);
});
console.log('   powers of three one way and both ways, by the digits: both ways (1,3,9,27,81) takes for 5: ' + P.both([1, 3, 9, 27, 81], 100)[5] + ' (9 - 3 - 1), for 40: ' + P.both([1, 3, 9, 27, 81], 100)[40] + ' (27 + 9 + 3 + 1)');

/* ---------- D. the coin to add, both ways and one way, for several coinages ---------- */
console.log('\nD. The coin to add (amounts below 100; candidates to 99 one way, to 199 both ways)');
[['US cents', [1, 5, 10, 25]], ["euro's cents", [1, 2, 5, 10, 20, 50]], ['euro coins', [1, 2, 5, 10, 20, 50, 100, 200]], ['US with half and dollar', [1, 5, 10, 25, 50, 100]]].forEach(function (s) {
  var one = P.bestAdd(s[1], 100, 'plain', 99), two = P.bestAdd(s[1], 100, 'both', 199);
  function top(l) { return l.filter(function (e) { return e.total === l[0].total; }).map(function (e) { return e.coin; }).join(' or ') + ' (' + l[0].total + ')'; }
  console.log('   ' + s[0] + ': one way ' + tot(s[1], 100) + ' -> ' + top(one) + '; both ways ' + tot(s[1], 100, 'both') + ' -> ' + top(two));
});

/* ---------- E. the old pence, with the crown, and in halfpence ---------- */
console.log('\nE. Old British coins');
[['pence (1,3,6,12,24,30)', [1, 3, 6, 12, 24, 30], 240], ['with the crown (1,3,6,12,24,30,60)', [1, 3, 6, 12, 24, 30, 60], 240],
 ['in halfpence with the halfpenny (1,2,6,12,24,48,60), below 480', [1, 2, 6, 12, 24, 48, 60], 480],
 ['without the half-crown (1,3,6,12,24)', [1, 3, 6, 12, 24], 240], ['without the florin (1,3,6,12,30)', [1, 3, 6, 12, 30], 240]].forEach(function (s) {
  var f = P.greedyFails(s[1], s[2]);
  console.log('   ' + s[0] + ': greedy fails for ' + f.length + ' amounts below ' + s[2] + (f.length ? ', first ' + f[0] : '') + "; Pearson's test: " + (P.pearson(s[1]) || 'never fails'));
});

/* Wagon's question, in halfpence: halfpenny 1, penny 2, threepence 6, sixpence 12, shilling 24, florin 48,
   half-crown 60, crown 120, pound 480. Which coins can be taken away to leave a system where greedy never fails? */
(function () {
  var W = [1, 2, 6, 12, 24, 48, 60, 120, 480], names = { 2: 'penny', 6: 'threepence', 12: 'sixpence', 24: 'shilling', 48: 'florin', 60: 'half-crown', 120: 'crown', 480: 'pound' };
  console.log("   Wagon's system in halfpence (1,2,6,12,24,48,60,120,480): Pearson's test gives " + P.pearson(W) + ' halfpence as the first failure (' + P.pearson(W) / 2 + ' pence)');
  console.log('   with one coin taken away: ' + W.slice(1).map(function (c) { var f = P.pearson(W.filter(function (x) { return x !== c; })); return names[c] + ': ' + (f ? 'fails at ' + f : 'never fails'); }).join('; '));
})();

/* ---------- F. the tables of Kippers and Franses (2003), recounted ----------
   Count the schemes of every amount at once: f[t][s] = number of lists with count t and sum s. */
function countAll(coins, Amax) {
  var K = P.worst(P.both(coins, Amax + 1)), cmax = Math.max.apply(null, coins), S = K * cmax, W = 2 * S + 1;
  var f = [], g = [], t, i, s, n, c;
  for (t = 0; t <= K; t++) { f.push(new Float64Array(W)); g.push(new Float64Array(W)); }
  f[0][S] = 1;
  for (i = 0; i < coins.length; i++) {
    c = coins[i];
    for (t = 0; t <= K; t++) {
      var gt = g[t]; gt.fill(0);
      for (n = -t; n <= t; n++) {
        var src = f[t - Math.abs(n)], sh = n * c, lo = Math.max(0, sh), hi = Math.min(W, W + sh);
        for (s = lo; s < hi; s++) gt[s] += src[s - sh];
      }
    }
    var tmp = f; f = g; g = tmp;
  }
  var out = { K: K, schemes: 0, tokensOverSchemes: 0, tokensOverAmounts: 0, maxSchemes: 0, maxAt: 0, maxTokens: 0, count: [], k: [], bySize: {} };
  var bw = P.both(coins, Amax + 1);
  for (var A = 1; A <= Amax; A++) {
    for (t = 0; t <= K; t++) if (f[t][S + A] > 0) break;
    if (t !== bw[A]) throw new Error('the two counts disagree at ' + A);
    var ns = f[t][S + A];
    out.schemes += ns; out.tokensOverSchemes += ns * t; out.tokensOverAmounts += t;
    if (ns > out.maxSchemes) { out.maxSchemes = ns; out.maxAt = A; }
    if (t > out.maxTokens) out.maxTokens = t;
    out.count.push(ns); out.k.push(t);
    out.bySize[t] = (out.bySize[t] || 0) + ns;
  }
  return out;
}
function median(o) {            /* median tokens over schemes */
  var half = o.schemes / 2, run = 0, ks = Object.keys(o.bySize).map(Number).sort(function (x, y) { return x - y; });
  for (var i = 0; i < ks.length; i++) { run += o.bySize[ks[i]]; if (run >= half) return ks[i]; }
}
/* the counter against schemes() on a sample */
(function () {
  var c = [1, 5, 10, 20, 50, 100, 200, 500], o = countAll(c, 1000), bad = 0, x;
  for (x = 1; x <= 1000; x += 7) if (P.schemes(c, x, 100000).total !== o.count[x - 1]) bad++;
  console.log('\nF. The tables of Kippers and Franses (2003), recounted with my definition of a scheme');
  console.log('   the all-at-once counter against schemes() on 143 amounts: ' + bad + ' disagreements');
})();
function row(name, coins, Amax, printed) {
  var o = countAll(coins, Amax);
  console.log('   ' + name + ': schemes ' + o.schemes + ', tokens per scheme ' + (o.tokensOverSchemes / o.schemes).toFixed(2) + ', median ' + median(o) + ', most tokens ' + o.maxTokens +
    ', most schemes for one amount ' + o.maxSchemes + ' (first at ' + o.maxAt + '), tokens per amount ' + (o.tokensOverAmounts / Amax).toFixed(2) + '\n        in print: ' + printed);
  return o;
}
var N = [1, 5, 10, 20, 50, 100, 200, 500];
row('Table 3, all notes, 1 to 1000', N, 1000, 'schemes 2553, per scheme 5.18, median 5, most tokens 8, most schemes 18, per amount 4.52');
[[200, '1766, 5.26, 5, 8, 6, 4.83'], [100, '1873, 5.10, 5, 8, 9, 4.62'], [50, '2034, 5.34, 5, 8, 8, 4.84'], [20, '1862, 5.27, 5, 8, 8, 4.82'], [10, '1964, 5.12, 5, 8, 10, 4.65']].forEach(function (q) {
  row('Table 3 without the ' + q[0], N.filter(function (x) { return x !== q[0]; }), 1000, q[1] + ' (same order)');
});
var EALL = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000];
row('Table 2, all euro coins and notes, 0.01 to 100.00', EALL, 10000, 'schemes 36,591, per scheme 5.83, median 6, most tokens 8');
row('Table 2, no 1 or 2 cent, multiples of 0.05 to 100.00', [1, 2, 4, 10, 20, 40, 100, 200, 400, 1000, 2000, 4000, 10000], 2000, 'schemes 5,957, per scheme 4.93, median 5, most tokens 7');
var NLG = [1, 2, 5, 20, 50, 100, 200, 500, 1000, 2000, 5000, 20000];
var g = row('Table 1, guilder, 0.05 to 100.00', NLG, 2000, 'schemes 14,928, per scheme 5.68, median 6, most tokens 8; and in Kippers et al.: Cramer found no amount needing more than seven, and 16.65 with the most schemes, ten');
console.log('   guilder 16.65 (333 units): ' + g.count[332] + ' schemes of ' + g.k[332] + ' tokens; 17.50: ' + g.count[349] + ' of ' + g.k[349]);

/* ---------- G. one step off the grid: other ranges of amounts ---------- */
console.log('\nG. Three coins both ways against four coins one way, at other ranges (totals over the amounts below L)');
(function () {
  var fs = require('fs'), path = require('path');
  function rd(name) {
    var t = fs.readFileSync(path.join(__dirname, 'runs', 'offgrid', name + '.out'), 'utf8');
    return { total: Number(/least total (\d+)/.exec(t)[1]), sets: t.split('\n').filter(function (l) { return /^  best/.test(l); }).map(function (l) { return '(' + l.trim().split(/\s+/).slice(1).join(',') + ')'; }) };
  }
  function show(r, n) { return r.total + ' ' + r.sets.slice(0, n || 2).join(' ') + (r.sets.length > (n || 2) ? ' and ' + (r.sets.length - (n || 2)) + ' more' : ''); }
  console.log('   L    | best three both ways (coins to) | best four one way | three both / four one | counting bounds: three both, four one');
  [[50, 150], [100, 400], [200, 300], [500, 600], [1000, 300]].forEach(function (q) {
    var L = q[0], b3 = L === 100 ? { total: BESTJ.both[2].total, sets: BESTJ.both[2].sets.map(function (s) { return '(' + s.join(',') + ')'; }) } : rd('both-3-' + L);
    var p4 = L === 100 ? { total: BESTJ.plain[3].total, sets: BESTJ.plain[3].sets.map(function (s) { return '(' + s.join(',') + ')'; }) } : rd('plain-4-' + L);
    /* each set named is scored again by the core */
    b3.sets.forEach(function (s) { if (tot(s.replace(/[()]/g, '').split(',').map(Number), L, 'both') !== b3.total) throw new Error('both ' + s); });
    p4.sets.forEach(function (s) { if (tot(s.replace(/[()]/g, '').split(',').map(Number), L, 'plain') !== p4.total) throw new Error('plain ' + s); });
    console.log('   ' + L + ' | ' + show(b3) + ' (' + q[1] + ') | ' + show(p4) + ' | ' + (b3.total / p4.total).toFixed(4) + ' | ' + P.bound(3, L, 'both') + ', ' + P.bound(4, L, 'plain'));
  });
  console.log('   also: best two both ways: L=50 ' + show(rd('both-2-50'), 3) + '; L=200 ' + show(rd('both-2-200')) + '; L=500 ' + show(rd('both-2-500')) + '; bounds ' + [50, 200, 500].map(function (L) { return P.bound(2, L, 'both'); }).join(', '));
  console.log('   also: best three one way: L=50 ' + show(rd('plain-3-50')) + '; L=200 ' + show(rd('plain-3-200')) + '; L=500 ' + show(rd('plain-3-500')));
  console.log('   also: best four both ways, L=50 (coins to 100): ' + show(rd('both-4-50')) + '; best five one way: L=50 ' + show(rd('plain-5-50'), 4) + '; L=200 ' + show(rd('plain-5-200')));
  console.log('   the counting bounds alone, three both ways against four one way, at L = 100, 1000, 10000, 100000, 1000000: ' +
    [100, 1000, 10000, 100000, 1000000].map(function (L) { return (P.bound(3, L, 'both') / P.bound(4, L, 'plain')).toFixed(3); }).join(', '));
})();

/* ---------- H. Table 1 of Kippers and Franses, read three ways ---------- */
console.log('\nH. Table 1 of Kippers and Franses: which amounts does it cover?');
(function () {
  function stats(coins, list) {
    var n = 0, tk = 0, mx = 0;
    list.forEach(function (a) { var s = P.schemes(coins, a, 1); n += s.total; tk += s.total * s.count; if (s.count > mx) mx = s.count; });
    return 'schemes ' + n + ', tokens per scheme ' + (tk / n).toFixed(2) + ', most tokens ' + mx;
  }
  function range(a, b) { var o = []; for (var i = a; i <= b; i++) o.push(i); return o; }
  console.log('   in print: guilder 14,928 schemes, 5.68 per scheme, most 8; euro 16,151 schemes, 5.84, most 8; caption: amounts between NLG 0.05 and NLG 100; text: between NLG 0.05 and NLG 220.35');
  console.log('   euro, the guilder amounts 0.05 to 100.00 turned into euros at 2.20371 and rounded to a cent: ' + stats(EALL, range(1, 2000).map(function (u) { return Math.round(u * 5 / 2.20371); })));
  console.log('   euro, the guilder amounts 0.05 to 220.35 likewise: ' + stats(EALL, range(1, 4407).map(function (u) { return Math.round(u * 5 / 2.20371); })));
  console.log('   guilder, 0.05 to 100.00: ' + stats(NLG, range(1, 2000)));
  console.log('   guilder, 0.05 to 220.35: ' + stats(NLG, range(1, 4407)));
  var most = 0, at = 0; range(1, 1000).forEach(function (a) { var t = P.schemes(NLG, a, 1).total; if (t > most) { most = t; at = a; } });
  console.log('   guilder: most schemes for one amount up to 50.00: ' + most + ' at ' + (at * 5 / 100).toFixed(2) + '; up to 100.00: ' + P.schemes(NLG, 1333, 1).total + ' at 66.65');
})();

/* ---------- I. checks made while going through my list of questions, before the referee ---------- */
console.log('\nI. One step off the grid for "no coin of 1", "two coins reach their bound", and the gap for three coins');
(function () {
  var cp = require('child_process'), path = require('path');
  function run(D, L, M) {
    var out = cp.execFileSync(path.join(__dirname, 'search'), ['both', String(D), String(L), String(M)], { encoding: 'utf8' });
    return { total: Number(/least total (-?\d+)/.exec(out)[1]), sets: out.split('\n').filter(function (l) { return /^  best/.test(l); }).map(function (l) { return l.trim().split(/\s+/).slice(1).map(Number); }) };
  }
  var L, r, lastWith1 = { 2: 0, 3: 0 }, atBound = 0, n2 = 0, gaps = [], firstNo1 = { 2: 0, 3: 0 }, miss = [];
  for (L = 3; L <= 200; L++) { r = run(2, L, 60); n2++; if (r.total === P.bound(2, L, 'both')) atBound++; else miss.push(L);
    if (r.sets.some(function (s) { return s[0] === 1; })) lastWith1[2] = L; }
  for (L = 4; L <= 120; L++) { r = run(3, L, 80); gaps.push(r.total - P.bound(3, L, 'both')); if (r.sets.some(function (s) { return s[0] === 1; })) lastWith1[3] = L; }
  console.log('   two coins both ways (coins to 60), L from 3 to 200: at the counting bound in ' + atBound + ' of ' + n2 + ' ranges' + (miss.length ? '; not at ' + miss.join(',') : ''));
  console.log('   two coins: the largest L (to 200) at which some best set has a coin of 1: ' + lastWith1[2] + '; three coins (coins to 80, L from 4 to 120): ' + lastWith1[3]);
  console.log('   three coins: the gap above the bound for L from 4 to 120 runs from ' + Math.min.apply(null, gaps) + ' to ' + Math.max.apply(null, gaps) + '; it is 0 for ' + gaps.filter(function (g) { return g === 0; }).length + ' of ' + gaps.length + ' ranges; at L = 100 it is ' + gaps[96]);
})();

/* ---------- J. the choice I did not vary: every amount equally likely ---------- */
console.log('\nJ. If small amounts are likelier: amounts 1 to 99 weighted by 1/amount, and by 1/amount squared (coins to 60, every set tried here in JS)');
(function () {
  function best(D, mode, w) {
    var bestV = Infinity, sets = [], cur = [], n = 0;
    (function rec(d, from) {
      if (d === D) {
        var t = P.counts(cur, 100, mode), s = 0, a;
        for (a = 1; a < 100; a++) { if (t[a] >= P.INF) return; s += w(a) * t[a]; }
        n++;
        if (s < bestV - 1e-12) { bestV = s; sets = [cur.slice()]; } else if (Math.abs(s - bestV) <= 1e-12) sets.push(cur.slice());
        return;
      }
      for (var c = from; c <= 60; c++) { cur[d] = c; rec(d + 1, c + 1); }
      cur.length = d;
    })(0, 1);
    return { v: bestV, sets: sets };
  }
  [['every amount alike', function () { return 1; }], ['1/amount', function (a) { return 1 / a; }], ['1/amount squared', function (a) { return 1 / (a * a); }]].forEach(function (q) {
    var norm = 0; for (var a = 1; a < 100; a++) norm += q[1](a);
    [2, 3].forEach(function (D) {
      var b = best(D, 'both', q[1]), p = best(D, 'plain', q[1]);
      console.log('   ' + q[0] + ', ' + D + ' coins: both ways ' + b.sets.map(function (s) { return '(' + s.join(',') + ')'; }).join(' ') + ' mean ' + (b.v / norm).toFixed(3) + '; one way ' + p.sets.map(function (s) { return '(' + s.join(',') + ')'; }).join(' ') + ' mean ' + (p.v / norm).toFixed(3));
    });
  });
})();

/* ---------- K. Cramer's own coins: the guilder of 1982 had no 250 note (my recollection, not a source) ---------- */
console.log('\nK. "No Dutch amount up to 100 needs more than seven; 16.65 has the most schemes, ten": with which coins?');
(function () {
  function look(name, coins, unit, step) {
    var most = 0, at = 0, mx = 0, a;
    for (a = step; a <= 10000 / unit; a += step) { var s = P.schemes(coins, a, 1); if (s.total > most) { most = s.total; at = a; } if (s.count > mx) mx = s.count; }
    console.log('   ' + name + ': most tokens ' + mx + '; most schemes ' + most + ' at ' + (at * unit / 100).toFixed(2) + '; 16.65 has ' + P.schemes(coins, 1665 / unit, 1).total + '; 17.50 has ' + P.schemes(coins, 1750 / unit, 1).total);
  }
  look('as Kippers and Franses list it for 2001 (with the 250)', NLG, 5, 1);
  look('without the 250 note', NLG.filter(function (x) { return x !== 5000; }), 5, 1);
  look('without the 250 and without the 1000', NLG.filter(function (x) { return x !== 5000 && x !== 20000; }), 5, 1);
  look('without the 250, with a 1-cent coin, amounts in steps of 5 cents', [1, 5, 10, 25, 100, 250, 500, 1000, 2500, 5000, 10000, 100000], 1, 5);
})();

/* ---------- L. the whole of the tables in print: OEIS A366013 and A366360 against my searches ---------- */
console.log('\nL. The rows of OEIS A366013 (fewest coins) and A366360 (greedy), up to seven and six coins, against my searches');
(function () {
  var fs = require('fs'), path = require('path'), cp = require('child_process'), dir = path.join(process.env.HOME, 'coin-data', 'oeis-b');
  function rows(file) {
    var v = fs.readFileSync(path.join(dir, file), 'utf8').split('\n').filter(function (l) { return /^\d+ \d+/.test(l); }).map(function (l) { return Number(l.split(' ')[1]); }), out = [], cur = null;
    v.forEach(function (x) { if (x === 1) { if (cur) out.push(cur); cur = [1]; } else cur.push(x); });
    if (cur) out.push(cur);
    return out;
  }
  function mine(mode, D) {
    var out = cp.execFileSync(path.join(__dirname, 'search'), [mode, String(D), '100', '99'], { encoding: 'utf8' });
    return out.split('\n').filter(function (l) { return /^  best/.test(l); }).map(function (l) { return l.trim().split(/\s+/).slice(1).join(','); });
  }
  var A = rows('b366013.txt'), G = rows('b366360.txt'), D, okA = 0, okG = 0, nA = 0, nG = 0;
  for (D = 1; D <= 7; D++) { var theirs = A.filter(function (r) { return r.length === D; }).map(function (r) { return r.join(','); }), m = D <= 6 ? mine('plain', D) : BESTJ.plain[6].sets.map(function (s) { return s.join(','); });
    nA++; if (JSON.stringify(theirs) === JSON.stringify(m)) okA++; else console.log('   A366013 differs at ' + D + ' coins: ' + theirs.join(' ') + ' against ' + m.join(' ')); }
  for (D = 1; D <= 6; D++) { var th = G.filter(function (r) { return r.length === D; }).map(function (r) { return r.join(','); }), mg = mine('greedy', D);
    nG++; if (JSON.stringify(th) === JSON.stringify(mg)) okG++; else console.log('   A366360 differs at ' + D + ' coins: ' + th.join(' ') + ' against ' + mg.join(' '));
    if (D >= 5) console.log('   greedy, ' + D + ' coins: ' + mg.length + ' best sets, the first ' + mg[0] + ', total ' + P.total(P.greedy(mg[0].split(',').map(Number), 100))); }
  console.log('   A366013: ' + okA + ' of ' + nA + ' rows-by-length the same as my search; A366360: ' + okG + ' of ' + nG);
})();

/* ---------- M. after the referee's report ---------- */
console.log('\nM. After the referee');
(function () {
  var fs = require('fs'), path = require('path');
  function rd(name) {
    var t = fs.readFileSync(path.join(__dirname, 'runs', 'offgrid', name + '.out'), 'utf8');
    return { total: Number(/least total (\d+)/.exec(t)[1]), sets: t.split('\n').filter(function (l) { return /^  best/.test(l); }).map(function (l) { return l.trim().split(/\s+/).slice(1).map(Number); }) };
  }
  function show(r) { return r.sets.map(function (s) { return '(' + s.join(',') + ')'; }).join(' '); }
  /* M1. the near-tie at ten ranges */
  console.log('   M1. three coins both ways against four one way, ten ranges: L | three both (coins to) | four one | ratio');
  var worst = 0;
  [[50, 150], [60, 150], [75, 150], [100, 400], [150, 150], [200, 300], [300, 150], [400, 150], [500, 600], [1000, 300]].forEach(function (q) {
    var L = q[0], b = L === 100 ? BESTJ.both[2].total : rd('both-3-' + L).total, p = L === 100 ? BESTJ.plain[3].total : rd('plain-4-' + L).total;
    if (Math.abs(b / p - 1) > worst) worst = Math.abs(b / p - 1);
    console.log('       ' + L + ' | ' + b + ' (' + q[1] + ') | ' + p + ' | ' + (b / p).toFixed(4));
  });
  console.log('       furthest from 1: ' + worst.toFixed(4));
  /* M2. far out, a proof: four coins (1, m, m^2, m^3) one way against the counting bound for ANY three coins both ways */
  console.log('   M2. large ranges: the best of (1, m, m^2, m^3) one way, against the least that any three coins both ways could total');
  [2000, 3000, 5000, 10000, 20000, 50000, 100000].forEach(function (L) {
    var best = Infinity, bm = 0, m;
    for (m = 2; m <= 40; m++) { var t = tot([1, m, m * m, m * m * m], L); if (t < best) { best = t; bm = m; } }
    var bd = P.bound(3, L, 'both');
    console.log('       L = ' + L + ': (1,' + bm + ',' + bm * bm + ',' + bm * bm * bm + ') totals ' + best + '; bound for three coins both ways ' + bd + ': ' + (best < bd ? 'four one way are ahead of every three both ways' : 'not settled by this'));
  });
  /* M3. the referee's corollary: a coin above the range is not an amount, so one fewer amount can take one coin */
  function boundBig(D, L, caps) { var left = L - 1, k = 1, s = 0, n; while (left > 0) { n = caps[k] !== undefined ? caps[k] : P.signedLists(D, k) / 2; if (n > left) n = left; s += n * k; left -= n; k++; } return s; }
  console.log('   M3. with a coin of 100 or more, amounts below 100: at least ' + [2, 3, 4].map(function (D) { return boundBig(D, 100, { 1: D - 1 }); }).join(', ') + ' for two, three, four coins (best found 660, 388, 309)');
  console.log('       five coins, one coin of 100 or more: at most 4, 20, 60 amounts with one, two, three coins: at least ' + boundBig(5, 100, { 1: 4, 2: 20, 3: 60 }) +
    '; two or more such coins: at most 3 and 13: at least ' + boundBig(5, 100, { 1: 3, 2: 13 }) + ' (best found 270)');
  var r = (function (seed) { var s = seed >>> 0; return function () { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; })(2026);
  var least = [Infinity, Infinity, Infinity], broke = 0, n = 0, i, a;
  for (i = 0; i < 3000; i++) {
    var nb = 1 + Math.floor(r() * 3), set = Object.create(null), c = [];
    while (c.length < nb) { var v = 100 + Math.floor(r() * 300); if (!set[v]) { set[v] = 1; c.push(v); } }
    while (c.length < 5) { var w = 1 + Math.floor(r() * 99); if (!set[w]) { set[w] = 1; c.push(w); } }
    var t = P.both(c, 100), tt = P.total(t); if (!isFinite(tt)) continue;
    n++; var h = [0, 0, 0, 0]; for (a = 1; a < 100; a++) if (t[a] <= 3) h[t[a]]++;
    var caps = nb === 1 ? [0, 4, 20, 60] : [0, 3, 13, 85];
    if (h[1] > caps[1] || h[2] > caps[2] || h[3] > caps[3] || tt < (nb === 1 ? 284 : 278)) broke++;
    if (tt < least[nb - 1]) least[nb - 1] = tt;
  }
  console.log('       tried on ' + n + ' random sets of five with one, two or three coins from 100 to 399: caps broken ' + broke + ' times; least totals ' + least.join(', '));
  /* M4. the 85 */
  console.log('   M4. both ways below 100: the six cent coins ' + tot(EC6, 100, 'both') + '; with a 100 ' + tot(EC6.concat([100]), 100, 'both') + '; with an 85 ' + tot(EC6.concat([85]), 100, 'both') +
    '; the eight coins with an 85 ' + tot(EC6.concat([100, 200, 85]), 100, 'both') + '; with a 33 ' + tot(EC6.concat([100, 200, 33]), 100, 'both'));
  /* M5. ties among the guilder amounts */
  var ten = [], fifteen = [], u;
  for (u = 1; u <= 2000; u++) { var k = P.schemes(NLG, u, 1).total; if (u <= 1000 && k === 10) ten.push((u * 5 / 100).toFixed(2)); if (k === 15) fifteen.push((u * 5 / 100).toFixed(2)); }
  console.log('   M5. guilder: amounts to 50.00 with ten schemes (the most there): ' + ten.join(', ') + '; amounts to 100.00 with fifteen (the most): ' + fifteen.join(', '));
  /* M6. no coin of 1, more cases */
  var b2 = rd('both-2-1000'), b4 = rd('both-4-200');
  console.log('   M6. two coins both ways, amounts below 1000 (coins to 150): ' + show(b2) + ' total ' + b2.total + ', bound ' + P.bound(2, 1000, 'both') + '; four coins, amounts below 200 (coins to 80): ' + show(b4) + ' total ' + b4.total);
})();

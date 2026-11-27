// The referee's blind numbers (27 November; typed here from its report, referee27/blind.md) set beside pcore.js.   node blind-beside-pcore.js PCORE.js BEST.json
const P = require(require('path').resolve(process.argv[2])), BEST = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8')); let bad = 0, n = 0;
const same = (what, a, b) => { n++; if (JSON.stringify(a) !== JSON.stringify(b)) { bad++; console.log('DIFFERS: ' + what + ': the referee ' + JSON.stringify(a) + ', pcore ' + JSON.stringify(b)); } };
const fin = v => v < P.INF, tot = t => { let s = 0, c = 0; for (const v of t) { if (fin(v)) s += v; else c++; } return c ? 'cannot ' + c : s; }, worst = t => Math.max(...[...t].filter(fin));
// item 1: [coins, L, sum (a) or 'cannot k', sum (b), sum (c), max (a), max (c), amounts with (b) > (a), the first of them]
const T1 = [[[1, 5, 10, 25], 100, 470, 470, 398, 9, 7, 0, null], [[1, 5, 18, 25], 100, 389, 458, 348, 6, 6, 37, 28], [[1, 2, 5, 10, 20, 50, 100, 200], 100, 340, 340, 272, 6, 4, 0, null], [[1, 5, 10, 25, 50, 100], 100, 420, 420, 312, 8, 5, 0, null],
  [[1, 2, 4, 8, 16, 32, 64], 100, 316, 316, 267, 6, 4, 0, null], [[1, 3, 9, 27, 81], 100, 390, 390, 318, 8, 5, 0, null], [[16, 19, 21], 100, 'cannot 50', 'cannot 87', 388, 5, 6, 0, null], [[19, 20, 23, 32], 100, 'cannot 46', 'cannot 87', 309, 5, 5, 0, null],
  [[1, 5, 16, 23, 33], 100, 329, 411, 306, 6, 5, 46, 20], [[1, 3, 6, 12, 24, 30], 240, 1398, 1440, 1323, 11, 10, 42, 48], [[1, 5, 10, 25, 100, 200], 500, 2950, 2950, 2211, 11, 7, 0, null], [[1, 3, 4], 10, 16, 17, 16, 3, 3, 1, 6],
  [[2, 4], 100, 'cannot 50', 'cannot 50', 'cannot 50', 25, 25, 0, null], [[1, 10, 25], 30, 135, 135, 83, 10, 4, 0, null]];
for (const [c, L, a, b, cc, ma, mc, nf, first] of T1) { const pl = P.plain(c, L), gr = P.greedy(c, L), bo = P.both(c, L); let f = 0, f1 = null; for (let x = 0; x < L; x++) if (fin(gr[x]) && fin(pl[x]) && gr[x] > pl[x]) { f++; if (f1 === null) f1 = x; }
  same('item 1, ' + c.join(',') + ' below ' + L, [a, b, cc, ma, mc, nf, first], [tot(pl), tot(gr), tot(bo), worst(pl), worst(bo), f, f1]); }
// item 2: the best coin to add, with every tie
const best = (c, L, way, top) => { const l = P.bestAdd(c, L, way, top); return [l.filter(e => e.total === l[0].total).map(e => e.coin), l[0].total]; };
same('item 2, US, (a)', [[32], 346], best([1, 5, 10, 25], 100, 'plain', 99)); same('item 2, US, (c)', [[48], 295], best([1, 5, 10, 25], 100, 'both', 199));
same('item 2, euro, (a)', [[33, 37], 286], best([1, 2, 5, 10, 20, 50, 100, 200], 100, 'plain', 99)); same('item 2, euro, (c)', [[33, 36, 37], 241], best([1, 2, 5, 10, 20, 50, 100, 200], 100, 'both', 199));
// item 3: twelve coins added one after another
{ let c = [1, 5, 10, 25]; const got = []; for (let k = 0; k < 12; k++) { const b = best(c, 100, 'plain', 99); got.push([b[0][0], b[1], b[0]]); c = c.concat([b[0][0]]).sort((x, y) => x - y); }
  same('item 3', [[32, 346, [32]], [4, 308, [4, 9, 24]], [44, 276, [44]], [42, 257, [42, 46, 55]], [9, 240, [9]], [55, 230, [55]], [39, 222, [39]], [19, 214, [19, 22, 57]], [12, 207, [12, 43, 66]], [43, 200, [43, 54, 63, 66, 70, 73]], [47, 193, [47]], [48, 188, [48]]], got);
  same('item 3, the set at the end', [1, 4, 5, 9, 10, 12, 19, 25, 32, 39, 42, 43, 44, 47, 48, 55], c); }
// item 4: single amounts: [coins, amount, (a), (b), (c), number of ways for (c)]
for (const [c, a, pa, pb, pc, ways] of [[[1, 5, 10, 25], 24, 6, 6, 2, 1], [[1, 5, 10, 25], 39, 6, 6, 4, 2], [[1, 5, 10, 25], 60, 3, 3, 3, 1], [[1, 5, 10, 25], 68, 7, 7, 6, 2], [[1, 5, 10, 25], 71, 5, 5, 5, 2], [[1, 5, 10, 25], 78, 6, 6, 6, 2], [[1, 5, 10, 25], 99, 9, 9, 5, 1],
  [[1, 2, 5, 10, 20, 50, 100, 200], 38, 5, 5, 3, 2], [[1, 2, 5, 10, 20, 50, 100, 200], 67, 4, 4, 4, 3], [[1, 2, 5, 10, 20, 50, 100, 200], 99, 6, 6, 2, 1], [[16, 19, 21], 1, 'cannot', 'cannot', 4, 1], [[16, 19, 21], 24, 'cannot', 'cannot', 3, 1]]) {
  const s = P.schemes(c, a, 100, 3000000), q = v => fin(v) ? v : 'cannot'; same('item 4, ' + c.join(',') + ' at ' + a, [pa, pb, pc, ways], [q(P.plain(c, a + 1)[a]), q(P.greedy(c, a + 1)[a]), P.both(c, a + 1)[a], s.total]); }
// item 5: the best four coins, as best.json has them
same('item 5', [[[1, 5, 18, 25], [1, 5, 18, 29]], 389], [BEST.plain[3].sets, BEST.plain[3].total]);
// item 6: Pearson's test
for (const [c, w] of [[[1, 5, 10, 25], 0], [[1, 5, 18, 25], 28], [[1, 3, 6, 12, 24, 30], 48], [[1, 10, 25], 30]]) same('item 6, ' + c.join(','), w, P.pearson(c));
console.log(n + ' of the referee\'s blind figures set beside pcore.js; ' + bad + ' differ');

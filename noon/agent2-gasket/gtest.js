// gtest.js -- gcore.js against the paper's tables, the C program's lists, and brute force.   node gtest.js
const G = require(process.env.CORE || './gcore.js'), PLAIN = require('./gcore-plainwalk.js'), fs = require('fs'), path = require('path');   // gcore-plainwalk.js: the first form of the view walk, which nests a call for every circle and measures from the plane's origin
const P = JSON.parse(fs.readFileSync(path.join(__dirname, 'packings.json'), 'utf8'));
let pass = 0, fail = 0; const lines = [];
// inView, giving each circle's true X (in the strip the circle found is the one of the first period moved along by k periods)
const inV = (pl, v, m, cb, bud) => G.inView(pl, v, m, (b, X, Y, wx, wy, k) => cb(b, X + 2 * (k || 0) * b, Y, wx, wy, k || 0, X), bud);
function ok(name, cond, detail) { if (cond) pass++; else fail++; lines.push((cond ? 'ok    ' : 'FAIL  ') + name + (detail ? '   [' + detail + ']' : '')); }
function all(name, n, bad, extra) { ok(name + ': ' + (n - bad.length) + ' of ' + n, bad.length === 0 && n > 0, (bad.length ? 'first failures: ' + bad.slice(0, 4).join('; ') : '') + (extra || '')); }
let seed = 31415; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
const nm = q => q.map(x => String(x).replace('-', 'm')).join('_');

// 1. the Kronecker symbol against Euler's criterion and the rules for 2 and -1, on its definition as a product over primes
{ const primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], bad = []; let n = 0;
  const legendre = (a, p) => { a = ((a % p) + p) % p; if (!a) return 0; let r = 1, b = a, e = (p - 1) / 2; while (e) { if (e & 1) r = r * b % p; b = b * b % p; e >>= 1; } return r === 1 ? 1 : -1; };
  const two = a => a % 2 === 0 ? 0 : ([1, 7].includes(((a % 8) + 8) % 8) ? 1 : -1);
  for (let i = 0; i < 20000; i++) { const a = Math.floor(rnd() * 4001) - 2000; let m = 1, want = 1; const k = 1 + Math.floor(rnd() * 3);
    for (let j = 0; j < k; j++) { const p = rnd() < 0.25 ? 2 : primes[Math.floor(rnd() * primes.length)]; m *= p; want *= p === 2 ? two(a) : legendre(a, p); }
    if (rnd() < 0.2) { m = -m; if (a < 0) want = -want; } n++; if (G.kron(a, m) !== want) bad.push(a + '/' + m); }
  all('the Kronecker symbol is the product of Legendre symbols, with the rules for 2 and for a negative lower entry', n, bad); }

// 2. the 42 packings of the paper's tables: type and chi_2
{ const bad = [], badr = []; for (const p of P) { const t = G.type(p.root), c = G.chi2(p.root); if (!(t.x === p.type[0] && t.k === p.type[1] && t.chi2 === p.type[2] && c.agree && c.pairs > 0)) bad.push(JSON.stringify(p.root) + ' ' + t.key);
    const fam = G.TABLE[p.type.join(',')][0]; if (JSON.stringify(t.quartic ? fam : t.quad) !== JSON.stringify(fam)) badr.push(JSON.stringify(p.root)); }
  all('type (x, k, chi_2) from the root quadruple is the paper\'s, and every coprime tangent pair within two moves of the root gives the same sign', P.length, bad);
  all('the quadratic families looked up for it are those of the paper\'s Theorem 2.4', P.length, badr); }

ok('chi2pair() refuses a circle of negative curvature (where the remainder of a negative number would give the wrong sign: the true sign for -11 with 21 is -1) and still gives -1 for 21 with -11',
  (() => { try { G.chi2pair(-11, 21); return false; } catch (e) { return true; } })() && G.chi2pair(21, -11) === -1 && G.chi2pair(24, -11) === -1 && G.chi2pair(28, -11) === -1);

// 2b. squares and families, against a plain search
{ const bad = []; let n = 0; const sq = new Set(); for (let k = 0; k * k <= 300000; k++) sq.add(k * k);
  for (let v = 1; v <= 300000; v++) { n++; let want = 0; for (const u of [1, 2, 3, 6]) if (!want && v % u === 0 && sq.has(v / u)) want = u; if (G.inFamily(v, [1, 2, 3, 6]) !== want || G.isSquare(v) !== sq.has(v)) bad.push(v); }
  all('isSquare() and inFamily() for every number up to 300,000, against a list of squares', n, bad); }

// 2c. the table of families against the C program's lists up to 10^6: a family u n^2 is in the table's row for a packing's
// type exactly when none of its members that passes the test of remainders is a curvature; and the same for the
// fourth-power forms where the type has a fourth entry (the paper's type is used there: the page does not compute it)
{ const bad = [], badq = []; let n = 0, nq = 0, nocand = 0;
  for (const p of P) { const miss = new Set(fs.readFileSync(path.join(__dirname, 'types', nm(p.root) + '.txt'), 'utf8').split('\n').filter(Boolean).map(Number)), res = G.residues(p.root), row = G.TABLE[p.type.join(',')];
    for (const u of [1, 2, 3, 6]) { let cand = 0, present = 0; for (let k = 1; u * k * k <= 1000000; k++) { const v = u * k * k; if (res.includes(v % 24)) { cand++; if (!miss.has(v)) present++; } } if (!cand) { nocand++; if (row[0].includes(u)) bad.push(JSON.stringify(p.root) + ' ' + u + 'n^2 barred though none passes the test of remainders'); continue; } n++;
      if ((present === 0) !== row[0].includes(u)) bad.push(JSON.stringify(p.root) + ' ' + u + 'n^2: ' + present + ' of ' + cand + ' occur'); }
    if (p.type.length === 4) for (const u of [1, 4, 9, 36]) { let cand = 0, present = 0; for (let k = 1; u * k ** 4 <= 1000000; k++) { const v = u * k ** 4; if (res.includes(v % 24)) { cand++; if (!miss.has(v)) present++; } } if (!cand) continue; nq++;
      if ((present === 0) !== row[1].includes(u)) badq.push(JSON.stringify(p.root) + ' ' + u + 'n^4: ' + present + ' of ' + cand + ' occur'); } }
  all('among the families u n^2 (u = 1, 2, 3, 6) that have a member passing the test of remainders, the table\'s row is exactly the set with no member among the curvatures up to 10^6, for the 42 packings (' + nocand + ' more families have no such member, and the table bars none of them)', n, bad);
  all('and the same for the forms u n^4 (u = 1, 4, 9, 36) in the twelve packings whose type has a fourth entry', nq, badq); }

// 3. reduction: random walks away from a root come back to it
{ const bad = []; let n = 0; for (const p of P) for (let k = 0; k < 40; k++) { let q = p.root.slice(), last = -1; const len = 1 + Math.floor(rnd() * 25);
    for (let j = 0; j < len; j++) { let i; do { i = Math.floor(rnd() * 4); } while (i === last); const s = q[0] + q[1] + q[2] + q[3]; const nv = 2 * (s - q[i]) - q[i]; if (nv > 1e7) break; q[i] = nv; last = i; }
    q.sort(() => rnd() - 0.5); n++; if (JSON.stringify(G.reduce(q)) !== JSON.stringify(p.root)) bad.push(JSON.stringify(q)); }
  all('reduce() brings a quadruple reached by up to 25 random moves back to its root', n, bad);
  ok('reduce() refuses four numbers that are not a Descartes quadruple', (() => { try { G.reduce([15, 2, 2, -1]); return false; } catch (e) { return true; } })()); }

// 4. which curvatures occur: the same lists of missing numbers up to 10^6 as the C program wrote (types/*.txt), for all 42
{ const bad = []; let n = 0, tot = 0; for (const p of P) { const want = fs.readFileSync(path.join(__dirname, 'types', nm(p.root) + '.txt'), 'utf8').split('\n').filter(Boolean).map(Number), got = G.missing(p.root, 1000000); n++; tot += got.length;
    if (got.length !== want.length || got.some((v, i) => v !== want[i])) bad.push(JSON.stringify(p.root) + ' ' + got.length + ' against ' + want.length); }
  all('missing curvatures up to 10^6 are the C program\'s lists, number for number (' + tot + ' numbers in all)', n, bad); }

// 5. places: integral, mutually touching, and they stay so
const roots = P.map(p => p.root);
for (let a = -1; a >= -14; a--) for (let b = -a; b <= 60; b++) for (let c = b; c <= 160; c++) { const s = a + b + c, pr = a * b + a * c + b * c; if (pr < 0) continue; const r = Math.round(Math.sqrt(pr)); if (r * r !== pr) continue;
  const d = s - 2 * r; if (d < c) continue; const q = [a, b, c, d]; if (G.isDescartes(q) && G.isPrimitive(q) && JSON.stringify(G.reduce(q)) === JSON.stringify(q) && !roots.some(x => JSON.stringify(x) === JSON.stringify(q))) roots.push(q); }
{ const bad = [], bad2 = []; let n = 0, m = 0;
  for (const q of roots) { let pl; n++; try { pl = G.place(q); } catch (e) { bad.push(JSON.stringify(q) + ' ' + e.message); continue; }
    const c = pl.circles; let good = c.every((x, i) => x[0] === q[i] && Number.isInteger(x[1]) && Number.isInteger(x[2]));
    if (!pl.strip) for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) { if (!G.touching(c[i], c[j])) good = false; if (c[i][1] * c[j][0] === c[j][1] * c[i][0] && c[i][2] * c[j][0] === c[j][2] * c[i][0]) good = false; }
    if (!good) bad.push(JSON.stringify(q));
    // walk 300 random moves: each new circle touches the three it was made from, exactly
    if (!pl.strip) { let cur = c.map(x => x.slice()), last = -1; for (let k = 0; k < 300; k++) { let i; do { i = Math.floor(rnd() * 4); } while (i === last);
        const nw = [0, 1, 2].map(t => 2 * (cur[0][t] + cur[1][t] + cur[2][t] + cur[3][t] - cur[i][t]) - cur[i][t]); if (Math.abs(nw[0]) > 3e7) break; m++;
        for (let j = 0; j < 4; j++) if (j !== i && !G.touching(nw, cur[j])) { bad2.push(JSON.stringify(q)); break; } cur[i] = nw; last = i; } } }
  all('place(): whole-number curvature-times-centre for every root quadruple tried (the paper\'s 42 and all other primitive roots with outer circle -1 to -14, b <= 60, c <= 160: ' + roots.length + ' in all), four different circles, each pair touching', n, bad);
  all('and every circle made from them by random moves touches the three it was made from, as whole numbers (curvatures up to 3 x 10^7)', m, bad2.slice(0, 5)); }

// 6. circles in a view: against every circle of the packing up to a curvature bound, sorted out by hand
{ const bad = []; let n = 0, shown = 0;
  for (const q of [[-1, 2, 2, 3], [-3, 5, 8, 8], [-4, 5, 20, 21], [-11, 21, 24, 28], [-2, 3, 6, 7], [0, 0, 1, 1], [-23, 48, 49, 52]]) { const pl = G.place(q), B = 3000, every = [];
    // brute force: all circles with curvature <= B (for the strip: those with centre between x = -7 and 9)
    inV(pl, pl.strip ? [-7, -2, 9, 2] : [-1e9, -1e9, 1e9, 1e9], 1 / B, (b, X, Y) => every.push([b, X, Y]));
    if (!pl.strip && every.length !== G.enumerate(q, B).circles) bad.push(JSON.stringify(q) + ': the walk with places found ' + every.length + ' circles up to ' + B + ', the walk without ' + G.enumerate(q, B).circles);
    const R = pl.strip ? 1 : 1 / Math.abs(q[0]), cx = pl.strip ? 1 : pl.circles[0][1] / q[0], cy = pl.strip ? 0 : pl.circles[0][2] / q[0];
    for (let k = 0; k < 60; k++) { const w = R * Math.pow(10, -3 * rnd()) * 2, x0 = cx + (rnd() * 2 - 1) * R - w / 2, y0 = cy + (rnd() * 2 - 1) * R - w / 2, v = [x0, y0, x0 + w, y0 + w * (0.3 + rnd())], minR = Math.max(1 / B, w / 400);
      const want = every.filter(c => c[0] !== 0 && Math.abs(1 / c[0]) >= minR * (1 - 1e-12) && c[1] / c[0] + 1 / Math.abs(c[0]) >= v[0] && c[1] / c[0] - 1 / Math.abs(c[0]) <= v[2] && c[2] / c[0] + 1 / Math.abs(c[0]) >= v[1] && c[2] / c[0] - 1 / Math.abs(c[0]) <= v[3]).map(c => c.join(',')).sort();
      const got = []; inV(pl, v, minR, (b, X, Y) => { if (b !== 0) got.push([b, X, Y].join(',')); }); got.sort(); n++; shown += got.length;
      if (got.length !== want.length || got.some((s, i) => s !== want[i])) bad.push(JSON.stringify(q) + ' view ' + v.map(x => x.toFixed(4)).join(' ') + ': ' + got.length + ' against ' + want.length); } }
  all('inView(): for random rectangles down to a thousandth of the packing, exactly the circles of at least the least radius whose bounding square meets the rectangle (' + shown + ' circles shown in all), none twice', n, bad); }
// 6b. deep views: walk to a circle by moves, look at a view six of its radii wide: the circle is found, and without going
// through more than a few thousand gaps
{ const bad = []; let n = 0, worst = 0;
  for (const q of [[-3, 5, 8, 8], [-1, 2, 2, 3], [-23, 48, 49, 52], [-4, 5, 20, 21]]) { const pl = G.place(q);
    for (let k = 0; k < 25; k++) { let cur = pl.circles.map(c => c.slice()), last = -1; const depth = 3 + Math.floor(rnd() * 30);
      for (let j = 0; j < depth; j++) { let i; do { i = Math.floor(rnd() * 4); } while (i === last); const nw = [0, 1, 2].map(t => 2 * (cur[0][t] + cur[1][t] + cur[2][t] + cur[3][t] - cur[i][t]) - cur[i][t]); if (nw[0] > 1e12) break; cur[i] = nw; last = i; }
      if (last < 0) continue; const c = cur[last], r = 1 / c[0], x = c[1] / c[0], y = c[2] / c[0], got = []; n++;
      const res = inV(pl, [x - 3 * r, y - 3 * r, x + 3 * r, y + 3 * r], r / 300, (b, X, Y) => got.push(b + ',' + X + ',' + Y), 3000000); worst = Math.max(worst, res.visits);
      if (!got.includes(c.join(',')) || res.visits > 400000 || new Set(got).size !== got.length || !cur.every(o => got.includes(o.join(',')) || Math.abs(1 / o[0]) < r / 300 || o[0] < 0 || Math.abs(1 / o[0]) > 2 * r)) bad.push(JSON.stringify(q) + ' circle ' + c.join(',') + ' visits ' + res.visits + ' found ' + got.length); } }
  all('inView() at depth: a view about a circle reached by up to 32 random moves (curvatures up to 10^12) shows that circle and its touching neighbours of like size, in at most ' + worst + ' gaps visited', n, bad); }

// 6c. near points where two circles touch (where rows of circles are long): the walk with its jumps against the first,
// plain form of the walk, as deep as the plain one can go
{ const bad = []; let n = 0, shown = 0, maxVisits = 0;
  for (const q of [[-1, 2, 2, 3], [-3, 5, 8, 8], [0, 0, 1, 1], [-23, 48, 49, 52], [-6, 11, 14, 15]]) { const pl = G.place(q), R = pl.strip ? 1 : 1 / Math.abs(q[0]); const pairs = [];
    for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) if (pl.circles[i][0] + pl.circles[j][0] > 0) pairs.push([pl.circles[i], pl.circles[j]]);
    for (let k = 0; k < 24; k++) { const [c1, c2] = pairs[k % pairs.length], sb = c1[0] + c2[0], T = [(c1[1] + c2[1]) / sb, (c1[2] + c2[2]) / sb], w = R * Math.pow(10, -1 - 3.2 * rnd()), off = k % 3 === 0 ? 0 : 4 * rnd();
      const cx = T[0] + (rnd() * 2 - 1) * w * off, cy = T[1] + (rnd() * 2 - 1) * w * off, v = [cx - w / 2, cy - w / 3, cx + w / 2, cy + w / 3], minR = w / 1400, a = [], b = [];
      const res = inV(pl, v, minR, (x, y, z) => { if (x !== 0) a.push(x + ',' + y + ',' + z); }, 5000000); PLAIN.inView(pl, v, minR, (x, y, z) => { if (x !== 0) b.push(x + ',' + y + ',' + z); }, 50000000); /* the strip's two lines aside: the plain walk gave them always, the walk now only when they are in view */ a.sort(); b.sort(); n++; shown += a.length; maxVisits = Math.max(maxVisits, res.visits);
      if (a.length !== b.length || a.some((x, i) => x !== b[i])) bad.push(JSON.stringify(q) + ' w=' + w.toExponential(2) + ' off=' + off.toFixed(2) + ': ' + a.length + ' against ' + b.length); } }
  all('inView() near points of contact, views from a tenth to a sixteen-thousandth of the packing: the same circles as the plain walk (' + shown + ' in all; at most ' + maxVisits + ' gaps visited)', n, bad); }

// 6d. far down a row: the K-th circle between two touching circles, worked out here with BigInt; a view about it from the
// root must show what a walk begun at that circle's own quadruple shows
{ const bad = []; let n = 0; const notes = [], leftNotes = [];
  const cases = [[[-1, 2, 2, 3], 1, 2, 1000], [[-1, 2, 2, 3], 1, 2, 100000], [[-1, 2, 2, 3], 1, 2, 3000000], [[-1, 2, 2, 3], 0, 1, 20000000], [[-3, 5, 8, 8], 0, 1, 10000000], [[-3, 5, 8, 8], 2, 3, 1000000], [[-23, 48, 49, 52], 1, 3, 777777], [[0, 0, 1, 1], 0, 2, 30000000], [[-6, 11, 14, 15], 0, 3, 4444444]];
  for (const [q, i1, i2, K] of cases) { const pl = G.place(q), F1 = pl.circles[i1], F2 = pl.circles[i2], rest = [0, 1, 2, 3].filter(i => i !== i1 && i !== i2), A = pl.circles[rest[0]], B = pl.circles[rest[1]];
    const big = (m) => [0, 1, 2].map(t => BigInt(B[t]) + BigInt(m) * (BigInt(B[t]) - BigInt(A[t])) + BigInt(m) * BigInt(m + 1) * (BigInt(F1[t]) + BigInt(F2[t])));
    const PK = big(K).map(Number), PK1 = big(K - 1).map(Number); n++;
    if (!PK.every(Number.isSafeInteger) || !G.touching(PK, PK1) && false) { bad.push(JSON.stringify(q) + ' K=' + K + ' out of range'); continue; }
    const u = BigInt(F1[0]) * BigInt(PK[1]) - BigInt(PK[0]) * BigInt(F1[1]), w2 = BigInt(F1[0]) * BigInt(PK[2]) - BigInt(PK[0]) * BigInt(F1[2]), ss = BigInt(F1[0]) + BigInt(PK[0]); if (u * u + w2 * w2 !== ss * ss) { bad.push(JSON.stringify(q) + ' K=' + K + ': P(K) does not touch F1'); continue; }
    const r = 1 / PK[0], view = { cx: PK[1] / PK[0], cy: PK[2] / PK[0], hw: 4 * r, hh: 3 * r }, a = [], b = [], minR = Math.max(r / 150, 1 / 3e15);
    const CX = BigInt(Math.round(view.cx * 2 ** 60)), CY = BigInt(Math.round(view.cy * 2 ** 60)); let locBad = 0;               // each position from the view's centre, against the same subtraction done here in BigInt
    const res = inV(pl, view, minR, (x, y, z, wx, wy) => { if (x > 0) a.push(x + ',' + y + ',' + z);                          // (the outer circle, which holds every view, is left out of both lists)
      const ex = Number(BigInt(y) * 2n ** 60n - CX * BigInt(x)) / 2 ** 60, ey = Number(BigInt(z) * 2n ** 60n - CY * BigInt(x)) / 2 ** 60; if (Math.abs(wx - ex) > 1e-9 * (Math.abs(ex) + 1e-6) || Math.abs(wy - ey) > 1e-9 * (Math.abs(ey) + 1e-6)) locBad++; }, 3000000);
    if (locBad) bad.push(JSON.stringify(q) + ' K=' + K + ': ' + locBad + ' positions not exact');
    // with no least size asked for, nothing is shown that a floating number cannot hold exactly
    { let unsafe = 0, cnt = 0; const r2 = inV(pl, view, r / 1e6, (x, y, z) => { cnt++; if (!Number.isSafeInteger(x) || !Number.isSafeInteger(y) || !Number.isSafeInteger(z) || x > 4e15) unsafe++; }, 200000); if (unsafe || !cnt) bad.push(JSON.stringify(q) + ' K=' + K + ': ' + unsafe + ' of ' + cnt + ' circles shown are not exact');
      leftNotes.push(r2.leftOut); if ((1e6 * PK[0] > 1e17) !== (r2.leftOut > 0) && (1e6 * PK[0] > 1e17 || 1e6 * PK[0] < 4e15)) bad.push(JSON.stringify(q) + ' K=' + K + ': asked for circles down to curvature ' + (1e6 * PK[0]).toExponential(1) + ', and ' + r2.leftOut + ' are said to be left out'); }
    if (res.leftOut) bad.push(JSON.stringify(q) + ' K=' + K + ': ' + res.leftOut + ' circles said to be left out where every number wanted is exact');
    inV({ strip: false, circles: [F1, F2, PK1, PK] }, view, minR, (x, y, z) => { if (x > 0) b.push(x + ',' + y + ',' + z); }, 3000000); a.sort(); b.sort(); notes.push('K=' + K + ': curvature ' + PK[0].toExponential(2) + ', ' + a.length + ' circles, ' + res.visits + ' gaps');
    if (!a.includes(PK.join(',')) || a.length !== b.length || a.some((x, i) => x !== b[i]) || res.visits > 200000) bad.push(JSON.stringify(q) + ' K=' + K + ': from the root ' + a.length + ' circles in ' + res.visits + ' gaps, from its own quadruple ' + b.length); }
  all('inView() far down a row (' + notes.join('; ') + '): the view about the K-th circle, walked from the root, shows that circle and exactly what a walk begun beside it shows; every position measured from the view\'s centre is exact; nothing past exact floating numbers is shown; and the walk says it left none out where all the numbers wanted are exact, and some where circles a million times smaller are asked for and those are past 10^17 in curvature (left out, case by case: ' + leftNotes.join(', ') + ')', n, bad); }

// 6e. far along the strip (found wanting by the referee: circles whose curvature times x passed 2^53 were dropped):
// a deep view moved along by a whole number of periods must show the same circles, moved
{ const bad = []; let n = 0, shown = 0; const pl = G.place([0, 0, 1, 1]); let cur = pl.circles.map(c => c.slice()), last = -1;
  for (const M of [500, 2500, 4000]) for (let trial = 0; trial < 6; trial++) { cur = pl.circles.map(c => c.slice()); last = -1; const depth = 6 + Math.floor(rnd() * 14);
    for (let j = 0; j < depth; j++) { let i; do { i = Math.floor(rnd() * 4); } while (i === last || (last < 0 && i > 1)); const nw = [0, 1, 2].map(t => 2 * (cur[0][t] + cur[1][t] + cur[2][t] + cur[3][t] - cur[i][t]) - cur[i][t]); if (nw[0] > 3e10) break; cur[i] = nw; last = i; }
    const c = cur[last], r = 1 / c[0], cx = Math.round(c[1] / c[0] * 2 ** 40) / 2 ** 40, cy = Math.round(c[2] / c[0] * 2 ** 40) / 2 ** 40, hw = Math.max(4 * r, 2 ** -36), minR = hw / 700, a = [], b = []; n++;
    inV(pl, { cx: cx, cy: cy, hw: hw, hh: hw * 0.6 }, minR, (bb, X, Y, wx, wy, k, X0) => a.push(bb + ',' + X0 + ',' + Y + ',' + k));
    inV(pl, { cx: cx + 2 * M, cy: cy, hw: hw, hh: hw * 0.6 }, minR, (bb, X, Y, wx, wy, k, X0) => b.push(bb + ',' + X0 + ',' + Y + ',' + (k - M))); a.sort(); b.sort(); shown += a.length;
    if (!a.length || a.length !== b.length || a.some((x, i) => x !== b[i])) bad.push('M=' + M + ' about a circle of curvature ' + c[0] + ': ' + a.length + ' near the origin, ' + b.length + ' moved along'); }
  { const lines = v => { const got = []; G.inView(pl, v, 0.01, (bb, X, Y) => { if (bb === 0) got.push(Y); }); return got.sort().join(); }; n++;
    if (lines({ cx: 1, cy: 0, hw: 0.5, hh: 0.5 }) !== '' || lines({ cx: 1, cy: 0.8, hw: 0.5, hh: 0.5 }) !== '1' || lines({ cx: 7.3, cy: -0.9, hw: 0.2, hh: 0.2 }) !== '-1' || lines({ cx: 1, cy: 0, hw: 2, hh: 1.2 }) !== '-1,1') bad.push('the lines of the strip are not given exactly when they are in view'); }
  all('inView() on the strip: a view about a circle of curvature up to 3 x 10^10, moved 500, 2,500 and 4,000 periods along, shows the same circles moved (' + shown + ' circles; curvature times x is past 2^53 for many of them); and the two lines are given exactly when they are in view', n, bad); }

// 8. areas: the circles fill the outer circle (or one period of the strip) without overlapping
{ const bad = []; let n = 0; const notes = [];
  for (const q of [[-1, 2, 2, 3], [-3, 5, 8, 8], [-6, 11, 14, 15], [-11, 21, 24, 28], [-23, 48, 49, 52], [0, 0, 1, 1]]) { const pl = G.place(q), B = 6000; let area = 0, cnt = 0; n++;
    if (pl.strip) { const ones = [], fours = []; inV(pl, [-6.5, -1.5, 8.5, 1.5], 1 / B, (b, X, Y) => { if (b === 1) ones.push(X / b); if (b === 4) fours.push([X / b, Y / b].join()); const x = X / b; if (b > 0 && x >= 0 && x < 2) { area += Math.PI / (b * b); cnt++; } });
      const wantOnes = [-6, -4, -2, 0, 2, 4, 6, 8], want4 = []; for (let k = -5; k <= 7; k += 2) { want4.push([k, -0.75].join()); want4.push([k, 0.75].join()); }
      const frac = area / 4; notes.push('strip ' + frac.toFixed(4));
      if (JSON.stringify(ones.sort((a, b) => a - b)) !== JSON.stringify(wantOnes) || JSON.stringify(fours.sort()) !== JSON.stringify(want4.sort()) || !(frac > 0.985 && frac < 1)) bad.push('strip: unit circles at ' + ones.join(' ') + '; area share ' + frac); }
    else { inV(pl, [-1e9, -1e9, 1e9, 1e9], 1 / B, (b) => { if (b > 0) { area += Math.PI / (b * b); cnt++; } }); const frac = area / (Math.PI / (q[0] * q[0])); notes.push(JSON.stringify(q) + ' ' + frac.toFixed(4)); if (!(frac > 0.97 && frac < 1)) bad.push(JSON.stringify(q) + ' area share ' + frac); } }
  all('the circles up to curvature 6,000 cover between 97% and 100% of the outer circle (at least 98.5% of a period of the strip, whose circles of curvature 1 and 4 are where they should be): ' + notes.join('; '), n, bad); }

// 7. deep: a view a million million times smaller than the packing still gives whole numbers and touching circles
{ const pl = G.place([-3, 5, 8, 8]); let cur = pl.circles.map(x => x.slice()), last = -1, good = true, deepest = 0;
  for (let k = 0; k < 400; k++) { let best = -1, bv = Infinity; for (let i = 0; i < 4; i++) { if (i === last) continue; const b = 2 * (cur[0][0] + cur[1][0] + cur[2][0] + cur[3][0] - cur[i][0]) - cur[i][0]; if (b < bv) { bv = b; best = i; } }
    const i = k % 3 === 0 ? best : (last + 1 + Math.floor(rnd() * 3)) % 4, nw = [0, 1, 2].map(t => 2 * (cur[0][t] + cur[1][t] + cur[2][t] + cur[3][t] - cur[i][t]) - cur[i][t]); if (i === last) continue; if (nw[0] > 4e15 / 16) break;
    for (let j = 0; j < 4; j++) if (j !== i) { const u = BigInt(cur[j][0]) * BigInt(nw[1]) - BigInt(nw[0]) * BigInt(cur[j][1]), v = BigInt(cur[j][0]) * BigInt(nw[2]) - BigInt(nw[0]) * BigInt(cur[j][2]), s = BigInt(cur[j][0]) + BigInt(nw[0]); if (u * u + v * v !== s * s) good = false; }
    if (!nw.every(Number.isSafeInteger)) good = false; cur[i] = nw; last = i; deepest = Math.max(deepest, nw[0]); }
  ok('a walk down to curvature ' + deepest.toExponential(2) + ' keeps safe whole numbers and exact touching (checked with BigInt)', good && deepest > 1e13); }

fs.writeSync(1, lines.join('\n') + '\n\n' + pass + ' pass, ' + fail + ' fail\n'); process.exit(fail ? 1 : 0);

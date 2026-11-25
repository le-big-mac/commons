/* otest.js: tests of ocore.js, peel.c and cell.c on cases worked by hand or by a second method.
   Run: node otest.js    (needs ./peel, ./peel-wide and ./cell built: see the README) */
'use strict';
var O = require('./ocore.js'), cp = require('child_process'), fs = require('fs'), os = require('os'), path = require('path');
var pass = 0, fail = 0;
function ok(name, cond, detail) { if (cond) { pass++; console.log('pass  ' + name); } else { fail++; console.log('FAIL  ' + name + (detail ? '   ' + detail : '')); } }
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function I(a) { return Int32Array.from(a); }
function peelOf(pts) { return O.peel(I(pts.map(function (p) { return p[0]; })), I(pts.map(function (p) { return p[1]; }))); }
function exe(name) { return path.join(__dirname, name); }
var TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'agent2-peel-'));
function cDepths(x, y, bin, extra) {          /* the C program's depths for the same points */
    var f = path.join(TMP, 'pts.txt'), g = path.join(TMP, 'dep.txt'), lines = [], i;
    for (i = 0; i < x.length; i++) lines.push(x[i] + ' ' + y[i]);
    fs.writeFileSync(f, lines.join('\n') + '\n');
    var out = JSON.parse(cp.execFileSync(exe(bin || 'peel'), ['file:' + f, '0', '0'].concat(extra || ['-plain']).concat(['-depths', g]), { encoding: 'utf8' }));
    return { depth: fs.readFileSync(g, 'utf8').trim().split('\n').map(function (l) { return Number(l.split(' ')[2]); }), out: out };
}
function sameDepth(a, b) { if (a.length !== b.length) return false; for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return false; return true; }

/* ---- turn ---- */
ok('turn by hand: (0,0),(1,0),(1,1) left; (0,0),(1,0),(1,-1) right; (0,0),(1,1),(2,2) in line', O.turn(I([0, 1, 1]), I([0, 0, 1]), 0, 1, 2) === 1 && O.turn(I([0, 1, 1]), I([0, 0, -1]), 0, 1, 2) === -1 && O.turn(I([0, 1, 2]), I([0, 1, 2]), 0, 1, 2) === 0);
ok('turn is exact at the largest coordinates allowed: (-L,-L),(L,L),(L-1,L) is left by one unit of area', (function () { var L = O.LIMIT - 1; return O.turn(I([-L, L, L - 1]), I([-L, L, L]), 0, 1, 2) === 1 && O.turn(I([-L, L, L]), I([-L, L, L - 1]), 0, 1, 2) === -1; })());

/* ---- peeling by hand ---- */
ok('a square and its centre: 4 then 1', (function () { var p = peelOf([[0, 0], [4, 0], [4, 4], [0, 4], [2, 2]]); return p.layers === 2 && eq(p.sizes, [0, 4, 1]) && eq(Array.from(p.depth), [1, 1, 1, 1, 2]); })());
ok('a 3 x 3 grid, every boundary point: 8 then 1', (function () { var pts = [], a, b; for (a = 0; a < 3; a++) for (b = 0; b < 3; b++) pts.push([a, b]); var p = peelOf(pts); return eq(p.sizes, [0, 8, 1]) && p.depth[4] === 2; })());
ok('a point on a side comes off with the corners: triangle (0,0),(4,0),(0,4), (2,0) on a side, (1,1) inside: 4 then 1', (function () { var p = peelOf([[0, 0], [4, 0], [0, 4], [2, 0], [1, 1]]); return eq(p.sizes, [0, 4, 1]) && eq(Array.from(p.depth), [1, 1, 1, 1, 2]); })());
ok('a point on the slanted side too: (2,2) on the side from (4,0) to (0,4)', (function () { var p = peelOf([[0, 0], [4, 0], [0, 4], [2, 2], [1, 1]]); return eq(Array.from(p.depth), [1, 1, 1, 1, 2]); })());
ok('five points in a line are one layer; one point is one layer; two points are one layer', eq(peelOf([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]).sizes, [0, 5]) && eq(peelOf([[7, 7]]).sizes, [0, 1]) && eq(peelOf([[0, 0], [5, 1]]).sizes, [0, 2]));
ok('three nested squares: 4, 4, 4', (function () { var pts = []; [10, 6, 2].forEach(function (s) { pts.push([-s, -s], [s, -s], [s, s], [-s, s]); }); var p = peelOf(pts); return eq(p.sizes, [0, 4, 4, 4]) && eq(Array.from(p.depth), [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]); })());
ok('an inner point that is outside the next square but inside the hull waits its turn: square of side 20, a point at (9,0), a square of side 4: 4, 1, 4', (function () {
    var p = peelOf([[-10, -10], [10, -10], [10, 10], [-10, 10], [9, 0], [-2, -2], [2, -2], [2, 2], [-2, 2]]); return eq(p.sizes, [0, 4, 5]) || eq(p.sizes, [0, 4, 1, 4]); })(), JSON.stringify(peelOf([[-10, -10], [10, -10], [10, 10], [-10, 10], [9, 0], [-2, -2], [2, -2], [2, 2], [-2, 2]]).sizes));
ok('  ... and by hand it is 4 then 5: with the big square gone, (9,0) and the small square are all corners of their hull', eq(peelOf([[-10, -10], [10, -10], [10, 10], [-10, 10], [9, 0], [-2, -2], [2, -2], [2, 2], [-2, 2]]).sizes, [0, 4, 5]));
ok('two points in one place on the rim go together; in the middle they are the last layer', (function () {
    var p = peelOf([[0, 0], [0, 0], [6, 0], [0, 6], [1, 1]]), q = peelOf([[0, 0], [6, 0], [0, 6], [1, 1], [1, 1]]); return eq(p.sizes, [0, 4, 1]) && eq(q.sizes, [0, 3, 2]); })());
ok('upright sides: a 2 x 4 block of grid points is one layer of 8; a 3 x 4 block is 10 then 2', (function () {
    var a = [], b = [], i, j; for (i = 0; i < 2; i++) for (j = 0; j < 4; j++) a.push([i, j]); for (i = 0; i < 3; i++) for (j = 0; j < 4; j++) b.push([i, j]); return eq(peelOf(a).sizes, [0, 8]) && eq(peelOf(b).sizes, [0, 10, 2]); })());
ok('every point gets a depth and the sizes add up (60 random clouds)', (function () {
    var r = O.rng(5), t, i;
    for (t = 0; t < 60; t++) { var n = 1 + Math.floor(r() * 400), c = O.sample(O.SHAPES[t % 4], n, r), p = O.peel(c.x, c.y), s = 0, cnt = [];
        for (i = 0; i <= p.layers; i++) cnt.push(0);
        for (i = 0; i < n; i++) { if (!(p.depth[i] >= 1 && p.depth[i] <= p.layers)) return false; cnt[p.depth[i]]++; }
        for (i = 1; i <= p.layers; i++) { s += p.sizes[i]; if (cnt[i] !== p.sizes[i] || p.sizes[i] < 1) return false; }
        if (s !== n) return false; }
    return true; })());
ok('each layer is the whole boundary of the hull of what is left, by a slow direct test (20 small clouds)', (function () {
    var r = O.rng(9), t, i, j, k;
    function onHull(x, y, alive, p) {          /* p is on the boundary iff some line through p has no living point strictly on one side: try all lines through p and another point, and in-line cases */
        var others = alive.filter(function (q) { return x[q] !== x[p] || y[q] !== y[p]; });
        if (others.length === 0) return true;
        for (var a = 0; a < others.length; a++) { var q = others[a], pos = 0, neg = 0; for (var b = 0; b < others.length; b++) { var s = O.turn(x, y, p, q, others[b]); if (s > 0) pos++; else if (s < 0) neg++; } if (pos === 0 || neg === 0) return true; }
        return false; }
    for (t = 0; t < 20; t++) { var n = 5 + Math.floor(r() * 60), c = O.sample(O.SHAPES[t % 4], n, r);
        if (t % 5 === 0) for (i = 0; i < n; i++) { c.x[i] = Math.round(c.x[i] / 400000); c.y[i] = Math.round(c.y[i] / 400000); }     /* coarse: many ties and points in line */
        var p = O.peel(c.x, c.y);
        for (k = 1; k <= p.layers; k++) { var alive = []; for (i = 0; i < n; i++) if (p.depth[i] >= k) alive.push(i);
            for (j = 0; j < alive.length; j++) if (onHull(c.x, c.y, alive, alive[j]) !== (p.depth[alive[j]] === k)) return false; } }
    return true; })());
ok('a part of a cloud has no more layers than the whole (40 random clouds and parts)', (function () {
    var r = O.rng(13), t, i;
    for (t = 0; t < 40; t++) { var n = 50 + Math.floor(r() * 500), c = O.sample(O.SHAPES[t % 4], n, r), keepX = [], keepY = [];
        for (i = 0; i < n; i++) if (r() < 0.6) { keepX.push(c.x[i]); keepY.push(c.y[i]); }
        if (keepX.length && O.peel(I(keepX), I(keepY)).layers > O.peel(c.x, c.y).layers) return false; }
    return true; })());
ok('peel refuses a coordinate of 2^25 and a fraction', [[O.LIMIT, 0], [0.5, 1]].every(function (p) { try { O.peel(Float64Array.from([p[0], 0, 1]), Float64Array.from([p[1], 1, 0])); return false; } catch (e) { return /whole numbers below/.test(e.message); } }));

/* ---- stretching ---- */
ok('stretching and shearing changes no depth (30 clouds, to 3000 points)', (function () {
    var r = O.rng(21), t; for (t = 0; t < 30; t++) { var c = O.sample(O.SHAPES[t % 4], 20 + Math.floor(r() * 3000), r), s = O.stretch(c.x, c.y); if (!sameDepth(O.peel(c.x, c.y).depth, O.peel(s.x, s.y).depth)) return false; } return true; })());
ok('stretch by hand: (2,5) goes to (11,5)', (function () { var s = O.stretch(I([2]), I([5])); return s.x[0] === 11 && s.y[0] === 5; })());

/* ---- the C program against the core, and its two methods against each other ---- */
ok('ocore.peel gives every point the depth that peel.c gives (16 clouds, 300 to 40,000 points, four shapes)', (function () {
    var r = O.rng(7), bad = 0; ['disc', 'ellipse', 'square', 'triangle'].forEach(function (sh) { [300, 3000, 12000, 40000].forEach(function (N) { var c = O.sample(sh, N, r); if (!sameDepth(cDepths(c.x, c.y).depth, O.peel(c.x, c.y).depth)) bad++; }); });
    return bad === 0; })());
ok('ocore.peel = peel.c on coarse clouds full of ties and points in line (8 clouds)', (function () {
    var r = O.rng(17), bad = 0, t, i; for (t = 0; t < 8; t++) { var c = O.sample(O.SHAPES[t % 4], 2000, r); for (i = 0; i < 2000; i++) { c.x[i] = Math.round(c.x[i] / 60000); c.y[i] = Math.round(c.y[i] / 60000); } if (!sameDepth(cDepths(c.x, c.y).depth, O.peel(c.x, c.y).depth)) bad++; }
    return bad === 0; })());
ok("peel.c's sector method gives the same depths as its plain method (disc, square, triangle; 30,000 and 300,000 points; -both)", (function () {
    var bad = 0; ['disc', 'square', 'triangle'].forEach(function (sh) { [[30000, 11], [30000, 12], [300000, 13]].forEach(function (q) { var o = JSON.parse(cp.execFileSync(exe('peel'), [sh, String(q[0]), String(q[1]), '-both'], { encoding: 'utf8' })); if (o.same !== 1 || o.fast_layers < 100) bad++; }); });
    return bad === 0; })());
ok('the sector method with 1, 4 and 16 times as many sectors gives the same count and estimates (disc, 200,000 points)', (function () {
    var outs = ['1', '4', '16'].map(function (m) { var o = JSON.parse(cp.execFileSync(exe('peel'), ['disc', '200000', '5', '-mult', m], { encoding: 'utf8' })); return [o.layers, o.first, o.a_prof, o.a_size].join(); });
    return outs[0] === outs[1] && outs[1] === outs[2]; })());
ok('the grid, vertices only: 1, 1, 3, 3, 6, 6, 9, 9, 12, 12, 15, 15, 19, 19, 23 layers for sides 1 to 15 (OEIS A290966)', (function () {
    var got = []; for (var g = 1; g <= 15; g++) got.push(JSON.parse(cp.execFileSync(exe('peel'), ['grid', String(g), '0', '-plain', '-vertices'], { encoding: 'utf8' })).layers);
    return eq(got, [1, 1, 3, 3, 6, 6, 9, 9, 12, 12, 15, 15, 19, 19, 23]); })());
ok('the grid, every boundary point: a 7 x 7 grid is 4 rings (24, 16, 8, 1) by peel.c and by ocore', (function () {
    var x = [], y = [], a, b; for (a = 0; a < 7; a++) for (b = 0; b < 7; b++) { x.push(a); y.push(b); }
    var p = O.peel(I(x), I(y)), c = cDepths(I(x), I(y)); return eq(p.sizes, [0, 24, 16, 8, 1]) && sameDepth(c.depth, p.depth) && c.out.layers === 4; })());
ok('peel-wide: a cloud and the same cloud stretched have the same depths (C, three shapes, 20,000 points)', (function () {
    var bad = 0; ['disc', 'square', 'triangle'].forEach(function (sh, i) {
        var a = cp.execFileSync(exe('peel-wide'), [sh, '20000', String(40 + i), '-plain', '-depths', '-'], { encoding: 'utf8', maxBuffer: 67108864 }).split('\n').filter(function (l) { return l.split(' ').length === 3; });
        var b = cp.execFileSync(exe('peel-wide'), [sh, '20000', String(40 + i), '-plain', '-affine', '-depths', '-'], { encoding: 'utf8', maxBuffer: 67108864 }).split('\n').filter(function (l) { return l.split(' ').length === 3; });
        var moved = 0, k; for (k = 0; k < a.length; k++) { if (a[k].split(' ')[2] !== b[k].split(' ')[2]) bad++; if (a[k].split(' ')[0] !== b[k].split(' ')[0]) moved++; }
        if (a.length !== 20000 || b.length !== 20000 || moved < 19000) bad++; });
    return bad === 0; })());
ok("peel.c's random clouds: all points inside their shape; the three shapes have the disc's area to 1 part in 10^8; the triangle has equal sides and its centre at 0", (function () {
    var R = 536870912, sq = 475789457, hb = 723043617, top = 834898854, bot = -417449427, bad = 0;
    ['disc', 'square', 'triangle'].forEach(function (sh) {
        var l = cp.execFileSync(exe('peel'), [sh, '20000', '3', '-plain', '-depths', '-'], { encoding: 'utf8', maxBuffer: 67108864 }).split('\n').filter(function (q) { return q.split(' ').length === 3; });
        l.forEach(function (q) { var x = Number(q.split(' ')[0]), y = Number(q.split(' ')[1]);
            if (sh === 'disc' && x * x + y * y > R * R) bad++;
            if (sh === 'square' && (Math.abs(x) > sq || Math.abs(y) > sq)) bad++;
            if (sh === 'triangle' && (y < bot || y > top || Math.abs(x) * (top - bot) > hb * (top - y) + 1)) bad++; });
        if (l.length !== 20000) bad++;
        /* and they fill it evenly: half the points in the inner half of the area, and some near the edge */
        var inner = 0, far = 0; l.forEach(function (q) { var x = Number(q.split(' ')[0]), y = Number(q.split(' ')[1]);
            if (sh === 'disc') { if (x * x + y * y < R * R / 2) inner++; if (x * x + y * y > 0.98 * R * R) far++; }
            if (sh === 'square') { if (Math.abs(x) < sq / 2) inner++; if (Math.abs(x) > 0.99 * sq || Math.abs(y) > 0.99 * sq) far++; }
            if (sh === 'triangle') { if (y < bot + (top - bot) * (1 - Math.SQRT1_2)) inner++; if (y > top - 0.1 * (top - bot)) far++; } });
        if (Math.abs(inner / 20000 - 0.5) > 0.02 || far < 20) bad++; });
    var disc = Math.PI * R * R; return bad === 0 && Math.abs(4 * sq * sq / disc - 1) < 1e-8 && Math.abs(hb * (top - bot) / disc - 1) < 1e-8 && Math.abs((top - bot) / hb / Math.sqrt(3) - 1) < 1e-8 && Math.abs(top + 2 * bot) <= 1; })());

ok('what peel.c reports is recomputed here from its own depths and sizes: layers, first layer, layers 20 to 40, a_tot, the slope, a_prof, the fit of sizes, a_size, the two roundness ratios (disc and square, 50,000 points)', (function () {
    var bad = 0; ['disc', 'square'].forEach(function (sh, si) {
        var fd = path.join(TMP, 'd.txt'), fz = path.join(TMP, 'z.txt'), n = 50000, R = 536870912;
        var o = JSON.parse(cp.execFileSync(exe('peel'), [sh, String(n), String(60 + si), '-depths', fd, '-sizes', fz], { encoding: 'utf8' }));
        var D = fs.readFileSync(fd, 'utf8').trim().split('\n').map(function (l) { return l.split(' ').map(Number); }), Z = [0].concat(fs.readFileSync(fz, 'utf8').trim().split('\n').map(Number)), N = Z.length - 1;
        var su = 0, sd = 0, suu = 0, sud = 0, c = 0, k1 = Math.floor(0.5 * N + 0.5), k2 = Math.floor(0.9 * N + 0.5), m1 = [Infinity, 0], m2 = [Infinity, 0];
        D.forEach(function (q) { var r = Math.sqrt(q[0] * q[0] + q[1] * q[1]) / R, u = 1 - Math.pow(r, 4 / 3); if (r >= 0.3 && r <= 0.9) { su += u; sd += q[2]; suu += u * u; sud += u * q[2]; c++; }
            if (q[2] === k1) { m1[0] = Math.min(m1[0], r); m1[1] = Math.max(m1[1], r); } if (q[2] === k2) { m2[0] = Math.min(m2[0], r); m2[1] = Math.max(m2[1], r); } });
        var slope = (sud - su * sd / c) / (suu - su * su / c), K = Math.pow(n / Math.PI, 2 / 3), sw = 0, sww = 0, k, m = 0;
        for (k = 1; k <= N; k++) { var f = k / N; if (f >= 0.1 && f <= 0.7) { var w = Math.sqrt(1 - f); sw += Z[k] * w; sww += w * w; } }
        for (k = 20; k <= 40; k++) m += Z[k] / 21;
        var cfit = sw / sww, near = function (a, b2) { return Math.abs(a - b2) <= 2e-6 * Math.max(1, Math.abs(b2)); };
        if (!(o.layers === N && D.length === n && o.removed === n && o.first === Z[1] && near(o.mean20to40, m) && near(o.a_tot, O.aTot(n, N)) && near(o.slope, slope) && near(o.a_prof, 4 / 3 * slope / K) && near(o.cfit, cfit) &&
            near(o.a_size, 2 * Math.pow(Math.PI, 2 / 3) * Math.pow(n, 1 / 3) / cfit) && near(o.ratio_half, m1[1] / m1[0]) && near(o.ratio_ninetenths, m2[1] / m2[0]))) bad++; });
    return bad === 0; })());
ok('peel-wide -affine really is (x, y) -> (3x + y, y)', (function () {
    var a = cp.execFileSync(exe('peel-wide'), ['disc', '50', '9', '-plain', '-depths', '-'], { encoding: 'utf8' }).split('\n').filter(function (l) { return l.split(' ').length === 3; }).map(function (l) { return l.split(' ').map(Number); });
    var b = cp.execFileSync(exe('peel-wide'), ['disc', '50', '9', '-plain', '-affine', '-depths', '-'], { encoding: 'utf8' }).split('\n').filter(function (l) { return l.split(' ').length === 3; }).map(function (l) { return l.split(' ').map(Number); });
    return a.length === 50 && a.every(function (q, i) { return b[i][0] === 3 * q[0] + q[1] && b[i][1] === q[1]; }); })());
ok('a file that cannot be written stops peel.c with a message, not a crash', (function () { try { cp.execFileSync(exe('peel'), ['disc', '100', '1', '-depths', '/nonexistent-dir/x'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }); return false; } catch (e) { return e.status === 3 && /cannot write/.test(String(e.stderr)); } })());

/* ---- the cell problem ---- */
ok("cell.c's column method gives the measured points the depths of its plain method (three windows, two column widths)", (function () {
    var bad = 0; [['1500', '100', '1'], ['1500', '100', '2'], ['2000', '160', '3']].forEach(function (q) { ['2', '6'].forEach(function (w) { var o = JSON.parse(cp.execFileSync(exe('cell'), q.concat(['-both', '-w', w]), { encoding: 'utf8' })); if (o.same !== 1 || o.measured < 10000) bad++; }); });
    return bad === 0; })());
ok('cell.c by hand: the lift turns a parabola into a line. Three points on y = 10 - (x-3)^2/2 lifted are in line, so with a fourth below they are not all corners', (function () {
    /* in the program's units xu = 1024 x, yu = 2^21 y; lifted Y = yu + xu^2. Points x = 1, 3, 5: y = 8, 10, 8. Lifted: 8*2^21 + 1024^2, 10*2^21 + 9*1024^2, 8*2^21 + 25*1024^2 */
    var Y = [8 * 2097152 + 1048576, 10 * 2097152 + 9 * 1048576, 8 * 2097152 + 25 * 1048576], X = [1024, 3072, 5120];
    return (X[1] - X[0]) * (Y[2] - Y[0]) - (Y[1] - Y[0]) * (X[2] - X[0]) === 0; })());

ok('cell.c: the slope of depth against height is near 1.33 (three small windows), and is the slope of the band means it writes out', (function () {
    var bad = 0, sum = 0; ['1', '2', '3'].forEach(function (sd) { var f = path.join(TMP, 'prof.txt'), o = JSON.parse(cp.execFileSync(exe('cell'), ['1500', '100', sd, '-profile', f], { encoding: 'utf8' }));
        var rows = fs.readFileSync(f, 'utf8').trim().split('\n').map(function (l) { return l.split(' ').map(Number); }).filter(function (q) { return q[0] >= 0.2 * 80; });
        var c = 0, sy = 0, sdp = 0, syy = 0, syd = 0; rows.forEach(function (q) { c += q[1]; sy += q[1] * q[0]; sdp += q[1] * q[2]; syy += q[1] * q[0] * q[0]; syd += q[1] * q[0] * q[2]; });
        var s = (syd - sy * sdp / c) / (syy - sy * sy / c); sum += o.alpha_02;
        if (Math.abs(s - o.alpha_02) > 0.004 || o.HM !== 80 || Math.abs(o.margin - 20 * Math.sqrt(160)) > 1) bad++; });
    return bad === 0 && sum / 3 > 1.31 && sum / 3 < 1.34; })());

/* ---- sampling ---- */
ok('sample: every point inside its shape; the same seed gives the same cloud; another seed another', (function () {
    var R = O.RAD, bad = 0;
    O.SHAPES.slice(0, 4).forEach(function (sh) { var c = O.sample(sh, 5000, O.rng(3)), d = O.sample(sh, 5000, O.rng(3)), e = O.sample(sh, 5000, O.rng(4)), i, diff = 0;
        for (i = 0; i < 5000; i++) { var x = c.x[i], y = c.y[i];
            if (sh === 'disc' && x * x + y * y > R * R) bad++;
            if (sh === 'ellipse' && x * x / 3 + y * y * 3 > R * R * 1.000001) bad++;
            if (sh === 'square' && (Math.abs(x) > R * Math.sqrt(Math.PI) / 2 || Math.abs(y) > R * Math.sqrt(Math.PI) / 2)) bad++;
            if (c.x[i] !== d.x[i] || c.y[i] !== d.y[i]) bad++; if (c.x[i] !== e.x[i]) diff++; }
        if (diff < 4000) bad++;
        var reach = 0, half = 0; for (i = 0; i < 5000; i++) { var X = c.x[i], Y = c.y[i];
            if (sh === 'disc') { if (X * X + Y * Y > 0.97 * R * R) reach++; if (X * X + Y * Y < R * R / 2) half++; }
            if (sh === 'ellipse') { if (X * X / 3 + Y * Y * 3 > 0.97 * R * R) reach++; if (X * X / 3 + Y * Y * 3 < R * R / 2) half++; }
            if (sh === 'square') { var q = R * Math.sqrt(Math.PI) / 2; if (Math.abs(X) > 0.985 * q || Math.abs(Y) > 0.985 * q) reach++; if (Math.abs(X) < q / 2) half++; } }
        if (sh !== 'triangle' && (reach < 50 || Math.abs(half / 5000 - 0.5) > 0.04)) bad++; });       /* the triangle has its own test below */
    return bad === 0; })());
ok('sample: the four shapes have the same area (their boxes filled alike: the share of 200,000 draws that land inside matches the area, within 1%)', (function () {
    /* each shape is drawn by throwing into its own box: the acceptance tells the area. Count throws through a counting generator. */
    var R = O.RAD, want = { disc: Math.PI / 4, ellipse: Math.PI / 4, square: 1, triangle: 0.5 }, bad = 0;
    Object.keys(want).forEach(function (sh) { var calls = 0, r0 = O.rng(8), r = function () { calls++; return r0(); }; O.sample(sh, 200000, r); var acc = 200000 / (calls / 2); if (Math.abs(acc / want[sh] - 1) > 0.01) bad++; });
    return bad === 0; })());
ok('sample: a triangle cloud is inside the triangle with corners (0, top), (-hb, bot), (hb, bot), and reaches near all three', (function () {
    var hb = Math.floor(O.RAD * Math.sqrt(Math.PI / Math.sqrt(3))), hgt = Math.floor(hb * Math.sqrt(3)), top = Math.floor(2 * hgt / 3), bot = top - hgt, c = O.sample('triangle', 20000, O.rng(2)), i, mxy = -Infinity, mnx = Infinity, mxx = -Infinity;
    for (i = 0; i < 20000; i++) { if (c.y[i] < bot || c.y[i] > top || Math.abs(c.x[i]) * hgt > hb * (top - c.y[i])) return false; if (c.y[i] > mxy) mxy = c.y[i]; if (c.x[i] < mnx) mnx = c.x[i]; if (c.x[i] > mxx) mxx = c.x[i]; }
    return mxy > top - 0.05 * hgt && mnx < -0.95 * hb && mxx > 0.95 * hb && Math.abs(hb * hgt / (Math.PI * O.RAD * O.RAD) - 1) < 1e-5; })());
ok('sample of your own shape: points inside the polygon given; a thin sliver is refused; fewer than three corners is refused', (function () {
    var poly = { x: [-1000000, 1000000, 1000000, 0, -1000000], y: [-800000, -800000, 800000, 100000, 800000] }, c = O.sample('own', 3000, O.rng(1), poly), i;
    for (i = 0; i < 3000; i++) if (!O.inside(poly.x, poly.y, c.x[i], c.y[i])) return false;
    var a = false, b = false; try { O.sample('own', 100, O.rng(1), { x: [0, 3000000, 3000001], y: [0, 3000000, 3000000] }); } catch (e) { a = /too thin/.test(e.message); }      /* a sliver along a diagonal */
    try { O.sample('own', 100, O.rng(1), { x: [0, 1], y: [0, 1] }); } catch (e) { b = /three corners/.test(e.message); }
    return a && b; })());
ok('sample of your own shape fills the whole of it, however far out it reaches: a long box from -3.5 RAD to 3.5 RAD has a tenth of its points in each tenth of its length; a corner at a quarter of the limit is refused', (function () {
    var R = O.RAD, poly = { x: [-3.5 * R, 3.5 * R, 3.5 * R, -3.5 * R], y: [-R / 2, -R / 2, R / 2, R / 2] }, c = O.sample('own', 20000, O.rng(5), poly), bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], i;
    for (i = 0; i < 20000; i++) { if (!(Math.abs(c.x[i]) <= 3.5 * R && Math.abs(c.y[i]) <= R / 2)) return false; bins[Math.min(9, Math.floor((c.x[i] + 3.5 * R) / (0.7 * R)))]++; }
    var far = false; try { O.sample('own', 10, O.rng(1), { x: [0, O.LIMIT / 4, 0], y: [0, 0, 5] }); } catch (e) { far = /too far out/.test(e.message); }
    return bins.every(function (b) { return Math.abs(b / 2000 - 1) < 0.1; }) && far; })());
ok('sample refuses an unknown shape, no points, and a fraction of a point', ['blob', 0, 2.5].every(function (v, i) { try { O.sample(i === 0 ? v : 'disc', i === 0 ? 10 : v, O.rng(1)); return false; } catch (e) { return true; } }));
ok('inside and polygonArea by hand: the square (0,0),(4,0),(4,4),(0,4) has area 16, holds (1,1), not (5,1); an L of area 12 holds (1,3), not (3,3)', (function () {
    var sx = [0, 4, 4, 0], sy = [0, 0, 4, 4], lx = [0, 4, 4, 2, 2, 0], ly = [0, 0, 2, 2, 4, 4];
    return O.polygonArea(sx, sy) === 16 && O.inside(sx, sy, 1, 1) && !O.inside(sx, sy, 5, 1) && O.polygonArea(lx, ly) === 12 && O.inside(lx, ly, 1, 3) && !O.inside(lx, ly, 3, 3); })());

/* ---- ring ---- */
ok('ring: the points of a layer in order round it, turning left all the way (40 layers of a cloud)', (function () {
    var c = O.sample('square', 4000, O.rng(6)), p = O.peel(c.x, c.y), k, i;
    for (k = 1; k <= 40; k++) { var g = O.ring(c.x, c.y, p.depth, k), m = g.length; if (m !== p.sizes[k]) return false; for (i = 0; i < m && m >= 3; i++) if (O.turn(c.x, c.y, g[i], g[(i + 1) % m], g[(i + 2) % m]) < 0) return false; }
    return O.ring(c.x, c.y, p.depth, p.layers + 5).length === 0; })());

/* ---- the formulas ---- */
ok('discLayers, discSize and aTot by hand: n = pi gives 0.75 x 1.326 layers; aTot of (n/pi)^(2/3) layers is 4/3; the formula sizes add up to n', (function () {
    var n = 1000000, N = O.discLayers(n), s = 0, k; for (k = 1; k <= Math.ceil(N); k++) s += O.discSize(n, k - 0.5);
    return Math.abs(O.discLayers(Math.PI) - 0.9945) < 1e-12 && Math.abs(O.aTot(n, Math.pow(n / Math.PI, 2 / 3)) - 4 / 3) < 1e-12 && Math.abs(s / n - 1) < 0.001 && O.discSize(n, N + 1) === 0 && O.ALPHA === 1.326; })());
ok('roundness by hand: points at distances 2 and 4 from the centre give 2', (function () { return O.roundness(I([2, 0, -4]), I([0, 2, 0]), I([1, 1, 1]), 1, 0, 0) === 2; })());

fs.rmSync(TMP, { recursive: true });
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);

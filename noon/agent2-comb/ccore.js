// ccore.js -- closed plane curves as polygons with equal edges: turning number, Whitney's deformation (his formulas (12) and
// (13)), the straight-line deformation and its kinks, crossings and his Theorem 2.  No drawing here; node tests it.
(function (root) {
  'use strict';
  var TAU = 2 * Math.PI;
  function wrap(a) { a = a % TAU; if (a > Math.PI) a -= TAU; if (a <= -Math.PI) a += TAU; return a; }
  function length(pts) { var L = 0, i, j; for (i = 0; i < pts.length; i++) { j = (i + 1) % pts.length; L += Math.hypot(pts[j][0] - pts[i][0], pts[j][1] - pts[i][1]); } return L; }
  // N points at equal steps of arc length round the closed polygon, beginning at its first point
  function resample(pts, N) {
    var L = length(pts), step = L / N, out = [], i = 0, done = 0, seg, a, b, k, t;
    a = pts[0]; b = pts[1 % pts.length]; seg = Math.hypot(b[0] - a[0], b[1] - a[1]);
    for (k = 0; k < N; k++) { t = k * step;
      while (done + seg < t && i < pts.length - 1) { done += seg; i++; a = pts[i]; b = pts[(i + 1) % pts.length]; seg = Math.hypot(b[0] - a[0], b[1] - a[1]); }
      var f = seg > 0 ? Math.min(1, (t - done) / seg) : 0; out.push([a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1])]); }
    return out;
  }
  // the direction of each edge as an angle that never jumps: F[k] for the edge from point k to point k + 1; F[N] is F[0] plus the whole turn
  function angles(pts) {
    var N = pts.length, F = [], k, a, prev;
    for (k = 0; k <= N; k++) { var p = pts[k % N], q = pts[(k + 1) % N]; a = Math.atan2(q[1] - p[1], q[0] - p[0]); F.push(k === 0 ? a : prev + wrap(a - prev)); prev = F[k]; }
    return F;
  }
  function turning(pts) { var F = angles(pts); return Math.round((F[pts.length] - F[0]) / TAU); }
  function centroid(pts) { var x = 0, y = 0, i; for (i = 0; i < pts.length; i++) { x += pts[i][0]; y += pts[i][1]; } return [x / pts.length, y / pts.length]; }
  function shape(pts) { return { pts: pts, N: pts.length, F: angles(pts), L: length(pts), c: centroid(pts), n: turning(pts) }; }
  // the curve whose edges point along the angles F (N of them), closed by taking the mean direction from each (Whitney's Lemma 1)
  function fromAngles(F, N, L, c) {
    var mx = 0, my = 0, k, pts = [], x = 0, y = 0, least = Infinity, cx = 0, cy = 0;
    for (k = 0; k < N; k++) { mx += Math.cos(F[k]); my += Math.sin(F[k]); } mx /= N; my /= N;
    for (k = 0; k < N; k++) { pts.push([x, y]); cx += x; cy += y; var ex = Math.cos(F[k]) - mx, ey = Math.sin(F[k]) - my, s = Math.hypot(ex, ey); if (s < least) least = s; x += ex * L / N; y += ey * L / N; }
    cx /= N; cy /= N; for (k = 0; k < N; k++) { pts[k][0] += c[0] - cx; pts[k][1] += c[1] - cy; }
    return { pts: pts, least: least, mean: Math.hypot(mx, my), gap: Math.hypot(x, y) };
  }
  // Whitney's deformation from shape A to shape B at u in [0, 1]: the angles go straight from the one to the other
  function whitney(A, B, u) {
    if (A.N !== B.N) throw new Error('whitney: the two curves must have the same number of points');
    if (A.n !== B.n) throw new Error('whitney: the two curves have turning numbers ' + A.n + ' and ' + B.n);
    var N = A.N, F = [], k, shift = TAU * Math.round((A.F[0] - B.F[0]) / TAU);                 /* B's angles taken on the branch nearest A's at the start */
    for (k = 0; k < N; k++) F.push((1 - u) * A.F[k] + u * (B.F[k] + shift));
    return fromAngles(F, N, (1 - u) * A.L + u * B.L, [(1 - u) * A.c[0] + u * B.c[0], (1 - u) * A.c[1] + u * B.c[1]]);
  }
  // the straight way: each point goes in a straight line to the point with the same number
  function straight(A, B, u) {
    var N = A.N, pts = [], k, least = Infinity, L = (1 - u) * A.L + u * B.L;
    for (k = 0; k < N; k++) pts.push([(1 - u) * A.pts[k][0] + u * B.pts[k][0], (1 - u) * A.pts[k][1] + u * B.pts[k][1]]);
    for (k = 0; k < N; k++) { var q = pts[(k + 1) % N], s = Math.hypot(q[0] - pts[k][0], q[1] - pts[k][1]) / (L / N); if (s < least) least = s; }
    return { pts: pts, least: least };
  }
  // where the straight way must kink: the places where the two curves' directions are exactly opposite.  Each is given with
  // the sense in which the difference of angles passes an odd multiple of pi (+1 rising, -1 falling), and the moment u.
  function kinks(A, B) {
    var N = A.N, out = [], k, shift = TAU * Math.round((A.F[0] - B.F[0]) / TAU), d0, d1, m;
    for (k = 0; k < N; k++) { d0 = B.F[k] + shift - A.F[k]; d1 = B.F[k + 1] + shift - A.F[k + 1];
      var lo = Math.min(d0, d1), hi = Math.max(d0, d1);
      for (m = Math.ceil((lo - Math.PI) / TAU); Math.PI + TAU * m <= hi; m++) { var v = Math.PI + TAU * m; if (v > lo && v <= hi) out.push({ k: k, sense: d1 > d0 ? 1 : -1, u: A.L / (A.L + B.L) }); } }
    return out;
  }
  // every crossing of the polygon with itself: [i, j, x, y, sign], i < j, sign that of the cross product of edge i with edge j
  function crossings(pts) {
    var N = pts.length, out = [], i, j;
    for (i = 0; i < N; i++) { var a = pts[i], b = pts[(i + 1) % N], rx = b[0] - a[0], ry = b[1] - a[1];
      for (j = i + 2; j < N; j++) { if (i === 0 && j === N - 1) continue; var c = pts[j], d = pts[(j + 1) % N], sx = d[0] - c[0], sy = d[1] - c[1], den = rx * sy - ry * sx; if (den === 0) continue;
        var t = ((c[0] - a[0]) * sy - (c[1] - a[1]) * sx) / den, w = ((c[0] - a[0]) * ry - (c[1] - a[1]) * rx) / den;
        if (t >= 0 && t < 1 && w >= 0 && w < 1) out.push([i, j, a[0] + t * rx, a[1] + t * ry, den > 0 ? 1 : -1]); } }
    return out;
  }
  // Whitney's Theorem 2: begin at an outside point (the lowest), mu = +1 or -1 as the curve leaves it rightward or leftward;
  // a crossing first passed along edge i and then along edge j is positive when edge j turns clockwise from edge i.
  function theorem2(pts) {
    var N = pts.length, s = 0, k, rot = [];
    for (k = 1; k < N; k++) if (pts[k][1] < pts[s][1] || (pts[k][1] === pts[s][1] && pts[k][0] < pts[s][0])) s = k;
    for (k = 0; k < N; k++) rot.push(pts[(s + k) % N]);
    var mu = rot[1][0] - rot[N - 1][0] > 0 ? 1 : -1, cr = crossings(rot), plus = 0, minus = 0;
    for (k = 0; k < cr.length; k++) { if (cr[k][4] < 0) plus++; else minus++; }
    return { mu: mu, plus: plus, minus: minus, n: mu + plus - minus, start: s };
  }
  function rng(seed) { var a = seed >>> 0; return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  // a random closed curve of turning number n: its direction turns n times steadily, with J waves of random size laid over
  function randomCurve(rand, n, J, amp, N) {
    var a = [], ph = [], j, k, F = [];
    for (j = 1; j <= J; j++) { a.push(amp * (0.3 + rand()) / Math.sqrt(j)); ph.push(TAU * rand()); }
    var rot = TAU * rand();
    for (k = 0; k < N; k++) { var t = (k + 0.5) / N, f = rot + TAU * n * t; for (j = 1; j <= J; j++) f += a[j - 1] * Math.sin(TAU * j * t + ph[j - 1]); F.push(f); }
    return fromAngles(F, N, TAU, [0, 0]).pts;
  }
  // the plainest curve of each class: a circle for 1 and -1, a circle wound |n| times with its strands held apart, a figure of eight for 0
  function standard(n, N) {
    var pts = [], k, t;
    for (k = 0; k < N; k++) { t = TAU * (k + 0.37) / N;                                    /* begun a little off the figure of eight's crossing, so that no corner sits on it */
      if (n === 0) pts.push([Math.sin(t), Math.sin(t) * Math.cos(t)]);
      else { var r = Math.abs(n) === 1 ? 1 : 1 + 0.32 * Math.cos(t); pts.push([r * Math.cos(n * t), r * Math.sin(n * t)]); } }
    return resample(pts, N);
  }
  function mirror(pts) { return pts.map(function (p) { return [p[0], -p[1]]; }); }
  function rotate(pts, a) { var c = Math.cos(a), s = Math.sin(a); return pts.map(function (p) { return [c * p[0] - s * p[1], s * p[0] + c * p[1]]; }); }
  function shift(pts, k) { var N = pts.length, out = [], i; for (i = 0; i < N; i++) out.push(pts[(i + k) % N]); return out; }
  // the least speed of Whitney's deformation from A to B over nineteen moments
  function clearance(A, B) { var least = Infinity, i; for (i = 1; i <= 19; i++) { var w = whitney(A, B, i / 20); if (w.least < least) least = w.least; } return least; }
  // the target begun at whichever of sixteen places keeps Whitney's deformation from A furthest from a kink.  (Turning the
  // target changes nothing, since it adds the same angle to every step; the referee showed me that.)  Whitney's own remedy
  // for class 0 is another; this one is mine, and is tried, not proved.
  function lay(A, pts) {
    var best = null, k, N = pts.length;
    for (k = 0; k < 16; k++) { var B = shape(shift(pts, Math.round(k * N / 16))); if (B.n !== A.n) continue;
      var c = clearance(A, B); if (!best || c > best.clear + 1e-12) best = { shape: B, clear: c, start: k }; }
    return best;
  }
  // the sharpest turn between two steps, in radians: near pi the polygon doubles back on itself and has no direction there
  function sharpest(pts) { var F = angles(pts), m = 0, k; for (k = 0; k < pts.length; k++) m = Math.max(m, Math.abs(F[k + 1] - F[k])); return m; }
  var api = { TAU: TAU, wrap: wrap, length: length, resample: resample, angles: angles, turning: turning, centroid: centroid, shape: shape, fromAngles: fromAngles, whitney: whitney, straight: straight, kinks: kinks, crossings: crossings, theorem2: theorem2, rng: rng, randomCurve: randomCurve, standard: standard, mirror: mirror, rotate: rotate, shift: shift, clearance: clearance, lay: lay, sharpest: sharpest };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.CCore = api;
})(this);

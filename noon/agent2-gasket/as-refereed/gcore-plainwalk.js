// gcore.js -- integral Apollonian circle packings, for the page and its tests.  No DOM.
// Sources: Graham, Lagarias, Mallows, Wilks, Yan, "Apollonian circle packings: number theory" (2003) for root quadruples
// and the walk over the Apollonian group; Haag, Kertzer, Rickards, Stange, "The local-global conjecture for Apollonian
// circle packings is false" (2024) for the residues modulo 24, the sign chi_2 and the families that never occur.
// A circle is [b, X, Y]: its curvature b and b times its centre.  For four mutually tangent circles, the other circle
// tangent to three of them is 2 * (the sum of those three) - the fourth, in each of the three coordinates; so if the
// first four are whole numbers, every circle of the packing is, and nothing here is ever rounded.
(function (root) {
  'use strict';
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function isDescartes(q) { var s = q[0] + q[1] + q[2] + q[3]; return s > 0 && s * s === 2 * (q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3]); }
  function isPrimitive(q) { return gcd(gcd(q[0], q[1]), gcd(q[2], q[3])) === 1; }
  // the reduction algorithm of the 2003 paper: while some move makes the sum smaller, make it; then sort
  function reduce(q) { if (!isDescartes(q)) throw new Error('not a Descartes quadruple'); q = q.slice(); for (var guard = 0; guard < 1e6; guard++) { var s = q[0] + q[1] + q[2] + q[3], done = true; for (var i = 0; i < 4; i++) { var nw = 2 * (s - q[i]) - q[i]; if (nw < q[i]) { q[i] = nw; done = false; break; } } if (done) break; } return q.sort(function (a, b) { return a - b; }); }
  // the Kronecker symbol (a / n)
  function kron(a, n) {
    if (n === 0) return Math.abs(a) === 1 ? 1 : 0; var s = 1, v = 0, t;
    if (n < 0) { n = -n; if (a < 0) s = -s; }
    while (n % 2 === 0) { n /= 2; v++; }
    if (v) { if (a % 2 === 0) return 0; if (v % 2 === 1) { t = ((a % 8) + 8) % 8; if (t === 3 || t === 5) s = -s; } }
    a = ((a % n) + n) % n;
    while (a) { while (a % 2 === 0) { a /= 2; t = n % 8; if (t === 3 || t === 5) s = -s; } t = a; a = n; n = t; if (a % 4 === 3 && n % 4 === 3) s = -s; a = a % n; }
    return n === 1 ? s : 0;
  }
  // chi_2 of a circle of curvature n > 0 tangent to a circle of curvature m, gcd(n, m) = 1, n + m > 0 (the 2024 paper's Definition 4.3 with rho = n + m)
  function chi2pair(n, m) { var rho = n + m, r = n % 4; return r === 0 || r === 1 ? kron(rho, n) : r === 2 ? kron(-rho, n / 2) : kron(2 * rho, n); }
  // chi_2 of the packing: from every such pair in the root quadruple and the quadruples one and two moves from it.  Returns { sign, pairs, agree }
  function chi2(rootq) {
    var seen = [], pairs = 0, quads = [rootq.slice()], i, j, k, q, s, c;
    for (k = 0; k < 4; k++) { q = rootq.slice(); s = q[0] + q[1] + q[2] + q[3]; q[k] = 2 * (s - q[k]) - q[k]; quads.push(q); for (j = 0; j < 4; j++) if (j !== k) { c = q.slice(); s = c[0] + c[1] + c[2] + c[3]; c[j] = 2 * (s - c[j]) - c[j]; quads.push(c); } }
    quads.forEach(function (q) { for (i = 0; i < 4; i++) for (j = 0; j < 4; j++) if (i !== j && q[i] > 0 && gcd(q[i], q[j]) === 1 && q[i] + q[j] > 0) { pairs++; c = chi2pair(q[i], q[j]); if (seen.indexOf(c) < 0) seen.push(c); } });
    return { sign: seen.length === 1 ? seen[0] : null, pairs: pairs, agree: seen.length === 1 };
  }
  // the residues modulo 24 that occur (the 2024 paper's Proposition 2.1 with its Lemmas 3.A, 3.B, 3.D), from the root quadruple alone
  function residues(rootq) {
    var r3 = 0, r8 = null, i, r, out = [];
    for (i = 0; i < 4; i++) { r = ((rootq[i] % 3) + 3) % 3; if (r) r3 = r; r = ((rootq[i] % 8) + 8) % 8; if (r % 2) r8 = r === 1 ? [0, 1, 4] : r === 5 ? [0, 4, 5] : [2, 3, 6, 7]; }
    for (r = 0; r < 24; r++) if ((r % 3 === 0 || r % 3 === r3) && r8.indexOf(r % 8) >= 0) out.push(r);
    return out;
  }
  // Theorem 2.4 of the 2024 paper: type -> the families u n^2 and u n^4 none of whose members is a curvature
  var TABLE = { '6,1,1,1': [[], []], '6,1,1,-1': [[], [1, 4, 9, 36]], '6,1,-1': [[1, 2, 3, 6], []], '6,5,1': [[2, 3], []], '6,5,-1': [[1, 6], []], '6,13,1': [[2, 6], []], '6,13,-1': [[1, 3], []],
    '6,17,1,1': [[3, 6], [9, 36]], '6,17,1,-1': [[3, 6], [1, 4]], '6,17,-1': [[1, 2], []], '8,7,1': [[3, 6], []], '8,7,-1': [[2], []], '8,11,1': [[], []], '8,11,-1': [[2, 3, 6], []] };
  function type(rootq) {                       // { res, x, k, chi2, quartic: true where the type has a fourth entry, key (without the fourth), quad: families u n^2 }
    var res = residues(rootq), k = res.filter(function (r) { return gcd(r, 24) === 1; })[0], c = chi2(rootq).sign, quartic = res.length === 6 && (k === 1 || k === 17) && c === 1;
    var key = res.length + ',' + k + ',' + c; return { res: res, x: res.length, k: k, chi2: c, quartic: quartic, key: key, quad: quartic ? (k === 17 ? [3, 6] : []) : (TABLE[key] || [[], []])[0] };
  }
  function isSquare(n) { var r = Math.round(Math.sqrt(n)); return r * r === n; }
  function inFamily(n, fam) { for (var i = 0; i < fam.length; i++) if (n % fam[i] === 0 && isSquare(n / fam[i])) return fam[i]; return 0; }

  // which curvatures up to N occur: a walk over the Apollonian group from the root quadruple (the 2003 paper's Theorem 3.3)
  function enumerate(rootq, N) {
    var bits = new Uint8Array((N >> 3) + 2), circles = 0, strip = rootq[0] === 0 && rootq[1] === 0, i, q = rootq.slice(), stack = [], sp = 0, last, s, nw, top;
    function mark(c) { if (c > 0 && c <= N) bits[c >> 3] |= 1 << (c & 7); }
    for (i = 0; i < 4; i++) { mark(q[i]); circles++; }
    // an explicit stack of frames [q0, q1, q2, q3, last, next index to try]
    stack = [q[0], q[1], q[2], q[3], -1, 0]; sp = 6;
    while (sp) {
      top = sp - 6; i = stack[top + 5];
      if (i > 3) { sp -= 6; continue; }
      stack[top + 5] = i + 1; last = stack[top + 4]; if (i === last) continue;
      s = stack[top] + stack[top + 1] + stack[top + 2] + stack[top + 3]; nw = 2 * (s - stack[top + i]) - stack[top + i];
      if (nw > N) continue; if (last < 0 && strip && nw <= stack[top + i] && stack[top + i] === 1) continue;
      circles++; mark(nw);
      stack[sp] = stack[top]; stack[sp + 1] = stack[top + 1]; stack[sp + 2] = stack[top + 2]; stack[sp + 3] = stack[top + 3]; stack[sp + i] = nw; stack[sp + 4] = i; stack[sp + 5] = 0; sp += 6;
    }
    return { bits: bits, circles: circles, N: N, has: function (c) { return c > 0 && c <= N && (bits[c >> 3] & (1 << (c & 7))) !== 0; } };
  }
  function missing(rootq, N, en) { en = en || enumerate(rootq, N); var res = residues(rootq), ok = [], out = [], c; for (c = 0; c < 24; c++) ok[c] = res.indexOf(c) >= 0; for (c = 1; c <= N; c++) if (ok[c % 24] && !en.has(c)) out.push(c); return out; }

  // a place for the root quadruple in the plane with every curvature-times-centre a pair of whole numbers.  Two circles
  // [b1, X1, Y1], [b2, X2, Y2] touch when (b2 X1 - b1 X2)^2 + (b2 Y1 - b1 Y2)^2 = (b1 + b2)^2.  Found by search.
  function touching(c1, c2) { var u = c2[0] * c1[1] - c1[0] * c2[1], v = c2[0] * c1[2] - c1[0] * c2[2], s = c1[0] + c2[0]; return u * u + v * v === s * s; }
  function reps(n) { var out = [], x, y; n = Math.abs(n); for (x = -n; x <= n; x++) { y = Math.round(Math.sqrt(n * n - x * x)); if (x * x + y * y === n * n) { out.push([x, y]); if (y) out.push([x, -y]); } } return out; }   // p^2 + q^2 = n^2
  function place(rootq) {
    var a = rootq[0], b = rootq[1], c = rootq[2], d = rootq[3], A = -a, X1, Y1, i2, i3, i4, r2, r3, r4, c1, c2, c3, c4, v;
    if (a === 0 && b === 0) return { strip: true, circles: [[0, 0, -1], [0, 0, 1], [1, 0, 0], [1, 2, 0]] };          // the lines y = -1 and y = 1, unit circles at 0 and 2
    if (a >= 0) throw new Error('not a root quadruple with an outer circle');
    r2 = reps(a + b); r3 = reps(a + c); r4 = reps(a + d);
    function cand(bj, list, X1, Y1) { var out = [], k, x, y; for (k = 0; k < list.length; k++) { x = bj * X1 - list[k][0]; y = bj * Y1 - list[k][1]; if (x % a === 0 && y % a === 0) out.push([bj, x / a + 0, y / a + 0]); } return out; }
    for (X1 = 0; X1 < A; X1++) for (Y1 = 0; Y1 < A; Y1++) {
      c1 = [a, X1, Y1]; var l2 = cand(b, r2, X1, Y1); if (!l2.length) continue; var l3 = cand(c, r3, X1, Y1), l4 = cand(d, r4, X1, Y1);
      for (i2 = 0; i2 < l2.length; i2++) { c2 = l2[i2]; for (i3 = 0; i3 < l3.length; i3++) { c3 = l3[i3]; if (!touching(c2, c3)) continue; if (c3[1] === c2[1] && c3[2] === c2[2] && c === b) continue;
          for (i4 = 0; i4 < l4.length; i4++) { c4 = l4[i4]; if (touching(c2, c4) && touching(c3, c4) && !(c4[1] === c3[1] && c4[2] === c3[2] && d === c) && !(c4[1] === c2[1] && c4[2] === c2[2] && d === b)) return { strip: false, circles: [c1, c2, c3, c4] }; } } }
    }
    throw new Error('no integral place found');
  }

  // the circles of the packing that meet a rectangle and are at least minR in radius.  view = [x0, y0, x1, y1].
  // Every circle made by a move, and all that follow from it, lie in the gap between the three circles the move keeps,
  // and that gap lies inside the circle through their three points of contact; if that circle misses the view, or the
  // new circle is already too small, the walk goes no further that way.  out(b, X, Y) is called for each circle found.
  function inView(P, view, minR, out, budget) {
    var x0 = view[0], y0 = view[1], x1 = view[2], y1 = view[3], count = 0, visits = 0, maxB = 1 / minR;
    function show(c) { var b = c[0], r, cx, cy; if (b === 0) { out(c[0], c[1], c[2]); count++; return; } r = 1 / Math.abs(b); cx = c[1] / b; cy = c[2] / b; if (cx + r >= x0 && cx - r <= x1 && cy + r >= y0 && cy - r <= y1) { out(c[0], c[1], c[2]); count++; } }
    function contact(c1, c2) { var s = c1[0] + c2[0]; return [(c1[1] + c2[1]) / s, (c1[2] + c2[2]) / s]; }
    // does the gap of the three circles (on the side where the point (px, py) is) possibly meet the view?
    function gapMeets(c1, c2, c3, px, py) {
      var p = contact(c1, c2), q = contact(c1, c3), r = contact(c2, c3), ax = q[0] - p[0], ay = q[1] - p[1], bx = r[0] - p[0], by = r[1] - p[1], det = 2 * (ax * by - ay * bx);
      if (Math.abs(det) < 1e-12 * (Math.abs(ax) + Math.abs(ay)) * (Math.abs(bx) + Math.abs(by))) return true;                    // three points in a line: no bound
      var a2 = ax * ax + ay * ay, b2 = bx * bx + by * by, ox = p[0] + (by * a2 - ay * b2) / det, oy = p[1] + (ax * b2 - bx * a2) / det, R = Math.sqrt((ox - p[0]) * (ox - p[0]) + (oy - p[1]) * (oy - p[1]));
      var dc = Math.sqrt((px - ox) * (px - ox) + (py - oy) * (py - oy)); if (dc > R) return true;                                // the gap is the outside of that circle: no bound
      var dx = ox < x0 ? x0 - ox : ox > x1 ? ox - x1 : 0, dy = oy < y0 ? y0 - oy : oy > y1 ? oy - y1 : 0; return dx * dx + dy * dy <= R * R * (1 + 1e-9);
    }
    function walk(q, last) {
      var i, j, s0, s1, s2, nw, o, b, keep;
      for (i = 0; i < 4; i++) { if (i === last) continue; if (budget && visits > budget) return;
        if (P.strip && last < 0 && i > 1) continue;                                                                               // the strip's translates are drawn by its period, not walked
        s0 = 0; s1 = 0; s2 = 0; for (j = 0; j < 4; j++) if (j !== i) { s0 += q[j][0]; s1 += q[j][1]; s2 += q[j][2]; }
        nw = [2 * s0 - q[i][0], 2 * s1 - q[i][1], 2 * s2 - q[i][2]]; b = nw[0]; visits++;
        if (b > maxB) continue;
        keep = []; for (j = 0; j < 4; j++) if (j !== i) keep.push(q[j]);
        if (!(P.strip && keep[0][0] === 0 && keep[1][0] === 0) && !gapMeets(keep[0], keep[1], keep[2], nw[1] / b, nw[2] / b)) continue;
        show(nw); o = q[i]; q[i] = nw; walk(q, i); q[i] = o; }
    }
    if (P.strip) {                                               // one period (between the unit circles at 0 and 2), moved along by twos
      var k0 = Math.floor((x0 - 2) / 2), k1 = Math.ceil((x1 + 2) / 2), k, base = P.circles, sv = view;
      for (k = k0; k <= k1; k++) { var sh = 2 * k, q = base.map(function (c) { return [c[0], c[1] + c[0] * sh, c[2]]; });
        show(q[2]); if (k === k0) { out(0, 0, -1); out(0, 0, 1); count += 2; }
        walk(q, -1); }
      return { count: count, visits: visits };
    }
    var q = P.circles.map(function (c) { return c.slice(); }); for (var i = 0; i < 4; i++) show(q[i]); walk(q, -1);
    return { count: count, visits: visits };
  }
  var api = { gcd: gcd, isDescartes: isDescartes, isPrimitive: isPrimitive, reduce: reduce, kron: kron, chi2pair: chi2pair, chi2: chi2, residues: residues, type: type, TABLE: TABLE,
    isSquare: isSquare, inFamily: inFamily, enumerate: enumerate, missing: missing, touching: touching, place: place, inView: inView };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.Gasket = api;
})(typeof window !== 'undefined' ? window : this);

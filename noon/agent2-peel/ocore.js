/* ocore.js: peeling a cloud of points, layer by layer. Pure functions, no page, no files.
   Noon (agent2), 24 November 2026.

   Points have whole-number coordinates smaller than 2^25 in size, so that every "which side of the line?" is exact
   in ordinary JavaScript numbers (products below 2^53).
   A layer is every remaining point on the boundary of the convex hull of the remaining points. */
(function (root) {
  'use strict';
  var RAD = 2097152;                 /* 2^21: the radius of the disc; the other shapes have the same area */
  var LIMIT = 33554432;              /* 2^25 */
  var ALPHA = 1.326;                 /* the constant, as this study measured it; Calder and Smart's suggestion was 4/3 */

  function rng(seed) {               /* mulberry32: a small generator, good enough for a picture */
    var s = seed >>> 0;
    return function () {
      s = (s + 0x6D2B79F5) >>> 0;
      var t = Math.imul(s ^ (s >>> 15), 1 | s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* +1 if a, b, c turn left, -1 if right, 0 if they lie in one line */
  function turn(x, y, a, b, c) {
    var v = (x[b] - x[a]) * (y[c] - y[a]) - (y[b] - y[a]) * (x[c] - x[a]);
    return v > 0 ? 1 : v < 0 ? -1 : 0;
  }

  /* is the point inside the closed polygon (even-odd rule)? px, py arrays of corners */
  function inside(px, py, qx, qy) {
    var c = false, i, j, n = px.length;
    for (i = 0, j = n - 1; i < n; j = i++) {
      if ((py[i] > qy) !== (py[j] > qy) && qx < (px[j] - px[i]) * (qy - py[i]) / (py[j] - py[i]) + px[i]) c = !c;
    }
    return c;
  }
  function polygonArea(px, py) {
    var s = 0, i, j, n = px.length;
    for (i = 0, j = n - 1; i < n; j = i++) s += px[j] * py[i] - px[i] * py[j];
    return Math.abs(s) / 2;
  }

  var SHAPES = ['disc', 'ellipse', 'square', 'triangle', 'own'];
  /* n points, uniform and independent, in a shape of the disc's area centred at 0.
     For 'own', poly = {x: [...], y: [...]} is a closed polygon, of any area, with corners less than LIMIT / 4 from 0
     each way (so that the cloud can still be stretched exactly); the points are thrown into its own bounding box. */
  function sample(shape, n, rand, poly) {
    var x = new Int32Array(n), y = new Int32Array(n), i = 0, a, b, u, v, tries = 0, maxTries = 4000 * n + 100000;
    var sqHalf = Math.floor(RAD * Math.sqrt(Math.PI) / 2), hb = Math.floor(RAD * Math.sqrt(Math.PI / Math.sqrt(3)));
    var hgt = Math.floor(hb * Math.sqrt(3)), top = Math.floor(2 * hgt / 3), bot = top - hgt;
    var ea = Math.floor(RAD * Math.sqrt(3)), eb = Math.floor(RAD / Math.sqrt(3)), bx0 = 0, bx1 = 0, by0 = 0, by1 = 0, j;
    if (SHAPES.indexOf(shape) < 0) throw new Error('unknown shape: ' + shape);
    if (shape === 'own') {
      if (!(poly && poly.x && poly.y && poly.x.length >= 3 && poly.y.length === poly.x.length)) throw new Error('a shape of your own needs at least three corners');
      bx0 = bx1 = poly.x[0]; by0 = by1 = poly.y[0];
      for (j = 0; j < poly.x.length; j++) {
        if (!(Math.abs(poly.x[j]) < LIMIT / 4 && Math.abs(poly.y[j]) < LIMIT / 4)) throw new Error('a corner of the shape is too far out');
        if (poly.x[j] < bx0) bx0 = poly.x[j]; if (poly.x[j] > bx1) bx1 = poly.x[j]; if (poly.y[j] < by0) by0 = poly.y[j]; if (poly.y[j] > by1) by1 = poly.y[j];
      }
    }
    if (!(n >= 1) || n !== Math.floor(n) || n > 2000000) throw new Error('the number of points must be a whole number from 1 to 2,000,000');
    while (i < n) {
      if (++tries > maxTries) throw new Error('the shape is too thin to fill');
      if (shape === 'disc') { a = Math.floor((rand() * 2 - 1) * RAD); b = Math.floor((rand() * 2 - 1) * RAD); if (a * a + b * b > RAD * RAD) continue; }
      else if (shape === 'ellipse') { a = Math.floor((rand() * 2 - 1) * ea); b = Math.floor((rand() * 2 - 1) * eb); u = a / ea; v = b / eb; if (u * u + v * v > 1) continue; }
      else if (shape === 'square') { a = Math.floor((rand() * 2 - 1) * sqHalf); b = Math.floor((rand() * 2 - 1) * sqHalf); }
      else if (shape === 'triangle') {
        a = Math.floor((rand() * 2 - 1) * hb); b = bot + Math.floor(rand() * hgt);
        if (Math.abs(a) * hgt > hb * (top - b)) continue;              /* outside the two slanted sides */
      } else { a = Math.floor(bx0 + rand() * (bx1 - bx0)); b = Math.floor(by0 + rand() * (by1 - by0)); if (!inside(poly.x, poly.y, a, b)) continue; }
      x[i] = a; y[i] = b; i++;
    }
    return { x: x, y: y };
  }

  /* the layers. Returns { depth: Int32Array (1 for the first layer), sizes: [0, s1, s2, ...], layers: N } */
  function peel(x, y) {
    var n = x.length, i, j, k, t, m, layer = 0, removed, a, b, c, cx, cy;
    for (i = 0; i < n; i++) if (!(Math.abs(x[i]) < LIMIT && Math.abs(y[i]) < LIMIT) || x[i] !== Math.floor(x[i]) || y[i] !== Math.floor(y[i])) throw new Error('coordinates must be whole numbers below 2^25 in size');
    var cur = new Int32Array(n), hull = new Int32Array(n + 2), depth = new Int32Array(n), sizes = [0];
    for (i = 0; i < n; i++) cur[i] = i;
    cur.sort(function (p, q) { return x[p] - x[q] || y[p] - y[q] || p - q; });
    m = n;
    while (m > 0) {
      layer++; removed = 0;
      if (m === 1) { depth[cur[0]] = layer; removed = 1; }
      else {
        /* the hull by a chain from left to right and back; the sums are written out here for speed (they are turn()) */
        k = 0;
        for (i = 0; i < m; i++) {
          c = cur[i]; cx = x[c]; cy = y[c];
          while (k >= 2) { a = hull[k - 2]; b = hull[k - 1]; if ((x[b] - x[a]) * (cy - y[a]) - (y[b] - y[a]) * (cx - x[a]) <= 0) k--; else break; }
          hull[k++] = c;
        }
        for (i = m - 2, t = k + 1; i >= 0; i--) {
          c = cur[i]; cx = x[c]; cy = y[c];
          while (k >= t) { a = hull[k - 2]; b = hull[k - 1]; if ((x[b] - x[a]) * (cy - y[a]) - (y[b] - y[a]) * (cx - x[a]) <= 0) k--; else break; }
          hull[k++] = c;
        }
        k--; if (k < 1) k = 1;
        if (k <= 2) { for (i = 0; i < m; i++) depth[cur[i]] = layer; removed = m; }       /* all in one line, or one place */
        else {
          var topV = 0, lo = 0, up = k, p, on, xmin, xmax;
          for (i = 1; i < k; i++) if (x[hull[i]] > x[hull[topV]] || (x[hull[i]] === x[hull[topV]] && y[hull[i]] > y[hull[topV]])) topV = i;
          xmin = x[hull[0]]; xmax = x[hull[topV]];
          for (i = 0; i < m; i++) {
            p = cur[i]; on = false;
            if (x[p] === xmin || x[p] === xmax) on = true;
            else {
              while (lo + 1 < topV && x[hull[lo + 1]] <= x[p]) lo++;
              if (turn(x, y, hull[lo], hull[lo + 1], p) === 0) on = true;
              else {
                while (up - 1 > topV && x[hull[up - 1]] <= x[p]) up--;
                if (turn(x, y, hull[up % k], hull[up - 1], p) === 0) on = true;
              }
            }
            if (on) { depth[p] = layer; removed++; }
          }
        }
      }
      sizes.push(removed);
      for (i = 0, j = 0; i < m; i++) if (depth[cur[i]] === 0) cur[j++] = cur[i];
      m = j;
    }
    return { depth: depth, sizes: sizes, layers: layer };
  }

  /* the points of layer k in order round the layer (counter-clockwise from the rightmost) */
  function ring(x, y, depth, k) {
    var idx = [], i, cx = 0, cy = 0;
    for (i = 0; i < depth.length; i++) if (depth[i] === k) { idx.push(i); cx += x[i]; cy += y[i]; }
    if (idx.length === 0) return idx;
    cx /= idx.length; cy /= idx.length;
    idx.sort(function (p, q) { return Math.atan2(y[p] - cy, x[p] - cx) - Math.atan2(y[q] - cy, x[q] - cx) || p - q; });
    return idx;
  }

  /* what a disc holding n points should give, by the constant measured in this study */
  function discLayers(n) { return 0.75 * ALPHA * Math.pow(n / Math.PI, 2 / 3); }
  function discSize(n, k) {            /* points on layer k of a disc of n points, by Calder and Smart's formula */
    var N = discLayers(n), f = 1 - k / N;
    return f > 0 ? 2 * Math.pow(Math.PI, 2 / 3) / ALPHA * Math.pow(n, 1 / 3) * Math.sqrt(f) : 0;
  }
  function aTot(n, layers) { return (4 / 3) * layers / Math.pow(n / Math.PI, 2 / 3); }

  /* stretch threefold one way and shear: (x, y) -> (3x + y, y). The layers must not change. */
  function stretch(x, y) {
    var n = x.length, X = new Int32Array(n), Y = new Int32Array(n), i;
    for (i = 0; i < n; i++) { X[i] = 3 * x[i] + y[i]; Y[i] = y[i]; }
    return { x: X, y: Y };
  }

  /* for a layer: the farthest and the nearest of its points from (cx, cy), as a ratio; 1 for a circle */
  function roundness(x, y, depth, k, cx, cy) {
    var mn = Infinity, mx = 0, i, d;
    for (i = 0; i < depth.length; i++) if (depth[i] === k) { d = Math.sqrt((x[i] - cx) * (x[i] - cx) + (y[i] - cy) * (y[i] - cy)); if (d < mn) mn = d; if (d > mx) mx = d; }
    return mn > 0 && mx > 0 ? mx / mn : NaN;
  }

  var api = { RAD: RAD, LIMIT: LIMIT, ALPHA: ALPHA, SHAPES: SHAPES, rng: rng, turn: turn, inside: inside, polygonArea: polygonArea, sample: sample, peel: peel,
    ring: ring, discLayers: discLayers, discSize: discSize, aTot: aTot, stretch: stretch, roundness: roundness };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ocore = api;
})(this);

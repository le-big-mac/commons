// core.js -- the river model of river.c, for the page.  No drawing in here.
// Lengths in units of D = H/(2 Cf); times in units of D^2/(E b U).  See river.c for the rules.
(function (root) {
  'use strict';
  function River(opt) {
    this.P = opt.P; this.DC = opt.DC; this.LX = opt.LX;
    this.DS = opt.DS || 0.1; this.DT = opt.DT || 0.1 * this.DS * this.DS;
    this.AMIN = opt.AMIN || 3 * this.DC; this.EVERY = opt.EVERY || 5;
    this.cap = opt.cap || 60000;
    var c = this.cap;
    this.X = new Float64Array(c); this.Y = new Float64Array(c); this.X2 = new Float64Array(c); this.Y2 = new Float64Array(c);
    this.L = new Float64Array(c); this.K = new Float64Array(c); this.I = new Float64Array(c); this.S = new Float64Array(c);
    this.NX = new Float64Array(c); this.NY = new Float64Array(c);
    this.nxt = new Int32Array(c); this.head = new Int32Array(0);
    this.N = 0; this.length = 0; this.now = 0; this.nstep = 0; this.ncut = 0; this.cutlen = 0;
    this.onCut = opt.onCut || null;       // called with (time, arc length, xs, ys) of each loop left behind
  }
  // the generator of river.c (xorshift64*), so that a seed gives the same river in both
  River.prototype.seed = function (seed) {
    var M = (1n << 64n) - 1n;
    var s = (88172645463325252n ^ ((BigInt(seed) * 2654435761n) & M)) & M;
    function rnd() {
      s ^= s >> 12n; s ^= (s << 25n) & M; s ^= s >> 27n;
      return Number(((s * 2685821657736338717n) & M) >> 11n) / 9007199254740992;
    }
    function gauss() { var u = rnd(), v = rnd(); if (u < 1e-300) u = 1e-300; return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
    var i; for (i = 0; i < 20; i++) rnd();
    this.N = Math.floor(this.LX / this.DS + 0.5);
    for (i = 0; i < this.N; i++) { this.X[i] = this.LX * i / this.N; this.Y[i] = 0.01 * gauss(); }
    this.now = 0; this.nstep = 0; this.ncut = 0; this.cutlen = 0;
  };
  River.prototype.setNodes = function (xy) {      // xy: [x0, y0, x1, y1, ...]
    this.N = xy.length / 2;
    for (var i = 0; i < this.N; i++) { this.X[i] = xy[2 * i]; this.Y[i] = xy[2 * i + 1]; }
    this.now = 0; this.nstep = 0; this.ncut = 0; this.cutlen = 0;
  };
  River.prototype.geometry = function () {
    var N = this.N, X = this.X, Y = this.Y, L = this.L, K = this.K, S = this.S, LX = this.LX, i, j, a, b, len = 0;
    for (i = 0; i < N; i++) {
      j = i + 1 < N ? i + 1 : 0;
      var dx = X[j] - X[i] + (j === 0 ? LX : 0), dy = Y[j] - Y[i];
      L[i] = Math.sqrt(dx * dx + dy * dy); S[i] = len; len += L[i];
    }
    this.length = len;
    for (i = 0; i < N; i++) {
      a = i > 0 ? i - 1 : N - 1; b = i + 1 < N ? i + 1 : 0;
      var ax = X[i] - X[a] + (i === 0 ? LX : 0), ay = Y[i] - Y[a];
      var bx = X[b] - X[i] + (b === 0 ? LX : 0), by = Y[b] - Y[i];
      var cx = ax + bx, cy = ay + by, c = Math.sqrt(cx * cx + cy * cy);
      K[i] = 2 * (ax * by - ay * bx) / (L[a] * L[i] * c);
      this.NX[i] = -cy / c; this.NY[i] = cx / c;
    }
  };
  River.prototype.upstream = function () {
    var N = this.N, L = this.L, K = this.K, I = 0, lap, i, a;
    for (lap = 0; lap < 2; lap++)
      for (i = 0; i < N; i++) {
        a = i > 0 ? i - 1 : N - 1;
        var l = L[a], E = Math.exp(-l), c2 = (1 - E * (1 + l)) / l, c1 = 1 - E;
        I = E * I + K[i] * (c1 - c2) + K[a] * c2;
        this.I[i] = I;
      }
  };
  River.prototype.respace = function () {
    var N = this.N, X = this.X, Y = this.Y, X2 = this.X2, Y2 = this.Y2, LX = this.LX, DS = this.DS;
    var lo = 0.5 * DS, hi = 1.5 * DS, i, j, m = 0, changed = false, dx, dy;
    for (i = 0; i < N; i++) {
      j = i + 1 < N ? i + 1 : 0;
      dx = X[j] - X[i] + (j === 0 ? LX : 0); dy = Y[j] - Y[i];
      if (dx * dx + dy * dy > hi * hi || dx * dx + dy * dy < lo * lo) { changed = true; break; }
    }
    if (!changed) return;
    for (i = 0; i < N; i++) {
      var a = i > 0 ? i - 1 : N - 1, k; j = i + 1 < N ? i + 1 : 0; k = j + 1 < N ? j + 1 : 0;
      var xa = X[a] - (i === 0 ? LX : 0), ya = Y[a], xi = X[i], yi = Y[i];
      var xj = X[j] + (j === 0 ? LX : 0), yj = Y[j], xk = X[k] + ((j === 0 || k === 0) ? LX : 0), yk = Y[k];
      dx = xj - xi; dy = yj - yi; var d2 = dx * dx + dy * dy, ex, ey;
      if (m > 0 && i > 0) { ex = xi - X2[m - 1]; ey = yi - Y2[m - 1]; if (ex * ex + ey * ey < lo * lo) continue; }
      if (i === N - 1 && m > 1) { ex = X2[0] + LX - xi; ey = Y2[0] - yi; if (ex * ex + ey * ey < lo * lo) continue; }
      X2[m] = xi; Y2[m] = yi; m++;
      if (d2 > hi * hi) {
        var parts = Math.ceil(Math.sqrt(d2) / DS), q;
        for (q = 1; q < parts; q++) {
          var t = q / parts, t2 = t * t, t3 = t2 * t;
          var w0 = -0.5 * t3 + t2 - 0.5 * t, w1 = 1.5 * t3 - 2.5 * t2 + 1, w2 = -1.5 * t3 + 2 * t2 + 0.5 * t, w3 = 0.5 * t3 - 0.5 * t2;
          X2[m] = w0 * xa + w1 * xi + w2 * xj + w3 * xk; Y2[m] = w0 * ya + w1 * yi + w2 * yj + w3 * yk; m++;
          if (m >= this.cap - 2) throw new Error('too many nodes');
        }
      }
    }
    this.N = m; X.set(X2.subarray(0, m)); Y.set(Y2.subarray(0, m));
  };
  River.prototype.cutoff = function () {
    var N, X = this.X, Y = this.Y, X2 = this.X2, Y2 = this.Y2, S = this.S, LX = this.LX, DC = this.DC, i, c, q;
    this.geometry(); N = this.N;
    var ymin = Infinity, ymax = -Infinity;
    for (i = 0; i < N; i++) { if (Y[i] < ymin) ymin = Y[i]; if (Y[i] > ymax) ymax = Y[i]; }
    var gx = Math.floor(LX / DC); if (gx < 3) gx = 3;
    var cw = LX / gx, gy0 = ymin - DC, gy = Math.ceil((ymax - ymin + 2 * DC) / DC) + 1;
    if (gx * gy > this.head.length) this.head = new Int32Array(gx * gy * 2);
    var head = this.head, nxt = this.nxt;
    for (c = 0; c < gx * gy; c++) head[c] = -1;
    for (i = N - 1; i >= 0; i--) {
      var xm = X[i] - LX * Math.floor(X[i] / LX), cx = Math.floor(xm / cw); if (cx >= gx) cx = gx - 1;
      var cy = Math.floor((Y[i] - gy0) / DC);
      c = cy * gx + cx; nxt[i] = head[c]; head[c] = i;
    }
    for (i = 0; i < N; i++) {
      xm = X[i] - LX * Math.floor(X[i] / LX); cx = Math.floor(xm / cw); if (cx >= gx) cx = gx - 1;
      cy = Math.floor((Y[i] - gy0) / DC);
      var ax, ay, best = -1, bestk = 0, besta = -1, j;
      for (ay = cy - 1; ay <= cy + 1; ay++) {
        if (ay < 0 || ay >= gy) continue;
        for (ax = cx - 1; ax <= cx + 1; ax++) {
          var bx = (ax + gx) % gx;
          for (j = head[ay * gx + bx]; j >= 0; j = nxt[j]) {
            if (j <= i) continue;
            var dx = X[j] - X[i], dy = Y[j] - Y[i], k = Math.floor(dx / LX + 0.5); dx -= k * LX;
            if (dx * dx + dy * dy >= DC * DC) continue;
            var a1 = S[j] - S[i], arc;
            if (k === 0) arc = a1; else if (k === 1) arc = this.length - a1; else throw new Error('winding ' + k);
            if (arc <= this.AMIN) continue;
            if (arc > besta) { besta = arc; best = j; bestk = k; }
          }
        }
      }
      if (best >= 0) {
        j = best; var m = 0;
        if (this.onCut) {
          var xs = [], ys = [];
          if (bestk === 0) for (q = i; q <= j; q++) { xs.push(X[q]); ys.push(Y[q]); }
          else { for (q = j; q < N; q++) { xs.push(X[q]); ys.push(Y[q]); } for (q = 0; q <= i; q++) { xs.push(X[q] + LX); ys.push(Y[q]); } }
          this.onCut(this.now, besta, xs, ys);
        }
        if (bestk === 0) { for (q = 0; q <= i; q++) { X2[m] = X[q]; Y2[m] = Y[q]; m++; } for (q = j; q < N; q++) { X2[m] = X[q]; Y2[m] = Y[q]; m++; } }
        else { for (q = i; q <= j; q++) { X2[m] = X[q]; Y2[m] = Y[q]; m++; } var shift = LX * Math.floor(X2[0] / LX); for (q = 0; q < m; q++) X2[q] -= shift; }
        this.N = m; X.set(X2.subarray(0, m)); Y.set(Y2.subarray(0, m));
        this.ncut++; this.cutlen += besta;
        return true;
      }
    }
    return false;
  };
  River.prototype.step = function () {
    var i, N, X = this.X, Y = this.Y, K = this.K, I = this.I, NX = this.NX, NY = this.NY, P = this.P, DT = this.DT;
    this.geometry(); this.upstream(); N = this.N;
    for (i = 0; i < N; i++) { var V = K[i] - P * I[i]; X[i] += DT * V * NX[i]; Y[i] += DT * V * NY[i]; }
    this.nstep++; this.now = this.nstep * DT;
    this.respace();
    if (this.nstep % this.EVERY === 0) while (this.cutoff()) this.respace();
  };
  River.prototype.sinuosity = function () { this.geometry(); return this.length / this.LX; };
  // the bell a loop rings as it is cut off: the longer the loop, the lower the bell (D major pentatonic, D3 to B4)
  var SCALE = [50, 52, 54, 57, 59, 62, 64, 66, 69, 71];
  var BREAKS = [38.5, 30.4, 25.0, 22.1, 20.3, 18.3, 16.8, 15.4, 13.9];             // loop lengths, longest first, that part the ten bells about evenly
  var BELL = [[0.5, 0.25, 1.92], [1, 1, 1.49], [2.0, 0.45, 0.96], [2.76, 0.3, 0.587], [4.07, 0.18, 0.373], [5.4, 0.1, 0.213]];   // ratio, level, seconds to fall by e
  function bellFor(arc, xfrac) {         // xfrac: where across the valley the neck was, 0 to 1
    var k = 0; while (k < BREAKS.length && arc < BREAKS[k]) k++;
    return { midi: SCALE[k], gain: 0.5, pan: +(1.6 * (xfrac - Math.floor(xfrac)) - 0.8).toFixed(3) };
  }
  var api = { River: River, SCALE: SCALE, BREAKS: BREAKS, BELL: BELL, bellFor: bellFor, hz: function (m) { return 440 * Math.pow(2, (m - 69) / 12); } };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.RiverCore = api;
})(typeof window !== 'undefined' ? window : this);

// core.js -- a braided river on a lattice of cells, after the cellular model of Murray and Paola (1994, 1997), as I have it
// from a thesis that describes it (see sources.md).  No drawing in here.
//
// The bed is a grid of heights h, NY rows from the head (row 0) to the foot, NX cells across, between two walls.
// One step:
//   1. Water.  Cells of the head row are given Q0 each (all of them, or a block in the middle: FEED).  Row by row, each cell
//      passes all its water to the three cells below it (below left, below, below right), in proportion to S^N for those that
//      are downhill of it (S the slope, the diagonal ones divided by root 2; N = 0.5).  If none is downhill the water goes on
//      over the lip, in proportion to |S|^-N: mostly over the lowest.  (That last rule I had from memory of the model; the
//      thesis I read gives it for its own model and says its water rules follow Murray and Paola: see sources.md.)
//   2. Sand.  Each of those three streams carries Qs = K (Q (S + CS))^M with it if S + CS is positive, M = 2.5.
//   3. Sideways.  A cell also takes sand from a higher neighbour in its own row: KL times the slope between them times the
//      sand the cell itself is sending on.
//   4. The bed rises by what came in less what went out, all of it scaled so that the greatest change in the step is
//      LIMIT of the fall from one row to the next (so a step is not a fixed length of time: `time` adds the lengths up, in
//      units in which K = 1).  The head and foot rows are held as they were.  On a nearly smooth bed almost nothing moves,
//      the steps grow long, and the bed jitters by up to LIMIT of a row-fall a step; DTMAX, if given, caps a step's length.
(function (root) {
  'use strict';
  function rng32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function Bed(opt) {
    opt = opt || {};
    this.NX = opt.NX || 96; this.NY = opt.NY || 320;
    this.SLOPE = opt.SLOPE || 0.05;            // the fall from one row to the next, at the start
    this.NOISE = opt.NOISE === undefined ? 0.5 : opt.NOISE;   // the roughness of the starting bed, as a share of that fall
    this.Q0 = opt.Q0 || 1; this.N = opt.N || 0.5; this.M = opt.M || 2.5;
    this.CS = opt.CS === undefined ? this.SLOPE : opt.CS;
    this.LIMIT = opt.LIMIT || 0.03;            // the greatest change of height in a step, as a share of a row's fall
    this.KL = opt.KL === undefined ? 0.6 : opt.KL;
    this.SAND = opt.SAND || 0;                 // if set: sand is fed into each head cell at SAND times what a cell of a smooth sheet carries,
                                               // and the head row is no longer held fixed (it rises or falls as feed and carrying differ)
    this.LOOP = !!opt.LOOP;                    // the bed joined end to end: what leaves the foot comes in again at the head (see stepLoop)
    this.DTMAX = opt.DTMAX || Infinity;        // the longest time a step may stand for (none by default: see the note on step 4 above)
    this.FEED = opt.FEED === undefined ? 0.25 : opt.FEED;   // the share of the head row's cells that are given water (a block in the middle)
    this.i0 = Math.round(this.NX * (1 - this.FEED) / 2); this.i1 = Math.max(this.i0 + 1, Math.round(this.NX * (1 + this.FEED) / 2));
    this.total = this.Q0 * (this.i1 - this.i0);
    var wd = Math.pow(this.SLOPE / Math.SQRT2, this.N), ws = Math.pow(this.SLOPE, this.N), wt = 2 * wd + ws;
    this.sheet = 2 * Math.pow(this.Q0 * wd / wt * (this.SLOPE / Math.SQRT2 + this.CS), this.M) + Math.pow(this.Q0 * ws / wt * (this.SLOPE + this.CS), this.M);   // sand one cell of a smooth sheet sends on
    var n = this.NX * this.NY;
    this.h = new Float64Array(n); this.Q = new Float64Array(n); this.dh = new Float64Array(n); this.out = new Float64Array(n);
    this.carry = new Float64Array(this.NX); this.carry2 = new Float64Array(this.NX);
    this.steps = 0; this.seed(opt.seed || 1);
  }
  Bed.prototype.seed = function (seed) {
    var r = rng32(seed), NX = this.NX, NY = this.NY, i, j;
    for (j = 0; j < NY; j++) for (i = 0; i < NX; i++) this.h[j * NX + i] = this.SLOPE * (NY - 1 - j) + (this.LOOP || (j > 0 && j < NY - 1) ? this.NOISE * this.SLOPE * (r() - 0.5) : 0);
    for (i = 0; i < NX; i++) this.carry[i] = i >= this.i0 && i < this.i1 ? this.Q0 : 0;
    this.steps = 0; this.time = 0; this.seedUsed = seed;
  };
  // one step; returns the length of time it stood for (in units in which the sediment law has K = 1)
  Bed.prototype.step = function (hold) {             // with hold: route the water and reckon the sand, but leave the bed as it is
    if (this.LOOP) return this.stepLoop(hold);
    var NX = this.NX, NY = this.NY, h = this.h, Q = this.Q, dh = this.dh, out = this.out, N = this.N, M = this.M, CS = this.CS, K = 1;
    var rootN = N === 0.5, m25 = M === 2.5;
    function pw(x) { return rootN ? Math.sqrt(x) : Math.pow(x, N); }
    function tr(x) { return m25 ? x * x * Math.sqrt(x) : M === 1 ? x : Math.pow(x, M); }
    var i, j, k, c, d, R2 = Math.SQRT2;
    Q.fill(0); dh.fill(0); out.fill(0);
    for (i = this.i0; i < this.i1; i++) Q[i] = this.Q0;
    for (j = 0; j < NY - 1; j++) {
      for (i = 0; i < NX; i++) {
        c = j * NX + i; var q = Q[c]; if (q <= 0) continue;
        var s0 = i > 0 ? (h[c] - h[c + NX - 1]) / R2 : NaN, s1 = h[c] - h[c + NX], s2 = i < NX - 1 ? (h[c] - h[c + NX + 1]) / R2 : NaN;
        var w0 = 0, w1 = 0, w2 = 0, any = (s0 > 0) || (s1 > 0) || (s2 > 0);
        if (any) { if (s0 > 0) w0 = pw(s0); if (s1 > 0) w1 = pw(s1); if (s2 > 0) w2 = pw(s2); }
        else { if (s0 === s0) w0 = 1 / pw(Math.abs(s0) + 1e-12); w1 = 1 / pw(Math.abs(s1) + 1e-12); if (s2 === s2) w2 = 1 / pw(Math.abs(s2) + 1e-12); }
        var wsum = w0 + w1 + w2, q0 = q * w0 / wsum, q1 = q * w1 / wsum, q2 = q * w2 / wsum, e, qs;
        if (q0 > 0) { Q[c + NX - 1] += q0; e = s0 + CS; if (e > 0) { qs = K * tr(q0 * e); dh[c] -= qs; dh[c + NX - 1] += qs; out[c] += qs; } }
        if (q1 > 0) { Q[c + NX] += q1; e = s1 + CS; if (e > 0) { qs = K * tr(q1 * e); dh[c] -= qs; dh[c + NX] += qs; out[c] += qs; } }
        if (q2 > 0) { Q[c + NX + 1] += q2; e = s2 + CS; if (e > 0) { qs = K * tr(q2 * e); dh[c] -= qs; dh[c + NX + 1] += qs; out[c] += qs; } }
      }
    }
    if (this.KL > 0) for (j = 1; j < NY - 1; j++) for (i = 0; i < NX; i++) {       // sideways, from the higher bank into the stream
      c = j * NX + i; if (out[c] <= 0) continue;
      for (k = -1; k <= 1; k += 2) { if (i + k < 0 || i + k >= NX) continue; d = h[c + k] - h[c]; if (d > 0) { var ql = this.KL * d * out[c]; dh[c + k] -= ql; dh[c] += ql; } }
    }
    var gone = 0; for (i = 0; i < NX; i++) gone += dh[(NY - 1) * NX + i];
    this.gone = gone;                                   // sand passed into the foot row in this step, per unit of time
    var j0 = 1; if (this.SAND > 0) { j0 = 0; for (i = this.i0; i < this.i1; i++) dh[i] += this.SAND * this.sheet; }
    if (hold) return 0;
    var big = 0;
    for (j = j0; j < NY - 1; j++) for (i = 0; i < NX; i++) { d = Math.abs(dh[j * NX + i]); if (d > big) big = d; }
    var scale = big > 0 ? this.LIMIT * this.SLOPE / big : 0; if (scale > this.DTMAX) scale = this.DTMAX;
    for (j = j0; j < NY - 1; j++) for (i = 0; i < NX; i++) { c = j * NX + i; h[c] += scale * dh[c]; }
    this.steps++; this.time += scale; return scale;
  };
  // The bed joined end to end, like a flume that sends its water and sand round again.  The same four rules; but the foot row
  // passes its water and sand to the head row (which lies a whole bed's fall above it), no row is held fixed, and the water
  // coming in at the head in one step is what left the foot in the step before.  Sand is neither fed nor lost.
  Bed.prototype.stepLoop = function (hold) {
    var NX = this.NX, NY = this.NY, h = this.h, Q = this.Q, dh = this.dh, out = this.out, N = this.N, M = this.M, CS = this.CS, K = 1;
    var rootN = N === 0.5, m25 = M === 2.5, DROP = this.SLOPE * NY, carry = this.carry, next = this.carry2;
    function pw(x) { return rootN ? Math.sqrt(x) : Math.pow(x, N); }
    function tr(x) { return m25 ? x * x * Math.sqrt(x) : M === 1 ? x : Math.pow(x, M); }
    var i, j, k, c, d, R2 = Math.SQRT2;
    Q.fill(0); dh.fill(0); out.fill(0); next.fill(0);
    for (i = 0; i < NX; i++) Q[i] = carry[i];
    for (j = 0; j < NY; j++) {
      var last = j === NY - 1, nb = last ? 0 : (j + 1) * NX, off = last ? DROP : 0;
      for (i = 0; i < NX; i++) {
        c = j * NX + i; var q = Q[c]; if (q <= 0) continue;
        var s0 = i > 0 ? (h[c] - h[nb + i - 1] + off) / R2 : NaN, s1 = h[c] - h[nb + i] + off, s2 = i < NX - 1 ? (h[c] - h[nb + i + 1] + off) / R2 : NaN;
        var w0 = 0, w1 = 0, w2 = 0, any = (s0 > 0) || (s1 > 0) || (s2 > 0);
        if (any) { if (s0 > 0) w0 = pw(s0); if (s1 > 0) w1 = pw(s1); if (s2 > 0) w2 = pw(s2); }
        else { if (s0 === s0) w0 = 1 / pw(Math.abs(s0) + 1e-12); w1 = 1 / pw(Math.abs(s1) + 1e-12); if (s2 === s2) w2 = 1 / pw(Math.abs(s2) + 1e-12); }
        var wsum = w0 + w1 + w2, q0 = q * w0 / wsum, q1 = q * w1 / wsum, q2 = q * w2 / wsum, e, qs;
        if (q0 > 0) { if (last) next[i - 1] += q0; else Q[nb + i - 1] += q0; e = s0 + CS; if (e > 0) { qs = K * tr(q0 * e); dh[c] -= qs; dh[nb + i - 1] += qs; out[c] += qs; } }
        if (q1 > 0) { if (last) next[i] += q1; else Q[nb + i] += q1; e = s1 + CS; if (e > 0) { qs = K * tr(q1 * e); dh[c] -= qs; dh[nb + i] += qs; out[c] += qs; } }
        if (q2 > 0) { if (last) next[i + 1] += q2; else Q[nb + i + 1] += q2; e = s2 + CS; if (e > 0) { qs = K * tr(q2 * e); dh[c] -= qs; dh[nb + i + 1] += qs; out[c] += qs; } }
      }
    }
    if (this.KL > 0) for (j = 0; j < NY; j++) for (i = 0; i < NX; i++) {
      c = j * NX + i; if (out[c] <= 0) continue;
      for (k = -1; k <= 1; k += 2) { if (i + k < 0 || i + k >= NX) continue; d = h[c + k] - h[c]; if (d > 0) { var ql = this.KL * d * out[c]; dh[c + k] -= ql; dh[c] += ql; } }
    }
    var gone = 0; for (i = 0; i < NX; i++) gone += out[(NY - 1) * NX + i];
    this.gone = gone;                                   // sand passed from the foot row round to the head in this step, per unit of time
    if (hold) return 0;
    var big = 0, n = NX * NY;
    for (c = 0; c < n; c++) { d = Math.abs(dh[c]); if (d > big) big = d; }
    var scale = big > 0 ? this.LIMIT * this.SLOPE / big : 0; if (scale > this.DTMAX) scale = this.DTMAX;
    for (c = 0; c < n; c++) h[c] += scale * dh[c];
    this.carry = next; this.carry2 = carry;
    this.steps++; this.time += scale; return scale;
  };
  // how many separate streams cross row j: runs of neighbouring cells each carrying more than `cut` of all the water
  Bed.prototype.streams = function (j, cut) {
    var NX = this.NX, Q = this.Q, lim = (cut || 0.0035) * this.total, n = 0, wet = false, i;
    for (i = 0; i < NX; i++) { var w = Q[j * NX + i] > lim; if (w && !wet) n++; wet = w; }
    return n;
  };
  // over the middle half of the rows: the mean number of streams, the share of cells that are wet, the share of the water
  // carried by the fullest cell of a row, and the relief (the root mean square height about each row's mean, in row-falls)
  Bed.prototype.braiding = function (cut) {
    var a = 0, wet = 0, n = 0, top = 0, rel = 0, j, i, NX = this.NX, lim = (cut || 0.0035) * this.total;
    for (j = Math.floor(this.NY / 4); j < Math.floor(3 * this.NY / 4); j++) {
      a += this.streams(j, cut); n++; var m = 0, hm = 0, q;
      for (i = 0; i < NX; i++) { q = this.Q[j * NX + i]; if (q > lim) wet++; if (q > m) m = q; hm += this.h[j * NX + i]; }
      top += m / this.total; hm /= NX; for (i = 0; i < NX; i++) rel += (this.h[j * NX + i] - hm) * (this.h[j * NX + i] - hm);
    }
    return { streams: a / n, wet: wet / (n * NX), top: top / n, relief: Math.sqrt(rel / (n * NX)) / this.SLOPE };
  };
  // the bed as whole numbers: height above the smooth starting slope, in units of UNIT of a row's fall
  var UNIT = 1 / 512;
  Bed.prototype.dump = function () {
    var NX = this.NX, NY = this.NY, a = new Int16Array(NX * NY), i, j;
    for (j = 0; j < NY; j++) for (i = 0; i < NX; i++) a[j * NX + i] = Math.max(-32768, Math.min(32767, Math.round((this.h[j * NX + i] - this.SLOPE * (NY - 1 - j)) / (this.SLOPE * UNIT))));
    return a;
  };
  Bed.prototype.load = function (a, steps, time) {
    var NX = this.NX, NY = this.NY, i, j;
    for (j = 0; j < NY; j++) for (i = 0; i < NX; i++) this.h[j * NX + i] = this.SLOPE * (NY - 1 - j) + a[j * NX + i] * this.SLOPE * UNIT;
    this.steps = steps || 0; this.time = time || 0;
  };
  // a fingerprint of the bed, the same in node and in a browser (every bit of every height goes into it)
  Bed.prototype.hash = function () {
    var b = new Uint8Array(this.h.buffer, this.h.byteOffset, this.h.byteLength), x = 0x811c9dc5, y = 0x01000193, k;
    for (k = 0; k < b.length; k++) { x = Math.imul(x ^ b[k], 0x01000193); y = Math.imul(y ^ b[k], 0x85ebca6b) + k | 0; }
    return ('0000000' + (x >>> 0).toString(16)).slice(-8) + ('0000000' + (y >>> 0).toString(16)).slice(-8);
  };
  var api = { Bed: Bed, rng32: rng32, UNIT: UNIT };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.BraidCore = api;
})(typeof window !== 'undefined' ? window : this);

// core.js -- watered silk, as geometry.  No drawing in here.
//
// A ribbed cloth: the ribs are the weft cords, lying across the width (X from 0 to W) and stacked along the length (Y),
// one every PITCH.  No weft is quite straight: the rib that should lie at height Y lies at Y + u(X, Y), where u is a bow
// (the weft lags in the middle of the width), a skew (one selvedge ahead of the other) and a slow wander.
// The cloth is folded lengthwise in half, face inward, so the point X meets the point W - X, and the upper half may slip
// by (slipX, slipY).  Under the press, where a rib of one half lies on a rib of the other the grain is flattened;
// where it lies in the furrow between two ribs it is not.  flat() is 1 for rib on rib and 0 for rib in furrow:
//
//     flat(x, Y) = (1 + cos(2 pi (u(x, Y) - u(W - x - slipX, Y + slipY) - slipY) / PITCH)) / 2
//
// Unfolded, each half carries that mark, the one the mirror of the other.
//
// With two: true the upper layer is not the cloth's own other half but a second piece of the same make, turned over and laid
// on the first: it has its own wander and its own bow (bow2), and the same skew.  Then a bow no longer cancels.
(function (root) {
  'use strict';
  function rng32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function Cloth(opt) {
    this.W = opt.W || 1; this.L = opt.L || 2 / 3;         // width and length of the piece shown, in widths
    this.PITCH = opt.PITCH || 1 / 300;                    // one rib
    this.bow = opt.bow === undefined ? 3 : opt.bow;       // how far the weft lags in the middle, in ribs
    this.skew = opt.skew === undefined ? 1.6 : opt.skew;  // how far one selvedge is ahead of the other, in ribs
    this.wander = opt.wander === undefined ? 1.4 : opt.wander;   // the size of the slow wander, in ribs (root mean square)
    this.slipX = opt.slipX || 0; this.slipY = opt.slipY || 0;    // the slip of the upper half: across in widths, along in ribs
    this.two = !!opt.two; this.bow2 = opt.bow2 === undefined ? 1 : opt.bow2;   // a second piece laid on the first, and its bow
    this.seed(opt.seed || 1);
  }
  Cloth.prototype.seed = function (seed) {                // the wander: a dozen slow waves with random headings and phases
    this.waves = this.makeWaves(seed); this.waves2 = this.makeWaves(seed + 7919); this.seedUsed = seed;
  };
  Cloth.prototype.makeWaves = function (seed) {
    var r = rng32(seed), k, waves = [], sum = 0;
    for (k = 0; k < 12; k++) {
      var kx = (0.5 + 2.2 * r()) * 2 * Math.PI / this.W * (r() < 0.5 ? -1 : 1), ky = (0.15 + 0.7 * r()) * 2 * Math.PI / this.W, a = 0.4 + r();
      waves.push([kx, ky, 2 * Math.PI * r(), a]); sum += a * a / 2;
    }
    var norm = 1 / Math.sqrt(sum);
    for (k = 0; k < 12; k++) waves[k][3] *= norm;         // so that the wander has root mean square 1 before it is scaled
    return waves;
  };
  Cloth.prototype.u = function (X, Y, second) {           // displacement of the rib at (X, Y), in units of length; second: of the other piece
    var t = 2 * X / this.W - 1, s = 0, w = second ? this.waves2 : this.waves, k;
    for (k = 0; k < w.length; k++) s += w[k][3] * Math.sin(w[k][0] * X + w[k][1] * Y + w[k][2]);
    return this.PITCH * ((second ? this.bow2 : this.bow) * (t * t - 1) + this.skew * t / 2 + this.wander * s);
  };
  Cloth.prototype.lag = function (x, Y) {                 // how many ribs the lower half is ahead of the upper at the folded point (x, Y)
    return (this.u(x, Y) - this.u(this.W - x - this.slipX * this.W, Y + this.slipY * this.PITCH, this.two)) / this.PITCH - this.slipY;
  };
  Cloth.prototype.flat = function (x, Y) { return 0.5 * (1 + Math.cos(2 * Math.PI * this.lag(x, Y))); };
  // the mark on the unfolded cloth at (X, Y): the lower half carries flat(X, Y); the upper half was lying, turned over, at
  // x = W - X - slipX W, Y - slipY PITCH
  Cloth.prototype.mark = function (X, Y) {
    if (this.two || X <= this.W / 2) return this.flat(X, Y);     // of two pieces, the lower is the one shown, across its whole width
    return this.flat(this.W - X - this.slipX * this.W, Y - this.slipY * this.PITCH);
  };
  // the whole mark as an array, nx by ny samples over the piece
  Cloth.prototype.field = function (nx, ny) {
    var f = new Float32Array(nx * ny), i, j;
    for (j = 0; j < ny; j++) { var Y = (j + 0.5) / ny * this.L; for (i = 0; i < nx; i++) f[j * nx + i] = this.mark((i + 0.5) / nx * this.W, Y); }
    return f;
  };
  // bands crossed along a line across one half at height Y: how many times the mark goes from flattened to not
  Cloth.prototype.bands = function (Y, n) {
    var c = 0, prev = null, i;
    for (i = 0; i <= n; i++) { var s = this.flat(i / n * this.W / 2, Y) > 0.5; if (prev !== null && s !== prev) c++; prev = s; }
    return c / 2;
  };
  var api = { Cloth: Cloth, rng32: rng32 };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.MoireCore = api;
})(typeof window !== 'undefined' ? window : this);

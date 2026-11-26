/* Thunder from the shape of a lightning stroke.   Noon (agent2), 26 November 2026.
   The model is the one Glassner describes ("The Digital Ceraunoscope", IEEE CG&A, 2000) after Ribner and Roy
   (1982) and Wright and Medendorp: every point of the channel gives off, at the instant of the flash, one
   N-shaped pulse of pressure; the pulses travel at the speed of sound, weaken as one over the distance, and
   add up at the listener.  Along a straight piece the sum can be done exactly, which is what this file does.
   Everything is in a vertical plane: x along the ground, z up, in metres.  No DOM in this file. */
(function (root) {
  'use strict';
  var C = 343;          // speed of sound, m/s
  var T = 0.005;        // length of the N-shaped pulse from one point, s (Glassner: "approximately 5 ms")
  var FS = 44100;       // samples a second
  var STEP = 3;         // length of the short straight pieces, m (Glassner: "usually 3 meters")
  var KINK = 16;        // mean size of the change of direction between neighbouring pieces, degrees (Hill, as Glassner reports him)
  var LEAD = 0.01;      // silence kept before the first sound, s, so that the blur of the air has room on both sides

  function rng(seed) {                       // mulberry32: whole-number arithmetic, the same in every engine
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function normal(r) {                       // twelve uniforms: near enough to a bell, and only additions
    var s = -6;
    for (var i = 0; i < 12; i++) s += r();
    return s;
  }

  /* a polyline cut into pieces of equal length `step` along it (the last may be shorter) */
  function resample(pts, step) {
    step = step || STEP;
    var out = [[pts[0][0], pts[0][1]]], need = step;
    for (var i = 1; i < pts.length; i++) {
      var ax = pts[i - 1][0], az = pts[i - 1][1], bx = pts[i][0], bz = pts[i][1];
      var len = Math.sqrt((bx - ax) * (bx - ax) + (bz - az) * (bz - az)), at = 0;
      while (len - at >= need) {
        at += need;
        out.push([ax + (bx - ax) * at / len, az + (bz - az) * at / len]);
        need = step;
      }
      need -= len - at;
    }
    var last = pts[pts.length - 1], o = out[out.length - 1];
    if (Math.sqrt((last[0] - o[0]) * (last[0] - o[0]) + (last[1] - o[1]) * (last[1] - o[1])) > 1e-6) out.push([last[0], last[1]]);
    return out;
  }

  /* small-scale crookedness laid on a line: each short piece keeps its length and is turned from the line's own
     direction by an angle that wanders (a first-order autoregression); then the whole is turned and stretched a
     little so that it still begins and ends where the line did.  `mean` is the mean size of the change of
     direction between neighbours, in degrees. */
  function jag(pts, seed, mean) {
    var keep = 0.85, sd = (mean === undefined ? KINK : mean) * Math.PI / 180 / 0.7979 / Math.sqrt(1 + (1 - keep) * (1 - keep) / (1 - keep * keep));
    var wander = sd * sd / (1 - keep * keep);              // variance of a piece's angle to the line
    var p = resample(pts, STEP * Math.exp(-wander / 2)), r = rng(seed), n = p.length - 1;   // shorter by the mean cosine: the stretch at the end brings them back near STEP
    if (n < 2) return p;
    var out = [[p[0][0], p[0][1]]], dev = 0, x = p[0][0], z = p[0][1];
    for (var i = 0; i < n; i++) {
      var dx = p[i + 1][0] - p[i][0], dz = p[i + 1][1] - p[i][1], len = Math.sqrt(dx * dx + dz * dz);
      dev = keep * dev + sd * normal(r);
      var cs = Math.cos(dev), sn = Math.sin(dev);
      x += dx * cs - dz * sn; z += dx * sn + dz * cs;
      out.push([x, z]);
    }
    // a similarity that takes out[0] -> p[0] and out[n] -> p[n]
    var ux = out[n][0] - out[0][0], uz = out[n][1] - out[0][1], vx = p[n][0] - p[0][0], vz = p[n][1] - p[0][1];
    var d = ux * ux + uz * uz;
    if (d < 1e-9) return p;
    var a = (ux * vx + uz * vz) / d, b = (ux * vz - uz * vx) / d;      // multiply by the complex number a + ib
    for (var k = 0; k <= n; k++) {
      var qx = out[k][0] - out[0][0], qz = out[k][1] - out[0][1];
      out[k] = [p[0][0] + a * qx - b * qz, p[0][1] + b * qx + a * qz];
    }
    return out;
  }

  /* a made-up stroke from the cloud base to the ground: a few large bends, then the small crookedness */
  function stroke(seed, opts) {
    opts = opts || {};
    var top = opts.top === undefined ? 5000 : opts.top, x0 = opts.x === undefined ? 0 : opts.x, r = rng(seed);
    var bends = [[x0, 0]], z = 0, x = x0;
    while (z < top) {
      var dz = 250 + 450 * r();
      z = Math.min(top, z + dz);
      x += dz * 0.45 * normal(r);
      bends.push([x, z]);
    }
    bends.reverse();                         // from the cloud down, as the leader comes
    return jag(bends, (seed * 7919 + 13) >>> 0, opts.kink);
  }

  function arc(cx, cz, radius, a0, a1) {      // a piece of a circle about (cx, cz): angles in degrees from the ground, anticlockwise
    var pts = [], n = Math.max(2, Math.ceil(radius * Math.abs(a1 - a0) * Math.PI / 180 / STEP));
    for (var i = 0; i <= n; i++) {
      var a = (a0 + (a1 - a0) * i / n) * Math.PI / 180;
      pts.push([cx + radius * Math.cos(a), cz + radius * Math.sin(a)]);
    }
    return pts;
  }

  function measure(pts) {                    // length, and the mean size of the change of direction between neighbours (degrees)
    var len = 0, turn = 0, m = 0, prev = null;
    for (var i = 1; i < pts.length; i++) {
      var dx = pts[i][0] - pts[i - 1][0], dz = pts[i][1] - pts[i - 1][1];
      len += Math.sqrt(dx * dx + dz * dz);
      var ang = Math.atan2(dz, dx);
      if (prev !== null) { var d = ang - prev; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; turn += Math.abs(d); m++; }
      prev = ang;
    }
    return { length: len, kink: m ? turn / m * 180 / Math.PI : 0, pieces: pts.length - 1 };
  }

  function distances(pts, L) {
    var r = new Float64Array(pts.length), lo = Infinity, hi = 0, ilo = 0, ihi = 0;
    for (var i = 0; i < pts.length; i++) {
      var dx = pts[i][0] - L[0], dz = pts[i][1] - L[1];
      r[i] = Math.sqrt(dx * dx + dz * dz);
      if (r[i] < lo) { lo = r[i]; ilo = i; }
      if (r[i] > hi) { hi = r[i]; ihi = i; }
    }
    return { r: r, nearest: lo, farthest: hi, inear: ilo, ifar: ihi };
  }

  /* the air: sound that arrives a time t after the flash has come c t metres, whatever part of the channel it
     left, so the loss of the high notes can be put on afterwards as a blur whose width grows with the time of
     arrival.  Three running means of width w are close to a bell-shaped blur of standard deviation w / 2.
     AIR is that standard deviation after one kilometre, in seconds; it grows as the square root of the distance. */
  var AIR = 0.00017;
  function blur(p, t0, air) {
    var n = p.length, out = p;
    for (var pass = 0; pass < 3; pass++) {
      var q = new Float64Array(n), D = new Float64Array(n + 1);
      for (var i = 0; i < n; i++) {                       // each sample is spread over its own window, so nothing is gained or lost
        var v = out[i];
        if (v === 0) continue;
        var t = t0 + i / FS, sd = air * Math.sqrt(Math.max(0, C * t) / 1000), h = sd * FS;   // half-width of one running mean, in samples
        if (h < 0.5) { q[i] += v; continue; }
        var a = i + 0.5 - h, b = i + 0.5 + h, dens = v / (2 * h);
        if (a < 0) a = 0;
        if (b > n) b = n;
        var ia = Math.floor(a), ib = Math.floor(b);
        if (ia === ib) { q[ia] += dens * (b - a); continue; }
        q[ia] += dens * (ia + 1 - a);
        if (ib < n) q[ib] += dens * (b - ib);
        D[ia + 1] += dens; D[ib] -= dens;                 // the whole samples between
      }
      var run = 0;
      for (var k = 0; k < n; k++) { run += D[k]; q[k] += run; }
      out = q;
    }
    return out;
  }

  /* the pressure at the listener L = [x, z], from the instant the first sound arrives.
     For a straight piece from a to b, of length l, whose ends are ra and rb from the listener:
        (l / r) x the mean, over arrival times between ra/c and rb/c, of the N-shaped pulse
      = (l / r) (T c / (rb - ra)) [ M((t - ra/c)/T) - M((t - rb/c)/T) ],   M(u) = u - u^2 on 0..1, else 0,
     so each corner of the channel gives one hump M whose size is the difference of its two pieces' factors.
     A piece square-on to the listener (rb = ra) gives the N itself. */
  function thunder(pts, L, opts) {
    opts = opts || {};
    var air = opts.air === undefined ? AIR : opts.air;
    var d = distances(pts, L), r = d.r, n = pts.length;
    var t0 = d.nearest / C - LEAD, len = Math.ceil(((d.farthest - d.nearest) / C + T + LEAD) * FS) + 2 + Math.ceil(0.02 * FS);
    var p = new Float64Array(len), B = new Float64Array(n), square = 0;
    for (var k = 0; k + 1 < n; k++) {
      var dx = pts[k + 1][0] - pts[k][0], dz = pts[k + 1][1] - pts[k][1], l = Math.sqrt(dx * dx + dz * dz);
      if (l === 0) continue;
      var rm = 0.5 * (r[k] + r[k + 1]), dr = r[k + 1] - r[k];
      if (rm < 1) rm = 1;                                 // nobody stands inside the channel
      if (Math.abs(dr) < 1e-9) {                          // square-on: the N itself, each sample its mean over one sample's time
        square++;
        var tau = 0.5 * (r[k] + r[k + 1]) / C - t0, i0 = Math.ceil(tau * FS) - 1, i1 = Math.floor((tau + T) * FS) + 1, hs = 0.5 / (FS * T), gs = (l / rm) * T * FS;
        for (var i = Math.max(0, i0); i <= i1 && i < len; i++) {
          var u = (i / FS - tau) / T, up = u + hs, um = u - hs;
          p[i] += gs * ((up > 0 && up < 1 ? up - up * up : 0) - (um > 0 && um < 1 ? um - um * um : 0));
        }
      } else {
        var g = (l / rm) * (T * C / dr);
        B[k] += g; B[k + 1] -= g;
      }
    }
    for (var j = 0; j < n; j++) {
      if (B[j] === 0) continue;
      var tj = r[j] / C - t0, a0 = Math.ceil(tj * FS), a1 = Math.floor((tj + T) * FS), b = B[j];
      for (var s = Math.max(0, a0); s <= a1 && s < len; s++) { var v = (s / FS - tj) / T; if (v > 0 && v < 1) p[s] += b * (v - v * v); }
    }
    var dry = p;
    if (air > 0) p = blur(p, t0, air);
    var peak = 0, ipeak = 0, sq = 0;
    for (var m = 0; m < len; m++) { var av = Math.abs(p[m]); if (av > peak) { peak = av; ipeak = m; } sq += p[m] * p[m]; }
    return { fs: FS, t0: t0, p: p, dry: dry, peak: peak, tpeak: t0 + ipeak / FS, energy: sq / FS, nearest: d.nearest, farthest: d.farthest,
             inear: d.inear, ifar: d.ifar, first: d.nearest / C, last: d.farthest / C + T, square: square, r: r };
  }

  /* the same sum done the slow way, as a string of points: for the tests only */
  function pearls(pts, L, per) {
    var d = distances(pts, L), t0 = d.nearest / C - LEAD, len = Math.ceil(((d.farthest - d.nearest) / C + T + LEAD) * FS) + 2 + Math.ceil(0.02 * FS);
    var p = new Float64Array(len);
    for (var k = 0; k + 1 < pts.length; k++) {
      var ax = pts[k][0], az = pts[k][1], bx = pts[k + 1][0], bz = pts[k + 1][1], l = Math.sqrt((bx - ax) * (bx - ax) + (bz - az) * (bz - az));
      var rm = 0.5 * (d.r[k] + d.r[k + 1]); if (rm < 1) rm = 1;
      for (var q = 0; q < per; q++) {
        var f = (q + 0.5) / per, x = ax + (bx - ax) * f - L[0], z = az + (bz - az) * f - L[1], rr = Math.sqrt(x * x + z * z);
        var tau = rr / C - t0, i0 = Math.ceil(tau * FS), i1 = Math.floor((tau + T) * FS), w = l / per / rm;
        for (var i = Math.max(0, i0); i <= i1 && i < len; i++) { var u = (i / FS - tau) / T; if (u >= 0 && u < 1) p[i] += w * (1 - 2 * u); }
      }
    }
    return { t0: t0, p: p };
  }

  var api = { C: C, T: T, FS: FS, STEP: STEP, KINK: KINK, AIR: AIR, LEAD: LEAD, rng: rng, normal: normal, resample: resample, jag: jag, stroke: stroke, arc: arc,
              measure: measure, distances: distances, blur: blur, thunder: thunder, pearls: pearls };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.THUNDER = api;
})(typeof window !== 'undefined' ? window : this);

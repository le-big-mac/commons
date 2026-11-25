// core.js: Dr Young's rods and the lens they serve. The same sums as lantern.py (lengths in focal lengths; distances along the axis
// from the painted slider toward the screen). Used by the page and, under node, by the tests.
(function (root) {
  'use strict';
  function focus(D) {                       // where the lens must stand for a sharp image on a screen at D: [s, m]
    if (D < 4) return null;
    var s = (D - Math.sqrt(D * D - 4 * D)) / 2; return [s, (D - s) / s];
  }
  function DofM(m) { return 2 + m + 1 / m; }
  function rods(o) {                        // a: IK; a2: KN; b: KL; p: I's distance from the slider; q: L's beyond the lens; e: N's beyond the screen; yI, yL, yN: heights
    var a = o.a, r = { a: a, a2: o.a2 === undefined ? a : o.a2, b: o.b === undefined ? Math.sqrt(a * a - 1) : o.b, p: o.p === undefined ? 2 : o.p, q: o.q === undefined ? 1 : o.q,
      e: o.e || 0, yI: o.yI || 0, yL: o.yL || 0, yN: o.yN || 0 };
    r.K = function (D) {                    // the top joint: the circle about I of radius a meets the circle about N of radius a2, upper side
      var dx = D + r.e - r.p, dy = r.yN - r.yI, d = Math.sqrt(dx * dx + dy * dy);
      if (d > r.a + r.a2 || d < Math.abs(r.a - r.a2) || d === 0) return null;
      var t = (r.a * r.a - r.a2 * r.a2 + d * d) / (2 * d), h2 = r.a * r.a - t * t; if (h2 < 0) return null;
      var h = Math.sqrt(h2); return [r.p + t * dx / d - h * dy / d, r.yI + t * dy / d + h * dx / d];
    };
    r.lens = function (D) {                 // where the rods put the lens
      var k = r.K(D); if (!k) return null;
      var w2 = r.b * r.b - (k[1] - r.yL) * (k[1] - r.yL); if (w2 < 0) return null;
      return k[0] - Math.sqrt(w2) - r.q;
    };
    r.reach = function () { return r.p - r.e + Math.sqrt(Math.max((r.a + r.a2) * (r.a + r.a2) - (r.yN - r.yI) * (r.yN - r.yI), 0)); };
    return r;
  }
  function blur(D, s) {                     // the patch one point of the slider makes on the screen, as a fraction of the lens's opening
    if (s <= 1) return Infinity;
    var si = s / (s - 1); return Math.abs((D - s) - si) / si;
  }
  function light(m, s, x0) {                // the brightness of the image, up to a constant: the lens's uncovered share over the square of the screen's distance
    var open = 1;                           // x0: where Young's falling shade would shut (in focal lengths past the lens's nearest place); undefined: no shade
    if (x0 !== undefined) { var u = (x0 - (s - 1)) / x0; open = u <= 0 ? 0 : Math.min(u * u, 1); }
    var sp = DofM(m) - s; return open / (sp * sp);
  }
  var api = { focus: focus, DofM: DofM, rods: rods, blur: blur, light: light };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.LANTERN = api;
})(typeof window !== 'undefined' ? window : this);

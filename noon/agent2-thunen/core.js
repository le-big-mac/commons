// core.js -- J. H. von Thünen's isolated state (Der isolierte Staat, part 1; first published in 1826, read here in the
// Jena edition of 1910, which reprints the second edition of 1842):
// what a bushel of rye is worth on a farm so many miles from the town, what rent the land then yields under his two
// grain-farming systems, which of his rings a place belongs to, and how far a place "is" from the town when part of the
// way can go by water.  No drawing in here.  Section numbers are the book's; sources.md gives the passages.
//
// Units are the book's: miles (German ones; it does not say which); Taler (gold, five to the Louis d'or); the Berlin
// Scheffel of rye; "Körner", the yield of rye after fallow under Koppelwirtschaft, in Scheffel from 100 Mecklenburg square
// rods (section 6: "8 Schfl. von 100 [square] Rut."); land rent in Taler for 100,000 square rods of arable.
(function (root) {
  'use strict';
  var T = {};
  // ---- section 4, and the formula printed with plate III --------------------------------------------------------------
  // rye on a farm d miles from a town where it sells at a Taler the Scheffel
  T.price = function (d, a) { return ((12000 - 150 * d) * a - 136.92 * d) / (12000 + 65.88 * d); };
  T.priceShort = function (d, a) { return ((182 - 2.3 * d) * a - 2.1 * d) / (182 + d); };       // the book's "abgekürzt"
  T.priceShort15 = function (d) { return (273 - 5.5 * d) / (182 + d); };                        // section 4, town price 1 1/2
  // the same turned round: how far out rye is worth b
  T.distance = function (b, a) { return 12000 * (a - b) / (150 * a + 65.88 * b + 136.92); };
  // freight of a full load of 2,400 pounds from d miles, in Taler (section 4; town price 1 1/2)
  T.freight = function (d) { return 199.5 * d / (182 + d); };
  // ---- sections 5 and 14: land rent ------------------------------------------------------------------------------------
  // y = yield in Körner on the Koppel scale (the same soil gives 0.84 of it under three fields); b = rye's worth on the farm
  T.rentKoppel = function (b, y) { var k = 10 - y; return (1710 - 271 * k) * b - (747 - 53 * k); };
  T.rentDrei = function (b, y) { var k = 10 - y; return (1000 - 152 * k) * b - (381 - 27 * k); };
  // the price of rye at which the two systems pay alike, and at which three-field farming pays nothing
  T.priceEqual = function (y) { var k = 10 - y, den = 710 - 119 * k; return den > 0 ? (366 - 26 * k) / den : Infinity; };
  T.priceZeroDrei = function (y) { var k = 10 - y, den = 1000 - 152 * k; return den > 0 ? (381 - 27 * k) / den : Infinity; };
  T.priceZeroKoppel = function (y) { var k = 10 - y, den = 1710 - 271 * k; return den > 0 ? (747 - 53 * k) / den : Infinity; };
  // ---- the third ring.  The book derives no limit for it; it calls its extent on the plates "assumed" (text to plate
  // III): 9.4 miles at 10 Körner and 1 1/2 Taler, falling quickly with the price, nothing at 0.9 Taler.  The page takes
  // the ring's WIDTH beyond the forest ring from the plates: on plate III it shrinks in a straight line with the town's
  // price (the referee's measurements); on plates I and IV, at 1 1/2 Taler, it is 2.9 miles on soil of 8 Körner (mine)
  // and nothing below about 7.33 (the referee's).  Straight lines between those points, and the two effects multiplied,
  // are MY reading; the book gives no rule.
  T.WECHSEL = [[7.33, 0], [8, 2.9], [10, 9.4]];              // yield in Körner, width in miles at 1 1/2 Taler
  T.widthWechsel = function (a, y) {
    var P = T.WECHSEL, w = y <= P[0][0] ? 0 : y <= P[1][0] ? P[1][1] * (y - P[0][0]) / (P[1][0] - P[0][0]) : P[1][1] + (P[2][1] - P[1][1]) * (y - P[1][0]) / (P[2][0] - P[1][0]);
    return Math.max(0, w * (a - 0.9) / 0.6);
  };
  // ---- the plain state: radii of the rings on uniform soil --------------------------------------------------------------
  T.STANDARD = { a: 1.5, y: 8, free: 4, forest: 7, stock: 50, plain: 31.5 };       // sections 19, 20, 22, 23, 26
  // how far the plough goes (three-field rent falls to nothing), for town price a and yield y
  T.plain = function (a, y) { var b = T.priceZeroDrei(y); return b < a ? Math.max(0, T.distance(b, a)) : 0; };
  // The first two rings and the last "stand in direct proportion to the size of the town, and so to that of the cultivated
  // plain" (text to plate III; said there of the first two; the stock ring I scale the same way, which is my assumption).
  T.scale = function (a, y) { return T.plain(a, y) / T.plain(T.STANDARD.a, T.STANDARD.y); };
  T.rings = function (a, y) {      // outer radius of each of the six rings on uniform soil; a ring that does not occur has the radius of the one inside it
    var s = T.scale(a, y), r1 = T.STANDARD.free * s, r2 = T.STANDARD.forest * s;
    function out(b) { return b < a ? Math.max(0, T.distance(b, a)) : 0; }          // how far out rye is still worth b
    var bk = Math.max(T.priceEqual(y), T.priceZeroKoppel(y));                      // Koppel pays, and pays more than three fields, above this price
    var r4 = Math.max(out(bk), r2), r3 = Math.min(r2 + T.widthWechsel(a, y), r4);
    var r5 = Math.max(out(T.priceZeroDrei(y)), r4), r6 = Math.max(T.STANDARD.stock * s, r5);
    return [r1, r2, r3, r4, r5, r6];
  };
  T.NAMES = ['Freie Wirtschaft', 'Forstwirtschaft', 'Fruchtwechselwirtschaft', 'Koppelwirtschaft', 'Dreifelderwirtschaft', 'Viehzucht', 'Wildnis'];
  T.ENGLISH = ['free farming', 'forestry', 'crop alternation', 'enclosed farming', 'three-field farming', 'stock farming', 'wilderness'];
  // which ring a place belongs to: d = its distance from the town in miles of land carriage (see Net below), y = its own
  // yield, a = the town's price, y0 = the yield of the country at large (which sets the size of the town)
  T.ring = function (d, y, a, y0) {
    var s = T.scale(a, y0 === undefined ? y : y0);
    if (d < T.STANDARD.free * s) return 1;
    if (d < T.STANDARD.forest * s) return 2;
    var b = T.price(d, a), rk = T.rentKoppel(b, y), rd = T.rentDrei(b, y);
    if (rk > 0 && rk >= rd) return d < T.STANDARD.forest * s + T.widthWechsel(a, y) ? 3 : 4;
    if (rd > 0) return 5;
    return d < T.STANDARD.stock * s ? 6 : 7;
  };
  // ---- section 28, "ad 2": water.  "Suppose ship freight were 1/10 of land freight: then a farm on a river 100 miles from
  // the market is, for the worth of its grain and all that follows from it, like the farm 10 miles from the town."
  // A Net holds the town and any number of lines (rivers, or made roads) along which a mile costs `ratio` of a land mile.
  // eq(x, y) is the least cost, in land miles, of any way to the town: straight over land, or over land to a line, along
  // it, off it again, and so on.  Lines are cut into nodes STEP apart.  What each node costs is found first (between any
  // two nodes one may go over land, or along the line at its rate); a place may then join a line at a node or anywhere
  // between two neighbouring nodes, at the point that is cheapest (found exactly, not by trying points).
  function Net(town, lines, step) {
    this.town = town; this.step = step || 0.5; var nodes = [{ x: town.x, y: town.y, g: 0 }], edges = [], segs = [], li, i;
    for (li = 0; li < (lines || []).length; li++) {
      var L = lines[li], pts = L.pts, prev = -1;
      for (i = 0; i + 1 < pts.length; i++) {
        var ax = pts[i][0], ay = pts[i][1], bx = pts[i + 1][0], by = pts[i + 1][1], len = Math.hypot(bx - ax, by - ay), n = Math.max(1, Math.ceil(len / this.step)), k;
        for (k = (i === 0 ? 0 : 1); k <= n; k++) {
          var node = { x: ax + (bx - ax) * k / n, y: ay + (by - ay) * k / n, g: Infinity }; nodes.push(node);
          if (prev >= 0) { edges.push([prev, nodes.length - 1, Math.hypot(node.x - nodes[prev].x, node.y - nodes[prev].y) * L.ratio]); segs.push([prev, nodes.length - 1]); }
          prev = nodes.length - 1;
        }
      }
    }
    this.nodes = nodes;
    // Dijkstra over the nodes: land between any two of them, the cheaper rate along a line
    var N = nodes.length, done = new Uint8Array(N), adj = []; for (i = 0; i < N; i++) adj.push([]);
    edges.forEach(function (e) { adj[e[0]].push([e[1], e[2]]); adj[e[1]].push([e[0], e[2]]); });
    for (var round = 0; round < N; round++) {
      var best = -1, bg = Infinity; for (i = 0; i < N; i++) if (!done[i] && nodes[i].g < bg) { bg = nodes[i].g; best = i; }
      if (best < 0) break; done[best] = 1; var p = nodes[best];
      for (i = 0; i < N; i++) if (!done[i]) { var c = bg + Math.hypot(nodes[i].x - p.x, nodes[i].y - p.y); if (c < nodes[i].g) nodes[i].g = c; }
      for (i = 0; i < adj[best].length; i++) { var q = adj[best][i]; if (bg + q[1] < nodes[q[0]].g) nodes[q[0]].g = bg + q[1]; }
    }
    // keep only the nodes that can be of use to some place (a node whose own best way is to walk to another is not)
    this.xs = new Float64Array(N); this.ys = new Float64Array(N); this.gs = new Float64Array(N);
    for (i = 0; i < N; i++) { this.xs[i] = nodes[i].x; this.ys[i] = nodes[i].y; this.gs[i] = nodes[i].g; }
    // the stretches between neighbouring nodes: start, unit direction, length, cost at the start, and the slope of cost along it
    var M = segs.length; this.sx = new Float64Array(M); this.sy = new Float64Array(M); this.ux = new Float64Array(M); this.uy = new Float64Array(M); this.sl = new Float64Array(M); this.sg = new Float64Array(M); this.sr = new Float64Array(M); this.sn = new Int32Array(M);
    for (i = 0; i < M; i++) { var A = nodes[segs[i][0]], B = nodes[segs[i][1]], len2 = Math.hypot(B.x - A.x, B.y - A.y) || 1e-12;
      this.sx[i] = A.x; this.sy[i] = A.y; this.ux[i] = (B.x - A.x) / len2; this.uy[i] = (B.y - A.y) / len2; this.sl[i] = len2; this.sg[i] = A.g; this.sr[i] = Math.max(-0.999999, Math.min(0.999999, (B.g - A.g) / len2)); this.sn[i] = segs[i][0]; }
  }
  // the cheapest joining of stretch i from the place (x, y): [cost, land miles to the joining point], or null if it is at an end
  Net.prototype.join = function (i, x, y) {
    var px = x - this.sx[i], py = y - this.sy[i], along = px * this.ux[i] + py * this.uy[i], h = Math.abs(px * this.uy[i] - py * this.ux[i]), r = this.sr[i];
    var t = along - r * h / Math.sqrt(1 - r * r); if (!(t > 0 && t < this.sl[i])) return null;
    var land = Math.hypot(h, t - along); return [land + this.sg[i] + r * t, land];
  };
  Net.prototype.eq = function (x, y) {
    var xs = this.xs, ys = this.ys, gs = this.gs, best = Infinity, i, d;
    for (i = 0; i < xs.length; i++) { d = gs[i] + Math.hypot(x - xs[i], y - ys[i]); if (d < best) best = d; }
    for (i = 0; i < this.sl.length; i++) { var j = this.join(i, x, y); if (j && j[0] < best) best = j[0]; }
    return best;
  };
  // the same, saying also how much of the way is over land to the first node (0 = the town itself)
  Net.prototype.way = function (x, y) {
    var best = Infinity, at = 0, i, d, land; for (i = 0; i < this.xs.length; i++) { d = this.gs[i] + Math.hypot(x - this.xs[i], y - this.ys[i]); if (d < best) { best = d; at = i; } }
    land = Math.hypot(x - this.xs[at], y - this.ys[at]);
    for (i = 0; i < this.sl.length; i++) { var j = this.join(i, x, y); if (j && j[0] < best) { best = j[0]; land = j[1]; at = -1; } }
    return { eq: best, node: at, land: land, crow: Math.hypot(x - this.town.x, y - this.town.y) };
  };
  T.Net = Net;
  if (typeof module !== 'undefined' && module.exports) module.exports = T; else root.Thunen = T;
})(typeof window !== 'undefined' ? window : this);

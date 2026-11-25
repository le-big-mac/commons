// core.js: the arithmetic of a pointer that is turned by an angle. Used by the page (inlined by build.py) and by the tests in node.
// A hand at h, measured from the middle of the board, shows as a ring at the same distance, turned by the angle.
(function (root) {
  var P = {};
  P.turn = function (x, y, deg) { var a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a); return [c * x - s * y, s * x + c * y]; };
  // the ring's place for a hand's place, both measured from the middle
  P.ring = function (hx, hy, deg) { return P.turn(hx, hy, deg); };
  // eight places for the dot, an eighth of a turn apart, at distance R; the first is straight up on the screen (y grows downward)
  P.target = function (k, R) { var a = (k % 8) * Math.PI / 4; return [R * Math.sin(a), -R * Math.cos(a)]; };
  // a hand that only chases: it sees the ring and the dot, and moves the way the dot lies from the ring, a share g of the distance at each step
  P.chase = function (hx, hy, tx, ty, deg, g) { var r = P.ring(hx, hy, deg); return [hx + g * (tx - r[0]), hy + g * (ty - r[1])]; };
  // what such a hand does, by the equation: the ring's distance from the dot shrinks as exp(-k t cos(angle)) while it swings round,
  // so its whole path is the straight distance over cos(angle); at a quarter turn it circles, and past that it flees
  P.pathRatio = function (deg) { var c = Math.cos(deg * Math.PI / 180); return c > 1e-12 ? 1 / c : Infinity; };
  // a run of the chaser from the middle to a dot: returns the ring's path, whether it arrived within eps, and the path's length over the straight distance
  P.run = function (deg, R, k, g, eps, maxSteps) {
    var t = P.target(k, R), h = [0, 0], r = [0, 0], len = 0, path = [[0, 0]], steps = 0, d = R;
    while (steps < maxSteps && d > eps && d < 50 * R) {
      h = P.chase(h[0], h[1], t[0], t[1], deg, g); var n = P.ring(h[0], h[1], deg); len += Math.hypot(n[0] - r[0], n[1] - r[1]); r = n; path.push(r); steps++; d = Math.hypot(t[0] - r[0], t[1] - r[1]);
    }
    return { path: path, arrived: d <= eps, ratio: len / (R - (d <= eps ? d : 0)), steps: steps, dist: d, len: len };
  };
  // the length of a path of points, and that over the straight line from its first point to its last
  P.length = function (pts) { var s = 0; for (var i = 1; i < pts.length; i++) s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return s; };
  P.ratioOf = function (pts) { var a = pts[0], b = pts[pts.length - 1], d = Math.hypot(b[0] - a[0], b[1] - a[1]); return d > 0 ? P.length(pts) / d : Infinity; };
  if (typeof module !== 'undefined' && module.exports) module.exports = P; else root.PUCK = P;
})(this);

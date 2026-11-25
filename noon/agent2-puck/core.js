// core.js: the arithmetic of a pointer that is turned by an angle. Used by the page (inlined by build.py) and by the tests in node.
// A hand at h, measured from the middle of the board, shows as a ring at the same distance, turned by the angle.
// Places are as on a screen: x to the right, y downward; a positive turn is clockwise as you look at the screen.
(function (root) {
  var P = {};
  P.turn = function (x, y, deg) { var a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a); return [c * x - s * y, s * x + c * y]; };
  // the ring's place for a hand's place, both measured from the middle
  P.ring = function (hx, hy, deg) { return P.turn(hx, hy, deg); };
  // how a real mouse must be turned, clockwise from above, for its pointer to be turned by deg: the other way.
  // (The mouse reports a movement in its own frame, so a mouse turned one way turns the pointer's movement the other.)
  P.mouseTurn = function (deg) { return -deg; };
  // eight places for the dot, an eighth of a turn apart, at distance R; the first is straight up on the screen
  P.target = function (k, R) { var a = (k % 8) * Math.PI / 4; return [R * Math.sin(a), -R * Math.cos(a)]; };
  // a turn folded into 0 to 180 degrees, whichever way it goes
  P.fold = function (deg) { return Math.abs(((deg % 360) + 540) % 360 - 180); };
  // A hand that only chases moves the way the dot lies from the ring, so the ring's offset from the dot, e, obeys e' = -k R(a) e.
  // By the equation: |e| shrinks as exp(-k t cos a) while e swings round the dot; the ring's whole path is the distance closed over cos a.
  P.pathRatio = function (deg) { var c = Math.cos(P.fold(deg) * Math.PI / 180); return c > 1e-9 ? 1 / c : Infinity; };
  P.outcome = function (deg) { var a = P.fold(deg); return a < 89.999 ? 'arrives' : a < 90.001 ? 'circles' : 'runs away'; };
  // the ring's path by that equation, exactly, from the middle to the dot at t: places at equal steps of k t, until it is within eps of the
  // dot, or has gone twice round (a quarter turn), or has left a board of half-width half (past a quarter turn)
  P.spiral = function (deg, t, eps, half) {
    var a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a), e0 = [-t[0], -t[1]], d0 = Math.hypot(e0[0], e0[1]), path = [[0, 0]], out = P.outcome(deg), tau = 0, step = 0.02;
    while (tau < 400) {
      tau += step; var m = Math.exp(-tau * c), q = P.turn(e0[0], e0[1], -tau * s * 180 / Math.PI), p = [t[0] + m * q[0], t[1] + m * q[1]];
      if (Math.abs(p[0]) > half || Math.abs(p[1]) > half) break;
      path.push(p);
      if (m * d0 <= eps) break;
      if (out === 'circles' && tau * Math.abs(s) >= 4 * Math.PI) break;
    }
    return { path: path, outcome: out, ratio: P.pathRatio(deg) };
  };
  // a hand that looks and moves in steps, a share g of the distance at each look: its path, over the distance closed, is g / (1 - r),
  // where r = sqrt(1 - 2 g cos a + g g) is what each step leaves of the distance (steady when r < 1, that is 0 < g < 2 cos a)
  P.stepRatio = function (deg, g) { var r = Math.sqrt(1 - 2 * g * Math.cos(P.fold(deg) * Math.PI / 180) + g * g); return r < 1 ? g / (1 - r) : Infinity; };
  // the length of a path of points
  P.length = function (pts) { var s = 0; for (var i = 1; i < pts.length; i++) s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return s; };
  if (typeof module !== 'undefined' && module.exports) module.exports = P; else root.PUCK = P;
})(this);

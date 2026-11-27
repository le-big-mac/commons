/* The turtle that turns twice as much each step (the book's GOSPEL; HAKMEM's problem 45).   Noon (agent2), 26 November 2026.
   The rule: turn left by ANGLE, go forward one step, double ANGLE, and again.  ANGLE is p/q of a whole turn.
   Headings are kept as whole numbers of q-ths of a turn, so the turning is exact; only the places are in floating point.
   What is here: the forecast (made from p and q alone, by the rule of the write-up) and the walk (the rule carried out
   step by step, which knows nothing of the forecast).  No DOM in this file. */
(function (root) {
  'use strict';
  var QMAX = 2000000;              // the largest denominator taken: the cycle of the turns can be as long as the denominator
  var NEAR = 1e-7;                 // "at the start": within this many steps of it

  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function mod(a, m) { return ((a % m) + m) % m; }

  // "12" -> 12; null unless it is a whole number of at most seven figures, with an optional sign
  function parse(s) {
    var m = /^\s*([+\-−]?)(\d{1,7})\s*$/.exec(String(s)); if (!m) return null;
    var v = parseInt(m[2], 10); return (m[1] === '-' || m[1] === '−') ? -v : v;
  }
  function commas(n) { return String(n).replace(/\B(?=(\d{3})+$)/g, ','); }

  function factor(m) {             // [[prime, exponent], ...] of a whole number m >= 1
    var out = [], l = 2;
    while (l * l <= m) { if (m % l === 0) { var e = 0; while (m % l === 0) { m /= l; e++; } out.push([l, e]); } l += (l === 2 ? 1 : 2); }
    if (m > 1) out.push([m, 1]);
    return out;
  }
  function order2(m) {             // the least n >= 1 with 2^n = 1 modulo m (m odd; 1 for m = 1), found by doubling
    if (m === 1) return 1;
    var n = 1, x = 2 % m; while (x !== 1) { x = x * 2 % m; n++; } return n;
  }
  function val(o, l) { var k = 0; while (o % l === 0) { o /= l; k++; } return k; }

  /* The forecast.  p/q in lowest terms, q = 2^s m with m odd.  After s steps the turns repeat with period n, the order of 2
     modulo m, and a round of n steps turns the turtle through a whole number of turns.  So it is bounded exactly when one
     round ends where it began, and the rule says when: some prime power l^e exactly dividing m, e >= 2, for which l divides
     the order of 2 modulo l^e more often than it divides the order of 2 modulo l^(e-1) or modulo any other prime of m. */
  function forecast(P, Q) {
    if (Q < 0) { P = -P; Q = -Q; }
    var g = gcd(P, Q) || 1, p = P / g, q = Q / g, s = 0, m = q;
    while (m % 2 === 0) { m /= 2; s++; }
    p = mod(p, q);
    var f = factor(m), n = order2(m), serves = null, spoilt = [], squares = 0, i, j;
    for (i = 0; i < f.length; i++) {
      var l = f[i][0], e = f[i][1]; if (e < 2) continue; squares++;
      var here = val(order2(Math.pow(l, e)), l), before = val(order2(Math.pow(l, e - 1)), l), by = null;
      if (here <= before) by = { l: l, e: e, self: true };                       // 2 has no larger order modulo l^e than modulo l^(e-1): 1093 and 3511
      for (j = 0; j < f.length && !by; j++) if (j !== i) { var o = order2(f[j][0]); if (val(o, l) >= here) by = { l: l, e: e, r: f[j][0], ord: o, k: here }; }
      if (by) spoilt.push(by); else if (!serves) serves = { l: l, e: e, k: here };
    }
    return { p: p, q: q, tail: s, m: m, round: n, factors: f, squares: squares, bounded: !!serves, serves: serves, spoilt: spoilt,
             home: !!serves && s === 0, straight: m === 1 };
  }

  /* The walk.  The turtle starts at (0, 0) facing up the page; a left turn is counter-clockwise.  Turn, then step.
     home: the first step after which it is at its start, facing as it started, with its first turn to come again. */
  function walk(P, Q, nsteps) {
    if (Q < 0) { P = -P; Q = -Q; }
    var g = gcd(P, Q) || 1, q = Q / g, p = mod(P / g, q), K = 2 * Math.PI / q;
    var turn = p, head = 0, x = 0, y = 0, xs = new Float64Array(nsteps + 1), ys = new Float64Array(nsteps + 1), home = 0, there = 0;
    for (var k = 1; k <= nsteps; k++) {
      head = (head + turn) % q; turn = turn * 2 % q;
      x -= Math.sin(head * K); y += Math.cos(head * K);                          // facing up, turned left through head
      xs[k] = x; ys[k] = y;
      if (x * x + y * y < NEAR * NEAR) { if (!there) there = k; if (!home && head === 0 && turn === p) home = k; }
    }
    return { xs: xs, ys: ys, home: home, there: there, head: head, turn: turn, q: q };
  }

  /* The clock (added 27 November).  The turns of one round, after the tail, as hours on a clock of q hours: the turn after
     k steps is p 2^k of q-ths of a whole turn.  Hour 0 is at the top and the hours are counted leftwards, the way the turtle
     turns.  The steps of a round, moved to start at the centre, are hands pointing at these hours, all turned back by the
     first turn; so a round ends where it began exactly when the hours balance about the centre, and it carries the turtle
     (number of hours) x (distance of their balance point from the centre).
     kinds: the odd primes l, coming into q twice or more, for which the hours fall into regular l-gons: with every hour a,
     the hour a + q/l is marked too.  An l-gon balances, so a round whose hours fall into l-gons closes; the rule says that
     no other round does, and the tests try that on every round of Python's table. */
  function clock(P, Q) {
    var f = forecast(P, Q), q = f.q, n = f.round, t = f.p, k, K = 2 * Math.PI / q;
    for (k = 0; k < f.tail; k++) t = t * 2 % q;
    var hours = new Int32Array(n), mark = new Uint8Array(q), cx = 0, cy = 0;
    for (k = 0; k < n; k++) { hours[k] = t; mark[t] = 1; cx -= Math.sin(t * K); cy += Math.cos(t * K); t = t * 2 % q; }
    var kinds = [], i, j;
    for (i = 0; i < f.factors.length; i++) {
      var l = f.factors[i][0], step = q / l, all = f.factors[i][1] >= 2;
      for (j = 0; j < n && all; j++) if (!mark[(hours[j] + step) % q]) all = false;
      if (all) kinds.push(l);
    }
    return { q: q, n: n, tail: f.tail, hours: hours, kinds: kinds, cx: cx / n, cy: cy / n, off: Math.hypot(cx, cy) / n };
  }
  /* The rule as D. H. and Emma Lehmer put Fuchs's theorem: a round closes exactly when, for some odd prime l that comes into the
     bottom number twice or more, it is l times as long as the round of the turtle with one l taken out.  For each such prime:
     l, how many times it comes in, the length n1 of the round with one l out, and whether this round is l times that.
     (It is either l times as long or no longer.) */
  function takeOut(P, Q) {
    var f = forecast(P, Q), out = [], i;
    for (i = 0; i < f.factors.length; i++) { var l = f.factors[i][0], e = f.factors[i][1]; if (e < 2) continue;
      var n1 = order2(f.m / l); out.push({ l: l, e: e, n1: n1, long: f.round === l * n1 }); }
    return out;
  }
  // one of the l-gons the hours fall into: the hours a, a + q/l, a + 2q/l, ...
  function polygon(a, q, l) { var out = [], k; for (k = 0; k < l; k++) out.push((a + k * (q / l)) % q); return out; }

  function box(w) {
    var x0 = 0, x1 = 0, y0 = 0, y1 = 0;
    for (var k = 1; k < w.xs.length; k++) { if (w.xs[k] < x0) x0 = w.xs[k]; if (w.xs[k] > x1) x1 = w.xs[k]; if (w.ys[k] < y0) y0 = w.ys[k]; if (w.ys[k] > y1) y1 = w.ys[k]; }
    return [x0, x1, y0, y1];
  }

  /* Every odd denominator from 3 up to top, with numerator 1, by the forecast:
     kind[i] for m = 2i + 3 is 2 if the turtle is bounded, 1 if m holds the square of a prime and it is not, 0 if m holds none. */
  function census(top) {
    var kind = new Uint8Array((top - 1) >> 1), closes = 0, spoilt = 0, plain = 0;
    for (var m = 3, i = 0; m <= top; m += 2, i++) {
      var f = forecast(1, m);
      if (f.bounded) { kind[i] = 2; closes++; } else if (f.squares) { kind[i] = 1; spoilt++; } else plain++;
    }
    return { kind: kind, closes: closes, spoilt: spoilt, plain: plain, top: top };
  }

  var api = { QMAX: QMAX, NEAR: NEAR, gcd: gcd, mod: mod, parse: parse, commas: commas, factor: factor, order2: order2, val: val, forecast: forecast, walk: walk, box: box, census: census, clock: clock, polygon: polygon, takeOut: takeOut };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.GOSPEL = api;
})(typeof window !== 'undefined' ? window : this);

/* The turtle that turns a little more each step (Abelson and diSessa's INSPI).   Noon (agent2), 26 November 2026.
   The rule: forward one step, turn right by ANGLE, add INC to ANGLE, and again.
   Angles are kept as whole thousandths of a degree, so the turning is exact; only the places are in floating point.
   What is here: the forecast (made from the two numbers alone, by the book's looping lemma and its formula for
   the turning in one lap), and the walk (the rule carried out step by step, which knows nothing of the forecast).
   No DOM in this file. */
(function (root) {
  'use strict';
  var UNIT = 1000;                 // thousandths of a degree
  var FULL = 360 * UNIT;           // one whole turn
  var NEAR = 1e-7;                 // "at the start": within this many steps of it

  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function mod(a, m) { return ((a % m) + m) % m; }

  // "2", "2.5", ".5", "-0.125" -> whole thousandths of a degree; null if it is not a plain number with at most six
  // figures before the point and three after.  The minus may be the keyboard's or the one this file prints.
  function parse(s) {
    var m = /^\s*([+\-\u2212]?)(\d{0,6})(?:\.(\d{0,3}))?\s*$/.exec(String(s)); if (!m || !(m[2] || m[3])) return null;
    var frac = m[3] || ''; while (frac.length < 3) frac += '0';
    var v = parseInt(m[2] || '0', 10) * UNIT + parseInt(frac, 10); return (m[1] === '-' || m[1] === '\u2212') ? -v : v;
  }
  function show(th) {              // thousandths back to a short decimal
    var neg = th < 0, v = Math.abs(th), whole = Math.floor(v / UNIT), frac = String(v % UNIT); while (frac.length < 3) frac = '0' + frac;
    frac = frac.replace(/0+$/, ''); return (neg ? '−' : '') + whole + (frac ? '.' + frac : '');
  }

  /* The forecast.  INC is p/q of a turn in lowest terms, so the turns repeat every q steps: one lap.
     The turning in one lap is T = q ANGLE + INC q(q-1)/2 = q ANGLE + 180 p (q-1) degrees (the book's formula).
     T not a whole number of turns: the turtle comes home after q v steps, v the denominator of T/360 (looping lemma).
     T a whole number of turns: every lap is the same displacement, of length exactly the square root of q, so it never comes home. */
  function forecast(A, I) {
    var a = mod(A, FULL), i = mod(I, FULL), g = gcd(i, FULL), q = i === 0 ? 1 : FULL / g, p = i === 0 ? 0 : i / g;
    var T = mod(q * a + (FULL / 2) * ((p * (q - 1)) % 2), FULL);        // q a is below 1.3e11: exact
    if (T === 0) return { home: false, q: q, p: p, T: 0, gain: Math.sqrt(q) };
    var v = FULL / gcd(T, FULL);
    return { home: true, q: q, p: p, T: T, laps: v, steps: q * v };
  }

  /* The walk.  The turtle starts at (0, 0) facing up the page, as in Logo; a right turn is clockwise.
     home: the first step after which it is at its start, facing as it started, with its turn back at its first value. */
  function walk(A, I, n) {
    var a0 = mod(A, FULL), ang = a0, inc = mod(I, FULL), head = 0, x = 0, y = 0, K = 2 * Math.PI / FULL;
    var xs = new Float64Array(n + 1), ys = new Float64Array(n + 1), home = 0, there = 0;
    for (var k = 1; k <= n; k++) {
      x += Math.sin(head * K); y += Math.cos(head * K);
      head = (head + ang) % FULL; ang = (ang + inc) % FULL;
      xs[k] = x; ys[k] = y;
      if (x * x + y * y < NEAR * NEAR) { if (!there) there = k; if (!home && head === 0 && ang === a0) home = k; }
    }
    return { xs: xs, ys: ys, home: home, there: there, head: head, ang: ang };
  }

  function box(w, upto) {          // the least rectangle holding the corners 0..upto
    var n = upto === undefined ? w.xs.length - 1 : upto, x0 = 0, x1 = 0, y0 = 0, y1 = 0;
    for (var k = 1; k <= n; k++) { if (w.xs[k] < x0) x0 = w.xs[k]; if (w.xs[k] > x1) x1 = w.xs[k]; if (w.ys[k] < y0) y0 = w.ys[k]; if (w.ys[k] > y1) y1 = w.ys[k]; }
    return [x0, x1, y0, y1];
  }

  /* Every pair of whole degrees, INC 1 to 359 and ANGLE 0 to 359, by the forecast:
     steps[inc * 360 + angle] is the number of steps to come home, 0 for never. */
  function census() {
    var steps = new Uint16Array(360 * 360), away = 0, home = 0, longest = 0, least = 0;
    for (var inc = 1; inc < 360; inc++) for (var a = 0; a < 360; a++) {
      var f = forecast(a * UNIT, inc * UNIT);
      if (f.home) { steps[inc * 360 + a] = f.steps; home++; if (f.steps > longest) longest = f.steps; if (!least || f.steps < least) least = f.steps; } else away++;
    }
    return { steps: steps, away: away, home: home, longest: longest, least: least };
  }

  function commas(n) { return String(n).replace(/\B(?=(\d{3})+$)/g, ','); }

  var api = { UNIT: UNIT, FULL: FULL, NEAR: NEAR, gcd: gcd, mod: mod, parse: parse, show: show, forecast: forecast, walk: walk, box: box, census: census, commas: commas };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.INSPI = api;
})(typeof window !== 'undefined' ? window : this);

// The clock against the rule and against the walk, wider than the page's tests go.   usage: node wide.js ../core.js > wide.out
// (1) every odd m from 3 to 100,001 with first turn 1/m: the hours fall into polygons exactly when the forecast (the rule) says the
//     round closes, and the polygons of the prime the forecast names are among them;
// (2) 4,000 made-up fractions p/q, q up to 40,000, odd and even: the same, and the number of hours times the distance of the
//     balance point from the centre is how far the page's own walk is carried by one round.
const path = require('path'); const T = require(path.resolve(process.argv[2]));
let t0 = Date.now(), bad = 0, n = 0, closed = 0, two = 0;
for (let m = 3; m <= 100001; m += 2) { const f = T.forecast(1, m), c = T.clock(1, m); n++; if ((c.kinds.length > 0) !== f.bounded) bad++; if (c.kinds.length > 1) two++; if (f.bounded) { closed++; if (c.kinds.indexOf(f.serves.l) < 0) bad++; } }
console.log(n + ' odd m from 3 to 100,001: the clock and the rule disagree for ' + bad + '; ' + closed + ' rounds close, ' + two + ' of them falling into polygons of two kinds or more');
bad = 0; n = 0; let seed = 12345, even = 0, tails = 0, cl = 0; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
for (let i = 0; i < 4000; i++) { const q = 2 + Math.floor(rnd() * 40000), p = 1 + Math.floor(rnd() * (q - 1)), f = T.forecast(p, q), c = T.clock(p, q), w = T.walk(p, q, f.tail + f.round);
  const gain = Math.hypot(w.xs[f.tail + f.round] - w.xs[f.tail], w.ys[f.tail + f.round] - w.ys[f.tail]); n++; if (f.q % 2 === 0) even++; if (f.tail) tails++; if (f.bounded) cl++;
  if ((c.kinds.length > 0) !== f.bounded || Math.abs(c.n * c.off - gain) > 1e-7) bad++; }
console.log(n + ' made-up fractions p/q, q up to 40,000 (' + even + ' with an even bottom number in lowest terms, ' + tails + ' with a tail, ' + cl + ' whose round closes): the clock against the rule and against the walk: disagree ' + bad);

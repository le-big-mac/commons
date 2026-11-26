// How far from closed does the page's own arithmetic leave a round that closes?
// For every odd m up to 2,000,000 whose rounds close (by core.js's forecast) and are of at most 20,000 steps (the most the page
// draws), walk 1/m for one round with core.js's walk, as the page does, and see how far from its start the turtle ends.
// usage: node closed-error.js ../core.js > closed-error.out
const T = require(require('path').resolve(process.argv[2]));
let tried = 0, worst = 0, at = 0, longest = 0, skipped = 0, open = 0, least = Infinity, leastAt = 0;
const t0 = Date.now();
for (let m = 3; m <= 2000000; m += 2) {
  // the order of 2 is found by doubling; stop early if it passes 20,000
  let n = 1, x = 2 % m; while (x !== 1 && n <= 20000) { x = x * 2 % m; n++; }
  if (n > 20000) { skipped++; continue; }
  const f = T.forecast(1, m);
  const w = T.walk(1, m, n), miss = Math.hypot(w.xs[n], w.ys[n]);
  if (!f.bounded) { open++; if (miss < least) { least = miss; leastAt = m; } continue; }
  tried++; if (miss > worst) { worst = miss; at = m; } if (n > longest) longest = n;
}
console.log('odd m from 3 to 2,000,000 with a round of at most 20,000 steps: ' + (tried + open) + ' (' + skipped + ' have longer rounds and are not walked)');
console.log('of those, ' + tried + ' close by the forecast: after one round of 1/m, walked as the page walks it, the turtle is at most ' + worst.toExponential(2) + ' steps from its start (m = ' + at + '); the longest such round has ' + longest + ' steps');
console.log('the other ' + open + ' do not close: after one round of 1/m the turtle is at least ' + least.toExponential(4) + ' steps from its start (m = ' + leastAt + ')');
console.log(((Date.now() - t0) / 1000).toFixed(0) + ' s');

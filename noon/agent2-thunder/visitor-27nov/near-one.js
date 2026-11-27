// Which of sixty made-up strokes does not begin with its loudest part from 500 m, and by how much?   node near-one.js CORE.JS
const TH = require(require('path').resolve(process.argv[2]));
for (const L of [500]) for (let seed = 1001; seed < 1061; seed++) { const r = TH.thunder(TH.stroke(seed), [L, 0]), f = (r.tpeak - r.firstHeard) / (r.last - r.firstHeard);
  if (f > 0.1) console.log('seed ' + seed + ': loudest ' + (r.tpeak - r.firstHeard).toFixed(2) + ' s into a thunder of ' + (r.last - r.firstHeard).toFixed(1) + ' s (' + (100 * f).toFixed(0) + '% of the way)'); }
let worst = 0, n = 0, over = 0; for (let seed = 1; seed <= 400; seed++) { const r = TH.thunder(TH.stroke(seed), [500, 0]), f = (r.tpeak - r.firstHeard) / (r.last - r.firstHeard); n++; if (f > 0.1) over++; worst = Math.max(worst, f); }
console.log('of ' + n + ' strokes (seeds 1 to 400) from 500 m: ' + over + ' have the loudest moment after the first tenth; the latest is ' + (100 * worst).toFixed(0) + '% of the way');

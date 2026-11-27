// my own numbers for the first and fourth tips, from core.js in node
const TH = require('/home/agent2/thunder/core.js'); const mean = a => a.reduce((s, v) => s + v, 0) / a.length;
const start = r => r.firstHeard === null ? r.first : r.firstHeard;
console.log('TIP 1: 100 made-up strokes (seeds 101-200) from each place; first tenth / middle / last tenth of the thunder');
for (const x of [-500, 500, 8000]) { let a = 0, mid = 0, late = 0; const pk = [], du = [], fs = [];
  for (let s = 101; s <= 200; s++) { const r = TH.thunder(TH.stroke(s), [x, 0]), t0 = start(r), f = (r.tpeak - t0) / (r.last - t0); if (f < 0.1) a++; else if (f > 0.9) late++; else mid++; pk.push(r.peak); du.push(r.last - t0); fs.push(t0); }
  console.log('  from', x, 'm: begins with its loudest part', a, ', loudest in the middle', mid, ', in the last tenth', late, 'of 100 | mean peak', mean(pk).toExponential(2), '| mean length', mean(du).toFixed(1), 's | first sound', mean(fs).toFixed(2), 's =', (mean(fs) / Math.abs(x) * 1000).toFixed(2), 's a km'); }
console.log('TIP 4: the smooth straight stroke');
const st = TH.resample([[0, 5000], [0, 0]], 3);
for (const x of [0, 500, 3000, 5000, 8000, 9000, 9700]) { const r = TH.thunder(st, [x, 0]); let click = 0, mid = 0, eC = 0, eM = 0, eK = 0;
  for (let i = 0; i < r.p.length; i++) { const t = r.t0 + i / r.fs, a = Math.abs(r.p[i]); if (t >= r.last - 0.03) { click = Math.max(click, a); eK += a * a; } else if (t >= r.first + 0.02) { mid = Math.max(mid, a); eM += a * a; } else eC += a * a; }
  console.log('  from', x, 'm: crack', r.peak.toExponential(3), '| click', click.toExponential(3), '= crack /', (r.peak / click).toFixed(2), '| largest between = crack /', (r.peak / mid).toFixed(1), '| energy outside the crack', (100 * (eM + eK) / (eC + eM + eK)).toFixed(2) + '%'); }

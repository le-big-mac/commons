// How does the thunder of made-up strokes change with distance, in this model?   usage: node fall.js [strokes] > fall.out
// A straight channel gives a peak falling as the square root of one over the distance; a single point, as one over the distance.
// Rewritten after the referee's reading: with and without the bending of sound, where in the thunder the loudest moment
// lies, the first tenth of a second against the rest, and one step off in the crookedness.
const TH = require('./core.js');
const N = +process.argv[2] || 60, xs = [500, 1000, 2000, 4000, 8000], lx = xs.map(Math.log);
function slope(x, y) { const n = x.length, mx = x.reduce((a, b) => a + b) / n, my = y.reduce((a, b) => a + b) / n; let sxy = 0, sxx = 0; for (let i = 0; i < n; i++) { sxy += (x[i] - mx) * (y[i] - my); sxx += (x[i] - mx) * (x[i] - mx); } return sxy / sxx; }
const stat = v => { const m = v.reduce((a, b) => a + b) / v.length, sd = Math.sqrt(v.reduce((a, b) => a + (b - m) * (b - m), 0) / (v.length - 1)); return m.toFixed(2) + ' (stroke by stroke from ' + Math.min(...v).toFixed(2) + ' to ' + Math.max(...v).toFixed(2) + '; the mean good to about ' + (sd / Math.sqrt(v.length)).toFixed(2) + ')'; };
function run(label, n, seed0, strokeOpts, opts) {
  const sl = { peak: [], rms: [], head: [], rest: [] }, mean = xs.map(() => 0), dur = xs.map(() => 0), tenth = xs.map(() => 0);
  for (let s = 1; s <= n; s++) {
    const pts = TH.stroke(seed0 + s, strokeOpts), pk = [], rm = [], hd = [], rs = [];
    xs.forEach((x, i) => { const r = TH.thunder(pts, [x, 0], opts), d = r.last - r.first, i1 = Math.round((r.first + 0.1 - r.t0) * r.fs); let a = 0, b = 0;
      for (let k = 0; k < r.p.length; k++) { const v = Math.abs(r.p[k]); if (k < i1) { if (v > a) a = v; } else if (v > b) b = v; }
      pk.push(Math.log(r.peak)); rm.push(0.5 * Math.log(r.energy / d)); hd.push(Math.log(a)); rs.push(Math.log(b)); mean[i] += r.peak / n; dur[i] += d / n; if (r.tpeak - r.first < 0.1 * d) tenth[i]++; });
    sl.peak.push(slope(lx, pk)); sl.rms.push(slope(lx, rm)); sl.head.push(slope(lx, hd)); sl.rest.push(slope(lx, rs));
  }
  console.log(label + ': ' + n + ' strokes (seeds ' + (seed0 + 1) + ' on)');
  console.log('   mean peak at ' + xs.join(', ') + ' m: ' + mean.map(v => v.toFixed(4)).join(', ') + '; mean length of the thunder: ' + dur.map(v => v.toFixed(1)).join(', ') + ' s');
  console.log('   strokes whose loudest moment is in the first tenth of the thunder: ' + tenth.join(', ') + ' of ' + n);
  console.log('   the peak falls as the distance to the power ' + stat(sl.peak));
  console.log('   the loudest moment of the first tenth of a second: ' + stat(sl.head) + '; of the rest: ' + stat(sl.rest));
  console.log('   the root-mean-square pressure over the thunder: ' + stat(sl.rms));
}
if (require.main === module) {
  console.log('Each made-up stroke is heard from ' + xs.join(', ') + ' m along the ground from where it struck.\n');
  run('AS THE PAGE HAS IT (the air, and the bending of sound)', N, 100, {}, {});
  run('WITHOUT THE BENDING OF SOUND', N, 100, {}, { bend: 0 });
  run('WITHOUT THE BENDING OR THE AIR', N, 100, {}, { bend: 0, air: 0 });
  console.log('\nOne step off in the crookedness (as the page has it otherwise):');
  for (const k of [0, 8, 32]) run('mean turn ' + k + ' degrees between 3 m pieces', 30, 100, { kink: k }, {});
  console.log('\nThe same three without the bending of sound (the referee\'s figures were of this kind):');
  for (const k of [0, 8, 32]) run('mean turn ' + k + ' degrees, no bending', 30, 100, { kink: k }, { bend: 0 });
  // a straight stroke, smooth, against the same line made crooked ten ways
  console.log('\nA smooth straight stroke 5 km tall, against the same line made crooked ten ways (as the page has it):');
  const line = [[0, 5000], [0, 0]], smooth = TH.resample(line, 3);
  for (const x of [1000, 2000, 3000, 4000, 5000, 6000, 8000, 9000]) {
    const r = TH.thunder(smooth, [x, 0]); let a = 0, b = 0; const i1 = Math.round((r.first + 0.02 - r.t0) * r.fs);
    for (let k = 0; k < r.p.length; k++) { const v = r.p[k] * r.p[k]; b += v; if (k < i1) a += v; }
    const pk = [], en = []; for (let sd = 1; sd <= 10; sd++) { const c = TH.thunder(TH.jag(line, 500 + sd), [x, 0]); pk.push(c.peak); en.push(c.energy); }
    console.log('   from ' + x + ' m: the smooth one peaks at ' + r.peak.toFixed(5) + ', with ' + (100 * a / b).toFixed(1) + '% of its energy in the first fiftieth of a second; the crooked ones peak at ' + Math.min(...pk).toFixed(5) + ' to ' + Math.max(...pk).toFixed(5)
      + ' (the smooth one above ' + pk.filter(v => r.peak > v).length + ' of 10) and have ' + (en.reduce((u, v) => u + v) / 10 / r.energy).toFixed(1) + ' times its energy on average');
  }
}

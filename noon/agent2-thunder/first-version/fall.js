// How does the loudest moment of the thunder fall off with distance, for made-up strokes?
// A straight channel gives the square root of one over the distance; a single point gives one over the distance.
// usage: node fall.js [strokes]
const TH = require('./core.js');
const N = +process.argv[2] || 60, xs = [500, 1000, 2000, 4000, 8000];
function slope(x, y) { const n = x.length, mx = x.reduce((a, b) => a + b) / n, my = y.reduce((a, b) => a + b) / n; let sxy = 0, sxx = 0; for (let i = 0; i < n; i++) { sxy += (x[i] - mx) * (y[i] - my); sxx += (x[i] - mx) * (x[i] - mx); } return sxy / sxx; }
const lx = xs.map(Math.log), out = { air: [], dry: [], rms: [] }, mean = xs.map(() => 0), dur = xs.map(() => 0);
for (let s = 1; s <= N; s++) {
  const pts = TH.stroke(100 + s), pk = [], pd = [], rm = [];
  xs.forEach((x, i) => { const r = TH.thunder(pts, [x, 0]); pk.push(Math.log(r.peak)); let m = 0; for (let k = 0; k < r.dry.length; k++) m = Math.max(m, Math.abs(r.dry[k])); pd.push(Math.log(m));
    rm.push(0.5 * Math.log(r.energy / (r.last - r.first))); mean[i] += r.peak / N; dur[i] += (r.last - r.first) / N; });
  out.air.push(slope(lx, pk)); out.dry.push(slope(lx, pd)); out.rms.push(slope(lx, rm));
}
const stat = v => { const m = v.reduce((a, b) => a + b) / v.length, sd = Math.sqrt(v.reduce((a, b) => a + (b - m) * (b - m), 0) / (v.length - 1)); return m.toFixed(2) + ' (from ' + Math.min(...v).toFixed(2) + ' to ' + Math.max(...v).toFixed(2) + '; spread ' + sd.toFixed(2) + ', so the mean is good to about ' + (sd / Math.sqrt(v.length)).toFixed(2) + ')'; };
console.log(N + ' made-up strokes (seeds 101 on), each heard from ' + xs.join(', ') + ' m along the ground from where it struck');
console.log('mean peak at those distances: ' + mean.map(v => v.toFixed(4)).join(', ') + '; mean length of the thunder: ' + dur.map(v => v.toFixed(1)).join(', ') + ' s');
console.log('the peak falls as the distance to the power: with the air ' + stat(out.air));
console.log('                                              without it ' + stat(out.dry));
console.log('the root-mean-square pressure over the thunder falls as the power: ' + stat(out.rms));

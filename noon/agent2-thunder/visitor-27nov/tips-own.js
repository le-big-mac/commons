// My own count of two things the referee's third check found (27 November).   node tips-own.js CORE.JS
// 1. Of made-up strokes, how many have their loudest moment "in the middle" (between a tenth and nine tenths of the thunder), place by place?
// 2. The smooth straight stroke: crack, click from the far end, largest pressure between, and the energy after the crack's first fiftieth of a second.
const TH = require(require('path').resolve(process.argv[2]));
const places = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9700];
{ const N = 60, row = [], first = [], rate = [];
  for (const L of places) { let mid = 0, early = 0, lo = 9, hi = 0;
    for (let seed = 1001; seed < 1001 + N; seed++) { const r = TH.thunder(TH.stroke(seed), [L, 0]); if (r.firstHeard === null) continue;
      const f = (r.tpeak - r.firstHeard) / (r.last - r.firstHeard); if (f > 0.1 && f < 0.9) mid++; if (f <= 0.1) early++;
      const k = r.firstHeard / (L / 1000); lo = Math.min(lo, k); hi = Math.max(hi, k); }
    row.push(mid); first.push(early); rate.push(lo.toFixed(2) + '-' + hi.toFixed(2)); }
  console.log('listener (m)            ' + places.join('  '));
  console.log('in the middle, of ' + N + ':   ' + row.join('    '));
  console.log('in the first tenth:      ' + first.join('    '));
  console.log('s per km to first sound: ' + rate.join(' ')); }
{ console.log('\nthe smooth straight stroke, 5 km tall, foot at 0');
  for (const L of [0, 300, 500, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 9000, 9700]) {
    const r = TH.thunder(TH.resample([[0, 5000], [0, 0]], TH.STEP), [L, 0]), n = r.p.length, fs = r.fs || 44100;
    const i1 = Math.round((r.first + 0.02 - r.t0) * fs), i2 = n - Math.round(0.03 * fs); let click = 0, mid = 0, e = 0, eAfter = 0;
    for (let i = 0; i < n; i++) { const a = Math.abs(r.p[i]); e += a * a; if (i >= i1) eAfter += a * a; if (i >= i2) click = Math.max(click, a); else if (i >= i1) mid = Math.max(mid, a); }
    console.log(String(L).padStart(5) + ' m: crack ' + r.peak.toExponential(3) + ', click ' + click.toExponential(3) + ' (crack/' + (r.peak / click).toFixed(2) + '), largest between ' + mid.toExponential(3) + ' (crack/' + (r.peak / mid).toFixed(1) + '), energy after the first fiftieth of a second ' + (100 * eAfter / e).toFixed(2) + '%, loudest ' + (1000 * (r.tpeak - r.first)).toFixed(1) + ' ms after the first sound'); } }

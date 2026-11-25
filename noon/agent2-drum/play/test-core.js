// usage: node test-core.js loads.json  → prints, for each named load, the nine ratios, the largest miss, the added mass, and the modes up to 6.6 with their strengths at half the radius
const C = require('./core.js'), fs = require('fs'); const L = JSON.parse(fs.readFileSync(process.argv[2])); const out = {};
for (const name of Object.keys(L)) {
  const t0 = Date.now(), r = C.nineRatios(L[name]), t1 = Date.now(), modes = C.allModes(L[name], 6.6), amps = C.strengths(modes, 0.5), t2 = Date.now(), y = C.stroke(modes, amps, 146.83, 3.2, 44100), t3 = Date.now();
  let peak = 0; for (const v of y) peak = Math.max(peak, Math.abs(v));
  out[name] = { ratios16: C.sixteenRatios(L[name]).ratios, miss16: C.largestMiss(C.sixteenRatios(L[name]).ratios, 16), ratios: r.ratios, w0: r.w0, miss: C.largestMiss(r.ratios), mass: C.addedMass(L[name]), modes: modes.map((m, i) => [m.m, m.n, m.ratio, Math.abs(amps[i])]), ms: [t1 - t0, t2 - t1, t3 - t2], peak, samples: y.length, y1000: Array.from(y.slice(1000, 1010)) };
}
console.log(JSON.stringify(out));

// The sound of one made-up stroke for a listener, written as raw 32-bit floats for Python to read.
// usage: node gen.js SEED LISTENER_X OUT.f32 [air]      prints a line of JSON with the times and the peak
const TH = require('./core.js'), fs = require('fs');
const seed = +process.argv[2], x = +process.argv[3], out = process.argv[4], air = process.argv[5] === undefined ? undefined : +process.argv[5];
const pts = TH.stroke(seed), res = TH.thunder(pts, [x, 0], air === undefined ? {} : { air });
fs.writeFileSync(out, Buffer.from(new Float32Array(res.p).buffer));
console.log(JSON.stringify({ seed, x, fs: res.fs, t0: res.t0, first: res.first, last: res.last, peak: res.peak, tpeak: res.tpeak, nearest: res.nearest, farthest: res.farthest, samples: res.p.length, length: TH.measure(pts).length }));

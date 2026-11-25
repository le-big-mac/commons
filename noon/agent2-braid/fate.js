// fate.js -- a long run of the page's bed: what becomes of the braids?  Prints the measures every 100,000 steps, keeps the bed
// at 600,000 steps and at the end, and a picture of the water at four times and the bed at the end.
//   usage: node fate.js STEPS 'KL=0.4,seed=1' NAME
const { Bed } = require('./core.js'); const png = require('./png.js'); const fs = require('fs');
const steps = +process.argv[2], extra = Object.fromEntries((process.argv[3] || '').split(',').filter(Boolean).map(kv => { const [k, v] = kv.split('='); return [k, +v]; })), name = process.argv[4];
const b = new Bed(Object.assign({ NX: 64, NY: 256, FEED: 1, NOISE: 3, CS: 0.05, KL: 0.4, seed: 1 }, extra)); const t0 = Date.now(), Z = 3;
const W = b.NY * Z, H1 = b.NX * Z + 4, strips = 5, rgb = new Uint8Array(W * H1 * strips * 3).fill(40);
function strip(k, f) { for (let y = 0; y < b.NX * Z; y++) for (let x = 0; x < W; x++) { const c = f(Math.floor(x / Z), Math.floor(y / Z)), o = ((k * H1 + y) * W + x) * 3; rgb[o] = c[0]; rgb[o + 1] = c[1]; rgb[o + 2] = c[2]; } }
function water(j, i) { const q = b.Q[j * b.NX + i] / b.total, v = Math.min(1, Math.sqrt(q / 0.25)); return q < 0.0035 ? [196, 178, 140] : [Math.round(150 - 130 * v), Math.round(185 - 110 * v), Math.round(215 - 60 * v)]; }
function bed(j, i) { let m = 0; for (let k = 0; k < b.NX; k++) m += b.h[j * b.NX + k]; m /= b.NX; const v = Math.max(0, Math.min(255, 128 + 20 * (b.h[j * b.NX + i] - m) / b.SLOPE)); return [v, v, v]; }
let k = 0;
for (let s = 1; s <= steps; s++) {
  b.step();
  if (s % 100000 === 0) { const br = b.braiding(); console.log(`step ${s}: time ${b.time.toExponential(2)}; streams ${br.streams.toFixed(1)}, wet ${(100 * br.wet).toFixed(0)}%, fullest cell ${(100 * br.top).toFixed(0)}% of the water, relief ${br.relief.toFixed(2)} row-falls`); }
  if (s === 600000) fs.writeFileSync(name + '-600k.bed', Buffer.from(b.h.buffer.slice(0)));
  if (s % Math.floor(steps / 4) === 0) strip(k++, water);
}
strip(4, bed); png.write(name + '.png', W, H1 * strips, rgb); fs.writeFileSync(name + '-end.bed', Buffer.from(b.h.buffer));
console.log(`${steps} steps in ${Date.now() - t0} ms`);

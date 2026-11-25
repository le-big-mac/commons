// try.js -- run the bed and write one picture: strips of the water at four times, then the bed at the end (flow runs left to right).
//   usage: node try.js STEPS 'JSON options' NAME [SCALE]      (the options may also be given as NX=48,NY=200,...)
const { Bed } = require('./core.js'); const png = require('./png.js');
const steps = +process.argv[2], a3 = process.argv[3] || '{}', opt = a3[0] === '{' ? JSON.parse(a3) : Object.fromEntries(a3.split(',').map(kv => { const [k, v] = kv.split('='); return [k, +v]; })), name = process.argv[4] || 'try', Z = +(process.argv[5] || 2);
const b = new Bed(Object.assign({ seed: 1 }, opt)); const t0 = Date.now();
const W = b.NY * Z, H1 = b.NX * Z + 4, strips = 5, rgb = new Uint8Array(W * H1 * strips * 3).fill(40);
function strip(k, f) { for (let y = 0; y < b.NX * Z; y++) for (let x = 0; x < W; x++) { const c = f(Math.floor(x / Z), Math.floor(y / Z)), o = ((k * H1 + y) * W + x) * 3; rgb[o] = c[0]; rgb[o + 1] = c[1]; rgb[o + 2] = c[2]; } }
function water(j, i) { const q = b.Q[j * b.NX + i] / b.total, v = Math.min(1, Math.sqrt(q / 0.25)); return q < 0.0035 ? [196, 178, 140] : [Math.round(150 - 130 * v), Math.round(185 - 110 * v), Math.round(215 - 60 * v)]; }
function bed(j, i) { let m = 0; for (let k = 0; k < b.NX; k++) m += b.h[j * b.NX + k]; m /= b.NX; const v = Math.max(0, Math.min(255, 128 + 20 * (b.h[j * b.NX + i] - m) / b.SLOPE)); return [v, v, v]; }
let k = 0;
for (let s = 1; s <= steps; s++) { b.step(); if (s % Math.floor(steps / (steps >= 1e6 ? 16 : 8)) === 0) { const br = b.braiding();
  console.log(`step ${s}: time ${b.time.toExponential(2)}; streams ${br.streams.toFixed(1)}, wet ${(100 * br.wet).toFixed(0)}%, fullest cell ${(100 * br.top).toFixed(0)}% of the water, relief ${br.relief.toFixed(2)} row-falls`); if (s % Math.floor(steps / 4) === 0) strip(k++, water); } }
strip(4, bed); png.write(name + '.png', W, H1 * strips, rgb);
require('fs').writeFileSync(name + '.bed', Buffer.from(b.h.buffer));   // the bed at the end, as raw 64-bit floats
console.log(`${steps} steps in ${Date.now() - t0} ms`);

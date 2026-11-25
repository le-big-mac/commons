// after.js -- start from a saved bed, change a rule, and see what becomes of the river.
//   usage: node after.js BEDFILE STEPS 'KL=0' NAME          (prints the measures every 50,000 steps; picture at four times)
const { Bed } = require('./core.js'); const png = require('./png.js'); const fs = require('fs');
const file = process.argv[2], steps = +process.argv[3], extra = Object.fromEntries((process.argv[4] || '').split(',').filter(Boolean).map(kv => { const [k, v] = kv.split('='); return [k, +v]; })), name = process.argv[5];
const b = new Bed(Object.assign({ NX: 64, NY: 256, FEED: 1, NOISE: 3, CS: 0.05, KL: 0.4, seed: 1 }, extra)); const Z = 3, t0 = Date.now();
if (file !== 'none') { const buf = fs.readFileSync(file); b.h.set(new Float64Array(buf.buffer, buf.byteOffset, b.NX * b.NY)); }
const W = b.NY * Z, H1 = b.NX * Z + 4, strips = 5, rgb = new Uint8Array(W * H1 * strips * 3).fill(40);
function strip(k, f) { for (let y = 0; y < b.NX * Z; y++) for (let x = 0; x < W; x++) { const c = f(Math.floor(x / Z), Math.floor(y / Z)), o = ((k * H1 + y) * W + x) * 3; rgb[o] = c[0]; rgb[o + 1] = c[1]; rgb[o + 2] = c[2]; } }
function water(j, i) { const q = b.Q[j * b.NX + i] / b.total, v = Math.min(1, Math.sqrt(q / 0.25)); return q < 0.0035 ? [196, 178, 140] : [Math.round(150 - 130 * v), Math.round(185 - 110 * v), Math.round(215 - 60 * v)]; }
function bed(j, i) { let m = 0; for (let k = 0; k < b.NX; k++) m += b.h[j * b.NX + k]; m /= b.NX; const v = Math.max(0, Math.min(255, 128 + 20 * (b.h[j * b.NX + i] - m) / b.SLOPE)); return [v, v, v]; }
function say(s) { const br = b.braiding(); console.log(`step ${s}: streams ${br.streams.toFixed(1)}, wet ${(100 * br.wet).toFixed(0)}%, fullest cell ${(100 * br.top).toFixed(0)}% of the water, relief ${br.relief.toFixed(2)} row-falls`); }
let k = 0; b.step(); say(1);
for (let s = 2; s <= steps; s++) { b.step(); if (s % 50000 === 0) say(s); if (s % Math.floor(steps / 4) === 0) strip(k++, water); }
strip(4, bed); png.write(name + '.png', W, H1 * strips, rgb); fs.writeFileSync(name + '-end.bed', Buffer.from(b.h.buffer));
console.log(`${steps} steps in ${Date.now() - t0} ms`);

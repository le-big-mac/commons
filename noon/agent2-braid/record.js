// record.js -- the page's "one line across the river, through time", made here: from a saved bed, the water along row JR
// every EVERY steps, one upright strip each.   usage: node record.js BEDFILE STEPS EVERY NAME
const { Bed } = require('./core.js'); const png = require('./png.js'); const fs = require('fs');
const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8')), [file, steps, every, name] = [process.argv[2], +process.argv[3], +process.argv[4], process.argv[5]];
const b = new Bed(SET), buf = fs.readFileSync(file); b.h.set(new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * b.NX * b.NY)));
const JR = Math.floor(0.75 * b.NY), n = Math.floor(steps / every), Z = 2, W = n * Z, H = b.NX * Z, rgb = new Uint8Array(W * H * 3);
for (let k = 0; k < n; k++) { for (let s = 0; s < every; s++) b.step();
  for (let i = 0; i < b.NX; i++) { const c = JR * b.NX + i, w = b.Q[c] / b.total; let col;
    if (w > 0.0035) { const v = Math.min(1, Math.sqrt(w / 0.25)); col = [150 - 130 * v, 185 - 110 * v, 215 - 60 * v]; }
    else { let s = 0.93 + 0.02 * (b.h[c] - b.SLOPE * (b.NY - 1 - JR)) / b.SLOPE; s = Math.max(0.78, Math.min(1.1, s)); col = [196 * s, 178 * s, 140 * s]; }
    for (let y = 0; y < Z; y++) for (let x = 0; x < Z; x++) { const o = ((i * Z + y) * W + k * Z + x) * 3; rgb[o] = col[0]; rgb[o + 1] = col[1]; rgb[o + 2] = col[2]; } } }
png.write(name + '.png', W, H, rgb); console.log(`${n} strips, ${every} steps apart`);

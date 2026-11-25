// supply.js -- sand in at the head against sand out at the foot, and how far the bed has been cut down, on saved beds.
//   usage: node supply.js BEDFILE [BEDFILE ...]        (the page's setting, fixed ends)
const { Bed } = require('./core.js'); const fs = require('fs');
const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8'));
for (const file of process.argv.slice(2)) {
  const b = new Bed(SET), buf = fs.readFileSync(file); b.h.set(new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * b.NX * b.NY)));
  b.step(true); let head = 0; for (let i = 0; i < b.NX; i++) head -= b.dh[i];
  const fresh = new Bed(Object.assign({}, SET, { NOISE: 0 })); fresh.step(true); let head0 = 0; for (let i = 0; i < fresh.NX; i++) head0 -= fresh.dh[i];
  function cut(j0, j1) { let wsum = 0, hsum = 0, all = 0; for (let j = j0; j < j1; j++) for (let i = 0; i < b.NX; i++) { const c = j * b.NX + i, d = (b.h[c] - b.SLOPE * (b.NY - 1 - j)) / b.SLOPE; all += d; wsum += b.Q[c]; hsum += b.Q[c] * d; } return [hsum / wsum, all / ((j1 - j0) * b.NX)]; }
  const parts = [[1, 9], [32, 64], [112, 144], [192, 224], [246, 255]].map(([a, z]) => { const [w, m] = cut(a, z); return `rows ${a}-${z - 1}: where the water is ${w.toFixed(1)}, all cells ${m.toFixed(1)}`; });
  console.log(`${file}: sand in at the head ${head.toExponential(2)} a unit of time (a smooth sheet gives ${head0.toExponential(2)}: ${(head / head0).toFixed(1)} times that); out at the foot ${b.gone.toExponential(2)}; out/in ${(b.gone / head).toFixed(2)}`);
  console.log('   height above the starting slope, in row-falls: ' + parts.join('; '));
}

// uphill.js -- how much of the water uses the rule for cells with no way down?  On saved beds: the share of wet cells (rows 1
// to NY-2) none of whose three downstream neighbours is lower, and the share of all cell-to-cell passings of water they make.
//   usage: node uphill.js BEDFILE [BEDFILE ...]
const { Bed } = require('./core.js'); const fs = require('fs');
const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8'));
for (const file of process.argv.slice(2)) {
  const b = new Bed(SET), buf = fs.readFileSync(file); b.h.set(new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * b.NX * b.NY)));
  b.step(true); let cells = 0, up = 0, water = 0, upwater = 0; const NX = b.NX, h = b.h;
  for (let j = 1; j < b.NY - 1; j++) for (let i = 0; i < NX; i++) { const c = j * NX + i, q = b.Q[c]; if (q <= 0) continue;
    const down = (i > 0 && h[c] > h[c + NX - 1]) || h[c] > h[c + NX] || (i < NX - 1 && h[c] > h[c + NX + 1]);
    cells++; water += q; if (!down) { up++; upwater += q; } }
  console.log(`${file}: ${cells} cells with water in rows 1 to ${b.NY - 2}; ${up} of them (${(100 * up / cells).toFixed(1)}%) have no way down, and they pass on ${(100 * upwater / water).toFixed(1)}% of the water that is passed`);
}

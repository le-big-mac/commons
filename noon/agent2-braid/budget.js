// budget.js -- has a bed gained sand or lost it, and where?  On saved beds: the mean height of the bed above its starting slope
// (rows 1 to NY-2), the same by quarters of the length from head to foot, and the lowest cell.  In row-falls.
//   usage: node budget.js BEDFILE [BEDFILE ...]        (added after the referee, who did this sum first)
const fs = require('fs'); const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8')), NX = SET.NX, NY = SET.NY, S = 0.05;
for (const file of process.argv.slice(2)) {
  const buf = fs.readFileSync(file), h = new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * NX * NY));
  let all = 0, n = 0, low = Infinity; const q = [0, 0, 0, 0], qn = [0, 0, 0, 0];
  for (let j = 1; j < NY - 1; j++) for (let i = 0; i < NX; i++) { const d = (h[j * NX + i] - S * (NY - 1 - j)) / S; all += d; n++; if (d < low) low = d; const k = Math.min(3, Math.floor(4 * j / NY)); q[k] += d; qn[k]++; }
  console.log(`${file}: mean height above the start ${(all / n).toFixed(2)}; by quarters from the head ${q.map((x, k) => (x / qn[k]).toFixed(1)).join(', ')}; lowest cell ${low.toFixed(1)}`);
}

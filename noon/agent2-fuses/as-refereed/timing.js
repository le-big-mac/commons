// timing.js -- how long the three successor procedures take on a grid (a timing run made BEFORE the sealed sheet; it
// covers only [0, 3/2] at steps of 1/256 and reports times and counts of distinct arguments, not agreement)
const F = require('./core.js'), fs = require('fs'); const f = new F.Fusible(); const t0 = Date.now(); let n = 0;
for (let k = 0; k <= 384; k++) { const r = F.D(k, 8); f.succ(r); f.tameSucc(r); f.meekSucc(r); n++; }
fs.writeSync(1, `${n} grid points in [0, 3/2] at steps of 1/256: ${Date.now() - t0} ms; distinct arguments ${JSON.stringify(f.calls)}\n`);

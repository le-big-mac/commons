// row-time2.js -- a row of 1000 columns with Fusible.column.  node row-time2.js CENTRE P BUDGET
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
const c = F.parse(process.argv[2]), p = +process.argv[3], budget = +process.argv[4], px = F.D(1, p);
const f = new F.Fusible(); f.maxDepth = +(process.argv[5] || 1e9); let t0 = Date.now(), a = F.sub(c, F.D(500, p)), n = [0, 0, 0, 0, 0], worst = 0;
for (let i = 0; i < 1000; i++) { const t = Date.now(); n[f.columnMemo(a, p, budget)]++; worst = Math.max(worst, Date.now() - t); a = F.add(a, px); }
say(`centre ${process.argv[2]}, pixel 2^-${p}, budget ${budget}: none ${n[0]}, tame ${n[1]}, wild only ${n[2]}, fusible ${n[3]}, not worked out ${n[4]}; ${Date.now() - t0} ms, worst column ${worst} ms; memory ${f.mKM.count()} + ${f.mM.count()}`);

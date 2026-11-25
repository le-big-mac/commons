// row-time.js -- how long does a row of 1000 columns take?  node row-time.js CENTRE P [BUDGET]   (pixel = 2^-P, centre as a fraction)
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
const c = F.parse(process.argv[2]), p = +process.argv[3], budget = +(process.argv[4] || 0), px = F.D(1, p), eta = F.D(1, p + 20);
const f = new F.Fusible(); let t0 = Date.now(), left = F.sub(c, F.D(500, p)), has = 0, tame = 0, over = 0, a = F.sub(left, eta), worst = 0;
for (let i = 0; i < 1000; i++) { const b = F.add(a, px), t = Date.now(), m = f.meekM(a, budget), mt = f.M(a, budget); worst = Math.max(worst, Date.now() - t);
  if (m === null) over++; else if (F.cmp(F.add(a, m), b) < 0) has++; if (mt !== null && F.cmp(F.add(a, mt), b) < 0) tame++; a = b; }
say(`centre ${process.argv[2]}, pixel 2^-${p}, budget ${budget || 'none'}: ${has} columns with a meek number, ${tame} with a tame one, ${over} over budget; ${Date.now() - t0} ms in all, worst column ${worst} ms; memory ${f.mKM.count()} + ${f.mM.count()} answers`);

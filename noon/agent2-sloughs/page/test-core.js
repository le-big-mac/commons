// test-core.js -- core.js against river.c: the same seed must give the same river, through its first cutoffs.
// usage: node test-core.js   (run from ~/meander/page; needs ../river, built from ../river.c)
const { River } = require('./core.js');
const { execFileSync } = require('child_process');
const cases = [[3, 0.4, 40, 30, 7], [3, 0.2, 40, 26, 8], [2, 0.8, 40, 80, 11], [4.5, 0.4, 30, 13, 12], [6, 0.8, 30, 8, 14]];
let bad = 0, cuts = 0;
for (const [P, DC, LX, T, seed] of cases) {
  const out = execFileSync('../river', [P, DC, LX, T, seed, '-out', '1'].map(String), { encoding: 'utf8' });
  const rows = out.split('\n').filter(l => l && !l.startsWith('#')).map(l => l.split(/\s+/));
  const r = new River({ P, DC, LX }); r.seed(seed);
  let ok = rows.length === T + 1, worst = 0, k = 0, nextout = 0;
  for (;;) {
    if (r.now >= nextout - 1e-9) {
      const s = r.sinuosity(), row = rows[k++];
      if (!row || Number(row[1]) !== r.N || Number(row[3]) !== r.ncut) ok = false;
      else { const d = Math.abs(Number(row[2]) - s); worst = Math.max(worst, d); if (d > 2e-5 || Math.abs(Number(row[4]) - r.cutlen) > 0.01) ok = false; }
      nextout += 1;
    }
    if (r.now >= T - 1e-9) break;
    r.step();
  }
  cuts += r.ncut; bad += ok ? 0 : 1;
  console.log(`P=${P} dc=${DC} LX=${LX} seed=${seed}: ${k} rows, ${r.ncut} cutoffs, greatest difference in length/LX ${worst.toExponential(1)}  ${ok ? 'agree' : 'DIFFER'}`);
}
console.log(`${cases.length - bad} of ${cases.length} cases agree; cutoffs covered: ${cuts}`);
process.exit(bad ? 1 : 0);

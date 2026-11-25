// landmarks.js -- the table of gaps for the page: after each named number, how far to the next by the tame rule (M), by the
// meek rule, and by the proved procedure (Algorithm 1) where it was run.   node --stack-size=60000 landmarks.js > landmarks.json
const F = require('./core.js'); const rows = [];
const alg1 = { '0': 1, '1/2': 1, '1': 1, '3/2': 1, '2': 1, '33/16': 1, '9/4': 1, '19/8': 1, '39/16': 1 };       // where Algorithm 1 is run here (a second each, 39/16 twenty)
for (const s of ['0', '1/2', '1', '3/2', '2', '33/16', '9/4', '19/8', '39/16', '5/2', '11/4', '23/8', '3']) {
  const r = F.parse(s), f = new F.Fusible(), row = { r: s };
  if (s !== '3') { const m = f.M(r); if (m[0] !== 1n) throw new Error('M not a power of two at ' + s); row.tame = m[1]; }
  if (s !== '3' && s !== '23/8') { const m = f.meekM(r); if (m[0] !== 1n) throw new Error('meekM'); row.meek = m[1]; }
  if (alg1[s]) { const g = F.sub(f.succ(r), r); if (g[0] !== 1n) throw new Error('succ'); row.proved = g[1]; }
  rows.push(row);
}
process.stdout.write(JSON.stringify(rows, null, 1) + '\n');

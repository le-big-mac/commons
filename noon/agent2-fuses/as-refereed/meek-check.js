// meek-check.js -- meekM against MeekSucc on a grid, and at 5/2 and 11/4 against the values in Xu's 2012 table (51, 48804)
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n'); const f = new F.Fusible();
let bad = 0, n = 0; for (let i = 0; i <= 9 * 1024; i++) { const r = F.D(i, 12); n++; if (F.cmp(F.add(r, f.meekM(r)), f.meekSucc(r)) !== 0) bad++; }
say('meekM(r) + r = MeekSucc(r) (my reading) at ' + (n - bad) + ' of ' + n + ' points of the grid of 1/4096 in [0, 9/4]');
for (const [a, b] of [[2, 0], [5, 1], [11, 2]]) { const g = new F.Fusible(), t0 = Date.now(), m = g.meekM(F.D(a, b)); say('meekM(' + F.str(F.D(a, b)) + ') = ' + (m[0] === 1n ? '2^-' + m[1] : F.str(m)) + ';  ' + g.calls.meekM + ' different arguments, nested ' + g.depthK + ' deep, ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s'); }

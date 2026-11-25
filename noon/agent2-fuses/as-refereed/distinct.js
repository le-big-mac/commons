// distinct.js -- of the arguments Algorithm 1 is asked about going up a grid, how many different answers are there?
const F = require('./core.js'), fs = require('fs'); const E = +process.argv[2], a = +process.argv[3], b = +process.argv[4];
const f = new F.Fusible(); for (let i = a; i <= b; i++) f.succ(F.D(i, E));
const ans = new Set(); let n = 0; for (const m of f.mS.maps) for (const v of m.values()) { n++; ans.add(F.key(v)); }
fs.writeSync(1, `grid 1/2^${E}, ${a}..${b}: ${n} arguments, ${ans.size} different answers\n`);

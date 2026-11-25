// time-succ.js -- how long each procedure takes going up a grid.  usage: node time-succ.js E FROM TO WHICH   (FROM, TO in units of 1/2^E)
const F = require('./core.js'), fs = require('fs'); const E = +process.argv[2], a = +process.argv[3], b = +process.argv[4], which = process.argv[5] || 'succ';
const f = new F.Fusible(), t0 = Date.now(); let last = t0;
for (let i = a; i <= b; i++) { const r = F.D(i, E); f[which](r); const now = Date.now(); if (now - last > 3000 || i === b) { fs.writeSync(1, F.str(r) + '  ' + ((now - t0) / 1000).toFixed(1) + ' s  calls ' + JSON.stringify(f.calls) + '\n'); last = now; } }

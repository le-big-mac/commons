// quarter.js -- is z + 1/4 fusible when z is?  (Asked because a broken copy of the picture's rule, looking a quarter of a
// unit below instead of a half, passed every test.)  By the second procedure, over the grid of 1/16384 up to 1.85.
const F = require('./core.js'), fs = require('fs'), f = new F.Fusible();
for (const [num, e, lab] of [[1, 2, '1/4'], [1, 3, '1/8'], [3, 3, '3/8'], [1, 1, '1/2'], [3, 2, '3/4']]) { let n = 0, yes = 0; const no = [];
  for (let i = 0; i <= 1.85 * 16384; i++) { const z = F.D(i, 14); if (!f.isFusible(z)) continue; n++; if (f.isFusible(F.add(z, F.D(num, e)))) yes++; else no.push(F.str(z)); }
  fs.writeSync(1, 'of the ' + n + ' fusible numbers z on the grid of 1/16384 up to 1.85, z + ' + lab + ' is fusible for ' + yes + (no.length ? '; not for ' + (no.length <= 4 ? no.join(', ') : no.slice(0, 3).join(', ') + ', ... , ' + no[no.length - 1] + ' (' + no.length + ' in all, the largest below 1)') : '') + '\n'); }

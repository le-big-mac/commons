// beside.js -- a broken copy that passed the tests, run beside the true program: where do they differ?
//   node --stack-size=20000 beside.js mutants/NAME.js     (the grid of 1/16384 below 35/16; 3,000 random dyadics below 2.18;
//   for the picture's rule, 3,000 random columns from 3 to 3.6 with widths 2^-8 to 2^-30)
const A = require('./core.js'), B = require('./' + process.argv[2]), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
const fa = new A.Fusible(), fb = new B.Fusible(); let seed = 99; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
let n = 0, ds = [], dw = [];
const one = r => { n++; if (A.cmp(fa.succ(r), fb.succ(r)) !== 0) ds.push(A.str(r)); if (A.cmp(fa.weakSucc(r), fb.weakSucc(r)) !== 0) dw.push(A.str(r)); };
for (let i = 0; i < 35 * 1024; i++) one(A.D(i, 14));
for (let i = 0; i < 3000; i++) { const e = 1 + Math.floor(rnd() * 24); one(A.D(Math.floor(rnd() * 2.18 * Math.pow(2, e)), e)); }
let nc = 0, dc = [], kinds = {};
for (let i = 0; i < 3000; i++) { const p = 8 + Math.floor(rnd() * 23), a = A.D(Math.floor((3 + rnd() * 0.6) * Math.pow(2, p)), p), x = fa.column(a, p, 20000), y = fb.column(a, p, 20000); nc++; if (x !== y) { dc.push(A.str(a) + ' p=' + p); kinds[x + '->' + y] = (kinds[x + '->' + y] || 0) + 1; } }
say(process.argv[2] + ': of ' + n + ' numbers, the first procedure differs at ' + ds.length + (ds.length ? ' (first ' + ds[0] + ')' : '') + ', the third at ' + dw.length + (dw.length ? ' (first ' + dw[0] + ')' : '') + '; of ' + nc + ' columns from 3 up, the picture differs at ' + dc.length + (dc.length ? ' ' + JSON.stringify(kinds) : ''));

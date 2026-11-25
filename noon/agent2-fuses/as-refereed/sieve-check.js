// sieve-check.js -- the paper's Algorithms 2 and 1 against the sieve on a whole grid.   node sieve-check.js K TOP [CORE]
// Algorithm 2 must call fusible exactly the grid numbers the sieve made (if it calls one fusible that the sieve did not
// make, that is either a fault or a number needing off-grid operands: listed).  Algorithm 1's successor of each grid point
// must not be greater than the next number the sieve made, and when it lies on the grid it must be that number.
const sieve = require('./sieve.js'), F = require(process.argv[4] || './core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
const K = +process.argv[2], top = Math.floor(eval(process.argv[3]) * (1 << K)), t0 = Date.now(), s = sieve(K, top), f = new F.Fusible();
let miss = [], extra = [], nf = 0; for (let i = 0; i < top; i++) { const is = f.isFusible(F.D(i, K)); if (is) nf++; if (s.has[i] && !is) miss.push(i + '/' + (1 << K)); if (!s.has[i] && is) extra.push(i + '/' + (1 << K)); }
say(`grid of 1/2^${K} below ${process.argv[3]} (${top} points): the sieve made ${s.list.length}; Algorithm 2 calls ${nf} fusible; made but not called fusible: ${miss.length}${miss.length ? ' ' + miss.slice(0, 5).join(' ') : ''}; called fusible but not made: ${extra.length}${extra.length ? ' ' + extra.slice(0, 5).join(' ') : ''}  (${((Date.now() - t0) / 1000).toFixed(1)} s)`);
let above = [], offgrid = 0, same = 0, differ = [], wildSame = 0, j = 0, n = 0;
for (let i = 0; i < top; i++) { while (j < s.list.length && s.list[j] <= i) j++; if (j >= s.list.length) break; n++; const r = F.D(i, K), z = f.succ(r), g = F.D(s.list[j], K), c = F.cmp(z, g);
  if (c > 0) above.push(F.str(r)); else if (z[1] > K) offgrid++; else if (c === 0) { same++; if (F.cmp(z, f.tameSucc(r)) !== 0) wildSame++; } else differ.push(F.str(r)); }
say(`Algorithm 1 at the ${n} grid points with a made number above them: successor greater than the sieve's next number at ${above.length}${above.length ? ' ' + above.slice(0, 5).join(' ') : ''}; on the grid and equal to it at ${same} (${wildSame} of them where the tame successor is another number); on the grid and less than it at ${differ.length}${differ.length ? ' ' + differ.slice(0, 5).join(' ') : ''}; off the grid (finer than 1/2^${K}) and below it at ${offgrid}  (${((Date.now() - t0) / 1000).toFixed(1)} s)`);
process.exit(miss.length || extra.length || above.length || differ.length ? 1 : 0);

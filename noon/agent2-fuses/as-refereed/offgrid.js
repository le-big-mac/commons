// offgrid.js -- sealed line 7 one step off its grid: the sixth procedure (my reading) against the first at random dyadics
// with denominators up to 2^24, and on the grid of 1/16384 below 35/16; and how the procedure AS PRINTED fares below 2.
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n'); const f = new F.Fusible();
let seed = 4242; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
let n = 0, same = 0, wild = 0, t0 = Date.now();
for (let i = 0; i < 4000; i++) { const e = 1 + Math.floor(rnd() * 24), r = F.D(Math.floor(rnd() * 2.15 * Math.pow(2, e)), e), s = f.succ(r), k = f.meekSucc(r); n++; if (F.cmp(s, k) === 0) same++; if (F.cmp(s, f.tameSucc(r)) !== 0) wild++; }
say(`4000 random dyadics in [0, 2.15) with denominators 2^1 to 2^24: the sixth procedure (my reading) = the first at ${same} of ${n} (${wild} of them where the tame successor is another number); ${((Date.now() - t0) / 1000).toFixed(1)} s`);
n = 0; same = 0; wild = 0; t0 = Date.now();
for (let i = 0; i < 35 * 1024; i++) { const r = F.D(i, 14), s = f.succ(r), k = f.meekSucc(r); n++; if (F.cmp(s, k) === 0) same++; if (F.cmp(s, f.tameSucc(r)) !== 0) wild++; }
say(`the grid of 1/16384 in [0, 35/16): the same at ${same} of ${n} (${wild} where the tame successor is another number); ${((Date.now() - t0) / 1000).toFixed(1)} s`);
// as printed: right, wrong, or not greater than its input, at each point of the grid of 1/256 in [0, 2)
let right = 0, wrong = 0, notGreater = 0, firstBad = null;
for (let i = 0; i < 512; i++) { const r = F.D(i, 8), g = new F.Fusible(); let z = null; try { z = g.meekSucc(r, true); } catch (e) { z = null; }
  if (z === null) { notGreater++; if (!firstBad) firstBad = r; } else if (F.cmp(z, f.succ(r)) === 0) right++; else { wrong++; if (!firstBad) firstBad = r; } }
say(`as printed, on the grid of 1/256 in [0, 2) (512 points): the true successor at ${right}, another number at ${wrong}, stopped because some call returned a number not greater than its input at ${notGreater}; the first point that is not right: ${F.str(firstBad)}`);

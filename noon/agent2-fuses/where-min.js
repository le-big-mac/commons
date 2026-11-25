// where-min.js -- in Algorithm 1's loop, at which pass is the least x ~ y found, and how far below r is its y?
// usage: node where-min.js K FROM TO    (grid of 1/2^K, FROM and TO as fractions)
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
const K = +process.argv[2], a = Math.floor(eval(process.argv[3]) * (1 << K)), b = Math.floor(eval(process.argv[4]) * (1 << K));
const f = new F.Fusible(); let comps = 0, passes = 0, firstPass = 0, maxPasses = 0, far = F.ZERO, farAt = null, laterWins = 0, hist = {};
f.succ = function (r) {                                         // the same procedure as core.js, counting
  if (r[0] < 0n) return F.ZERO; const got = this.gS.get(r); if (got) return got; comps++;
  let min = null, y = r, x, z, n = 0, at = 0, aty = null; const r2 = F.dbl(r), lim = F.sub(r, F.HALF);
  do { x = this.succ(F.sub(F.sub(r2, y), F.UNIT)); y = this.succ(F.sub(F.sub(r2, x), F.UNIT)); z = F.fuse(x, y); n++;
    if (min === null || F.cmp(z, min) < 0) { min = z; at = n; aty = y; }
    y = F.sub(y, F.ulp(y)); } while (F.cmp(y, lim) > 0);
  passes += n; if (n > maxPasses) maxPasses = n; if (at === 1) firstPass++; else { laterWins++; hist[at] = (hist[at] || 0) + 1; }
  const d = F.sub(r, aty); if (at > 1 && F.cmp(d, far) > 0) { far = d; farAt = r; }
  this.gS.set(r, min); return min; };
for (let i = a; i < b; i++) f.succ(F.D(i, K));
say(`grid of 1/2^${K} in [${process.argv[3]}, ${process.argv[4]}): ${comps} computations (the grid points and all they called for), ${passes} passes of the loop in all, at most ${maxPasses} in one;`);
say(`the least x ~ y was found at the first pass in ${firstPass}, at a later pass in ${laterWins}; passes at which it was found, when later: ${JSON.stringify(hist)};`);
say(farAt === null ? 'it was never found at a later pass; the loop runs down to r - 1/2' : `when it was found at a later pass, the y of the least pair was never further below r than ${F.str(far)} = ${F.num(far).toFixed(6)} (at r = ${F.str(farAt)}); the loop runs down to r - 1/2`);

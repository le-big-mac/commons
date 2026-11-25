// runM.js -- M at 3 - 2^-(n-1): the exponent of the answer, how many different arguments M was asked for, how deep the calls
// nested.   usage: node runM.js N SECONDS        (N = 3 means 11/4; stops with "not finished" after SECONDS)
const F = require('./core.js'), fs = require('fs'); const n = +process.argv[2], limit = +process.argv[3] * 1000;
const r = F.sub(F.D(3, 0), F.D(1, n - 1)), f = new F.Fusible(), t0 = Date.now();
const timer = setTimeout(() => {}, 0); let c = 2; const cs = [2]; for (let k = 1; k < n; k++) { c = 1 + (k + 1) * c; cs.push(c); } let d = n + 9; for (let k = 1; k < n; k++) d += (k + 3) * cs[k];
// a watchdog inside the loop: M checks nothing itself, so run it in slices by throwing from a counter
const origSet = f.mM.set.bind(f.mM); let count = 0; f.mM.set = function (k, v) { if ((++count & 4095) === 0 && Date.now() - t0 > limit) throw new Error('time'); return origSet(k, v); };
let out; try { const m = f.M(r); out = (m[0] === 1n ? '2^-' + m[1] : F.str(m)) + (m[0] === 1n && m[1] === d ? '   = the formula\'s 2^-' + d : '   NOT the formula\'s 2^-' + d); } catch (e) { out = 'not finished in ' + process.argv[3] + ' s (the formula says 2^-' + d + ')'; }
fs.writeSync(1, `M(${F.str(r)}) = ${out};  ${f.calls.m} different arguments, calls nested ${f.depthM} deep, ${((Date.now() - t0) / 1000).toFixed(1)} s\n`);
